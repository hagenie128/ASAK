# Timeout and Accessibility Implementation

## useIdleTimer

감지:

- pointer
- touch
- keyboard

정책:

- 20초 warning
- 10초 countdown
- processing 제외

## resetSession

reset reason을 전달한다.

## Accessibility

Store:

```js
{
  fontScale,
  contrastMode
}
```

localStorage에 유지.

## CSS

root class 또는 data attribute:

```text
data-font-scale
data-contrast-mode
```
