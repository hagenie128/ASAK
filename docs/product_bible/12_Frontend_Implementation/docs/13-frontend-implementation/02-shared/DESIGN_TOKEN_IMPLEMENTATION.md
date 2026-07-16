# Design Token Implementation

## CSS Variables

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

## 원칙

- 현재 스타일을 한 번에 전환하지 않는다.
- 반복되는 값부터 token으로 교체한다.
- 기존 Figma 색·간격을 유지한다.
- 모든 화면을 동시에 리팩터링하지 않는다.
