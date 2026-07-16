# Menu Management API Contract

> Status: Draft

## 1. Create Menu

```http
POST /api/admin/menus
```

### Request

```json
{
  "menuName": "멕시칸 랩",
  "description": "...",
  "categoryCode": "WRAP",
  "basePrice": 7200,
  "imageUrl": "...",
  "isActive": true,
  "tagCodes": ["BEST"],
  "ingredients": [
    {
      "ingredientId": 33,
      "role": "STANDARD",
      "quantity": 30,
      "unit": "g",
      "canRemove": true
    }
  ],
  "optionGroups": [
    {
      "optionGroupName": "드레싱",
      "isRequired": true,
      "minimumSelection": 1,
      "maximumSelection": 1,
      "options": [
        {
          "optionItemId": 101,
          "additionalAmount": 0,
          "isRecommended": true,
          "isActive": true
        }
      ]
    }
  ]
}
```

---

## 2. Update Menu

```http
PATCH /api/admin/menus/{menuId}
```

---

## 3. Delete Menu

```http
DELETE /api/admin/menus/{menuId}
```

권장 semantics:

- soft delete
- order history 유지

---

## 4. Ingredient Search

```http
GET /api/admin/ingredients?keyword=&categoryCode=&page=
```

---

## 5. Image Upload

```http
POST /api/admin/menuImages
```

확정 전에는 Draft 상태로 둔다.

---

## 6. Recalculate Nutrition

```http
POST /api/admin/menus/nutrition/calculate
```

MVP에서 미구현 가능.

---

## 7. Error Codes

```text
MENU_NAME_REQUIRED
MENU_NAME_DUPLICATED
MENU_PRICE_INVALID
CATEGORY_REQUIRED
INGREDIENT_DUPLICATED
OPTION_GROUP_INVALID
RECOMMENDED_OPTION_INVALID
IMAGE_UPLOAD_FAILED
MENU_DELETE_CONFLICT
```
