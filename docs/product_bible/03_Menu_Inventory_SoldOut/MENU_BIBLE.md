# Menu Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `MENU_API_CONTRACT.md`
- `MENU_ARCHITECTURE.md`
- `MENU_DETAIL_FLOW_AND_VALIDATION.md`
- `MENU_EDGE_CASE_AND_QA.md`

---

## 원문: `MENU_API_CONTRACT.md`

### Menu API Contract

> Status: Current decision (2026-07-23)

#### Common rules

- All APIs use `{ success, status, code, message, data }`.
- Use `categoryId`. The live `category` table has no category code.
- Use `tagId` for filtering; `tagCode` is only the display/code value from `tag.code`.
- Use `name`, `price`, and `isSoldOut`. A menu `isActive` field is not supported by the live DB.

#### 1. Kiosk menu list

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

#### 2. Kiosk menu detail

```http
GET /api/kiosk/menuDetail/{menuId}
```

`data` contains the menu, ingredients, allergens, and option groups together. The first backend implementation does not add a separate `/api/menus/{menuId}/options` endpoint.

#### 3. Admin menu list

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

#### 4. Admin menu detail

```http
GET /api/admin/menus/{menuId}
```

The detail response adds ingredients, nutrition, allergens, tags, and option-policy data. The list response must remain lightweight.

#### 5. Admin basic create/update

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

#### 6. Deferred operations / Admin write notes

- Tag, ingredient, nutrition, and option-policy **writes** are handled in admin create/update (`CreateMenuRequest` children), not in this kiosk read contract.
- `DELETE /api/admin/menus/{menuId}` is **implemented as soft delete** (`menu.deleted_at`). See `MENU_MANAGEMENT_API_CONTRACT.md`.
- Kiosk/admin list·detail exclude rows where `deleted_at IS NOT NULL`.

#### 7. Error codes

```text
MENU_NOT_FOUND
INVALID_CATEGORY
INVALID_MENU_PRICE
INVALID_OPTION_SELECTION
OPTION_ITEM_SOLD_OUT
```

---

## 원문: `MENU_ARCHITECTURE.md`

### Menu Architecture

> Status: Current
> Domain: Menu

#### 1. 목적

Menu 도메인은 고객이 주문 가능한 상품 단위를 정의한다.

ASAK에서 Menu는 이름과 가격만 가진 단순 상품이 아니다.

Menu는 다음 요소의 조합이다.

- 카테고리
- 기본 가격
- 이미지
- 칼로리 및 영양정보
- 포함 재료
- 제외 가능한 재료
- 옵션 그룹
- 추천 옵션
- 태그
- 알레르기 정보
- 판매 상태
- 품절 영향

---

#### 2. Canonical Menu Model

```json
{
  "menuId": 1,
  "menuName": "멕시칸 랩",
  "description": "신선한 채소와 단백질을 담은 랩",
  "categoryCode": "WRAP",
  "basePrice": 7200,
  "imageUrl": "...",
  "calories": 430,
  "isActive": true,
  "isSoldOut": false,
  "tags": ["BEST"],
  "ingredients": [],
  "optionGroups": [],
  "allergens": []
}
```

---

#### 3. Menu Category

권장 code:

```text
SALAD
SANDWICH
WARM_BOWL
WRAP
SIDE
DRINK
```

카테고리명은 Figma·API·DB에서 동일하게 유지한다.

주의:

- `웜볼`
- `웜 보울`
- `Warm Bowl`

처럼 표기가 흔들리지 않도록 displayName과 code를 분리한다.

예:

```json
{
  "categoryCode": "WARM_BOWL",
  "displayName": "웜볼"
}
```

---

#### 4. Menu Status

##### isActive

- 고객에게 노출할 수 있는지
- 관리자가 숨김 처리할 수 있음

##### isSoldOut

- 현재 주문 가능한지
- 직접 품절 또는 전파 품절 가능

##### 상태 조합

| isActive | isSoldOut | 의미 |
|---|---|---|
| true | false | 판매 중 |
| true | true | 노출되지만 품절 |
| false | false | 숨김 |
| false | true | 운영상 비활성 + 품절 |

