# ASAK 공부 레포트

## 0. 문서 기본 정보

| 항목 | 내용 |
| --- | --- |
| 공부 주제 | 관리자 메뉴 관리 화면의 목록·상세·편집 패널 흐름 |
| 대상 화면 | `SCR-016` Admin Menu Management |
| 확인 기준일 | `2026-08-06` |
| 확인한 범위 | Frontend / Backend / API 명세 / DB 조회 SQL / Screen Bible / 편집 패널 Mock 흐름 |
| 이 문서의 결론 | 관리자 메뉴 관리 화면은 백엔드 페이지네이션 목록을 기준으로 카드를 렌더링하고, 선택된 `menuId`로 상세 API를 다시 조회해 우측 패널을 채우는 구조이며, 편집 패널은 아직 저장 API 없이 로컬 state와 mock 선택 UI를 중심으로 동작하는 단계다. |

### 한 줄 결론

오늘 확인한 관리자 메뉴 관리 흐름의 핵심은 `목록(PageResult)과 상세(menuId 단건 조회)를 분리`하고, `편집 패널은 별도 form state로 로컬 편집`하며, `옵션 그룹은 내부 policy 이름이 아니라 화면용 그룹 이름으로 표시`하도록 정리하는 것이다.

---

## 1. 목적과 사용자 관점 동작

### 사용자 관점

관리자는 `/menus` 화면에서 카테고리와 검색어로 메뉴를 찾고, 카드 선택 후 우측 패널에서 기본 정보·재료·옵션 그룹·영양·태그를 확인해야 한다.

### 개발 관점

오늘 작업 기준으로 화면은 아래 흐름을 가진다.

1. 목록 진입 시 `GET /api/admin/menus?page=&size=&categoryId=&keyword=` 호출
2. 목록 카드 중 하나를 선택하면 `selectedMenuId`만 변경
3. `selectedMenuId` 변경 후 `GET /api/admin/menus/{menuId}`로 상세 조회
4. 상세 패널에서 옵션 그룹은 `필수/선택`, `1개 선택/최대 N개`, `추천 항목`을 함께 표시
5. 편집 패널에서는 재료/옵션/태그를 로컬 state로 조작한 뒤 `onSave` payload로 모아 전달한다

---

## 2. 학습 범위

- Frontend
  - `ASAK-Admin/src/pages/admin/MenuManagePage.jsx`
  - `ASAK-Admin/src/hooks/useMenusQuery.js`
  - `ASAK-Admin/src/api/menusApi.js`
  - `ASAK-Admin/src/components/admin/MenuListPanel.jsx`
  - `ASAK-Admin/src/components/admin/MenuDetailPanel.jsx`
  - `ASAK-Admin/src/components/admin/MenuEditPanel.jsx`
  - `ASAK-Admin/src/components/admin/IngredientSelectModal.jsx`
  - `ASAK-Admin/src/constants/pagination.js`
  - `ASAK-Admin/src/styles/admin/menu.css`
- Backend
  - `ASAK-back/src/main/java/com/asak/admin/controller/AdminMenuController.java`
  - `ASAK-back/src/main/java/com/asak/admin/service/AdminMenuService.java`
  - `ASAK-back/src/main/resources/mappers/AdminMenuMapper.xml`
  - `ASAK-back/src/main/java/com/asak/admin/dto/response/MenuOptionGroupSummaryResponse.java`
  - `ASAK-back/src/main/java/com/asak/admin/dto/response/MenuDetailResponse.java`
  - `ASAK-back/src/main/java/com/asak/admin/mapper/AdminMenuMapper.java`
- 문서
  - `ASAK/docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-016-ADMIN-MENU-MANAGEMENT.md`
  - `ASAK/docs/wiki/rest-api-spec.md`

---

## 3. 확인 파일과 읽은 이유

