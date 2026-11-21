# 학습 세션·Obsidian·코드 리뷰 템플릿

> 일자·환경·코드·실측·오답을 남겨 학습이 대화를 넘어 계속될 수 있도록 한다. '안 했다'를 체크해도 괜찮지만 '안 했는데 성공'은 금지.

## Antigravity CLI용 시작 템플릿

JetBrains IDE에서 **Git 루트**를 확인하고 `agy`를 실행한 뒤 다음을 입력한다.

```text
my_traceroute 학습을 이어가자.
루트 AGENTS.md와 roadmap/state.json, roadmap/curriculum.json,
roadmap/08-session-protocol.md, 현재 roadmap/weeks/Wxx.md를 확인해.
roadmap/01-progress.md는 과거 ChatGPT 이력으로만 참고해.
로컬 Rust crate와 Git 상태를 읽기만 하되 자동으로 수정하지 마.
현재 이해한 부분/미검증 항목/다음 한 과제만 정리하고 내 답을 기다려.
완성 코드는 공개하지 말고 내가 먼저 구현하도록 H0/H1 힌트를 사용해.
```

수업 종료 시 학생이 제공한 증거를 정리해 `state.json`/`journal/Wxx.md` **변경안을 먼저 제시**하고, 승인 후에만 저장하도록 한다. [CLI 사용 가이드](07-antigravity-cli.md)와 [세션 계약](08-session-protocol.md) 참고.

## A. 다음 차시 시작 프롬프트

```text
나는 dev-kdy/my_traceroute 저장소의 Rust 초보 학습자야.
먼저 루트 README.md, roadmap/README.md, roadmap/01-progress.md 및
현재 roadmap/weeks/Wxx.md를 읽고 이 학습을 이어가줘.
프로젝트 기준은 12주·24차시, 현재는 Wxx-Lx [진행 중/보충 필요].
내가 마지막으로 직접 작성한 함수/코드:
확인된 명령/종료 코드:
오답·미해결:
다음에 할 단일 과제:
한 번에 하나만 내고, 내가 제출하기 전에는 정답 코드를 공개하지 마.
C 함수의 전체 호출/분기·상태를 먼저 지도화하고 해당 차시 부분을 깊이 분석해줘.
Java와 비교하고, 패킷 증거가 없으면 미검증이라고 표시해줘.
```

## B. 차시별 노트(Obsidian Markdown 복사)

```markdown
---
project: my_traceroute
week: Wxx
lesson: Lx
date: YYYY-MM-DD
status: in-progress
environment: macOS-or-Ubuntu
rust_version: ""
edition: unknown
git_commit: ""
---
# Wxx-Lx — 주제

## 학습 목표 — 내 말로
1.
2.

## 선수 개념 확인
- 질문/내 답:
- 틀린 부분/반례:

## Rust 개념과 Java 비교
| 키워드(영어) | 정의 | Java 비슷한 점 | 중요한 차이 | traceroute 적용 |
|---|---|---|---|---|

## 네트워크 개념/공식 근거
- IPv4/UDP/ICMP 필드:
- RFC 번호/절:
- 그림/상태 전이:
- 내 예상:

## C 원본 분석
- 파일/함수/원본 링크/커밋:
- 함수 전체 호출/분기 지도:
- 변경하는 상태:
- 경계/오류 반환:
- 직접 확인한 사실:
- 아직 검증하지 않은 위험 가설:

## Rust 직접 구현
- 수정한 파일/함수:
- 입력·출력·오류 계약:
- 왜 이 타입을 선택했는가:
- 내가 작성한 핵심 코드:
- 다른 설계 선택/트레이드오프:

## 테스트·실행 기록
| 명령과 입력 | 예상 | 실제 stdout/stderr·exit code | 판정 |
|---|---|---|---|

## 패킷 관측 또는 통제 대체 검증
- 허가된 대상/인터페이스/환경:
- capture filter / display filter:
- 송신 TTL·포트·ID·Sequence:
- 응답 ICMP Type/Code·quoted header:
- 해당 Probe에 연결한 근거:
- 예상과 다른 점·불확실성:

## 오류·해결
- 초기 오류:
- 가장 작은 재현:
- 내 수정:
- 재검증 로그:

## 확인 문제 및 오답
- Rust 1:
- 네트워크 1:
- 네트워크 2:
- C/Rust 독해 1:
- 도움 요청 수준(H0~H5):
- 새로운 문제로 재평가:

## 아직 이해하지 못한 내용
-
## 다음 차시로 갈 조건
- [ ] 확인한 증거:
- [ ] 보충할 사항:
- 다음 한 개의 실습:
```

## C 함수 독해 템플릿

```text
원본 경로·링크:
함수명·파라미터 타입·반환 타입:
호출하는 함수/호출받는 곳:
정상/오류/타임아웃 분기 전체:
변경되는 mgr/msg/pkt/resp_buf 필드:
실제 버퍼에 복사되는 시점:
네트워크에서 검증되지 않은 가정:
가능한 테스트 벡터:
Rust로 남길 의미와 개선할 안전성:
```

## 코드 리뷰 요청 프롬프트

```text
내가 작성한 코드만 기반으로 리뷰해줘.
1. 첫 컴파일/타입·소유권·가변성 문제
2. 전제 조건·상태 전이·함수 역할
3. 바이트/경계/ICMP Type/Code/Quoted Probe 검증
4. 가장 작은 수정 힌트(H1 단계)를 하나만
5. 재현할 정상/경계/오류 테스트 3개
실행하지 않았다면 미검증. 전체 수정 코드는 요청할 때만 제공해줘.
```

## Git 운영과 주차 종료

- `learn(w01): verify ttl simulation and cargo checks`처럼 **자기 구현 단위**로 커밋.
- `target/`은 무시하고 Binary crate의 `Cargo.lock`은 커밋. 캡처 파일은 민감정보 확인 후 보관 여부 결정.
- 코드 커밋·test 성공·프로토콜 검증·독립 설명·확인 문제를 **각각** 기록.
- Wxx 노트를 닫을 때 [평가표](04-assessment.md)의 **Exit Gate**와 미확인 항목을 갱신.
- 다시 시작할 때는 Wxx 번호만 말하지 말고 **마지막 코드를 어디까지 테스트했는지** 전달한다.
