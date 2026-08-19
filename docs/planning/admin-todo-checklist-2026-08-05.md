# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-076)

> Status: **HISTORY**
> 인라인 주석 태그: `TODO-NNN`
> **번호 순 = 교사 우선순위** (주문 → 메뉴 → 품절 → 결제수단 → 매출 → 대시보드)
> 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.
> 검색: `TODO-00` / `TODO-0` / `TODO-`
> 진행 갱신: 2026-08-06 (오늘 작업 순서 재정렬: 메뉴 조회 먼저)
> 2026-08-18 overlay: 기존 8/5~8/6 TODO 기록은 보존하고, 아래에 **현재 코드 기준 후속 순서**만 덧붙인다.
> 작업 원칙: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행한다.
> 상세 검증: [`admin-feature-verify-todos-2026-08-06.md`](admin-feature-verify-todos-2026-08-06.md)

## 2026-08-19 실제 인라인 TODO 기준 일정

> 기존 8/5~8/6 기록과 번호 재매핑은 **이력으로 보존**한다. 아래 일정의 번호 정본은 `ASAK-back`과 `ASAK-Admin` 소스에 실제로 남아 있는 `TODO-NNN` 주석이다.
>
> `08/17~08/21`의 최우선은 RTOS 최소 연동이다. 이때 RTOS는 Admin과 Kiosk로 나눈 별도 기능이 아니라 **하나의 공통 흐름**으로 다룬다. 대시보드·결제의 앞단/백단 준비는 같은 기간에 병행하고, 기능 완결·피드백 반영·테스트는 `08/24~08/28`에 마감한다.

| 날짜 | 인라인 TODO | 작업 묶음 | 의존 순서·완료 확인 |
|---|---|---|---|
| **8/19** | `015~018`, `023` | RTOS 공통 흐름 설계 + 대시보드 백단 | RTOS 이벤트의 단일 흐름(서버 API → 한 React 화면 → 콘솔)을 정하고, 대시보드 summary·dashboard 응답/집계 기준을 확정한다. |
| **8/20** | `019~025`, `011~012` | **RTOS 테스트 시연 가능 상태 만들기** + 대시보드 앞단 + 결제 백단 | RTOS 이벤트가 React에 보이도록 연결하고, 테스트 시연에 쓸 서버 API·React 표시·콘솔 출력을 한 번 끝까지 재현한다. 대시보드 API 소비 구조와 결제수단 Controller→Service/Mapper를 준비한다. |
| **8/21 (금)** | `013~014` | **RTOS 테스트 시연** + 결제 앞단 | 새 기능 구현보다 RTOS 테스트 시연을 우선한다. 서버 API → React 표시 → 콘솔 출력 순서로 실제 실행 결과를 보여 주고 확인 항목을 남긴다. 결제수단 API→draft 연결은 시연 후 가능한 범위에서 진행한다. |
| **8/24** | `015~025` | 대시보드·매출 기능 마감 | `015~018` 집계 API를 확정하고 `019~022` 매출 화면, `023~025` 대시보드 순으로 연결·검증한다. |
| **8/25** | `011~014` | 결제수단 기능 마감 | `011 → 012 → 013 → 014`의 API·draft·화면 저장과 오류 상태를 검증한다. |
| **8/26** | `003~010` | 메뉴 잔여·품절 | 메뉴 생성/삭제 잔여를 확인한 뒤 `007 → 008 → 009 → 010` 순서로 품절 API·draft 연결을 완결한다. |
| **8/27** | `027~037` | 관리자 로그인·보호 경로 | `027 → 028 → 029 → 030` 백단 인증 뒤 `031~035`, 오류 매핑 `037`을 연결한다. |
| **8/28** | `001`, `038~043` | 환불·영수증 및 통합 QA | 승인 결제 취소·환불 상태 정책을 먼저 결정한다. 미결정이면 구현하지 않고 `결정 필요`로 기록한다. |
| **8/31~9/01** | 미완료만 | 발표 전 회귀·문서 | 남은 TODO의 구현 여부와 API/화면/DB 검증 결과를 구분해 기록한다. |

### 실제 인라인 TODO 묶음과 위치

