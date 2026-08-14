# Menu API Contract

> Status: Current decision (2026-07-23)

## Common rules

- All APIs use `{ success, status, code, message, data }`.
- Use `categoryId`. The live `category` table has no category code.
- Use `tagId` for filtering; `tagCode` is only the display/code value from `tag.code`.
- Use `name`, `price`, and `isSoldOut`. A menu `isActive` field is not supported by the live DB.

## 1. Kiosk menu list

```http
GET /api/kiosk/menuList?categoryId=231
```

```json
{
  "success": true,
  "status": 200,
  "code": "MENU_LIST_SUCCESS",
  "message": "메뉴 목록 조회 성공",
  "data": {
    "categories": [{ "categoryId": 231, "name": "신메뉴", "sortOrder": 0 }],
    "menus": [
      {
        "menuId": 364,
        "categoryId": 231,
        "name": "스파이시 쉬림프 샌드위치",
        "price": 8900,
        "imageUrl": "/assets/menu/364.png",
        "baseKcal": 464,
        "isSoldOut": false,
        "hasSoldOutIngredient": false,
        "isOrderable": true
      }
    ]
  }
}
```

## 2. Kiosk menu detail

```http
GET /api/kiosk/menuDetail/{menuId}
```

`data` contains the menu, ingredients, allergens, and option groups together. The first backend implementation does not add a separate `/api/menus/{menuId}/options` endpoint.

## 3. Admin menu list

```http
GET /api/admin/menus?categoryId=231&keyword=&isSoldOut=false&tagId=&page=0&size=20&sort=name,asc
```

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_MENU_LIST_SUCCESS",
  "message": "관리자 메뉴 목록 조회 성공",
  "data": {
    "content": [
      {
        "menuId": 364,
        "categoryId": 231,
        "categoryName": "신메뉴",
        "name": "스파이시 쉬림프 샌드위치",
        "price": 8900,
        "imageUrl": "/assets/menu/364.png",
        "isSoldOut": false
      }
    ],
    "page": 0,
    "size": 20,
    "totalElements": 1
  }
}
```

## 4. Admin menu detail

```http
GET /api/admin/menus/{menuId}
```

The detail response adds ingredients, nutrition, allergens, tags, and option-policy data. The list response must remain lightweight.

## 5. Admin basic create/update

```http
POST  /api/admin/menus
PATCH /api/admin/menus/{menuId}
```

```json
{
  "categoryId": 231,
  "name": "스파이시 쉬림프 샌드위치",
  "price": 8900,
  "imageUrl": "/assets/menu/364.png",
  "description": "메뉴 설명"
}
```

The create/update response is intentionally a summary object, not the list shape.

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_MENU_UPSERT_SUCCESS",
  "message": "메뉴 저장 성공",
  "data": {
    "menuId": 364,
    "categoryId": 231,
    "name": "스파이시 쉬림프 샌드위치",
    "price": 8900,
    "imageUrl": "/assets/menu/364.png",
    "isSoldOut": false
  }
}
```

## 6. Deferred operations / Admin write notes

- Tag, ingredient, nutrition, and option-policy **writes** are handled in admin create/update (`CreateMenuRequest` children), not in this kiosk read contract.
- `DELETE /api/admin/menus/{menuId}` is **implemented as soft delete** (`menu.deleted_at`). See `MENU_MANAGEMENT_API_CONTRACT.md`.
- Kiosk/admin list·detail exclude rows where `deleted_at IS NOT NULL`.

## 7. Error codes

```text
MENU_NOT_FOUND
INVALID_CATEGORY
INVALID_MENU_PRICE
INVALID_OPTION_SELECTION
OPTION_ITEM_SOLD_OUT
```
