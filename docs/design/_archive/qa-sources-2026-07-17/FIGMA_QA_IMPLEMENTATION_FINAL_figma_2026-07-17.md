# ASAK 디자인 시스템 종합 QA

> 기준: 키오스크는 **15~27인치 터치 스탠드**, 관리자는 **웹·태블릿** 환경입니다.

## 1. 종합 결론

현재 디자인은 키오스크의 다크 배경·음식 사진·라임 컬러 조합으로 브랜드 정체성이 잘 드러납니다. 다만 키오스크에서 사용하는 일부 컴포넌트가 웹·모바일 크기로 제작되어 가독성과 터치 영역이 부족합니다. 또한 `lineHeight: AUTO`, 절대 좌표 레이아웃, 위험 동작의 약한 구분을 우선 정리해야 합니다.

### 즉시 수정 7건

| 우선 | 대상 | 조치 |
| --- | --- | --- |
| 1 | `Kiosk/MenuDetailSummary` | 뱃지 14px, 이름 28px 이상, 가격 24px 이상으로 전체 스케일업 |
| 2 | `Kiosk/OptionGroup`, `OptionSelectionRow` | 폰트 16~20px, radius 12, 체크 아이콘 추가 |
| 3 | `Kiosk/MenuCard` | Vertical Auto Layout 적용, kcal 28px → 16px |
| 4 | `Admin/SoldOutCard` | 글자 9px → 12px 이상, 카드 크기 확대 |
| 5 | `Admin/OrderActionButtons` | 환불을 빨간 outline 버튼으로 구분하고 확인 단계 추가 |
| 6 | `Kiosk/BottomCTA` | 내부 버튼 radius 20, 좌우 여백 적용 |
| 7 | `Admin/DataTableRow` | Hover Variant 추가 |

### 높은 우선순위

1. `lineHeight: AUTO`를 아래 명시값으로 일괄 교체합니다.
2. `Kiosk/CategoryTab` 높이를 52px에서 64px로 늘립니다.
3. `Shared/EmptyState`, `Shared/ErrorState` radius를 0에서 12px로 변경합니다.
4. `Kiosk/Header`, `Shared/CartFooterBar`를 Auto Layout으로 변환합니다.
5. `Admin/Navbar` padding을 12 / 16으로 조정하고 active accent bar를 추가합니다.
6. `Shared/ConfirmDialog` 제목을 18px Bold로 통일합니다.

---

## 2. Shared 컴포넌트

### `Shared/Modal`

| 항목 | 현재 판정 | 권장 |
| --- | --- | --- |
| 사이즈 | 480×196 ✅ | — |
| Padding | 32 all ✅ | — |
| Radius | 16 ✅ | — |
| Title | 22px Bold, lh 28px ✅ | — |
| Body | 16px Regular, lh 24px ✅ | — |
| Button text | 16px Medium, lh 20px ⚠️ | 키오스크용 버튼 높이 48px 확보 |

### `Shared/ConfirmDialog`

| 항목 | 현재 판정 | 권장 |
| --- | --- | --- |
| Title | 16px Medium, lh 20px 🔴 | 18px Bold, lh 24px |
| Body | 14px Regular, lh 20px ✅ | — |
| 색상 | `#e5e7eb` (Tailwind계) ⚠️ | 시스템 Neutral `#f5f5f5` |

> `Modal` 제목은 22/28 Bold인데 `ConfirmDialog` 제목은 16/20 Medium입니다. 같은 역할의 다이얼로그 간 위계를 맞춰야 합니다.

### `Shared/Toast`

| 항목 | 현재 판정 | 권장 |
| --- | --- | --- |
| 사이즈 | 299×76 ✅ | 키오스크는 높이 80px 이상 |
| Radius | 12 ✅ | — |
| Text | 14px Regular, lh 20px ✅ | — |
| 닫기 | `✕` 텍스트 ⚠️ | 24×24 Icon 컴포넌트 |

### 상태 컴포넌트

| 컴포넌트 | 문제 | 권장 |
| --- | --- | --- |
| `Shared/EmptyState` | radius 0 🔴, 아이콘 배경 `#e5e7eb` ⚠️ | radius 12, 아이콘 배경 `#f5f5f5` |
| `Shared/ErrorState` | radius 0 🔴, CTA 라임색 ⚠️ | radius 12, Error CTA는 neutral dark `#292d30` |
| `Shared/LoadingState` | Skeleton `#f5f5f5` ✅, 라임 spinner 약함 ⚠️ | spinner `#6c9700` |
| `AllergenTag` | radius 4 ⚠️ | 시스템 최소 radius 8 |