| 묶음 | TODO | 실제 위치 |
|---|---|---|
| 주문 환불·영수증 | `001`, `038~043` | `AdminOrderService`·`AdminOrderController`·`AdminOrderMapper.xml` / `ordersApi.js`·`OrderManagePage.jsx` |
| 메뉴 잔여 | `003~006` | `AdminMenuController` / `MenuManagePage.jsx`·`MenuEditPanel.jsx` |
| 품절 | `007~010` | `AdminSoldOutController`·`AdminSoldOutService` / `soldOutApi.js`·`useSoldOutDraft.js` |
| 결제수단 | `011~014` | `AdminPaymentMethodController`·`AdminPaymentMethodService` / `paymentMethodsApi.js`·`usePaymentMethodDraft.js` |
| 매출·대시보드 | `015~025` | `AdminStatsController`·`AdminStatsService`·`AdminStatsMapper` / `salesApi.js`·`useSalesQuery.js`·`adminApi.js`·`useDashboard.js` |
| 로그인·보호 경로 | `027~037` | `AdminAuthController`·`JwtTokenProvider`·`JwtAuthenticationFilter`·`SecurityConfig` / `adminApi.js`·`adminSession.js`·`apiClient.js`·`useAdminAuth.js`·`LoginPage.jsx` |

### 일정 해석 메모

- 이 표는 구현 완료를 뜻하지 않는다. `TODO-NNN`이 소스에 남아 있는 항목만 일정에 넣었다.
- 번호는 재사용·재배치하지 않는다. 백엔드 선행 항목이 끝나기 전 프런트 API 호출을 추가하지 않는다.
- RTOS 작업은 Admin과 Kiosk로 기능을 분할하지 않는다. 하나의 이벤트 계약과 하나의 React 표시 흐름을 기준으로 서버·화면·콘솔을 함께 확인한다. 저장소/화면 통합 방식은 팀이 결정해야 하며, 이 일정은 저장소 병합을 지시하지 않는다.
- **8/21 금요일 테스트 시연**의 최소 확인은 `Spring Boot API 호출 → React 이벤트 표시 → 콘솔 출력`이다. 전날인 8/20에 동일 흐름을 한 번 재현하고, mock만 보이지 않도록 실제 API 응답 여부를 확인한다.
- 환불·영수증은 상태 전이와 책임 경계 결정이 선행 조건이다. `8/28`까지 결정되지 않으면 발표 전 구현 항목이 아니라 `결정 필요`로 남긴다.

## 오늘 작업 우선순위 (8/5 + 8/6 합본)

| 순위 | 작업 | 인라인 TODO | 비고 |
|---|---|---|---|
| **1** | 메뉴 **목록·상세 조회** FE 실연동 + 검증 | **015·016** | BE GET 있음. 목록 0건=`MENU_NOT_FOUND` 제거. **등록보다 조회 먼저** |
| **2** | 메뉴 **등록·수정** BE → FE | **017~025** | 기본 필드만. Create/Update Request 정리됨 |
| **3** | 메뉴 **삭제** BE → FE | **026~028·030·031** | 8/6. 스키마 제약 확인 |
| **4** | 품절 C→S→M | **032~039** | 8/6 |
| **5** | 결제수단 C→S→M | **040~047** | 8/6 |
| 병행 | 주문 통합 테스트 | **008·010·012** + 검증 | 8/5. 메뉴 조회 줄기 후·여유 시 |
| 후순위 | 매출 → 대시보드 | **048~058** | 오늘 필수 아님 |
| 보류 | TTS·Live스크롤·로그인·키오스크·문서 | **059**, 013a~d, 060~ | 8/6 키오스크·문서는 관리자 메뉴 줄기 이후 |

## 번호 재매핑 (2026-08-06)

| 구간 | 구 번호 | 신 번호 |
|---|---|---|
| 메뉴 CRUD | 032~048 | **015~031** |
| 품절 | 015~022 | **032~039** |
| 결제수단 | 024~031 | **040~047** |
| 매출 | 049~056 | **048~055** |
| 대시보드 | 057~059 | **056~058** |
| Live 가로스크롤 | 023 | **059** |
| 주문 잔여·인증·Future | 008·010·012, 060~076 | 유지 |
| 완료 주석 제거 | 007, 013(기본 TTS) | IDE TODO에서 제거 |

## 진행 요약

| 상태 | 번호 |
|---|---|
| 완료(주석 제거) | **001~007**, **009**, **011**, **013**(기본 TTS), **014** |
| 완료 | **015**, **016** |
| 부분/잔여 | **008**, **010**(코드테이블화 진행), **012**(hook 수정·화면확인) |
| 진행 중 | **017~025** (메뉴 등록·수정 설계/연결), **032~039**, **040~047** |
| 미착수 | **026~031**, **048~076** |

다음 착수: **① 메뉴 등록·수정(T-3~T-6)** → **② 메뉴 삭제(T-7)** → **③ 품절·결제수단 C→S→M** → (여유) 주문 검증 · 매출·대시보드

### 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-08-06 | 오늘 순서를 메뉴 **조회 먼저**로 재정렬. Request DTO MVP 정리. Empty/Error·Live 빈목록 수정. |
| 2026-08-06 | 메뉴 조회 실연동 반영: `useMenusQuery`가 `PageResult` 기준으로 목록/필터/페이지네이션 연동, `AdminMenuController.getMenus`는 빈 목록도 200으로 응답. |
| 2026-08-06 | 문서·DevCopilot 동기화(코드 기준). 주문 BE/FE 연동은 구현됨·**미검증**. 메뉴 POST/PATCH/DELETE는 미구현. |

