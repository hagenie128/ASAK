> Status: **CURRENT**
> 기준일: **2026-09-02** · 코드: `ASAK-back` **main** `b0718b3`, `ASAK-Admin` **main** `6071c68`, `ASAK-Kiosk` **main** `e1994e4`
> 계약 필드: [정본](../governance/contract-decisions-2026-07-16.md) · Bruno: `ASAK-back/api/`
> Hub API 카드: workspace 2 (환불 id **449**, 환불 사유 id **457** — **정본 API 번호 미배정**)
> 2026-08-25 결정: 관리자 로그인(매장 번호 하드코드)·환불 정책 — [`admin-todo-2026-08-24.md`](../planning/admin-todo-2026-08-24.md)
> 2026-08-28: 환불·환불 사유 API **main 머지**. FE body `refundReasonCode`/`refundReasonDetail` 연결.
> 2026-09-02 QA: [Admin](qa-execution-report-2026-09-02.md) **22/24 PASS** · [Kiosk](qa-kiosk-execution-report-2026-09-02.md) **17/18 PASS** (API E2E, UI 클릭 제외).

# ASAK REST API 명세서

모든 서비스 path는 `/api`로 시작한다. JSON은 `camelCase`. DB `snake_case`는 API에 노출하지 않는다.

공통 envelope:

```json
{ "success": true, "status": 200, "code": "...", "message": "...", "data": {} }
```

- 인증: JWT 없음. `POST /api/admin/login`은 `{storeNumber}` 고정값 `"0001"` 비교만 (**구현됨** · TC-009 API PASS 2026-09-02).
- 헤더: `Content-Type: application/json` (POST/PATCH), `Accept: application/json`
- 에러: HTTP status + `success=false`. 프론트는 `code`로 분기.
- Git 커밋 ≠ HTTP E2E 통과. 아래 **구현**은 Controller 메서드 존재, **스텁**은 `@RequestMapping`만 있고 메서드 없음.

Hub 카드 ID와 예전 Notion `API-013` 번호가 다를 수 있다. **Hub·Bruno 경로를 우선**한다. 구 path `/api/menus`, `/api/orders`는 폐기.

## 구현된 endpoint (Controller 메서드 있음)

