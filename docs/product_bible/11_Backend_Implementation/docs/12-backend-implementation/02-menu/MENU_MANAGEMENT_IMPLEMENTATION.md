# Menu Management Implementation

## Current Code Status (2026-08-11)

- 구현됨: `GET/POST/PATCH/DELETE /api/admin/menus`, `GET .../categories`, `GET .../ingredients`, `GET .../{menuId}`
- 삭제: **soft delete** (`menu.deleted_at`). 주문 이력 FK 유지.
- 등록/수정: JSON `CreateMenuRequest`. 이미지 multipart는 Controller 미연결(`saveMenuImage`만 존재).
- 조회 SQL: `vw_menu_list`(삭제 제외), `menu + category`, `vw_menu_ing_json`, `vw_menu_opt_policy_json`, `menu_nutr`, `menu_tag`
- DDL/마이그레이션 문서: `ASAK-back/docs/migrations/2026-08-11_menu_soft_delete.sql`, `docs/view.sql` (`WHERE m.deleted_at IS NULL`)

## Create

```text
CreateMenuRequest 검증(categoryId 등)
→ insertMenu
→ insertChildren (ingredients / optionGroups+override / nutrition / tags)
→ getMenuDetail
```

근거: `AdminMenuService.createMenu`, `AdminMenuMapper.insert*`

## Update

```text
requireActiveMenu (deleted_at IS NULL)
→ updateMenu (본문)
→ ingredients/optionGroups/nutrition/tags 가 null이 아니면 자식 교체(delete+insert)
→ getMenuDetail
```

optionGroups 교체 시 `menu_opt_override`를 먼저 삭제한다.

## Delete

```text
requireActiveMenu
→ softDeleteMenu (deleted_at = NOW, updated_at = NOW)
```

자식 테이블은 지우지 않는다. hard delete / cascade 삭제는 사용하지 않는다.

## Validation (현재 코드)

- `categoryId` 필수(등록 Controller)
- ingredient `ingredientId` / role·unit common_code 해석
- optionGroup → opt_policy 존재, 추천 optionItem이 정책에 속하는지
- tag code/name으로 기존 tag 조회 (없으면 `MENU_CREATE_INVALID`)

## Current Read Flow

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

## Decision Needed

- 등록/수정 요청 형식: JSON `imageUrl` 유지 vs multipart 업로드 API 연결
- Draft 오류 코드(`MENU_DELETE_CONFLICT` 등) vs 구현 `ErrorCode` 통합
- 재료 목록 keyword/paging 추가 여부 (현재 전체 목록 1페이지)
