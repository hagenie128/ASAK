# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-043)

> Status: **HISTORY**
> 인라인 주석 태그: `TODO-NNN`
> **번호 순 = 구현 순서** (주문 → 메뉴 → 품절 → 결제수단 → 매출 → 대시보드 → 로그인 → 환불)
> 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.
> 검색: `TODO-00` / `TODO-0` / `TODO-`
> **갱신: 2026-08-19 18:56 — 실제 소스 `TODO-NNN` 주석과 코드 구현 상태 기준 전체 업데이트**
> 작업 원칙: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행한다.
> 상세 검증: [`admin-verify-todos-2026-08-06.md`](admin-verify-todos-2026-08-06.md)

## 진행 요약 (2026-08-19 기준)

| 상태                         | 인라인 TODO                                                                                        | 비고                                                                         |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| ✅ 완료(주석 제거)           | 구 001~007, 009, 011, 013(기본 TTS), 014                                                           | 8/6 이전 완료                                                                |
| ✅ 구현 완료(TODO 주석 잔존) | **003** (메뉴 POST), **004** (메뉴 삭제 후 선택 정리), **005** (재료 서버 검색), **006** (재료 QA) | BE POST/PATCH/DELETE·FE menusApi 구현됨. 주석은 잔여 QA 메모로 남아 있음     |
| ✅ 구현 완료(TODO 주석 잔존) | **002** (주문 조회 검증)                                                                           | useOrdersQuery empty/error 분리 반영. 필터 쿼리 검증 잔여                    |
| 🟡 부분 구현                 | **015** (매출 summary Controller), **018** (매출 Mapper/Service)                                   | BE summary 엔드포인트·Service·Mapper(vw_sales_daily) 구현. **런타임 미검증** |
| 🟡 부분 구현                 | **016** (매출 monthly)                                                                             | BE 엔드포인트 존재하나 `Collections.emptyList()` 반환 스텁                   |
| ⬜ TODO 주석 잔존·미구현     | **001** (APPROVED 취소 정책), **017** (daily 매출), **023** (dashboard)                            |                                                                              |
| ⬜ TODO 주석 잔존·미구현     | **007~010** (품절 Controller/Service/Mapper/FE)                                                    |                                                                              |
| ⬜ TODO 주석 잔존·미구현     | **011~014** (결제수단 Controller/Service/FE API/draft)                                             |                                                                              |
| ⬜ TODO 주석 잔존·미구현     | **019~022** (매출 FE getSummary/getMonthly/getDaily/useSalesQuery)                                 | salesApi.js 빈 셸                                                            |
| ⬜ TODO 주석 잔존·미구현     | **024~026** (dashboard FE)                                                                         |                                                                              |
| ⬜ TODO 주석 잔존·미구현     | **027~037** (로그인·JWT·보호 경로)                                                                 |                                                                              |
| ⬜ TODO 주석 잔존·미구현     | **038~043** (환불·영수증)                                                                          | 정책 결정 선행                                                               |

## 2026-08-20 관리자 TODO 기준 일정

> 기존 8/5~8/6 기록과 번호 재매핑은 **이력으로 보존**한다. 아래 일정의 번호 정본은 `ASAK-back`과 `ASAK-Admin` 소스에 실제로 남아 있는 `TODO-NNN` 주석이다.
>
> **오늘(8/20)의 최우선은 RTOS 최소 흐름을 거의 끝내는 것**이다. 8/21에는 새 RTOS 기능을 만들지 않고 시연 재현과 오류 보완만 한다. 기능 상세는 표에 넣지 않고 아래 TODO에서 확인한다.

