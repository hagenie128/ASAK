# OrderCard

## Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: `Admin/OrderCard`

## Used By

- SCR-009 Live Order Board
- SCR-022 Dashboard summary

## Props

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

## Rules

- 상태별 next action 1개만 강조
- elapsed warning은 색상+텍스트 병행
- 완료 성공 후 TTS
- Polling 조회만으로 TTS 실행 금지
