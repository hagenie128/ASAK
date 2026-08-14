# Cart Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `CART_API_AND_DATA_CONTRACT.md`
- `CART_ARCHITECTURE.md`
- `CART_EDGE_CASE_AND_QA.md`
- `CART_STATE_AND_EVENT_FLOW.md`

---

## 원문: `CART_API_AND_DATA_CONTRACT.md`

### Cart API and Data Contract

> Status: Draft

#### 1. Local Cart Model

```json
{
  "cartItemId": "local-1",
  "menuId": 1,
  "menuName": "멕시칸 랩",
  "imageUrl": "...",
  "quantity": 2,
  "baseAmount": 7200,
  "optionAmount": 1200,
  "unitAmount": 8400,
  "lineAmount": 16800,
  "selectedOptions": [
    {
      "optionGroupId": 10,
      "optionItemId": 101,
      "optionItemName": "아보카도",
      "additionalAmount": 1200
    }
  ],
  "excludedIngredients": [
    {
      "ingredientId": 33,
      "ingredientName": "양파"
    }
  ]
}
```

---

#### 2. Validate Cart

확장 API:

```http
POST /api/kiosk/cart/validate
```

##### Request

```json
{
  "items": [
    {
      "menuId": 1,
      "quantity": 2,
      "selectedOptionItemIds": [101],
      "excludedIngredientIds": [33]
    }
  ]
}
```

##### Response

```json
{
  "success": true,
  "data": {
    "isValid": true,
    "totalAmount": 16800,
    "itemResults": []
  }
}
```

---

#### 3. Validation Failure Example

```json
{
  "success": true,
  "data": {
    "isValid": false,
    "totalAmount": 15600,
    "itemResults": [
      {
        "menuId": 1,
        "reason": "OPTION_ITEM_SOLD_OUT",
        "affectedOptionItemIds": [101]
      }
    ]
  }
}
```

---

#### 4. Contract Rules

- Cart는 local state로 먼저 운영 가능
- 서버 validation은 Order 생성 직전 필수
- `lineAmount`와 `totalAmount`는 UI 표시용
- 서버 계산값이 최종

---

## 원문: `CART_ARCHITECTURE.md`

### Cart Architecture

> Status: Current

#### 1. 목적

Cart는 메뉴 상세에서 선택한 구성을 결제 전까지 안전하게 보관하고 수정하는 클라이언트 주문 준비 영역이다.

Cart의 핵심은 저장이 아니라 **검토와 복구**다.

---

#### 2. Cart Item Identity

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

##### 왜 index를 피하는가

- 삭제 후 index가 바뀐다.
- 정렬 시 대상이 달라진다.
- 동일 메뉴의 다른 옵션 조합을 구분하지 못한다.

---

#### 3. Cart State

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

#### 4. Figma Mapping

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

#### 5. Option Summary

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

#### 6. Quantity Rules

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

#### 7. Delete Policy

삭제는 irreversible action이므로 ConfirmDialog 사용.

```text
선택한 메뉴를 삭제할까요?
취소 / 삭제
```

마지막 항목 삭제 후 Empty state.

---

#### 8. Edit Options

옵션 수정은 기존 Menu Detail의 OptionGroup을 재사용한다.

권장 방식:

- Cart 위 Modal/Sheet
- 기존 선택값 preload
- 저장 시 해당 cartItemId만 갱신
- 취소 시 변경 폐기

---

#### 9. Persistence

MVP 권장:

- Zustand
- session/local persistence는 선택

Timeout 또는 주문 완료 시 반드시 reset.

결제 실패 시 유지.

---

#### 10. Implementation Checklist

- [ ] cartItemId
- [ ] option summary
- [ ] edit options
- [ ] delete confirm
- [ ] quantity min
- [ ] total recalculation
- [ ] empty state
- [ ] sold-out validation
- [ ] reset reason

---

## 원문: `CART_EDGE_CASE_AND_QA.md`

### Cart Edge Cases and QA

#### Edge Cases

##### 동일 메뉴, 다른 옵션

두 개의 Cart Item으로 유지.

##### 동일 메뉴, 동일 옵션

정책 선택:

- quantity 증가
- 별도 item 유지

MVP 권장: quantity 증가.

##### 옵션 수정 중 품절

저장 시 validation.
품절 option은 선택 불가.

##### 마지막 항목 삭제

Empty state 이동.

##### 결제 실패 후 복귀

Cart 유지.

##### Timeout

정책에 따라 warning 후 reset.

##### 가격 변경

Order 생성 시 최신 금액 안내.

---

#### Figma QA

- [ ] 옵션 수정 visible
- [ ] 삭제 visible
- [ ] 제외/추가 분리
- [ ] 중복 아보카도 제거
- [ ] `__spec` 화면 밖
- [ ] 16,800원 유지
- [ ] Empty state
- [ ] Delete Confirm
- [ ] quantity min

#### React QA

- [ ] cartItemId key
- [ ] no index mutation
- [ ] immutable update
- [ ] total derived correctly
- [ ] modal draft separated
- [ ] reset only on valid reason

---

## 원문: `CART_STATE_AND_EVENT_FLOW.md`

### Cart State and Event Flow

#### 1. State Machine

```text
EMPTY
  ↓ add item
HAS_ITEM
  ↓ validation
VALID
  ↓ order create
SUBMITTING
  ↓ success
ORDER_CREATED
```

Failure:

```text
SUBMITTING
  ↓ failed
VALID + error
```

---

#### 2. Add Item

```text
Menu Detail
→ validate required options
→ calculate unit amount
→ create cartItemId
→ addItem
→ recalculate total
→ Cart or continue shopping
```

---

#### 3. Update Quantity

```text
click plus/minus
→ find cartItemId
→ update quantity
→ recalculate line total
→ recalculate cart total
```

---

#### 4. Edit Options

```text
click 옵션 수정
→ open modal
→ clone current selection
→ edit local draft
→ validate
→ save
→ updateItemOptions(cartItemId)
→ recalculate
```

Modal draft는 저장 전 원본 Cart Item을 직접 수정하지 않는다.

---

#### 5. Delete

```text
click 삭제
→ confirm open
→ confirm
→ removeItem(cartItemId)
→ if zero items: EMPTY
```

---

#### 6. Validation Before Order

```text
item exists
quantity valid
menu active
menu not sold-out
required option selected
option not sold-out
price current
```

Client validation은 UX용이며 서버 validation을 대체하지 않는다.

---

#### 7. Reset Reasons

```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
USER_RESET
SESSION_EXPIRED
```

결제 실패는 reset reason이 아니다.
