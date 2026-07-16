# BottomCTA

## Tier / Owner

- Tier: Composite
- Owner: Kiosk
- Figma: `Kiosk/BottomCTA`
- React: 기존 `BottomCTA.jsx` 우선

## Used By

- SCR-004 Menu Detail
- SCR-005 Cart
- SCR-007 Payment

## Purpose

현재 화면의 최종 행동과 금액을 하단 고정 영역에서 제공한다.

## Props

```js
{
  label,
  amount,
  disabled,
  loading,
  helperText,
  onClick
}
```

## States

```text
default
disabled
loading
error
```

## Layout

- 화면 하단 고정
- content와 구분선
- 주요 CTA 한 개
- 금액은 천 단위 콤마 + `원`

## Rules

- 화면마다 별도 FooterButton을 만들지 않는다.
- payment processing 중 disabled
- amount null일 때 임의 0원 노출 금지
- safe area와 frame height 유지

## Dependency

```text
BottomCTA
→ Button
→ Spinner
```

## QA

- [ ] 16,800원 정합성
- [ ] loading 중 중복 클릭 차단
- [ ] disabled contrast
- [ ] touch target