> `Modal`(16), `Toast`(12), `Loading`(12)은 모두 둥근 형태인데 `EmptyState`만 각져 있습니다.

---

## 3. Kiosk 컴포넌트

| 컴포넌트 | 발견 사항 | 권장 조치 |
| --- | --- | --- |
| `Kiosk/Header` | 절대 좌표 레이아웃 🔴 | Horizontal Auto Layout |
| `Kiosk/HomeActionButton` | 44px/26px 텍스트 lh AUTO, root radius 없음 | lh 54px / 34px, root radius 24 명시 |
| `Kiosk/CategoryTab` | 높이 52px 🔴, padding 8/12, 30px 텍스트 lh AUTO | 높이 64px, padding 12/16, lh 38px |
| `Kiosk/Category` | 선택 상태가 weight 차이만 있음 | 3px 라임 underline 추가, 32px lh 40px |
| `Kiosk/MenuCard` 🔴 | layout NONE, kcal 28px 과대, radius 0 | Vertical Auto Layout, kcal 16px/lh 24px, radius 16 |
| `Kiosk/MenuCard` | 메뉴명 30px/가격 38px lh AUTO, 가격색 약함 | lh 38px/46px, 가격 `#4A7A00` |
| `Kiosk/MenuDetailSummary` 🔴🔴 | 웹·모바일 크기처럼 작음 | 뱃지 14/20, 이름 28~32/36~40, 설명 16/24, kcal 14~16/20~24, 가격 24~28/32~36 |
| `Kiosk/OptionGroup` 🔴 | 제목·필수·설명 글자 작음, padding 부족 | 20/28 Bold, 14/20, 16/24, padding 20/32 |
| `Kiosk/OptionSelectionRow` 🔴 | radius 0, padding 불균형, 선택 표시 약함 | radius 12, padding 20/24, 옵션 18/26, 추가금액 16/24, 3px border + 체크 아이콘 |
| `Kiosk/QuantityStepper` | 64×64, 기호 20px, 숫자 18px | 버튼 72×72, 기호 24px, 숫자 22~24px |
| `Kiosk/BottomCTA` 🔴 | 전체너비 사각형, radius 0, disabled 문구 혼란 | 좌우 32px margin, 내부 pill radius 20, Text lh 44px, `메뉴를 담아주세요` 또는 opacity 50% |
| `Kiosk/CartItemCard` | 좌우 padding 비대칭, 수정/삭제 버튼 작음 | 좌우 32px, 48px pill 버튼, 상품별 합계 lh 34px |
| `Kiosk/PaymentMethodCard` | 미선택 border 없음 | 1px `#e6e6e6` border |
| `Kiosk/StepIndicator` | 높이 16px | 20~24px |
| `Kiosk/SoldOutBadge` | radius 4 | radius 8 |
| `Kiosk/AllergyAccordion` | 높이 52px, 14px lh AUTO | 높이 60px, 16px/lh 24px |
| `Shared/CartFooterBar` | layout NONE 🔴 | Auto Layout 변환 |
| `Kiosk/CategoryTap` (작은 버전) | 25×11 🔴🔴 | 삭제 또는 Deprecated 처리 |

> `MenuDetailSummary`는 키오스크 폭 1080px에 맞춰 전체 스케일업이 필요합니다.

---

## 4. Admin 컴포넌트

