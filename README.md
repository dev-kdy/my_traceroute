# my_traceroute

> Rust와 네트워크의 개념과 동작을 학습하며 `traceroute`를 나만의 소스코드로 구현하는 프로젝트.

**학습 목표:** C로 작성된 `traceroute`를 이해하고, IPv4·UDP·ICMP·TTL·Raw Socket을 패킷 수준에서 검증하며 안전한 Rust로 재설계한다. 단순 번역이 아니라 **원리 이해 → 직접 구현 → 실험 → 설명**을 목표로 한다.

- **대상:** Java 등 다른 언어 경험은 있지만 Rust는 처음인 개발자
- **기간:** 12주 · 주 4~6시간(약 48~72시간) · 주당 2차시 + 실습·복습
- **기준 환경:** Linux(권장 Ubuntu VM), Rust stable / Edition 2024
- **범위:** IPv4 UDP traceroute → ICMP Echo 모드 → 테스트 및 리팩터링
- **원본 참고:** [Dauie/traceroute](https://github.com/Dauie/traceroute) · 강의자료(보유한 경우)

> 원본 C 구현과 공개 강의자료는 **학습용 참고 자료**다. 원본을 무조건 직역하지 않고 Rust의 타입·소유권·에러 모델을 활용한다. 패킷 전송은 본인 소유/승인된 환경에서만 실행한다.

## 목차

1. [학습 원칙과 통과 기준](#학습-원칙과-통과-기준)
2. [12주 전체 로드맵](#12주-전체-로드맵)
3. [주차별 상세 커리큘럼](#주차별-상세-커리큘럼)
4. [C 원본 → Rust 모듈 대응](#c-원본--rust-모듈-대응)
5. [프로젝트 실행 환경과 검증](#프로젝트-실행-환경과-검증)
6. [최종 완료 기준과 공식 자료](#최종-완료-기준과-공식-자료)

## 학습 원칙과 통과 기준

각 차시는 **개념 20분 → C 코드 읽기 15분 → Rust 직접 구현 30분 → 패킷 캡처/테스트 15분 → 확인 문제 10분**을 기본으로 한다. 차시 후 남은 시간에 과제·복습을 진행한다.

1. 학습자가 직접 코드를 먼저 작성한다. AI는 처음부터 정답 전체를 제시하지 않고 힌트·리뷰·테스트 설계를 우선한다.
2. Rust의 `Ownership`, `Borrowing`, `Option`, `Result`, `&[u8]`를 실제 패킷 처리와 연결한다.
3. 네트워크 관련 설명은 RFC·Linux 문서와 실제 Wireshark/tcpdump 캡처로 검증한다.
4. “컴파일 성공”과 “올바른 프로토콜 동작”은 구별한다. 출력만 비슷하다고 정상 구현이라 단정하지 않는다.
5. 매 차시 **직접 구현 코드 + 실행 증거 + 개념 요약 + 확인 문제**를 남긴다.
6. 통과 조건: 구현을 실행할 수 있고, 오류 상황을 설명하며, 패킷/테스트 증거를 제시할 수 있어야 한다.

### 체크포인트

- **3주차:** Rust CLI / 구성 타입과 에러 처리 완성
- **6주차:** TTL이 적용된 UDP 송신 + 수신 ICMP 패킷 파싱
- **10주차:** UDP/ICMP traceroute 동작
- **12주차:** 테스트·문서·예외 처리 및 Linux 재현 실험 완료

## 12주 전체 로드맵

| 주차 | Rust 핵심 | 네트워크 핵심 | C 원본 연결 | 주간 산출물 |
|---|---|---|---|---|
| 1 | 설치·Cargo·변수·흐름 제어 | 패킷·홉·TTL·traceroute 원리 | `main.c`, `traceroute.c` | 원본 실행 로그·경로 흐름도 |
| 2 | Ownership·Borrowing·Struct | 주소·상태·C 메모리 관리 | `traceroute.h` | `Config` 모델 |
| 3 | Enum·Option·Result·모듈 | DNS·IP·CLI·유효성 검사 | `main.c`, `set_port_ttl_probe.c` | Rust CLI |
| 4 | 배열·Slice·바이트·비트 | IPv4/UDP/ICMP 헤더·체크섬 | `traceroute.c`, `check_packet.c` | 안전한 패킷 파서 |
| 5 | `std::net`·I/O 에러 | UDP·라우팅·ARP·TTL | `send_recv_echo.c` | TTL별 UDP 송신 |
| 6 | Crate·Socket API | Raw Socket·ICMP·권한 | `send_recv_echo.c` | ICMP 수신기 |
| 7 | 패턴 매칭·타입 모델 | ICMP 내 원래 패킷·매칭 | `check_packet.c` | Probe 응답 검증 |
| 8 | `Instant`·`Duration`·테스트 | RTT·Timeout·응답 지연 | `send_recv_echo.c`, `handle_response.c` | 시간 측정 모듈 |
| 9 | 반복·상태 관리 | TTL 루프·목적지 도달 | `traceroute.c` | UDP traceroute |
| 10 | Trait·모드 분리 | ICMP Echo·UDP와 비교 | `traceroute.c`, `main.c` | UDP/ICMP 지원 |
| 11 | Unit/Integration·Clippy | 위조·짧은 패킷·소켓 오류 | `check_packet.c`, `set_addr_iface.c` | 검증·회귀 테스트 |
| 12 | 코드 정리·문서 | NAT·방화벽·ECMP·경로 제한 | 전체 | 최종 CLI·분석 보고서 |

## 주차별 상세 커리큘럼

### 1주차 — traceroute와 Rust의 첫 만남

- **1차시: traceroute 관찰** — IP 패킷, 라우터, 홉, TTL, ICMP Time Exceeded, UDP Port Unreachable를 개념도로 설명한다. `traceroute.c`의 `ping_loop()`가 TTL을 증가시키는 순서를 따라간다.
- **2차시: Rust 개발 환경** — `rustup`, `cargo new`, `cargo run`, 변수/가변성, 함수, `if`/`loop`/`for`를 연습한다. C `main()`과 Rust `fn main()`을 비교한다.
- **실습:** 원본 또는 시스템 `traceroute`로 승인된 대상에 경로를 확인하고 `icmp` 필터로 캡처한다. 각 홉의 IP, RTT, `*` 표기를 설명한다.
- **산출물:** 환경 점검 기록, C 함수 호출 흐름도, 최초 Rust Hello CLI.
- **통과 질문:** TTL=1인 패킷은 왜 첫 라우터에서 사라지는가? `*`가 반드시 패킷 손실인가?

### 2주차 — 소유권과 프로그램 상태

- **1차시: 메모리 모델** — Stack/Heap, `String`과 `&str`, move/copy, immutable/mutable borrow, `Drop`을 다룬다.
- **2차시: C 구조체 재설계** — `traceroute.h`의 `t_mgr`·플래그·상수를 분석한다. `struct Config`, `enum ProbeProtocol`, `impl Default`로 표현한다.
- **실습:** 유효한 TTL 범위, Probe 수, 포트를 보장하는 생성자와 타입을 만든다.
- **산출물:** `src/config.rs` 및 기본값 테스트.
- **통과 질문:** Rust에서 move 후 원래 변수는 왜 사용할 수 없는가? 가변 참조와 공유 참조는 언제 충돌하는가?

### 3주차 — CLI, DNS와 오류 처리

- **1차시: Rust 타입·에러** — `Option<T>`, `Result<T,E>`, `match`, `?`, `mod`와 `use`를 배운다.
- **2차시: C 옵션 파싱** — `main.c`의 `parse_args()`, `set_program_defaults()`와 `set_port_ttl_probe.c`를 읽는다. `clap`으로 `-f`, `-m`, `-p`, `-q`, `-I`를 파싱하고 DNS/IP를 처리한다.
- **실습:** 범위 초과 TTL, 잘못된 IP, 누락된 대상, 유효하지 않은 포트 처리 테스트.
- **산출물:** 송신 전 단계까지 동작하는 Rust CLI.
- **통과 질문:** 예외 대신 `Result`를 반환하면 호출부가 어떻게 달라지는가? DNS 조회와 실제 라우팅은 다른 단계인가?

### 4주차 — 바이트 수준의 패킷 이해

- **1차시: 바이너리 처리** — `[u8; N]`, `Vec<u8>`, `&[u8]`, 슬라이스 경계, 비트마스크, `u16::from_be_bytes`, `to_be_bytes`를 학습한다.
- **2차시: 프로토콜 헤더** — IPv4 Version/IHL/Total Length/TTL/Protocol/Checksum, UDP 포트·길이·체크섬, ICMP Type/Code/Checksum을 읽는다. `fill_packet()`, `check_packet()`을 분석한다.
- **실습:** 샘플 바이트로 IPv4·UDP·ICMP를 파싱하고 짧거나 손상된 버퍼에서 패닉 없이 오류를 반환한다.
- **산출물:** `src/packet.rs` 및 정상/비정상 패킷 테스트.
- **통과 질문:** 왜 네트워크 바이트 순서가 중요한가? IPv4 IHL을 20바이트로 가정하면 어떤 버그가 생기는가?

### 5주차 — UDP와 커널 네트워크 스택

- **1차시: 소켓 기초** — `socket`, `bind`, `sendto`, 로컬·원격 주소, 커널의 UDP/IP 헤더 생성 역할과 `std::net::UdpSocket`을 다룬다.
- **2차시: 실제 전송 경로** — 서브넷, 기본 게이트웨이, 라우팅 테이블, ARP, Ethernet의 다음 홉을 학습하고 `send_echo()`의 의미를 분석한다.
- **실습:** TTL을 1, 2, 3으로 설정한 UDP 전송을 만들고 캡처에서 TTL·포트·목적지를 비교한다.
- **산출물:** `src/socket.rs`, TTL별 송신 로그.
- **통과 질문:** 목적지 IP와 Ethernet 목적지 MAC은 언제 다른가? 일반 UDP 소켓과 IP 헤더 포함 Raw Socket은 무엇이 다른가?

### 6주차 — Raw Socket과 ICMP 수신

- **1차시: Raw Socket 원리** — `socket2`, IPPROTO_ICMP, Linux `CAP_NET_RAW`, `IP_HDRINCL`, 소켓 소유권/해제를 다룬다. 일반 UDP 송신 + ICMP 수신 소켓을 구분한다.
- **2차시: 응답 수신** — `recv_echo()`의 `select()`/`recvfrom()` 흐름을 분석하고 수신한 IPv4+ICMP의 Type/Code를 구분한다.
- **실습:** ICMP Time Exceeded(Type 11/Code 0), Destination Unreachable(Type 3)의 수신과 오류를 로깅한다.
- **산출물:** ICMP 수신기 및 pcap 비교 결과.
- **통과 질문:** 응답을 읽는 데 왜 UDP 수신 소켓만으로 충분하지 않을 수 있는가? `CAP_NET_RAW` 권한은 왜 필요한가?

### 7주차 — 수신 응답과 Probe를 정확하게 연결

- **1차시: ICMP Error Payload** — ICMP 오류 메시지에 인용된 원래 IPv4 헤더와 전송계층의 시작 부분을 해석한다. IPv4 IHL과 실제 길이를 기반으로 오프셋을 계산한다.
- **2차시: 매칭 설계** — `check_packet.c`의 UDP 출발지·목적지 포트 / ICMP Identifier·Sequence 검사와 `handle_response.c`를 분석한다.
- **실습:** 다른 Probe의 지연 응답, 무관한 ICMP, 잘린 패킷을 걸러낸다. 홉별 Probe마다 고유한 식별 규칙을 설계한다.
- **산출물:** `src/response.rs` 및 Probe 매칭 단위 테스트.
- **통과 질문:** ICMP를 받았다는 사실만으로 왜 내 Probe의 응답이라고 할 수 없는가?

### 8주차 — RTT, Timeout, 정확한 시계

- **1차시: 시간 API** — `std::time::Instant`·`Duration`·단조 시계를 배운다. `gettimeofday`를 시간 측정에 쓰는 방식의 한계를 비교한다.
- **2차시: 수신 제한시간** — `select()`의 대기, 수신 제한, `*` 출력, 늦은 응답·무관한 응답을 같은 deadline 안에서 처리하는 흐름을 학습한다.
- **실습:** Probe별 송신 시각·응답 시각을 기록하고 RTT를 밀리초로 표시한다. Timeout/late reply를 가짜 clock 또는 결정적 테스트 데이터로 검증한다.
- **산출물:** `src/timing.rs`, Timeout 테스트.
- **통과 질문:** RTT와 one-way latency는 같은가? Timeout은 네트워크 단절을 증명하는가?

### 9주차 — UDP traceroute 구현 완성

- **1차시: 홉 탐색 루프** — `ping_loop()`에서 TTL 증가, 홉당 반복 Probe, Max TTL 종료, 중간 라우터·목적지를 식별하는 흐름을 재구성한다.
- **2차시: 목적지 판정** — TTL 초과와 Port Unreachable을 구별하고 올바른 Probe의 응답에 한해서 완료 상태를 결정한다. 주소가 일치한다는 이유만으로 모든 ICMP 응답을 성공으로 처리하지 않는다.
- **실습:** `traceroute -m 5 -q 3 1.1.1.1`에 대응하는 기본 CLI 동작을 승인된 환경에서 실행하고 원본/시스템 도구와 결과를 비교한다. 경로가 동적으로 달라질 수 있음을 기록한다.
- **산출물:** `src/trace.rs`, IPv4 UDP traceroute MVP.
- **통과 질문:** 목적지 IP에서 ICMP가 왔어도 언제 종료해서는 안 되는가?

### 10주차 — ICMP Echo 모드와 옵션 통합

- **1차시: Echo Request/Reply** — ICMP Type 8/0, Identifier, Sequence, Checksum을 배우고 C 코드 `update_echopkt()`를 분석한다.
- **2차시: 공통 엔진** — `enum ProbeProtocol { Udp, Icmp }` 기반 모드 전환, 공통 결과 타입과 메시지 포맷팅을 설계한다. `-I`, `-s`, `-i` 옵션은 시스템별 차이를 검증한 뒤 단계적으로 지원한다.
- **실습:** UDP와 ICMP 모드의 송신·응답 캡처를 비교하고 옵션별 테스트를 작성한다.
- **산출물:** UDP + ICMP traceroute, 도움말.
- **통과 질문:** UDP 기반 종료 신호와 ICMP Echo 기반 종료 신호가 왜 다른가?

### 11주차 — 오류 분석과 안전성·회귀 테스트

- **1차시: C 코드 리뷰** — `check_packet.c`의 고정 오프셋 가정, `set_addr_iface.c`의 소켓 초기화 순서와 `setsockopt` 검사, `send_recv_echo.c`의 Timeout·수신 흐름을 검토한다. 의심 지점은 재현 실험으로 확정한다.
- **2차시: Rust 테스트** — `cargo fmt`, `cargo clippy`, `cargo test`, 비정상 길이/옵션/체크섬/포트/ICMP Type 테스트를 작성한다. `unsafe`는 기본적으로 피하고, 필요할 경우 경계와 근거를 문서화한다.
- **실습:** 무작위·잘린·무관한 응답에 대해 패닉 없이 무시/오류 처리. CI에서 네트워크 권한이 없는 단위 테스트를 먼저 실행한다.
- **산출물:** 테스트 스위트, 발견한 C 구현 개선점 문서.
- **통과 질문:** C 구조체를 패킷 바이트로 무조건 캐스팅하면 어떤 위험이 생기는가?

### 12주차 — 재현 가능한 네트워크 실험과 최종 발표

- **1차시: 통제된 테스트 네트워크** — Linux network namespace·veth·라우팅 테이블을 사용해 2개 이상 홉을 만드는 실험을 선택적으로 수행한다. TTL 감소, 중간 홉 응답, 불완전 경로를 검증한다.
- **2차시: 관찰과 한계** — NAT, 방화벽, ICMP rate limiting, ECMP, 비대칭 경로 때문에 traceroute 결과가 실제 모든 패킷의 고정 경로를 증명하지 못함을 설명한다. 코드·README·설계·테스트를 마무리한다.
- **실습:** 정상 도달, 제한 TTL, Timeout, 다른 응답 유형의 결과를 녹화/캡처/로그로 증명한다.
- **산출물:** Rust CLI, 실행 가이드, C↔Rust 설계 비교, 네트워크 캡처 설명서, 최종 회고.
- **통과 질문:** traceroute가 네트워크 경로를 보여주는 원리와 한계는 무엇인가? 결과가 실행 때마다 달라질 수 있는 이유는?

## C 원본 → Rust 모듈 대응

| C 파일/구성 | 분석 대상 | Rust 재설계 예시 |
|---|---|---|
| [`src/main.c`](https://github.com/Dauie/traceroute/blob/master/src/main.c) | CLI·초기화·소켓 생성 | `main.rs`, `cli.rs` |
| [`incl/traceroute.h`](https://github.com/Dauie/traceroute/blob/master/incl/traceroute.h) | `t_mgr`·기본값·옵션 | `config.rs` |
| [`src/set_port_ttl_probe.c`](https://github.com/Dauie/traceroute/blob/master/src/set_port_ttl_probe.c) | 옵션 검증 | `config.rs` |
| [`src/set_addr_iface.c`](https://github.com/Dauie/traceroute/blob/master/src/set_addr_iface.c) | 주소·인터페이스 | `socket.rs` |
| [`src/traceroute.c`](https://github.com/Dauie/traceroute/blob/master/src/traceroute.c) | 패킷 조립·홉 루프 | `probe.rs`, `trace.rs` |
| [`src/send_recv_echo.c`](https://github.com/Dauie/traceroute/blob/master/src/send_recv_echo.c) | `sendto`·`select`·`recvfrom` | `socket.rs`, `timing.rs` |
| [`src/check_packet.c`](https://github.com/Dauie/traceroute/blob/master/src/check_packet.c) | 응답 매칭 | `packet.rs`, `response.rs` |
| [`src/handle_response.c`](https://github.com/Dauie/traceroute/blob/master/src/handle_response.c) | RTT·출력·ICMP 코드 | `response.rs`, `output.rs` |
| [`src/useage.c`](https://github.com/Dauie/traceroute/blob/master/src/useage.c) | CLI 도움말 | `cli.rs` |

**주의:** 원본에는 `libft`, `ping` 심볼릭 링크가 있어, 원본 C 빌드에는 연관 소스가 추가로 필요할 수 있다. 원본 저장소의 전체 빌드 가능 여부는 별도로 확인하고, Rust 구현의 필수 의존성으로 삼지 않는다.

## 프로젝트 실행 환경과 검증

- **OS:** Ubuntu Linux VM 또는 격리된 Linux 개발 환경. macOS/Windows 개발자는 VM 권장(소켓/권한 동작 차이).
- **도구:** Rust stable, `rustup`, `cargo`, `rust-analyzer`, Wireshark/tcpdump, `iproute2`.
- **Crate:** 처음에는 `std`; 필요해지면 `clap`(CLI), `socket2`(소켓). `pnet`은 직접 파싱을 익힌 뒤 선택적으로.
- **권한:** Raw ICMP Socket에는 Linux `CAP_NET_RAW`가 필요할 수 있다. 무조건 루트 실행·권한 광역 부여 대신 VM/격리 환경에서 최소권한으로 관리한다.
- **Wireshark Display Filters:** `icmp`, `icmp.type == 11`, `icmp.type == 3 && icmp.code == 3`, `udp.dstport == 33434`, `ip.ttl == 1`.
- **중요한 검증:** ICMP 오류에 포함된 원본 IP 헤더의 IHL(가변 길이), 실제 버퍼 길이, 원본 포트/ID를 검사한다. `*`는 반드시 손실이 아니라 응답 차단·지연·rate limit일 수 있다.
- **테스트:** 단위 테스트는 권한/외부 네트워크 없이 실행; 실소켓 통합 테스트는 명시적으로 분리해 제한된 환경에서 수행한다.

```bash
# 초기 세팅(1주차)
rustup --version
cargo --version
cargo new my_traceroute --bin
cd my_traceroute
cargo run
cargo fmt --check
cargo test
```

> 이 저장소 루트에 Rust 코드를 생성할 때는 실제 디렉터리 구조를 확인하고 중첩 `my_traceroute/my_traceroute`가 생기지 않도록 한다. README 커리큘럼의 명령은 독립 실습 디렉터리 예시이다.

### 학습 기록 템플릿

- **차시:** 주차/차시
- **오늘 목표:** Rust 개념 1~2개 + 네트워크 원리 1개
- **읽은 C 코드:** 파일/함수/핵심 줄
- **직접 작성:** Rust 파일·함수, 테스트 결과
- **관측:** 사용 명령·패킷 필터·패킷 필드·기대한 값과 실제 값
- **문제 해결:** 실패 재현 → 원인 → 수정 → 재검증
- **퀴즈:** Rust/네트워크/코드 읽기
- **판정:** 완료 / 복습 필요 / 미진행

## 최종 완료 기준과 공식 자료

최종 프로젝트 완료 조건:

- [ ] IPv4 UDP traceroute의 TTL 단계별 송수신과 목적지 판정 구현
- [ ] ICMP Echo 모드 구현 및 주요 CLI 옵션 검증
- [ ] 오프셋/길이/무관한 응답/Timeout/이상 ICMP에 안전하게 대응
- [ ] 단위 테스트·권한 분리 실소켓 테스트·포맷·Clippy 점검
- [ ] 실제 네트워크 또는 격리 네임스페이스에서 Wireshark/tcpdump 근거 확보
- [ ] C 원본과 Rust 설계의 차이, 네트워크 관측 한계 설명
- [ ] 설치·사용법·알려진 제약·테스트 절차 문서화

**공식 학습 자료**

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rustlings](https://rustlings.rust-lang.org/)
- [std::net](https://doc.rust-lang.org/std/net/)
- [socket2](https://docs.rs/socket2/latest/socket2/)
- [RFC 791: IPv4](https://www.rfc-editor.org/rfc/rfc791)
- [RFC 792: ICMP](https://www.rfc-editor.org/rfc/rfc792)
- [RFC 768: UDP](https://www.rfc-editor.org/rfc/rfc768)
- [RFC 1812: Router Requirements](https://www.rfc-editor.org/rfc/rfc1812)
- [Linux ip(7)](https://man7.org/linux/man-pages/man7/ip.7.html)
- [Linux raw(7)](https://man7.org/linux/man-pages/man7/raw.7.html)
- [Wireshark Display Filter Reference](https://www.wireshark.org/docs/dfref/)

**학습 시작 프롬프트:** `1주차 1차시를 시작하자. C 원본에서 관련 함수를 먼저 보여주고 설명한 뒤 Rust 개념을 학습시키고, 직접 구현하도록 힌트만 줘. 마지막에 퀴즈와 검증 체크리스트를 제시해 줘.`