| 날짜 | 관리자 작업 | 짧은 완료 표시 |
| --- | --- | --- |
| **8/19 ✅** | 매출 summary 골격 (`015`, `018`) | summary 코드 존재. 런타임 검증은 남음 |
| **8/20** | **RTOS 구현 마감** + 매출 최소 진행 | RTOS 이벤트 1건 E2E 통과, 매출은 백엔드·화면 진행 상태 기록 |
| **8/21 (금)** | RTOS 시연 재현·오류 보완 | 같은 E2E 흐름을 다시 통과하고 시연 증거 남김 |
| **8/24** | 대시보드 BE·FE (`023~025`) | 대시보드 API 1회와 화면 표시 확인 |
| **8/25** | 결제수단 (`011~014`) | 목록 조회와 토글 저장 확인 |
| **8/26** | 품절·메뉴 QA (`003~010`) | 저장 1건과 실패 1건 확인 |
| **8/27** | 로그인·보호 경로 (`027~037`) | 로그인 후 보호 화면 진입 확인 |
| **8/28** | 환불·영수증·통합 QA (`001`, `038~043`) | 정책 결정 또는 보류 기록 |
| **8/31~9/01** | 발표 전 회귀·문서 | 시연 흐름과 미완료 목록 확인 |

### 8/20 상세 TODO — RTOS 구현 마감 (최우선)

1. WSL 홈 `~/ASAK-RTOS`에서 빌드·실행 명령을 확인하고, Spring Boot `8080`에 연결한다.
2. 관리자 영수증 재출력 요청으로 이벤트 1건을 만든다: `POST /api/admin/orders/{orderId}/receipt-print`.
3. RTOS가 `GET /api/rtos/device-events/pending`으로 그 이벤트를 한 번만 가져오는지 확인한다.
4. RTOS 콘솔에서 영수증 출력 결과를 확인한다.
5. RTOS가 `PATCH /api/rtos/device-events/{eventId}/finish`로 처리 결과를 보낸다.
6. Admin 조회 결과에서 같은 `eventId`의 최종 상태를 확인한다.
7. 성공 요청·콘솔 출력·최종 상태를 캡처 또는 작업 기록으로 남긴다.

**오늘 종료선:** 위 1~6이 한 번 이어서 통과하면 RTOS 구현은 거의 완료로 보고, 8/21은 재현·오류 수정만 한다. React 상태 표시 위치가 아직 없으면 새 화면을 만들지 말고, 기존 Admin 이벤트 조회에서 실제 상태 확인까지를 오늘의 최소 범위로 한다.

### 8/21 동영상 시연의 큰 흐름

1. **관리자**가 주문의 영수증 재출력 버튼을 누른다.
2. Spring Boot가 영수증 출력 이벤트를 만들고, Admin 조회에서 `PENDING` 상태를 보여 준다.
3. **RTOS**가 pending 이벤트를 polling으로 가져와 영수증 내용을 콘솔에 출력한다.
4. RTOS가 처리 완료를 Spring Boot에 보고한다.
5. **관리자**가 같은 이벤트의 완료 상태를 다시 확인한다.

> 동영상에서는 주문 생성·결제까지 새로 보여 주려 하지 않는다. 이미 존재하는 주문 1건을 사용해 `관리자 요청 → 서버 이벤트 → RTOS 출력 → 관리자 완료 확인`을 끊기지 않게 보여 준다.

### 8/20 병행 TODO — 매출 API와 관리자 화면

**백엔드 (`015~018`)**

1. `summary`의 날짜 범위와 빈 기간 응답을 먼저 고정한다.
2. `monthly`가 선택한 연도·월의 **일자 목록**을 반환하도록 Controller → Service → Mapper를 연결한다.
3. `daily`에 `date`, `intervalMinutes(30|60)`를 받고, 30분 View 집계와 영업시간 내 0-fill을 Service에서 처리한다.
4. Bruno 요청을 `summary`, `monthly`, `daily` 계약에 맞춘다. 실제 DB View 적용 여부는 별도로 기록한다.

**프런트 (`019~022`)**

1. `salesApi.js`에 summary·monthly·daily 요청 메서드를 추가한다.
2. 응답의 `ApiResponse.data`와 빈 배열을 같은 형태로 정리한다.
3. `useSalesQuery`의 mock을 매출 API 호출로 교체한다.
4. 일별 화면은 날짜 변경, 30/60분 전환, Loading·Empty·Error를 각각 확인한다.

