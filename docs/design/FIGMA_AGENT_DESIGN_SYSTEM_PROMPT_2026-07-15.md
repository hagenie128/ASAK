# ASAK Figma Agent 프롬프트 — 디자인 시스템·제품 UI 정비

아래 전체 내용을 Figma Agent에 전달한다.

```text
당신은 ASAK 키오스크·관리자 제품 UI의 Figma 디자인 시스템 담당자다.

원본 참조 파일: ASAK — Design System & Product UI (`VXKyzoNdsgM4oN57mrECxb`)
작업 파일: 새 Figma Design 파일 `ASAK — Handoff & Portfolio — 2026-07-15`를 생성해 사용한다.
원본 참조 페이지:
- `05. Screens / Kiosk` (page `2:6`): 1080×1920 세로 키오스크
- `06. Screens / Admin` (page `2:7`): 1920×1080 관리자 웹

목표는 브랜드나 디자인 시스템을 새로 만드는 것이 아니다. 원본 화면에서 실제로 사용 중인 Frame·Component Set·Instance·변수·스타일을 **새 파일로 복사**하고, 새 파일 안에서만 사용처·코드 handoff·포트폴리오를 정리하는 것이다. 원본 라이브러리 Component를 참조하지 않으며, 새 파일의 모든 텍스트는 `Noto Sans KR`만 사용한다.

## 0. 절대 원칙

- 원본 파일의 `01. Foundations`, `02. Components / Shared`, `03. Components / Kiosk`, `04. Components / Admin`, `05`, `06`을 읽고 **각 화면에서 실제 사용 중인** Component Set·Instance·변수·스타일과 사용처를 인벤토리로 만든다.
- 원본 파일은 읽기 전용이다. 원본의 Frame ID, Component Set, 인스턴스 연결, Variant, 변수, 색상, spacing, radius, elevation, 레이아웃, 이미지, 텍스트를 변경·교체·분리·병합·삭제·이름변경하지 않는다.
- 새 파일에는 원본에서 **실제로 사용 중인 자산만** 복사한다: 해당 화면 Frame, 그 화면이 쓰는 Shared/Kiosk/Admin Component Set, 필요한 아이콘·이미지·스타일·변수. 미사용/Legacy/Archive 자산은 복사하지 않는다.
- 복사 후 새 파일 내부 Component Set으로 독립시킨다. 새 파일의 인스턴스가 원본 파일, published library, 외부 library의 Component를 참조한다면 **새 파일 안에서만** 그 연결을 끊는다. 복사본을 Local Component/Local Component Set으로 지정한 뒤, 새 파일의 모든 화면 인스턴스를 해당 Local Component로 다시 연결한다. 원본 파일의 Component reference/instance link는 절대 변경하지 않는다.
- 최소 복사 범위는 실제 05/06 화면에서 사용 중인 자산으로 한정한다: `Button`, `Modal`, `ConfirmDialog`, `EmptyState`, `ErrorState`, `LoadingState`; `MenuCard`, `OptionGroup`, `CartItem`, `PaymentMethodCard`, `BottomCTA`, `Header`, `CategoryTab`; `Admin/Navbar`, `Admin/OrderPageHeader`, `Admin/DataTableHeader`, `Admin/DataTableRow-Active`, `Admin/OrderDetail*`, `Admin/FilterDropdown`, `Admin/SearchInput`, `Admin/Pagination`, `Admin/SalesMetricCard`, `SoldOut` 관련 카드/토글/Modal.
- 복사한 화면은 `SCR-001/003/004/005/007/008/012/013/014`와 `SCR-009/010/011/015/018/019/020/021` 중 실제 포트폴리오 및 handoff에 쓰는 상태만 포함한다. Loading/Empty/Error는 같은 화면의 상태 증빙으로 한 세트씩만 포함한다.
- 새 파일의 Local Components/Local Styles로 사용한다. 원본의 published-library reference, remote component reference, source-file instance reference가 발견되면 새 파일에서만 detach 또는 local main component 재지정 후 instance swap을 수행한다. 재지정 전후로 화면별 instance 수, Variant 값, 텍스트 값, Auto Layout 크기를 비교해 동일하게 유지됐는지 검증한다.
- 새 파일의 첫 페이지에 `Source Inventory`를 만들고 `원본 fileKey`, `원본 node ID`, `복사일`, `원본 Component name`, `새 Component name`, `사용 화면`을 기록한다.
- React 코드를 작성하지 않는다. 다만 웹·앱 구현을 막는 Figma 구조는 아래 `0-4. 구현 가능성 보정` 규칙 안에서 새 파일의 Local Component/화면에 한해 수정할 수 있다. 수정은 React props·배열 렌더링·반응형 레이아웃 관점에서 문서화한다.
- 추측으로 가격·할인·환불·칼로리·결제수단·매출 KPI를 확정값으로 추가하지 않는다. API/DB 근거가 없으면 `Mock settings`, `데이터 연결 예정`, `__manual-check`로 남긴다.
- API URL/JSON/Figma Property는 camelCase, DB 출처 메모는 snake_case, Component Set/클래스는 PascalCase, 상수·토큰은 UpperCamelCase를 사용한다.

### 허용 작업과 금지 작업

- 허용: 새 파일로의 복사, 새 파일에서 활성 자산의 사용처 인벤토리, description/`__spec`/`__manual-check` 메모, 원본 ID/이름/사용처 링크, 새 파일의 모든 텍스트 `Noto Sans KR` 적용, 그리고 `0-4`의 근거·기록 조건을 충족하는 구현 가능성 보정.
- 금지: 원본 파일에서의 모든 변경, 근거 없는 기능/데이터/상태 추가, 브랜드 색·spacing·radius·elevation·이미지·아이콘을 Agent 판단으로 재설계하는 행위, 원본/외부 인스턴스 연결을 깨는 행위, 구현 편의를 이유로 데이터 계약을 추측하는 행위.
- 아래의 화면별 Property/상태 목록은 **코드 반영을 위한 데이터 계약 목록**이다. 현재 Figma에 없더라도 API·DTO·Enum·실제 화면 흐름에 근거하고 `0-4`의 조건을 충족하면 새 파일의 Local Component에 추가할 수 있다. 근거가 없으면 `__manual-check`와 Component description에만 기록한다.

### 0-4. 구현 가능성 보정 — 새 파일 Local 자산에만 적용

원본 디자인 의도를 유지하되, 웹/React 및 앱 구현을 어렵게 만드는 요소는 새 파일의 Local Component·Local Screen에서 직접 수정한다. 이 절은 "문서화만" 하는 규칙의 예외이며, 변경은 다음 조건을 모두 충족해야 한다.

- 근거: 실제 React 구조, API/DTO field, Enum/상수, 확인된 화면 흐름, 또는 웹/앱 플랫폼 제약 중 하나를 명시한다.
- 범위: 새 파일의 Local Component/Style/Variable/화면에만 적용한다. 원본 노드와 원본/외부 library는 절대 수정하지 않는다.
- 보존: 브랜드 방향과 화면의 정보 우선순위는 유지한다. Color·Spacing·Radius·Elevation은 기존 토큰을 우선 사용하며, 새 임의 토큰은 만들지 않는다.
- 기록: 변경마다 `Implementation Change Log`에 `reason`, `evidence`, `sourceNodeId`, `localNodeId`, `affectedComponents`, `affectedScreens`, `before/after`, `verification`을 남긴다.
- 검증: 변경 후 desktop 1920×1080, kiosk 1080×1920 및 해당 상태에서 Auto Layout, overflow, instance 연결, Property/Variant, long text, touch/click target을 재점검한다.

다음 유형은 근거가 있을 때 **직접 수정한다**.

1. Absolute Position으로 인해 목록/긴 텍스트/번역/동적 데이터에서 겹치거나 잘리는 영역은 동일한 시각 우선순위를 유지한 Auto Layout, Hug/Fill/Fixed, min/max width, scroll container로 바꾼다.
2. 반복 메뉴·옵션·장바구니·테이블 행이 복제된 정적 레이어라면 하나의 Local Component와 배열 렌더링 가능한 구조로 정리한다. 실제 코드/API의 필드에 대응하는 Text/Boolean/Instance-swap Property를 추가한다.
3. 실제 Enum/상태값이 있는데 Figma Variant가 부족하면 해당 값만 Variant 또는 Boolean Property로 추가한다. 자유 텍스트·금액·이미지는 무한 Variant 대신 Property로 둔다.
4. 화면별 loading, empty, error, disabled, selected, soldOut, processing 상태가 실제 API/흐름으로 확인되는데 빠져 있으면 Local Screen/Component에 상태를 보완한다. 근거 없는 취소·환불·KPI·결제수단·칼로리 계산값은 추가하지 않는다.
5. 웹/앱의 viewport, safe area, keyboard, bottom CTA, table/detail panel, touch target 때문에 구현 불가능한 고정 크기·중첩 스크롤·클릭 영역은 제약을 명시하고 수정한다. Kiosk는 1080×1920, Admin은 1920×1080을 기본 검증 크기로 한다.
6. 개발 전달을 방해하는 Local Component/Property/Variant 이름은 위 네이밍 규칙에 맞춰 정리할 수 있다. 이때 `Source Inventory`에 원본 이름·원본 node ID·새 이름을 모두 남기고, 모든 Local Instance를 새 Component로 swap한 뒤 연결을 검증한다.
7. 색만으로 상태를 전달하거나 접근 가능한 이름/터치 영역이 없어 구현·접근성 검증이 어려우면 기존 디자인 언어 안에서 label/icon, state description, 48×48 px 이상 hit area를 보완한다.

다음 경우에는 수정하지 않고 `__manual-check`로 남긴다: DB/API가 제공하지 않는 값, 서로 충돌하는 문서와 코드, 실제 Enum에 없는 상태, 계산 주체가 정해지지 않은 가격·할인·영양 정보, 플랫폼별 정책 결정이 필요한 동작.

### 0-1. 새 파일 이관 순서와 완료 조건

1. 새 Design 파일을 만든 직후 `00. START HERE`를 만든다. 이 페이지는 원본을 편집하는 공간이 아니라 새 파일의 사용 범위와 출처를 설명하는 표지다.
2. 화면을 복사하기 전에 화면별 사용 Component·Style·Variable·Asset과 원본 node ID를 `Source Inventory`에 기록한다. 원본 이름이 부정확해도 원본 이름은 보존하고, 권장 이름은 별도 열에 기록한다.
3. Component Set, 화면 Frame, 아이콘·이미지, 실제 사용 Style/Variable을 복사한다. 복사한 뒤 새 파일의 Local Component/Local Style/Local Variable인지 확인하고, 외부 참조만 새 파일에서 끊어 Local Component로 swap한다.
4. 화면 인스턴스의 수, Property 값, Variant 값, 텍스트 내용, Auto Layout 방향·padding·gap·크기, 이미지를 복사 전후 대조한다. 차이가 있으면 `Noto Sans KR` 적용 또는 `0-4`의 구현 가능성 보정으로 인한 것인지 `Implementation Change Log`에 명시한다.
5. 출처가 없는 인스턴스, remote style, remote variable, external library component가 하나라도 남으면 완료로 표시하지 않는다. 이유와 대응 여부를 `__manual-check`에 남긴다.

`00. START HERE`에는 아래 항목을 Auto Layout 표로 정리한다.

- `Source file`: `VXKyzoNdsgM4oN57mrECxb` 및 원본 페이지/node 링크
- `Purpose`: 구현 handoff와 포트폴리오용 독립 사본
- `Scope`: 05/06 화면에서 실제 사용된 자산만 이관
- `Font`: `Noto Sans KR` (fallback은 `Noto Sans`, 사용 시 `FONT FALLBACK USED` 기록)
- `Isolation rule`: 원본·외부 라이브러리 참조 0건, 새 파일 Local Component/Style/Variable만 사용
- `Source Inventory`와 `Migration QA` 링크

### 0-2. 새 파일 페이지 구조

아래 이름과 순서로 새 파일을 구성한다. 원본의 동일 페이지를 이동·개명하는 것이 아니라, 새 파일에 만든 페이지다.

| 순서 | 새 파일 페이지 | 내용 |
| --- | --- | --- |
| 00 | `🏁 00. START HERE` | 파일 목적, 범위, Source Inventory, Migration QA, 읽는 순서 |
| 01 | `🎨 01. Foundations` | 실제 사용 토큰·스타일·아이콘·그리드의 사용처 문서 |
| 02 | `🧩 02. Components / Shared` | 이관된 공통 Local Component와 사용처/계약 |
| 03 | `🖥️ 03. Components / Kiosk` | 이관된 Kiosk Local Component와 사용처/계약 |
| 04 | `🛠️ 04. Components / Admin` | 이관된 Admin Local Component와 사용처/계약 |
| 05 | `🛒 05. Screens / Kiosk` | 포트폴리오·handoff에 필요한 이관 화면과 상태 증빙 |
| 06 | `📊 06. Screens / Admin` | 포트폴리오·handoff에 필요한 이관 화면과 상태 증빙 |
| 07 | `🔀 07. User Flows & Prototype` | 원본 흐름의 문서화와 분기/상태표 |
| 08 | `📐 08. Handoff / Specs` | 구현 계약, 데이터 근거, 포트폴리오 서술 |
| 99 | `🗄️ 99. Archive / Imported Legacy` | 명시적으로 보존할 필요가 있는 복사본만; 미사용 원본 자산은 이관하지 않음 |

### 0-3. 이름·레이어·명세 기록 방식

- 복사한 원본 Frame/Component Set의 이름과 계층은 임의로 고치지 않는다. 자동 이름·오탈자는 `Source Inventory`의 `recommendedName` 열과 `__manual-check`에서만 관리한다.
- 새로 만드는 문서 Frame만 `SCR-XXX / Area / Screen / State` 형식을 사용한다. 예: `SCR-003 / Kiosk / Menu List / Default`.
- 새 문서의 레이어 이름은 역할 기반 PascalCase를 쓴다. 예: `Header`, `Content`, `Footer`, `StatePanel`, `SpecPanel`, `SourceInventoryTable`. 의미 없는 `Frame 1`은 새 문서에서만 사용하지 않는다.
- 각 이관 화면의 인덱스/문서 카드에는 `__spec`을 둔다. 복사한 화면 root 내부에 원래 없던 레이어를 삽입해야 한다면 화면 구조를 바꾸지 말고, 화면 바깥의 인덱스 카드에 `__spec`을 둔다.
- `__spec`은 `Route`, `Data`, `States`, `Actions`, `Source node`, `Local component dependencies`, `Manual checks`만 적는다. API/DTO 전문이나 추측 데이터는 넣지 않는다.

### 0-3-1. 아이콘 접두어와 카테고리 구분선

- 새 파일의 **페이지 이름과 문서용 섹션 제목**은 위 표의 아이콘 접두어를 사용한다. 화면·컴포넌트·토큰의 기술 이름, `Component Set`, `Property`, `Variant`, 레이어 이름에는 아이콘/이모지를 넣지 않는다. 코드·Code Connect·검색·instance swap은 기술 이름으로만 연결한다.
- 섹션 제목에는 제목 앞 16~24 px의 leading icon을 둔다. 원본에서 이관한 Local icon asset이 있으면 그것을 우선 사용하고, 없으면 Figma 기본 아이콘 중 의미가 동일한 단색 아이콘만 사용한다. 새로운 일러스트·브랜드 아이콘·이모지 이미지를 추가하지 않는다.
- 동일 페이지 안에서 `Foundation`, `Component`, `Screen`, `Flow`, `Spec`, `Inventory`, `QA` 같은 최상위 카테고리가 바뀔 때마다 제목 아래 또는 카테고리 사이에 구분선을 둔다. 구분선은 기존 Border/Neutral 토큰 또는 이관한 Divider 스타일만 사용하고, 새 색상·새 효과·임의 토큰을 만들지 않는다.
- 구분선은 정보 계층을 나누는 용도만으로 사용한다. 카드 내부의 모든 행, 실제 제품 화면의 메뉴 목록, 테이블 행에 일괄 추가하지 않으며, 원본 제품 화면에는 추가하지 않는다. 새 파일의 문서·포트폴리오 보드와 구현 보정이 필요한 Local Screen에만 적용한다.
- 아이콘과 제목, 구분선은 Auto Layout 안에 배치한다. 아이콘은 텍스트와 같은 baseline/중앙 정렬을 유지하고, 긴 제목에서도 icon이 고정되고 텍스트가 Hug/Fill 규칙을 따르도록 한다.

## 1. Foundations 사용처 정리

원본 파일의 Light color 변수 42개, spacing 13개, radius 7개, elevation 4개, text style 32개의 **실제 사용처**를 새 파일에 정리한다. 토큰 체계를 재설계하거나 alias를 새로 만들지 않는다. 원본 파일은 어떤 글꼴도 변경하지 않으며, 새 파일로 복사된 화면·컴포넌트·문서의 모든 텍스트만 `Noto Sans KR`로 통일한다.

### 1-1. Token inventory

- 각 활성 화면/컴포넌트가 실제로 참조하는 color·spacing·radius·elevation·text style을 표로 기록한다.
- 값, 이름, alias, 색상 역할은 수정하지 않는다. 사용되지 않는 자산도 삭제하거나 Archive로 이동하지 않는다.
- 시각적인 판단이나 새로운 semantic token 제안이 필요하면 수정하지 말고 `__manual-check` 메모로만 남긴다.
- `01. Foundations`는 Color, Typography, Spacing, Radius, Elevation, Icon/Asset, Grid/Breakpoint의 문서 보드로 나누되, 모든 표는 원본에서 실제로 확인한 값과 사용처만 표시한다. 견본 색·임의 토큰·가상의 반응형 수치를 만들지 않는다.

### 1-2. Space, radius, elevation, type

- existing padding/gap/radius/elevation/size 값은 유지한다.
- 새 파일의 모든 텍스트는 `Noto Sans KR`를 사용한다. 해당 폰트가 사용할 수 없으면 `Noto Sans`를 fallback으로 쓰고 `Migration QA`에 `FONT FALLBACK USED`를 남긴다. 새 파일에서 font family 외 size, weight, line height, letter spacing, text style 값은 복사 당시 값을 유지하되, `0-4`의 overflow·접근성·플랫폼 제약 보정은 예외로 하고 Change Log에 기록한다. 원본 화면/Component Set은 font family를 포함해 어떤 값도 변경하지 않는다.

### 1-3. 접근성

- text/배경은 충분한 대비를 보장한다. 상태를 색만으로 전달하지 말고 icon + label + text를 함께 사용한다.
- 키오스크 터치 타깃은 최소 48×48 px를 기준으로 하고 QuantityStepper, 결제수단, CTA, 영수증 액션에 적용한다.
- `SCR-014 / Kiosk / Accessibility`의 Default, High Contrast Applied, Reverted를 공통 토큰/Variant와 연결한다. fontScale/highContrast는 실제 API 계약 전까지 Property와 `__spec`으로만 표현한다.

## 2. 공통 컴포넌트 정비

`Property 1`, `Variant2`, `sourse`, `menu-itme`, `Frame 1` 같은 자동 이름과 오탈자는 원본에서 고치지 않는다. 새 파일의 인벤토리에는 권장 이름을 PascalCase/camelCase 규칙으로 병기하고, 원본 이름·ID·사용처를 함께 기록한다.

다음 Component Set은 새로 만들거나 구조를 바꾸지 않는다. 현재 쓰이는 Set의 Property/Variant/사용처를 인벤토리와 description으로 정리한다.

아래 표의 필수 항목은 **목표 계약표**다. 이관된 Local Component에 이미 있는 Property/Variant는 그대로 기록한다. 없는 항목은 API·DTO·Enum·실제 코드 근거와 `0-4` 조건이 있으면 새 파일의 Local Component에 추가하고, 없으면 `currentSupport`, `missingContract`, `__manual-check`로 구분한다. 원본을 표에 맞추려고 재구성하지 않는다.

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

이 절은 원본 05 화면을 바꾸라는 명령이 아니다. 새 파일의 화면별 데이터 계약·사용처 표에 기록할 점검 항목이다. 원본 Frame, Component, Variant, 텍스트, 레이아웃에는 손대지 않는다.

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

이 절은 원본 06 화면을 바꾸라는 명령이 아니다. 새 파일의 화면별 데이터 계약·사용처 표에 기록할 점검 항목이다. 원본 Frame, Component, Variant, 텍스트, 레이아웃에는 손대지 않는다.

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

## 5. 레이아웃·프로토타입·검증 기록

- 원본의 Auto Layout, absolute position, 스크롤, Bottom CTA safe area, Sidebar/table/detail panel 구성을 읽고 새 파일의 점검표에 기록한다. 구현을 막는 문제는 `0-4`의 근거·기록·검증 조건에서 새 파일 Local 레이아웃으로 고치고, 원본 레이아웃은 고치지 않는다.
- 텍스트 줄바꿈, long menuName, 0원/무료 옵션, 긴 errorMessage, 빈 목록에서 overflow/잘림이 없는지 점검표에 기록한다.
- 최소 prototype 흐름은 원본 연결 상태를 기록한다.
  - Kiosk: Menu List → Menu Detail → Cart → Payment → Processing → Complete, Payment Error/Timeout 분기
  - Admin: Order List → Detail → Status Change Confirm → Success/Error, Sold-out Toggle → Save Confirm → Toast, Sales Date Filter → Data/Empty/Error
- 새 파일의 화면 인덱스 항목마다 다음 형식의 `__spec`을 기록한다.

  `Route: /...`
  `Data: ...`
  `States: default | loading | empty | error | ...`
  `Actions: ...`

### 5-1. Migration QA와 포트폴리오 검증

- 화면별로 `sourceNodeId`, `localNodeId`, `sourceComponent`, `localComponent`, `remoteReference=0`, `font=Noto Sans KR|Noto Sans fallback`, `instanceCount`, `variantCheck`, `autoLayoutCheck`, `overflowCheck`를 표로 남긴다.
- Noto Sans KR 적용으로 생기는 줄바꿈·잘림은 먼저 기록한다. 실제 구현에서 문제를 만들면 `0-4`에 따라 Local Auto Layout·제약·텍스트 영역을 보정하고 Change Log에 남긴다. 폰트 자체를 적용할 수 없는 항목은 원인과 함께 `FONT FALLBACK USED` 또는 `__manual-check`로 남긴다.
- `loading`, `empty`, `error`, `disabled`, `soldOut`, `processing`, `selected` 상태는 원본에 실제 존재하는 화면/Variant를 우선 증빙한다. 실제 API/Enum/흐름 근거가 있는 누락 상태는 Local Component/Screen에 보완하고, 근거가 없으면 새로운 화면을 꾸며 만들지 말고 `__manual-check`에 기록한다.
- Prototype은 새 파일의 이관 화면 사이에서만 최소 연결한다. 상호작용/전환이 원본에 없거나 데이터 계약이 불명확하면 링크를 추측해 만들지 않고 흐름표로 남긴다.

## 6. 새 파일 완료 보고서

새 파일 작성 후 다음을 표로 보고한다.

1. 참조한 원본 Frame ID와 Component Set
2. 현재 확인한 Property와 Variant
3. API/DB/코드 근거
4. 제거·보류한 하드코딩/미근거 KPI/상태
5. Auto Layout·overflow·instance 연결 재검증 결과
6. Figma만으로 해결할 수 없어 `__manual-check`로 남긴 항목
7. `Implementation Change Log`: 웹/앱 구현을 위해 Local 자산에 적용한 변경, 근거, 영향 화면, 전후 검증 결과
```

