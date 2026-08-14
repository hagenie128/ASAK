# Menu Management Frontend Implementation

## Current Code Status (2026-08-06)

- `useMenusQuery`가 `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`를 실제 호출한다.
- 화면 조합은 `MenuManagePage` + `MenuListPanel` + `MenuDetailPanel` + `MenuEditPanel` 구조다.
- `view / edit / create` 패널 모드는 구현되어 있다.
- `create`, `update`, `delete` 저장은 아직 API 미연결이며 현재 화면에서 stub toast만 호출한다.
- `IngredientSelectModal` 자동완성과 이미지 업로드는 아직 미연결이다.

## Shared Form

Add/Edit는 동일 Form.

State:

```text
original
draft
dirtyFields
validationErrors
```

현재 코드에는 `dirtyFields`, `validationErrors`의 세밀한 분리보다 `baseline` 비교 기반 dirty 계산이 먼저 들어가 있다.

## Sections

- Basic
- Tags
- Ingredients
- Option Groups
- Nutrition
- Allergens

## Modal

IngredientSelectModal 기존 Figma/React 구현 우선.

현재는 모달 열기/선택/중복 제거 UI만 구현되어 있고, `menusApi.listIngredients`는 아직 없다.

## Save

- 중복 클릭 방지
- 실패 시 draft 유지
- 성공 후 original 갱신

## Current Data Flow

```text
MenuManagePage
→ useMenusQuery
→ menusApi.listMenus / getMenu / listCategories
→ 목록 선택
→ MenuDetailPanel 또는 MenuEditPanel 렌더
```

```text
수정/등록 저장 클릭
→ MenuManagePage.handleSaveEdit()
→ 현재는 로컬 updateMenu 또는 stub toast
→ 실제 POST/PATCH API 연결은 TODO 상태
```

## Current Gaps

- `menusApi.createMenu`, `updateMenu`, `deleteMenu`, `listIngredients` 없음
- 편집 패널의 카테고리/태그/옵션그룹 payload는 UI 기준이며 실제 저장 계약은 아직 미확정
- 이미지 파일 선택 버튼은 비활성 상태