| 파일 | 읽은 이유 |
| --- | --- |
| `ASAK-Admin/src/pages/admin/MenuManagePage.jsx` | 화면 진입점, 검색/카테고리/페이지네이션/패널 모드 흐름 확인 |
| `ASAK-Admin/src/hooks/useMenusQuery.js` | 목록 API와 상세 API가 어떻게 분리되는지 확인 |
| `ASAK-Admin/src/api/menusApi.js` | 실제 요청 URL과 `params` 전달 방식 확인 |
| `ASAK-Admin/src/components/admin/MenuListPanel.jsx` | 카드 목록, 검색 submit, 선택 카드 렌더링 확인 |
| `ASAK-Admin/src/components/admin/MenuDetailPanel.jsx` | 옵션 그룹 표시 문구, 필수 우선 정렬, 상세 패널 상태 확인 |
| `ASAK-Admin/src/components/admin/MenuEditPanel.jsx` | 신규/수정 패널의 로컬 form state, 저장 payload, 재료/옵션/태그 조작 흐름 확인 |
| `ASAK-Admin/src/components/admin/IngredientSelectModal.jsx` | 재료 추가가 실제 API가 아닌 mock 카탈로그 기반인지 확인 |
| `ASAK-Admin/src/constants/pagination.js` | 메뉴 목록이 왜 12개 단위로 보이는지 확인 |
| `ASAK-Admin/src/styles/admin/menu.css` | 내부 스크롤 제거와 4열 3행 그리드 레이아웃 근거 확인 |
| `ASAK-back/.../AdminMenuController.java` | `/api/admin/menus`, `/api/admin/menus/{menuId}`, `/categories` 진입점 확인 |
| `ASAK-back/.../AdminMenuService.java` | `PageResult` 조립과 상세 조회 책임 분리 확인 |
| `ASAK-back/.../AdminMenuMapper.xml` | 목록 SQL, 상세 SQL, 옵션 그룹 SQL, 알레르기 SQL 확인 |
| `ASAK-back/.../MenuOptionGroupSummaryResponse.java` | 옵션 그룹 응답 필드 확장 여부 확인 |
| `ASAK-back/.../MenuDetailResponse.java` | 편집/상세 패널이 받는 상세 응답 구조 확인 |
| `ASAK-back/.../AdminMenuMapper.java` | 쓰기용 Mapper가 아직 TODO 상태인지 확인 |
| `ASAK/docs/.../SCR-016-ADMIN-MENU-MANAGEMENT.md` | Route, Figma node, 목적, 상태 요구사항 확인 |
| `ASAK/docs/wiki/rest-api-spec.md` | API-011 관리자 메뉴 목록, API-004 옵션 계약 비교 |

---

## 4. 전체 호출·데이터 흐름 그림

```text
[관리자 /menus 진입]
    ▼
[MenuManagePage]
    ▼
[useMenusQuery.fetchMenus()]
    ▼
[menusApi.listMenus()]
    ▼
GET /api/admin/menus?page&size&categoryId&keyword
    ▼
[AdminMenuController.getMenus]
    ▼
[AdminMenuService.getMenus]
    ▼
[AdminMenuMapper.getMenus + countMenus]
    ▼
[vw_menu_list]
    ▼
PageResult(content, totalElements) 반환
    ▼
[MenuListPanel 카드 렌더링]

[카드 선택]
    ▼
selectedMenuId 변경
    ▼
[useMenusQuery.fetchSelectedMenu()]
    ▼
[menusApi.getMenu(menuId)]
    ▼
GET /api/admin/menus/{menuId}
    ▼
[AdminMenuController.getMenuDetail]
    ▼
[AdminMenuService.getMenuDetail]
    ▼
[AdminMenuMapper.getMenuDetail + 하위 select]
    ▼
menu / menu_nutr / vw_menu_ing_json / vw_menu_opt_policy_json / menu_tag
    ▼
[MenuDetailPanel 렌더링]

[수정 버튼 클릭]
    ▼
panelMode = "edit"
    ▼
[MenuEditPanel useEffect]
    ▼
menu.detail 데이터를 form / ingredients / optionGroups / tags 로 복사
    ▼
[재료 추가 / 옵션 그룹 추가 / 태그 추가]
    ▼
로컬 state 갱신
    ▼
[handleSave()]
    ▼
onSave(payload)
    ▼
현재는 toast + view 전환, 실제 저장 API는 TODO
```

---

## 5. 파일별 복습

### 5-1. 화면 진입점: `MenuManagePage.jsx`

- 역할: `SCR-016` 화면에서 목록 패널과 상세/편집 패널을 조립한다.
- 핵심 상태:
  - `panelMode`: `view | edit | create`
  - `draftKeyword`: 엔터 제출형 검색 입력 상태
  - `deleteConfirmOpen`: 삭제 확인 모달 상태