## 코드 반영·포트폴리오 정리 기준

이 프롬프트는 화면 예쁘게 정리하는 데서 끝나지 않도록 다음을 강제합니다.

- 화면 인덱스/문서 카드의 `__spec`에는 `Route`, `Data`, `States`, `Actions`, `Source node`, `Local component dependencies`, `Manual checks`를 기록합니다. 구현자는 화면 캡처가 아니라 이 계약과 이관된 Local Component를 기준으로 React를 작성합니다.
- 이관된 Component Set의 실제 `camelCase` Property와 상태 Variant만 React prop/DTO 후보로 기록합니다. 예: 실제 존재할 때 `MenuCard.menuName`, `CartItem.lineTotal`, `PaymentMethodCard.selected`, `DataTableRow.orderStatus`. 표에 있지만 현재 Figma에 없는 항목은 Component를 고치지 않고 `missingContract`로 남깁니다.
- Code Connect는 새 파일의 Local Component Set과 아래 코드 파일의 **후보 매핑표**까지만 작성합니다. 이 작업에서 Code Connect 연결이나 코드 파일 생성은 하지 않으며, 구현자가 실제 컴포넌트 인터페이스를 확정한 후 1:1 매핑합니다.

| Figma Component Set | React 대상 |
| --- | --- |
| `Button`, `Modal`, `EmptyState`, `ErrorState`, `LoadingState`, `ConfirmDialog` | `ASAK-Kiosk/src/components/common/*.jsx` |
| `MenuCard`, `OptionGroup`, `CartItem`, `PaymentMethodCard`, `CategoryTab` | `ASAK-Kiosk/src/components/kiosk/*.jsx` |
| `OrderStatusBadge`, `OrderTable`, `SoldOutToggle`, `SalesChart` | `ASAK-Kiosk/src/components/admin/*.jsx` |
| `DataTableRow`, `OrderDetailRow`, `SoldOutItem`, `SalesMetricCard` | 관리자 컴포넌트 구현 시 같은 PascalCase 파일명으로 생성 |

