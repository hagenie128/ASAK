# Menu Management Implementation

## Current Code Status (2026-08-06)

- 구현됨: `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`
- 미구현: `POST /api/admin/menus`, `PATCH /api/admin/menus/{menuId}`, `DELETE /api/admin/menus/{menuId}`
- `AdminMenuService.createMenu(MultipartFile imageFile)`는 이미지 저장 골격만 있고 DB 저장은 아직 없다.
- 실제 조회 SQL은 `vw_menu_list`, `menu + category`, `vw_menu_ing_json`, `vw_menu_opt_policy_json`, `menu_nutr`, `menu_tag`를 사용한다.

## Create

```text
validate basic fields
→ category 조회
→ ingredient 관계 검증
→ option group 검증
→ nutrition/allergen 계산 또는 저장
→ Menu 저장
→ 관계 저장
```

현재 코드 기준으로는 위 흐름이 아직 구현되지 않았다. 특히 `CreateMenuRequest`, INSERT Mapper, 생성 응답 규격이 모두 TODO 상태다.

## Update

- original entity 조회
- 변경 가능한 필드만 반영
- 연관관계 orphan 정책 확인
- transaction 내 처리

현재 코드에는 Update endpoint/service/mapper가 없다.

## Delete

soft delete 권장.

```text
isDeleted = true
deletedAt = now
```

기존 order history를 보존한다.

현재 코드에는 soft delete / hard delete 정책이 아직 확정되지 않았다.

## Validation

- menuName required
- price >= 0
- minSelection <= maxSelection
- recommended option active
- duplicate ingredient policy

## Current Read Flow

```text
AdminMenuController.getMenus
→ AdminMenuService.getMenus
→ AdminMenuMapper.getMenus / countMenus
→ vw_menu_list 기반 PageResult 반환
```

```text
AdminMenuController.getMenuDetail
→ AdminMenuService.getMenuDetail
→ AdminMenuMapper.getMenuDetail
→ nutrition / ingredients / optionGroups / allergens / tags 서브조회
```

## Decision Needed

- 등록/수정 요청 형식: JSON vs multipart
- 삭제 정책: soft delete vs hard delete
- 재료 검색 endpoint 경로와 응답 shape
