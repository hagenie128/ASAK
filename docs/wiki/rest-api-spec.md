> Status: **CURRENT**
> 기준일: **2026-08-25** · 코드: `ASAK-back` Controller 매핑
> 계약 필드: [정본](../governance/contract-decisions-2026-07-16.md) · Bruno: `ASAK-back/api/`
> Hub API 카드: workspace 2 (기존 ID 갱신)
> 2026-08-25 결정: 관리자 로그인(매장 번호 하드코드)·환불 정책 확정 — 상세는
> [`admin-todo-2026-08-24.md`](../planning/admin-todo-2026-08-24.md) 참고.
> 2026-08-25 Hub 대조: API-015/016 카드를 실제 코드 기준으로 갱신 완료(구현 상태, 응답 필드명·shape 수정).
> 로그인·환불은 정본 API 번호가 아직 없어 Hub에 새 카드를 만들지 않음(기존 방침 유지).

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
| API-006 | POST | `/api/kiosk/payments` | `UserPayController` | 구현 · **계약 불일치:** Kiosk `API_ENDPOINTS.payments`는 `/payments`. `PaymentProcessingPage`는 `createOrder`만 호출하고 `approvePayment`는 미호출 |
| API-014 | GET | `/api/kiosk/payment-methods` | `UserPayController` | 구현 · `PaymentPage`가 `getPaymenMethods` 호출. JSON 키 `active` (DB `pay_method_cfg.active`. 구 `isEnabled` 폐기) |
| API-007 | GET | `/api/admin/orders` | `AdminOrderController` | 구현 · 미검증. query: page,size,orderStatus,paymentStatus,orderType,dateFrom,dateTo,keyword |
| API-022 | GET | `/api/admin/orders/{orderId}` | 동상 | 구현 · 미검증 |
| API-021 | GET | `/api/admin/orders/live` | 동상 | 구현 · 미검증 |
| API-008 | PATCH | `/api/admin/orders/{orderId}/{status}` | 동상 | 구현 · path status=`PREPARING`\|`COMPLETED` · body 없음 |
| API-024 | PATCH | `/api/admin/orders/{orderId}/cancel` | 동상 | 구현 · 미검증 |
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
| — | PATCH | `/api/admin/orders/{orderId}/refund` | `AdminOrderController` TODO(TODO-038). **2026-08-25 정책 확정**(TODO-001): order_status는 `CANCELED` 재사용, payment_status는 `REFUNDED`. 외부 결제사 API 먼저 호출 후 성공 시 DB 트랜잭션. 멱등성은 `payment_status` 상태 체크로만 보장, 별도 키 없음. 미구현 — 상세는 `admin-todo-2026-08-24.md` 참고 |

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
| API-006 | `{orderId, orderStatus(=READY), paymentMethodCode, idempotencyKey}` | `paymentId, orderId, orderNo, paymentStatus, approvedAmount, approvedAt, waitingOrderCount` · 금액은 서버 재계산 |
| API-014 | — | `{methods:[{methodId, methodCode, methodName, imageAssetId, imageUrl, description, active, sortOrder}]}` |

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
