# ASAK Naming Bible

> Status: Current

## 1. Frontend Variable / Function / State / Props

```text
camelCase
```

좋은 예:

```js
selectedCategory
totalAmount
waitingOrderCount
handlePayment
fetchOrderList
```

---

## 2. Backend Field / Method / Package Variable

```text
camelCase
```

```java
orderService
totalAmount
findOrderById()
updateOrderStatus()
```

---

## 3. Class / React Component

```text
PascalCase
```

```text
OrderController
OrderService
OrderDetailResponse
MenuCard
CartItemCard
```

---

## 4. Database

```text
snake_case
```

```text
order_item
payment_method
created_at
order_status
```

---

## 5. URL

```text
camelCase
```

```text
/admin/paymentMethods
/kiosk/menuDetail
```

---

## 6. Constants

사용자 결정:

```text
UpperCamelCase
```

```js
export const OrderStatus = {
  Received: "RECEIVED",
  Preparing: "PREPARING",
  Completed: "COMPLETED",
};
```

상수 객체명과 key는 UpperCamelCase.

실제 code value는 UPPER_SNAKE_CASE.

---

## 7. Figma Component

```text
Domain/PascalCase
```

```text
Admin/StatusBadge
Kiosk/BottomCTA
Shared/ConfirmDialog
```

---

## 8. Figma Layer / Variant Property

```text
camelCase
```

```text
mainContent
totalAmount
state=loading
status=success
```

---

## 9. Git Branch

```text
feature/
fix/
docs/
refactor/
hotfix/
```

예:

```text
feature/admin-dashboard
fix/payment-amount
docs/tts-architecture
```