- 입력 → 처리 → 출력
  - 입력: 카테고리 클릭, 검색어 입력/엔터, 카드 선택
  - 처리: `useMenusQuery`의 `onCategoryIdChange`, `onKeywordChange`, `onSelectMenu`, `onPageChange`
  - 출력: `MenuListPanel`, `MenuDetailPanel`, `MenuEditPanel`
- 초보자 주의점:
  - 검색어는 즉시 API를 치지 않고 `draftKeyword`에 담았다가 엔터로 제출한다.
  - 목록 선택과 상세 데이터는 같은 상태가 아니라 분리된 흐름이다.

### 5-2. 상태/요청 훅: `useMenusQuery.js`

- 역할: 목록 조회, 카테고리 조회, 상세 조회를 관리한다.
- 핵심 함수:
  - `buildListParams()`: `page`, `size`, `categoryId`, `keyword`를 백엔드 계약으로 조립
  - `fetchMenus()`: 목록 PageResult 수신
  - `fetchSelectedMenu()`: 선택된 `menuId`의 상세 재조회
- 상태:
  - `menus`: 현재 페이지 카드 목록
  - `selectedMenuId`: 현재 선택한 메뉴 ID
  - `selectedMenu`: 상세 API 응답
  - `page`, `totalElements`, `categories`, `keyword`, `selectedCategoryId`
- 초보자 주의점:
  - `menusApi.getMenu()`는 `apiClient`가 공통 envelope을 이미 벗긴 객체를 반환한다.
  - 목록과 상세를 한 번에 들고 가지 않고, 상세는 `selectedMenuId`가 바뀔 때 다시 읽는다.

### 5-3. API 모듈: `menusApi.js`

- 역할: 메뉴 목록/상세/카테고리 API 함수를 모은다.
- 사실:
  - `listMenus: (params) => apiClient.get("/admin/menus", { params })`
  - `getMenu: (menuId) => apiClient.get(\`/admin/menus/${menuId}\`)`
- 초보자 주의점:
  - `apiClient.get(url, { params })` 형태여야 쿼리스트링이 붙는다.
  - 이전에 `requestParams`를 그대로 넘기면 Axios 설정 객체로 해석되지 않아 페이지네이션이 틀어질 수 있다.

### 5-4. 목록 패널: `MenuListPanel.jsx`

- 역할: 카테고리 탭, 검색 입력, 카드 그리드, 페이지네이션 슬롯을 렌더링한다.
- 사실:
  - `전체` 탭이 있고, 카테고리 탭은 `categories.map(...)`
  - 검색창은 엔터 시 `onKeywordSubmit?.()` 호출
  - 카드 선택은 `onSelectMenu(menu.menuId)`
- 초보자 주의점:
  - `menus === null` 분기는 비어 있지만, 실제 훅은 빈 배열을 주로 사용한다.
  - 카드 강조는 `selectedMenuId`와 목록 아이템의 `menuId` 비교로 결정된다.

### 5-5. 상세 패널: `MenuDetailPanel.jsx`

- 역할: 기본 정보, 재료, 옵션 그룹, 영양 정보, 알레르기, 태그를 표시한다.
- 오늘 확인한 핵심:
  - `formatOptionRule(group)`로 `필수 · 1개 선택`, `선택 · 최대 5개` 같은 문구를 만든다.
  - `sortedOptionGroups`에서 `isRequired`가 `true`인 그룹을 위로 올린다.
- 초보자 주의점:
  - 옵션 그룹은 단순한 문자열 리스트가 아니라 `name`, `isRequired`, `selectType`, `maxSelect`, `recommendedLabel`까지 가진 구조다.
  - 옵션 그룹 정렬은 렌더링 직전에 복사 배열을 정렬해야 원본 state를 건드리지 않는다.

### 5-6. 편집 패널: `MenuEditPanel.jsx`

- 역할: 신규/수정 공용 편집 카드로, 상세 응답을 form 편집용 state로 복사한다.
- props:
  - `mode`
  - `menu`
  - `categoryOptions`
  - `optionGroupCatalog`
  - `onCancel`, `onSave`, `onDelete`
- 핵심 상태:
  - `form`
  - `ingredients`
  - `optionGroups`
  - `nutrition`
  - `allergens`
  - `tags`
  - `baseline`
  - `ingredientModalOpen`, `tagPickerOpen`, `optionGroupPickerOpen`