| Hub | Method | Path | 코드 | 상태 |
|---|---|---|---|---|
| API-025 | GET | `/api/health` | `HealthController` | 구현 · Bruno health 테스트 있음 |
| API-001 | GET | `/api/kiosk/categories` | `UserMenuController` | 구현 · **실DB QA PASS** (K-001, 2026-09-02) |
| API-002 | GET | `/api/kiosk/menuList` | `UserMenuController` | 구현 · **실DB QA PASS** (K-002) |
| API-003 | GET | `/api/kiosk/menuDetail/{menuId}` | `UserMenuController` | 구현 · **실DB QA PASS** (K-003, 404 수동 확인) |
| API-004 | POST | `/api/kiosk/cart/validate` | `UserOrderController` | 구현 · **실DB QA PASS** (K-005~007) |
| API-005 | POST | `/api/kiosk/orders` | `UserOrderController` | 구현 · **실DB QA PASS** (TC-001) |
| API-006 | POST | `/api/kiosk/payments` | `UserPayController` | 구현 · **실DB QA PASS** (TC-002). CARD 직접 승인, KAKAO/NAVER/TOSS는 토스 SDK `tossPayment` body 포함 |
| API-014 | GET | `/api/kiosk/payment-methods` | `UserPayController` | 구현 · **실DB QA PASS** (K-010). `methodId` = **`common_code.id`** · Admin OFF→Kiosk 노출 **FAIL** (아래 참고) |
| API-015 | GET | `/api/admin/paymentMethods` | `AdminPaymentMethodController` | 구현 · **실DB QA PASS** (TC-012a). `methodId` = **`pay_method_cfg.id`** · 응답 `active`, `sortNo` |
| — | POST | `/api/kiosk/orders/{orderId}/receipt-print` | `UserReceiptController` | 구현 · **실DB QA PASS** (K-011). RTOS 연동 임시 코드 |
| — | POST | `/api/kiosk/orders/{orderId}/waiting-number-print` | `UserReceiptController` | 구현 · 미검증 |
| API-007 | GET | `/api/admin/orders` | `AdminOrderController` | 구현 · query: page,size,orderStatus,paymentStatus,orderType,dateFrom,dateTo,keyword |
| API-022 | GET | `/api/admin/orders/{orderId}` | 동상 | 구현 · **실DB QA PASS** (SC-022) |
| API-021 | GET | `/api/admin/orders/live` | 동상 | 구현 · **실DB QA PASS** (TC-014a) |
| API-008 | PATCH | `/api/admin/orders/{orderId}/{status}` | 동상 | 구현 · **실DB QA PASS** (TC-014b/c) |
| API-024 | PATCH | `/api/admin/orders/{orderId}/cancel` | 동상 | 구현 · APPROVED **409** **PASS** · **READY `ORDER_CANCEL_NOT_ALLOWED` 409** **PASS** (HTTP 2026-09-02, orderId=51984) |
| — | PATCH | `/api/admin/orders/{orderId}/refund` | `AdminOrderController` | 구현 · 사유 목록 **PASS** (TC-017). 실주문 환불은 QA 스킵 |
| — | GET | `/api/admin/refund-reasons` | `AdminRefundReasonController` | 구현 · **실DB QA PASS** (TC-017). Hub id **457** |
| — | POST | `/api/admin/login` | `AdminAuthController` | 구현 · **실DB QA PASS** (TC-009) |
| API-011 | GET | `/api/admin/menus` | `AdminMenuController` | 구현 · query categoryId,keyword,isSoldOut,tagId,page,size,sort |
| API-023 | GET | `/api/admin/menus/{menuId}` | 동상 | 구현 |
| API-026 | GET | `/api/admin/menus/categories` | 동상 | 구현 · `/{menuId}`보다 위에 선언 |
| API-027 | GET | `/api/admin/menus/ingredients` | 동상 | 구현 |
| API-012 | POST | `/api/admin/menus` | 동상 | 구현 · 브라우저 E2E 미실행 |
| API-013 | PATCH | `/api/admin/menus/{menuId}` | 동상 | 구현 · 브라우저 E2E 미실행 |
| API-028 | DELETE | `/api/admin/menus/{menuId}` | 동상 | 구현 · **soft delete** (`deleted_at`) |
| API-029 | GET | `/api/admin/opts/groups` | `AdminOptionController` | 구현 |
| API-030 | GET | `/api/admin/opts/{optionGroupId}` | 동상 | 구현 |
| API-009 | PATCH | `/api/admin/soldOut` | `AdminSoldOutController` | 구현 · **실DB QA PASS** (TC-006). body `changes[{targetType,targetId,isSoldOut}]` |
| API-010 | GET | `/api/admin/soldOut` | 동상 | 구현 · **실DB QA PASS** (TC-006a). INGREDIENT ing125 Kiosk 반영 **FAIL** |
| API-016 | PATCH | `/api/admin/paymentMethods/{methodId}` | `AdminPaymentMethodController` | 구현 · **실DB QA PASS** (TC-012b/c). body `active`, `sortNo` · PATCH id = `pay_method_cfg.id` |
| API-020 | GET | `/api/admin/dashboard` | `AdminSalesController` | 구현 · **실DB QA PASS** (WBS-040) |
| API-018 | GET | `/api/admin/sales/summary` | 동상 | 구현 · **실DB QA PASS** (TC-013 today/week/month, 8/28 합계) |
| API-019 | GET | `/api/admin/sales/monthly` | 동상 | 구현 · **실DB QA PASS** (TC-013-monthly) |
| API-017 | GET | `/api/admin/sales/daily` | 동상 | 구현 · 응답 `rows[]` (QA 스크립트 `dailySales` 기대와 **필드명 불일치** — TC-013-daily FAIL, API 자체는 200) |
| — | GET | `/api/admin/sales/daily/time-slots` | 동상 | 구현 · query `date`, `intervalMinutes=30\|60` · 미검증 |
| — | POST | `/api/admin/orders/{orderId}/receipt-print-text` | `AdminDeviceEventController` | 구현 · 미검증 (Admin 재출력) |
| — | GET | `/api/admin/device-events` | 동상 | 구현 · 미검증 |
| — | GET | `/api/rtos/device-events/pending` | 동상 | 구현 · RTOS polling 임시 코드 · 미검증 |
| — | PATCH | `/api/rtos/device-events/{eventId}/finish` | 동상 | 구현 · RTOS 결과 보고 임시 코드 · 미검증 |

