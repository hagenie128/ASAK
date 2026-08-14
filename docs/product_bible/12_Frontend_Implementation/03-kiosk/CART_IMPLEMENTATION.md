# Cart Implementation

## Store Model

```js
{
  cartItems: [],
  orderType: null,
  orderId: null,
  orderNo: null
}
```

## 필수 Actions

```text
addItem
removeItem
updateQuantity
updateItemOptions
clearCart
resetSession
```

## 기존 코드 보호

기존 action 이름이 다르면 무조건 교체하지 않는다.

- 기존 이름 유지 가능성 검토
- adapter 또는 alias 가능
- 팀원 코드 import 영향 확인

## CartItem

key:

```text
cartItemId
```

## Option Edit

기존 Menu Detail UI 또는 Option component 재사용.

## Delete

ConfirmDialog.
