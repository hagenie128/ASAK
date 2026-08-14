# Section Components

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `CATEGORY_TABS.md`
- `DASHBOARD_SUMMARY.md`
- `ORDER_SUMMARY.md`
- `ORDER_TABLE.md`

---

## 원문: `CATEGORY_TABS.md`

### CategoryTabs

#### Tier / Owner

- Tier: Section
- Owner: Kiosk

#### Props

```js
{
  categories,
  selectedCategoryCode,
  onChange
}
```

#### Rules

- active 명확
- overflow/scroll 정책
- category code와 displayName 분리

---

## 원문: `DASHBOARD_SUMMARY.md`

### DashboardSummary

#### Tier / Owner

- Tier: Section
- Owner: Admin

#### Includes

- SalesMetricCard × 4
- ActiveOrderSummary
- PopularMenuList
- SoldOutSummary

#### Rules

- widget partialError 허용
- KPI 4개 우선
- 고객 수와 주문 수 중복 배치 금지

---

## 원문: `ORDER_SUMMARY.md`

### OrderSummary

#### Tier / Owner

- Tier: Section
- Owner: Kiosk

#### Includes

- totalQuantity
- subtotal
- optionAmount
- totalAmount

#### Rules

- 금액 계산은 derived state
- 서버 승인 금액과 비교
- 16,800원 정합성 유지

---

## 원문: `ORDER_TABLE.md`

### OrderTable

#### Tier / Owner

- Tier: Section
- Owner: Admin

#### Includes

- Header
- Row
- Empty
- Loading
- Pagination
- Selection

#### Rules

- SCR-010 전용
- Live Order Board 카드와 역할 분리
- row click과 action button 충돌 방지
