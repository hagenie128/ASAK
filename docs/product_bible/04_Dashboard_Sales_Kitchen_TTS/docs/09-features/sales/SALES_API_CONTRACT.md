# Sales API Contract

> Status: Draft

## Summary

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

## Monthly

```http
GET /api/admin/sales/monthly?year=2026
```

## Daily

```http
GET /api/admin/sales/daily?date=2026-07-16
```

## Rules

- amount는 integer
- ratio는 0~1
- 날짜는 ISO `YYYY-MM-DD`
- timezone은 Asia/Seoul
- 지원하지 않는 field는 반환하지 않는다


## Customer Count Contract

```text
customerCount = count(paymentStatus = APPROVED)
```

현재 Mock Data에서는 `orderCount`와 `customerCount`가 동일할 수 있다.

향후 한 결제에 여러 주문을 묶거나 회원 식별 기능이 추가되면 정의를 재검토한다.


## Customer Count Contract

```text
customerCount = count(paymentStatus = APPROVED)
```

현재 Mock Data에서는 `orderCount`와 `customerCount`가 동일할 수 있다. 향후 주문과 결제의 관계가 변경되면 정의를 재검토한다.
