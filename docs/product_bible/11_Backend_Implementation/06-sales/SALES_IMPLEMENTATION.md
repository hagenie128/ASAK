# Sales Implementation

## 데이터 정의

```text
고객 수 = 결제 승인 건수
평균 객단가 = 총매출 / 고객 수
```

## Endpoints

```http
GET /api/admin/sales/summary
GET /api/admin/sales/monthly
GET /api/admin/sales/daily
```

## Mock Data

현재 포트폴리오용 Mock Data를 사용할 수 있다.

단:

- KPI 합계
- 차트 합계
- 표 합계
- 비율 100%
- 비교율

은 반드시 일치시킨다.

## 실제 query 구현 시

- paymentStatus = APPROVED
- Asia/Seoul date boundary
- amount integer
- group by date/hour/menu/category
