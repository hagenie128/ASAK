# Menu Management API Contract

> Status: Partial — 조회·등록·수정·삭제·재료 목록은 코드 반영 (2026-08-11). Image upload·nutrition calculate는 Draft.

## 0. Current Code Snapshot (2026-08-11)

| API | 현재 코드 상태 | 근거 |
| --- | --- | --- |
| `GET /api/admin/menus` | 구현됨 | `AdminMenuController.getMenus` → `vw_menu_list` (`deleted_at IS NULL`) |
| `GET /api/admin/menus/{menuId}` | 구현됨 | `getMenuDetail` · `menu.deleted_at IS NULL` |
| `GET /api/admin/menus/categories` | 구현됨 | `getCategories` |
| `GET /api/admin/menus/ingredients` | 구현됨 | `getIngredients` · `IngredientResponse` |
| `POST /api/admin/menus` | 구현됨 | JSON `CreateMenuRequest` · code `ADMIN_MENU_UPSERT_SUCCESS` |
| `PATCH /api/admin/menus/{menuId}` | 구현됨 | 동일 body shape · code `ADMIN_MENU_UPDATE_SUCCESS` |
| `DELETE /api/admin/menus/{menuId}` | 구현됨 | **soft delete** (`menu.deleted_at`) · code `ADMIN_MENU_DELETE_SUCCESS` |
| `POST /api/admin/menuImages` | 미연결 | `AdminMenuService.saveMenuImage`만 존재, Controller 매핑 없음 |
| `POST /api/admin/menus/nutrition/calculate` | 미구현 | — |

인증: 현재 Admin 메뉴 Controller에 JWT/권한 검사는 없다. (공통 Security 설정에 따름 — 미검증)

목록·상세은 soft-deleted 메뉴를 반환하지 않는다.

---

## 1. List Menus

```http
GET /api/admin/menus
```

성공 code: `ADMIN_MENU_LIST_SUCCESS`

### Query

| name | type | required | notes |
| --- | --- | --- | --- |
| `categoryId` | number | 선택 | 카테고리 필터 |
| `keyword` | string | 선택 | 메뉴명 부분 검색 |
| `isSoldOut` | boolean | 선택 | 품절 여부 필터 |
| `tagId` | number | 선택 | 태그 필터 |
| `page` | number | 선택 | 기본 0 |
| `size` | number | 선택 | 기본 **12** (`MenuListRequest`, max 100) |
| `sort` | string | 선택 | `name,asc`(기본), `name,desc`, `price,asc`, `price,desc` |

### Response `data`

