# ASAK Figma 새 파일 재구성 마스터 프롬프트

> 작성일: 2026-07-14  
> 대상 원본: [ASAK Figma](https://www.figma.com/design/o9mxSeovLQPdWNwM4mNySk/ASAK)  
> 사용법: 아래 **복사해서 Figma에 전달할 프롬프트** 전체를 Figma AI 또는 내일 실행할 Figma MCP 작업 지시로 사용한다.

## 작업 원칙

- 원본 파일은 수정·삭제·이동하지 않는다. 백업은 원본 안에 복제하지 말고, 별도의 새 Figma Design 파일로 만든다.
- 새 파일은 `ASAK — Design System & Product UI — 2026-07-14`로 생성한다. 원본은 `ASAK — Legacy (Read only) — 2026-07-14`라는 이름으로 남겨 둔다. 파일명을 바꿀 권한이 없으면 새 파일명만 위 이름으로 하고 원본은 그대로 보존한다.
- 새 파일은 원본의 색, 타이포그래피, 브랜드 톤과 실제 화면 내용을 기준으로 재구성한다. 보이는 화면을 단순 스크린샷처럼 복제하지 말고, 재사용 가능한 컴포넌트·변수·오토레이아웃 구조로 만든다.
- 이 문서에서 확정하지 않은 API 데이터는 그럴듯한 수치로 꾸며내지 않는다. 빈 상태 또는 `데이터 연결 예정` 상태를 만든다.
- 완료 기준은 “예쁜 화면”이 아니라, 명명 규칙과 구조가 정리되어 내일 MCP/Code Connect에서 안전하게 읽고 수정할 수 있는 파일이다.

## 복사해서 Figma에 전달할 프롬프트

```text
당신은 ASAK 제품의 수석 Figma 디자이너이자 디자인 시스템 정리 담당자다.

목표는 기존 ASAK Figma 파일을 절대로 훼손하지 않고 백업으로 보존한 뒤, 별도의 새 Figma Design 파일에 디자인 시스템, 키오스크, 관리자 화면, 프로토타입을 실제 개발 연동이 가능한 수준으로 재구성하는 것이다. 기존 원본을 수정하거나 기존 노드를 삭제/이동/이름 변경하지 마라.

────────────────────────────────
0. 안전한 백업과 새 파일 생성
────────────────────────────────
1) 현재 원본 파일을 읽기 전용 기준점으로 남긴다. 원본 안에 작업하지 않는다.
2) 새 Figma Design 파일을 생성하고 이름을 아래처럼 지정한다.
   `ASAK — Design System & Product UI — 2026-07-14`
3) 새 파일의 첫 페이지 `00. START HERE`에 아래 내용을 포함한 메모 프레임을 만든다.
   - Source: ASAK Legacy file
   - Created: 2026-07-14
   - Purpose: MCP / Code Connect ready design source
   - Rule: legacy file must not be edited
   - Handoff: frontend implementation uses Figma components, not screen screenshots
4) 원본에서 필요한 화면과 스타일을 새 파일로 복제해 시작하되, 복제 후에는 아래 구조와 이름으로 정리한다.
5) 새 파일의 모든 편집 대상은 Auto Layout 기반으로 만들고, 절대 위치 배치만으로 화면을 구성하지 않는다.

────────────────────────────────
1. 페이지 구조 (페이지 이름은 정확히 사용)
────────────────────────────────
새 파일에 아래 페이지를 이 순서대로 만든다.

`00. START HERE`
`01. Foundations`
`02. Components / Shared`
`03. Components / Kiosk`
`04. Components / Admin`
`05. Screens / Kiosk`
`06. Screens / Admin`
`07. User Flows & Prototype`
`08. Handoff / Specs`
`99. Archive / Imported Legacy`

- 기존 화면을 원형 보관해야 하면 `99. Archive / Imported Legacy`에만 둔다.
- 개발에 사용할 정리된 화면은 반드시 `05`, `06`에 둔다.
- 페이지 이름, 섹션 이름, 프레임 이름, 컴포넌트 이름에 이모지, 임시 이름, 한글/영문 혼용의 모호한 약어를 쓰지 않는다.

────────────────────────────────
2. 명명 및 레이어 규칙 (엄격 적용)
────────────────────────────────
금지 이름: `Frame 123`, `Group 4`, `Component 2`, `Variant2`, `Property 1`, `bg`, `copy`, `final final`, 숫자만 있는 이름.

모든 화면 루트 프레임 이름:
`SCR-XXX / Area / Screen / State=...`

예시:
- `SCR-001 / Kiosk / Home / State=Default`
- `SCR-004 / Kiosk / Menu Detail / State=Default`
- `SCR-007 / Kiosk / Payment / Summary=Collapsed`
- `SCR-009 / Admin / Order List / State=Default`
- `SCR-019 / Admin / Sales Summary / State=Default`

모든 레이어는 사용자에게 보이는 문구가 아니라 역할과 데이터 의미로 이름을 짓는다.

권장 레이어 구조:
```text
screen-root
├─ app-shell
│  ├─ global-header
│  ├─ side-navigation
│  └─ page-content
├─ page-header
│  ├─ title-area
│  └─ page-actions
├─ primary-content
├─ secondary-content
├─ overlay-layer
└─ __spec
```

- 반복 요소는 `menu-card/`, `order-row/`, `metric-card/`처럼 역할별 접두어를 사용한다.
- 아이콘 레이어는 `icon/Name`, 이미지 레이어는 `image/MenuName`, 텍스트는 `text/Role` 형식으로 명확하게 이름을 붙인다.
- 숨겨진 프로토타입용 레이어도 `prototype/...` 이름을 사용한다.
- 모든 화면의 루트 프레임 마지막 자식에 `__spec` 메모를 둔다. 메모에는 Route, Data, States, Actions를 적는다.

`__spec` 예시:
```text
Route: /admin/sales
Data: from, to, dailySales[], orderList[]
States: default | loading | empty | error
Actions: selectPeriod, openMonthlySales, openDailySales
```

────────────────────────────────
3. Foundations 및 디자인 토큰
────────────────────────────────
`01. Foundations`에서 원본의 Palette, Semantic color, 텍스트, 그림자, 그리드 스타일을 검토해 다음 항목을 정리한다.

1) Color variables
   - Collection: `Color`
   - Groups: `Color/Surface`, `Color/Text`, `Color/Border`, `Color/Action`, `Color/Status`, `Color/Brand`
   - 기본 모드는 `Light`로 명명한다. `Mode 1`을 사용하지 않는다.
   - 원본의 팔레트 값을 그대로 활용하되 UI에는 primitive 색상 대신 semantic color variable을 바인딩한다.
2) Number variables
   - Collection: `Layout`
   - `Space/0`, `Space/4`, `Space/8`, `Space/12`, `Space/16`, `Space/20`, `Space/24`, `Space/32`, `Space/40`, `Space/48`
   - `Radius/0`, `Radius/4`, `Radius/8`, `Radius/12`, `Radius/16`, `Radius/Full`
   - `Stroke/Default`, `Elevation/1`, `Elevation/2`, `Elevation/3`
3) Text styles
   - 모호한 숫자형 이름 대신 `Kiosk/Heading/L`, `Kiosk/Body/M`, `Admin/Heading/L`, `Admin/Body/M`, `Shared/Label/S`처럼 역할 기반으로 정리한다.
   - 오탈자 `payment_boidy`가 있으면 새 파일에는 `Payment/Body`로 정정한다.
4) Effect and grid styles
   - 그림자와 레이아웃 그리드는 명시적 이름을 사용한다.
5) 각 foundation 영역에는 사용 규칙과 Do/Don't를 짧은 메모로 남긴다.

────────────────────────────────
4. 공통 컴포넌트와 속성
────────────────────────────────
컴포넌트는 반드시 최상위 Component Set으로 만들고, 인스턴스 복제본을 컴포넌트처럼 방치하지 않는다. 상태 변화는 필요한 경우에만 Variant로 만들고, 텍스트·아이콘·단순 표시 여부는 Component Property를 우선 사용한다.

공통 컴포넌트:
- `Shared/Button`
  - properties: `variant=primary|secondary|tertiary|danger`, `size=sm|md|lg`, `state=default|hover|pressed|disabled|loading`, `label` Text, `leadingIcon` Instance swap, `trailingIcon` Instance swap
- `Shared/Modal`
  - properties: `type=confirm|paymentError|timeout|info`, `title` Text, `description` Text, `primaryLabel` Text, `secondaryLabel` Text
- `Shared/Badge`
  - properties: `status=received|preparing|completed|cancelled|paymentPending|paymentFailed|refunded`, `label` Text
- `Shared/EmptyState`
  - properties: `type=general|sales|paymentMethods|orders`, `title` Text, `description` Text, `showAction` Boolean
- `Shared/ErrorState`
  - properties: `type=load|save|payment`, `title` Text, `description` Text, `retryLabel` Text
- `Shared/LoadingState`
  - properties: `type=page|card|table|button`
- `Shared/ConfirmDialog`
  - properties: `type=delete|discardChanges|disableAllPaymentMethods`, `title` Text, `description` Text

키오스크 컴포넌트:
- `Kiosk/OrderTypeButton`: `type=eatIn|takeOut`, `state=default|selected|disabled`, `label` Text
- `Kiosk/MenuCard`: `menuName`, `price`, `calories` Text; `image` Instance swap; `soldOut`, `recommended`, `ingredientSoldOut` Boolean
- `Kiosk/CategoryTab`: `label` Text, `selected` Boolean, `disabled` Boolean
- `Kiosk/OptionCategory`: `title` Text, `required` Boolean, `maxSelectable` Text, `status=default|error|soldOut`
- `Kiosk/CartItem`: `menuName`, `optionSummary`, `quantity`, `unitPrice` Text; `soldOut`, `expanded` Boolean
- `Kiosk/PaymentMethodCard`: `methodName` Text, `selected`, `disabled` Boolean, `icon` Instance swap
- `Kiosk/AllergenTag`: `type=nut|milk|egg|shellfish|soy|wheat|etc`, `state=default|warning`, `label` Text
- `Kiosk/DietaryTag`: `type=vegan|vegetarian|etc`, `label` Text
- `Kiosk/AllergenNotice`: `state=default|hasAllergen|optionChanged`, `title` Text, `description` Text
- `Kiosk/AllergenDetailModal`: 성분명 및 포함 출처(기본 구성/추가 옵션) 표시

관리자 컴포넌트:
- `Admin/OrderStatusBadge`
- `Admin/DataTableRow`: `orderNo`, `orderType`, `paymentStatus`, `orderStatus`, `amount`, `orderedAt` Text
- `Admin/PaymentMethodSettingRow`: `state=enabled|disabled|maintenance`, `name`, `description` Text, `icon` Instance swap, `enabled` Boolean
- `Admin/PaymentMethodOrderControl`: `state=default|first|last`, `direction=up|down`
- `Admin/PaymentPolicyCard`: `policyType=resetOnFailure|notice|receipt`, `state=default|changed`
- `Admin/SaveBar`: `state=idle|dirty|saving|success|error`
- `Admin/SalesPeriodFilter`: `state=default|open|customRange|loading`
- `Admin/SalesMetricCard`: `metric=totalSales|orderCount|averageOrderValue`, `state=default|loading|empty`
- `Admin/SalesChart`: `granularity=daily|monthly`, `state=default|loading|empty|error`
- `Admin/SalesBreakdownTable`: `type=daily|monthly|menu|order`, `state=default|empty|loading|error`

동일한 기능의 `MenuCard`와 `Menu Card`처럼 이름만 다른 중복 컴포넌트는 새 파일에서 하나의 정식 컴포넌트로 통합한다.

────────────────────────────────
5. 키오스크 화면 (05. Screens / Kiosk)
────────────────────────────────
아래 화면을 만들거나 원본 화면을 재구성하고, 각 화면의 default와 필요한 예외 상태를 준비한다.

- `SCR-001 / Kiosk / Home / State=Default`
  - 매장/포장 선택, 선택 상태, 비활성 상태
- `SCR-003 / Kiosk / Menu List / State=Default`
  - 카테고리 탭, 추천/품절/이미지 없음 메뉴 카드, 가격·칼로리 표시
- `SCR-004 / Kiosk / Menu Detail / State=Default`
  - 필수 옵션 미선택 오류, 최대 선택 초과, 옵션 품절, 추가 금액 갱신 상태
  - `product-info`와 첫 `OptionCategory` 사이에 `allergen-section`을 삽입한다.
  - 레이어: `allergen-section > allergen-section-header, allergen-tag-list, allergen-notice`
  - 알레르기 위험 성분은 태그로 표시하고 옵션 선택으로 새 성분이 포함되면 warning notice로 바뀐다.
  - 의학적 안전 보장 문구는 쓰지 말고, 성분 정보 안내 문구만 사용한다.
- `SCR-005 / Kiosk / Cart / State=Default`
  - 빈 장바구니, 재고/품절 경고, 수량 최소·최대, 주문 확인 모달
- `SCR-007 / Kiosk / Payment / Summary=Collapsed`
- `SCR-007 / Kiosk / Payment / Summary=Expanded`
  - 결제수단 선택/비활성, 결제 버튼 로딩을 명확히 분리한다.
- `SCR-007 / Kiosk / Payment Processing / State=Default`
  - 카드 삽입/태깅 대기, 취소 가능 여부, 진행 상태
- `SCR-012 / Kiosk / Payment Error / State=Default`
  - 오류 코드, 재시도, 장바구니 복귀, 금액 불일치 안내
- `SCR-013 / Kiosk / Timeout Modal / State=Default`
  - 남은 시간, 주문 계속, 처음으로 버튼, 자동 초기화 결과
- `SCR-008 / Kiosk / Order Complete / State=Default`
  - `orderNo`, `paidAt`, `paymentStatus`, 영수증 선택 및 출력 실패 상태
- `SCR-014 / Kiosk / Accessibility / State=Default`
  - 글자 크기, 고대비 적용/되돌리기 상태

키오스크 화면은 실제 키오스크 기준으로 넉넉한 터치 영역과 버튼 간 간격을 유지한다. 각 화면은 app shell, 콘텐츠, 하단 CTA가 구조적으로 분리되어야 한다.

────────────────────────────────
6. 관리자 화면 (06. Screens / Admin)
────────────────────────────────
아래 모든 화면은 기본, loading, empty, error 상태를 필요한 수준으로 준비한다.

- `SCR-015 / Admin / Login / State=Default`: 기본, 입력 오류, 로그인 진행, 권한 없음
- `SCR-009 / Admin / Order List / State=Default`: 전체/상태 필터, 검색, loading, empty, error, pagination
- `SCR-010 / Admin / Order Detail / State=Default`: 상태별 섹션, 변경 확인, 변경 실패, 옵션/제외 재료
- `SCR-011 / Admin / Sold-out Management / State=Default`: 메뉴/재료 구분, 토글 진행/성공/실패, 품절 사유
- `SCR-016 / Admin / Menu Management / State=Default`: 검색, 필터, 정렬, 빈 목록, 메뉴 등록 진입
- `SCR-017 / Admin / Menu Edit / State=Create`: 등록/수정, 필수값 오류, 이미지 없음/업로드/취소/실패
- `SCR-018 / Admin / Payment Methods / State=Default`
  - 수단 목록, 아이콘, 이름, 설명, 활성 여부, 노출 순서, 정책 카드
  - 변경되면 `Admin/SaveBar`가 dirty로 표시된다.
  - 저장 중/성공/오류 상태와 “모든 결제수단 비활성화”, “변경사항 버리기” 확인 다이얼로그를 만든다.
  - 실제 설정 저장 API가 확정되지 않았으므로 화면에 `Mock settings` 또는 `연동 예정`임을 __spec에 명시한다.
- `SCR-019 / Admin / Sales Summary / State=Default`
  - 기간 필터: 오늘, 최근 7일, 이번 달, 직접 선택
  - 총매출, 총 주문 수, 평균 객단가
  - 일별 매출 추이, 메뉴별 판매량 상위 목록, 최근 주문 목록
  - 별도 화면: `SCR-020 / Admin / Monthly Sales / State=Default`, `SCR-021 / Admin / Daily Sales / State=Default`

매출 화면의 실제 사용 가능 데이터는 아래로 제한한다.
- 일별 매출 API: `date`, `orderCount`, `totalAmount`
- 관리자 주문 목록: `orderNo`, `orderType`, `totalPrice`, `orderStatus`, `paymentStatus`, `createdAt`, `items[].menuName`, `items[].quantity`

따라서 시간대별 매출, 결제수단별 매출, 전년/전월 비교, 목표 달성률, 환불/취소 분석은 수치를 가공해 만들지 않는다. 해당 영역이 필요하면 `데이터 연결 예정` 카드와 필요한 필드를 명시한다.

────────────────────────────────
7. 프로토타입 (07. User Flows & Prototype)
────────────────────────────────
`07. User Flows & Prototype`에 흐름도와 실제 클릭 가능한 프로토타입 시작 프레임을 만든다. 흐름도는 화살표와 조건 레이블을 사용해 다음 분기를 모두 표현한다.

키오스크 대표 흐름:
1) Home → 매장/포장 선택 → Menu List → Menu Detail
2) 옵션을 정상 선택 → 장바구니 추가 → Cart → Payment Summary Collapsed → 결제수단 선택 → Payment Processing → Order Complete
3) 필수 옵션 미선택 → Menu Detail의 오류 상태
4) 품절 메뉴 또는 옵션 → 선택 불가/경고 상태
5) 결제 실패 → Payment Error → 재시도 또는 장바구니 복귀
6) 시간 초과 → Timeout Modal → 주문 계속 또는 처음으로
7) 접근성 버튼 → Accessibility → 적용 → 이전 화면 복귀

관리자 대표 흐름:
1) Login → Order List → Order Detail → 주문 상태 변경 확인 → 성공 또는 실패
2) Sold-out Management → 토글 변경 → 진행 → 성공 또는 실패
3) Payment Methods → 활성화/순서 변경 → SaveBar dirty → 저장 → success/error
4) Sales Summary → 기간 선택 → Monthly Sales 또는 Daily Sales

프로토타입 연결 규칙:
- 각 화면의 실제 CTA와 메뉴/탭만 연결한다. 장식 레이어 전체에 연결하지 않는다.
- 기본 전환은 `Navigate to` + `Smart animate`(200~300ms, Ease out)를 사용한다.
- 모달은 `Open overlay`, 닫기는 `Close overlay`를 사용하고, 배경 클릭 닫힘이 적절한 모달에만 적용한다.
- 토글, 탭, 요약 확장/축소는 가능하면 component interactive variant로 연결한다.
- 로딩은 실제 기다림을 흉내 내는 긴 지연보다 명확한 별도 상태 프레임으로 연결한다.
- 시작점 이름: `Prototype Start / Kiosk Order`, `Prototype Start / Admin Operations`
- 모든 연결 대상은 정식 화면 프레임이어야 하며 archive 프레임에 연결하지 않는다.

────────────────────────────────
8. Handoff 및 MCP 준비 (08. Handoff / Specs)
────────────────────────────────
1) `Screen Inventory` 테이블을 만든다: Screen ID, Figma frame name, route, code page/component, states, prototype entry.
2) `Component Inventory` 테이블을 만든다: Figma component, properties, intended frontend component.
3) 아래 코드 매핑을 기록한다.
   - `Shared/Button` → `frontend/src/components/common/Button.jsx`
   - `Shared/Modal` → `frontend/src/components/common/Modal.jsx`, `ConfirmDialog.jsx`
   - `Kiosk/MenuCard` → `frontend/src/components/kiosk/MenuCard.jsx`
   - `Kiosk/CategoryTab` → `frontend/src/components/kiosk/CategoryTabs.jsx`
   - `Kiosk/CartItem` → `frontend/src/components/kiosk/CartItem.jsx`
   - `Kiosk/OptionCategory` → `frontend/src/components/kiosk/OptionGroup.jsx`
   - `Kiosk/PaymentMethodCard` → `frontend/src/components/kiosk/PaymentMethodList.jsx`
   - `Kiosk/OrderTypeButton` → `frontend/src/components/kiosk/OrderTypeSelector.jsx`
   - `Admin/OrderStatusBadge` → `frontend/src/components/admin/OrderStatusBadge.jsx`
   - `Admin/DataTableRow` → `frontend/src/components/admin/OrderTable.jsx`
   - `Admin/SoldOutToggle` → `frontend/src/components/admin/SoldOutToggle.jsx`
4) Code Connect의 대상은 화면 프레임이 아니라 최상위 Component Set임을 명시한다.
5) MCP가 읽기 쉽도록 모든 디자인 요소의 이름, variant property, text property가 의미 있는 영어 식별자인지 최종 점검한다.

────────────────────────────────
9. 완료 전 강제 검수
────────────────────────────────
다음 항목을 모두 확인하고, `00. START HERE`에 `QA checklist`로 체크 상태를 남긴다.

- [ ] 원본 파일은 변경하지 않았고 새 파일에서만 작업했다.
- [ ] 새 파일의 9개 페이지가 지정된 순서와 이름으로 존재한다.
- [ ] `Frame`, `Group`, `Component`, `Variant`, `Property`의 자동 생성 이름이 남아 있지 않다.
- [ ] 모든 화면 루트 프레임이 `SCR-XXX / Area / Screen / State=...` 규칙을 따른다.
- [ ] 모든 화면에 `__spec`이 있고 route/data/states/actions가 적혀 있다.
- [ ] 모든 반복 UI가 Auto Layout과 정식 컴포넌트 인스턴스를 사용한다.
- [ ] Button, MenuCard, OptionCategory, CartItem, PaymentMethodCard, Badge가 속성과 상태를 갖춘 Component Set이다.
- [ ] 키오스크의 빈/로딩/오류/필수 옵션 오류/결제 실패/시간 초과 상태가 있다.
- [ ] 관리자의 빈/로딩/오류/저장 실패/권한 없음 상태가 있다.
- [ ] 알레르기 섹션과 옵션 변경 경고가 Menu Detail에 있다.
- [ ] 미확정 매출 데이터에 가짜 수치가 없고 `데이터 연결 예정`으로 처리했다.
- [ ] 키오스크와 관리자 프로토타입 시작점 및 핵심 분기 연결이 작동한다.
- [ ] `08. Handoff / Specs`에 Screen/Component inventory와 코드 매핑이 있다.

완료 보고는 아래 형식으로 간단히 작성한다.
1. 새 파일 링크와 이름
2. 원본 보존 여부
3. 생성한 페이지 및 화면 수
4. 생성/정리한 Component Set 목록
5. 연결한 프로토타입 플로우 목록
6. 데이터 연결 예정으로 남긴 항목
7. 남은 수동 확인 항목
```

## 내일 MCP 실행 시 권장 순서

1. 새 Figma 파일을 만든 뒤 위 프롬프트의 0~2단계만 먼저 실행하고, 페이지·이름·원본 보존을 확인한다.
2. Foundations → Components → Screens 순서로 작성한다. 화면부터 만들면 중복 컴포넌트와 레이어명이 다시 생긴다.
3. 화면과 상태가 모두 마련된 뒤에만 Prototype과 Handoff 페이지를 연결한다.
4. 마지막으로 `00. START HERE`의 QA checklist를 MCP로 다시 읽어, 미체크 항목을 보완한다.

## 원본 대비 핵심 변경점

- 기존 원본을 고치지 않고 별도 파일에서 재구성한다.
- 화면 명칭을 `k001`, `A-006` 같은 내부 임시명에서 `SCR-XXX / Area / Screen` 규칙으로 정규화한다.
- 화면뿐 아니라 컴포넌트 속성, 상태, `__spec`, 프로토타입, Code Connect 매핑까지 인계 범위에 넣는다.
- 현재 API로 만들 수 없는 분석은 가짜 데이터 대신 명확한 연결 예정 상태로 남긴다.
