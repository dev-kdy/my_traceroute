#!/usr/bin/env python3
"""Validate my_traceroute's lesson map, state and internal Markdown links.

Runs without third-party libraries, network access, Cargo or administrator rights.
It intentionally does NOT grade students or execute packet experiments.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
ROADMAP = ROOT / "roadmap"
ALLOWED_LESSON = {"not_started", "in_progress", "needs_review", "passed", "blocked"}
ALLOWED_EVIDENCE = {"unverified", "user_reported", "agent_observed"}
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    """Append each failure while continuing the rest of the audit."""
    if not condition:
        errors.append(message)


def read_json(path: Path) -> dict:
    """Read structured files without silently ignoring malformed content."""
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        check(isinstance(obj, dict), f"{path}: expected a JSON object")
        return obj if isinstance(obj, dict) else {}
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: cannot parse JSON: {exc}")
        return {}


def check_local_links(path: Path) -> None:
    """Check repository-local Markdown links; external URLs are not fetched."""
    source = path.read_text(encoding="utf-8")
    for raw in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", source):
        url = raw.strip().split(' "')[0]
        if url.startswith("#"):
            continue
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            continue
        if not parsed.path or parsed.path.startswith("mailto:"):
            continue
        relative = unquote(parsed.path)
        destination = (path.parent / relative).resolve()
        try:
            destination.relative_to(ROOT)
        except ValueError:
            check(False, f"{path.relative_to(ROOT)}: link leaves repo: {raw}")
            continue
        check(destination.exists(), f"{path.relative_to(ROOT)}: missing link: {raw}")


def main() -> int:
    """Perform a read-only repository integrity check."""
    required = [
        "README.md",
        "AGENTS.md",
        "roadmap/README.md",
        "roadmap/00-method.md",
        "roadmap/01-progress.md",
        "roadmap/02-c-atlas.md",
        "roadmap/03-labs.md",
        "roadmap/04-assessment.md",
        "roadmap/05-templates.md",
        "roadmap/06-references.md",
        "roadmap/07-antigravity-cli.md",
        "roadmap/08-session-protocol.md",
        "roadmap/09-review-report.md",
        "roadmap/11-agent-acceptance.md",
        "roadmap/10-context-map.md",
        "roadmap/curriculum.json",
        "roadmap/state.json",
        "roadmap/source-snapshot.json",
        "roadmap/journal/W01.md",
    ] + [f"roadmap/weeks/W{i:02d}.md" for i in range(1, 13)]
    for relative in required:
        check((ROOT / relative).is_file(), f"missing required file: {relative}")

    course = read_json(ROADMAP / "curriculum.json")
    state = read_json(ROADMAP / "state.json")
    snapshot = read_json(ROADMAP / "source-snapshot.json")
    source_files = snapshot.get("files", {})
    check(snapshot.get("upstream") == "Dauie/traceroute", "source snapshot: unknown upstream")
    check(isinstance(source_files, dict) and len(source_files) >= 9, "source snapshot: expected at least 9 C source fingerprints")
    if isinstance(source_files, dict):
        for source_path, sha in source_files.items():
            check(source_path.startswith(("src/", "incl/")), f"source snapshot: invalid path {source_path}")
            check(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha) is not None,
                  f"source snapshot: invalid SHA for {source_path}")
    weeks = course.get("weeks", [])
    check(isinstance(weeks, list) and len(weeks) == 12, "curriculum must have 12 weeks")
    check(course.get("lessons_total") == 24, "curriculum lessons_total must be 24")
    lesson_ids: list[str] = []

    for index in range(1, 13):
        expected_week = f"W{index:02d}"
        week = weeks[index - 1] if isinstance(weeks, list) and len(weeks) >= index else {}
        check(isinstance(week, dict), f"{expected_week}: expected object")
        if not isinstance(week, dict):
            continue
        check(week.get("id") == expected_week, f"{expected_week}: wrong id or ordering")
        document = week.get("document")
        check(document == f"roadmap/weeks/{expected_week}.md", f"{expected_week}: wrong document")
        lessons = week.get("lessons", [])
        check(isinstance(lessons, list) and len(lessons) == 2, f"{expected_week}: exactly 2 lessons required")
        if not isinstance(lessons, list):
            continue
        for n, lesson in enumerate(lessons, start=1):
            lid = f"{expected_week}-L{n:02d}"
            if not isinstance(lesson, dict):
                errors.append(f"{lid}: expected object")
                continue
            check(lesson.get("id") == lid, f"{lid}: incorrect ID")
            lesson_ids.append(lid)
            for key in ("title", "network_topic", "task_outcome"):
                check(isinstance(lesson.get(key), str) and bool(lesson.get(key)), f"{lid}: missing {key}")
            for key in ("rust_topics", "c_sources"):
                check(isinstance(lesson.get(key), list) and bool(lesson.get(key)), f"{lid}: missing {key}")
            for source in lesson.get("c_sources", []) if isinstance(lesson.get("c_sources"), list) else []:
                check(isinstance(source, str) and source.startswith(("src/", "incl/")), f"{lid}: invalid C source {source}")
                if isinstance(source, str) and "*" not in source and isinstance(source_files, dict):
                    check(source in source_files, f"{lid}: C source missing from snapshot: {source}")
        path = ROOT / f"roadmap/weeks/{expected_week}.md"
        if path.is_file():
            body = path.read_text(encoding="utf-8")
            check("1차시" in body and "2차시" in body, f"{expected_week}: both lesson headings required")

    check(len(set(lesson_ids)) == 24, "lesson IDs must be unique and cover 24 lessons")
    check(state.get("current_lesson") in lesson_ids, "state.current_lesson not in course")
    check(state.get("current_week") in [f"W{i:02d}" for i in range(1, 13)], "invalid current week")
    check(state.get("current_lesson", "").startswith(state.get("current_week", "INVALID")), "current week/lesson mismatch")
    for name, expected, allowed in [
        ("lesson_status", set(lesson_ids), ALLOWED_LESSON),
        ("week_status", {f"W{i:02d}" for i in range(1, 13)}, ALLOWED_LESSON),
    ]:
        values = state.get(name, {})
        check(isinstance(values, dict) and set(values) == expected, f"state {name}: missing or extra entries")
        if isinstance(values, dict):
            for key, status in values.items():
                check(status in allowed, f"state {name}.{key}: unknown status {status}")
    for evidence in state.get("evidence", []):
        if not isinstance(evidence, dict):
            errors.append("state: evidence entries must be objects")
            continue
        check(evidence.get("status") in ALLOWED_EVIDENCE, f"evidence {evidence.get('id')}: invalid status")
        check(evidence.get("lesson") in lesson_ids, f"evidence {evidence.get('id')}: unknown lesson")
    check(state.get("current_task", {}).get("id", "").startswith(state.get("current_lesson", "") + "-"), "current task/lesson mismatch")

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        check_local_links(path)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Roadmap check FAILED: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print("Roadmap check OK: 12 weeks, 24 lessons, state schema, required files and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
