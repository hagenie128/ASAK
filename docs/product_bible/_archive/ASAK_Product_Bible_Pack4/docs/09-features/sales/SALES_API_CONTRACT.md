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
