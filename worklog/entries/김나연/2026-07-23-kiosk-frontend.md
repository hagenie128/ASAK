# 2026-07-23 키오스크 공통 UI·레이아웃·고객 API·주문·메뉴·관리자 주문·Live·TTS

> **일일 기록:** [2026-07-23 daily](../../daily/김나연/2026-07-23.md)
> **근거:** Git 커밋·`git show --stat`·변경 파일. **코드 커밋 ≠ 통합 검증 완료.**

---

## 1. 기본 정보

- 작업 날짜: 2026-07-23
- 담당자: 김나연
- 저장소: `ASAK-Kiosk` / `ASAK-back`
- 브랜치: remotes/origin/ai-review/api-contract-alignment-20260723~3, remotes/origin/ai-review/api-contract-alignment-20260723~4, remotes/origin/ai-review/api-contract-alignment-20260723~5
- 관련 이슈/PR/화면: API-005
- 작업 유형: `feature` / `fix` / `chore`
- 구현 근거: `dcdf676`, `152a53b`, `dc47377`, `a0e98ca`, `37c73c9`, `6457765`, `76fda07`, `524c199`, `a9f19e7`
- Figma 기준: 당일 커밋에 Figma 노드 추가/변경 evidence가 명시되지 않으면 `Figma 미확인`으로 둔다. UI 커밋이 있어도 상태별(Frame/Loading/Empty/Error) 재대조는 별도 검증이다.
- 완료 판정: 커밋 반영은 확인. **Gradle/npm/Bruno/브라우저/실DB 통합 결과는 이 기록에서 재실행하지 않음.**

## 2. 작업 목적

- ASAK-Kiosk / ASAK-back에서 확인된 당일 작업을 **키오스크 공통 UI·레이아웃 · 고객 API·주문·메뉴 · 관리자 주문·Live·TTS** 단위로 정리한다.
- 고객(`user`) 도메인 API가 키오스크 계약(필드명·상태값)과 어긋나지 않게 Mapper/DTO/서비스를 맞춘다.
- 키오스크 주문 세션(유형→메뉴→옵션→장바구니→결제)에서 끊기지 않는 UI/상태 흐름을 맞추는 것이 목표다.
- mock/화면/API/문서 중 실제로 손댄 경계를 커밋·파일로 구분해, 다음 실연동·검증 범위를 남긴다.
- 완료 판정은 코드 반영과 분리한다. 통합 테스트·브라우저·실DB 증거가 없으면 미검증으로 둔다.

## 3. 직접 구현 영역

Git 커밋 이력으로 다음 직접 작업을 확인했다.

- **키오스크 공통 UI·레이아웃:**
  - `dcdf676` update: kiosk_scale add
  - 주요 파일: `src/apps/kiosk/KioskApp.jsx`, `src/styles/kiosk/base.css` (`dcdf676`)
- **고객 API·주문·메뉴:**
  - `6457765` update : api-005 작업 백업
  - `76fda07` update: common ApiResponse 응답 추가
  - `524c199` update: user/controller 각각 service연결작업 & paymentService생성
  - `a9f19e7` update : swagger_config 및 라이브러리 설치
  - 주요 파일: `src/main/java/com/asak/user/dto/CreateOrderRequest.java`, `src/main/java/com/asak/user/dto/CreateOrderResponse.java`, `src/main/java/com/asak/user/dto/OptionItemRequest.java`, `src/main/java/com/asak/user/dto/OrderItemRequest.java`, `src/main/java/com/asak/user/dto/request.java`, `src/main/java/com/asak/user/dto/response.java`, `src/main/java/com/asak/common/response/ApiResponse.java`, `src/main/java/com/asak/user/controller/UserMenuController.java` 외 7개 (`6457765`, `76fda07`, `524c199`, `a9f19e7`)