- 핵심 함수:
  - `normalizeOptionGroups()`: 필수 그룹만 추천 옵션 1개를 정리
  - `handleAddIngredients()`: 중복 ID/이름을 막고 재료를 추가
  - `selectRecommendedOption()`: 필수 옵션 그룹의 추천 항목을 1개로 유지
  - `handleSave()`: 현재 편집 상태를 하나의 payload로 모아 상위로 전달
- 입력 → 처리 → 출력
  - 입력: 메뉴명/가격/설명/판매상태 변경, 재료 추가/삭제, 옵션 그룹 추가/삭제, 추천 옵션 변경, 태그 추가/삭제
  - 처리: 모두 컴포넌트 내부 state 갱신
  - 출력: `onSave(payload)` 호출
- 초보자 주의점:
  - 지금은 저장 버튼이 실제 API를 치지 않고 상위 `onSave`로만 전달된다.
  - `dirtyCount`는 사실상 0 또는 1로 동작하는 변경 여부 플래그에 가깝다.
  - `categoryName`을 `select value`로 쓰고 있어, 나중에 실제 저장 API 계약이 `categoryId` 중심이면 변환 로직이 필요하다.

### 5-7. 재료 선택 모달: `IngredientSelectModal.jsx`

- 역할: 메뉴 편집 화면의 `+ 재료 추가` 모달이다.
- 사실:
  - 기본 `catalog`는 `MOCK_INGREDIENT_CATALOG`
  - 카테고리 필터와 키워드 검색을 클라이언트에서 처리
  - 이미 추가된 재료는 `alreadyAdded`로 비활성화
  - `selectedIds`를 `Set`으로 관리해 다중 선택
- 초보자 주의점:
  - 이 모달은 아직 실제 서버 검색이 아니라 mock 기반이다.
  - 같은 재료를 `ingredientId`와 `name` 두 축으로 중복 방지한다.

### 5-8. 화면 설정 파일: `pagination.js`, `menu.css`

- `pagination.js`
  - `SCR-016` 메뉴 목록은 `pageSize: 12`
  - 주석상 의도는 `4열 × 3행 카드 그리드`
- `menu.css`
  - `.menu-management__grid`는 `overflow: visible`
  - 상세 패널 안쪽만 `overflow-y: auto`
- 해석:
  - 목록 내부 스크롤을 없애고, 페이지 단위로 카드 수를 고정하려는 설계다.

### 5-9. 백엔드 Controller/Service

- `AdminMenuController.getMenus`
  - `@ModelAttribute MenuListRequest`로 쿼리파라미터 바인딩
  - `ApiResponse<PageResult<MenuListResponse>>` 반환
- `AdminMenuController.getMenuDetail`
  - `menuId` 단건 상세 조회
  - 없으면 `MENU_NOT_FOUND`
- `AdminMenuService.getMenus`
  - `adminMenuMapper.getMenus(request)`
  - `adminMenuMapper.countMenus(request)`
  - `new PageResult<>(content, request.getPage(), request.getSize(), totalElements)`

### 5-10. Mapper/SQL

- 목록 SQL:
  - `vw_menu_list` 기반
  - `categoryId`, `keyword`, `isSoldOut`, `tagId` 필터
  - `LIMIT #{request.size} OFFSET #{request.offset}`
- 상세 SQL:
  - `menu`, `category` join
  - 재료: `vw_menu_ing_json`
  - 옵션 그룹: `vw_menu_opt_policy_json`
  - 알레르기: 재료 + 옵션을 `UNION`
- 옵션 그룹 응답:
  - `MenuOptionGroupSummaryResponse`에 `groupType`, `selectType`, `minSelect`, `maxSelect` 필드가 추가됐다.

---

## 6. 화면 상태

### Default

확인됨. `MenuManagePage`가 `MenuListPanel`과 `MenuDetailPanel`을 동시에 렌더링한다.

### Loading

확인됨. `status === "loading"`이면 `AdminAsyncState`의 `loadingVariant="card"`를 사용한다.

### Empty

부분 확인. `MenuListPanel`은 빈 목록 시 `"조건에 맞는 메뉴가 없습니다"`를 표시한다. 다만 `menus === null` 분기를 쓰고 있어 빈 배열 중심 구조와 완전히 일치하지는 않는다. `MenuEditPanel`은 비어 있는 재료/옵션/태그에 대해 각 섹션별 empty 문구를 둔다.

### Error

부분 확인. `useMenusQuery`는 `status = "error"`와 `error`를 설정한다. 하지만 `MenuManagePage`의 별도 error 전용 렌더링은 오늘 읽은 범위에서 명시적이지 않았다.

