# State Management Rules

> Status: Current  
> Library: Zustand

## 1. Zustand 사용 기준

여러 화면에서 공유되거나 session lifecycle에 포함되는 상태만 store에 둔다.

적합:

- orderSession
- cartItems
- accessibility
- TTS settings

부적합:

- 한 Modal open
- 한 Input value
- 단일 페이지 filter draft

---

## 2. Store Structure

```js
export const useOrderSessionStore = create((set, get) => ({
  orderType: null,
  cartItems: [],
  orderId: null,
  orderNo: null,
  orderStatus: null,
  paymentStatus: null,

  setOrderType: (orderType) => set({ orderType }),
  addItem: (item) => {},
  resetSession: (reason) => {},
}));
```

---

## 3. Action Naming

동사형 camelCase:

```text
addItem
removeItem
updateQuantity
updateItemOptions
setOrderType
resetSession
```

---

## 4. Derived State

가능하면 저장하지 않고 계산한다.

예:

```js
const totalAmount = cartItems.reduce(...);
```

다만 성능 또는 계약상 store에 저장하면 action마다 일관되게 갱신한다.

---

## 5. Persistence

localStorage 대상:

- Accessibility
- TTS settings

선택 대상:

- Cart

저장하지 않음:

- 결제 처리 중 임시 state
- error object
- modal open

---

## 6. Reset Policy

reset은 이유를 받는다.

```js
resetSession("ORDER_COMPLETED");
```

공식 reason:

```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
TIMEOUT_EXPIRED
USER_RESET
SESSION_EXPIRED
```

---

## 7. Store에서 금지

- API 호출 남발
- DOM 접근
- React component 반환
- 서버 가격 최종 결정
- Router 강결합
