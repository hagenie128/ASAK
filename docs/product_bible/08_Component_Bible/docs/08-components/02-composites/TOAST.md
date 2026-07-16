# Toast

## Tier / Owner

- Tier: Composite
- Owner: Shared/Admin
- Figma: `Admin/Toast` id 93:475

## Variants

```text
success
deleted
loading
failed
```

## Props

```js
{
  status,
  message,
  duration,
  actionLabel,
  onAction,
  onClose
}
```

## Rules

- 성공 2~3초
- 실패는 사용자가 읽을 시간 제공
- 중요한 destructive confirm 대체 금지
- 서버 raw message 노출 금지
