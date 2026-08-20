# Admin Dashboard · Sales DTO / API 설계 정리

> 기준 화면: Dashboard / Sales Summary / Monthly Sales / Daily Sales  
> 목적: 프론트 실제 사용 필드 기준으로 API 응답과 DTO 구조를 정리하고, 중복 데이터와 UI 전용 필드를 제거한다.

---

## 1. 결론

페이지는 4개지만, 실제 API 응답 DTO는 **5개**로 나누는 것이 가장 자연스럽다.

| 화면 | 호출 API | Response DTO |
| --- | --- | --- |
| Dashboard | `GET /api/admin/dashboard` | `AdminDashboardResponse` |
| Sales Summary | `GET /api/admin/sales/summary` | `SalesSummaryResponse` |
| Monthly Sales | `GET /api/admin/sales/monthly` + `GET /api/admin/sales/daily` | `MonthlySalesResponse` + `DailySalesResponse` |
| Daily Sales | `GET /api/admin/sales/daily` + `GET /api/admin/sales/daily/time-slots` | `DailySalesResponse` + `List<DailySalesTimeSlotResponse>` |

핵심은 **페이지별 DTO 1개**가 아니라, **API 책임별 DTO**로 나누는 것이다.

특히:

- `DailySalesResponse`는 Summary / Monthly / Daily에서 공통으로 재사용한다.
- Daily의 30분 / 1시간 단위 데이터는 `time-slots` 별도 API로 분리한다.
- `fill`, `barHeight` 같은 차트 렌더링 값은 API에서 보내지 않는다.
- 랭킹 필드명은 Summary / Monthly / Daily 모두 동일하게 맞춘다.

---

# 2. 공통 응답 Wrapper

아래 필드는 개별 DTO마다 반복해서 넣지 않는다.

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_XXX_SUCCESS",
  "message": "응답 메시지",
  "data": {}
}
```

기존 공통 응답 객체가 있다면 다음처럼 사용한다.

```java
ApiResponse<AdminDashboardResponse>
ApiResponse<SalesSummaryResponse>
ApiResponse<MonthlySalesResponse>
ApiResponse<DailySalesResponse>
ApiResponse<List<DailySalesTimeSlotResponse>>
```

즉 각 Response DTO는 **`data` 내부 구조만 담당**한다.

---

# 3. 공용 DTO

## 3.1 `SalesKpiResponse`

Dashboard와 Summary에서 공용으로 사용할 수 있다.

```java
@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SalesKpiResponse {

    private String label;
    private long value;
    private String display;

    // Summary에서만 사용
    private Double delta;
    private String deltaLabel;
}
```

### Dashboard 예시

```json
{
  "label": "오늘 매출",
  "value": 392500,
  "display": "392,500원"
}
```

### Summary 예시

```json
{
  "label": "총매출",
  "value": 6842500,
  "display": "6,842,500원",
  "delta": 12.4,
  "deltaLabel": "전월 대비"
}
```

---

## 3.2 `SalesShareResponse`

결제수단 비중과 주문유형 비중 공용.

```java
@Getter
@Builder
public class SalesShareResponse {

    private String label;
    private double percent;
}
```

예시:

```json
{
  "label": "카드",
  "percent": 65
}
```

### 제외할 필드

```json
{
  "fill": 260
}
```

`fill`은 API 데이터가 아니라 차트 렌더링 값이므로 제외한다.

---

## 3.3 `MenuSalesRankingResponse`

Summary / Monthly / Daily의 인기 메뉴 랭킹 필드명을 통일한다.

```java
@Getter
@Builder
public class MenuSalesRankingResponse {

    private int rank;
    private Long menuId;
    private String menuName;
    private int orderCount;
    private long salesAmount;
}
```

예시:

```json
{
  "rank": 1,
  "menuId": 2037,
  "menuName": "우삼겹 포케",
  "orderCount": 9,
  "salesAmount": 106000
}
```

### 프론트 필드도 통일

기존 Monthly / Daily:

```js
row.name
row.count
row.amount
```

통일 후:

```js
row.menuName
row.orderCount
row.salesAmount
```

Summary는 이미 이 이름을 사용하고 있으므로 이 형태를 기준으로 맞추는 것이 좋다.

---

# 4. Dashboard

## 4.1 API

```http
GET /api/admin/dashboard
```

## 4.2 Response DTO

```java
@Getter
@Builder
public class AdminDashboardResponse {

