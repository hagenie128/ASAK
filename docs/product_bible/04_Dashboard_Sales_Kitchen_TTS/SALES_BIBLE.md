# Sales Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `SALES_API_CONTRACT.md`
- `SALES_ARCHITECTURE.md`
- `SALES_CANCELLATION_REFUND_RULES.md`
- `SALES_DATA_INTEGRITY_AND_QA.md`

---

## 원문: `SALES_API_CONTRACT.md`

### Sales API Contract

> Status: Draft

#### Summary

```http
GET /api/admin/sales/summary?startDate=2026-07-01&endDate=2026-07-16
```

```json
{
  "success": true,
  "data": {
    "period": {
      "startDate": "2026-07-01",
      "endDate": "2026-07-16",
      "preset": "CUSTOM",
      "comparisonLabel": "직전 동일 기간 대비"
    },
    "kpis": {
      "netSales": 8420000,
      "orderCount": 723,
      "customerCount": 723,
      "averageOrderValue": 11646,
      "comparisonRate": 0.15
    },
    "dailyTrend": [
      {"date": "2026-07-01", "salesAmount": 510000, "orderCount": 42}
    ],
    "hourlyTrend": [
      {"hour": 12, "salesAmount": 680000, "orderCount": 58}
    ],
    "popularMenus": [],
    "orderTypeRatio": []
  }
}
```

#### Monthly

```http
GET /api/admin/sales/monthly?year=2026
```

#### Daily

```http
GET /api/admin/sales/daily?date=2026-07-16
```

#### Rules

- amount는 integer
- ratio는 0~1
- 날짜는 ISO `YYYY-MM-DD`
- timezone은 Asia/Seoul
- 지원하지 않는 field는 반환하지 않는다


#### Customer Count Contract

```text
customerCount = count(paymentStatus = APPROVED)
```

현재 Mock Data에서는 `orderCount`와 `customerCount`가 동일할 수 있다.

향후 한 결제에 여러 주문을 묶거나 회원 식별 기능이 추가되면 정의를 재검토한다.


#### Customer Count Contract

```text
customerCount = count(paymentStatus = APPROVED)
```

현재 Mock Data에서는 `orderCount`와 `customerCount`가 동일할 수 있다. 향후 주문과 결제의 관계가 변경되면 정의를 재검토한다.

---

## 원문: `SALES_ARCHITECTURE.md`

### Sales Architecture

> Status: Current
> Figma: SCR-019, SCR-020, SCR-021

#### 1. 목적

Sales는 주문·결제 데이터를 집계해 매장 성과를 해석하도록 돕는다. 차트를 많이 보여주는 것이 아니라 매출 변화, 주문 피크, 인기 메뉴, 객단가를 설명해야 한다.

#### 2. 안정적으로 계산 가능한 데이터

- orderId
- orderNo
- orderType
- orderStatus
- paymentStatus
- approvedAmount
- createdAt
- menuName
- quantity
- categoryCode

계산 가능:
- 일별·월별 매출
- 주문 수
- 평균 객단가
- 인기 메뉴
- 카테고리별 매출
- 주문 유형 비율

#### 3. 추가 계약이 필요한 지표

- 고객 수
- 재방문율
- 회원별 매출
- 목표 달성률
- 전년 대비
- 환불률
- 결제수단별 매출

계약 전에는 제거하거나 `Mock`, `데이터 연결 예정`으로 표시한다.

#### 4. KPI 정의

```text
netSales = approvedAmount - refundedAmount
orderCount = APPROVED 주문 수
averageOrderValue = netSales / orderCount
```

#### 5. 화면 책임

##### SCR-019 Sales Summary
- KPI
- 매출 추이
- 시간대별 주문·매출
- 인기 메뉴
- 주문 유형 또는 결제수단 비율
- 상세표

##### SCR-020 Monthly Sales
- 월별 추이
- 전월 대비
- 주문 수
- 평균 객단가

##### SCR-021 Daily Sales
- 특정 날짜
- 시간대별 매출
- 피크타임
- 인기 메뉴
- 주문 상세

#### 6. 날짜 범위

```js
{
  startDate: "2026-07-01",
  endDate: "2026-07-16",
  preset: "THIS_MONTH"
}
```

Preset:
- TODAY
- THIS_WEEK
- THIS_MONTH
- CUSTOM

#### 7. 비교 문구

| Preset | Label |
|---|---|
| TODAY | 전일 대비 |
| THIS_WEEK | 전주 대비 |
| THIS_MONTH | 전월 대비 |
| CUSTOM | 직전 동일 기간 대비 |

