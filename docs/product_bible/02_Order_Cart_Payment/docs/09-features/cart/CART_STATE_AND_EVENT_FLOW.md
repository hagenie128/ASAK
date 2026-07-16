# Cart State and Event Flow

## 1. State Machine

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

## 2. Add Item

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

## 3. Update Quantity

```text
click plus/minus
→ find cartItemId
→ update quantity
→ recalculate line total
→ recalculate cart total
```

---

## 4. Edit Options

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

## 5. Delete

```text
click 삭제
→ confirm open
→ confirm
→ removeItem(cartItemId)
→ if zero items: EMPTY
```

---

## 6. Validation Before Order

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

## 7. Reset Reasons

```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
USER_RESET
SESSION_EXPIRED
```

결제 실패는 reset reason이 아니다.
