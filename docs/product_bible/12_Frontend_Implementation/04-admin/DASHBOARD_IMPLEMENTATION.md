# Dashboard Implementation

## Components

- SalesMetricCard
- ActiveOrderSummary
- PopularMenuList
- SoldOutSummary

## API

```text
GET dashboard
```

## State

```text
loading
error
data
isRefreshing
```

## Partial Error

API가 분리된 경우 widget별 error.
Aggregate API면 전체 상태 우선.

## 고객 수

Dashboard에서는 주문 수와 중복될 수 있으므로 기본 KPI는:

- 순매출
- 주문 수
- 객단가
- 진행 주문
