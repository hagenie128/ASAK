# CartItemCard

## Tier / Owner

- Tier: Composite
- Owner: Kiosk

## Props

```js
{
  cartItemId,
  menuName,
  imageUrl,
  optionSummary,
  quantity,
  lineAmount,
  onEditOptions,
  onIncrease,
  onDecrease,
  onDelete
}
```

## Rules

- key는 cartItemId
- 옵션 수정과 삭제 분리
- quantity 1에서 minus disabled
- 삭제는 ConfirmDialog
- 옵션 요약은 3줄 초과 시 축약

## Do Not

- index key
- minus를 삭제 동작으로 사용
