# Antigravity CLI 학습 운영 가이드 (JetBrains IDE 터미널)

> **목적:** 매 수업 시작 시 동일한 학습 규칙과 **마지막 학습 상태**를 복원하고, 에이전트가 답을 대신 작성하거나 무단으로 실습 환경을 변경하지 않도록 운영한다. Google 공식 [CLI 시작하기](https://antigravity.google/docs/cli/tutorial/), [Rules](https://antigravity.google/docs/rules-workflows/), [Best Practices](https://antigravity.google/docs/cli/best-practices/) 확인을 기반으로 작성.

## 1. Antigravity CLI란?

Antigravity CLI는 터미널에서 사용하는 Google Antigravity 에이전트이다. **실행 파일은 `agy`**. 기존 `Gemini CLI`와 동일하다고 가정하지 않는다. 공식 문서의 프로젝트 규칙 후보는 루트 `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` 등이다. 이 저장소는 **루트 `AGENTS.md` 한 개**로 규칙을 연결한다. 중복된 규칙 파일을 여러 개 생성하여 우선순위 충돌·토큰 낭비를 만들지 않는다.

**중요한 구분:** IDE의 Antigravity 확장 프로그램과 **IDE 터미널에서 직접 실행한 `agy`**는 서로 다른 시작 경로다. 이 문서는 **터미널 CLI**를 기준으로 한다. 반드시 CLI를 **저장소 루트에서** 실행하여 해당 저장소의 루트 지침을 발견하도록 한다.

## 2. 설치 확인 및 첫 실행 (읽기 전용 준비)

JetBrains IDE의 Terminal에서 다음을 **직접** 확인한다.

```bash
pwd                               # 예상: 프로젝트 Git 루트 또는 그 하위
git rev-parse --show-toplevel      # 실제 Git 저장소 루트
git status --short                 # 미커밋 수정이 있는지 확인(무단 덮어쓰기 금지)
command -v agy                     # 설치된 CLI 경로(미설치 시 출력이 없을 수 있음)
agy --help                         # 사용 중인 CLI 버전의 명령을 공식 도움말과 대조
```

`agy`가 없으면 [공식 설치 안내](https://antigravity.google/docs/cli/getting-started/)를 따르되, 설치 스크립트 실행 전에 다운로드 소스와 동작을 검토한다. AI가 사용자 동의 없이 `curl | bash` 설치를 수행하지 않게 한다.

프로젝트 루트에서 실행:

```bash
agy
```

또는 공식 문서에서 설명하는 **초기 프롬프트 포함 인터랙티브 세션**:

```bash
agy -i "my_traceroute 학습을 이어가자. 루트 AGENTS.md를 따르고 roadmap/state.json 및 현재 주차 문서를 확인한 뒤 첫 미완료 과제 하나만 제시해."
```

실행 전 **실제 작업 디렉터리가 루트인지** 확인. 에이전트가 부모 디렉터리에서 실행되면 루트 `AGENTS.md` 자동 탐색/프로젝트 파일 인식이 기대와 달라질 수 있다.

## 3. 첫 화면에서 에이전트가 해야 하는 일

1. **읽기만:** `AGENTS.md` → `README.md` → `roadmap/README.md` → `roadmap/state.json` → `roadmap/curriculum.json`.
2. 이어서 **현재 주차** `roadmap/weeks/Wxx.md`와 `roadmap/01-progress.md`(과거 대화 인계)를 읽는다. 12개 주차 문서를 처음부터 모두 올리지 않는다.
3. `git status --short`, `Cargo.toml` 존재/Edition, rustc 설치 등은 **사용자의 실제 로컬 작업 디렉터리**에서 확인(필요한 안전한 읽기 명령만). 로컬 crate가 다른 경로라면 확인 질문.
4. '지금 Wxx-Lyy, 이 증거는 확인되었고 이것은 미확인, 다음에 직접 할 한 가지'를 한국어로 5~10문장 요약.
5. *첫 과제 한 개*를 제시하고 사용자 답변까지 대기. 다음 단계로 자동 진행 금지.

**현재 기준 첫 과제:** `rustup show active-toolchain` 출력과 `rustc` vs `rustup` 역할 설명. 앞선 학습의 `cargo fmt --check` 종료 코드는 여전히 확인 필요.

## 4. CLI 세션 / 파일 학습 상태는 다르다

- 공식 CLI에는 `/resume` 등 대화 세션 기능이 있지만, **세션 재개 가능성만을 진도의 SSOT로 사용하지 않는다**.
- 세션 기록이 사라지거나 새 터미널이 열려도 **Git에 저장된 `roadmap/state.json`** 및 주차별 과제/증거를 기준으로 학습을 이어간다.
- `roadmap/01-progress.md`는 이 ChatGPT 대화에서 옮긴 **이력 스냅샷**이다. 현재 로컬 파일의 진실을 우선한다.
- `roadmap/state.json`에는 진행 중 차시와 다음 과제, 통과/미확인 상태만 최소한으로 기록한다. 상세 오답·패킷 로그는 `roadmap/journal/` 또는 학습자의 Obsidian에 별도 보관.
- 진도를 변경할 때는 어떤 **사용자 응답/실제 명령 출력**이 근거인지 기록. "CLI가 그렇게 생각했다"는 증거가 아니다.

## 5. 권한 설정 및 안전한 행동

현재 버전의 CLI에는 작업 실행/승인 모드를 설정하는 기능이 있으므로 [공식 Agent Settings](https://antigravity.google/docs/agent-settings)와 현재 `agy --help`를 확인한다. **실습에서는 최소 권한·변경 전 확인**을 기본으로 한다. CLI 설정에서 자동 명령 승인 모드를 사용하더라도 교육상의 사전 승인 규칙을 생략해서는 안 된다.

- 읽기·탐색: `pwd`, `git status`, `cat`, `rg`, `rustc --version` 등은 통상 작은 위험.
- 코드 검사: `cargo check`/`cargo fmt --check`/`cargo clippy`/`cargo test`는 프로젝트의 빌드 스크립트/테스트에 따라 실행 코드·부작용이 있을 수 있다. 실행 전 소스 및 사용자 의도를 확인한다.
- 코드를 자동 수정하는 `cargo fmt`, 패키지 설치, `git add/commit/push`, `cargo new`, `rm`, `sudo tcpdump`, `ip route`, `ip netns`, Raw Socket 등은 **구체적 승인 이후**에만.
- 트레이스 대상은 반드시 본인/허가된 호스트. 허가가 불명확하면 네트워크 패킷 대신 오프라인 fixture 분석으로 바꾼다.
- 개인 IP/로컬 홈 경로·비밀·로그인 토큰/pcap을 학습 문서에 그대로 넣지 않는다.

## 6. 수업 중 권장 명령(대화 내부)

| 목적 | 에이전트에게 입력할 요청 |
|---|---|
| 현재 차시 이어가기 | `진도와 미완료 증거를 확인한 뒤 한 가지 실습부터 이어가자.` |
| 오답 보충 | `정답을 주지 말고 내가 놓친 개념을 힌트 H1로 질문해.` |
| 소스 독해 | `해당 C 함수를 실제 원본에서 확인하고 전체 분기/호출을 지도화해. 오늘 배울 부분만 깊게 설명해.` |
| 내 코드 리뷰 | `내가 작성한 코드를 읽고 가장 작은 오류부터 힌트를 하나만 줘. 자동 수정하지 마.` |
| 패킷 분석 | `내가 제출한 pcap의 TTL/Type/Code/quoted fields를 식별하고 아직 모르는 것은 추정으로 표시해.` |
| 기록 마무리 | `검증된 사실만 state.json과 journal에 반영할 변경안을 보여줘. 승인 후 파일을 수정해.` |

CLI의 `/resume`, `/context` 등은 [공식 Feature Overview](https://antigravity.google/docs/cli/features/) 참조. **가용 명령과 문법은 설치된 CLI 도움말이 최종 기준**이다.

## 7. 설정·호환성 문제가 생기면

- `AGENTS.md`가 적용되지 않은 것 같으면: `pwd`와 Git root 확인 → `agy`를 저장소 루트에서 실행 → 에이전트에게 *문서가 자동 로드되었는지 추정하지 말고* `AGENTS.md` 첫 세 줄을 요약하도록 요청.
- Agent가 전체 답안을 먼저 쓰면: `AGENTS.md`의 H0/H1 및 `roadmap/08-session-protocol.md`를 명시, 해당 응답을 학습자의 독립 구현으로 기록하지 않는다.
- 세션 기록이 사라져도 `roadmap/state.json`/`journal`에서 재개. `/resume` 없음을 이유로 W01부터 초기화하지 않는다.
- Rust 프로젝트가 GitHub 루트에 아직 없다면 현재 로컬 `Cargo.toml`을 찾고 **절대 자동 중첩 `cargo new` 하지 않는다**.
- `.agents/` 룰/`GEMINI.md`를 별도로 작성할 때에는 기존 루트 규칙과 충돌·중복 여부부터 검토한다.

## 8. 학습 튜터의 실제 동작 검사

[인수 테스트](11-agent-acceptance.md)의 A01(현 진도 복원), A04(기존 Cargo 보존), A05(완성 코드 금지), A09(재시작), S02(권한 승인), T01(C 원본 전체 흐름)를 사용자의 **실제 CLI**에서 확인한다. 문서 CI 성공만으로 이 테스트까지 성공한 것으로 기록하지 않는다.

## 8. 최초 수업용 복사 프롬프트

```text
이 저장소는 Rust 입문자용 my_traceroute 12주·24차시 학습이다.
AGENTS.md, roadmap/state.json, roadmap/curriculum.json, roadmap/01-progress.md,
현재 roadmap/weeks/Wxx.md, roadmap/08-session-protocol.md를 먼저 읽어.
내 실제 로컬 Cargo 프로젝트/현재 Git 상태를 확인하되 파일은 수정하지 마.
이번 대화에서는 한 번에 하나의 과제만 제시하고 내 답을 기다려.
완성 Rust 코드/퀴즈 정답을 먼저 공개하지 마.
지금 W01 2차시 Toolchain 명령 실습을 재개해. 1차시 미확인 항목도 보존해.
```
