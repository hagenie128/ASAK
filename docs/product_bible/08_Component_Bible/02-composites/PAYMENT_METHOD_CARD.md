# PaymentMethodCard

## Tier / Owner

- Tier: Composite
- Owner: Kiosk

## Props

```js
{
  code,
  displayName,
  description,
  icon,
  status,
  selected,
  onSelect
}
```

## Status

```text
ENABLED
DISABLED
MAINTENANCE
```

## Rules

- disabled와 maintenance를 구분
- selected 상태 명확히
- Processing 중 선택 변경 금지
