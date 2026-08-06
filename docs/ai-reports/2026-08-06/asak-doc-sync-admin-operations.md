# ASAK Admin 운영 문서 동기화 근거 보고서

- 기준 시점: **2026-08-06**
- Git 자동 commit/push/merge: **하지 않음**
- 범위: 관리자 `메뉴 관리`, `품절 관리`, `결제수단 설정` 관련 로컬 문서만 갱신

## 1. 대상 저장소와 기준 커밋

| 저장소 | 기준 커밋 | 비고 |
| --- | --- | --- |
| `ASAK-Admin` | `bf72b3c` | 메뉴/품절/결제수단 프론트 작업 트리 변경 존재 |
| `ASAK-back` | `a09faa6` | 메뉴 조회 구현, 품절/결제수단 스텁 상태 |
| `ASAK` | `bd2e675` | 문서 저장소 |

## 2. 확인한 코드와 문서

### 코드

- `ASAK-Admin/src/api/menusApi.js`
- `ASAK-Admin/src/pages/admin/MenuManagePage.jsx`
- `ASAK-Admin/src/components/admin/MenuListPanel.jsx`
- `ASAK-Admin/src/components/admin/MenuDetailPanel.jsx`
- `ASAK-Admin/src/components/admin/MenuEditPanel.jsx`
- `ASAK-Admin/src/hooks/useMenusQuery.js`
- `ASAK-Admin/src/api/soldOutApi.js`
- `ASAK-Admin/src/hooks/useSoldOutDraft.js`
- `ASAK-Admin/src/pages/admin/SoldOutManagePage.jsx`
- `ASAK-Admin/src/api/paymentMethodsApi.js`
- `ASAK-Admin/src/hooks/usePaymentMethodDraft.js`
- `ASAK-Admin/src/pages/admin/PaymentMethodPage.jsx`
- `ASAK-back/src/main/java/com/asak/admin/controller/AdminMenuController.java`
- `ASAK-back/src/main/java/com/asak/admin/service/AdminMenuService.java`
- `ASAK-back/src/main/java/com/asak/admin/mapper/AdminMenuMapper.java`
- `ASAK-back/src/main/resources/mappers/AdminMenuMapper.xml`
- `ASAK-back/src/main/java/com/asak/admin/controller/AdminSoldOutController.java`
- `ASAK-back/src/main/java/com/asak/admin/controller/AdminPaymentMethodController.java`
- `ASAK-back/src/main/resources/mappers/AdminSoldOutMapper.xml`
- `ASAK-back/src/main/resources/mappers/AdminPaymentMethodMapper.xml`

### 문서

- `docs/product_bible/03_Menu_Inventory_SoldOut/docs/09-features/menu-management/MENU_MANAGEMENT_API_CONTRACT.md`
- `docs/product_bible/12_Frontend_Implementation/docs/13-frontend-implementation/04-admin/MENU_MANAGEMENT_IMPLEMENTATION.md`
- `docs/product_bible/11_Backend_Implementation/docs/12-backend-implementation/02-menu/MENU_MANAGEMENT_IMPLEMENTATION.md`
- `docs/product_bible/12_Frontend_Implementation/docs/13-frontend-implementation/04-admin/SOLD_OUT_IMPLEMENTATION.md`
- `docs/product_bible/11_Backend_Implementation/docs/12-backend-implementation/05-admin/SOLD_OUT_IMPLEMENTATION.md`
- `docs/product_bible/11_Backend_Implementation/docs/12-backend-implementation/04-payment/PAYMENT_METHOD_IMPLEMENTATION.md`

## 3. 갱신한 문서

| 문서 | 변경 내용 | 상태 |
| --- | --- | --- |
| `MENU_MANAGEMENT_API_CONTRACT.md` | 실제 구현된 `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`를 추가하고, Create/Update/Delete/Ingredient Search를 Draft/미구현으로 분리 | 반영 완료 |
| `MENU_MANAGEMENT_IMPLEMENTATION.md` (FE) | 실제 화면 조합, 조회 API 연결, 저장 stub 상태, 미연결 기능을 코드 기준으로 명시 | 반영 완료 |
| `MENU_MANAGEMENT_IMPLEMENTATION.md` (BE) | 현재 구현된 조회 경로와 SQL 출처, 미구현 write endpoint, 결정 필요 항목을 명시 | 반영 완료 |
| `SOLD_OUT_IMPLEMENTATION.md` (FE) | mock 기반 draft 훅 구조, 좌우 패널 흐름, 탭 값, API 미연결 상태를 명시 | 반영 완료 |
| `SOLD_OUT_IMPLEMENTATION.md` (BE) | Controller/Service/Mapper 스텁 상태와 결정 필요 항목을 명시 | 반영 완료 |
| `PAYMENT_METHOD_IMPLEMENTATION.md` | backend 스텁 상태, 프론트 mock 연동 상태, 결정 필요 항목을 명시 | 반영 완료 |

