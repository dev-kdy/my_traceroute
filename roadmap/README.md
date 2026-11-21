# my_traceroute — 12주·24차시 상세 학습 로드맵

> **수료 목표:** 외부 구현을 베끼지 않고 Rust로 IPv4 UDP traceroute와 ICMP Echo 모드를 스스로 설계·구현하고, 패킷 캡처와 테스트로 의미를 검증한다.

## CLI에서 학습하는 가장 빠른 경로

1. **루트 [AGENTS.md](../AGENTS.md)** — Antigravity가 자동 발견할 튜터 행동/권한 규칙.
2. **[Antigravity CLI 실행 가이드](07-antigravity-cli.md)** — JetBrains IDE 터미널의 `agy` 실행, 파일 문맥 로드, 안전한 사용법.
3. **[24차시 메타데이터](curriculum.json) + [현재 진도 SSOT](state.json)** — 이전 채팅에 의존하지 않고 재개.
4. **[수업 상태 기계](08-session-protocol.md) + [문맥 인덱스](10-context-map.md)** — 한 턴 한 과제·정답 금지·증거 갱신.
5. **[과거 대화 이력](01-progress.md) + [W01 기록](journal/W01.md)** — 이미 한 실습을 불필요하게 반복하지 않음.
6. **[자동 검사 스크립트](tools/check_roadmap.py) + [2차 점검 보고서](09-review-report.md)** — 문서 및 학습 상태 무결성 확인.

**시작 명령(기존 로컬 프로젝트/작업 트리를 확인한 후):** 저장소 루트에서 `agy`. 첫 프롬프트는 `"my_traceroute 학습을 이어가자. 현재 진도와 미확인을 읽고 다음 실습 하나만 제시해."`. [공식 Antigravity Rules](https://antigravity.google/docs/rules-workflows/)가 루트 `AGENTS.md` 같은 프로젝트 규칙을 지원한다.

**두 진실을 구별:** `state.json`은 현재 진도, `01-progress.md`는 기존 ChatGPT 대화에서 넘겨받은 **이력 스냅샷**이다. 실제 로컬 코드/명령 출력보다 어떤 문서도 우선하지 않는다. **학생의 실제 구현 코드가 없거나 위치가 불명확하면 자동 생성하지 않는다.**

- [정본 README](../README.md): 12주 목표·마일스톤의 최상위 기준
- [학습 운영 원칙](00-method.md): 튜터 힌트·실습·복습·Java 비교
- [현재 진도 및 미확인 증거](01-progress.md): W01 중간에서 재개
- [C 코드 독해 지도](02-c-atlas.md): C 함수 전체 흐름과 검증할 가설
- [macOS/Ubuntu 환경과 패킷 실험](03-labs.md): 통제 실험과 증거 작성
- [평가와 마일스톤](04-assessment.md): 통과/재학습 게이트
- [학습 기록과 Obsidian 템플릿](05-templates.md): 대화 재개와 지속 기록
- [공식 출처](06-references.md): Rust/Cargo/RFC/OS/원본

## 주차별 이동

| 주차 | Rust | 네트워크·C | 직접 구현 산출물 |
|---|---|---|---|
| [W01](weeks/W01.md) | Cargo·가변성·조건·반복·함수 | IPv4·라우터·홉·TTL·`ping_loop` | TTL/Probe 시뮬레이터 + 시스템 traceroute 관찰 |
| [W02](weeks/W02.md) | Ownership·Borrowing·Struct | 관리자 상태·주소·C `t_mgr` | `Config`와 기본값 테스트 |
| [W03](weeks/W03.md) | `Option`·`Result`·`match`·모듈 | CLI·DNS·입력 검증 | 소켓 없는 안전한 CLI (M1) |
| [W04](weeks/W04.md) | Slice·바이트·Endian | IPv4/UDP/ICMP 헤더·IHL·체크섬 | 안전한 패킷 파서 |
| [W05](weeks/W05.md) | `std::net`·I/O | UDP·IP 라우팅·ARP·TTL | TTL 변경 UDP 송신 |
| [W06](weeks/W06.md) | `socket2`·권한 | Raw Socket·ICMP 수신 | 송신/수신 분리 (M2) |
| [W07](weeks/W07.md) | 타입 모델·상태 분류 | Quoted IP/UDP·Probe 매칭 | 무관한 응답 거부 |
| [W08](weeks/W08.md) | `Instant`·`Duration` | RTT·timeout·deadline | 테스트 가능한 시간 처리 |
| [W09](weeks/W09.md) | 루프·상태 전이 | UDP traceroute 종료 판정 | UDP 추적 MVP |
| [W10](weeks/W10.md) | Trait·프로토콜 추상화 | ICMP Echo 모드 | UDP+ICMP 엔진 (M3) |
| [W11](weeks/W11.md) | 단위/통합·회귀·Clippy | C 가정의 안전성 검사 | 경계·오류 테스트 |
| [W12](weeks/W12.md) | 리팩터링·문서 | 다중 홉·NAT·ECMP·제약 | 재현 가능한 최종 결과 (M4) |

## 한 차시(기본 90분) 진행 순서

1. 선수 개념 회상(5분) — 지난 차시 핵심을 답안 없이 설명한다.
2. Rust 1~2개·네트워크 1개 개념(15분) — Java와 비교, 문법/프로토콜 분리.
3. 관련 **C 함수 전체** 제어 흐름 지도(15분) — 호출·분기·반환·상태 변경 빠짐없이 확인.
4. Rust 직접 구현(30분) — 한 번에 하나의 작은 과제, 정답 선공개 금지.
5. 테스트/실측 검증(15분) — `cargo` 로그, 결정적 테스트, 필요한 경우 승인된 네트워크 캡처.
6. Rust 1·네트워크 2·C/Rust 독해 1문제(10분) — 제출 후 채점.
7. 별도 기록 — 가설/코드/실제 출력/오답/다음 행동을 Obsidian과 Git에 남긴다.

## 실무·학습 안전 원칙

- **출력 성공 ≠ 실제 Probe 전송 ≠ 올바른 Probe 응답 검증**. 세 가지를 별도 평가.
- 패킷 전송과 캡처는 본인 소유·승인된 네트워크에서만, 최소 Probe 수·TTL로 수행.
- C 원본은 사례이지 RFC가 아니다. 위험한 코드는 재현 전까지 `검증 가설`로 표시.
- 외부 C 소스 전체나 완성 Rust 정답은 로드맵에 포함하지 않는다.
- 현재 GitHub `main`에서 Rust crate는 확인되지 않았다. 로컬 Rust 코드를 원격에 올린 것으로 오인하지 않는다.
- 1주차가 미완료라면 2주차를 완료한 것처럼 기록하지 않는다.

**지금 재개:** [W01 2차시의 활성 Toolchain 확인](weeks/W01.md). 자세한 미검증 목록은 [진도 기록](01-progress.md) 참고.
