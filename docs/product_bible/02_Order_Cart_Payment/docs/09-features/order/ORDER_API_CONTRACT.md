# Order API Contract

> Status: Draft  
> URL naming follows project camelCase rule.

## 1. Create Order

```http
POST /api/kiosk/orders
```

### Request

```json
{
  "orderType": "EAT_IN",
  "items": [
    {
      "menuId": 1,
      "quantity": 2,
      "selectedOptionItemIds": [101, 104],
      "excludedIngredientIds": [33]
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "orderId": 128,
    "orderNo": "1225",
    "orderStatus": "RECEIVED",
    "paymentStatus": "READY",
    "totalAmount": 16800,
    "items": [
      {
        "orderItemId": 500,
        "menuId": 1,
        "menuName": "멕시칸 랩",
        "quantity": 2,
        "unitAmount": 8400,
        "lineAmount": 16800
      }
    ]
  }
}
```

---

## 2. Get Order

```http
GET /api/admin/orders/{orderId}
```

### Response

```json
{
  "success": true,
  "data": {
    "orderId": 128,
    "orderNo": "1225",
    "orderType": "EAT_IN",
    "orderStatus": "PREPARING",
    "paymentStatus": "APPROVED",
    "totalAmount": 16800,
    "createdAt": "2026-07-16T03:15:00",
    "items": []
  }
}
```

---

## 3. Change Order Status

```http
PATCH /api/admin/orders/{orderId}/status
```

### Request

```json
{
  "status": "COMPLETED"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "orderId": 128,
    "orderNo": "1225",
    "previousStatus": "PREPARING",
    "status": "COMPLETED",
    "updatedAt": "2026-07-16T03:25:00"
  }
}
```

---

## 4. Error Codes

```text
ORDER_NOT_FOUND
ORDER_ITEM_REQUIRED
INVALID_ORDER_TYPE
INVALID_ORDER_STATUS
INVALID_ORDER_STATUS_TRANSITION
MENU_NOT_FOUND
MENU_SOLD_OUT
OPTION_ITEM_SOLD_OUT
INVALID_OPTION_SELECTION
ORDER_PRICE_CHANGED
```

---

## 5. Important Rules

- Client totalAmount를 request 기준으로 신뢰하지 않는다.
- orderNo와 orderId는 분리한다.
- API JSON은 camelCase.
- DB는 snake_case.
- completed 상태 재요청은 idempotent 처리 권장.
