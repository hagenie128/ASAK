# Order Entity Implementation

## Entity

```text
Order
OrderItem
OrderItemOption
```

## Order

필드:

```text
id
orderNo
orderType
orderStatus
paymentStatus
totalAmount
createdAt
updatedAt
```

## OrderItem Snapshot

반드시 당시 값을 보관한다.

```text
menuId
menuName
unitAmount
quantity
lineAmount
```

메뉴명이 바뀌어도 과거 주문이 바뀌지 않아야 한다.

## OrderItemOption Snapshot

```text
optionItemId
optionItemName
additionalAmount
```

## 상태

```text
RECEIVED
PREPARING
COMPLETED
```
