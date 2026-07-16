# Payment and Complete Implementation

## Payment

Flow:

```text
order create
→ payment method
→ processing
→ approved / failed
```

## 중복 방지

```js
if (isSubmitting) return;
```

Button disabled + API idempotency.

## Processing

- 뒤로가기 차단
- Timeout 차단
- Modal 닫기 금지

## Complete

표시:

- orderNo
- waitingOrderCount
- totalAmount
- auto return

## 정합성

```text
16,800원
```

Cart/Payment/Error/Timeout/Complete 모두 동일.
