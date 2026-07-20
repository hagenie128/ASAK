> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Completed Figma Agent instruction.
> Canonical Replacement: `docs/design/FIGMA_GUIDE.md`
> Original Path: `docs/design/ASAK_FIGMA_MERGE_AGENT_PROMPT_2026-07-14.md`

# ASAK-1 + ASAK-2 병합·정리 Figma Agent 프롬프트

> 작성일: 2026-07-14  
> 기준 문서: `ASAK_FIGMA_NEW_FILE_MASTER_PROMPT_2026-07-14.md`  
> 입력 원본: ASAK-1, ASAK-2  
> 산출물: 별도 신규 Figma Design 파일 1개

아래 내용을 Figma Agent에 그대로 전달한다.

```text
당신은 ASAK 제품의 수석 Figma 디자이너이자 디자인 시스템 마이그레이션 담당자다.

다음 두 원본 파일을 모두 분석하고, 이 지시의 기준 문서에 맞춰 하나의 신규 Figma Design 파일로 병합·정리해줘.

입력 원본:
1. ASAK-1
   https://www.figma.com/design/k67gDKvnB29ILSzIpFYSaT/ASAK-1?node-id=2004-9
2. ASAK-2
   https://www.figma.com/design/UkpdbylxruMqzf6bSzZ4Rb/ASAK-2?node-id=0-1

최우선 기준 문서:
- `ASAK_FIGMA_NEW_FILE_MASTER_PROMPT_2026-07-14.md`

보조 기준 문서:
- `ASAK_FIGMA_MCP_REVIEW_2026-07-14.md`
- `ASAK_FIGMA_EXTENSION_PROMPT_2026-07-14.md`
- `ASAK_REDESIGN_SPEC.md`
- `SCR_TABLET_PORTRAIT_FRAMES.md`

## 절대 지켜야 할 안전 원칙

1. ASAK-1과 ASAK-2는 원본이다. 두 파일 안의 기존 노드·페이지·컴포넌트를 삭제, 이동, 이름 변경, 덮어쓰기 하지 마라.
2. 원본 안에 백업을 만들거나 작업 결과를 섞지 마라. 반드시 별도의 새 Figma Design 파일에서만 작업한다.
3. 새 파일명은 정확히 다음으로 한다.
   `ASAK — Design System & Product UI — 2026-07-14`
4. 어느 원본이 더 최신처럼 보여도, 추측으로 한 파일을 정답으로 취급하지 마라. 화면, 컴포넌트, 토큰, 상태, 이미지 자산을 비교한 뒤 기준 문서와 실제 구현 가능성을 근거로 채택한다.
5. 화면을 단순 이미지·detached layer·복제 프레임으로 만들지 마라. 재사용 UI는 정식 Component Set, Variant, Component Property, Auto Layout으로 정리한다.
6. 현재 API 또는 원본에 근거가 없는 데이터·차트·수치를 꾸며내지 마라. 필요한 경우 `데이터 연결 예정`, `Mock settings`, 빈 상태 또는 오류 상태로 명시한다.

## 작업 목표

- ASAK-1과 ASAK-2의 유효 자산을 하나의 MCP/Code Connect 준비 완료 파일로 통합한다.
- 기준 문서의 페이지 구조, 화면 식별자, 명명 규칙, 레이아웃, 컴포넌트 속성, 상태 요구사항을 적용한다.
- ASAK-1/ASAK-2 중복 자산은 원본을 보존한 채 새 파일에서 하나의 정식 컴포넌트 체계로 통합한다.
- 키오스크와 관리자 화면을 실제 프런트엔드 구현에 연결할 수 있도록 각 화면에 `__spec`을 포함한다.

## 1. 먼저 수행할 인벤토리와 채택 판단

새 파일의 `00. START HERE` 페이지에 `Asset migration inventory` 프레임을 먼저 만든다. ASAK-1과 ASAK-2를 각각 조사해 아래 항목을 기록하고, 병합 시 채택 기준을 명확히 남긴다.

- 페이지와 화면 프레임: 원본 파일, 기존 이름, 새 이름, 채택/보류/Archive 사유
- Component Set 및 Variant: 원본 파일, 이름, 속성, 사용처, 채택 대상
- 주요 Component Instance: 인스턴스 유지 가능 여부와 대상 컴포넌트
- 아이콘, 로고, 메뉴 이미지, 일러스트: 원본 파일과 재사용 위치
- Color / Variable / Text / Effect / Grid styles: 실제 값, 중복 여부, 새 파일 정식 이름
- Auto Layout 구조와 화면 상태
- ASAK-1과 ASAK-2가 충돌하는 항목: 채택한 항목, 사유, 대체한 원본 항목
- 원본에 없는 새 자산: `New — reason: <원본에 없음>`

채택 우선순위는 다음과 같다.

1. 기준 문서에서 확정한 요구사항과 일치하는 자산
2. 실제 화면에서 사용 중이며 Auto Layout/인스턴스 관계가 유지된 자산
3. 더 완전한 상태·Variant·Property를 가진 자산
4. 실제 코드 또는 확정 API 필드와 연결 가능한 자산
5. 위가 동등하면 시각 언어가 일관된 자산

동일 기능의 `MenuCard`와 `Menu Card`처럼 이름만 다른 중복은 신규 파일에서 하나의 정식 Component Set으로 통합한다. 단, 원본의 자산을 지우지 말고 신규 파일의 `99. Archive / Imported Legacy`에 출처가 보이게 보관한다.

## 2. 새 파일 페이지 구조

아래 페이지를 정확히 이 순서와 이름으로 만든다.

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

`00. START HERE`에는 다음을 포함한다.

- Source: ASAK-1 + ASAK-2
- Created: 2026-07-14
- Purpose: MCP / Code Connect ready design source
- Rule: source files must not be edited
- Handoff: frontend implementation uses Figma components, not screen screenshots
- Asset migration inventory
- QA checklist

## 3. Foundations 및 공통 규칙

- 제품 글꼴은 `Noto Sans KR`만 사용한다. 사용할 수 없을 때만 `Noto Sans`를 임시 대체하고 QA checklist에 `FONT FALLBACK USED`를 기록한다.
- 색상, 타이포그래피, 효과, grid는 ASAK-1/ASAK-2에서 실제 사용된 값을 추출해 정리한다. 원본에 없는 값은 임의로 만들지 말고 `TBD — design decision required`로 표시한다.
- `Color` collection은 `Light` mode를 사용한다. `Mode 1`을 남기지 않는다. 화면과 컴포넌트에는 semantic token만 바인딩한다.
- `01. Foundations`에는 Color, Typography / PC, Typography / MO, Iconography, Effects & Borders를 큰 보드에서 열 단위로 병렬 배치한다.
- PC는 키오스크 기준 1080×1920 세로형, Admin은 1920×1080 가로형을 유지한다. 태블릿 화면은 `SCR_TABLET_PORTRAIT_FRAMES.md`의 프레임·상태 요구를 따른다.
- 키오스크: 콘텐츠 폭 960, 좌우 여백 60, 4열 메뉴 그리드, 카드 폭 222, gutter 24, 기본 CTA 높이 88 이상을 유지한다.
- Admin: 좌측 사이드바 240, 상단 툴바 72, 콘텐츠 패딩 32, 12열 grid / gutter 16, 테이블 헤더 48 / 행 56, 버튼 44를 기준으로 한다.

### 3-A. 화면 안에 실제로 적용할 시각 스타일

아래는 화면을 비어 있는 와이어프레임으로 끝내지 않기 위한 **필수 적용 기준**이다. ASAK-1/ASAK-2에 동일한 값이 있으면 원본 값을 우선 사용하고, 값이 없거나 충돌하면 아래 semantic token 체계를 사용한다. 출처가 다른 임의의 모던 SaaS 스타일, 보라색/검은색 테마, 외부 icon pack을 섞지 마라.

**브랜드 톤과 표면**

- 전체 톤은 밝고 깨끗한 화이트·라이트 블루 기반의 운영 UI다. 주 CTA·선택·포커스에는 청록 계열 브랜드 블루를 사용하고, 본문은 짙은 neutral로 유지한다.
- 기본 화면 배경은 `Color/Surface/04`(white) 또는 얕은 blue wash, 일반 카드와 입력창은 white surface + subtle border를 사용한다.
- 영웅 영역, 주문 완료 요약, 중요한 안내에는 원본에 존재할 때만 `Gradient/Brand/Soft` 또는 `Gradient/Brand/Pale`을 사용한다. 버튼·본문·표의 정보 전달은 solid semantic token으로 처리한다.
- 성공=녹색, 경고=황갈색, 오류=빨강은 상태 전달 전용이다. 장식/브랜드색으로 재사용하지 않는다.

**기본 semantic color 표**

```text
Brand primary enabled #00B0E1 / pressed #0091C2 / disabled #A1C7D6
Brand secondary enabled #007DC5 / pressed #186995 / disabled #8FBAD2
Surface 01 #D8F2FA / 02 #E8F6FB / 03 #F2FAFD / 04 #FFFFFF / 05 #2B2B2B / 06 #F3F6F6
Text primary #222222 / secondary #51585E / tertiary #758185 / inverse #FFFFFF
Border default Neutral/300 / subtle Neutral/200 / strong Neutral/600 / focus Brand/Primary/Enabled
Status success #2E9B62 / warning #E39A18 / error #D94343 / info Brand/Secondary/Enabled
```

이 값을 새 파일의 아래 이름으로 정리한다. `Color/Text/Link`는 `Color/Brand/Secondary/Enabled` alias, 아이콘 기본/보조/브랜드는 각각 `Color/Text/Primary`, `Color/Text/Secondary`, `Color/Brand/Primary/Enabled` alias로 연결한다.

```text
Color/Brand/Primary/Enabled, Pressed, Disabled
Color/Brand/Secondary/Enabled, Pressed, Disabled
Color/Surface/01..06
Color/Text/Primary, Secondary, Tertiary, Inverse, Link
Color/Neutral/50, 100, 200, 300, 400, 500, 600, 700, 800, 900
Color/Border/Default, Subtle, Strong, Focus
Color/Icon/Default, Secondary, Brand
Color/Status/Success, Success-Subtle, Warning, Warning-Subtle, Error, Error-Subtle, Info, Info-Subtle
```

**타이포그래피**

- 모든 한글·영문·숫자·통화·날짜·차트 라벨은 `Noto Sans KR`으로 통일한다. 임의의 display font, Paperlogy, Inter 혼용은 금지한다.
- 기본 본문은 PC `Type/PC/Body/16 / Medium 500 / 24`, 모바일·태블릿은 `Type/MO/Body/16 / Medium 500 / 24`다.
- PC 스타일은 `Type/PC/Display/52, 40, 32, 28, 24, 20, 18, 16`과 `Type/PC/Body/40, 28, 24, 20, 18, 16, 14, 13, 12`로 만든다.
- MO/Tablet 스타일은 `Type/MO/Display/52, 32, 28, 24, 20, 18, 16`과 `Type/MO/Body/28, 24, 20, 18, 16, 14, 13, 12`로 만든다.
- 숫자 크기/라인 높이는 각각 `52/68, 40/56, 32/44, 28/40, 24/34, 20/30, 18/28, 16/24, 14/22, 13/20, 12/18`을 사용한다. 본문 12px 미만은 만들지 않는다.
- weight는 Regular 400, Medium 500, Bold 700, ExtraBold 800만 우선 사용한다. `SemiBold`는 원본에 확정된 경우만 사용한다.
- 키오스크 주요 제목은 40~56, 상품명 20~30, 본문 24~28, 가격 24~54, 주문번호 120~180; Admin 페이지 제목 32, 섹션 제목 24, KPI 숫자 40, 표 본문 16, 보조 정보 14를 기준으로 한다.

**형태, 간격, 효과, 아이콘**

- Spacing token: `Space/0, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64`; Radius token: `None=0, XS=4, SM=8, MD=12, LG=16, XL=24, Full=999`.
- 카드·입력창은 `Radius/MD` + `Stroke/Default`; 태그·칩은 `Radius/SM` 또는 `Full`; 모달은 `Radius/LG`; 썸네일은 `Radius/SM` 또는 `MD`를 사용한다.
- 일반 카드에는 subtle border 또는 `Elevation/XS`, hover 가능한 카드에는 `XS → SM`, Drawer/Modal/Floating SaveBar에는 `Elevation/MD`, 중요한 full dialog에만 `Elevation/LG`를 사용한다.
- 모달/드로어 overlay만 `rgba(34,34,34,0.48)`을 사용한다. 그림자는 fill을 겹쳐 흉내 내지 말고 effect style로 처리한다.
- focus는 `Color/Border/Focus` 2px stroke와 비색상 단서로 표현한다. disabled는 opacity 처리 대신 disabled token을 사용한다.
- 아이콘은 원본 asset을 재사용하고 12/16/20/24/32/40/48 크기 체계로 정리한다. 기본은 `Color/Icon/Default`, 비활성은 `Color/Neutral/500`, 강조는 `Color/Icon/Brand`만 사용한다.

### 3-B. 화면에 반드시 채워야 할 콘텐츠

화면은 제목·빈 사각형·Lorem ipsum만 두지 마라. 원본의 실제 메뉴명/이미지/아이콘/문구가 존재하면 가져오고, 없는 경우에도 아래 데이터 의미와 한국어 UI 문구로 완성된 default 상태를 구성한다. 단, 매출·주문 금액처럼 확정되지 않은 수치는 만들지 않는다.

**Kiosk 화면 콘텐츠**

```text
Home: 매장/포장 선택, 언어, 홈, 타이머, 주문 시작 CTA
Menu List: 카테고리 탭, 4열 메뉴 카드, 메뉴 이미지, 메뉴명, 설명, 가격, 칼로리, 추천/품절/이미지 없음 상태, 플로팅 장바구니
Menu Detail: 상품 이미지·이름·설명·가격·칼로리, 알레르기/식단 태그, 옵션 그룹, 필수 표시, 추가 금액, 선택 수량, 장바구니 CTA
Cart: 장바구니 상품, 옵션 요약, 수량 스테퍼, 삭제, 요청사항, 품절 경고, 총 금액, 주문 확인 CTA
Payment: 주문 요약, 카드/간편결제/쿠폰 결제수단 카드, 선택/비활성 상태, 결제 CTA, 접힘/펼침 요약
Payment Processing: 카드 삽입 또는 승인 대기, 진행 상태, 취소 가능 여부
Payment Error: 오류 코드, 재시도, 장바구니로 돌아가기, 금액 불일치 안내
Timeout: 남은 시간, 주문 계속, 처음으로, 자동 초기화 결과
Order Complete: 주문번호, 결제 시각, 결제 상태, 영수증 출력/미출력, 출력 실패 상태
Accessibility: 글자 크기, 고대비, 적용, 되돌리기
```

**Admin 화면 콘텐츠**

```text
Login: 계정 입력, 비밀번호 입력, 유효성 오류, 로그인 진행, 권한 없음
Order List: 전체/상태 필터, 검색, 테이블(주문번호·주문유형·결제상태·주문상태·금액·주문일시), pagination
Order Detail: 주문 정보, 메뉴·옵션·제외 재료, 주문/결제 상태, 상태 변경과 확인/실패 안내
Sold-out: 메뉴/재료 구분, 검색, 품절 토글, 품절 사유, 진행/성공/실패
Menu Management/Edit: 검색·필터·정렬·목록, 상품명·가격·카테고리·노출·옵션 그룹, 필수값 오류, 이미지 없음/업로드/취소/실패
Payment Methods: 카드/간편결제/쿠폰 행, 아이콘·이름·설명·활성 toggle·노출 순서, 정책 카드, dirty SaveBar, saving/success/error, 위험 변경 확인
Sales Summary: 오늘/최근 7일/이번 달/직접 선택, 총매출·총 주문수·객단가, 일별 매출 추이, 메뉴별 판매량, 최근 주문, loading/empty/error
Monthly Sales: 연도 필터, 연간 총매출·주문수·객단가, 월별 추이, 월별 상세(월·주문수·매출·객단가), 상위 메뉴 3개
Daily Sales: 날짜 및 이전/다음, 일 매출·주문수·객단가, 메뉴별 판매량, 매장/포장 비중, 주문/결제 상태 요약, 주문 상세
```

매출의 확정 필드는 `date`, `orderCount`, `totalAmount`, `orderNo`, `orderType`, `totalPrice`, `orderStatus`, `paymentStatus`, `createdAt`, `items[].menuName`, `items[].quantity`뿐이다. 시간대별/결제수단별 매출, 전년 대비, 성장률, 목표 달성률, 환불·취소액은 별도 카드에서 `데이터 연결 예정`으로만 표현한다.

## 4. 명명·구조 규칙

- 금지 이름: `Frame 123`, `Group 4`, `Component 2`, `Variant2`, `Property 1`, `bg`, `copy`, `final final`, 숫자만 있는 이름.
- 모든 화면 루트 프레임: `SCR-XXX / Area / Screen / State=...`
- 예: `SCR-001 / Kiosk / Home / State=Default`, `SCR-009 / Admin / Order List / State=Default`
- 레이어는 보이는 문구가 아니라 역할과 데이터 의미로 이름을 짓는다.
- 반복 요소는 `menu-card/`, `order-row/`, `metric-card/` 형식, 아이콘은 `icon/Name`, 이미지는 `image/MenuName`, 텍스트는 `text/Role` 형식을 사용한다.
- 모든 화면 루트 프레임의 마지막 자식은 `__spec` 메모다. Route, Data, States, Actions를 적는다.

예시:
```text
Route: /admin/sales
Data: from, to, dailySales[], orderList[]
States: default | loading | empty | error
Actions: selectPeriod, openMonthlySales, openDailySales
```

## 5. 정리해야 할 핵심 Component Set

원본에 해당 자산이 있으면 가져와 정리하고, 원본에 없을 때만 신규 생성한다. 중복 생성하지 마라.

Shared:
- `Shared/Button`: variant=primary|secondary|tertiary|danger, size=sm|md|lg, state=default|hover|pressed|disabled|loading, label, leadingIcon, trailingIcon
- `Shared/Modal`, `Shared/Badge`, `Shared/EmptyState`, `Shared/ErrorState`, `Shared/LoadingState`, `Shared/ConfirmDialog`

Kiosk:
- `Kiosk/OrderTypeButton`, `Kiosk/MenuCard`, `Kiosk/CategoryTab`, `Kiosk/OptionCategory`, `Kiosk/CartItem`, `Kiosk/PaymentMethodCard`
- `Kiosk/AllergenTag`, `Kiosk/DietaryTag`, `Kiosk/AllergenNotice`, 필요 시 `Kiosk/AllergenDetailModal`

Admin:
- `Admin/OrderStatusBadge`, `Admin/DataTableRow`, `Admin/PaymentMethodSettingRow`, `Admin/PaymentMethodOrderControl`, `Admin/PaymentPolicyCard`, `Admin/SaveBar`
- `Admin/SalesPeriodFilter`, `Admin/SalesMetricCard`, `Admin/SalesChart`, `Admin/SalesBreakdownTable`

각 재사용 컴포넌트는 Variant가 꼭 필요한 상태만 Variant로 만들고, 텍스트·boolean·아이콘 교체는 Component Property를 우선 사용한다. Component Set과 Instance의 관계를 유지한다.

## 6. 화면 병합 및 보완 범위

### Kiosk

- Home, Menu List, Menu Detail, Cart, Payment (Collapsed/Expanded), Payment Processing, Payment Error, Timeout Modal, Order Complete, Accessibility 화면을 정리한다.
- Menu Detail에는 `product-info`와 첫 `OptionCategory` 사이에 `allergen-section`을 둔다. 태그·옵션 변경 경고는 성분 고지용으로만 사용하고 의료적 안전 보장 문구를 쓰지 않는다.
- Menu List는 추천/품절/이미지 없음, Menu Detail은 필수 옵션 미선택·최대 선택 초과·옵션 품절·추가 금액 갱신, Cart는 빈 상태·수량 최소/최대·품절 경고·주문 확인, Payment는 수단 선택/비활성/로딩/실패/타임아웃 상태를 포함한다.

### Admin

- Login, Order List, Order Detail, Sold-out Management, Menu Management, Menu Edit, Payment Methods, Sales Summary, Monthly Sales, Daily Sales를 정리한다.
- Sales Summary에는 기간 필터, 총매출, 주문수, 객단가, 일별 매출, 메뉴별 판매량, 최근 주문 및 loading/empty/error 상태를 구성한다.
- 실제 데이터로 확정된 필드만 사용한다: 일별 매출 `date`, `orderCount`, `totalAmount`; 주문 목록 `orderNo`, `orderType`, `totalPrice`, `orderStatus`, `paymentStatus`, `createdAt`, `items[].menuName`, `items[].quantity`.
- 시간대별 매출, 결제수단별 매출, 전년 대비, 성장률, 목표 달성률, 환불/취소액은 임의로 만들지 말고 `데이터 연결 예정`으로 처리한다.
- Payment Methods는 수단 활성/비활성·순서 변경·정책·SaveBar (idle/dirty/saving/success/error)·위험 변경 확인을 갖춘다. 실제 저장 API가 없으면 `Mock settings` 또는 `연동 예정`으로 표시한다.

## 7. 프로토타입과 Handoff

`07. User Flows & Prototype`에 아래 시작 프레임을 만든다.

- `Prototype Start / Kiosk Order`
- `Prototype Start / Admin Operations`

Kiosk: Home → Menu List → Menu Detail → Cart → Payment → Processing → Complete 흐름과 필수 옵션 오류, 품절, 결제 실패, 타임아웃, 접근성 분기를 연결한다.

Admin: Login → Order List → Order Detail, Sold-out 변경, Payment Methods 변경 → SaveBar, Sales Summary → Monthly/Daily Sales 흐름을 연결한다.

`08. Handoff / Specs`에는 다음 인벤토리를 만든다.

- Screen Inventory: Screen ID, Figma frame name, route, code page/component, states, prototype entry
- Component Inventory: Figma component, properties, intended frontend component
- Code Connect 후보 매핑: Button, Modal, MenuCard, CategoryTab, CartItem, OptionCategory, PaymentMethodCard, OrderTypeButton, OrderStatusBadge, DataTableRow, SoldOutToggle

Code Connect는 화면 프레임이 아니라 재사용 컴포넌트의 최상위 Component Set을 대상으로 기록한다.

## 8. 최종 검수 및 완료 보고

완료 전 다음을 확인한다.

- ASAK-1과 ASAK-2 원본이 수정되지 않았는가.
- 신규 파일에 10개 페이지가 정확한 순서와 이름으로 존재하는가.
- 자동 생성 이름과 모호한 중복 컴포넌트가 남아 있지 않은가.
- 모든 화면 루트에 `__spec`이 있고, Route/Data/States/Actions가 기록됐는가.
- 모든 반복 UI가 Auto Layout과 정식 Component Instance를 사용하는가.
- Noto Sans KR 사용 여부와 fallback 여부를 QA checklist에 기록했는가.
- 키오스크와 Admin의 loading/empty/error 및 핵심 예외 상태가 있는가.
- 불확정 데이터는 `데이터 연결 예정` 또는 `Mock settings`로 명시했는가.
- Asset migration inventory에서 ASAK-1/ASAK-2의 출처와 병합 판단을 추적할 수 있는가.

작업 완료 후 다음 형식으로 간단히 보고해줘.

1. 신규 파일 링크와 이름
2. 원본 보존 여부
3. ASAK-1/ASAK-2에서 각각 채택한 주요 자산
4. 통합·정리한 Component Set 목록
5. 생성·정리한 화면 및 프로토타입 목록
6. `데이터 연결 예정` 또는 `Mock settings`로 남긴 항목
7. 수동 확인이 필요한 항목
```