    private String dateLabel;

    private List<SalesKpiResponse> kpis;

    private List<DashboardRecentOrderResponse> recentOrders;

    private List<DashboardOrderStatusResponse> statusSummary;

    private DashboardOrderTypeSummaryResponse orderTypeSummary;

    private List<DashboardInventoryAlertResponse> inventoryAlerts;

    private List<DashboardWeeklySalesResponse> weeklySales;
}
```

### `DashboardRecentOrderResponse`

```java
@Getter
@Builder
public class DashboardRecentOrderResponse {

    private String orderNo;
    private String orderType;
    private String menuSummary;
    private long totalAmount;
    private String orderStatus;
    private String createdAtLabel;
}
```

### `DashboardOrderStatusResponse`

```java
@Getter
@Builder
public class DashboardOrderStatusResponse {

    private String label;
    private int count;
    private String tone;
}
```

> `tone`은 현재 UI와의 호환을 위해 유지 가능하다. 장기적으로는 상태 코드만 보내고 FE에서 스타일을 매핑하는 편이 더 깔끔하다.

### `DashboardOrderTypeSummaryResponse`

```java
@Getter
@Builder
public class DashboardOrderTypeSummaryResponse {

    private int eatIn;
    private int takeOut;
}
```

### `DashboardInventoryAlertResponse`

```java
@Getter
@Builder
public class DashboardInventoryAlertResponse {

    private String label;
    private String badge;
    private String tone;
}
```

### `DashboardWeeklySalesResponse`

차트 라이브러리 사용 기준으로 `barHeight`는 제거한다.

```java
@Getter
@Builder
public class DashboardWeeklySalesResponse {

    private String label;
    private long amount;
    private Boolean isCurrent;
}
```

예시:

```json
{
  "label": "20일",
  "amount": 392500,
  "isCurrent": true
}
```

제거:

```json
{
  "barHeight": 113
}
```

차트 라이브러리가 `amount` 기준으로 높이를 계산하게 한다.

## 4.3 Dashboard 최종 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_DASHBOARD_SUCCESS",
  "message": "대시보드 요약",
  "data": {
    "dateLabel": "2026.07.20",
    "kpis": [
      {
        "label": "오늘 매출",
        "value": 392500,
        "display": "392,500원"
      }
    ],
    "recentOrders": [
      {
        "orderNo": "A-20260720-001",
        "orderType": "TAKE_OUT",
        "menuSummary": "오리엔탈 우삼겹 샐러드 외 1",
        "totalAmount": 15800,
        "orderStatus": "RECEIVED",
        "createdAtLabel": "09:05"
      }
    ],
    "statusSummary": [
      {
        "label": "대기",
        "count": 43,
        "tone": "waiting"
      }
    ],
    "orderTypeSummary": {
      "eatIn": 14,
      "takeOut": 22
    },
    "inventoryAlerts": [
      {
        "label": "타코 쉬림프 포케볼",
        "badge": "품절",
        "tone": "danger"
      }
    ],
    "weeklySales": [
      {
        "label": "20일",
        "amount": 392500,
        "isCurrent": true
      }
    ]
  }
}
```

---

# 5. Sales Summary

## 5.1 API

```http
GET /api/admin/sales/summary?period=month
```

사용 기간:

```text
period=today
period=week
period=month
```

## 5.2 Response DTO

```java
@Getter
@Builder
public class SalesSummaryResponse {

    private String label;
    private String dateRange;

    private List<String> availablePeriods;

    private List<SalesKpiResponse> kpis;

    private List<HourlySalesResponse> hourlySales;

    private List<SalesShareResponse> paymentShare;

    private List<SalesShareResponse> orderShare;

    private List<MenuSalesRankingResponse> ranking;
}
```

## 5.3 시간대별 매출

