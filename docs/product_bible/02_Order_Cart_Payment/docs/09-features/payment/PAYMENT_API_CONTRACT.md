# Payment API Contract

> Status: Draft

## 1. Start Payment

```http
POST /api/kiosk/payments
```

### Request

```json
{
  "orderId": 128,
  "paymentMethodCode": "CARD",
  "idempotencyKey": "uuid"
}
```

### Approved Response

```json
{
  "success": true,
  "data": {
    "paymentId": 900,
    "orderId": 128,
    "orderNo": "1225",
    "paymentStatus": "APPROVED",
    "approvedAmount": 16800,
    "waitingOrderCount": 3,
    "approvedAt": "2026-07-16T03:20:00"
  }
}
```

### Failed Response

```json
{
  "success": false,
  "message": "PAYMENT_FAILED",
  "data": {
    "orderId": 128,
    "paymentStatus": "FAILED",
    "failureCode": "CARD_DECLINED",
    "canRetry": true
  }
}
```

---

## 2. Active Payment Methods

```http
GET /api/kiosk/paymentMethods
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "paymentMethodCode": "CARD",
      "displayName": "신용카드",
      "status": "ENABLED",
      "sortOrder": 1
    }
  ]
}
```

---

## 3. Admin Settings

```http
GET /api/admin/paymentMethods
PATCH /api/admin/paymentMethods/{paymentMethodId}
```

### Fields

```text
status
sortOrder
displayName
receiptMessage
failureRetentionMinutes
```

---

## 4. Error Codes

```text
ORDER_NOT_FOUND
ORDER_AMOUNT_MISMATCH
PAYMENT_METHOD_DISABLED
PAYMENT_ALREADY_APPROVED
PAYMENT_IN_PROGRESS
PAYMENT_FAILED
PAYMENT_TIMEOUT
```
