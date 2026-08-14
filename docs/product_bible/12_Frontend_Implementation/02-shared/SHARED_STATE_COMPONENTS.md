# Shared State Components

## Components

```text
LoadingState
EmptyState
ErrorState
Toast
ConfirmDialog
Spinner
```

## 구현 순서

1. 기존 컴포넌트 검색
2. Props 확인
3. Kiosk/Admin 공통 사용 가능성 확인
4. 중복 최소화

## ErrorState Props

```js
{
  title,
  description,
  actionLabel,
  onRetry
}
```

## Toast

서버 raw message를 직접 표시하지 않는다.
