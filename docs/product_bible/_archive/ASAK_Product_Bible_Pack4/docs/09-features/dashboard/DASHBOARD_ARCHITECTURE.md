# Dashboard Architecture

> Status: Current  
> Figma: SCR-022

## 1. 목적

Dashboard는 관리자가 로그인한 직후 매장 전체 상태를 3초 안에 파악하도록 한다. 주문 목록의 축약판이 아니라 운영 판단 화면이다.

## 2. KPI 정의

### 오늘 순매출

```text
승인 결제 합계 - 취소·환불 금액
```

환불 기능이 MVP에 없다면 승인 결제 합계로 계산한다.

### 주문 수

```text
paymentStatus = APPROVED인 주문 수
```

### 평균 객단가

```text
순매출 / 유효 주문 수
```

주문 수가 0이면 `-`로 표시한다.

### 진행 중 주문

```text
OrderStatus IN (RECEIVED, PREPARING)
```

## 3. 화면 구조

### 상단
- 오늘 매출
- 주문 수
- 평균 객단가
- 진행 중 주문

### 좌측 본문
- 실시간 주문 요약
- 상태별 주문 수
- 최근 주문

### 우측 본문
- 인기 메뉴 TOP 5
- 품절 현황
- 운영 알림

## 4. 데이터 갱신

| 데이터 | 권장 갱신 |
|---|---|
| 진행 주문 | 5~10초 polling |
| 오늘 매출 | 30~60초 |
| 인기 메뉴 | 5분 |
| 품절 | 변경 즉시 또는 30초 |

MVP는 페이지 진입 시 fetch + 30초 polling을 기본으로 하고, 진행 주문만 별도 5~10초 polling 가능하다.

## 5. API 전략

### 권장: Aggregate API

```http
GET /api/admin/dashboard
```

장점:
- 데이터 시점이 맞는다.
- 프론트 호출 수가 줄어든다.
- 화면 구현이 단순하다.

## 6. 응답 초안

```json
{
  "success": true,
  "data": {
    "summary": {
      "netSales": 842000,
      "orderCount": 72,
      "averageOrderValue": 11694,
      "activeOrderCount": 8
    },
    "orderStatusCounts": {
      "received": 3,
      "preparing": 5,
      "completed": 64
    },
    "popularMenus": [],
    "soldOutSummary": {
      "menuCount": 2,
      "ingredientCount": 3,
      "optionItemCount": 1
    },
    "recentOrders": [],
    "generatedAt": "2026-07-16T08:00:00"
  }
}
```

## 7. 필수 상태

- default
- loading
- empty
- error
- refreshing
- partialError

일부 widget만 실패하면 해당 카드만 Error 처리하고 전체 Dashboard는 유지한다.

## 8. React Mapping

```text
DashboardPage
DashboardSummary
SalesMetricCard
ActiveOrderSummary
RecentOrderList
PopularMenuList
SoldOutSummary
DashboardAlertPanel
```

## 9. 디자인 규칙

- 모든 KPI를 초록색으로 만들지 않는다.
- 진행 중 주문과 경고 상태만 기능색을 적극 사용한다.
- 장식보다 숫자와 상태를 먼저 보여준다.
- Navbar Home을 활성화한다.

## 10. 구현 체크리스트

- [ ] SCR-022 registry
- [ ] route `/`
- [ ] 로그인 성공 후 Dashboard
- [ ] aggregate DTO
- [ ] KPI 계산 정의
- [ ] polling
- [ ] partial error
- [ ] last updated
- [ ] 0건 상태
