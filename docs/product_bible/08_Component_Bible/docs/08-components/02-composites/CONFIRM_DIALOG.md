# ConfirmDialog

## Tier / Owner

- Tier: Composite
- Owner: Shared
- Figma: `Shared/ConfirmDialog`

## Use Cases

- Cart item delete
- Menu delete
- Sold-out save
- 전체 결제수단 비활성화
- 변경사항 폐기

## Props

```js
{
  open,
  title,
  description,
  confirmLabel,
  cancelLabel,
  destructive,
  loading,
  onConfirm,
  onCancel
}
```

## Rules

- Shared/Modal 중복 정리 전 삭제 금지
- destructive action만 danger 강조
- loading 중 닫기 정책 명확히
