# Cart API and Data Contract

> Status: Draft

## 1. Local Cart Model

```json
{
  "cartItemId": "local-1",
  "menuId": 1,
  "menuName": "멕시칸 랩",
  "imageUrl": "...",
  "quantity": 2,
  "baseAmount": 7200,
  "optionAmount": 1200,
  "unitAmount": 8400,
  "lineAmount": 16800,
  "selectedOptions": [
    {
      "optionGroupId": 10,
      "optionItemId": 101,
      "optionItemName": "아보카도",
      "additionalAmount": 1200
    }
  ],
  "excludedIngredients": [
    {
      "ingredientId": 33,
      "ingredientName": "양파"
    }
  ]
}
```

---

## 2. Validate Cart

확장 API:

```http
POST /api/kiosk/cart/validate
```

### Request

```json
{
  "items": [
    {
      "menuId": 1,
      "quantity": 2,
      "selectedOptionItemIds": [101],
      "excludedIngredientIds": [33]
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "data": {
    "isValid": true,
    "totalAmount": 16800,
    "itemResults": []
  }
}
```

---

## 3. Validation Failure Example

```json
{
  "success": true,
  "data": {
    "isValid": false,
    "totalAmount": 15600,
    "itemResults": [
      {
        "menuId": 1,
        "reason": "OPTION_ITEM_SOLD_OUT",
        "affectedOptionItemIds": [101]
      }
    ]
  }
}
```

---

## 4. Contract Rules

- Cart는 local state로 먼저 운영 가능
- 서버 validation은 Order 생성 직전 필수
- `lineAmount`와 `totalAmount`는 UI 표시용
- 서버 계산값이 최종