기존 mock의 `chartBars`처럼 픽셀 높이를 직접 보내지 않는다.

```java
@Getter
@Builder
public class HourlySalesResponse {

    private int hour;
    private long salesAmount;
}
```

예시:

```json
[
  {
    "hour": 10,
    "salesAmount": 152000
  },
  {
    "hour": 11,
    "salesAmount": 248000
  }
]
```

FE에서는 차트 라이브러리에서 `salesAmount`를 `dataKey`로 사용한다.

```js
const chartData = data.hourlySales.map((item) => ({
  hour: `${item.hour}시`,
  salesAmount: item.salesAmount,
}));
```

## 5.4 Summary 최종 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_SALES_SUMMARY_SUCCESS",
  "message": "매출 요약",
  "data": {
    "label": "이번 달",
    "dateRange": "2026.07.01 ~ 2026.07.20",
    "availablePeriods": ["today", "week", "month"],
    "kpis": [
      {
        "label": "월 총매출",
        "value": 6842500,
        "display": "6,842,500원",
        "delta": 12.4,
        "deltaLabel": "전월 대비"
      }
    ],
    "hourlySales": [
      {
        "hour": 10,
        "salesAmount": 152000
      }
    ],
    "paymentShare": [
      {
        "label": "카드",
        "percent": 65
      }
    ],
    "orderShare": [
      {
        "label": "매장",
        "percent": 42
      }
    ],
    "ranking": [
      {
        "rank": 1,
        "menuId": 1,
        "menuName": "로스트닭다리살 샐러드",
        "orderCount": 120,
        "salesAmount": 1536000
      }
    ]
  }
}
```

---

# 6. Monthly Sales

## 6.1 호출 API

Monthly 화면은 실제로 두 데이터를 조합한다.

```http
GET /api/admin/sales/monthly
GET /api/admin/sales/daily
```

Monthly API가 담당:

- 월 누적 매출
- 월 주문 수
- 월 평균 객단가
- 월 인기 메뉴

Daily API가 담당:

- 일별 매출 차트
- 일별 주문 수 차트
- 평일 / 주말 계산
- 일자별 상세

## 6.2 `MonthlySalesResponse`

```java
@Getter
@Builder
public class MonthlySalesResponse {

    private int year;

    private List<MonthlySalesRowResponse> rows;

    private Map<String, List<MenuSalesRankingResponse>> ranking;
}
```

## 6.3 `MonthlySalesRowResponse`

```java
@Getter
@Builder
public class MonthlySalesRowResponse {

    // 예: "2026-07"
    private String month;

    private int orderCount;
    private long totalAmount;
    private long avgAmount;
}
```

## 6.4 Monthly 최종 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_SALES_MONTHLY_SUCCESS",
  "message": "월별 매출",
  "data": {
    "year": 2026,
    "rows": [
      {
        "month": "2026-07",
        "orderCount": 642,
        "totalAmount": 6842500,
        "avgAmount": 10658
      }
    ],
    "ranking": {
      "2026-07": [
        {
          "rank": 1,
          "menuId": 2037,
          "menuName": "우삼겹 포케",
          "orderCount": 120,
          "salesAmount": 1536000
        }
      ]
    }
  }
}
```

---

# 7. Daily Sales

## 7.1 호출 API

Daily 화면도 두 API를 사용한다.

```http
GET /api/admin/sales/daily
GET /api/admin/sales/daily/time-slots
```

---

# 8. `DailySalesResponse`

`DailySalesResponse`는 Summary / Monthly / Daily 화면에서 공용으로 사용하는 기초 데이터 역할을 한다.

```java
@Getter
@Builder
public class DailySalesResponse {

    private LocalDate from;
    private LocalDate to;

    private List<DailySalesRowResponse> rows;

    private Map<String, List<MenuSalesRankingResponse>> ranking;

    private Map<String, DailySalesBreakdownResponse> breakdown;
}
```

## 8.1 `DailySalesRowResponse`

```java
@Getter
@Builder
public class DailySalesRowResponse {

    private LocalDate date;

    private int orderCount;

    private long totalAmount;

    private long avgAmount;
}
```