`AdminOrderController`의 class mapping은 `"api/admin/orders"`(선행 `/` 없음)다. Spring은 보통 동일하게 `/api/admin/orders`로 붙는다.

### 환불 사유 목록 API — 현재 코드 근거 (2026-08-28)

> 상태: **구현 · 미검증**. `common_code` 그룹 `REFUND_REASON` seed 필요 — `docs/migrations/20260828_refund_reason_codes.sql`.

```http
GET /api/admin/refund-reasons
```

| 구분 | 현재 코드 사실 |
|---|---|
| 응답 | `ApiResponse` + `RefundReasonResponse[]` — `code`, `name`, `sortNo`, `requiresDetail`(코드 `OTHER`일 때 true) |
| 정렬 | `sort_no ASC`, `id ASC` |
| 데이터 | `code_group.group_code = 'REFUND_REASON'` 하위 활성 `common_code` |

### 환불 API — 현재 코드 근거 (2026-08-28)

> 상태: **초안 구현 · 미검증**. DB migration(`payment_refund` 등) 적용 완료. 완료 구현·통합 통과로 쓰지 않는다.

```http
PATCH /api/admin/orders/{orderId}/refund
Content-Type: application/json

{ "refundReasonCode": "CUSTOMER_REQUEST", "refundReasonDetail": "기타 상세(OTHER일 때만)" }
```

| 구분 | 현재 코드 사실 |
|---|---|
| path | `orderId`: 내부 주문 PK |
| request body | `OrderRefundRequest.refundReasonCode` (`@NotBlank`, max 50), `refundReasonDetail` (선택, max 200). `OTHER` 코드일 때 detail 필수. 서버가 코드→라벨(또는 detail)로 `payment_refund.reason` 저장. 결제수단·금액·`paymentKey`는 클라이언트가 보내지 않는다. |
| 서버 검증 | `AdminPaymentMapper.findRefundTarget`로 최신 `APPROVED` payment 조회. 미승인·이미 취소 주문·금액≤0·CARD 외 수단은 ErrorCode로 거부. |
| 외부 호출 | DB 트랜잭션 밖 `PaymentService.cardRefund`만. **가상** `VIRTUAL-CANCEL-{uuid}` 반환. 실제 토스/카드 PG cancel 미연결. |
| DB 반영 | `@Transactional` `applyRefund`: payment `APPROVED→REFUNDED`(1건), `payment_refund` INSERT(1건), 제공 전 주문만 `CANCELED`+`canceled_at`. **COMPLETED는 주문 상태 유지**(회의록 2026-W31 확정과 일치). |
| 성공 응답 | `ApiResponse` + `OrderDetailResponse` 재조회. `paymentMethod`는 객체(`methodName` 등, `vw_order_summary` association). 별도 `refundedAmount`/`refundReason` 필드는 응답 DTO에 없음. |

| 상황 | HTTP | 코드 ErrorCode |
|---|---:|---|
| 주문 없음 | 404 | `ORDER_NOT_FOUND` |
| APPROVED payment 없음 / 미승인 | 409 | `ONLY_APPROVED_PAYMENT_CAN_BE_REFUNDED` |
| 이미 CANCELED 주문 | 409 | `CANCELED_ORDER_CANNOT_BE_REFUNDED` |
| 금액 무효 | 400 | `AMOUNT_INVALID_NOT_ALLOWED` |
| CARD 외 수단 | 400 | `PAYMENT_METHOD_NOT_SUPPORTED_FOR_REFUND` |
| 잘못된/비활성 환불 사유 코드 | 400 | `INVALID_REFUND_REASON` |
| OTHER 코드인데 detail 없음 | 400 | `REFUND_REASON_DETAIL_REQUIRED` |
| DB 1건 갱신/INSERT 실패 | 500 | `ORDER_REFUND_FAILED` |

#### 남은 불일치 · 결정 필요

