# Kiosk Frontend Implementation

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `CART_IMPLEMENTATION.md`
- `HOME_MENU_IMPLEMENTATION.md`
- `KIOSK_ROUTE_IMPLEMENTATION.md`
- `PAYMENT_COMPLETE_IMPLEMENTATION.md`
- `TIMEOUT_ACCESSIBILITY_IMPLEMENTATION.md`

---

## 원문: `CART_IMPLEMENTATION.md`

### Cart Implementation

#### Store Model

```js
{
  cartItems: [],
  orderType: null,
  orderId: null,
  orderNo: null
}
```

#### 필수 Actions

```text
addItem
removeItem
updateQuantity
updateItemOptions
clearCart
resetSession
```

#### 기존 코드 보호

기존 action 이름이 다르면 무조건 교체하지 않는다.

- 기존 이름 유지 가능성 검토
- adapter 또는 alias 가능
- 팀원 코드 import 영향 확인

#### CartItem

key:

```text
cartItemId
```

#### Option Edit

기존 Menu Detail UI 또는 Option component 재사용.

#### Delete

ConfirmDialog.

---

## 원문: `HOME_MENU_IMPLEMENTATION.md`

### Home and Menu Implementation

#### Home

기존 디자인·컴포넌트 유지.

추가 확인:

- EAT_IN / TAKE_OUT
- 선택 state
- 접근성 진입
- Menu route
- orderType store

#### Menu List

기존 MenuCard 재사용.

연결:

```text
GET menuList
→ loading
→ empty
→ error
→ default
```

#### Menu Detail

- API data
- option draft
- validation
- price derived state
- Cart add

기존 UI 구조를 유지하고 로직만 연결한다.

---

## 원문: `KIOSK_ROUTE_IMPLEMENTATION.md`

### Kiosk Route Implementation

#### Routes

```text
/                  Home
/menu              Menu List
/menu/:menuId      Menu Detail
/cart              Cart
/payment           Payment
/complete          Complete
/accessibility     Accessibility
```

#### Route Guard

##### Payment

- Cart 없음 → Cart 또는 Home
- orderId 없음 → Cart

##### Complete

- approved result 없음 → Home

#### Navigation

승인 후 Complete는 replace navigation 권장.

---

## 원문: `PAYMENT_COMPLETE_IMPLEMENTATION.md`

### Payment and Complete Implementation

#### Payment

Flow:

```text
order create
→ payment method
→ processing
→ approved / failed
```

#### 중복 방지

```js
if (isSubmitting) return;
```

Button disabled + API idempotency.

#### Processing

- 뒤로가기 차단
- Timeout 차단
- Modal 닫기 금지

#### Complete

표시:

- orderNo
- waitingOrderCount
- totalAmount
- auto return

#### 정합성

```text
16,800원
```

Cart/Payment/Error/Timeout/Complete 모두 동일.

---

## 원문: `TIMEOUT_ACCESSIBILITY_IMPLEMENTATION.md`

### Timeout and Accessibility Implementation

#### useIdleTimer

감지:

- pointer
- touch
- keyboard

정책:

- 20초 warning
- 10초 countdown
- processing 제외

#### resetSession

reset reason을 전달한다.

#### Accessibility

Store:

```js
{
  fontScale,
  contrastMode
}
```

localStorage에 유지.

#### CSS

root class 또는 data attribute:

```text
data-font-scale
data-contrast-mode
```
