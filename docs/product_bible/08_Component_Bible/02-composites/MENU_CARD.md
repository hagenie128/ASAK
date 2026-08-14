# MenuCard

## Tier / Owner

- Tier: Composite
- Owner: Kiosk
- Figma: menu-card / Kiosk Menu Card
- React: 기존 `MenuCard.jsx` 우선

## Props

```js
{
  menuId,
  menuName,
  description,
  imageUrl,
  price,
  calories,
  tags,
  isSoldOut,
  onSelect
}
```

## States

```text
default
hover
selected
soldOut
imageMissing
```

## Rules

- 품절은 opacity만 사용하지 않는다.
- 이미지 fallback 제공
- BEST/NEW/VEGAN tag 지원
- 카드 전체를 button semantics로 구현 가능

## Do Not

- FoodCard/ProductCard 신규 생성 금지
