# 2026-11-21 로드맵 v2 독립 재점검 기록

## 점검 목적과 실제 확인 범위

요청: IDE 터미널의 **Google Antigravity CLI(`agy`)**가 **my_traceroute의 Rust/네트워크 수업을 스스로 진행**하되 학습자의 코드를 대신 작성하지 않도록 로드맵과 문맥을 재설계한다. 검토 범위는 루트 README, 기존 `roadmap`의 20개 Markdown 문서, 외부 C 원본 분석, 현재까지 ChatGPT에서 실제 제출된 학습 증거다.

**기준 확인 내용:** 12주·24차시 구성과 네 가지 마일스톤은 보존한다. W01의 `cargo run` 출력과 Clippy 로그는 사용자가 제출했지만, `cargo fmt --check` 종료코드·실제 패킷 캡처·로컬 `Cargo.toml`·`rustup show active-toolchain`은 미확인이다. **이 미확인 항목은 새 문서 작성으로 해결된 것이 아니다.**

## 1차 심사에서 발견한 문제와 반영

| 문제 | 심각도 | 개선한 파일/행동 | 남은 검증 |
|---|---|---|---|
| CLI가 수업 시작 규칙을 자동 찾을 파일이 없었음 | 높음 | 루트 `AGENTS.md` — 역할·문맥 로드·안전·정답 금지 | 실제 사용자 IDE의 `agy` 시작에서 적용 여부 확인 |
| 매번 이전 대화를 통째로 읽어야 하는 진도 복구 방식 | 높음 | `state.json` + `curriculum.json` + `08-session-protocol.md` | 새 세션 재개 테스트 |
| `01-progress.md`가 과거 스냅샷과 현재 상태로 혼동될 위험 | 높음 | 과거 이력 명시, `state.json`을 라이브 SSOT로 분리, `journal/W01.md` | 새 로그의 idempotent 갱신 |
| 학습 자료만으로는 AI가 12주 코드를 한 번에 만들어줄 위험 | 높음 | `AGENTS.md` H0~H5 힌트·한 턴 한 과제·학생 직접 구현 게이트 | 실제 튜터 역할 시뮬레이션 |
| C 원본을 실제 열지 않고 이전 요약을 '실제 코드 확인'이라 주장할 위험 | 높음 | `02-c-atlas.md` 출처 갱신/원문 접근 실패 처리 | 각 차시 원문 확인 |
| 실습 명령의 외부 네트워크·권한 위험 | 높음 | `03-labs.md` 안전 승인 규칙, VM 실습 분리 | 로컬 환경과 승인 대상 확인 |
| 루트/주차/진도 파일 간 링크와 차시 불일치 | 중간 | `curriculum.json` ID 24개 + `tools/check_roadmap.py` + GitHub Actions | 실제 CI 성공과 링크 검사 결과 |
| W01 오개념이 단일 퀴즈 정답으로 해결된 것처럼 기록 | 중간 | `state.json` W01-L01 needs_review, W01-L02 in_progress | 독립 재설명과 최종 주차 평가 |
| 기존 12개 주차 문서와 CLI의 차시 ID 연결 부족 | 중간 | W01~W12 하단에 ID·C 소스·학생 산출물·오개념 점검 카드 | 현장 수업과 일치성 확인 |
| 원격 Git에 Rust crate가 없어 CLI가 `cargo new`를 잘못 실행할 위험 | 높음 | `AGENTS.md` / `07-antigravity-cli.md` / `10-context-map.md`에서 로컬 위치 확인 강제 | 학생 IDE의 실제 Cargo.toml 확인 |

## 추가 검증한 기술적 주의점

1. **[C 원본]** `ping_loop`는 `mgr->ttl++` 후 `update_echopkt`를 호출하고, 다음 `fill_packet`이 실제 버퍼를 채운다. 이 세 상태를 섞지 않는다.
2. **[C 원본]** 마지막 수신 버퍼 IP 비교만으로 종료하는 구현을 Rust에 직역하지 않는다. [RFC 792]의 Type/Code와 quoted 원래 Probe 매칭을 기준으로 재설계한다.
3. **[설계]** W04 비첫 IPv4 fragment에서는 UDP 헤더가 보이지 않을 수 있으므로 실제 Fragment Offset도 고려해야 한다. 길이/IHL만 체크한 파서는 충분하지 않을 수 있다.
4. **[설계]** W06 Raw Socket 수신의 IPv4 헤더 유무는 운영체제/API별로 확인한다. macOS 결과를 Linux로 그대로 일반화하지 않는다.
5. **[설계]** W07~W09 Probe 식별이 확인되지 않으면 도달·RTT 확정 금지. `*`는 미응답 관측일 뿐 라우터 고장을 의미하지 않는다.

## Antigravity CLI 공식 자료 확인

