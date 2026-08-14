# Dashboard Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `DASHBOARD_ARCHITECTURE.md`
- `DASHBOARD_DECISIONS_AND_QA.md`

---

## 원문: `DASHBOARD_ARCHITECTURE.md`

### Dashboard Architecture

> Status: Current
> Figma: SCR-022

#### 1. 목적

Dashboard는 관리자가 로그인한 직후 매장 전체 상태를 3초 안에 파악하도록 한다. 주문 목록의 축약판이 아니라 운영 판단 화면이다.

#### 2. KPI 정의

##### 오늘 순매출

```text
승인 결제 합계 - 취소·환불 금액
```

환불 기능이 MVP에 없다면 승인 결제 합계로 계산한다.

##### 주문 수

```text
paymentStatus = APPROVED인 주문 수
```

##### 평균 객단가

```text
순매출 / 유효 주문 수
```

주문 수가 0이면 `-`로 표시한다.

##### 진행 중 주문

```text
OrderStatus IN (RECEIVED, PREPARING)
```

#### 3. 화면 구조

##### 상단
- 오늘 매출
- 주문 수
- 평균 객단가
- 진행 중 주문

##### 좌측 본문
- 실시간 주문 요약
- 상태별 주문 수
- 최근 주문

##### 우측 본문
- 인기 메뉴 TOP 5
- 품절 현황
- 운영 알림

#### 4. 데이터 갱신

| 데이터 | 권장 갱신 |
|---|---|
| 진행 주문 | 5~10초 polling |
| 오늘 매출 | 30~60초 |
| 인기 메뉴 | 5분 |
| 품절 | 변경 즉시 또는 30초 |

MVP는 페이지 진입 시 fetch + 30초 polling을 기본으로 하고, 진행 주문만 별도 5~10초 polling 가능하다.

#### 5. API 전략

##### 권장: Aggregate API

```http
GET /api/admin/dashboard
```

장점:
- 데이터 시점이 맞는다.
- 프론트 호출 수가 줄어든다.
- 화면 구현이 단순하다.

#### 6. 응답 초안

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

#### 7. 필수 상태

- default
- loading
- empty
- error
- refreshing
- partialError

일부 widget만 실패하면 해당 카드만 Error 처리하고 전체 Dashboard는 유지한다.

#### 8. React Mapping

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

#### 9. 디자인 규칙

- 모든 KPI를 초록색으로 만들지 않는다.
- 진행 중 주문과 경고 상태만 기능색을 적극 사용한다.
- 장식보다 숫자와 상태를 먼저 보여준다.
- Navbar Home을 활성화한다.

#### 10. 구현 체크리스트

- [ ] SCR-022 registry
- [ ] route `/`
- [ ] 로그인 성공 후 Dashboard
- [ ] aggregate DTO
- [ ] KPI 계산 정의
- [ ] polling
- [ ] partial error
- [ ] last updated
- [ ] 0건 상태

---

## 원문: `DASHBOARD_DECISIONS_AND_QA.md`

### Dashboard Decisions and QA

#### 왜 별도 Dashboard인가

실시간 주문 처리와 매장 전체 운영 판단은 목적이 다르다. 주문 보드를 홈으로 사용하면 매출·품절·인기 메뉴를 즉시 파악할 수 없고 Navbar의 Home과 주문관리 역할도 겹친다.

#### 왜 KPI는 4개인가

핵심 지표가 많아질수록 판단 속도가 느려진다. Dashboard MVP에서는 순매출, 주문 수, 평균 객단가, 진행 중 주문을 우선한다.

매출 화면에서 사용하는 `고객 수`는 고유 방문자 수가 아니라 `결제 승인 건수`로 정의한다. 따라서 회원 식별 정보가 없어도 구현할 수 있다. 다만 Dashboard에서는 주문 수와 고객 수가 같은 기준이 되므로 두 지표를 동시에 배치해 중복시키지 않는다.

#### 왜 Partial Error가 필요한가

Dashboard는 여러 도메인의 데이터를 조합한다. 인기 메뉴 한 건 실패 때문에 전체 화면을 막으면 운영에 불리하다.

#### Edge Cases

##### 주문 0건
- 매출 0원
- 주문 수 0건
- 객단가 `-`
- 인기 메뉴 Empty

##### 품절 0건
- `현재 품절 항목이 없습니다.`

##### Polling 중 이전 요청 미완료
- 새 요청 중복 금지

#### QA

- [ ] KPI 정의 일치
- [ ] active order count 일치
- [ ] popular menu 수량 일치
- [ ] sold-out count 일치
- [ ] generatedAt 표시
- [ ] Home active
- [ ] partial error
- [ ] 0 value
- [ ] unsupported metric 없음
