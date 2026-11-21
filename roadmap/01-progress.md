# 학습 진행 원장 — 2026-11-21 기준

> **인계 당시의 역사적 스냅샷(2026-11-21).** Antigravity CLI가 현재 진도를 읽을 때의 **변경 가능한 단일 기준은 [state.json](state.json)**이다. 이 문서는 ChatGPT 대화에서 사용자 제출 내용을 옮긴 근거이고, 새 실습이 진행되더라도 소급하여 합격 기록으로 수정하지 않는다. 추가 사건은 [journal/W01.md](journal/W01.md)에 기록한다. [실습 프로토콜](08-session-protocol.md)을 따른다.

**상태: W01 진행 중 / W02 시작 금지.** 현재 사용자의 대화와 원격 GitHub 구조에서 확인한 것만 기록한다. 단순 진도 체크와 실제 테스트 통과는 별도다.

## 재개 지점

- 마지막 수업: **Phase 2 — Toolchain/Rust 개발 환경**의 첫 실습 `rustup show active-toolchain` 요청 직후.
- 다음 한 가지 과제: 위 명령의 실행 결과와 `rustc`(컴파일러) vs `rustup`(툴체인 관리자) 차이 설명.
- 그다음 남은 W01 학습: Cargo 구조, `Cargo.toml` Edition 확인, `let/mut/const/String/&str/함수/반복/조건`, C 전체 실행 흐름, 시뮬레이터 소과제, macOS 실제/대체 패킷 관찰, 주간 평가.
- 사용자 보고 환경: macOS Apple Silicon, JetBrains 계열 IDE, Rust 1.100.0, Cargo 1.100.0.
- **중요:** 원격 GitHub `main`에서 확인되는 파일은 `README.md`, `LICENSE`뿐. 로컬 `Cargo.toml`/`src/main.rs`/`Cargo.lock`은 원격에서 확인되지 않았다.

## 학습한 코드·개념

직접 제출한 기존 `main.rs`에는 `START_TTL: u8=1`, `MAX_TTL: u8=3`, `PROBES_PER_HOP: u8=3`, `fn print_probe(ttl,probe)`, 이중 `for` 반복, 목적지 문자열 출력과 종료 문구가 있다. `let mut domain`을 `let domain = String::from("example.com")`으로 고친 코드를 사용자가 직접 답했다.

학습한 네트워크 키워드: IP, Router, Hop, TTL, Probe, ICMP Time Exceeded, UDP Port Unreachable, traceroute 개념. Rust: `const`, `fn`, `println!`, `for`, `1..=3`, 중첩 반복, macro/함수 차이, 불변성.

## 검증 상태: 증거와 판정 분리

| 항목 | 대화에 제출된 사실 | 판정 |
|---|---|---|
| `rustc --version` | `rustc 1.100.0 (0ef1bc386 2026-11-09)` | 보고된 버전 확인 |
| `cargo --version` | `cargo 1.100.0 (3acc79c0c 2026-11-05)` | 보고된 버전 확인 |
| `cargo run` | `example.com`, TTL 1·2·3 각각 probe 1·2·3, 종료 출력 제출 | **출력 동작 일치**. 빌드 로그/종료코드는 미제출 |
| `cargo fmt --check` | 명령 호출 표시, 오류 메시지 없음 | **종료 코드 미확인**; 성공 단정 불가 |
| `cargo clippy -- -D warnings` | `Checking my_traceroute v0.1.0` → `Finished dev profile`, 경고 없음 | 로그상 정상 완료; 종료코드는 미제출 |
| `cargo test` | 로그 미제출 | 미검증 |
| `Cargo.toml`의 `edition` | 파일 미제출 | 미확인; 2024로 임의 확정 금지 |
| `rustup show active-toolchain` | 미제출 | 미검증 |
| 시스템 `traceroute`와 pcap | 미제출 | 미관찰 |
| 실제 UDP/ICMP Rust 구현 | 아직 없음(초기 시뮬레이터만 제출됨) | 미구현 |
| 원격 Rust crate 커밋 | 원격 `main`에 해당 파일 없음 | GitHub 반영 미확인 |

## 확인 문제와 오개념 원장

| W01-L01 문제 | 학습자 최초 답변 | 피드백/보충 |
|---|---|---|
| `const` vs `let mut` | 증가하는 TTL은 `let mut` | 본질 맞음. 불변 기준 상수와 상태 변수를 구분 |
| TTL=1의 운명 | 첫 라우터에서 0이 되어 drop, ICMP 오류 | 개념 맞음; 정식 이름 **Time Exceeded Type 11/Code 0** 추가 필요 |
| `*`의 의미 | 설정된 시간 동안 응답 없음 | 관측 설명 맞음; **장애·실패를 확정할 수 없음** 보충 |
| C `mgr->ttl++` 이후 `update_echopkt` | 처음 모름; 추가 대화에서 'ttl 값이 줄어들지 않는다' | 발신 프로그램의 TTL 증가 vs 라우터의 감소를 구분하는 보충 시행. 이유를 독립 재설명할지 재평가 필요 |

최초 4문항 진단 점수는 튜터가 **55/100**으로 제시했다. 이 수치는 보충 전 점수이므로 **수료 점수와 동일하지 않음**. 이후 `패킷 헤더 TTL=1이면 어느 라우터에서 폐기되는가`에는 **첫 번째 라우터**라고 올바르게 답했다. 단일 답변으로 `update_echopkt` 내부 동작 전체를 숙달했다고 판정하지 않는다.

## W01에서 빠진 증거

- [ ] `cargo fmt --check; echo $?`에서 종료 코드 0 확인.
- [ ] `rustup show active-toolchain` 및 `Cargo.toml` 출력 제출.
- [ ] `while`/`loop`/`if`/반환값 실습을 학습자가 직접 작성.
- [ ] `main.c` → `traceroute.c`의 **모든 분기/호출** 포함한 상태 흐름 설명.
- [ ] TTL, Probe, ICMP Type/Code, `*`, RTT를 실제 traceroute 또는 통제된 대체 실험으로 설명.
- [ ] W01 마지막 4문항 독립 응답 및 1주차 통합 과제 검토.
- [ ] 코드의 GitHub 커밋 여부 학습자가 확인(이 문서에서 자동으로 커밋하지 않음).

## 기록 갱신 방법

날짜·파일 경로·커밋·명령·stdout/stderr·exit code·pcap·내 설명을 남긴 뒤 체크박스를 바꾼다. 실패/오답을 삭제하지 않는다. 모든 Phase가 끝나기 전에는 W01을 '완료'로 표시하지 않는다. **1주차 미달 항목이 있다면 그 부분만 보충한다.**
