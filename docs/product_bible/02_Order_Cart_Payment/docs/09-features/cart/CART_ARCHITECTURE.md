# Cart Architecture

> Status: Current

## 1. 목적

Cart는 메뉴 상세에서 선택한 구성을 결제 전까지 안전하게 보관하고 수정하는 클라이언트 주문 준비 영역이다.

Cart의 핵심은 저장이 아니라 **검토와 복구**다.

---

## 2. Cart Item Identity

같은 menuId라도 옵션 조합이 다르면 다른 Cart Item이다.

따라서 식별자는 index나 menuId가 아니라 `cartItemId`를 사용한다.

```js
{
  cartItemId: "local-uuid",
  menuId: 1,
  menuName: "멕시칸 랩",
  quantity: 2,
  selectedOptions: [],
  excludedIngredients: []
}
```

### 왜 index를 피하는가

- 삭제 후 index가 바뀐다.
- 정렬 시 대상이 달라진다.
- 동일 메뉴의 다른 옵션 조합을 구분하지 못한다.

---

## 3. Cart State

```js
{
  cartItems: [],
  totalQuantity: 0,
  totalAmount: 0,
  validationErrors: []
}
```

필요 actions:

```text
addItem
removeItem
updateQuantity
updateItemOptions
clearCart
recalculateTotals
validateCart
```

---

## 4. Figma Mapping

SCR-005 Default:

- 상품 이미지
- 메뉴명
- 옵션 요약
- 옵션 수정
- 삭제
- 수량
- line total
- order summary
- payment CTA

SCR-005 Empty:

- Empty State
- 메뉴 보러 가기

추가 상태:

- deleteConfirm
- quantityMin
- quantityMax
- soldOutWarning
- validationError
- orderCreating

---

## 5. Option Summary

전체 옵션을 카드 안에 길게 나열하지 않는다.

권장:

```text
베이스: 현미밥
드레싱: 시저
추가: 아보카도 외 2개
제외: 양파
```

3줄을 넘으면 `외 n개`로 요약한다.

---

## 6. Quantity Rules

```text
minimum = 1
maximum = product/order policy
```

MVP에서 maximum이 확정되지 않았다면:

- UI는 1 이상만 보장
- 과도한 수량은 서버 정책 확정 후 제한

quantity가 1일 때 minus 동작:

권장:

- minus disabled
- 삭제는 별도 action

수량 감소와 삭제를 같은 동작으로 만들지 않는다.

---

## 7. Delete Policy

삭제는 irreversible action이므로 ConfirmDialog 사용.

```text
선택한 메뉴를 삭제할까요?
취소 / 삭제
```

마지막 항목 삭제 후 Empty state.

---

## 8. Edit Options

옵션 수정은 기존 Menu Detail의 OptionGroup을 재사용한다.

권장 방식:

- Cart 위 Modal/Sheet
- 기존 선택값 preload
- 저장 시 해당 cartItemId만 갱신
- 취소 시 변경 폐기

---

## 9. Persistence

MVP 권장:

- Zustand
- session/local persistence는 선택

Timeout 또는 주문 완료 시 반드시 reset.

결제 실패 시 유지.

---

## 10. Implementation Checklist

- [ ] cartItemId
- [ ] option summary
- [ ] edit options
- [ ] delete confirm
- [ ] quantity min
- [ ] total recalculation
- [ ] empty state
- [ ] sold-out validation
- [ ] reset reason