### 8/21 상세 TODO — RTOS 시연 재현·오류 보완

1. 8/20과 같은 이벤트 흐름을 처음부터 다시 실행한다.
2. 실패하면 실패 지점을 `이벤트 등록 / polling / 콘솔 출력 / finish 보고 / Admin 조회` 중 하나로만 분류한다.
3. 수정 뒤 같은 이벤트 ID 흐름을 다시 확인한다.
4. React 상태 표시는 기존 화면에 넣을 위치가 확정된 경우에만 연결한다. 새 화면 설계는 이 일정에 추가하지 않는다.

**시연 완료 표시:** 이벤트 1건의 상태가 `PENDING → PROCESSING → 완료 상태`로 바뀌고, RTOS 콘솔 출력과 Admin 조회 결과가 같은 이벤트 ID를 가리킨다.

### RTOS 연동 원칙

- RTOS 작업은 Admin과 Kiosk로 기능을 분할하지 않는다. 하나의 이벤트 계약과 하나의 React 표시 흐름을 기준으로 서버·화면·콘솔을 함께 확인한다. 저장소/화면 통합 방식은 팀이 결정해야 하며, 이 일정은 저장소 병합을 지시하지 않는다.
- **8/21 금요일 테스트 시연**은 위 상세 TODO 1~5 순서대로 한다. WSL의 `~/ASAK-RTOS` 실행 또는 Admin 화면 표시 위치가 없으면, 시연 완료가 아니라 `선행 조건 미충족`으로 기록한다.
- RTOS 저장소: WSL 홈 `~/ASAK-RTOS` (독립 저장소, `hagenie128/ASAK-RTOS`)
  - `src/main.c` — FreeRTOS CommandPollTask(1초 polling) → WorkerTask → handle_print_receipt(콘솔 ASCII 영수증) → report_result(PATCH finish)
  - `src/http_client.c` — POSIX TCP 연결, HTTP 요청/응답, chunked body 처리
  - Spring Boot API: `GET /api/rtos/device-events/pending` → `PATCH /api/rtos/device-events/{eventId}/finish`
  - 현재 payload: `주문번호|메뉴요약|금액` 파이프 구분 문자열. JSON DTO 전환은 미확정.
  - WSL Ubuntu에서 `make run SERVER_URL=http://$HOST_IP:8080`으로 실행. Windows Spring Boot 8080과 연결.

### 실제 인라인 TODO 묶음과 위치

| 묶음             | TODO             | API 계약                                                                      | 실제 위치                                                                                                                                                                                                                                                   |
| ---------------- | ---------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 주문 환불·영수증 | `001`, `038~043` | 번호 미연결 · `API-024` 취소와 별도 환불 계약 필요                            | `AdminOrderService`·`AdminOrderController`·`AdminOrderMapper.xml` / `ordersApi.js`·`OrderManagePage.jsx`                                                                                                                                                    |
| 메뉴 잔여 QA     | `003~006`        | `API-012` POST · `API-013` PATCH · `API-028` DELETE                           | `AdminMenuController`(POST `createMenu` + PATCH `updateMenu` + DELETE soft delete) / `MenuManagePage.jsx`·`MenuEditPanel.jsx` — **BE·FE 구현 완료, 브라우저 E2E·Figma 미검증**                                                                              |
| 품절             | `007~010`        | `API-009` PATCH · `API-010` GET                                               | `AdminSoldOutController`·`AdminSoldOutService` / `soldOutApi.js`·`useSoldOutDraft.js` — `targetType` 분기(menu/ingredient), `is_sold_out` 토글 UPDATE, 실패/롤백 기준 정리 필요                                                                             |
| 결제수단         | `011~014`        | `API-015` GET · `API-016` PATCH                                               | `AdminPaymentMethodController`·`AdminPaymentMethodService` / `paymentMethodsApi.js`·`usePaymentMethodDraft.js` — `active` 필드 통일 결정(8/18) 반영 필요                                                                                                    |
| 매출·대시보드    | `015~025`        | `API-017` summary · `API-018` daily · `API-019` monthly · `API-020` dashboard | `AdminSalesController`(summary 구현, monthly 스텁, daily 미구현)·`AdminSalesService`(vw_sales_daily·vw_sales_hourly·topMenu 4개 SELECT)·`AdminSalesMapper.xml` / `salesApi.js`(빈 셸)·`useSalesQuery.js`(mock)·`adminApi.js`(빈 셸)·`useDashboard.js`(mock) |
| 로그인·보호 경로 | `027~037`        | 번호 미연결 · `POST /api/admin/login` 스텁                                    | `AdminAuthController`·`JwtTokenProvider`·`JwtAuthenticationFilter`·`SecurityConfig` / `adminApi.js`·`adminSession.js`·`apiClient.js`·`useAdminAuth.js`·`LoginPage.jsx`                                                                                      |
| RTOS 장치 이벤트 | 번호 미연결      | `GET /api/rtos/device-events/pending` · `PATCH .../finish`                    | `ASAK-back`: `AdminDeviceEventController` src 존재 확인. RTOS는 WSL 홈 `~/ASAK-RTOS`에 있음(실행 검증 대기). React 이벤트 표시 컴포넌트 미확정                                                     |

