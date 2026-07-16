# Menu API Contract

> Status: Draft

## 1. Menu List

```http
GET /api/kiosk/menuList
```

### Query

```text
categoryCode
tag
keyword
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "menuId": 1,
      "menuName": "멕시칸 랩",
      "categoryCode": "WRAP",
      "displayCategoryName": "랩",
      "price": 7200,
      "calories": 430,
      "imageUrl": "...",
      "isActive": true,
      "isSoldOut": false,
      "tags": ["BEST"]
    }
  ]
}
```

---

## 2. Menu Detail

```http
GET /api/kiosk/menuDetail/{menuId}
```

### Response

```json
{
  "success": true,
  "data": {
    "menuId": 1,
    "menuName": "멕시칸 랩",
    "description": "...",
    "basePrice": 7200,
    "calories": 430,
    "imageUrl": "...",
    "isSoldOut": false,
    "ingredients": [
      {
        "ingredientId": 33,
        "ingredientName": "양파",
        "role": "STANDARD",
        "canRemove": true,
        "isSoldOut": false
      }
    ],
    "optionGroups": [
      {
        "optionGroupId": 10,
        "optionGroupName": "드레싱",
        "isRequired": true,
        "minimumSelection": 1,
        "maximumSelection": 1,
        "options": [
          {
            "optionItemId": 101,
            "optionItemName": "시저",
            "additionalAmount": 0,
            "isRecommended": true,
            "isSoldOut": false
          }
        ]
      }
    ],
    "allergens": [
      {
        "allergenCode": "MILK",
        "displayName": "우유"
      }
    ]
  }
}
```

---

## 3. Admin Menu List

```http
GET /api/admin/menus
```

Query:

```text
keyword
categoryCode
status
tag
page
size
sort
```

---

## 4. Admin Create

```http
POST /api/admin/menus
```

### Request

```json
{
  "menuName": "멕시칸 랩",
  "categoryCode": "WRAP",
  "basePrice": 7200,
  "description": "...",
  "imageUrl": "...",
  "isActive": true,
  "tagCodes": ["BEST"],
  "ingredients": [],
  "optionGroups": []
}
```

---

## 5. Admin Update

```http
PATCH /api/admin/menus/{menuId}
```

---

## 6. Error Codes

```text
MENU_NOT_FOUND
MENU_NAME_DUPLICATED
INVALID_CATEGORY
INVALID_MENU_PRICE
INVALID_INGREDIENT_ROLE
INVALID_OPTION_GROUP
INVALID_OPTION_SELECTION_RANGE
IMAGE_UPLOAD_FAILED
```
