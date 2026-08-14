# Admin Components

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `DATE_PICKERS.md`
- `FILTER_DROPDOWN.md`
- `ORDER_CARD.md`
- `SALES_METRIC_CARD.md`

---

## 원문: `DATE_PICKERS.md`

### DatePicker and DateRangePicker

#### Owner

Admin

#### Figma

- DateRangePicker: 113:491
- DatePicker: 114:491

#### Props

```js
{
  value,
  minDate,
  maxDate,
  presets,
  onChange,
  onApply,
  onCancel
}
```

#### Presets

```text
TODAY
THIS_WEEK
THIS_MONTH
CUSTOM
```

#### Rules

- comparisonLabel과 연동
- 2025년 2월 하드코딩 제거
- Asia/Seoul 기준

---

## 원문: `FILTER_DROPDOWN.md`

### FilterDropdown

#### Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/FilterDropdown`
- Open variant: id 110:1052

#### States

```text
default
active
open
disabled
```

#### Props

```js
{
  label,
  value,
  options,
  open,
  onToggle,
  onChange
}
```

#### Rules

- panel은 absolute overlay
- 선택 항목 강조
- 바깥 클릭/ESC 닫기
- 주문상태·결제상태·주문유형에 재사용

---

## 원문: `ORDER_CARD.md`

### OrderCard

#### Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/OrderCard`

#### Used By

- SCR-009 Live Order Board
- SCR-022 Dashboard summary

#### Props

```js
{
  orderId,
  orderNo,
  orderType,
  status,
  createdAt,
  elapsedMinutes,
  itemSummary,
  onStart,
  onComplete
}
```

#### Rules

- 상태별 next action 1개만 강조
- elapsed warning은 색상+텍스트 병행
- 완료 성공 후 TTS
- Polling 조회만으로 TTS 실행 금지

---

## 원문: `SALES_METRIC_CARD.md`

### SalesMetricCard

#### Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/SalesMetricCard`

#### Props

```js
{
  label,
  value,
  unit,
  comparisonLabel,
  comparisonRate,
  trend,
  loading,
  error
}
```

#### Rules

- 모든 숫자를 초록색으로 만들지 않는다.
- comparisonRate가 null이면 `비교 데이터 없음`
- 고객 수는 결제 승인 건수 기준
- value와 chart/table 합계 일치