고정 `전월 대비` 사용 금지.

#### 8. 시간대 정책

```text
Timezone: Asia/Seoul
Day boundary: 00:00:00 ~ 23:59:59
```

#### 9. React Mapping

```text
SalesSummaryPage
MonthlySalesPage
DailySalesPage
SalesMetricCard
SalesTrendChart
HourlySalesChart
PopularMenuTable
SalesDetailTable
DateRangePicker
SalesPeriodFilter
```

#### 10. 구현 체크리스트

- [ ] KPI 정의
- [ ] DateRangePicker 연결
- [ ] comparisonLabel 동적
- [ ] timezone
- [ ] summary API
- [ ] monthly API
- [ ] daily API
- [ ] Mock 표시
- [ ] loading/empty/error

---

## 원문: `SALES_CANCELLATION_REFUND_RULES.md`

### Sales Cancellation and Refund Rules

> Status: Current (2026-07-23)
> Related: API-024, DEV-ORDER-002, SCR-010, SCR-019, SCR-020, SCR-021

#### 1. Timestamp preservation

- `payment.paid_at` is the original approval time. A later cancellation or refund must not erase it.
- `orders.canceled_at` records when an order is cancelled.
- `payment.refunded_at` records when an approved payment is refunded.

#### 2. Cancellation state transition

Only orders in `RECEIVED` or `PREPARING` may be cancelled.

1. Set the order status to `CANCELED` and populate `orders.canceled_at`.
2. If the payment was approved, retain `payment.paid_at`, set the payment status to `REFUNDED`, and populate `payment.refunded_at`.
3. A completed or already-cancelled order returns `409 ORDER_CANCEL_NOT_ALLOWED`.

#### 3. Completed-order refund

A refund after the product has been handed to the customer is a payment action, not an order cancellation.

1. Only a `COMPLETED` order with an `APPROVED` payment may use the separate refund API.
2. Keep the order status as `COMPLETED`; do not add `REFUNDED` to `OrderStatus`.
3. Set the payment status to `REFUNDED` and populate `payment.refunded_at`, while preserving `payment.paid_at`.
4. A non-completed order, unpaid order, or already-refunded payment returns `409 ORDER_REFUND_NOT_ALLOWED`.

#### 4. Sales aggregation

- Gross sales includes every payment with a non-null `paid_at`, including a payment later refunded.
- Cancelled amount includes only a paid transaction whose order is `CANCELED` or whose payment is `CANCELED` or `REFUNDED`.
- Net sales equals gross sales minus cancelled amount. A fully refunded payment therefore contributes zero net sales, never a negative amount.
- Sales date and hour use the original `paid_at`; an unpaid cancellation falls back to the order creation timestamp only for cancellation counts.

#### 5. Menu sales and ranking

`vw_top_menu_daily` and `vw_top_menu_hourly` include an item only when:

- `payment.paid_at` is not null;
- the order status is not `CANCELED`; and
- the payment status is neither `CANCELED` nor `REFUNDED`.

Cancelled or refunded order items must not affect menu quantity, order count, sales amount, or popularity ranking.

#### 6. Verification

- No row in `vw_sales_daily` or `vw_sales_hourly` may have negative `net_sales_amount`.
- The sales views and top-menu views must use the same cancellation/refund predicates.

---

## 원문: `SALES_DATA_INTEGRITY_AND_QA.md`

### Sales Data Integrity and QA

#### 현재 Figma 즉시 수정 대상

- SCR-019 반복 날짜 `2025.02.22`
- SCR-021 반복 날짜
- 고객 수 정의 누락
- 동일 패턴의 고객수/매출 차트
- 고정 비교 문구
- 지원되지 않는 성장률·환불 지표
- 카테고리 명칭 불일치

#### 차트와 표 정합성

```text
sum(chart sales) = KPI netSales
sum(table sales) = KPI netSales
```

#### Empty

주문이 없으면:
- KPI 0
- chart empty
- table empty
- `선택한 기간에 주문 데이터가 없습니다.`

#### 비교율

```text
(current - previous) / previous
```

previous가 0이면 ratio는 null, 문구는 `비교 데이터 없음`.

#### QA

- [ ] 승인 결제만 포함
- [ ] timezone 경계
- [ ] previous 0 처리
- [ ] dynamic comparison label
- [ ] duplicate dummy 제거
- [ ] chart/table 합계
- [ ] filter reset
- [ ] API date validation