| 컴포넌트 | 발견 사항 | 권장 조치 |
| --- | --- | --- |
| `Admin/Navbar` | 메뉴 lh AUTO, padding 10/12, active가 배경색만 사용 | lh 20px, padding 12/16, 좌측 4px accent bar |
| `Admin/OrderCard` | 옵션 12px, 취소와 완료 호출의 위계 동일 🔴 | 옵션 13~14px, 취소는 텍스트 링크로 격하 |
| `Admin/DataTableRow` 🔴 | 13px lh AUTO, hover 없음, active row 분리 | lh 18px, hover Variant `#f9fafb`, state set으로 통합 |
| `Admin/AnalyticsMetricCard` | 모든 텍스트 lh AUTO | 라벨 14/20, 값 28/34, 변화율 13/18 |
| `Admin/OrderActionButtons` 🔴 | 환불이 일반 버튼과 동일 | 빨간 outline + confirm, 영수증 출력의 primary 여부 확인 |
| `Admin/SoldOutCard` 🔴🔴 | 130×134, 메뉴 11px, 카테고리·뱃지 9px | 150×160, 메뉴 13px, 카테고리 12px, 뱃지 11px |
| `Admin/DetailPanel` | 환불이 영수증 출력과 같은 줄·크기 | 주문 상세 lh 24px, 라벨/값 lh 18px, 환불 시각적 분리 |
| `Admin/ModalActionBar` | 버튼 12px Bold 🔴, 제목 lh AUTO | 버튼 14px, 제목 22/28 |
| `Admin/MenuCard` | `EDITING` 뱃지가 빨강 | 편집은 파랑 또는 노랑 |
| `Admin/StatusBadge` | 11px/16px | 12px 이상 |
| `Admin/SaveBar` | 저장 버튼 강조 약함 | Bold + 배경색 |
| `Admin/HourlySalesChart` | 단일 초록색 | 피크 시간(12~14시)은 더 진한 색 |

### 양호한 Admin 컴포넌트

- `Admin/IngredientCard`: 15/22 Bold, 13/20 Regular ✅
- `Admin/OptionItemCard`: 14/20 Medium ✅
- `Admin/IngredientTableRow`: 14/20, 12/18 ✅

> 9px 텍스트는 웹에서도 읽기 어렵습니다. `Admin/SoldOutCard`는 즉시 수정 대상입니다.

---

## 5. 화면별 피드백

### 05-C. Kiosk

| Screen ID | 화면 | 피드백 |
| --- | --- | --- |
| `SCR-001` | Home | ✅ 다크 배경 + 음식 사진 + 라임 아이덴티티가 좋음. `HomeActionButton`의 lineHeight는 명시 필요 |
| `SCR-003` | Menu List | 🔴 kcal 28px → 16px, 가격 `#6C9700` → `#4A7A00`, disabled CTA 문구 명확화, 선택 카테고리 underline 추가 |
| `SCR-004` | Menu Detail | 🔴 `MenuDetailSummary` 1120px → 1432px 스케일업, `OptionGroup/Row` 폰트 확대, Row radius 12, 장바구니 CTA pill radius 20 |
| `SCR-005` | Cart | 🔴 옵션 수정/삭제 터치 영역 48px 확보, 상품별 합계는 border 또는 배경으로 구분 강화 |
| `SCR-007` | Payment | ⚠️ disabled `결제하기`의 상태를 더 명확하게 표시 |
| `SCR-008` | Order Complete | ⚠️ 주문번호와 안내문 사이 여백 과다. 대기 시간 정보 또는 일러스트 추가 |

### 06-C. Admin

| Screen ID | 화면 | 피드백 |
| --- | --- | --- |
| `SCR-009` | Live Order | 옵션 텍스트는 `#888`로 위계 낮추기. 🔴 취소는 같은 줄·크기의 버튼 대신 텍스트 링크로 |
| `SCR-010` | Order Management | 🔴 DataTableRow hover 추가, DetailPanel의 환불 동작 분리 |
| `SCR-011` | Sold-out Management | 🔴 선택 메뉴 border/체크 표시, 화살표에 `품절 등록 →` / `← 해제` 레이블, SoldOutCard 9px → 12px |
| `SCR-016` | Menu Management | ⚠️ 빨간 `EDITING` 뱃지를 파랑 또는 노랑으로 변경 |
| `SCR-019` | Sales Summary | ⚠️ 시간대별 차트 피크 색상 강조, 결제수단 라벨~% 간격 정렬 |

---

## 6. Line-height 매핑 가이드

| 글자 크기 | Line-height | 용도 |
| --- | --- | --- |
| 44px | 54px | 키오스크 대제목 |
| 38px | 46px | 키오스크 가격 |
| 34px | 44px | CTA |
| 32px | 40px | 카테고리 |
| 30px | 38px | 탭 |
| 28px | 36px | Heading 2 |
| 26px | 34px | 부제 |
| 24px | 32px | — |
| 22px | 28px | Heading 3 |
| 20px | 28px | Body L |
| 18px | 24px | Admin 타이틀 |
| 16px | 24px | Body M |
| 15px | 22px | Admin 본문 |
| 14px | 20px | Body S |
| 13px | 18px | Admin 보조 |
| 12px | 16px | Caption |
| 11px | 16px | 뱃지 최소 |