| 상태 | 내용 |
|---|---|
| `구현 불일치` | `findRefundTarget` SELECT에 `providerPaymentKey` 없음 → `cardRefund`가 `ORDER_REFUND_FAILED` 가능. |
| `구현 불일치` | `insertPaymentRefund` XML `#{cancelTransactionKey}` vs Service map `providerCancelTransactionKey`. |
| `미검증` | HTTP/Bruno/실서버 E2E·실PG cancel·seed SQL 적용·부분환불 미실행. |
| `결정 필요` | Hub/Notion 정본 API 번호. `provider`/`provider_payment_key` 재도입. 토스페이 포함 시점. |

## 미구현 (명세·요구만, Controller 없음)

| 요구 | Method | Path | 비고 |
|---|---|---|---|
| RTOS-DEVICE-004~006 | POST | `/api/device/scan` | EXCLUDED |
| KSD-MEMBER-001 | POST | `/api/membership/stamps` | FUTURE |
| — | GET | `/api/ui/accessibility-options` | 코드 없음 |

> 영수증 출력: 구 명세 path `/api/orders/{orderId}/receipt-print`는 폐기. 현재 구현은 `/api/kiosk/orders/{orderId}/receipt-print`(Kiosk) · `/api/admin/orders/{orderId}/receipt-print-text`(Admin 재출력).

## 영수증·장치 이벤트 — DB 테이블 없음 (2026-09-02 정본)

**`receipt` 테이블은 없다.** Hub ERD·`아삭_mysql.sql` 모두 영수증 전용 테이블을 정의하지 않는다. 영수증에 표시할 금액·메뉴·주문번호는 **`orders` · `order_item` · `payment`** 등 기존 주문·결제 데이터에서 조회한다.

**`device_event` 테이블도 없다.** 출력 요청·처리 상태는 DB에 쌓지 않고, `DeviceEventService`가 **Spring 메모리 큐**(`ConcurrentHashMap`)로 `PENDING → PROCESSING → COMPLETED/FAILED`만 검증한다. `DeviceEventMapper.xml`은 DDL 확정 전 **placeholder**(SQL 없음). 서버 재시작 시 큐가 비워진다.

| 구분 | 저장 위치 | 비고 |
|---|---|---|
| 영수증 본문(메뉴·금액·주문번호) | 주문·결제 테이블 | 별도 `receipt` row 없음 |
| 출력 요청·RTOS polling 이벤트 | JVM 메모리 | `UserReceiptController` · `AdminDeviceEventController` |
| 대기번호 출력 payload | `orders.waiting_order_no` | `UserReceiptService`가 조회 후 이벤트 생성 |

| Endpoint | 역할 |
|---|---|
| `POST /api/kiosk/orders/{orderId}/receipt-print` | Kiosk 영수증 출력 요청 → 메모리 이벤트 (**K-011 PASS**) |
| `POST /api/kiosk/orders/{orderId}/waiting-number-print` | 대기번호 출력 요청 |
| `POST /api/admin/orders/{orderId}/receipt-print-text` | Admin 재출력(텍스트) · 미검증 |
| `GET /api/admin/device-events` | 메모리 이벤트 목록 · 미검증 |
| `GET /api/rtos/device-events/pending` | RTOS polling · 미검증 |
| `PATCH /api/rtos/device-events/{eventId}/finish` | RTOS 완료 보고 · 미검증 |

종강 MVP: 실물 프린터·영구 출력 이력은 **범위 밖**. 후속에 출력 이력이 필요하면 `device_event` 또는 `receipt_print_log` 테이블을 **신규 설계**한다.

## 키오스크 계약 요약

| ID | Request | 성공 data 요지 |
|---|---|---|
| API-001 | — | `[{categoryId, categoryName, sortOrder, isActive}]` |
| API-002 | — | `{categories, menus[{menuId, categoryId, name, price, imageUrl, isSoldOut, ...}]}` |
| API-003 | path menuId | 상세 + `ingredients` + `optionGroups` |
| API-004 | `{items:[{menuId, quantity, optionItems[{optionItemId,quantity}], excludedIngredientIds}]}` | `totalAmount` 등 |
| API-005 | `{orderType: EAT_IN\|TAKE_OUT, items:[...]}` | `orderId, orderNo, totalAmount, status(=READY)` |
| API-006 | `{orderId, orderStatus(=RECEIVED), paymentMethodCode, idempotencyKey, tossPayment?}` | `paymentId, orderId, orderNo, paymentStatus, approvedAmount, approvedAt, waitingOrderNo` · CARD는 `tossPayment` 없음, 간편결제는 토스 SDK 결과 포함 |
| API-014 | — | `{methods:[{methodId, methodCode, methodName, imageAssetId, imageUrl, description, active, sortOrder}]}` |