- **관리자 주문·Live·TTS:**
  - `152a53b` fix : 파일 구조 수정 -  xml파일 위치 java -> resources로 이동
  - `dc47377` fix: admin/ user  mapper -> class에서 interface로 수정
  - `a0e98ca` update : xml파일들 기본 xml 틀 적용
  - `37c73c9` update : common 공통 파일에 eunms 상수 추가
  - 주요 파일: `README.md`, `src/main/resources/application.properties`, `src/main/resources/mappers/AdminMenuMapper.xml`, `src/main/resources/mappers/AdminOrderMapper.xml`, `src/main/resources/mappers/UserMenuMapper.xml`, `src/main/resources/mappers/UserOrderMapper.xml`, `src/main/java/com/asak/admin/mapper/AdminMenuMapper.java`, `src/main/java/com/asak/admin/mapper/AdminOrderMapper.java` 외 8개 (`152a53b`, `dc47377`, `a0e98ca`, `37c73c9`)

## 4. 구현 로직 / 적용한 방식

- **근거 순서:** Git 커밋·변경 파일 → 현재 코드 경로 → (있으면) Screen/API 문서. Product Bible과 코드가 다르면 코드/실측을 우선하고 문서는 별도 TODO로 남긴다.
- **저장소 경계:** ASAK-Kiosk / ASAK-back. 프론트·백엔드·문서 커밋이 섞이면 영역별로 나눠 기록한다.
- **키오스크 공통 UI·레이아웃:** Header/Footer/Stepper/공통 CSS로 화면 간 레이아웃을 맞췄다. 대표 파일: `KioskApp.jsx`, `base.css`.
- **고객 API·주문·메뉴:** Controller→Service→Mapper(XML)→DTO 흐름으로 고객 메뉴/주문 API를 보강했다. 대표 파일: `CreateOrderRequest.java`, `CreateOrderResponse.java`, `OptionItemRequest.java`, `OrderItemRequest.java`.
- **관리자 주문·Live·TTS:** Admin 주문 상태 전이/취소 가드·Live/TTS/TODO 정리처럼 운영 흐름 쪽을 다뤘다. 대표 파일: `README.md`, `application.properties`, `AdminMenuMapper.xml`, `AdminOrderMapper.xml`.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: `2026-07-23` 작업을 2026-07-23 API 계약 entry 수준의 12섹션 상세 기록으로 재작성하도록 요청했다.
- AI가 도움 준 내용: 커밋·파일 목록 수집, 영역 분류, 이슈/TODO/검증 문장 구조화.
- 그대로 사용한 부분: 커밋 해시, 메시지, 변경 파일 경로, stat 요약.
- 수정해서 사용한 부분: 서술 문장·영역 묶음. 원 구현 시점의 AI 사용 여부와 런타임 로그는 커밋만으로 복원하지 않았다.

## 6. 발생 이슈

### 이슈 1 — 백업/WIP 커밋과 기능 커밋이 같은 날에 섞임

- 증상: 커밋 메시지에 백업·작업중 표현이 있어 최종 상태와 중간 스냅샷 구분이 필요하다.
- 원인: 화면/API를 이어 붙이는 동안 안전한 지점을 자주 커밋했다.
- 해결: 이 기록에서는 WIP를 중간 스냅샷으로만 해석하고, 완료 판정은 통합 검증 전으로 남긴다.

### 이슈 — 프론트·백엔드가 같은 날 움직여도 실연동 증거는 별개

- 증상: 키오스크와 백엔드 커밋이 함께 있어도 Network 탭/Bruno 성공 로그가 없으면 연동 완료로 볼 수 없다.
- 원인: 저장소·실행 환경이 분리되어 있다.
- 해결: `구현 진행`으로 두고 adapter·실DB 검증을 TODO로 분리한다.

### 이슈 — 스펙/코드 불일치를 fix 커밋으로 맞춤

