# SalesMetricCard

## Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/SalesMetricCard`

## Props

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

## Rules

- 모든 숫자를 초록색으로 만들지 않는다.
- comparisonRate가 null이면 `비교 데이터 없음`
- 고객 수는 결제 승인 건수 기준
- value와 chart/table 합계 일치
