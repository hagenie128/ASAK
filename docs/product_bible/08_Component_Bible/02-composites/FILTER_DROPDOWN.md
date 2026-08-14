# FilterDropdown

## Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/FilterDropdown`
- Open variant: id 110:1052

## States

```text
default
active
open
disabled
```

## Props

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

## Rules

- panel은 absolute overlay
- 선택 항목 강조
- 바깥 클릭/ESC 닫기
- 주문상태·결제상태·주문유형에 재사용
