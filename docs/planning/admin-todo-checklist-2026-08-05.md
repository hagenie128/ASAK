# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-076)

> 인라인 주석 태그: `TODO-NNN`  
> 순서대로 구현하면 된다. 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.  
> 검색: `TODO-00` / `TODO-0` / `TODO-`

| # | 위치 | 할 일 |
|---|---|---|
| **001** | `ASAK-back/.../AdminOrderController.java` `changeOrderStatus` | `response == null` → `ORDER_NOT_FOUND` (NPE 방지) |
| **002** | 동상 `changeOrderStatus` | 상태변경 거절 시 `ORDER_CANCEL_NOT_ALLOWED` 대신 전이 불가 ErrorCode 분리 |
| **003** | `AdminOrderService.changeOrderStatus` | `RECEIVED→PREPARING→COMPLETED` 허용 전이만 통과 |
| **004** | 동상 | `statusId` 12/13 하드코딩 → enum/코드테이블 조회 |
| **005** | `AdminOrderMapper.xml` `changeOrderStatus` (+ Service map) | optimistic concurrency (`expectedStatusId`) |
| **006** | `AdminOrderController.changeOrderStatus` | update 0건 → 전이 불가 vs 409 충돌 구분 |
| **007** | `AdminOrderController.cancelOrder` | `response == null` → `ORDER_NOT_FOUND` |
| **008** | `AdminOrderService.cancelOrder` | 취소 가능 상태 + APPROVED 환불 정책 연동 |
| **009** | `AdminOrderMapper` + XML | `cancleOrder` → `cancelOrder` 오타 수정 |
| **010** | `AdminOrderMapper.xml` cancel | `status_id=43` 매직넘버 → 코드테이블/상수 |
| **011** | `LiveOrderPreview.jsx` `runOrderAction` catch | 409·envelope code별 메시지, 목록 재조회 |
| **012** | `useOrdersQuery.js` | Empty(0건) vs Error UI·필터 쿼리 정합 |
| **013** | `LiveOrderPreview.jsx` 성공 직후 | TTS 호출 (실패해도 주문 상태 유지) |
| **014** | `LiveOrderPreview.jsx` fixture/`console.log` | QA 후 fixture·로그 제거 또는 개발 전용 |
| **015** | `SoldOutPatchRequest.java` | DTO 필드: `targetType`, `targetId`, `isSoldOut` |
| **016** | `AdminSoldOutMapper` + XML | 품절 카탈로그 SELECT |
| **017** | 동상 | `is_sold_out` UPDATE |
| **018** | `AdminSoldOutService.java` | 조회·변경·롤백 서비스 |
| **019** | `AdminSoldOutController.java` | `GET` / `PATCH /api/admin/soldOut` |
| **020** | `soldOutApi.js` | `listSoldOutCatalog` |
| **021** | `soldOutApi.js` | `patchSoldOut` |
| **022** | `useSoldOutDraft.js` | mock → `soldOutApi` 교체 |
| **023** | `LiveOrderPreview.jsx` 보드 | `livePage` 제거 → `scrollBy` 가로 스크롤 |
| **024** | `PatchPaymentMethodRequest.java` | DTO 필드 채우기 |
| **025** | `AdminPaymentMethodMapper` + XML | `selectPaymentMethods` |
| **026** | 동상 | `updatePaymentMethod` |
| **027** | `AdminPaymentMethodService.java` | 목록·PATCH 서비스 |
| **028** | `AdminPaymentMethodController.java` | `GET /`, `PATCH /{id}` |
| **029** | `paymentMethodsApi.js` | `listPaymentMethods` |
| **030** | `paymentMethodsApi.js` | `patchPaymentMethod` |
| **031** | `usePaymentMethodDraft.js` | mock → `paymentMethodsApi` 교체 |
| **032** | `CreateMenuRequest.java` (+ Service) | 등록 DTO 필드 채우기 |
| **033** | `AdminMenuMapper.java` | `insertMenu` |
| **034** | `AdminMenuService.createMenu` | image + INSERT 트랜잭션 |
| **035** | `AdminMenuController` | `@PostMapping` 등록 |
| **036** | `AdminMenuMapper.java` | `updateMenu` |
| **037** | `AdminMenuService` | `updateMenu(...)` |
| **038** | `AdminMenuController` | `@PatchMapping("/{menuId}")` |
| **039** | `AdminMenuMapper.java` | `deleteMenu` / soft delete |
| **040** | `AdminMenuService` | `deleteMenu(...)` |
| **041** | `AdminMenuController` | `@DeleteMapping("/{menuId}")` |
| **042** | `AdminMenuMapper` + Controller | 재료 목록 `GET /ingredients` |
| **043** | `menusApi.js` | `createMenu` |
| **044** | `menusApi.js` | `updateMenu` |
| **045** | `menusApi.js` | `deleteMenu` |
| **046** | `useMenusQuery.js` | mock → `menusApi.listMenus`/`getMenu` |
| **047** | `MenuManagePage.jsx` `handleSaveEdit` | create/update API 호출 후 refetch |
| **048** | `MenuManagePage.jsx` `handleDeleteConfirm` | `deleteMenu` 후 목록 갱신 |
| **049** | `AdminStatsController` | `GET /sales/summary` |
| **050** | 동상 | `GET /sales/monthly` |
| **051** | 동상 | `GET /sales/daily` |
| **052** | `AdminStatsService` + `AdminStatsMapper`(+XML) | 집계 쿼리/서비스 |
| **053** | `salesApi.js` | `getSummary` |
| **054** | `salesApi.js` | `getMonthly` |
| **055** | `salesApi.js` | `getDaily` |
| **056** | `useSalesQuery.js` | mock → `salesApi` 교체 |
| **057** | `AdminStatsController` | `GET /dashboard` |
| **058** | `adminApi.js` | `getDashboard` |
| **059** | `useDashboard.js` | mock → `adminApi.getDashboard` |
| **060** | `AdminAuthController` (+ SecurityConfig 연동) | `POST /login` |
| **061** | `JwtTokenProvider.java` | create/validate/getClaims |
| **062** | `JwtAuthenticationFilter.java` | Bearer 검증, `/api/admin/**` 보호 |
| **063** | `SecurityConfig.java` | filter 등록 + authorize 규칙 |
| **064** | `adminApi.js` | `login` |
| **065** | `adminSession.js` (+ store 연동) | token 저장·만료 판정 |
| **066** | `apiClient.js` | Bearer interceptor + 401 리다이렉트 |
| **067** | `LoginPage.jsx` `handleSubmit` | `adminApi.login` 실연동 |
| **068** | `useAdminAuth.js` | JWT 세션 + 보호 라우트 401 |
| **069** | `AdminApp.jsx` `staticPages` | Canonical vs kebab 경로 정렬 |
| **070** | `apiClient.js` | 403 등 공통 ErrorCode 매핑 |
| **071** | `AdminOrderController` | Future: `PATCH /{id}/refund` |
| **072** | `AdminOrderMapper.xml` | Future: payments 환불 UPDATE 분리 |
| **073** | `ordersApi.js` | Future: `refundOrder` |
| **074** | `ordersApi.js` | Future: `printReceipt` |
| **075** | `OrderManagementPreview.jsx` | Future: 환불 ConfirmDialog 연결 |
| **076** | `OrderManagementPreview.jsx` | Future: 영수증 ConfirmDialog 연결 |

## 구간 요약

| 구간 | 주제 |
|---|---|
| 001–010 | 주문 상태·취소 BE |
| 011–014, 023 | Live FE (에러·TTS·정리·스크롤) |
| 015–022 | 품절 BE→FE |
| 024–031 | 결제수단 BE→FE |
| 032–048 | 메뉴 CRUD BE→FE |
| 049–059 | 매출·대시보드 BE→FE |
| 060–068 | 로그인·JWT BE→FE |
| 069–070 | 라우트·공통 에러 |
| 071–076 | Future 환불·영수증 |

## 사용법

1. `TODO-001`부터 구현한다.
2. 완료한 항목은 인라인 주석을 지우거나 `DONE-NNN`으로 바꾼다.
3. 이 표와 코드 주석이 어긋나면 **코드 인라인을 정본**으로 맞춘다.
