# Menu and Order Implementation

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `MENU_ENTITY_IMPLEMENTATION.md`
- `MENU_MANAGEMENT_IMPLEMENTATION.md`
- `MENU_QUERY_IMPLEMENTATION.md`
- `ORDER_CREATE_IMPLEMENTATION.md`
- `ORDER_ENTITY_IMPLEMENTATION.md`
- `ORDER_STATUS_IMPLEMENTATION.md`

---

## 원문: `MENU_ENTITY_IMPLEMENTATION.md`

### Menu Entity Implementation

#### 최소 Entity

- MenuCategory
- Menu
- Ingredient
- MenuIngredient
- OptionGroup
- OptionItem
- MenuOptionGroup
- Allergen
- IngredientAllergen
- MenuTag

#### Menu 주요 필드

```text
id
menuName
description
basePrice
imageUrl
calories
isActive
directSoldOut
derivedSoldOut
createdAt
updatedAt
```

#### effectiveSoldOut

DB 컬럼으로 저장할지 계산할지 결정해야 한다.

MVP 권장:

```java
public boolean isEffectiveSoldOut() {
    return directSoldOut || derivedSoldOut;
}
```

#### Ingredient Role

```text
CORE
BASE
STANDARD
OPTIONAL
```

#### 주의

Ingredient는 여러 Menu에서 공유한다.
Menu 삭제 cascade로 Ingredient를 삭제하지 않는다.

---

## 원문: `MENU_MANAGEMENT_IMPLEMENTATION.md`

### Menu Management Implementation

#### Current Code Status (2026-08-11)

- 구현됨: `GET/POST/PATCH/DELETE /api/admin/menus`, `GET .../categories`, `GET .../ingredients`, `GET .../{menuId}`
- 삭제: **soft delete** (`menu.deleted_at`). 주문 이력 FK 유지.
- 등록/수정: JSON `CreateMenuRequest`. 이미지 multipart는 Controller 미연결(`saveMenuImage`만 존재).
- 조회 SQL: `vw_menu_list`(삭제 제외), `menu + category`, `vw_menu_ing_json`, `vw_menu_opt_policy_json`, `menu_nutr`, `menu_tag`
- DDL/마이그레이션 문서: `ASAK-back/docs/migrations/2026-08-11_menu_soft_delete.sql`, `docs/view.sql` (`WHERE m.deleted_at IS NULL`)

#### Create

```text
CreateMenuRequest 검증(categoryId 등)
→ insertMenu
→ insertChildren (ingredients / optionGroups+override / nutrition / tags)
→ getMenuDetail
```

근거: `AdminMenuService.createMenu`, `AdminMenuMapper.insert*`

#### Update

```text
requireActiveMenu (deleted_at IS NULL)
→ updateMenu (본문)
→ ingredients/optionGroups/nutrition/tags 가 null이 아니면 자식 교체(delete+insert)
→ getMenuDetail
```

optionGroups 교체 시 `menu_opt_override`를 먼저 삭제한다.

#### Delete

```text
requireActiveMenu
→ softDeleteMenu (deleted_at = NOW, updated_at = NOW)
```

자식 테이블은 지우지 않는다. hard delete / cascade 삭제는 사용하지 않는다.

#### Validation (현재 코드)

- `categoryId` 필수(등록 Controller)
- ingredient `ingredientId` / role·unit common_code 해석
- optionGroup → opt_policy 존재, 추천 optionItem이 정책에 속하는지
- tag code/name으로 기존 tag 조회 (없으면 `MENU_CREATE_INVALID`)

#### Current Read Flow

```text
AdminMenuController.getMenus
→ AdminMenuService.getMenus
→ AdminMenuMapper.getMenus / countMenus
→ vw_menu_list (deleted_at IS NULL) 기반 PageResult
```

```text
AdminMenuController.getMenuDetail
→ AdminMenuService.getMenuDetail
→ AdminMenuMapper.getMenuDetail
→ nutrition / ingredients / optionGroups / allergens / tags 서브조회
```

```text
AdminMenuController.deleteMenu
→ AdminMenuService.deleteMenu
→ AdminMenuMapper.softDeleteMenu
```

#### Decision Needed

- 등록/수정 요청 형식: JSON `imageUrl` 유지 vs multipart 업로드 API 연결
- Draft 오류 코드(`MENU_DELETE_CONFLICT` 등) vs 구현 `ErrorCode` 통합
- 재료 목록 keyword/paging 추가 여부 (현재 전체 목록 1페이지)

---

## 원문: `MENU_QUERY_IMPLEMENTATION.md`

### Menu Query Implementation

#### Kiosk Menu List

```http
GET /api/kiosk/menuList
```

Service 순서:

1. categoryCode 검증
2. active menu 조회
3. effective sold-out 계산
4. list DTO 변환
5. sortOrder 적용

#### Kiosk Menu Detail

```http
GET /api/kiosk/menuDetail/{menuId}
```

필요 데이터:

- Menu
- Category
- Ingredients
- Option Groups
- Option Items
- Allergens
- Tags

#### N+1 방지

선택지:

- fetch join
- EntityGraph
- DTO projection
- 명시적 query 분리

모든 관계 EAGER 전환 금지.

---

## 원문: `ORDER_CREATE_IMPLEMENTATION.md`

### Order Create Implementation

#### Endpoint

```http
POST /api/kiosk/orders
```

#### Service Flow

1. items 존재 확인
2. menuId 일괄 조회
3. active / sold-out 검증
4. option group 규칙 검증
5. option sold-out 검증
6. ingredient 영향 검증
7. 서버 가격 계산
8. orderNo 생성
9. Order 저장
10. OrderItem 저장
11. OrderItemOption 저장
12. response 반환

#### 서버 가격 계산

```text
unitAmount = menu.basePrice + selectedOptionAmount
lineAmount = unitAmount × quantity
totalAmount = sum(lineAmount)
```

클라이언트 totalAmount는 신뢰하지 않는다.

#### Transaction

Order + Item + Option 전체 저장은 하나의 transaction.

---

## 원문: `ORDER_ENTITY_IMPLEMENTATION.md`

### Order Entity Implementation

#### Entity

```text
Order
OrderItem
OrderItemOption
```

#### Order

필드:

```text
id
orderNo
orderType
orderStatus
paymentStatus
totalAmount
createdAt
updatedAt
```

#### OrderItem Snapshot

반드시 당시 값을 보관한다.

```text
menuId
menuName
unitAmount
quantity
lineAmount
```

메뉴명이 바뀌어도 과거 주문이 바뀌지 않아야 한다.

#### OrderItemOption Snapshot

```text
optionItemId
optionItemName
additionalAmount
```

#### 상태

```text
RECEIVED
PREPARING
COMPLETED
```

---

## 원문: `ORDER_STATUS_IMPLEMENTATION.md`

### Order Status Implementation

#### Endpoint

```http
PATCH /api/admin/orders/{orderId}/{status}
```

#### 허용 전이

```text
RECEIVED → PREPARING
PREPARING → COMPLETED
```

#### 중복 완료

이미 COMPLETED면:

- 현재 상태를 idempotent하게 반환
- 완료 event 중복 생성 금지

#### TTS

Backend는 음성을 실행하지 않는다.

Frontend는 상태 변경 성공 응답 후 TTS를 실행한다.

#### Response

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_ORDER_STATUS_CHANGE_SUCCESS",
  "message": "관리자 주문 상태 변경 성공",
  "data": null
}
```