- 증상: 필드명·경로·SQL·UI 상태 중 일부가 명세 또는 화면과 달랐다.
- 원인: mock·문서·API가 병렬로 진화했다.
- 해결: fix 커밋의 변경 파일 기준으로 정합을 맞췄다. 회귀 테스트는 별도 실행이 필요하다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| 당일 커밋 | 9건 (`dcdf676` … `a9f19e7`) | 각 저장소 `git log --since/--until` |
| 키오스크 공통 UI·레이아웃 | 커밋 1건 · 파일 2+ | `src/apps/kiosk/KioskApp.jsx` |
| 고객 API·주문·메뉴 | 커밋 4건 · 파일 15+ | `src/main/java/com/asak/user/dto/CreateOrderRequest.java` |
| 관리자 주문·Live·TTS | 커밋 4건 · 파일 16+ | `README.md` |
| 실행 검증 | 이 entry 보강 시점에 Gradle/npm/Bruno/브라우저 재실행 없음 | 저장소별 test/build · Network 탭 |

## 8. 이번 작업에서 배운 점

1. 화면이 보이는 것과 API/DB까지 연결된 것은 다른 완료 기준이다. 커밋 수만으로 DONE을 올리지 않는다.
2. 같은 날의 백업 커밋과 기능 커밋을 구분해야 포트폴리오 설명이 정확해진다.
3. 변경 파일 목록이 있어야 메뉴/장바구니/결제/Admin 같은 단위로 작업을 설명할 수 있다.
4. 백엔드는 Controller/Service/Mapper/DTO를 한 줄로 묶어 수직 슬라이스 단위로 검증하는 편이 안전하다.
4. 키오스크는 공통 Footer/Header/Stepper와 페이지 상태가 어긋나면 결제 직전 UX가 바로 깨진다.

## 9. 개선사항 / TODO

- [ ] 관련 화면을 브라우저에서 Loading/Empty/Error까지 수동 확인
- [ ] 실연동 구간이면 Bruno 또는 Network 탭으로 요청/응답 envelope 확인
- [ ] 필드명(`totalAmount`, `CANCELED`, `EAT_IN`/`TAKE_OUT` 등) 정본과 불일치 여부 재대조
- [ ] `ASAK-back`에서 `./gradlew test` 또는 최소 bootRun 스모크
- [ ] 해당 FE 저장소 `npm run build` 회귀
- [ ] 메뉴 조회→장바구니→주문 생성 경로를 실DB fixture로 한 사이클 확인

## 10. 검증 내용

- 실행한 명령어:
  - `git log --since/--until` (ASAK-Kiosk / ASAK-back)
  - `git show --stat --name-only <commit>`
- 테스트한 시나리오:
  - Git evidence로 영역별 변경 범위 확인
  - 기능 시나리오(주문 완료, Admin 상태 변경, 실DB 저장 등)는 **미실행**
- 확인 결과:
  - 2026-07-23 작성자 커밋 **9건**과 영역별 파일 목록을 확인했다.
  - 이 entry 작성/보강 시점에는 자동 테스트·실서버 호출·E2E 성공 결과를 새로 확보하지 않았다.

## 11. 포트폴리오용 요약

2026-07-23 김나연 작업은 ASAK-Kiosk / ASAK-back에서 키오스크 공통 UI·레이아웃 · 고객 API·주문·메뉴 · 관리자 주문·Live·TTS 범위를 커밋 9건으로 진행한 기록이다. 변경 파일과 영역 경계를 기준으로 설명하고, 통합 테스트·실DB·브라우저 검증은 완료로 과장하지 않았다.

## 12. 첨부하면 좋은 자료

- 일일 기록: [2026-07-23 daily](../../daily/김나연/2026-07-23.md)
- 관련 커밋: `dcdf676`, `152a53b`, `dc47377`, `a0e98ca`, `37c73c9`, `6457765`, `76fda07`, `524c199`, `a9f19e7`
- 변경이 큰 경로: `src/apps/kiosk/KioskApp.jsx`, `src/styles/kiosk/base.css`
