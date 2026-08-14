# Menu Detail Flow and Validation

> Status: Current

## 1. 화면 목적

SCR-004 Menu Detail의 목적은 고객이 메뉴 구성을 실수 없이 완성하게 하는 것이다.

---

## 2. 권장 선택 순서

1. 베이스
2. 필수 옵션
3. 추가 옵션
4. 제외 재료
5. 드레싱
6. 수량

실제 메뉴 구조에 따라 순서는 바뀔 수 있지만, 필수 옵션은 선택 옵션보다 먼저 둔다.

---

## 3. Required States

```text
default
validationError
soldOut
optionSoldOut
maximumExceeded
minimumNotMet
priceUpdated
```

---

## 4. Validation Rules

### Required Group

```text
selectedCount >= minimumSelection
```

### Maximum

```text
selectedCount <= maximumSelection
```

### Single Select

```text
maximumSelection = 1
```

### Sold-out Option

- 선택 불가
- disabled
- 품절 badge
- 기존 선택이 품절되면 validation error

---

## 5. Price Calculation

```text
basePrice
+ sum(selected option additionalAmount)
= unitAmount
```

수량 반영:

```text
unitAmount × quantity = lineAmount
```

가격 변화는 선택 직후 반영한다.

---

## 6. Back Navigation

뒤로 가도 선택을 유지한다.

권장 방식:

- local draft state
- route state
- store draft

단, Cart에 담기기 전 draft와 Cart item을 혼동하지 않는다.

---

## 7. Add to Cart Sequence

```text
select options
→ validate
→ calculate
→ create cartItemId
→ addItem
→ success feedback
```

---

## 8. Validation Copy

### 필수 미선택

`필수 옵션을 선택해주세요.`

### 최대 초과

`최대 {n}개까지 선택할 수 있어요.`

### 품절 옵션

`선택한 옵션이 품절되었습니다. 다른 옵션을 선택해주세요.`

---

## 9. QA

- [ ] 필수 옵션 표시
- [ ] min/max 표시
- [ ] sold-out disabled
- [ ] 가격 즉시 반영
- [ ] allergen 변경 반영
- [ ] 뒤로가기 선택 유지
- [ ] add CTA disabled 기준
