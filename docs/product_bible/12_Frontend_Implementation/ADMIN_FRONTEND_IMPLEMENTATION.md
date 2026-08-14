# Admin Frontend Implementation

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ADMIN_ROUTE_IMPLEMENTATION.md`
- `DASHBOARD_IMPLEMENTATION.md`
- `LIVE_ORDER_TTS_IMPLEMENTATION.md`
- `MENU_MANAGEMENT_IMPLEMENTATION.md`
- `ORDER_MANAGEMENT_IMPLEMENTATION.md`
- `SALES_IMPLEMENTATION.md`
- `SOLD_OUT_IMPLEMENTATION.md`

---

## 원문: `ADMIN_ROUTE_IMPLEMENTATION.md`

### Admin Route Implementation

#### Routes

```text
/login
/
/orders/live
/orders
/soldOut
/menus
/paymentMethods
/sales
/sales/monthly
/sales/daily
```

#### Login Success

Dashboard `/`.

#### Layout

- Navbar/Sidebar
- Main content
- route outlet

기존 Admin layout이 있으면 우선 재사용.

---

## 원문: `DASHBOARD_IMPLEMENTATION.md`

### Dashboard Implementation

#### Components

- SalesMetricCard
- ActiveOrderSummary
- PopularMenuList
- SoldOutSummary

#### API

```text
GET dashboard
```

#### State

```text
loading
error
data
isRefreshing
```

#### Partial Error

API가 분리된 경우 widget별 error.
Aggregate API면 전체 상태 우선.

#### 고객 수

Dashboard에서는 주문 수와 중복될 수 있으므로 기본 KPI는:

- 순매출
- 주문 수
- 객단가
- 진행 주문

---

## 원문: `LIVE_ORDER_TTS_IMPLEMENTATION.md`

### Live Order and TTS Implementation

#### Polling

- 5초
- 중복 요청 방지
- unmount cleanup
- stale response 방지

#### 상태 변경

```text
button loading
→ PATCH
→ success UI
→ Toast
→ TTS
```

#### TTS

- API 성공 후
- same orderNo 10초 block
- mute localStorage
- queue 유지

#### 금지

렌더링 또는 polling response만으로 발화하지 않는다.

---

## 원문: `MENU_MANAGEMENT_IMPLEMENTATION.md`

### Menu Management Frontend Implementation

#### Current Code Status (2026-08-06)

- `useMenusQuery`가 `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`를 실제 호출한다.
- 화면 조합은 `MenuManagePage` + `MenuListPanel` + `MenuDetailPanel` + `MenuEditPanel` 구조다.
- `view / edit / create` 패널 모드는 구현되어 있다.
- `create`, `update`, `delete` 저장은 아직 API 미연결이며 현재 화면에서 stub toast만 호출한다.
- `IngredientSelectModal` 자동완성과 이미지 업로드는 아직 미연결이다.

#### Shared Form

Add/Edit는 동일 Form.

State:

```text
original
draft
dirtyFields
validationErrors
```

현재 코드에는 `dirtyFields`, `validationErrors`의 세밀한 분리보다 `baseline` 비교 기반 dirty 계산이 먼저 들어가 있다.

#### Sections

- Basic
- Tags
- Ingredients
- Option Groups
- Nutrition
- Allergens

#### Modal

IngredientSelectModal 기존 Figma/React 구현 우선.

현재는 모달 열기/선택/중복 제거 UI만 구현되어 있고, `menusApi.listIngredients`는 아직 없다.

#### Save

- 중복 클릭 방지
- 실패 시 draft 유지
- 성공 후 original 갱신

#### Current Data Flow

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

#### Current Gaps

- `menusApi.createMenu`, `updateMenu`, `deleteMenu`, `listIngredients` 없음
- 편집 패널의 카테고리/태그/옵션그룹 payload는 UI 기준이며 실제 저장 계약은 아직 미확정
- 이미지 파일 선택 버튼은 비활성 상태

---

## 원문: `ORDER_MANAGEMENT_IMPLEMENTATION.md`

### Order Management Implementation

#### 구성

- FilterBar
- DatePicker
- SearchInput
- OrderTable
- Pagination
- OrderDetailPanel

#### Filter State

가능하면 URL query와 동기화 검토.

```text
status
orderType
startDate
endDate
keyword
page
```

#### 역할

SCR-009 Live Board와 분리한다.

---

## 원문: `SALES_IMPLEMENTATION.md`

### Sales Frontend Implementation

#### Mock Data

현재 모든 매출 데이터는 Portfolio Demo Data로 구현 가능.

#### 공식 정의

```text
고객 수 = 결제 승인 건수
평균 객단가 = 총매출 / 고객 수
```

#### 화면

- Summary
- Monthly
- Daily

#### 정합성

- KPI = chart/table 합계
- 비율 100%
- 날짜 중복 없음
- comparison 계산 일치

#### Date Components

기존 DateRangePicker/DatePicker를 재사용.

---

## 원문: `SOLD_OUT_IMPLEMENTATION.md`

### Sold-out Frontend Implementation

#### Current Code Status (2026-08-06)

- 화면은 `SoldOutManagePage` + `useSoldOutDraft`로 동작한다.
- 초기 로드와 저장은 아직 `adminMockRepository`를 사용한다.
- `soldOutApi.listSoldOutCatalog`, `soldOutApi.patchSoldOut`는 아직 없다.
- 좌측 판매 항목 / 우측 품절 항목 2패널, 탭, 검색, 카테고리, 페이지네이션, 저장 확인 다이얼로그까지는 구현되어 있다.

#### Draft

```js
{
  changes: []
}
```

현재 구현은 단순 `changes[]`보다 아래 상태를 함께 들고 있다.

```text
available
soldOut
selectedAvailable
selectedSoldOut
dirtyCount
baselineAvailable
baselineSoldOut
```

#### 흐름

```text
toggle
→ dirty change
→ affected count
→ SaveBar
→ ConfirmDialog
→ PATCH
→ Toast
```

현재 코드 기준 실제 흐름:

```text
mock getSoldOutCatalog()
→ available / soldOut 로드
→ 카드 선택 후 → / ← 이동
→ dirtyCount 계산
→ 저장 확인
→ mock saveSoldOutCatalog()
→ 성공 시 baseline 갱신 / 실패 시 baseline 롤백
```

#### 위계

- Menu / Ingredient / Option = Tabs
- Category = Chips

현재 탭 값은 `MENU`, `INGREDIENT`, `OPTION`이다.

#### 기존 컴포넌트

Admin/Toast, ConfirmDialog, Filter components를 재사용.

#### Current Gaps

- 실제 API 미연결
- Error 상태 분기는 저장 toast 외에는 제한적이며, 초기 load 실패 처리도 mock 기준
- 영향 메뉴 수(`affectedMenus`)는 현재 코드에 없다
