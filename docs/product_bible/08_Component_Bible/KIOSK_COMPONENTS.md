# Kiosk Components

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `BOTTOM_CTA.md`
- `CART_ITEM_CARD.md`
- `INGREDIENT_SELECT_MODAL.md`
- `MENU_CARD.md`
- `PAYMENT_METHOD_CARD.md`

---

## 원문: `BOTTOM_CTA.md`

### BottomCTA

#### Tier / Owner

- Tier: Composite
- Owner: Kiosk
- Figma: `Kiosk/BottomCTA`
- React: 기존 `BottomCTA.jsx` 우선

#### Used By

- SCR-004 Menu Detail
- SCR-005 Cart
- SCR-007 Payment

#### Purpose

현재 화면의 최종 행동과 금액을 하단 고정 영역에서 제공한다.

#### Props

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

#### States

```text
default
disabled
loading
error
```

#### Layout

- 화면 하단 고정
- content와 구분선
- 주요 CTA 한 개
- 금액은 천 단위 콤마 + `원`

#### Rules

- 화면마다 별도 FooterButton을 만들지 않는다.
- payment processing 중 disabled
- amount null일 때 임의 0원 노출 금지
- safe area와 frame height 유지

#### Dependency

```text
BottomCTA
→ Button
→ Spinner
```

#### QA

- [ ] 16,800원 정합성
- [ ] loading 중 중복 클릭 차단
- [ ] disabled contrast
- [ ] touch target

---

## 원문: `CART_ITEM_CARD.md`

### CartItemCard

#### Tier / Owner

- Tier: Composite
- Owner: Kiosk

#### Props

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

#### Rules

- key는 cartItemId
- 옵션 수정과 삭제 분리
- quantity 1에서 minus disabled
- 삭제는 ConfirmDialog
- 옵션 요약은 3줄 초과 시 축약

#### Do Not

- index key
- minus를 삭제 동작으로 사용

---

## 원문: `INGREDIENT_SELECT_MODAL.md`

### IngredientSelectModal

#### Tier / Owner

- Tier: Composite
- Owner: Admin
- Figma: id 98:5485

#### Props

```js
{
  open,
  ingredients,
  selectedIngredientIds,
  keyword,
  onSearch,
  onToggle,
  onConfirm,
  onCancel
}
```

#### Rules

- 기존 선택 preload
- draft와 original 분리
- label overlap 금지
- 검색창 문구 `재료명 검색`
- 버튼 `취소 / 추가`

---

## 원문: `MENU_CARD.md`

### MenuCard

#### Tier / Owner

- Tier: Composite
- Owner: Kiosk
- Figma: menu-card / Kiosk Menu Card
- React: 기존 `MenuCard.jsx` 우선

#### Props

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

#### States

```text
default
hover
selected
soldOut
imageMissing
```

#### Rules

- 품절은 opacity만 사용하지 않는다.
- 이미지 fallback 제공
- BEST/NEW/VEGAN tag 지원
- 카드 전체를 button semantics로 구현 가능

#### Do Not

- FoodCard/ProductCard 신규 생성 금지

---

## 원문: `PAYMENT_METHOD_CARD.md`

### PaymentMethodCard

#### Tier / Owner

- Tier: Composite
- Owner: Kiosk

#### Props

```js
{
  code,
  displayName,
  description,
  icon,
  status,
  selected,
  onSelect
}
```

#### Status

```text
ENABLED
DISABLED
MAINTENANCE
```

#### Rules

- disabled와 maintenance를 구분
- selected 상태 명확히
- Processing 중 선택 변경 금지