관리 화면에서는 상태를 하나의 toggle로 뭉치지 않는다.

---

#### 5. Ingredient Role

Menu와 Ingredient의 관계는 역할을 가진다.

권장 role:

```text
CORE
BASE
STANDARD
OPTIONAL
```

##### CORE

핵심 재료.

품절 시 메뉴 품절로 전파될 수 있다.

##### BASE

메뉴의 기반.

품절 시 메뉴 또는 해당 기반 카테고리 주문 불가.

##### STANDARD

기본 포함 재료.

제외 가능 여부를 가질 수 있다.

##### OPTIONAL

추가 옵션 또는 선택 재료.

---

#### 6. Option Structure

```text
Menu
└─ Option Group
   └─ Option Item
```

Option Group fields:

```text
optionGroupId
optionGroupName
isRequired
minimumSelection
maximumSelection
sortOrder
isActive
```

Option Item fields:

```text
optionItemId
optionItemName
additionalAmount
isRecommended
isSoldOut
sortOrder
```

---

#### 7. Nutrition

Nutrition은 두 수준으로 나눈다.

##### Base Nutrition

메뉴 기본 구성 기준.

##### Calculated Nutrition

선택 옵션과 제외 재료를 반영한 추정값.

MVP 권장:

- Figma/React는 계산 가능 구조를 유지
- 실제 자동 계산은 추가 구현 범위
- 계산되지 않은 값은 확정값처럼 보여주지 않는다

---

#### 8. Allergen

알레르기 정보는 메뉴에 직접 수기 입력하는 방식보다 재료 기반 집계를 권장한다.

```text
Ingredient
→ IngredientAllergen
→ MenuIngredient
→ Menu Allergen Summary
```

관리 화면은 집계 결과를 보여주되, 관리자가 예외를 확인할 수 있어야 한다.

---

#### 9. Tags

권장 tags:

```text
BEST
NEW
VEGAN
```

Tag는 UI 장식이 아니라 검색·필터·운영에 활용 가능한 code로 관리한다.

---

#### 10. Figma Mapping

##### Kiosk

- SCR-003 Menu List
- SCR-004 Menu Detail
- SCR-005 Cart option summary

##### Admin

- SCR-016 Menu Management
- IngredientSelectModal
- MenuCard
- OptionGroup
- SaveBar

---

#### 11. React Mapping

##### Kiosk

```text
MenuListPage
MenuDetailPage
MenuCard
CategoryTabs
OptionGroup
OptionItem
AllergenNotice
NutritionSummary
```

##### Admin

```text
MenuManagementPage
MenuForm
IngredientSelectModal
OptionGroupEditor
NutritionPanel
AllergenPanel
TagSelector
SaveBar
```

---

#### 12. Backend Mapping

```text
menu/
ingredient/
option/
allergen/
nutrition/
tag/
```

권장 domain package 기준으로 분리하되 실제 프로젝트 구조에 맞춘다.

---

#### 13. Implementation Checklist

- [ ] category code 통일
- [ ] Menu active/sold-out 분리
- [ ] ingredient role
- [ ] option group min/max
- [ ] recommended option
- [ ] nutrition source 구분
- [ ] allergen aggregation
- [ ] tags
- [ ] Kiosk sold-out state
- [ ] Admin validation

---

## 원문: `MENU_DETAIL_FLOW_AND_VALIDATION.md`

### Menu Detail Flow and Validation

> Status: Current

#### 1. 화면 목적

SCR-004 Menu Detail의 목적은 고객이 메뉴 구성을 실수 없이 완성하게 하는 것이다.

---

#### 2. 권장 선택 순서

1. 베이스
2. 필수 옵션
3. 추가 옵션
4. 제외 재료
5. 드레싱
6. 수량

실제 메뉴 구조에 따라 순서는 바뀔 수 있지만, 필수 옵션은 선택 옵션보다 먼저 둔다.

---

#### 3. Required States

