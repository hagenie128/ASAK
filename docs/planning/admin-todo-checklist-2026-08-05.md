# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-076)

> 인라인 주석 태그: `TODO-NNN`
> **번호 순 = 교사 우선순위** (주문 → 메뉴 → 품절 → 결제수단 → 매출 → 대시보드)
> 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.
> 검색: `TODO-00` / `TODO-0` / `TODO-`
> 진행 갱신: 2026-08-06 (인라인 번호 교사순 재매핑)
> 작업 원칙: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행한다.
> 상세 검증: [`admin-feature-verify-todos-2026-08-06.md`](./admin-feature-verify-todos-2026-08-06.md)

## 작업 우선순위 (교사 지시 2026-08-05)

| 순위 | 작업 | 인라인 TODO | 비고 |
|---|---|---|---|
| **P1** | 주문 목록·상세·Live·상태 변경·취소 **API 통합 테스트** | **008·010·012** (+ 완료분 001~007·009·011·014 검증) | TTS 기본 호출은 구현됨. **013a~d·059**(보드 스크롤) 보류 |
| **P2** | 메뉴 목록·상세·등록·수정 **API 연동** | **015~025** (삭제 **026~031** 후순위) | 구 032~048 |
| **P3** | 품절 관리 **API 연동** | **032~039** | 구 015~022 |
| **P4** | 결제수단 → 매출 → 대시보드 | **040~047** → **048~055** → **056~058** | 구 024~031 → 049~059 |
| 보류 | Live 스크롤·TTS 명세·로그인·Future | **059**, **013a~d**, **060~076** | P1~P4 이후 |

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
| 부분/잔여 | **008**, **010**, **012** |
| 미착수 | **015~076** (059·060~는 보류/후순위 포함) |

다음 착수: **P1 주문 API 통합 테스트** → **P2 메뉴(015~)** → **P3 품절(032~)** → **P4 결제(040~)→매출(048~)→대시보드(056~)**

---

### P1 · 주문 잔여 (통합 테스트와 함께)

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **008** | 🟡 부분 | `AdminOrderService.cancelOrder` | APPROVED 시 환불 연동 미완(현재 0 반환) |
| **010** | ⬜ 미착수 | `AdminOrderMapper.xml` cancel | `status_id=43` → 코드테이블/상수 |
| **012** | 🟡 부분 | `useOrdersQuery.js` | Empty vs Error UI·필터 정합 확인 |

상세 검증 ID: `P1-1`~`P1-9` → 검증 투두 문서

### P2 · 메뉴 (015~031) — SCR-016

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **015** | ⬜ | `CreateMenuRequest.java` | DTO 필드 |
| **016** | ⬜ | `AdminMenuMapper.java` | insertMenu |
| **017** | ⬜ | `AdminMenuService.createMenu` | INSERT 트랜잭션 |
| **018** | ⬜ | `AdminMenuController` | POST |
| **019** | ⬜ | `AdminMenuMapper.java` | updateMenu |
| **020** | ⬜ | `AdminMenuService` | updateMenu |
| **021** | ⬜ | `AdminMenuController` | PATCH |
| **022** | ⬜ | `menusApi.js` | createMenu |
| **023** | ⬜ | `menusApi.js` | updateMenu |
| **024** | ⬜ | `useMenusQuery.js` | mock → API |
| **025** | ⬜ | `MenuManagePage.jsx` | save → API |
| **026** | ⬜ 후순위 | `AdminMenuMapper.java` | deleteMenu |
| **027** | ⬜ 후순위 | `AdminMenuService` | deleteMenu |
| **028** | ⬜ 후순위 | `AdminMenuController` | DELETE |
| **029** | ⬜ 후순위 | Mapper + Controller | ingredients |
| **030** | ⬜ 후순위 | `menusApi.js` | deleteMenu |
| **031** | ⬜ 후순위 | `MenuManagePage.jsx` | delete → API |

상세 검증: `P2-1`~`P2-6`

### P3 · 품절 (032~039) — SCR-011

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **032** | ⬜ | `SoldOutPatchRequest.java` | DTO 필드 |
| **033** | ⬜ | `AdminSoldOutMapper` + XML | 카탈로그 SELECT |
| **034** | ⬜ | 동상 | `is_sold_out` UPDATE |
| **035** | ⬜ | `AdminSoldOutService.java` | 조회·변경·롤백 |
| **036** | ⬜ | `AdminSoldOutController.java` | GET/PATCH |
| **037** | ⬜ | `soldOutApi.js` | `listSoldOutCatalog` |
| **038** | ⬜ | `soldOutApi.js` | `patchSoldOut` |
| **039** | ⬜ | `useSoldOutDraft.js` | mock → API |

상세 검증: `P3-1`~`P3-4`

### P4A · 결제수단 (040~047) — SCR-018

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **040** | ⬜ | `PatchPaymentMethodRequest.java` | DTO 필드 |
| **041** | ⬜ | `AdminPaymentMethodMapper` + XML | SELECT |
| **042** | ⬜ | 동상 | UPDATE |
| **043** | ⬜ | `AdminPaymentMethodService.java` | 서비스 |
| **044** | ⬜ | `AdminPaymentMethodController.java` | GET/PATCH |
| **045** | ⬜ | `paymentMethodsApi.js` | list |
| **046** | ⬜ | `paymentMethodsApi.js` | patch |
| **047** | ⬜ | `usePaymentMethodDraft.js` | mock → API |

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
| **069** | ⬜ | `AdminApp.jsx` | Canonical 경로 |
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
