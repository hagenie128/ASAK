# Dashboard Implementation

## Endpoint

```http
GET /api/admin/dashboard
```

## Aggregate

- netSales
- orderCount
- averageOrderValue
- activeOrderCount
- statusCounts
- popularMenus
- soldOutSummary
- recentOrders
- generatedAt

## 구현 방식

MVP 권장:

- DashboardQueryService
- 여러 Repository 조합
- readOnly transaction

## partialError

Backend aggregate API에서는 전체 실패가 단순하다.

Frontend widget partialError를 원하면 API를 분리하거나 nullable field + error metadata를 설계한다.

MVP는 전체 aggregate 성공을 우선한다.
