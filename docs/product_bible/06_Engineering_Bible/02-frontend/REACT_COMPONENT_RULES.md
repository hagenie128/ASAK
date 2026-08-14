# React Component Rules

> Status: Current

## 1. Component Naming

```text
PascalCase.jsx
```

좋은 예:

```text
MenuCard.jsx
CartItemCard.jsx
SalesMetricCard.jsx
IngredientSelectModal.jsx
```

나쁜 예:

```text
menu-card.jsx
menu_card.jsx
Admin/Nav-Item.jsx
```

---

## 2. Props Naming

```js
camelCase
```

```jsx
<MenuCard
  menuName="멕시칸 랩"
  isSoldOut={false}
  onSelect={handleSelectMenu}
/>
```

Event prop:

```text
onSelect
onClose
onConfirm
onChange
onRetry
```

Handler:

```text
handleSelect
handleClose
handleConfirm
handleRetry
```

---

## 3. Boolean Props

긍정형 권장:

```text
isLoading
isDisabled
isSelected
showBackButton
canRemove
```

피한다:

```text
notActive
noHeader
isNotVisible
```

---

## 4. Controlled vs Uncontrolled

ASAK Form/Modal은 controlled component를 우선한다.

```jsx
<OptionGroup
  selectedOptionIds={selectedOptionIds}
  onChange={handleOptionChange}
/>
```

이유:

- Cart 수정 draft 제어
- validation
- Figma state 재현
- 테스트 용이

---

## 5. Rendering Rules

배열 key:

```jsx
key={item.id}
```

피한다:

```jsx
key={index}
```

Cart는 `cartItemId`.

---

## 6. Conditional Rendering

복잡한 삼항 연산자 중첩 금지.

나쁜 예:

```jsx
{isLoading ? <Loading /> : error ? <Error /> : data ? <View /> : null}
```

권장:

```jsx
if (isLoading) return <LoadingState />;
if (error) return <ErrorState />;
return <View />;
```

---

## 7. Business Logic

Component 안에 넣지 않는다:

- 가격 권한 계산
- 품절 전파
- 상태 전이 검증
- API error mapping

Feature/Hook/Service로 분리한다.

---

## 8. Figma Mapping

Figma와 React 이름을 무조건 동일하게 만들 필요는 없다.

하지만 mapping 문서에 다음을 기록한다.

```text
Figma: Admin/StatusBadge
React: OrderStatusBadge.jsx
```

같은 역할의 중복 컴포넌트를 새로 만들지 않는다.

---

## 9. Accessibility

- Button은 실제 `<button>`
- form label 연결
- focus outline 유지
- disabled 이유 표시
- icon-only button에 aria-label