### Disabled

부분 확인. `MenuEditPanel`은 이미지 업로드 버튼과 영양 재계산 버튼이 disabled 상태이고, 옵션 그룹 추가 버튼은 더 이상 추가할 그룹이 없으면 disabled 된다. 저장 중 pending 제어는 아직 없다.

### Figma / Screen Bible

- Screen ID: `SCR-016`
- Route: `/menus`
- Figma node: Default `134:12137`, Add `134:12328`, Edit `134:12668`, Saving `241:17178`, Error `241:17719`
- 사실:
  - 문서에는 `default`, `detailAdd`, `detailEdit`, `saving`, `error` 상태가 요구된다.
  - 코드에는 기본/로딩/빈목록이 비교적 뚜렷하지만, 저장/실패는 TODO가 남아 있다.

---

## 7. 데이터 필드와 Mock·API·DB·명세의 검증 상태

| 항목 | 현재 확인 상태 | 근거 |
| --- | --- | --- |
| 목록 API PageResult(`content`, `totalElements`) | 확인됨 | `useMenusQuery.js`, `AdminMenuService.java` |
| 목록 쿼리 `page/size/categoryId/keyword` | 확인됨 | `menusApi.js`, `MenuListRequest`, `AdminMenuMapper.xml` |
| 상세 API `GET /api/admin/menus/{menuId}` | 확인됨 | `AdminMenuController.java`, `useMenusQuery.js` |
| 옵션 그룹 표시 이름 | 정리 중 | `vw_menu_opt_policy_json`를 화면용 이름으로 개선 논의 |
| 옵션 그룹 선택 규칙(`SINGLE/MULTI`, min/max) | 확인됨(응답/프론트) | `AdminMenuMapper.xml`, `MenuOptionGroupSummaryResponse.java`, `MenuDetailPanel.jsx` |
| 편집 payload 구조(`form + ingredients + optionGroups + nutrition + allergens + tags`) | 확인됨(프론트 로컬) | `MenuEditPanel.jsx` |
| 재료 검색 API 연결 | 미구현 | `IngredientSelectModal.jsx`, `menusApi.js`, `AdminMenuMapper.java` TODO |
| 메뉴 등록/수정/삭제 실제 저장 | 미구현 | `MenuManagePage.jsx`, `menusApi.js`, `AdminMenuController.java` TODO |
| 이미지 경로 `/assets/menu/{id}.png` | 확인됨 | `rest-api-spec.md`, 실제 화면 변경 이력 |
| DB 직접 조회 재검증 | 오늘 문서 범위에서는 미실행 | SQL/매퍼 기준으로만 확인 |

---

## 8. 확인한 사실

- 목록은 백엔드 페이지네이션 응답을 그대로 사용한다.
- 상세 패널은 목록 데이터가 아니라 선택한 `menuId`의 상세 API 응답으로 채운다.
- 검색은 엔터 제출형으로 바뀌었다.
- 옵션 그룹은 `필수/선택`, `1개 선택/최대 N개`, `추천 항목`을 함께 표시한다.
- 옵션 그룹 카드 정렬은 프론트에서 `isRequired` 기준으로 필수 우선 정렬한다.
- `AdminMenuMapper.xml`은 옵션 그룹을 `vw_menu_opt_policy_json`에서 읽는다.
- 편집 패널은 상세 응답을 로컬 편집 state로 펼쳐 놓고 저장 payload를 다시 조립한다.
- 재료 추가 모달은 아직 실제 API가 아니라 mock 카탈로그를 사용한다.
- 메뉴 목록은 12개 고정 페이지와 내부 스크롤 제거 CSS를 같이 써서 4열 3행 화면을 유지하려고 한다.

---

## 9. 코드 근거에 따른 해석

- 목록과 상세를 분리한 구조는, 목록 카드가 가벼운 요약 응답을 받고 우측 패널만 필요할 때 상세를 다시 읽게 하려는 의도다.
- 옵션 그룹을 DTO로 확장한 것은 UI에서 단순 추천값만이 아니라 선택 규칙까지 설명하기 위해서다.
- `policy 5` 같은 내부 이름이 화면에 노출된 문제는 프론트보다 `vw_menu_opt_policy_json`의 표시용 이름 정리가 더 근본 해결책이다.
- 현재 `MenuManagePage`의 create/edit/delete는 stub이므로, 문서상 목적은 “관리”이지만 구현 현실은 “조회 중심 + 저장 TODO 남음” 상태다.
- `MenuEditPanel`은 실제 서버 저장 전 단계의 프로토타입 성격이 강하고, 사용자가 바꾸는 거의 모든 값이 아직 프론트 로컬 state에서만 순환한다.
- 재료 검색과 이미지 업로드가 stub인 점을 보면, 편집 화면은 UI 구조와 payload 모양을 먼저 굳히는 중이라고 해석할 수 있다.