---

### P1 · 주문 잔여 (통합 테스트와 함께)

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **008** | 🟡 부분 | `AdminOrderService.cancelOrder` | ① APPROVED 취소 정책 확정 ② 환불 흐름 분리 여부 결정 ③ Controller/ErrorCode 기준 정리 |
| **010** | ✅ 완료 | `AdminOrderMapper.xml` cancel | `status_id=43` 제거, `findOrderStatusId("CANCELED")` 사용 |
| **012** | 🟡 부분 | `useOrdersQuery.js` | ① Empty/Error 분리 반영 ② 필터 쿼리 정합 확인 ③ OrderManagement 화면 수동 검증 |

상세 검증 ID: `P1-1`~`P1-9` → 검증 투두 문서

### P2 · 메뉴 (015~031) — SCR-016 · 조회→등록·수정→삭제

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **015** | ✅ 완료 | `useMenusQuery.js` | mock 제거, `menusApi.listMenus` / `getMenu` + `PageResult` 페이지네이션 연동 |
| **016** | ✅ 완료 | `AdminMenuController.getMenus` | 목록 0건 → 200+빈 `PageResult` (`MENU_NOT_FOUND` 제거) |
| **017** | ⬜ 진행 중 | `AdminMenuMapper.java` | `insertMenu` 선언 → XML INSERT → generated key 반환 |
| **018** | ⬜ 진행 중 | `AdminMenuService.createMenu` | 이미지 저장 → request + imageUrl로 INSERT → 요약 응답 연결 |
| **019** | ⬜ 진행 중 | `AdminMenuController` | POST 바인딩 방식 결정(JSON/multipart) → service 호출 → 성공 응답 |
| **020** | ⬜ 진행 중 | `AdminMenuMapper.java` | `updateMenu` 선언 → XML UPDATE → 수정 건수 반환 |
| **021** | ⬜ 진행 중 | `AdminMenuService` | menuId 기준 update 호출 → 존재하지 않음/성공 기준 정리 |
| **022** | ⬜ 진행 중 | `AdminMenuController` | PATCH 바인딩 → service 호출 → `MENU_NOT_FOUND`/성공 응답 |
| **023** | ⬜ 진행 중 | `menusApi.js` | `createMenu(payload)` 추가 → 백엔드 POST 규격 연결 |
| **024** | ⬜ 진행 중 | `menusApi.js` | `updateMenu(menuId, payload)` 추가 → 백엔드 PATCH 규격 연결 |
| **025** | ⬜ 진행 중 | `MenuManagePage.jsx` | create/edit 분기 호출 → 성공 refetch/optimistic update → 실패 toast 처리 |
| **026** | ⬜ 오늘③ | `AdminMenuMapper.java` | 삭제 정책 확정 후 `deleteMenu`/`updateMenuActive` 선언·XML 구현 |
| **027** | ⬜ 오늘③ | `AdminMenuService` | 삭제 service 구현 → 정책(soft/hard) 반영 |
| **028** | ⬜ 오늘③ | `AdminMenuController` | DELETE endpoint → 성공/실패 응답 규격 정리 |
| **029** | ⬜ 후순위 | Mapper + Controller | ingredients |
| **030** | ⬜ 오늘③ | `menusApi.js` | `deleteMenu(menuId)` 추가 |
| **031** | ⬜ 오늘③ | `MenuManagePage.jsx` | 삭제 확인 → API 호출 → refetch/선택 메뉴 이동/view 복귀 |

> CreateMenuRequest / UpdateMenuRequest 기본 필드 DTO는 정리 완료(별도 TODO 번호 없음).

상세 검증: `T-1`~`T-7` ([검증 투두](admin-feature-verify-todos-2026-08-06.md))

### P3 · 품절 (032~039) — SCR-011

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **032** | ✅ 완료 | `SoldOutPatchRequest.java` | DTO 필드(`targetType`, `targetId`, `isSoldOut`) |
| **033** | ⬜ | `AdminSoldOutMapper` + XML | ① 대상별 SELECT ② 공통 row shape 정리 ③ XML 추가 |
| **034** | ⬜ | 동상 | ① targetType 분기 ② `is_sold_out` 토글 UPDATE ③ 변경 건수 반환 |
| **035** | ⬜ | `AdminSoldOutService.java` | ① 조회 메서드 ② patch 메서드 ③ 실패/롤백 기준 정리 |
| **036** | ⬜ | `AdminSoldOutController.java` | ① GET 응답 ② PATCH 바인딩 ③ ErrorCode 규격 정리 |
| **037** | ⬜ | `soldOutApi.js` | ① `listSoldOutCatalog()` 추가 ② 초기 load 연결 |
| **038** | ⬜ | `soldOutApi.js` | ① `patchSoldOut(body)` 추가 ② body 규격 정리 |
| **039** | ⬜ | `useSoldOutDraft.js` | ① mock load 교체 ② mock save 교체 ③ baseline 롤백 유지 |