`PageResult` of `MenuListResponse`

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
  "size": 12,
  "totalElements": 1,
  "totalPages": 1
}
```

---

## 2. Get Menu Detail

```http
GET /api/admin/menus/{menuId}
```

성공 code: `ADMIN_MENU_DETAIL_SUCCESS`
없으면 `MENU_NOT_FOUND` (삭제된 메뉴 포함).

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

성공 code: `ADMIN_CATEGORY_LIST_SUCCESS`

### Response `data` (코드 필드)

```json
{
  "content": [
    {
      "categoryId": 1,
      "categoryName": "샐러드",
      "sortOrder": 1,
      "isActive": true
    }
  ],
  "page": 0,
  "size": 1,
  "totalElements": 1,
  "totalPages": 1
}
```

---

## 4. Create Menu

```http
POST /api/admin/menus
Content-Type: application/json
```

성공 code: `ADMIN_MENU_UPSERT_SUCCESS`
요청: `CreateMenuRequest` (camelCase)

```json
{
  "categoryId": 236,
  "name": "Bruno Sample Menu",
  "price": 8900,
  "imageUrl": "/assets/menu/sample.png",
  "description": "Bruno contract sample menu",
  "ingredients": [
    {
      "ingredientId": 143,
      "role": "core",
      "quantity": 0,
      "unit": "G",
      "isDefault": true,
      "canRemove": false
    }
  ],
  "optionGroups": [
    {
      "optionGroupId": 240,
      "isRequired": true,
      "recommendedOptionItemId": 269,
      "items": [
        { "optionItemId": 265, "isRecommended": false },
        { "optionItemId": 269, "isRecommended": true }
      ]
    }
  ],
  "nutrition": {
    "kcal": 320,
    "carbG": 12,
    "proteinG": 14,
    "fatG": 18,
    "sodiumMg": 410
  },
  "tags": [
    { "code": "NEW", "name": "NEW" }
  ]
}
```

Write 대상: `menu`, `menu_ing`, `menu_opt_policy`, `menu_opt_override`(추천), `menu_nutr`, `menu_tag`.
allergens는 저장하지 않음(상세 조회 시 조인).

> 구 Draft 필드명(`menuName`, `basePrice`, `categoryCode`, `isActive` 등)은 **현재 DTO와 계약 불일치**. 클라이언트는 위 shape를 쓴다.

---

## 5. Update Menu

```http
PATCH /api/admin/menus/{menuId}
Content-Type: application/json
```

성공 code: `ADMIN_MENU_UPDATE_SUCCESS`
body: Create와 **동일 shape** (`CreateMenuRequest`).

- 본문(categoryId, name, price, imageUrl, description)은 항상 갱신.
- `ingredients` / `optionGroups` / `nutrition` / `tags`가 **null이 아니면** 해당 자식 테이블을 삭제 후 재삽입.
- null이면 해당 섹션 유지.
- soft-deleted 메뉴는 `MENU_NOT_FOUND`.

---

## 6. Delete Menu

```http
DELETE /api/admin/menus/{menuId}
```

성공 code: `ADMIN_MENU_DELETE_SUCCESS`

Semantics (**구현됨**):

- soft delete: `menu.deleted_at = CURRENT_TIMESTAMP`
- `order_item.menu_id` FK 유지 → 주문 이력·매출 보존
- 자식(`menu_ing`, `menu_nutr`, `menu_opt_*`, `menu_tag`)은 **삭제하지 않음**
- 목록/상세/키오스크 조회는 `deleted_at IS NULL`만 노출

오류:

- `MENU_DELETE_INVALID` — menuId 무효
- `MENU_NOT_FOUND` — 없거나 이미 삭제됨
- `MENU_DELETE_FAILED` — UPDATE 실패

> Draft의 `MENU_DELETE_CONFLICT`는 현재 `ErrorCode`에 없음 → **계약 불일치 / 결정 필요**.

---

## 7. Ingredient List

```http
GET /api/admin/menus/ingredients
```

성공 code: `ADMIN_MENU_INGREDIENTS_SUCCESS`
경로 주의: `/api/admin/ingredients`가 아니라 **`/api/admin/menus/ingredients`**.

`data`: `PageResult` of `IngredientResponse`
필드: `id`, `name`, `isSoldOut`, `roleName`, `unitName`, `servingG`, `kcal`, `carbG`, `sugarG`, `proteinG`, `fatG`, `saturatedFatG`, `sodiumMg`
현재 구현은 keyword/paging 없이 전체 목록을 한 페이지로 반환한다.

---

## 8. Image Upload

```http
POST /api/admin/menuImages
```

**미연결.** `FileUtil.saveMenuImage` / `AdminMenuService.saveMenuImage` 골격만 있음.
등록·수정은 JSON `imageUrl` 문자열만 받는다. → **결정 필요** (multipart 연결 여부).

---

## 9. Recalculate Nutrition

```http
POST /api/admin/menus/nutrition/calculate
```

MVP에서 미구현.

---

## 10. Error Codes (코드 기준)

```text
MENU_NOT_FOUND
MENU_CREATE_INVALID
MENU_INSERT_FAILED
MENU_UPDATE_FAILED
MENU_UPDATE_INVALID
MENU_UPDATE_NOT_FOUND
MENU_DELETE_INVALID
MENU_DELETE_NOT_FOUND
MENU_DELETE_FAILED
MENU_IMAGE_SAVE_FAILED
```

구 Draft 코드(`MENU_NAME_REQUIRED`, `MENU_DELETE_CONFLICT` 등)는 현재 `ErrorCode`와 **계약 불일치**. 통합 여부는 결정 필요.
