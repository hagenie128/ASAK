> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Dated MCP review evidence.
> Canonical Replacement: `docs/design/figma-guide.md`
> Original Path: `docs/design/ASAK_FIGMA_MCP_REVIEW_2026-07-14.md`

# ASAK Figma MCP 점검 및 보완 목록

> 점검일: 2026-07-14  
> 대상: [ASAK Figma 파일](https://www.figma.com/design/o9mxSeovLQPdWNwM4mNySk/ASAK?node-id=324-2755)  
> 목적: React 프론트엔드로의 디자인 반영 및 향후 Code Connect 매핑 준비

## 결론

현재 파일은 키오스크 주문 흐름, 관리자 화면, 공통 컴포넌트를 갖추고 있어 구현을 시작할 수 있다. 특히 키오스크는 홈(`k001`)부터 주문 완료(`k007`), 결제 실패/타임아웃까지 준비되어 있다.

다만 Figma MCP/Code Connect로 안정적으로 코드를 가져오려면 다음 세 가지를 먼저 정리해야 한다.

1. 화면 프레임 이름을 `k001`, `A-001`에서 **SCR·라우트·화면 역할이 드러나는 이름**으로 바꾼다.
2. `Property 1`, `Variant2`, `Frame 1707479439` 같은 자동 이름을 **의미 있는 Variant/레이어 이름**으로 바꾼다.
3. 프론트엔드에 있는 화면(`AccessibilityPage`, 관리자 로그인·메뉴·결제수단 등)과 Figma 화면을 **1:1 매트릭스**로 연결한다.

## 파일 현황

| Figma 페이지 | 확인 결과 | 판단 |
| --- | --- | --- |
| `🎨 00. 디자인 시스템` | Palette 67개, Semantic 11개 변수와 텍스트/효과/그리드 스타일이 존재 | 토큰 기반 구현 가능. 명명 정리 필요 |
| `🧩 01. 컴포넌트` | Kiosk, Admin, Shared 영역 및 키오스크/관리자 컴포넌트 존재 | 주요 자산은 충분하나 Variant 명명 불균일 |
| `🔀 03. User Flow` | 비어 있음 | 실제 클릭 흐름/예외 분기 문서화 필요 |
| `📱 04. 고객 키오스크 와이어프레임` | `k001`~`k007`, 결제 실패·타임아웃 포함 | 화면명/상태/접근성 화면 보강 필요 |
| `💻 05. 관리자 웹 와이어프레임` | `A-001`~`A-007`, 매출 일/월/요약 포함 | 화면-기능 매핑과 로그인/관리 화면 확인 필요 |
| `🖼️ 06. Hi-fi 디자인` | 비어 있음 | 현재 와이어프레임을 구현 기준으로 사용할지 결정 필요 |

## 화면별 보완 사항

### 키오스크

| 현재 프레임 | 권장 이름 | 코드 화면 | 상태 / 보완 |
| --- | --- | --- | --- |
| `k001` | `SCR-001 / Kiosk / Home` | `HomePage` | 매장/포장 선택의 선택/비활성/재진입 상태를 명시 |
| `k002` | `SCR-003 / Kiosk / Menu List` | `MenuListPage` | 메뉴 카드의 `soldOut`, `recommended`, 이미지 없음, 가격/칼로리 등의 상태를 Variant로 분리 |
| `k003` | `SCR-004 / Kiosk / Menu Detail` | `MenuDetailPage` | 필수 옵션 미선택, 최대 선택 수 도달, 옵션 품절, 알레르기 경고, 추가 금액 갱신 상태 필요 |
| `k004` | `SCR-005 / Kiosk / Cart` | `CartPage` | 빈 장바구니, 삭제 확인, 수량 최소/최대, 주문 확인 모달 상태 필요 |
| `k005 (접힘)` | `SCR-007 / Kiosk / Payment / Summary=Collapsed` | `PaymentPage` | 선택된 결제수단, 비활성 수단, 결제 버튼 로딩을 명확히 분리 |
| `k005 (펼침)` | `SCR-007 / Kiosk / Payment / Summary=Expanded` | `PaymentPage` | 위 프레임의 Variant 또는 프로토타입 상태로 연결 |
| `k006` | `SCR-007 / Kiosk / Payment Processing` | `PaymentPage` | 카드 투입/승인 대기/취소 가능 여부와 진행 시간 명시 |
| `k006/ 결제 실패` | `SCR-012 / Kiosk / Payment / Error` | `PaymentPage` | 오류 코드, 재시도/장바구니 복귀 액션, 금액 불일치 문구 추가 |
| `k006/ 타임아웃` | `SCR-013 / Kiosk / Timeout Modal` | `useKioskTimeout` | 남은 초, 계속 주문/처음으로 버튼, 자동 초기화 결과를 명시 |
| `k007` | `SCR-008 / Kiosk / Order Complete` | `OrderCompletePage` | `orderNo`, `paidAt`, `paymentStatus`, 영수증 선택/출력 실패 상태 필요 |

**누락 또는 확인 필요:** 코드에 있는 `AccessibilityPage`에 해당하는 `SCR-014 / Kiosk / Accessibility` 프레임을 활성 화면 영역에 추가해야 한다. 글자 크기, 고대비, 적용/되돌리기 상태가 필요하다.

### 관리자

현재 `A-001`~`A-007` 프레임은 존재하지만 프레임 이름만으로 `LoginPage`, `OrderListPage` 등의 대응을 확정하기 어렵다. 아래 이름으로 정리하고 각 프레임의 우측 상단에 SCR/라우트/데이터 상태를 메모로 남긴다.

| 권장 이름 | 코드 화면 | 필수 상태 |
| --- | --- | --- |
| `SCR-015 / Admin / Login` | `LoginPage` | 기본, 입력 오류, 로그인 진행, 권한 없음 |
| `SCR-009 / Admin / Order List` | `OrderListPage` | 전체/상태 필터, 검색, 로딩, 빈 목록, 오류, 페이지네이션 |
| `SCR-010 / Admin / Order Detail` | `OrderDetailPage` | 주문 상태별 액션, 변경 확인, 변경 실패, 옵션/제외 재료 표시 |
| `SCR-011 / Admin / Sold-out Management` | `SoldOutManagePage` | 메뉴/재료 구분, 토글 진행/성공/실패, 품절 사유 |
| `SCR-016 / Admin / Menu Management` | `MenuManagePage` | 검색/필터, 품절, 빈 목록, 등록 진입 |
| `SCR-017 / Admin / Menu Edit` | `MenuEditPage` | 등록/수정, 필수값 오류, 이미지 없음/업로드, 저장/취소/실패 |
| `SCR-018 / Admin / Payment Methods` | `PaymentMethodPage` | 활성/비활성, 순서 변경, 저장 진행/실패 |
| `SCR-019 / Admin / Sales Summary` | `SalesSummaryPage` | 일/월 기간 선택, 데이터 없음, 로딩, API 오류, 차트 범례 |

관리자 페이지에는 `A-006 sales-summary`, `A-006 monthly-sales`, `A-006 daily-sales`가 있으므로, 이를 하나의 `SalesSummaryPage`의 기간/집계 Variant로 정의하는 편이 구현과 일치한다.

## 컴포넌트 정리 우선순위

### 1. 이름과 Variant 이름 수정 (최우선)

다음 컴포넌트는 이미 존재하지만 코드 매핑용 이름으로 정리해야 한다.

| 현재 | 변경 권장 | 이유 |
| --- | --- | --- |
| `MenuCard`와 `Menu Card` | `MenuCard` 하나로 통합 | 동일 역할의 중복 명칭 제거 |
| `Property 1=Default`, `Variant2` | `state=default`, `state=selected` 등 | 프로퍼티의 의미를 코드 props로 바로 연결 |
| `OrderDetailRow / Property 1=Normal` | `OrderDetailRow / state=default` | `normal`, `press`, `error`, `disabled`를 일관되게 표현 |
| `HomeActionButton / Property 1=...` | `OrderTypeButton / type=eatIn|takeOut, state=default|selected` | 주문 유형 데이터와 직접 연결 |
| `menu btn`, `orderMenuOptionList` | `Admin/MenuActionButton`, `Admin/OrderOptionList` | 공통 라이브러리 검색성 향상 |
| `sourse` | `source` 또는 역할별 정확한 명칭 | 오탈자 수정 |
| `Frame ...`, `Component 2`, `bg` | `OrderFilters`, `CartBadge`, `Background` 등 | MCP 결과의 레이어 의미 보존 |

### 2. Figma Component Property 추가

Variant만으로 텍스트와 단순 표시 상태를 복제하지 않는다. 아래는 Boolean/Text/Instance swap Property로 추가한다.

| 컴포넌트 | 권장 Property |
| --- | --- |
| `Button` | `label`(Text), `leadingIcon`/`trailingIcon`(Instance swap), `disabled`, `loading`(Boolean), `variant` |
| `MenuCard` | `menuName`, `price`, `calories`(Text), `image`(Instance swap), `soldOut`, `recommended`, `ingredientSoldOut` |
| `CategoryTab` | `label`(Text), `selected`, `disabled` |
| `OptionCategory` | `title`, `required`, `maxSelectable`, `status=default|error|soldOut` |
| `CartItem`/`CartItemRow` | `menuName`, `optionSummary`, `quantity`, `unitPrice`, `soldOut`, `expanded` |
| `PaymentMethodCard` | `methodName`, `selected`, `disabled`, `icon` |
| `Modal` | `title`, `description`, `primaryLabel`, `secondaryLabel`, `type=paymentError|timeout|confirm` |
| `Badge` | `status=received|preparing|completed|cancelled|paymentPending|paymentFailed|refunded` |
| `DataTable/Row` | `orderNo`, `orderType`, `paymentStatus`, `orderStatus`, `amount`, `orderedAt` |

### 3. 코드 컴포넌트와 Figma 매핑 대상

Code Connect를 설정할 때는 화면 Frame이 아니라 **재사용 컴포넌트의 최상위 Component Set**을 대상으로 한다.

| Figma | 코드 후보 |
| --- | --- |
| `Button` | `frontend/src/components/common/Button.jsx` |
| `Modal` | `frontend/src/components/common/Modal.jsx`, `ConfirmDialog.jsx` |
| `MenuCard` | `frontend/src/components/kiosk/MenuCard.jsx` |
| `CategoryTab` | `frontend/src/components/kiosk/CategoryTabs.jsx` |
| `CartItem` 또는 `CartItemRow` | `frontend/src/components/kiosk/CartItem.jsx` |
| `OptionCategory` | `frontend/src/components/kiosk/OptionGroup.jsx` |
| `PaymentMethodCard` | `frontend/src/components/kiosk/PaymentMethodList.jsx` |
| `OrderTypeButton` (정리 후) | `frontend/src/components/kiosk/OrderTypeSelector.jsx` |
| `Badge` | `frontend/src/components/admin/OrderStatusBadge.jsx` |
| `DataTable/*` | `frontend/src/components/admin/OrderTable.jsx` |
| `Toggle` | `frontend/src/components/admin/SoldOutToggle.jsx` |

`Header`, `BottomCTA`, `StepIndicator`처럼 레이아웃 공통 요소도 이후 매핑 대상이지만, 먼저 위 데이터 중심 컴포넌트의 이름/Property를 정리하는 것이 효과가 크다.

## 디자인 토큰 보완

Figma에는 `Palette`(67개)와 `Semantic`(11개) 변수 컬렉션, 텍스트/효과/그리드 스타일이 있다. 코드의 `frontend/src/styles/tokens.css`는 현재 자리표시자이므로 토큰을 CSS 변수로 옮길 기준을 먼저 합의해야 한다.

- Palette는 원색 값, Semantic은 `surface`, `text`, `border`, `action`, `status`처럼 역할 기준 이름으로 유지한다.
- Semantic의 모드 이름 `Mode 1`은 `Light` 또는 실제 테마명으로 변경한다. 다크/고대비를 지원한다면 같은 컬렉션에 모드를 추가한다.
- Text style 중 `payment_boidy`는 `Payment/Body`처럼 오탈자와 경로를 정리한다.
- 스타일 표기 `K/*`, `A/*`는 유지해도 좋으나, 숫자만 있는 `A/20R`, `A-14DM`처럼 의미가 모호한 항목은 역할명을 앞에 붙인다.
- 여백, radius, stroke, z-index/elevation도 Variables로 만들고 Auto Layout의 padding/gap에 바인딩한다.

## 화면 데이터 표기 규칙

각 화면의 루트 Frame 설명(Description) 또는 바로 아래 `__spec` 메모에 다음을 기록한다. 디자인에서 빠지기 쉬운 로딩/빈 목록/오류는 이 규칙으로 관리한다.

```text
Route: /kiosk/menu
Data: categories[], menus[], selectedCategoryId, cartItemCount
States: loading | empty | error | default
Actions: selectCategory, openMenuDetail, openCart
```

레이어 이름은 사용자에게 보이는 문구 대신 데이터 의미를 사용한다.

```text
menuName, menuPrice, calorieInfo, soldOutBadge,
orderNumber, paymentStatus, totalPrice, retryButton
```

## 구현 전 체크리스트

- [ ] 활성 화면 Frame 이름을 `SCR-XXX / 영역 / 화면`으로 변경
- [ ] `k001`~`k007`, `A-001`~`A-007`의 라우트 매핑을 이 문서 표대로 확정
- [ ] `SCR-014 / Kiosk / Accessibility` 생성 또는 범위 제외를 명시
- [ ] 관리자 로그인·메뉴·결제수단 화면이 실제 Frame으로 존재하는지 확정하고 이름 변경
- [ ] `Property 1`, `Variant2`, `Frame ...`, `Component 2`, `bg` 자동 이름 제거
- [ ] 중복 `MenuCard`/`Menu Card` 통합
- [ ] Button, MenuCard, OptionCategory, CartItem, PaymentMethodCard에 Component Property 추가
- [ ] 키오스크의 빈/로딩/오류/품절/필수 옵션 오류/타임아웃 상태를 준비
- [ ] 관리자의 로딩/빈 목록/오류/저장 실패/권한 없음 상태를 준비
- [ ] `03. User Flow`에 홈→메뉴→상세→장바구니→결제→완료 및 실패/타임아웃 분기 연결
- [ ] `frontend/src/styles/tokens.css`로 옮길 토큰명과 값 확정
- [ ] 정리된 최상위 Component Set에 Code Connect 매핑 추가

## 권장 작업 순서

1. 화면 Frame 이름과 라우트 매핑을 확정한다.
2. 공통 `Button`, `MenuCard`, `OptionCategory`, `CartItem`, `PaymentMethodCard`, `Badge`의 이름·Variant·Property를 정리한다.
3. 키오스크 MVP 화면의 예외 상태를 추가한다.
4. Figma Variables/Text styles를 `tokens.css` 설계로 변환한다.
5. 정리된 컴포넌트부터 Code Connect를 코드 파일과 연결한다.

이 순서를 따르면 Figma MCP로 화면을 읽어 구현할 때 디자인 의도와 React props가 직접 대응하고, 화면별 복제/수정 비용도 줄어든다.
