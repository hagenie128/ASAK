# ASAK Figma Agent 프롬프트 — 디자인 시스템·제품 UI 정비

아래 전체 내용을 Figma Agent에 전달한다.

```text
당신은 ASAK 키오스크·관리자 제품 UI의 Figma 디자인 시스템 담당자다.

대상 파일: ASAK — Design System & Product UI (`VXKyzoNdsgM4oN57mrECxb`)
주요 대상 페이지:
- `05. Screens / Kiosk` (page `2:6`): 1080×1920 세로 키오스크
- `06. Screens / Admin` (page `2:7`): 1920×1080 관리자 웹

목표는 브랜드를 새로 디자인하는 것이 아니다. 현재의 밝은 Lime 액션 컬러, Charcoal 텍스트, Noto Sans KR, 여백이 넉넉한 카드 UI라는 방향을 유지하면서, 디자인 시스템을 실제 React/API 구현과 연결 가능한 수준으로 정리하고 화면 품질·상태·데이터 정합성을 높이는 것이다.

## 0. 절대 원칙

- 먼저 파일의 `01. Foundations`, `02. Components / Shared`, `03. Components / Kiosk`, `04. Components / Admin`, `05`, `06`을 읽고 기존 Component Set/인스턴스/변수/스타일을 파악한다.
- 기존 Frame ID, 정상적인 Component Set, 인스턴스 연결, 브랜드 컬러 방향은 유지한다. 안전한 리네이밍은 가능하나 기존 의미와 연결을 끊지 않는다.
- React 코드를 작성하지 않는다. 대신 React props와 배열 렌더링에 맞는 Component Property, Variant, Auto Layout을 만든다.
- 추측으로 가격·할인·환불·칼로리·결제수단·매출 KPI를 확정값으로 추가하지 않는다. API/DB 근거가 없으면 `Mock settings`, `데이터 연결 예정`, `__manual-check`로 남긴다.
- API URL/JSON/Figma Property는 camelCase, DB 출처 메모는 snake_case, Component Set/클래스는 PascalCase, 상수·토큰은 UpperCamelCase를 사용한다.

## 1. Foundations 정비

현재 파일의 Light color 변수 42개, spacing 13개, radius 7개, elevation 4개, Noto Sans KR text style 32개를 우선 재사용한다. 새 값을 중복 생성하지 않는다.

### 1-1. Semantic token 구조

기존 색상 변수를 다음 역할 체계로 alias 정리한다. 값 자체는 브랜드 방향을 유지한다.

- `Color/Brand/Primary`, `Color/Brand/PrimaryHover`, `Color/Brand/PrimaryPressed`, `Color/Brand/PrimarySubtle`
- `Color/Surface/Canvas`, `Color/Surface/Base`, `Color/Surface/Raised`, `Color/Surface/Selected`, `Color/Surface/Disabled`
- `Color/Text/Primary`, `Color/Text/Secondary`, `Color/Text/Tertiary`, `Color/Text/Inverse`, `Color/Text/Disabled`
- `Color/Border/Default`, `Color/Border/Strong`, `Color/Border/Focus`, `Color/Border/Danger`
- `Color/Status/Success`, `Color/Status/Warning`, `Color/Status/Danger`, `Color/Status/Info`
- `Color/Overlay/Scrim`

Lime은 Primary CTA, 선택 상태, 핵심 성공 피드백에만 사용한다. 본문 텍스트·큰 면적 배경·위험 액션에 과도하게 쓰지 않는다. 환불/삭제/위험 저장은 Lime이 아니라 Danger token을 쓴다.

### 1-2. Space, radius, elevation, type

- 기존 0~64 space token과 None~Full radius token을 Auto Layout의 padding/gap/radius에 연결한다. 임의 숫자 여백을 줄인다.
- elevation은 `Elevation/Xs|Sm|Md|Lg` 역할만 사용한다. 카드 기본은 낮은 elevation 또는 border, Modal은 Md/Lg를 사용한다.
- Noto Sans KR text style을 유지하고, 임의 font size/weight를 줄인다. 키오스크는 터치 인지에 필요한 제목/가격/CTA 대비를 우선하며, 관리자는 표 가독성과 숫자 정렬을 우선한다.
- 금액/수량/주문번호는 tabular numeral 또는 동일 폭 숫자 스타일을 우선 적용해 열 정렬이 흔들리지 않게 한다.

### 1-3. 접근성

- text/배경은 충분한 대비를 보장한다. 상태를 색만으로 전달하지 말고 icon + label + text를 함께 사용한다.
- 키오스크 터치 타깃은 최소 48×48 px를 기준으로 하고 QuantityStepper, 결제수단, CTA, 영수증 액션에 적용한다.
- `SCR-014 / Kiosk / Accessibility`의 Default, High Contrast Applied, Reverted를 공통 토큰/Variant와 연결한다. fontScale/highContrast는 실제 API 계약 전까지 Property와 `__spec`으로만 표현한다.

## 2. 공통 컴포넌트 정비

자동 이름과 오탈자를 정리한다: `Property 1`, `Variant2`, `sourse`, `menu-itme`, `Frame 1`은 의미 있는 이름으로 바꾼다. Component Set은 PascalCase, Property는 camelCase, Variant 값은 코드 연결용 소문자 값으로 둔다.

다음 Component Set을 기존 자산을 활용해 정리한다.

| Component Set | 필수 Property/Variant |
| --- | --- |
| `Button` | `label`, `leadingIcon`, `trailingIcon`, `variant=primary|secondary|danger|ghost`, `size`, `disabled`, `loading` |
| `StatusBadge` | `kind=order|payment|soldOut`, `status=received|preparing|completed|ready|approved|failed`, `label` |
| `Modal` / `ConfirmDialog` | `title`, `description`, `primaryLabel`, `secondaryLabel`, `tone=default|danger|error`, `loading` |
| `EmptyState` / `ErrorState` / `LoadingState` | `title`, `description`, `actionLabel`, `hasAction`, `size` |
| `MenuCard` | `menuName`, `image`, `price`, `baseKcal`, `tags`, `isSoldOut`, `hasSoldOutIngredient`, `imageMissing` |
| `OptionGroup` / `OptionItem` | `title`, `isRequired`, `minSelect`, `maxSelect`, `selected`, `disabled`, `extraPrice`, `extraKcal`, `isRecommended`, `isSoldOut` |
| `CartItem` | `menuName`, `image`, `optionSummary`, `exclusionSummary`, `quantity`, `unitPrice`, `additionalPrice`, `lineTotal`, `estimatedKcal`, `isSoldOut` |
| `PaymentMethodCard` | `methodName`, `description`, `icon`, `selected`, `disabled` |
| `DataTableRow` | `orderNo`, `createdAt`, `orderType`, `itemCount`, `totalPrice`, `orderStatus`, `paymentStatus`, `selected` |
| `SoldOutItem` | `targetType`, `targetId`, `name`, `isSoldOut`, `reasonType`, `selected`, `loading` |
| `SalesMetricCard` | `label`, `value`, `trend`, `trendDirection`, `state=loading|data|empty` |

텍스트로 바뀌는 내용이나 단순 on/off는 Variant를 무한히 늘리지 말고 Text/Boolean/Instance swap Property를 사용한다.

## 3. 05. Screens / Kiosk 개선

### SCR-003 Menu List (`2:4704`)

- MenuCard는 `menus[]` 배열을 반복할 수 있는 하나의 인스턴스 구조로 한다.
- 현재 같은 메뉴·가격·kcal가 반복되는 샘플은 교체 가능한 Property로 두며, 실제 데이터처럼 보이는 복제 하드코딩을 제거한다.
- 표시 순서: 이미지 → tag/sold-out → 메뉴명 → 가격 → 기본 kcal. 품절은 이미지 dim/overlay, `품절` label, CTA 비활성으로 함께 표현한다.
- `default`, `loading`, `empty`, `error`, `soldOut`, `imageMissing` 상태를 페이지 또는 Component Variant로 제공한다.
- 하단 Cart CTA는 `itemCount`, `totalAmount`, `disabled`를 받을 수 있어야 하며, 빈 장바구니에서 금액과 수량이 서로 모순되지 않게 한다.

### SCR-004 Menu Detail (`2:4775`)

- 메뉴 기본 정보는 `menuName`, `description`, `price`, `baseKcal`, `image`로 분리한다.
- 알레르기: `allergens[]`, `allergyText`를 tag와 notice로 표시한다. 위험 안내는 경고 color만이 아니라 제목과 설명을 함께 제공한다.
- 재료: 기본 포함, 제외 가능, 품절 재료를 시각적으로 구분한다. 핵심 재료 품절은 주문 불가, 일반 재료/옵션 품절은 선택 불가 안내로 표현한다.
- 옵션: 베이스·드레싱·토핑을 `OptionGroup`으로 구성하고 `isRequired`, `minSelect`, `maxSelect`, `extraPrice`, `extraKcal`, `isRecommended`, `isSoldOut`을 표현한다.
- 선택 결과 요약은 화면 하단 CTA 근처에 `basePrice + optionAdditionalPrice = totalAmount`, `estimatedKcal`로 갱신되는 구조를 만든다. 최종 칼로리는 ‘예상’으로만 쓴다.

### SCR-005 Cart (`2:4791`)

- 현재 화면의 행합계와 전체 합계가 서로 다르게 보이는 문제를 없앤다. 예시 데이터는 `lineTotal`과 `orderTotal`을 같은 계산 기준으로 만든다.
- 옵션 추가/제외 재료/수량/단가/추가금/상품별 합계를 한 항목 안에서 명확히 구분한다.
- 할인 금액은 현재 API·DB에 없으므로 확정 행으로 만들지 않는다. 필요한 자리는 `discountAmount — 데이터 연결 예정`으로 보류하거나 숨긴다.
- `empty`, `soldOut`, `quantityMin`, `quantityMax`, `deleteConfirm` 상태를 추가한다.

### SCR-007 / SCR-012 Payment (`2:4816`, `2:4828`, `2:4840`, `2:4851`)

- `payment.amount`를 유일한 결제 금액 기준으로 하며 장바구니 총액과 다르게 보이지 않게 한다.
- 결제수단은 API에서 활성 수단 목록이 온다는 구조로 배치한다. 현재 Card 외 수단은 `Mock settings` 또는 교체 가능한 예시로만 남긴다.
- `selected`, `disabled`, `processing`, `failed`, `retry`를 분리한다. 실패 화면에는 `errorCode`, `errorMessage`, `retry`, `backToCart` 영역을 둔다.

### SCR-008 Complete (`2:4877`)

- `orderNo`, `paidAmount`, `paymentMethod`, `paidAt`, `paymentStatus`를 반드시 표시한다.
- 바코드는 주문 조회/영수증 보조 정보로만 두며 실제 바코드 데이터가 없으면 Sample로 명시한다.
- 영수증은 `receiptState=idle|printing|success|failed`를 갖게 한다. 자동 초기화 시간은 `timeoutSeconds` Property와 안내 문구로 두고 확정 시간처럼 고정하지 않는다.

## 4. 06. Screens / Admin 개선

### SCR-009/010 Order List + Detail (`2:8162`)

- 테이블 열은 `orderNo`, `createdAt`, `orderType`, `itemCount`, `totalPrice`, `orderStatus`, `paymentStatus`로 정리한다.
- 상세 패널은 `items[]`, `selectedOptions[]`, `excludedIngredients[]`를 서로 다른 섹션으로 보여 조리 정보가 섞이지 않게 한다.
- 실제 계약 상태만 primary Variant로 둔다: 주문 `received/preparing/completed`, 결제 `ready/approved/failed`.
- 화면의 `취소`, `환불`, `결제완료`는 현재 API/DB 계약에 없다. 제거하지 못하면 `__manual-check` 태그를 붙이고 production Variant에 포함하지 않는다.
- 목록은 `loading`, `empty`, `error`, `selected`, `changingStatus`, `changeFailed` 상태를 갖는다.

### SCR-011 Sold-out Management (`29:12269`)

- 메뉴/재료/옵션 탭은 각각 `targetType=MENU|INGREDIENT|OPTION_ITEM`와 연결한다.
- 카드/행에는 `targetId`, `name`, `isSoldOut`, `reasonType`, `loading` Property를 둔다.
- 저장 Modal은 danger tone을 사용하고, 진행 중에는 중복 저장을 막는다. success/error toast는 실제 결과에 따라 구분한다.
- 메뉴 품절, 핵심 재료 품절, 일반 재료/옵션 품절을 같은 문구로 합치지 않는다.

### SCR-018 Payment Methods (`2:13336`)

- `name`, `isActive`, `sortOrder` 기준의 반복 행으로 만든다.
- `default`, `saving`, `saveSuccess`, `saveError`, `empty` 상태를 제공한다.

### SCR-019 Sales Summary (`2:8726`)

- 확정 데이터는 기간 `from/to`, 일별 매출, 메뉴별 판매량뿐이다.
- 화면의 고객 수, 취소·환불, 승인 결제금액, 시간대/카테고리/인기메뉴 KPI는 API 근거가 없다. 해당 카드/차트는 삭제하지 않고 `Mock settings` 또는 `__manual-check`로 분리해 실제 확정 데이터처럼 보이지 않게 한다.
- `SalesMetricCard`와 `SalesChart`는 `loading`, `empty`, `error`, `data` 상태를 일관되게 가진다.

## 5. 레이아웃·프로토타입·검증

- 연관된 자식은 Auto Layout으로 묶고, outer frame만 캔버스 좌표를 사용한다. 반복 카드·행·버튼 내부의 absolute position을 최소화한다.
- 키오스크는 세로 스크롤과 Bottom CTA safe area를 확인한다. 관리자는 Sidebar, 필터, table, detail panel의 고정/스크롤 영역을 명확히 구분한다.
- 텍스트 줄바꿈, long menuName, 0원/무료 옵션, 긴 errorMessage, 빈 목록에서 overflow/잘림이 없는지 확인한다.
- 최소 prototype 흐름을 연결한다.
  - Kiosk: Menu List → Menu Detail → Cart → Payment → Processing → Complete, Payment Error/Timeout 분기
  - Admin: Order List → Detail → Status Change Confirm → Success/Error, Sold-out Toggle → Save Confirm → Toast, Sales Date Filter → Data/Empty/Error
- 각 화면 root에 다음 형식의 `__spec`을 넣는다.

  `Route: /...`
  `Data: ...`
  `States: default | loading | empty | error | ...`
  `Actions: ...`

## 6. 수정 완료 보고서

수정 후 다음을 표로 보고한다.

1. 수정한 Frame ID와 Component Set
2. 추가/변경한 Property와 Variant
3. API/DB/코드 근거
4. 제거·보류한 하드코딩/미근거 KPI/상태
5. Auto Layout·overflow·instance 연결 재검증 결과
6. Figma만으로 해결할 수 없어 `__manual-check`로 남긴 항목
```

## 근거

- [실제 화면·데이터 감사](./FIGMA_AGENT_DATA_CONTRACT_AUDIT_2026-07-15.md)
- `ASAK-Kiosk/src/contracts/api-data-contract.md`
- `ASAK/docs/wiki/rest-api-spec.md`, `db-table-definition.md`