## 4. 변경 근거

### 메뉴 관리

- 백엔드는 `AdminMenuController`에서 `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`만 실제 구현되어 있다.
- 프론트는 `menusApi.listMenus`, `getMenu`, `listCategories`를 실제 호출한다.
- `createMenu`, `updateMenu`, `deleteMenu`, `listIngredients`는 프론트 API 함수가 없고, 백엔드도 TODO만 존재한다.
- 메뉴 상세 응답은 `MenuDetailResponse` 기준으로 `menuId`, `categoryId`, `categoryName`, `name`, `price`, `imageUrl`, `description`, `isSoldOut`, `ingredients`, `optionGroups`, `nutrition`, `allergens`, `tags`를 반환한다.

### 품절 관리

- 프론트는 `useSoldOutDraft`에서 `getSoldOutCatalog`, `saveSoldOutCatalog` mock 저장소를 사용한다.
- 백엔드는 `AdminSoldOutController`, `AdminSoldOutService`, `AdminSoldOutMapper.xml`이 모두 스텁 상태다.
- 따라서 품절 관련 문서는 “현재 서버 구현”이 아니라 “현재 화면 mock 동작”과 “서버 구현 목표”를 구분해서 적어야 했다.

### 결제수단 설정

- 프론트는 `usePaymentMethodDraft`에서 mock 저장소를 사용하며, 현재 저장 대상은 사실상 `methodId`, `isActive`, `sortOrder` 중심이다.
- 백엔드는 `AdminPaymentMethodController`, `AdminPaymentMethodService`, `AdminPaymentMethodMapper.xml`이 모두 스텁 상태다.

## 5. 실행 또는 검증 결과

| 항목 | 결과 |
| --- | --- |
| 코드 읽기 대조 | 수행 |
| `git diff --check` | 수행 예정, 아래 8절 기록 |
| 프론트 런타임 확인 | 미실행 |
| 백엔드 HTTP 호출 확인 | 미실행 |
| DB 조회 검증 | 미실행 |

실행하지 않은 항목은 통과로 기록하지 않는다.

## 6. 남은 불일치

1. `MenuEditPanel`은 편집 초기값을 `menu.detail?.description`, `menu.detail?.ingredients` 등에서 읽지만, 현재 `menusApi.getMenu()`가 받는 `MenuDetailResponse`는 top-level 필드 구조다. 문서에는 이 점을 **구현 불일치**로 남기고 코드 정답처럼 덮어쓰지 않았다.
2. `MenuDetailResponse.tags`는 `List<String>`인데, 프론트 `MenuDetailPanel`/`MenuEditPanel`은 `tag.code`, `tag.name` 형태도 함께 가정한다. 실제 어댑터 또는 응답 변경 여부 확인이 필요하다.
3. 품절 관리 설계 문서는 `OPTION_ITEM`을 쓰지만, 프론트 탭 값은 `OPTION`이다. API 계약 확정이 필요하다.
4. 결제수단 경로는 현재 코드가 `/api/admin/paymentMethods` camelCase다. kebab-case로 바꿀지 결정이 필요하다.

## 7. 결정 필요 사항

- 메뉴 등록/수정 요청 형식: JSON vs multipart
- 메뉴 삭제 정책: soft delete vs hard delete
- 재료 검색 endpoint와 응답 shape
- 품절 PATCH body를 `targetType/targetId/isSoldOut`로 확정할지 여부
- 결제수단 저장 방식: 개별 PATCH vs 일괄 저장

## 8. 수정하지 않은 범위

- Screen Bible 본문: 기획/디자인 의도 문서라 구현 사실만으로 조용히 바꾸지 않음
- 소스코드
- DB, Figma, 원격 문서
- 테스트/QA PASS 상태
