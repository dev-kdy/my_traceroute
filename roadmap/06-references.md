# 1차 학습 자료·검증 우선순위

**구분 규칙:** [README]=프로젝트 목표, [C 원본]=사례의 실제 구현, [공식]=Rust/RFC/OS 명세, [설계]=개선 제안, [실측]=자신이 기록한 실행 결과. 다른 범주를 섞어서 확정적 표현을 하지 않는다.

## Antigravity CLI 공식 자료

- [Google Antigravity CLI: Getting started](https://antigravity.google/docs/cli/tutorial/) — `agy` 실행과 초기 프롬프트.
- [Google Antigravity: Rules](https://antigravity.google/docs/rules-workflows/) — 루트 `AGENTS.md`, 프로젝트·디렉터리 규칙 발견.
- [Google Antigravity CLI: Best Practices](https://antigravity.google/docs/cli/best-practices/) — 작업 공간 지침 활용.
- [Google Antigravity CLI: Agent settings](https://antigravity.google/docs/agent-settings) — 명령 실행 권한과 승인 모드.
- [Google Antigravity CLI: Features](https://antigravity.google/docs/cli/features/) — `/resume`/`/context` 등. 세션 재개가 학습 상태 기록을 대체하지는 않는다.

**규칙 설계 판단 [설계]:** 이 저장소는 여러 중복 `GEMINI.md`/`.agents/rules`를 만들지 않고 루트 `AGENTS.md`로 [세션 계약](08-session-protocol.md)과 [상태 파일](state.json)을 연결한다. 문서·상태가 실제 로컬 파일보다 오래되었다면 이를 바로잡아야 한다.

## Rust 공식 자료(버전·Edition을 확인한 뒤 사용)

| 범위 | 문서 |
|---|---|
| 전체 언어 | [The Rust Programming Language](https://doc.rust-lang.org/book/) |
| Cargo 입문 | [Rust Book: Hello Cargo](https://doc.rust-lang.org/book/ch01-03-hello-cargo.html) |
| 변수/가변성 | [Rust Book 3.1](https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html) |
| 제어 흐름/타입 | [Rust Book Chapter 3](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html) |
| Ownership/Borrowing | [Rust Book Chapter 4](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) |
| Struct/Enum | [Rust Book Ch 5](https://doc.rust-lang.org/book/ch05-00-structs.html), [Ch 6](https://doc.rust-lang.org/book/ch06-00-enums.html) |
| 오류 처리 | [Rust Book Chapter 9](https://doc.rust-lang.org/book/ch09-00-error-handling.html) |
| 테스트 | [Rust Book Chapter 11](https://doc.rust-lang.org/book/ch11-00-testing.html) |
| 패키지·매니페스트·Lock | [Cargo Book](https://doc.rust-lang.org/cargo/), [Cargo.toml vs Cargo.lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html) |
| Edition 2024 | [Edition Guide](https://doc.rust-lang.org/edition-guide/rust-2024/) |
| 네트워크/시간 API | [std::net](https://doc.rust-lang.org/std/net/), [std::time](https://doc.rust-lang.org/std/time/) |
| Linter | [Clippy](https://doc.rust-lang.org/clippy/) |
| 참고 라이브러리 | [clap](https://docs.rs/clap/latest/clap/), [socket2](https://docs.rs/socket2/latest/socket2/) — 도입 주차에 버전·API 재검토 |

## 프로토콜 표준

| 표준 | 확인 내용 | 적용 주차 |
|---|---|---|
| [RFC 791 IPv4](https://www.rfc-editor.org/rfc/rfc791) | TTL, Version, IHL, Protocol, Total Length, Checksum | W01, W04, W05 |
| [RFC 792 ICMP](https://www.rfc-editor.org/rfc/rfc792) | Time Exceeded, Destination Unreachable, Echo/Reply, Type/Code | W01, W04, W06~W10 |
| [RFC 768 UDP](https://www.rfc-editor.org/rfc/rfc768) | Source/Destination Port, Length, Checksum/Pseudo Header | W04~W07 |
| [RFC 1812 IPv4 Router Requirements](https://www.rfc-editor.org/rfc/rfc1812) | 5.3.1 TTL, 5.2.7.3 ICMP Time Exceeded | W01, W05, W12 |

응답이 보이지 않는다는 것만으로 RFC를 위반하는 장비라고 단정하지 않는다. 주소 유형, 응답 차단·제한, ICMP 생성 예외와 관측 지점을 함께 살펴본다.

## OS와 캡처

- macOS: `man traceroute`, `man tcpdump`, [Apple Developer — Recording a Packet Trace](https://developer.apple.com/documentation/network/recording-a-packet-trace).
- Linux: [raw(7)](https://man7.org/linux/man-pages/man7/raw.7.html), [ip(7)](https://man7.org/linux/man-pages/man7/ip.7.html), [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), [ip-netns(8)](https://man7.org/linux/man-pages/man8/ip-netns.8.html).
- 캡처: [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/), [Wireshark Display Filter Reference](https://www.wireshark.org/docs/dfref/).

## 프로젝트/C 참고 소스

- [학습 프로젝트의 정본 README](../README.md)
- [Dauie/traceroute](https://github.com/Dauie/traceroute) 및 [main.c](https://github.com/Dauie/traceroute/blob/master/src/main.c), [traceroute.c](https://github.com/Dauie/traceroute/blob/master/src/traceroute.c), [traceroute.h](https://github.com/Dauie/traceroute/blob/master/incl/traceroute.h), [send_recv_echo.c](https://github.com/Dauie/traceroute/blob/master/src/send_recv_echo.c), [check_packet.c](https://github.com/Dauie/traceroute/blob/master/src/check_packet.c), [handle_response.c](https://github.com/Dauie/traceroute/blob/master/src/handle_response.c), [set_port_ttl_probe.c](https://github.com/Dauie/traceroute/blob/master/src/set_port_ttl_probe.c), [set_addr_iface.c](https://github.com/Dauie/traceroute/blob/master/src/set_addr_iface.c).

**개정 시 필수 점검:** 현재 Rust Compiler/Edition, OS, C 원본 커밋에 따라 문서가 달라질 수 있다. 기술 사실은 최신 공식 문서와 로컬 `man`을 우선 확인하고, 예시 코드의 성공은 실행 기록 없이는 주장하지 않는다.
