# Sales Architecture

> Status: Current  
> Figma: SCR-019, SCR-020, SCR-021

## 1. 목적

Sales는 주문·결제 데이터를 집계해 매장 성과를 해석하도록 돕는다. 차트를 많이 보여주는 것이 아니라 매출 변화, 주문 피크, 인기 메뉴, 객단가를 설명해야 한다.

## 2. 안정적으로 계산 가능한 데이터

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

## 3. 추가 계약이 필요한 지표

- 고객 수
- 재방문율
- 회원별 매출
- 목표 달성률
- 전년 대비
- 환불률
- 결제수단별 매출

계약 전에는 제거하거나 `Mock`, `데이터 연결 예정`으로 표시한다.

## 4. KPI 정의

```text
netSales = approvedAmount - refundedAmount
orderCount = APPROVED 주문 수
averageOrderValue = netSales / orderCount
```

## 5. 화면 책임

### SCR-019 Sales Summary
- KPI
- 매출 추이
- 시간대별 주문·매출
- 인기 메뉴
- 주문 유형 또는 결제수단 비율
- 상세표

### SCR-020 Monthly Sales
- 월별 추이
- 전월 대비
- 주문 수
- 평균 객단가

### SCR-021 Daily Sales
- 특정 날짜
- 시간대별 매출
- 피크타임
- 인기 메뉴
- 주문 상세

## 6. 날짜 범위

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

## 7. 비교 문구

| Preset | Label |
|---|---|
| TODAY | 전일 대비 |
| THIS_WEEK | 전주 대비 |
| THIS_MONTH | 전월 대비 |
| CUSTOM | 직전 동일 기간 대비 |

고정 `전월 대비` 사용 금지.

## 8. 시간대 정책

```text
Timezone: Asia/Seoul
Day boundary: 00:00:00 ~ 23:59:59
```

## 9. React Mapping

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

## 10. 구현 체크리스트

- [ ] KPI 정의
- [ ] DateRangePicker 연결
- [ ] comparisonLabel 동적
- [ ] timezone
- [ ] summary API
- [ ] monthly API
- [ ] daily API
- [ ] Mock 표시
- [ ] loading/empty/error
