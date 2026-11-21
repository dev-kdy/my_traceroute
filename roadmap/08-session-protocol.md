# Antigravity 학습 세션 프로토콜

> **자동 문맥 로드:** 루트 [AGENTS.md](../AGENTS.md) → [state.json](state.json) → [curriculum.json](curriculum.json) → 현재 [주차 문서](weeks/W01.md). [01-progress.md](01-progress.md)는 과거 ChatGPT 대화 기록이며 현재 학습 상태를 자동 갱신하는 파일이 아니다.

## 1. 문맥 읽기 순서 (Progressive Disclosure)

1. `git rev-parse --show-toplevel`과 `git status --short`로 실제 작업 저장소/미커밋 변경을 확인. 사용자의 실제 Rust crate가 다른 경로라면 먼저 확인한다.
2. `AGENTS.md`, 루트 `README.md`, `roadmap/README.md`, `state.json`, `curriculum.json` 로드.
3. 지금 주차 `weeks/Wxx.md` **한 개만** 정독. 다른 11주 전체를 한 번에 컨텍스트로 넣지 않는다.
4. 최초 시작만 과거 `01-progress.md`를 보고 현재 실제 코드·로그와 대조. 이후에는 `roadmap/journal/`의 새 사건만 읽는다.
5. 개념·C·패킷·평가가 필요한 시점에만 `02-c-atlas.md`/`03-labs.md`/`04-assessment.md`/관련 원본·RFC를 추가 읽는다.
6. 원문 C 파일을 접근할 수 없다면 **원문을 보았다고 말하지 않는다**. 문서에 요약된 내용과 직접 열어 확인한 사실을 구분한다.

## 2. 상태와 증거의 의미

차시/주차 상태는 `not_started` / `in_progress` / `needs_review` / `passed` / `blocked`. 증거 상태는 `unverified` / `user_reported` / `agent_observed`.

- `unverified`: 명령을 기록만 하거나 결과·종료코드·응답이 없다.
- `user_reported`: 학생이 실행 출력/코드/답변을 제공했지만 이번 CLI에서 실행 확인하지 않았다. **제출된 내용만큼만 인정**.
- `agent_observed`: 현재 워크스페이스 파일/명령/캡처를 도구로 직접 확인함. 원본 위치/명령/결과/시각 기록.
- **통과는 증거+설명+주차 게이트**로 결정. `cargo` 명령 한 개 성공은 주차 완료가 아니다.
- 오답 최초 점수는 지우지 않고 보충·새 문제 결과를 별도 기록한다.

## 3. 한 턴 한 과제 상태 기계

| 단계 | AI가 할 일 | 학생이 할 일 | STOP 조건 |
|---|---|---|---|
| BOOTSTRAP | 지금 위치/확인/미확인/다음 한 과제만 요약 | 로컬 crate가 맞는지 확인 | 경로 충돌 시 질문 |
| TEACH | Rust 최대 두 개·네트워크 한 개, C **전체 함수 지도**와 Java 비교 | 예측 답변 | 소스 미확인 시 사실 구분 |
| TASK | H0 입력·출력·경계 테스트 조건 **하나만** | 자신의 Rust 코드 또는 답변 작성 | **응답을 기다림** |
| REVIEW | 최초 오류 **하나**와 H1 질문 | 코드 수정·이유 설명 | 다음 과제 선공개 금지 |
| VALIDATE | 명령/코드/pcap의 실제 증거를 구분 | 로그와 결과 제시 | 승인 없는 네트워크 명령 금지 |
| ASSESS | Rust 1·네트워크 2·C/Rust 1문항 출제(정답 숨김) | 4문항 직접 답 | 정답 제출 전 공개 금지 |
| CHECKPOINT | 모든 Exit Gate 확인, 미완료와 다음 행동 정리 | 기록·커밋 승인 여부 결정 | 미달이면 다음 주차 시작 금지 |
| PAUSE | 학생의 다음 입력 대기 | 직접 실습 | 자동 이어서 구현 금지 |

### 과제 카드 형식

```text
ID: Wxx-Lyy-Tzz
이번 한 가지 목표:
선수 개념/지금 C 원본 출처:
입력과 기존 함수:
기대 동작(정답 코드 공개 없이):
경계 또는 실패 사례:
학생이 작성할 범위:
실행/제출할 증거:
힌트 단계: H0
정지 조건: 답변 제출까지 대기
```

## 4. 오답/힌트/정답 선공개 방지

H0 요구사항·테스트 → H1 사고 질문 → H2 의사코드 → H3 짧은 주석 포함 문법 예시 → H4 요청한 부분 함수 → H5 명시적으로 요청한 전체 풀이. **완성 구현이 공개되었다면 이를 독립 구현 성취로 판정하지 않는다.** 한 번에 하나의 오류 원인만 짚고 새로운 반례로 확인한다.

## 5. 상태 파일 저장 절차

1. 학생이 제출한 코드·실행 출력·퀴즈 답 또는 CLI의 실제 관찰을 분리 기록.
2. `state.json`에서 **해당 차시/증거 항목만** 수정할 변경 내용을 학생에게 제시.
3. 학생이 저장을 승인한 후 `state.json`과 해당 `journal/Wxx.md`를 업데이트. 이전 기록/첫 시도 점수 삭제 금지.
4. `python3 roadmap/tools/check_roadmap.py`로 구조/링크/차시 개수 검사. 오류가 있으면 상태 갱신을 완료로 주장하지 않는다.
5. 원격 Git `commit`/`push`는 별도의 명시적 승인 요구. **학습 상태 기록과 코딩 산출물 수정은 분리**.
6. 실행 가능한 파일(`src/`, `Cargo.toml`)은 학생이 직접 편집. 요청 없이 에이전트가 작성·수정하지 않는다.

## 6. 누락된 증거를 처리하는 방법

- `cargo fmt --check` 명령만 보임 → 종료코드 `unverified`.
- `cargo clippy` 완료 로그만 있음 → `user_reported`, 종료코드까지 있다고 주장 금지.
- `Cargo.toml`을 실제 읽어 `edition` 확인 → `agent_observed`.
- 캡처에서 ICMP Type/Code만 확인 → 메시지 종류 관찰만 통과. **Quoted Probe 매칭은 별도**.
- rustc가 사용자의 머신이 아닌 Agent의 격리 환경에서 실행됨 → 그 환경을 명시하고 사용자 로컬 통과와 분리.

## 7. 다음 대화에서도 이어지는 재개 테스트

새 Antigravity CLI 세션을 시작한 뒤 에이전트에게 `state.json`과 현재 주차 문서를 열도록 요청. 에이전트가 (a) 현 W01-L02 (b) `rustup show active-toolchain` 미제출 (c) `cargo fmt` 종료코드 미확인 (d) C `update_echopkt` 독립 설명 보충 필요 (e) 아직 GitHub 원격 Rust crate 확인되지 않음을 각각 구별하면 초기 문맥 복원 성공.

이 중 하나가 틀리면 임의 진도 이동 금지. `state.json`/실제 소스를 다시 읽고 교정한다. **목표는 대화 이력 흉내가 아니라 정확한 역량 성장을 입증하는 것**이다.
