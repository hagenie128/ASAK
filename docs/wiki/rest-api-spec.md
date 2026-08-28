> Status: **CURRENT**
> 기준일: **2026-08-28** · 코드: `ASAK-back` **main** `494baef`, `ASAK-Admin` **main** `4f0c9cd`
> 계약 필드: [정본](../governance/contract-decisions-2026-07-16.md) · Bruno: `ASAK-back/api/`
> Hub API 카드: workspace 2 (환불 id **449**, 환불 사유 id **457** — **정본 API 번호 미배정**)
> 2026-08-25 결정: 관리자 로그인(매장 번호 하드코드)·환불 정책 — [`admin-todo-2026-08-24.md`](../planning/admin-todo-2026-08-24.md)
> 2026-08-28: 환불·환불 사유 API **main 머지**. FE body `refundReasonCode`/`refundReasonDetail` 연결. HTTP/실PG **미검증**.

# ASAK REST API 명세서

모든 서비스 path는 `/api`로 시작한다. JSON은 `camelCase`. DB `snake_case`는 API에 노출하지 않는다.

공통 envelope:

```json
{ "success": true, "status": 200, "code": "...", "message": "...", "data": {} }
```

- 인증: 현재 Controller에 JWT 검사 없음. `POST /api/admin/login`은 **스텁**.
- 헤더: `Content-Type: application/json` (POST/PATCH), `Accept: application/json`
- 에러: HTTP status + `success=false`. 프론트는 `code`로 분기.
- Git 커밋 ≠ HTTP E2E 통과. 아래 **구현**은 Controller 메서드 존재, **스텁**은 `@RequestMapping`만 있고 메서드 없음.

Hub 카드 ID와 예전 Notion `API-013` 번호가 다를 수 있다. **Hub·Bruno 경로를 우선**한다. 구 path `/api/menus`, `/api/orders`는 폐기.

## 구현된 endpoint (Controller 메서드 있음)

| Hub | Method | Path | 코드 | 상태 |
|---|---|---|---|---|
| API-025 | GET | `/api/health` | `HealthController` | 구현 · Bruno health 테스트 있음 |
| API-001 | GET | `/api/kiosk/categories` | `UserMenuController` | 구현 · 미검증 |
| API-002 | GET | `/api/kiosk/menuList` | `UserMenuController` | 구현 · 미검증 |
| API-003 | GET | `/api/kiosk/menuDetail/{menuId}` | `UserMenuController` | 구현 · 미검증 |
| API-004 | POST | `/api/kiosk/cart/validate` | `UserOrderController` | 구현 · 미검증 |
| API-005 | POST | `/api/kiosk/orders` | `UserOrderController` | 구현 · 미검증 |
| API-006 | POST | `/api/kiosk/payments` | `UserPayController` | 구현 · 미검증. `PaymentProcessingPage` → `approvePayment` 호출. CARD 직접 승인, KAKAO/NAVER/TOSS는 토스 SDK `tossPayment` body 포함 |
| API-014 | GET | `/api/kiosk/payment-methods` | `UserPayController` | 구현 · `PaymentPage`가 `getPaymenMethods` 호출. JSON 키 `active` (DB `pay_method_cfg.active`. 구 `isEnabled` 폐기) |
| API-007 | GET | `/api/admin/orders` | `AdminOrderController` | 구현 · 미검증. query: page,size,orderStatus,paymentStatus,orderType,dateFrom,dateTo,keyword |
| API-022 | GET | `/api/admin/orders/{orderId}` | 동상 | 구현 · 미검증 |
| API-021 | GET | `/api/admin/orders/live` | 동상 | 구현 · 미검증 |
| API-008 | PATCH | `/api/admin/orders/{orderId}/{status}` | 동상 | 구현 · path status=`PREPARING`\|`COMPLETED` · body 없음 |
| API-024 | PATCH | `/api/admin/orders/{orderId}/cancel` | 동상 | 구현 · 미검증 |
| — | PATCH | `/api/admin/orders/{orderId}/refund` | `AdminOrderController` | 구현 · 미검증. body `refundReasonCode`, `refundReasonDetail`(OTHER 시 필수). Hub id **449** |
| — | GET | `/api/admin/refund-reasons` | `AdminRefundReasonController` | 구현 · 미검증. `common_code` 그룹 `REFUND_REASON`. Hub id **457** |
| API-011 | GET | `/api/admin/menus` | `AdminMenuController` | 구현 · query categoryId,keyword,isSoldOut,tagId,page,size,sort |
| API-023 | GET | `/api/admin/menus/{menuId}` | 동상 | 구현 |
| API-026 | GET | `/api/admin/menus/categories` | 동상 | 구현 · `/{menuId}`보다 위에 선언 |
| API-027 | GET | `/api/admin/menus/ingredients` | 동상 | 구현 |
| API-012 | POST | `/api/admin/menus` | 동상 | 구현 · 브라우저 E2E 미실행 |
| API-013 | PATCH | `/api/admin/menus/{menuId}` | 동상 | 구현 · 브라우저 E2E 미실행 |
| API-028 | DELETE | `/api/admin/menus/{menuId}` | 동상 | 구현 · **soft delete** (`deleted_at`) |
| API-029 | GET | `/api/admin/opts/groups` | `AdminOptionController` | 구현 |
| API-030 | GET | `/api/admin/opts/{optionGroupId}` | 동상 | 구현 |
| API-015 | GET | `/api/admin/paymentMethods` | `AdminPaymentMethodController` | 구현 · 런타임 미검증. 응답 필드 `active`, `sortNo` (`receiptMessage`는 계약 없음) |
| API-016 | PATCH | `/api/admin/paymentMethods/{methodId}` | 동상 | 구현 · 런타임 미검증. body `active`, `sortNo`만. 한 행만 수정 — 여러 행 재정렬·409는 미제공 |
| API-020 | GET | `/api/admin/dashboard` | `AdminSalesController` | 구현 · `AdminDashboardResponse` |
| API-018 | GET | `/api/admin/sales/summary` | 동상 | 구현 · query `period=today\|week\|month` |
| API-019 | GET | `/api/admin/sales/monthly` | 동상 | 구현 · query `year=YYYY` |
| API-017 | GET | `/api/admin/sales/daily` | 동상 | 구현 · query `from=YYYY-MM-DD`, `to` 선택 |
| — | GET | `/api/admin/sales/daily/time-slots` | 동상 | 구현 · query `date`, `intervalMinutes=30\|60` |

