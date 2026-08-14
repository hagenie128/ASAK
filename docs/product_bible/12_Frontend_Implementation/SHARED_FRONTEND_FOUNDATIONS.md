# Shared Frontend Foundations

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `DESIGN_TOKEN_IMPLEMENTATION.md`
- `SHARED_STATE_COMPONENTS.md`

---

## 원문: `DESIGN_TOKEN_IMPLEMENTATION.md`

### Design Token Implementation

#### CSS Variables

```css
:root {
  --color-brand-primary: #...;
  --color-text-primary: #...;
  --color-text-secondary: #...;
  --color-surface-default: #...;
  --color-border-default: #...;

  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;

  --radius-sm: ...;
  --radius-md: ...;
  --radius-lg: ...;
}
```

#### 원칙

- 현재 스타일을 한 번에 전환하지 않는다.
- 반복되는 값부터 token으로 교체한다.
- 기존 Figma 색·간격을 유지한다.
- 모든 화면을 동시에 리팩터링하지 않는다.

---

## 원문: `SHARED_STATE_COMPONENTS.md`

### Shared State Components

#### Components

```text
LoadingState
EmptyState
ErrorState
Toast
ConfirmDialog
Spinner
```

#### 구현 순서

1. 기존 컴포넌트 검색
2. Props 확인
3. Kiosk/Admin 공통 사용 가능성 확인
4. 중복 최소화

#### ErrorState Props

```js
{
  title,
  description,
  actionLabel,
  onRetry
}
```

#### Toast

서버 raw message를 직접 표시하지 않는다.
