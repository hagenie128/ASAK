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
GET /api/kiosk/payment-methods
```

### Response

```json
{
  "success": true,
  "status": 200,
  "code": "KIOSK_PAYMENT_METHOD_LIST_SUCCESS",
  "message": "결제수단 목록 조회 성공",
  "data": {
    "methods": [
      {
        "methodCode": "CARD",
        "methodName": "카드·삼성페이",
        "isEnabled": true,
        "sortOrder": 1
      },
      {
        "methodCode": "KAKAO_PAY",
        "methodName": "카카오페이",
        "isEnabled": false,
        "sortOrder": 2
      },
      {
        "methodCode": "NAVER_PAY",
        "methodName": "네이버페이",
        "isEnabled": false,
        "sortOrder": 3
      }
    ]
  }
}
```

`CARD`는 카드 단말 결제이며 삼성페이를 포함한다. `KAKAO_PAY`, `NAVER_PAY`는 현재
비활성 상태여도 화면에는 표시하고 선택만 막는다.

---

## 3. Admin Settings

```http
GET /api/admin/payment-methods
PATCH /api/admin/payment-methods/{methodId}
```

### Fields

```text
isEnabled
sortOrder
methodName
receiptMessage
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