### 일정 해석 메모

- 이 표는 구현 완료를 뜻하지 않는다. `TODO-NNN`이 소스에 남아 있는 항목만 일정에 넣었다.
- 번호는 재사용·재배치하지 않는다. 백엔드 선행 항목이 끝나기 전 프런트 API 호출을 추가하지 않는다.
- 환불·영수증은 상태 전이와 책임 경계 결정이 선행 조건이다. `8/28`까지 결정되지 않으면 발표 전 구현 항목이 아니라 `결정 필요`로 남긴다.
- RTOS 인라인 TODO 번호는 아직 부여하지 않았다. 기존 `API-019` 표기는 월별 매출 API와 충돌하므로 사용하지 않는다. RTOS 관련 API 번호는 팀 합의 후 부여한다.

---

## 영역별 상세 (2026-08-19 코드 기준)

### P1 · 주문 잔여 (통합 테스트와 함께)

| #       | 상태    | 위치                            | 할 일                                                                                 |
| ------- | ------- | ------------------------------- | ------------------------------------------------------------------------------------- |
| **001** | 🟡 미결 | `AdminOrderService.cancelOrder` | ① APPROVED 취소 정책 확정 ② 환불 흐름 분리 여부 결정 ③ Controller/ErrorCode 기준 정리 |
| **002** | ✅ 구현 | `useOrdersQuery.js`             | empty/error 분리 반영. 필터 쿼리 정합 검증 잔여                                       |

### P2 · 메뉴 (003~006) — SCR-016

| #       | 상태    | 위치                                    | 할 일                                                                                                                                                            |
| ------- | ------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **003** | ✅ 구현 | `AdminMenuController` POST·PATCH·DELETE | BE POST(CreateMenuRequest+검증), PATCH(menuId+body), DELETE(soft delete) **모두 구현**. FE `menusApi` create/update/delete 연결됨. **브라우저 E2E·Figma 미검증** |
| **004** | ✅ 구현 | `MenuManagePage.jsx`                    | 삭제 후 선택 상태 정리 로직 존재. QA 잔여                                                                                                                        |
| **005** | 🟡 잔여 | `MenuEditPanel.jsx`                     | 재료 목록 서버 검색·페이지 처리 잔여 QA                                                                                                                          |
| **006** | 🟡 잔여 | `MenuEditPanel.jsx`                     | 재료 추가·저장 수동 QA 잔여                                                                                                                                      |

### P3 · 품절 (007~010) — SCR-011

> 스크린샷 참조: 품절 상세 검증(`P3-1`~`P3-4`)은 아래 번호를 32~39로 세분화한 이전 검증표 기준이다. 현재 인라인 번호는 007~010으로 통합되어 있다.