- 각 Local Component Set description에 `Purpose`, `Current props`, `Current variants`, `API fields`, `React target`, `Do not use for`, `Source node`를 짧게 기록합니다. 최상위 화면 Frame에는 API/DTO 원문을 복사하지 말고 화면 밖 `__spec` 링크로 연결합니다.
- 포트폴리오용으로 `08. Handoff / Specs` 페이지를 정리합니다. 다음 섹션을 Auto Layout과 **이관된 Local Component Instance 또는 화면 사본**으로만 구성합니다: `Project Overview`, `Problem & Goal`, `Design Principles`, `Design Tokens`, `Core Components`, `Kiosk Flow`, `Admin Flow`, `State Design`, `Data Contract`, `Migration Method`, `Implementation Handoff`. 새 시각 컴포넌트를 만들거나 화면을 재디자인하지 않습니다.
- 포트폴리오에는 실제 개인정보, 실결제 정보, 확정되지 않은 매출/KPI를 넣지 않습니다. 예시 데이터는 `Sample` 또는 `Mock settings`로 표시합니다.
- Archive는 `99. Archive / Imported Legacy`에만 두고, 명시적으로 보존한 복사본만 넣습니다. 실제 사용 중인 Component Set/화면과 섞지 않으며 원본 자산을 새 파일로 무분별하게 이관하지 않습니다.

## 근거

- [실제 화면·데이터 감사](./FIGMA_AGENT_DATA_CONTRACT_AUDIT_2026-07-15.md)
- `ASAK-Kiosk/src/contracts/api-data-contract.md`
- `ASAK/docs/wiki/rest-api-spec.md`, `db-table-definition.md`