상세 검증: `P3-1`~`P3-4`

### P4A · 결제수단 (040~047) — SCR-018

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **040** | ✅ 완료 | `PatchPaymentMethodRequest.java` | DTO 필드(`status`, `sortOrder`, `receiptMessage`) |
| **041** | ⬜ | `AdminPaymentMethodMapper` + XML | ① 목록 SELECT ② row shape 정리 ③ XML 추가 |
| **042** | ⬜ | 동상 | ① methodId 기준 UPDATE ② 변경 건수 반환 |
| **043** | ⬜ | `AdminPaymentMethodService.java` | ① 목록 메서드 ② patch 메서드 ③ 0건 처리 기준 정리 |
| **044** | ⬜ | `AdminPaymentMethodController.java` | ① GET 목록 ② PATCH 바인딩 ③ 응답/ErrorCode 규격 |
| **045** | ⬜ | `paymentMethodsApi.js` | ① `listPaymentMethods()` 추가 ② 초기 load 연결 |
| **046** | ⬜ | `paymentMethodsApi.js` | ① `patchPaymentMethod()` 추가 ② 저장 방식(순차/일괄) 확정 |
| **047** | ⬜ | `usePaymentMethodDraft.js` | ① mock load 교체 ② mock save 교체 ③ baseline 롤백 유지 |

상세 검증: `P4A-1`~`P4A-2`

### P4B · 매출 (048~055) — SCR-019/020/021

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **048** | ⬜ | `AdminStatsController` | sales/summary |
| **049** | ⬜ | 동상 | sales/monthly |
| **050** | ⬜ | 동상 | sales/daily |
| **051** | ⬜ | Stats Service/Mapper | 집계 |
| **052** | ⬜ | `salesApi.js` | getSummary |
| **053** | ⬜ | `salesApi.js` | getMonthly |
| **054** | ⬜ | `salesApi.js` | getDaily |
| **055** | ⬜ | `useSalesQuery.js` | mock → API |

상세 검증: `P4B-1`~`P4B-3`

### P4C · 대시보드 (056~058) — SCR-022

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **056** | ⬜ | `AdminStatsController` | dashboard |
| **057** | ⬜ | `adminApi.js` | getDashboard |
| **058** | ⬜ | `useDashboard.js` | mock → API |

상세 검증: `P4C-1`

### 보류 · Live UX · TTS 명세 · 인증 · Future

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **059** | ⬜ 보류 | `LiveOrderPreview.jsx` | 가로 스크롤 (구 023) |
| **013a~d** | ⬜ 보류 | TTS | 중복방지·Queue·Mute·localStorage |
| **060** | ⬜ | `AdminAuthController` | POST /login |
| **061** | ⬜ | `JwtTokenProvider.java` | JWT |
| **062** | ⬜ | `JwtAuthenticationFilter.java` | 필터 |
| **063** | ⬜ | `SecurityConfig.java` | authorize |
| **064** | ⬜ | `adminApi.js` | login |
| **065** | ⬜ | `adminSession.js` | token |
| **066** | ⬜ | `apiClient.js` | Bearer + 401 |
| **067** | ⬜ | `LoginPage.jsx` | 실로그인 |
| **068** | ⬜ | `useAdminAuth.js` | 401 가드 |
| **069** | ⬜ | `AdminApp.jsx` | 정본 경로 |
| **070** | ⬜ | `apiClient.js` | 403 매핑 |
| **071** | ⬜ Future | `AdminOrderController` | refund |
| **072** | ⬜ Future | `AdminOrderMapper.xml` | payments 환불 |
| **073** | ⬜ Future | `ordersApi.js` | refundOrder |
| **074** | ⬜ Future | `ordersApi.js` | printReceipt |
| **075** | ⬜ Future | `OrderManagementPreview.jsx` | 환불 UI |
| **076** | ⬜ Future | `OrderManagementPreview.jsx` | 영수증 UI |

## 사용법

1. IDE TODO 패널을 번호순으로 보면 **교사 우선순위**와 같다.
2. 각 기능은 **화면–API–DB**를 함께 확인한 뒤 다음 번호로 넘어간다.
3. 완료한 항목은 인라인 주석을 지우고, 이 표 상태를 ✅로 갱신한다.
4. 이 표와 코드 주석이 어긋나면 **코드 인라인을 정본**으로 맞춘다.