| #       | 상태 | 위치                                               | 할 일                                                                                                                                                                   |
| ------- | ---- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **007** | ⬜   | `AdminSoldOutController.java`                      | ① GET 응답 ② PATCH 바인딩 ③ `ErrorCode` 규격 정리. `SoldOutPatchRequest.java`의 DTO 필드(`targetType`, `targetId`, `isSoldOut`)는 ✅ 완료 상태.                         |
| **008** | ⬜   | `AdminSoldOutService` / `AdminSoldOutMapper` + XML | ① 대상별 SELECT ② 공통 row shape 정리 ③ XML 추가. ④ `targetType` 분기 ⑤ `is_sold_out` 토글 UPDATE ⑥ 변경 건수 반환. ⑦ 조회 메서드 ⑧ patch 메서드 ⑨ 실패/롤백 기준 정리. |
| **009** | ⬜   | `soldOutApi.js`                                    | ① `listSoldOutCatalog()` 추가 ② 초기 load 연결. ③ `patchSoldOut(body)` 추가 ④ body 규격 정리.                                                                           |
| **010** | ⬜   | `useSoldOutDraft.js`                               | ① mock load 교체 ② mock save 교체 ③ baseline 롤백 유지.                                                                                                                 |

### P4A · 결제수단 (011~014) — SCR-018

> `active` 필드 통일 결정(8/18): Lombok `boolean isEnabled` → Jackson이 `enabled`로 직렬화하여 FE에서 `method.isEnabled`가 `undefined`로 깨지는 이슈. `active`로 통일하기로 합의.

| #       | 상태 | 위치                                 | 할 일                                                                                                          |
| ------- | ---- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **011** | ⬜   | `AdminPaymentMethodController`       | Controller 구현. GET 목록 + PATCH 토글. `active` 필드 기준으로 Kiosk 8종 결제수단과 정합.                      |
| **012** | ⬜   | `AdminPaymentMethodService` / Mapper | Service/Mapper/DTO 구현. `pay_method_cfg.active` 기준 토글. DTO에서 `isEnabled` 사용 금지(Lombok 직렬화 이슈). |
| **013** | ⬜   | `paymentMethodsApi.js`               | GET 목록·PATCH 연결. 응답 필드 `active` 기준으로 FE 바인딩.                                                    |
| **014** | ⬜   | `usePaymentMethodDraft.js`           | mock → API 교체. Figma 4종(card/kakao/naver/zero) + Kiosk 8종 정합 TODO.                                       |

### P4B · 매출 (015~022) — SCR-019/020/021

| #       | 상태    | 위치                                         | 할 일                                                                                                                                         |
| ------- | ------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **015** | 🟡 부분 | `AdminSalesController`                       | summary 엔드포인트 구현됨. 날짜 validation·빈 기간 응답 정리 잔여. **런타임 미검증**                                                          |
| **016** | 🟡 스텁 | `AdminSalesController`                       | monthly 엔드포인트 존재하나 `Collections.emptyList()` 반환. 실제 집계 미구현                                                                  |
| **017** | ⬜      | `AdminSalesController`                       | daily 엔드포인트 미구현                                                                                                                       |
| **018** | 🟡 부분 | `AdminSalesService` + `AdminSalesMapper.xml` | summary(vw_sales_daily), hourly(vw_sales_hourly), topMenu(daily/hourly) 4개 SELECT 구현. monthly·dashboard 집계 미구현. **DB 뷰 존재 미검증** |
| **019** | ⬜      | `salesApi.js`                                | getSummary — 빈 셸                                                                                                                            |
| **020** | ⬜      | `salesApi.js`                                | getMonthly — 빈 셸                                                                                                                            |
| **021** | ⬜      | `salesApi.js`                                | getDaily — 빈 셸                                                                                                                              |
| **022** | ⬜      | `useSalesQuery.js`                           | mock → API 교체                                                                                                                               |

### P4C · 대시보드 (023~025) — SCR-022