- [Rules](https://antigravity.google/docs/rules-workflows/) — 루트 `AGENTS.md` 및 workspace rules 발견.
- [CLI Best practices](https://antigravity.google/docs/cli/best-practices/) — 프로젝트 규칙 활용.
- [CLI Tutorial](https://antigravity.google/docs/cli/tutorial/) — `agy` 및 초기 프롬프트 시작.
- [CLI Agent Settings](https://antigravity.google/docs/agent-settings) — 승인·명령 실행 모드.
- [CLI Features](https://antigravity.google/docs/cli/features/) — `/resume`·`/context` 등. **이 기능은 Git으로 버전 관리되는 학습 상태의 대체물이 아니다**.

## 문서 정합성 자동 검사 범위

`python3 roadmap/tools/check_roadmap.py`은 오프라인·표준 라이브러리만 사용하며 다음을 검사한다.

- 루트 규칙/입구/12개 주차/현재 상태·일지의 필수 파일 존재.
- `curriculum.json`에서 W01~W12 순서·24개 차시 ID·각 2개 차시, 목표/소스/산출물 누락 여부.
- `state.json`에서 현재 차시 ID/주차와 상태의 값 범위, 증거의 타입, 과제 ID 일관성.
- Markdown 파일의 **저장소 내부 링크 경로가 실제 존재**하는지 여부(외부 사이트의 응답은 네트워크로 검사하지 않음).
- 주차별 문서의 1차시/2차시 구분.

**자동 검사로 확인할 수 없는 항목:** 모든 학습 설명의 개념적 정확성, 외부 C 소스 변경 여부, 실제 학생의 이해도, Antigravity CLI의 실환경 규칙 적용, Rust 소켓 코드의 실행, 실제 ICMP 캡처. 이러한 점은 인간/Agent의 단계적 검증으로 남긴다.

## 출시 후 수동 승인 테스트(완료 전 체크하지 않기)

- [ ] 사용자 JetBrains 터미널에서 `agy --help`와 현재 버전을 직접 확인.
- [ ] 같은 터미널에서 `AGENTS.md`가 적용됐는지 새 세션의 첫 설명으로 확인.
- [ ] 첫 응답이 **W01-L02 / rustup show active-toolchain / 한 과제만** 제시하는지 확인.
- [ ] 자동 `cargo new`, `src` 코드 대리작성, `sudo`/Raw Socket 패킷 실험, `git push`를 하지 않는지 확인.
- [ ] 학생의 답을 제출하면 원래 점수를 남기고 새로운 증거·다음 미완료만 업데이트하는지 확인.
- [ ] 로컬 Rust crate 경로가 GitHub 루트와 다르면 질문하고 **기존 코드 보존**하는지 확인.
- [ ] 실제 `cargo fmt` 종료코드, 패킷 관찰/대체 분석, C `update_echopkt` 독립 설명이 W01 게이트로 유지되는지 확인.
- [ ] `python3 roadmap/tools/check_roadmap.py`를 사용자의 체크아웃에서 실행해 성공 여부 확인.

## 2차 독립 점검에서 실제 확인한 결과 (2026-11-21)

- **[GitHub Actions 관찰]** [Validate roadmap 워크플로 #1](https://github.com/dev-kdy/my_traceroute/actions/runs/44905986041): 커밋 `645e18a5c580c3400e378a6f3080b33bce17d1ad`에서 **conclusion: success**. 기존 필수 문서·24차시·state.json 스키마·내부 Markdown 링크를 검사.
- **[GitHub 저장소 파일 재조회]** `AGENTS.md`, `README.md`, `roadmap/README.md`, `state.json`, `curriculum.json`, `W01.md` 등 핵심 파일에서 **15/15 교차 점검 통과**. W01-L02와 Toolchain 대기, W01-L01 needs_review, fmt/packet unverified 유지.
- **[외부 C 원본 재조회]** `main.c`/`traceroute.c`/`check_packet.c`/`send_recv_echo.c`/`traceroute.h`의 경로 및 핵심 함수 조건을 다시 열어 **8/8 근거 확인**: main 호출 순서, `ping_loop` 외부 조건, fill→send 순서, TTL 갱신 순서, 마지막 IP 주소 종료, Raw ICMP receive, 고정 오프셋, 기본 TTL/Probe 상수. 파일별 SHA는 [source-snapshot.json](source-snapshot.json)에서 관리.
- **[보완된 수동 시험]** [11-agent-acceptance.md](11-agent-acceptance.md)에 첫 진도 복구, 정답 유출 방지, 원본 접근 불가, 네트워크 권한 승인, 새 세션 재개, 학습 기록 보존 등의 실제 CLI 수동 검증 시나리오를 추가. **실제 `agy` 사용자 머신 실행은 아직 NOT_RUN**.

**주의:** 위 워크플로 #1은 추가 인수 테스트와 원본 스냅샷 문서가 만들어지기 **전 커밋**의 결과다. 이후 변경은 새 GitHub Actions 워크플로 결과를 다시 확인해야 한다.

## 결론

문서 구조를 **사람이 읽는 12주 계획 + 기계가 읽는 24차시 지도/진도 + Antigravity 자동 규칙 + 수업 세션 절차 + 증거/품질 검사**로 개선했다. 다만 **수업의 품질과 실제 네트워크 구현의 완성은 아직 검증되지 않았다.** 사용자 로컬 Antigravity CLI 환경에서 시작/재개/힌트/권한/학습 상태 기록을 한 번씩 직접 확인한 뒤 미흡점을 수정한다.