`AdminOrderController`의 class mapping은 `"api/admin/orders"`(선행 `/` 없음)다. Spring은 보통 동일하게 `/api/admin/orders`로 붙는다.

## 스텁 (클래스만, 메서드 없음)

| Hub | Method | Path | 비고 |
|---|---|---|---|
| API-009 | PATCH | `/api/admin/soldOut` | `AdminSoldOutController` 비어 있음. TODO body `changes[]` |
| API-010 | GET | `/api/admin/soldOut` | 동상 |
| — | POST | `/api/admin/login` | `AdminAuthController` TODO. **2026-08-25 계약 확정**: body `{storeNumber}`, `storeNumber == "0001"` 하드코드 비교만(DB 조회·AuthenticationManager·JWT 없음). 불일치 401(ErrorCode 미정), 일치 시 단순 승인 플래그(`{approved:true}` 형태) 응답. 미구현 |

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
| RTOS-DEVICE-001 | POST | `/api/orders/{orderId}/receipt-print` | 8/21 최소 범위 **결정 필요**. 코드 없음 |
| RTOS-DEVICE-004~006 | POST | `/api/device/scan` | EXCLUDED |
| KSD-MEMBER-001 | POST | `/api/membership/stamps` | FUTURE |
| — | GET | `/api/ui/accessibility-options` | 코드 없음 |

## 키오스크 계약 요약

| ID | Request | 성공 data 요지 |
|---|---|---|
| API-001 | — | `[{categoryId, categoryName, sortOrder, isActive}]` |
| API-002 | — | `{categories, menus[{menuId, categoryId, name, price, imageUrl, isSoldOut, ...}]}` |
| API-003 | path menuId | 상세 + `ingredients` + `optionGroups` |
| API-004 | `{items:[{menuId, quantity, optionItems[{optionItemId,quantity}], excludedIngredientIds}]}` | `totalAmount` 등 |
| API-005 | `{orderType: EAT_IN\|TAKE_OUT, items:[...]}` | `orderId, orderNo, totalAmount, status(=READY)` |
| API-006 | `{orderId, orderStatus(=RECEIVED), paymentMethodCode, idempotencyKey, tossPayment?}` | `paymentId, orderId, orderNo, paymentStatus, approvedAmount, approvedAt, waitingOrderCount` · CARD는 `tossPayment` 없음, 간편결제는 토스 SDK 결과 포함 |
| API-014 | — | `{methods:[{methodId, methodCode, methodName, imageAssetId, imageUrl, description, active, sortOrder}]}` |

### 키오스크 FE 연결 (2026-08-28 · main · 미검증)

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