---

## 10. 미확인 또는 TODO

- `vw_menu_opt_policy_json` 실제 최종 DDL이 현재 DB에 어떻게 반영됐는지 미확인
- `MenuManagePage`의 `error` 화면 분기 보완 여부 미확인
- 메뉴 등록/수정/삭제 실제 API 연동 미구현
- 재료 검색용 실제 endpoint, request param, response DTO 미정
- `MenuEditPanel`의 `categoryName` 기반 select가 최종 저장 계약과 일치하는지 미확인
- `optionGroupCatalog`가 현재 상세 API 구조에서 실질적으로 얼마나 쓰이는지 추가 확인 필요
- 카테고리 API DTO(`CategoryResponse` vs `AdminCategoryResponse`) 정합 최종 상태 미확인

---

## 11. 검증 기록

| 항목 | 결과 | 메모 |
| --- | --- | --- |
| 프론트 build | 확인됨 | `ASAK-Admin`에서 `npm run build` 성공 |
| 백엔드 test | 확인됨 | `ASAK-back`에서 `.\gradlew.bat test` 성공 |
| lint | 부분 확인 | 최근 수정 파일 `ReadLints` 기준 에러 없음 |
| 브라우저 | 부분 확인 | 화면 스크린샷으로 옵션 그룹 UI와 메뉴 카드 동작 확인 |
| API | 확인됨 | `AdminMenuController`, `menusApi`, `useMenusQuery` 흐름 대조 |
| DB | 부분 확인 | 실제 SQL/뷰 정의와 매퍼 기준 확인, 오늘 이 문서 작성 중 직접 조회는 미실행 |

---

## 12. 직접 해 볼 확인 항목

1. `/menus` 화면에서 검색어를 입력하고 Enter를 눌렀을 때만 목록 API가 다시 호출되는지 Network에서 확인한다.
2. 페이지네이션 1 → 2 → 3으로 이동할 때 `GET /api/admin/menus?page=` 값이 바뀌는지 확인한다.
3. 다른 메뉴 카드를 눌렀을 때 `GET /api/admin/menus/{menuId}`가 다시 호출되는지 확인한다.
4. 옵션 그룹 카드에서 `필수` 배지가 붙은 항목이 항상 위쪽에 오는지 확인한다.
5. `policy 5` 같은 내부 이름이 사라지고 그룹명만 보이는지 뷰 수정 후 재확인한다.
6. 편집 패널에서 재료를 추가한 뒤 저장 버튼을 눌렀을 때 상위로 전달되는 payload shape를 콘솔로 확인한다.

---

## 13. 연습문제

1. `useMenusQuery`에서 목록 API와 상세 API를 왜 분리했는지 자신의 말로 설명해 본다.
2. `apiClient`가 envelope을 벗기기 때문에 `menusApi.getMenu()` 호출 결과에서 `response.data`를 쓰면 왜 문제가 되는지 적어 본다.
3. `MenuDetailPanel`의 옵션 그룹 카드에 `groupType`을 추가로 보여주려면 백엔드와 프론트 중 어느 쪽을 먼저 읽어야 하는지 순서를 적어 본다.
4. `vw_menu_list`와 `vw_menu_opt_policy_json`이 각각 어떤 화면 책임을 가지는지 비교해 본다.
5. 메뉴 등록 기능을 실제로 붙이려면 `Page → Hook → API → Controller → Service → Mapper` 순서로 무엇을 먼저 구현해야 하는지 적어 본다.
6. `MenuEditPanel`이 `baseline`과 `dirtyCount`를 쓰는 이유를 "폼 변경 감지" 관점에서 설명해 본다.

---

## 14. 다음에 읽을 파일 최대 3개

1. `ASAK-Admin/src/components/admin/AdminConfirmDialog.jsx`
2. `ASAK-back/src/main/java/com/asak/admin/dto/request/MenuListRequest.java`
3. `ASAK/docs/wiki/db-view-definition.md`