| #       | 상태 | 위치                   | 할 일                       |
| ------- | ---- | ---------------------- | --------------------------- |
| **023** | ⬜   | `AdminSalesController` | dashboard 엔드포인트 미구현 |
| **024** | ⬜   | `adminApi.js`          | getDashboard — 빈 셸        |
| **025** | ⬜   | `useDashboard.js`      | mock → API 교체             |

### 보류 · Live UX · TTS · 인증 · Future

| #       | 상태      | 위치                           | 할 일         |
| ------- | --------- | ------------------------------ | ------------- |
| **026** | ⬜ 보류   | `LiveOrderBoard.jsx`           | 가로 스크롤   |
| **027** | ⬜        | `AdminAuthController`          | POST /login   |
| **028** | ⬜        | `JwtTokenProvider.java`        | JWT           |
| **029** | ⬜        | `JwtAuthenticationFilter.java` | 필터          |
| **030** | ⬜        | `SecurityConfig.java`          | authorize     |
| **031** | ⬜        | `adminApi.js`                  | login         |
| **032** | ⬜        | `adminSession.js`              | token         |
| **033** | ⬜        | `apiClient.js`                 | Bearer + 401  |
| **034** | ⬜        | `LoginPage.jsx`                | 실로그인      |
| **035** | ⬜        | `useAdminAuth.js`              | 401 가드      |
| **036** | ⬜        | `AdminApp.jsx`                 | 정본 경로     |
| **037** | ⬜        | `apiClient.js`                 | 403 매핑      |
| **038** | ⬜        | `AdminOrderController`         | 환불 endpoint |
| **039** | ⬜        | `AdminOrderMapper.xml`         | 환불 SQL      |
| **040** | ⬜ Future | `ordersApi.js`                 | refundOrder   |
| **041** | ⬜ Future | `ordersApi.js`                 | printReceipt  |
| **042** | ⬜ Future | `OrderManagePage.jsx`          | 환불 UI       |
| **043** | ⬜ Future | `OrderManagePage.jsx`          | 영수증 UI     |

---

## 이력

### 번호 재매핑 (2026-08-06 → 2026-08-19)

8/6에 TODO 번호를 재배치(032~048 → 015~031 등)한 뒤, 8/19에 인라인 주석을 구현 순서대로 001~043으로 재정리했다. 구 번호와 신 번호의 대응은 소스 커밋 `6f4201f`(ASAK-back)·`c08190f`(ASAK-Admin) 참조.

### 진행 로그

| 날짜       | 내용                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-08-06 | 메뉴 조회 먼저 재정렬. Empty/Error·Live 빈목록 수정.                                                                                             |
| 2026-08-06 | 메뉴 조회 실연동: `useMenusQuery` PageResult 기준 연동.                                                                                          |
| 2026-08-06 | 문서·DevCopilot 동기화. 주문 BE/FE 연동 구현됨·미검증.                                                                                           |
| 2026-08-11 | 관리자 메뉴 상세·영양·재료·soft delete API 구현. Admin FE 연동.                                                                                  |
| 2026-08-14 | AdminMenuMapper·AdminOptionMapper 분리. 빌드 성공(8/13 WIP 해소).                                                                                |
| 2026-08-18 | 결제 계약 정합화(`active` 통일). READY 주문 버튼 비활성화.                                                                                       |
| 2026-08-19 | 매출 summary Controller+Service+Mapper 구현. monthly 스텁. DTO 패키지 정리. TODO 001~043 재정리. 기기 출력 이벤트 API 추가(build만, src 미반영). |

## 사용법

1. IDE TODO 패널을 번호순으로 보면 **구현 순서**와 같다.
2. 각 기능은 **화면–API–DB**를 함께 확인한 뒤 다음 번호로 넘어간다.
3. 완료한 항목은 인라인 주석을 지우고, 이 표 상태를 ✅로 갱신한다.
4. 이 표와 코드 주석이 어긋나면 **코드 인라인을 정본**으로 맞춘다.
