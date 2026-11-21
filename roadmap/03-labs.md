# 실습 환경 — macOS에서 시작하고 Linux VM에서 검증

## Antigravity CLI 안전 실행 규칙

에이전트는 사용자의 명시적 승인 없이 `sudo`, `traceroute` 실송신, `tcpdump` 캡처, `ip route`, `ip netns`, Raw Socket, 외부 연결 테스트를 실행하지 않는다. **각 실험 전에** 승인된 목적지·최대 TTL·Probe 수·인터페이스·권한·실패 시 복구 방법을 사용자가 확인하도록 한다. 실제로 관찰하지 못하면 다음 단계로 넘어가기보다 해당 결과를 `unverified` 또는 `통제된 대체 실험`으로 기록한다. [세션 프로토콜](08-session-protocol.md)과 [진도 상태](state.json)에 근거를 남긴다.

## 0. 실험 안전 범위

**본인 소유/승인된 네트워크와 호스트만** 테스트한다. 먼저 `-m`(최대 홉)과 `-q`(Probe 수)를 작게 설정하고 필요 최소한의 트래픽만 보낸다. 공유 pcap에서 IP, MAC, DNS 이름 등 개인·조직 정보는 익명화한다. 허가 없이 제3자 네트워크에 raw 패킷 또는 다량 Probe를 보내지 않는다.

## 1. Rust 개발 툴체인 점검

학습자 보고 버전은 `rustc 1.100.0`, `cargo 1.100.0`. 나머지는 직접 실행·기록한다.

```bash
pwd                               # Cargo.toml 위치에서 실행하는지 확인
rustup show active-toolchain      # 현재 도구 체인/대상 플랫폼
rustup target list --installed    # 설치된 타깃 목록
rustc --version                   # 컴파일러
cargo --version                   # 패키지/빌드 관리 도구
cargo check                       # 빠른 컴파일 검사
cargo build                       # 디버그 실행 파일 빌드
cargo run                         # 빌드하고 실행
cargo test                        # 테스트
cargo fmt --check                 # 포맷 검사(수정하지 않음)
echo $?                           # 바로 직전 명령 종료 상태
cargo clippy -- -D warnings       # 경고도 오류로 검사
```

- **주의:** 원격 GitHub `main`에는 Rust crate가 아직 확인되지 않았다. 로컬 `Cargo.toml`을 먼저 찾아야 한다. 실수로 저장소 안에 `my_traceroute/my_traceroute` 중첩 프로젝트를 만들지 않는다.
- `Cargo.toml`: 패키지 이름, `edition`, 의존성 선언. `Cargo.lock`: 해결된 의존성 버전 기록(Binary crate는 커밋). `src/main.rs`: 통상적인 Binary crate 진입점. `src/lib.rs`: Library crate 진입점. `target/`: 빌드 산출물로 Git에서 제외.
- Toolchain 버전과 Edition은 별도. `edition = "2024"` 여부는 **실제 로컬 매니페스트**에서 확인한다.

## 2. macOS 시스템 traceroute(W01)

1. `man traceroute`/`man tcpdump`와 `ifconfig`로 해당 macOS의 동작/옵션 확인.
2. `route -n get <승인된_IPV4>`로 인터페이스/게이트웨이 확인. 출력은 외부에 그대로 공유하지 않아도 된다.
3. 다음 명령으로 **승인된 IPv4 주소**에만 제한된 실험 실행.

```bash
traceroute -n -m 5 -q 1 -w 1 <승인된_IPV4>
```

**실험 전 예측:** TTL=1에서 어떤 ICMP가 기대되는가? 호스트가 응답하지 않으면 `*`는 무엇을 의미하는가? RTT는 단방향인가 왕복인가? **정답 없이 먼저 서술**.

### 패킷 캡처

캡처 인터페이스를 `ifconfig`·라우팅 정보로 확인하여 사용(`en0` 고정 가정 금지).

```bash
sudo tcpdump -ni <선택_인터페이스> -vv 'icmp or (udp and portrange 33434-33534)'
```

다른 터미널에서 위 `traceroute` 실행. 필요한 경우 한정된 승인 실험에서 `sudo tcpdump -ni <인터페이스> -s 0 -w trace-w01.pcap 'icmp or udp'`로 저장. 권한·인터페이스·필터·중간 방화벽·응답 지연으로 관찰하지 못할 수 있으므로 **출력과 관측 차이도 기록**한다.