## 8.2 `DailySalesBreakdownResponse`

```java
@Getter
@Builder
public class DailySalesBreakdownResponse {

    private List<SalesShareResponse> paymentShare;

    private List<SalesShareResponse> orderShare;
}
```

## 8.3 Daily 메인 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_SALES_DAILY_SUCCESS",
  "message": "일별 매출",
  "data": {
    "from": "2026-07-01",
    "to": "2026-07-31",
    "rows": [
      {
        "date": "2026-07-20",
        "orderCount": 30,
        "totalAmount": 318000,
        "avgAmount": 10600
      }
    ],
    "ranking": {
      "2026-07-20": [
        {
          "rank": 1,
          "menuId": 2037,
          "menuName": "우삼겹 포케",
          "orderCount": 9,
          "salesAmount": 106000
        }
      ]
    },
    "breakdown": {
      "2026-07-20": {
        "paymentShare": [
          {
            "label": "카드",
            "percent": 65
          }
        ],
        "orderShare": [
          {
            "label": "매장",
            "percent": 42
          },
          {
            "label": "포장",
            "percent": 58
          }
        ]
      }
    }
  }
}
```

---

# 9. Daily Time Slots

30분 / 1시간 단위는 Daily 메인 응답에 넣지 않고 별도 API로 조회한다.

## 9.1 API

```http
GET /api/admin/sales/daily/time-slots?date=2026-07-20&intervalMinutes=30
```

또는:

```http
GET /api/admin/sales/daily/time-slots?date=2026-07-20&intervalMinutes=60
```

## 9.2 DTO

```java
@Getter
@Builder
public class DailySalesTimeSlotResponse {

    private int salesHour;

    private int salesMinute;

    private int orderCount;

    private long netSalesAmount;

    private long averageOrderAmount;
}
```

## 9.3 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_SALES_TIME_SLOTS_SUCCESS",
  "message": "시간대별 매출",
  "data": [
    {
      "salesHour": 9,
      "salesMinute": 0,
      "orderCount": 3,
      "netSalesAmount": 28000,
      "averageOrderAmount": 9333
    },
    {
      "salesHour": 9,
      "salesMinute": 30,
      "orderCount": 2,
      "netSalesAmount": 19500,
      "averageOrderAmount": 9750
    }
  ]
}
```

현재 Daily FE의 변환 함수와도 자연스럽게 맞는다.

```js
function toTimeSlot(row) {
  return {
    hour: row.salesHour ?? row.hour,
    minute: row.salesMinute ?? row.minute ?? 0,
    orderCount: row.orderCount ?? 0,
    totalAmount: row.netSalesAmount ?? row.totalAmount ?? 0,
    avgAmount: row.averageOrderAmount ?? row.avgAmount ?? 0,
  };
}
```

---

# 10. 페이지별 데이터 조합

## Dashboard

```text
DashboardPage
└─ GET /dashboard
   └─ AdminDashboardResponse
      ├─ dateLabel
      ├─ kpis
      ├─ recentOrders
      ├─ statusSummary
      ├─ orderTypeSummary
      ├─ inventoryAlerts
      └─ weeklySales
```

## Sales Summary

```text
SalesSummaryPage
├─ GET /sales/summary
│  └─ SalesSummaryResponse
│     ├─ KPI
│     ├─ 시간대별 매출
│     ├─ 결제수단 비중
│     ├─ 주문유형 비중
│     └─ 인기 메뉴
│
└─ GET /sales/daily
   └─ DailySalesResponse
      └─ 하단 일자별 매출 테이블
```

## Monthly Sales

```text
MonthlySalesPage
├─ GET /sales/monthly
│  └─ MonthlySalesResponse
│     ├─ 선택 월 KPI
│     └─ 월 인기 메뉴
│
└─ GET /sales/daily
   └─ DailySalesResponse
      ├─ 일별 매출 추이
      ├─ 일별 주문 수
      ├─ 평일 vs 주말
      └─ 일자별 상세
```

## Daily Sales

