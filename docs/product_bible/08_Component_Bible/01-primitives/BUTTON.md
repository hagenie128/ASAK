# Button

## Tier / Owner

- Tier: Primitive
- Owner: Shared

## Purpose

사용자의 명시적 행동을 실행한다.

## Variants

```text
primary
secondary
danger
ghost
```

## States

```text
default
hover
pressed
focus
disabled
loading
```

## Props

```js
{
  type,
  variant,
  size,
  disabled,
  loading,
  icon,
  children,
  onClick,
  ariaLabel
}
```

## Rules

- loading 중 중복 클릭 금지
- disabled 이유가 필요한 경우 주변 문구 제공
- icon-only는 aria-label 필수
- Kiosk 최소 터치 영역 80×80px

## Do Not

- `<div onClick>`로 구현하지 않는다.
- 화면마다 새로운 button style을 만들지 않는다.