```text
default
validationError
soldOut
optionSoldOut
maximumExceeded
minimumNotMet
priceUpdated
```

---

#### 4. Validation Rules

##### Required Group

```text
selectedCount >= minimumSelection
```

##### Maximum

```text
selectedCount <= maximumSelection
```

##### Single Select

```text
maximumSelection = 1
```

##### Sold-out Option

- 선택 불가
- disabled
- 품절 badge
- 기존 선택이 품절되면 validation error

---

#### 5. Price Calculation

```text
basePrice
+ sum(selected option additionalAmount)
= unitAmount
```

수량 반영:

```text
unitAmount × quantity = lineAmount
```

가격 변화는 선택 직후 반영한다.

---

#### 6. Back Navigation

뒤로 가도 선택을 유지한다.

권장 방식:

- local draft state
- route state
- store draft

단, Cart에 담기기 전 draft와 Cart item을 혼동하지 않는다.

---

#### 7. Add to Cart Sequence

```text
select options
→ validate
→ calculate
→ create cartItemId
→ addItem
→ success feedback
```

---

#### 8. Validation Copy

##### 필수 미선택

`필수 옵션을 선택해주세요.`

##### 최대 초과

`최대 {n}개까지 선택할 수 있어요.`

##### 품절 옵션

`선택한 옵션이 품절되었습니다. 다른 옵션을 선택해주세요.`

---

#### 9. QA

- [ ] 필수 옵션 표시
- [ ] min/max 표시
- [ ] sold-out disabled
- [ ] 가격 즉시 반영
- [ ] allergen 변경 반영
- [ ] 뒤로가기 선택 유지
- [ ] add CTA disabled 기준

---

## 원문: `MENU_EDGE_CASE_AND_QA.md`

### Menu Edge Cases and QA

#### Edge Cases

##### 메뉴 숨김과 품절 동시 적용

관리 화면에서는 두 상태를 분리해서 보여준다.

##### 추천 옵션이 품절

추천 badge 제거 또는 다른 추천으로 변경.

##### Option Group의 min > active option count

메뉴 판매 차단 또는 관리자 저장 차단.

##### 알레르기 자동 집계 누락

재료 기반 집계 실패 시 관리자 경고.

##### 메뉴 이미지 없음

Kiosk fallback image.

##### 가격 0 또는 음수

서버 validation.

##### 동일 메뉴명

정책에 따라 unique 또는 category 내 unique.

---

#### Allergy integrity (2026-08-12)

- Source of truth: `asak-data/scripts/input/allergy_260715.csv`; prefer `SALADY` rows.
- Menu allergens are derived by the `menu_ing -> ing_allergen -> allergen` relation. Correct high-confidence omissions at the ingredient relation, not by copying menu values.
- High-confidence links: implemented in seed and live DB, 11 links across 10 ingredients.
- Live checklist: 36 mismatches before, 26 remaining after the change; 10 menu records now match the official sheet.
- Deletion candidates remain `decision required`: shared dressing and sauce ingredients need an impact review before removing any allergen.
- Customer display remains `not connected`: the kiosk detail API and `MenuDetailPage` do not currently pass or render an allergens field.

##### Allergy regression QA

- [x] The 11 approved links exist in seed and DB.
- [x] `ing_allergen` has no duplicate `(ing_id, allergen_id)` pairs in seed.
- [x] The original 36-menu checklist was recalculated against live DB.
- [ ] Add `allergens: string[]` to `GET /api/kiosk/menuDetail/{menuId}`.
- [ ] Render the real API data through `AllergenAccordion` in the kiosk detail screen.
- [ ] Browser QA: no allergen, one allergen, and long allergen-list states.

#### Figma QA

- [ ] Menu List Error
- [ ] image fallback
- [ ] sold-out badge
- [ ] Detail validation state
- [ ] option sold-out
- [ ] recommendation
- [ ] allergen
- [ ] nutrition note

#### Admin QA

- [ ] add/edit 구분
- [ ] required field
- [ ] image state
- [ ] tags
- [ ] ingredient role
- [ ] option min/max
- [ ] save/cancel/delete
