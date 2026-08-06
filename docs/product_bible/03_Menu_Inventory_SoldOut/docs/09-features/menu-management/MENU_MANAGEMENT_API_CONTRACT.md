# Menu Management API Contract

> Status: Draft

## 0. Current Code Snapshot (2026-08-06)

| API | 현재 코드 상태 | 근거 |
| --- | --- | --- |
| `GET /api/admin/menus` | 구현됨 | `AdminMenuController.getMenus`, `menusApi.listMenus` |
| `GET /api/admin/menus/{menuId}` | 구현됨 | `AdminMenuController.getMenuDetail`, `menusApi.getMenu` |
| `GET /api/admin/menus/categories` | 구현됨 | `AdminMenuController.getCategories`, `menusApi.listCategories` |
| `POST /api/admin/menus` | 미구현 | Controller/Service/Mapper TODO 주석만 존재 |
| `PATCH /api/admin/menus/{menuId}` | 미구현 | Controller/Service/Mapper TODO 주석만 존재 |
| `DELETE /api/admin/menus/{menuId}` | 미구현 | Controller/Service/Mapper TODO 주석만 존재 |
| `GET /api/admin/ingredients` | 미구현 | endpoint 미정, TODO 주석만 존재 |

아래 Create/Update/Delete/Ingredient Search 섹션은 아직 초안이다. 현재 코드와 충돌하는 항목은 구현 사실로 간주하지 않는다.

---

## 1. List Menus

```http
GET /api/admin/menus
```

### Query

| name | type | required | notes |
| --- | --- | --- | --- |
| `categoryId` | number | 선택 | 카테고리 필터 |
| `keyword` | string | 선택 | 메뉴명 부분 검색 |
| `isSoldOut` | boolean | 선택 | 품절 여부 필터 |
| `tagId` | number | 선택 | 태그 필터 |
| `page` | number | 선택 | 기본 0 |
| `size` | number | 선택 | 페이지 크기 |
| `sort` | string | 선택 | 현재 코드 기준 `name,asc` 기본, `name,desc`, `price,asc`, `price,desc` 지원 |

### Response `data`

```json
{
  "content": [
    {
      "menuId": 1,
      "categoryId": 10,
      "name": "리코타 샐러드",
      "price": 8900,
      "imageUrl": "/uploads/menu/ricotta.png",
      "isSoldOut": false,
      "hasSoldOutIngredient": false,
      "isOrderable": true
    }
  ],
  "page": 0,
  "size": 20,
  "totalElements": 1,
  "totalPages": 1
}
```

---

## 2. Get Menu Detail

```http
GET /api/admin/menus/{menuId}
```

### Response `data`

```json
{
  "menuId": 1,
  "categoryId": 10,
  "categoryName": "샐러드",
  "name": "리코타 샐러드",
  "price": 8900,
  "imageUrl": "/uploads/menu/ricotta.png",
  "description": "설명",
  "isSoldOut": false,
  "ingredients": [],
  "optionGroups": [],
  "nutrition": {
    "kcal": 320,
    "carbG": 12,
    "proteinG": 14,
    "fatG": 18,
    "sodiumMg": 410
  },
  "allergens": ["우유"],
  "tags": ["BEST"]
}
```

`optionGroups[]`는 현재 `optionGroupId`, `name`, `groupType`, `selectType`, `minSelect`, `maxSelect`, `isRequired`, `recommendedLabel`을 반환한다.

---

## 3. List Categories

```http
GET /api/admin/menus/categories
```

### Response `data`

```json
{
  "content": [
    {
      "categoryId": 1,
      "categoryName": "샐러드",
      "categorySortNo": 1,
      "categoryActive": true
    }
  ],
  "page": 0,
  "size": 20,
  "totalElements": 1,
  "totalPages": 1
}
```

---

## 4. Create Menu

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

## 5. Update Menu

```http
PATCH /api/admin/menus/{menuId}
```

---

## 6. Delete Menu

```http
DELETE /api/admin/menus/{menuId}
```

권장 semantics:

- soft delete
- order history 유지

---

## 7. Ingredient Search

```http
GET /api/admin/ingredients?keyword=&categoryCode=&page=
```

---

## 8. Image Upload

```http
POST /api/admin/menuImages
```

확정 전에는 Draft 상태로 둔다.

---

## 9. Recalculate Nutrition

```http
POST /api/admin/menus/nutrition/calculate
```

MVP에서 미구현 가능.

---

## 10. Error Codes

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
