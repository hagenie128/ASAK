# Payment and Admin Implementation

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `PAYMENT_IMPLEMENTATION.md`
- `PAYMENT_METHOD_IMPLEMENTATION.md`
- `ADMIN_ORDER_IMPLEMENTATION.md`
- `DASHBOARD_IMPLEMENTATION.md`
- `SOLD_OUT_IMPLEMENTATION.md`

---

## 원문: `PAYMENT_IMPLEMENTATION.md`

### Payment Implementation

#### Entity

```text
Payment
PaymentMethod
```

#### PaymentStatus

```text
READY
APPROVED
FAILED
```

#### Endpoint

```http
POST /api/kiosk/payments
```

#### Service Flow

1. Order 조회
2. 이미 승인된 Payment 확인
3. PaymentMethod 활성 상태 검증
4. 승인 금액 = Order totalAmount
5. Mock 승인/실패 결정
6. Payment 저장
7. waitingOrderCount 계산
8. response 반환

#### 중복 방지

- orderId 기준 승인 Payment unique 검토
- idempotencyKey 저장 검토
- UI isSubmitting과 함께 3중 방어

---

## 원문: `PAYMENT_METHOD_IMPLEMENTATION.md`

### Payment Method Implementation

#### Current Code Status (2026-08-06)

- `AdminPaymentMethodController`는 `@RequestMapping("/api/admin/paymentMethods")`만 있고 메서드는 없다.
- `AdminPaymentMethodService`, `AdminPaymentMethodMapper`, `AdminPaymentMethodMapper.xml`도 구현 스텁 상태다.
- Admin 프론트 화면은 존재하지만 현재 `usePaymentMethodDraft` + mock repository로만 동작한다.
- 따라서 아래 필드/규칙은 현재 서버 구현 사실이 아니라 **구현 목표/초안**이다.

#### 상태

```text
ENABLED
DISABLED
MAINTENANCE
```

#### Kiosk 조회

활성/점검 중 수단만 정책에 따라 반환한다.

#### Admin 수정

필드:

```text
displayName
status
sortOrder
receiptMessage
failureRetentionMinutes
```

현재 프론트 저장 상태는 `methodId`, `isActive`, `sortOrder` 중심이며, `receiptMessage`, `failureRetentionMinutes`는 정적 정책 카드로만 노출된다.

#### 주의

전체 결제수단 비활성화는 ConfirmDialog와 Server validation이 필요하다.

#### Decision Needed

- 경로 표기를 `/paymentMethods`로 유지할지 kebab-case로 바꿀지
- 저장 방식을 개별 PATCH 순차 호출로 할지, 일괄 저장 endpoint로 둘지
- `MAINTENANCE` 상태와 키오스크 미리보기의 노출 규칙을 어디서 판정할지

---

## 원문: `ADMIN_ORDER_IMPLEMENTATION.md`

### Admin Order Implementation

#### Live Orders

```http
GET /api/admin/orders/live
```

조건:

```text
status IN (RECEIVED, PREPARING)
```

정렬:

```text
createdAt ASC
```

#### Order List

```http
GET /api/admin/orders
```

Filter:

- status
- orderType
- startDate
- endDate
- keyword
- page
- size

#### Order Detail

- items
- options
- payment
- timestamps

---

## 원문: `DASHBOARD_IMPLEMENTATION.md`

### Dashboard Implementation

#### Endpoint

```http
GET /api/admin/dashboard
```

#### Aggregate

- netSales
- orderCount
- averageOrderValue
- activeOrderCount
- statusCounts
- popularMenus
- soldOutSummary
- recentOrders
- generatedAt

#### 구현 방식

MVP 권장:

- DashboardQueryService
- 여러 Repository 조합
- readOnly transaction

#### partialError

Backend aggregate API에서는 전체 실패가 단순하다.

Frontend widget partialError를 원하면 API를 분리하거나 nullable field + error metadata를 설계한다.

MVP는 전체 aggregate 성공을 우선한다.

---

## 원문: `SOLD_OUT_IMPLEMENTATION.md`

### Sold-out Implementation

#### Current Code Status (2026-08-06)

- `AdminSoldOutController`는 `@RequestMapping("/api/admin/soldOut")`만 있고 메서드는 없다.
- `AdminSoldOutService`, `AdminSoldOutMapper`, `AdminSoldOutMapper.xml`도 구현 스텁 상태다.
- 따라서 아래 규칙은 현재 실행 중인 서버 동작이 아니라 **구현 목표/설계 메모**로 봐야 한다.

#### 대상

```text
MENU
INGREDIENT
OPTION_ITEM
```

#### Service Flow

1. 변경 목록 검증
2. 대상 조회
3. direct sold-out 변경
4. 영향 메뉴 계산
5. derived sold-out 갱신
6. 전체 transaction commit

#### 핵심 규칙

- CORE → 메뉴 품절
- BASE 일부 → 대체 가능성 확인
- BASE 전체 → 메뉴 품절
- STANDARD → 제거 가능 시 메뉴 유지
- OPTIONAL → 옵션만 disabled
- Required group 전체 불가 → 메뉴 품절

#### 복구

원인이 모두 해소되면 derived sold-out 해제.
directSoldOut이 true면 계속 품절.

#### Decision Needed

- 실제 PATCH body를 `targetType/targetId/isSoldOut`로 확정할지 여부
- `OPTION_ITEM` 대신 프론트 탭 값 `OPTION`과 어떤 호환 계층을 둘지 여부
- 영향 메뉴 수를 API가 직접 계산해 줄지 여부