### 키오스크 FE 연결 (2026-09-02 · main · API QA PASS, UI 클릭 미검증)

| API | FE 파일 | 흐름 |
|---|---|---|
| API-001 | `MenuListPage` → `getCategories` | 카테고리 탭 |
| API-002 | `MenuListPage` → `getMenus` | 메뉴 카드 |
| API-003 | `MenuDetailPage` → `getMenu` | 옵션·담기 |
| API-004 | `CartPage` → `validateCart` | 결제 전 서버 검증 |
| API-005 | `PaymentProcessingPage` → `createOrderForPayment` | 주문 생성(READY 재사용) |
| API-006 | `PaymentProcessingPage` → `approvePayment` | CARD 직접 / 간편결제 `tossPayment` |
| API-014 | `PaymentPage` → `getPaymenMethods` | 활성 결제수단만 선택 |

`VITE_API_BASE_URL` + `API_BASE_PATH=/api/kiosk` → 실제 호출 `/api/kiosk/...`. 결제 실패 시 cart 유지(`orderSessionStore`). `/paymentProcessing`에서 타임아웃 비활성.

## 관리자 메뉴·옵션

- 삭제: 물리 DELETE가 아니라 `deleted_at`. 주문 이력 FK 유지.
- 수정: 자식 컬렉션이 `null`이 아니면 교체. `CORE` 재료는 서버에서 제거 불가.
- 옵션 그룹 요약 필드: `optionGroupId, name, groupType, selectType, minSelect, maxSelect, isRequired, recommendedLabel`

## 상태값

| 구분 | 코드 |
|------|------|
| 주문 | `READY`, `RECEIVED`, `PREPARING`, `COMPLETED`, `CANCELED` |
| 결제 | `READY`, `APPROVED`, `FAILED`, `REFUNDED` |
| 주문유형 | `EAT_IN`, `TAKE_OUT` |
| 결제수단 | `CARD`, `KAKAO_PAY`, `NAVER_PAY` · enums에 `TOSS_PAY` 추가됨(**정본 3종과 결정 필요** — 미해결). 2026-08-25: 환불 대상 범위만 카드/신용카드 확정, 토스페이는 연동+통합 테스트 성공 시 포함으로 별도 결정(전체 결제수단 정본 3종 결정과는 별개) |

## Bruno

`ASAK-back/api/kiosk/` · `api/admin/` · `api/health/`. 성공 assert는 health만.

## 2026-09-02 QA 잔여 불일치

| 상태 | 항목 | 근거 |
|---|---|---|
| `구현 불일치` | Admin 결제수단 OFF → Kiosk에 CARD 계속 노출 | `methodId` 값 자체가 달라서가 아님(Admin=`pay_method_cfg.id`, Kiosk=`common_code.id`). Kiosk 목록 API·`PaymentPage`가 `active=false`를 숨기지 않음. 승인 API는 `validateMethodForPayment`로 비활성 차단 |
| `구현 불일치` | INGREDIENT ing125 품절 → Kiosk `menuList` 변화 없음 | `affectedMenuCount=0` · MENU/OPTION 품절은 PASS |
| `계약 불일치` | API-014 vs API-015 `methodId` 의미 | 동일 키 이름이 서로 다른 PK를 가리킴 — Admin PATCH id로 Kiosk 행을 지정할 수 없음. 연동은 `methodCode` 또는 `pay_method_cfg.id` 통일 필요 |
| `계약 불일치` | API-017 일별 매출 | 응답 `data.rows[]` vs QA 스크립트 `data.dailySales` 기대 |
| `미검증` | Admin·Kiosk UI 브라우저 클릭 E2E | API QA만 완료 |
