# C 원본 분석 지도 — 전체 제어 흐름과 위험 가설

**[실제 C 원본 확인]** [Dauie/traceroute](https://github.com/Dauie/traceroute/tree/master)에서 직접 확인한 경로/함수를 바탕으로 정리한다. 원본은 학습 사례일 뿐 네트워크 표준이 아니다. 코드를 분석할 때는 매번 링크를 다시 열어 변경 여부를 확인한다.

## 파일별 읽기 위치

| 파일(실제 원본 링크) | 실제 주요 함수/정의 | 권장 주차 | Rust 대응 후보[설계] |
|---|---|---|---|
| [`main.c`](https://github.com/Dauie/traceroute/blob/master/src/main.c) | `main, set_args, parse_args, set_program_defaults, create_sock` | W01, W03 | `main.rs, cli.rs` |
| [`traceroute.h`](https://github.com/Dauie/traceroute/blob/master/incl/traceroute.h) | `t_mgr, t_flags, DEF_INIT_TTL, DEF_MAX_TTL, DEF_PROB_AMT` | W01, W02 | `config.rs` |
| [`traceroute.c`](https://github.com/Dauie/traceroute/blob/master/src/traceroute.c) | `traceroute, initialize_echopacket, ping_loop, fill_packet, update_echopkt` | W01, W04, W09, W10 | `packet.rs, trace.rs` |
| [`send_recv_echo.c`](https://github.com/Dauie/traceroute/blob/master/src/send_recv_echo.c) | `send_echo, recv_echo` | W05, W06, W08 | `socket.rs, timing.rs` |
| [`check_packet.c`](https://github.com/Dauie/traceroute/blob/master/src/check_packet.c) | `icmppkt_check, udppkt_check, check_packet` | W04, W07, W11 | `packet.rs, response.rs` |
| [`handle_response.c`](https://github.com/Dauie/traceroute/blob/master/src/handle_response.c) | `print_specials, handle_response` | W07, W08 | `response.rs, output.rs` |
| [`set_port_ttl_probe.c`](https://github.com/Dauie/traceroute/blob/master/src/set_port_ttl_probe.c) | `set_init_ttl, set_max_ttl, set_port, set_probe_amt` | W03 | `config.rs` |
| [`set_addr_iface.c`](https://github.com/Dauie/traceroute/blob/master/src/set_addr_iface.c) | `set_addr_iface, set_addr` | W03, W05, W11 | `socket.rs` |
| [`useage.c`](https://github.com/Dauie/traceroute/blob/master/src/useage.c) | `useage` | W03 | CLI help |

## 1. 프로그램 전체: `main()` [원본]

1. `ft_memalloc(sizeof(t_mgr))`로 관리자 구조체를 확보한다.
2. 인자가 없으면 `useage()`를 호출한다.
3. `set_program_defaults(mgr)`: `flags.run=true`, 기본 UDP 모드, 시작 TTL 1, 최대 TTL 30, 홉당 Probe 3, UDP 포트 33434 등 초기화.
4. `parse_args(mgr,ac,av)`: `-f/-m/-p/-s/-i/-q/-I` 파싱, 도메인/IP 처리.
5. 목적지 주소 지정 여부 검사.
6. `create_sock()`: 송신 raw socket, 수신 ICMP raw socket 생성, 원본은 `IP_HDRINCL`과 bind를 사용.
7. `traceroute(mgr)` → `free(mgr)`.

**독해 실습:** 각 단계가 실패하면 무엇이 실행되지 않는지, `mgr`의 어떤 값이 먼저 유효해야 하는지, 설정 파싱과 소켓 생성 순서가 안전한지 **원본 근거**로 판단한다.

## 2. 핵심 함수 `ping_loop()` [원본]

`traceroute()`가 패킷/메시지를 초기화하고 `initialize_echopacket()`에서 첫 패킷 헤더를 준비한 후 `ping_loop()`로 진입한다.

1. 바깥 `while`: `flags.run == TRUE && mgr->ttl <= mgr->max_ttl`.
2. `probe=0` 설정, 현재 TTL 번호 출력.
3. 안쪽 `while(probe++ < mgr->nprobes)`에서:
   - `fill_packet()`: 구조체의 IP/UDP 혹은 ICMP 헤더를 송신 바이트 버퍼에 복사; `gettimeofday`로 송신 시각 기록.
   - `send_echo()`: `sendto`로 송신.
   - `ft_memset(resp_buff,0,IP_MAXPACKET)`: 수신 버퍼 초기화.
   - `recv_echo()`: `select`로 대기 후 `recvfrom`, 수신 시간 기록; timeout이면 `*` 출력과 FAILURE 반환.
   - `handle_response()`: `check_packet` 검사 후 IP/RTT/ICMP 특수 출력을 시도.
4. 홉 내 Probe 종료 후 줄바꿈, `mgr->ttl++`.
5. `update_echopkt(mgr,msg)`: 증가된 TTL을 다음 패킷의 헤더 구조체에 반영. **전송 버퍼 갱신은 다음 `fill_packet` 때 일어남**.
6. 마지막 수신 버퍼 출발지 IP가 목적지 주소와 일치하면 `flags.run=FALSE`.
7. 바깥 `while` 조건을 다시 평가한다.

### TTL의 세 종류를 추적해 보자

| 시점 | 관리 값 `mgr->ttl` | 구조체 `msg.iphdr` TTL | 실제 송신 버퍼 `pkt` TTL |
|---|---:|---:|---:|
| 첫 `fill_packet` 수행 후 | 1 | 1 | 1 |
| `mgr->ttl++` 직후 | 2 | 1 | 1 |
| `update_echopkt` 직후 | 2 | 2 | 1 |
| 다음 `fill_packet` 직후 | 2 | 2 | 2 |

`update_echopkt`는 TTL을 감소시키지 않는다. **프로그램은 탐색 범위를 늘리기 위해 송신 TTL을 증가**시키고, **라우터는 전달하면서 TTL을 감소**시킨다. [RFC 1812 5.3.1](https://www.rfc-editor.org/rfc/rfc1812)에서 라우터의 감소 동작을 확인한다.

## 3. C 코드의 한계: 확인된 코드 사실 / 아직 검증할 가설

| 원본의 실제 형태 | 가설·검증 질문(미확정 버그) | Rust 목표[설계] |
|---|---|---|
| `check_packet.c`는 `IPV4_HDRLEN` 고정 오프셋에 포인터 캐스팅 | IPv4 IHL > 5/잘린 응답에서 읽기 위험? | 수신 길이·IHL 확인 후 바이트 slice 파싱 |
| `recv_echo()` 실패 반환값을 `ping_loop()`가 검사하지 않음 | timeout인데 `handle_response`가 어떤 버퍼·시각을 읽는가? | `Timeout/Response/IOError` 분리 |
| 종료를 **마지막 응답의 출발지 IP** 일치로 판단 | 무관한 ICMP/잘못된 Type/Code에도 멈출 수 있는가? | 올바른 Probe·유효한 ICMP 종료 신호만 인정 |
| `update_echopkt`의 UDP 소스 포트는 `pid+ttl`, 목적지 포트는 `udp_port` | 홉당 여러 Probe를 정확히 구별할 수 있는가? | Probe별 식별 전략과 지연·중복 처리 |
| `set_addr_iface`가 파싱 중 호출될 수 있는데 소켓은 이후 생성 | `setsockopt`에 유효한 FD가 전달되는가? | 파싱/검증/소켓 생성 단계 분리 |
| `set_addr_iface`의 `if (!(setsockopt(...)))` | 성공 반환 0을 오류로 처리하는가? | 시스템 호출 반환값 명시적 검사 |
| 원본 RTT는 `gettimeofday` 기반 | 시스템 시각 변화 영향을 받는가? | `Instant`로 경과 시간 측정 |
| `libft`·`ping`는 심볼릭 링크 | 외부 컴포넌트 없이 원본이 빌드되는가? | 원본 C 빌드를 Rust 학습의 필수 선행 조건으로 두지 않음 |

이 표의 위험은 **검증해야 할 가설**이다. 실제 입력·환경에서 재현하기 전에 '발견한 버그'라고 확정하지 않는다. 특히 UDP 원본과 macOS 시스템 traceroute의 Probe 포트 생성 규칙은 서로 다를 수 있다.

## 4. 각 함수 독해를 위한 고정 질문 8개

1. 입력 타입과 버퍼 길이는 무엇인가?
2. 리턴값이 성공/실패를 충분히 나타내는가?
3. 이 함수가 쓰거나 읽는 `mgr` 필드는 무엇인가?
4. 다른 함수가 업데이트한 값은 즉시 패킷에 반영되는가?
5. 네트워크에서 읽은 값은 길이/출처를 검증했는가?
6. Timeout과 오류, 수신 성공이 서로 구별되는가?
7. 목적지 도달 조건은 **해당 Probe와 응답 종류**에 의존하는가?
8. 같은 동작을 Rust로 만들 때 어떤 데이터 타입과 테스트로 더 안전해지는가?

**학습 범위 조정:** W01에는 위 전체 호출 지도는 반드시 이해하되 socket/raw packet의 **내부 바이트 구현**은 W04~W08에서 다룬다. '길어서 생략'이 아니라 '전체 흐름 파악 → 깊이 조절'이다.