Wireshark **표시 필터(display filter)**: `icmp`, `icmp.type == 11`, `icmp.type == 3 && icmp.code == 3`, `udp`, `ip.ttl == 1`. tcpdump의 **캡처 필터(capture filter)**와 문법이 다르다.

## 3. 관측에서 반드시 구별할 것

| 관측 | 의미 | 잘못된 결론 |
|---|---|---|
| IPv4 TTL=1 패킷 | 첫 라우터가 전달할 때 수명이 소진될 수 있음 | '프로그램이 TTL을 자동 감소시킨다' |
| ICMP Type 11 Code 0 | TTL exceeded in transit | '목적지 도달 완료' |
| ICMP Type 3 Code 3 | Destination Unreachable / Port Unreachable | 내 Probe인지 확인하기 전에 종료 |
| ICMP Type 0 Code 0 | Echo Reply(ICMP Echo 모드) | UDP 모드 종료로 무조건 사용 |
| `*` | 제한 시간 안에 유효한 응답을 관측하지 못함 | 라우터 고장·실제 패킷 손실 확정 |
| RTT(ms) | 송신→관련 응답 수신 **왕복** 경과 시간 | 홉 간 편도 지연 |
| Quoted IP/UDP | ICMP 오류에 인용된 원래 패킷 정보 | 인용 대상이 내 Probe라고 무조건 가정 |

방화벽, ICMP rate limit, NAT, ECMP, 비대칭 경로, 캡처 위치, NIC checksum offload 등으로 실제 결과는 달라질 수 있다. **송신/수신을 같은 Probe로 매칭했는지**부터 판단한다.

## 4. Ubuntu VM 전환과 Linux 전용 기능(W05~W12)

| 목적 | macOS에서 가능한 내용 | Ubuntu VM에서 수행할 내용 |
|---|---|---|
| Cargo, 기본 Rust, 타입·테스트 | 우선 시행 | 재현 |
| 시스템 traceroute/tcpdump | 환경·권한에 따라 가능 | 재현 |
| `std::net::UdpSocket` 송신 | 가능 | 라우팅·TTL 관찰 |
| Raw ICMP Socket/`socket2` | OS마다 제약 다름 | `CAP_NET_RAW` 최소권한 및 `raw(7)` |
| `ip netns`/`veth` 다중 홉 | Linux 기능이 아니므로 제외 | 격리 실습 네트워크 생성 |
| CI 단위 테스트 | 네트워크 불필요 | 관리자 권한 없이 실행 |

Linux 환경 점검 명령: `ip addr`, `ip route`, `ip netns list`. 격리 namespace 구성 및 라우터 포워딩은 W12에서 단계별로 직접 실습하되 실제 호스트 네트워크 설정을 함부로 바꾸지 않는다.

## 5. 제출할 실험 증거 템플릿

```text
실험 ID / 시각 / OS·커널 / Toolchain·Edition:
호스트·대상(승인 여부, 필요 시 익명화) / 인터페이스:
가설: 예상 TTL/Type/Code/포트/응답 형태
실행 명령과 옵션:
기대 출력:
실제 stdout/stderr/exit code:
패킷: 송신 프레임 번호·TTL·Port·ID, 응답 프레임 번호·ICMP Type/Code·quoted fields
응답이 나의 Probe에 해당하는 근거:
불확실성(타임아웃, 필터, 권한, 라우팅, ICMP 차단):
판정: 관측 성공 / 관측 실패 / 통제된 대체 검증 / 미실행
```

**실패 시 대체 실습:** 본인 VM의 제한된 테스트 패킷 또는 공식 Wireshark 예제 pcap에서 Type/Code, TTL, quoted fields를 분석. **실제 외부 traceroute를 관찰했다고 기재하지 않는다.**

공식 근거: [Apple Developer packet trace](https://developer.apple.com/documentation/network/recording-a-packet-trace), [RFC 791](https://www.rfc-editor.org/rfc/rfc791), [RFC 792](https://www.rfc-editor.org/rfc/rfc792), [Linux raw(7)](https://man7.org/linux/man-pages/man7/raw.7.html).