```text
DailySalesPage
├─ GET /sales/daily
│  └─ DailySalesResponse
│     ├─ 선택 일 KPI
│     ├─ 전일 대비 계산
│     ├─ 결제수단별 비중
│     ├─ 주문유형별 비중
│     └─ 메뉴 판매 순위
│
└─ GET /sales/daily/time-slots
   └─ List<DailySalesTimeSlotResponse>
      ├─ 30분 단위
      └─ 1시간 단위
```

---

# 11. 차트 라이브러리 사용 기준

차트 라이브러리를 사용할 예정이므로 API는 **업무 데이터만 전달**한다.

## API에서 내려줄 값

```text
amount
salesAmount
orderCount
percent
hour
date
```

## API에서 제거할 값

```text
barHeight
fill
weekdayWidth
weekendWidth
```

이 값들은 렌더링 전용 값이다.

## 주간 매출 예시

나쁜 형태:

```json
{
  "label": "20일",
  "amount": 392500,
  "barHeight": 113
}
```

권장:

```json
{
  "label": "20일",
  "amount": 392500
}
```

차트 라이브러리:

```jsx
<Bar dataKey="amount" />
```

## 결제수단 예시

나쁜 형태:

```json
{
  "label": "카드",
  "percent": 65,
  "fill": 260
}
```

권장:

```json
{
  "label": "카드",
  "percent": 65
}
```

FE:

```js
const chartData = paymentShare.map((item) => ({
  name: item.label,
  value: item.percent,
}));
```

---

# 12. DTO 파일 구조 추천

```text
dto/response/admin/
├─ AdminDashboardResponse.java
├─ DashboardRecentOrderResponse.java
├─ DashboardOrderStatusResponse.java
├─ DashboardOrderTypeSummaryResponse.java
├─ DashboardInventoryAlertResponse.java
└─ DashboardWeeklySalesResponse.java


dto/response/sales/
├─ SalesSummaryResponse.java
├─ MonthlySalesResponse.java
├─ MonthlySalesRowResponse.java
├─ DailySalesResponse.java
├─ DailySalesRowResponse.java
├─ DailySalesBreakdownResponse.java
├─ DailySalesTimeSlotResponse.java
├─ HourlySalesResponse.java
│
├─ SalesKpiResponse.java
├─ SalesShareResponse.java
└─ MenuSalesRankingResponse.java
```

---

# 13. 최종 정리

## 유지

- Dashboard는 전용 DTO 하나로 구성
- Summary는 자체 요약 데이터 전용
- Monthly는 월 단위 집계만 담당
- Daily는 일 단위 공용 기초 데이터 역할
- 시간대 30분 / 1시간 조회는 별도 API 유지

## 통일

랭킹:

```text
rank
menuId
menuName
orderCount
salesAmount
```

비중:

```text
label
percent
```

일별 기본:

```text
date
orderCount
totalAmount
avgAmount
```

## 제거

```text
fill
barHeight
```

그리고 가능하면 장기적으로:

```text
tone
display
createdAtLabel
dateLabel
```

같은 표시 전용 값도 FE 책임으로 옮길 수 있다.

단, 현재 화면 수정량을 최소화하려면 이 값들은 우선 유지해도 된다.

---

# 14. 지금 구현 순서

1. 공용 DTO 생성
   - `SalesKpiResponse`
   - `SalesShareResponse`
   - `MenuSalesRankingResponse`

2. `DailySalesResponse` 정리
   - `rows`
   - `ranking`
   - `breakdown`
   - 기존 mock용 `hourly` 제거

3. `DailySalesTimeSlotResponse` 별도 유지
   - 30분 / 60분 조회

4. `MonthlySalesResponse` 생성
   - `year`
   - `rows`
   - `ranking`

5. `SalesSummaryResponse` 생성
   - `chartBars` 대신 `hourlySales` 권장

6. `AdminDashboardResponse` 생성
   - `weeklySales.barHeight` 제거

7. FE 랭킹 필드명 통일
   - `name` → `menuName`
   - `count` → `orderCount`
   - `amount` → `salesAmount`

8. 차트 라이브러리 연결 후 UI 전용 계산 제거
