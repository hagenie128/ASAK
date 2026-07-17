# ASAK Figma Implementation Final 정량 QA

> 작성일: 2026-07-17  
> 대상 파일: `JSrjOy668zhfkiLplCkreh`  
> 대상 페이지: Foundations `148:12745`, Shared `145:2`, Kiosk Components `150:2`, Admin Components `150:2860`, Kiosk Screens `134:7720`, Admin Screens `134:10606`  
> 방식: Figma 읽기 전용 노드 추출. 이 문서는 Figma나 소스코드를 수정하지 않는다.

## 1. 결론

화면 상태의 범위와 컴포넌트의 기능 분류는 충분하다. 키오스크는 **66개 프레임**, 관리자는 **72개 프레임**으로 Default·Loading·Empty·Error·Saving·Toast·확인 모달까지 설계되어 있다.

다만 화면 반영 전에 아래 5개를 먼저 정리해야 한다.

| 우선순위 | 확인 가능한 사실 | 화면 반영 전 처리 |
|---|---|---|
| P0 | Foundations 표지에는 Primitive 80 / Semantic 47로 표시되지만, 실제 컬렉션은 Primitive **83개** / Semantic **51개**다. | 표지 수치를 `83 / 51`로 고치거나, 집계 기준을 표지에 명시한다. |
| P0 | `day` 컴포넌트 세트(`389:44743`)는 Figma가 `variantGroupProperties`를 읽을 때 오류를 반환한다. | Variant 오류를 먼저 해소한다. 이 상태에서는 개발자가 Variant 속성을 신뢰할 수 없다. |
| P0 | 화면 텍스트 스타일 미연결 비율: Kiosk Screens **2470 / 2536 (97.4%)**, Admin Screens **5868 / 6002 (97.8%)**. | 화면 텍스트를 14개 `ASAK/*` Text Style로 연결한다. 단순히 px가 같은지보다 “Style ID가 연결됐는지”가 기준이다. |
| P1 | 키오스크의 실제 선택 표시·탭·칩 내부 높이가 **20·28·32·38·42px**인 사례가 반복된다. | 내부 아이콘 크기와 별개로 실제 클릭 프레임을 **최소 64×64px**로 만든다. |
| P1 | 관리자의 MenuButton은 **16×16px**, Checkbox는 **20×20px**, DateSelector는 **232×35px**다. | 웹은 클릭 영역 **최소 40×40px**, 태블릿 터치 가능 화면은 **44×44px**로 확장한다. 아이콘은 가운데 16~20px로 유지한다. |

## 2. 검토 기준

프로젝트 토큰 문서의 8px 그리드를 기준으로 삼되, 아래 값은 허용한다.

- 아이콘과 텍스트의 미세 간격: 4px
- 배지 내부 여백: 4px 또는 6px
- 본문 계층: 12 / 16 / 20 / 24 / 28 / 36 / 48 / 64px
- 키오스크 조작: 터치 영역 64px 이상, 보조 터치 영역도 56px 이상
- 관리자 웹: 마우스 조작 40px 이상, 태블릿 가능 화면은 44px 이상
- 본문 줄간격: 16px 글자에는 24px, 14px 글자에는 20px, 12px 글자에는 16px 이상

`8px grid`는 모든 수가 8의 배수여야 한다는 뜻이 아니다. 4px·12px·20px은 역할이 명확하면 유지할 수 있다. 문제는 같은 역할의 컴포넌트가 10px, 12px, 14px, 18px, 20px을 무작위로 섞는 경우다.

## 3. Foundations — `148:12745`

### 실제 자산

| 항목 | 실제 수치 | 피드백 |
|---|---:|---|
| Primitive 변수 | 83개 | 표지의 80과 불일치. 표지 갱신 필요. |
| Semantic 변수 | 51개, Default / High Contrast 2개 모드 | 표지의 47과 불일치. High Contrast 모드는 이미 있으므로 화면 적용 범위를 명시해야 한다. |
| Text Style | 14개 | Display 2, Heading 3, Body 3, Label 3, Number 3. 구성이 충분하다. |
| Effect Style | 3개 | Subtle, Floating, Focus Ring. 관리자 카드/모달 외 과사용 금지. |
| 변수 scope | Primitive 83개와 Semantic 51개 모두 `ALL_SCOPES` | 색·간격·폰트 선택기에 불필요한 변수가 모두 노출된다. 다음 정리 때 Color는 `TEXT_FILL` / `FRAME_FILL`, Spacing은 `GAP` / `WIDTH_HEIGHT`, Radius는 `CORNER_RADIUS`처럼 scope를 나눈다. |

### 색상

현재 핵심 색상은 Brand Lime `#B5E30F`, Dark Surface `#1A1A1A`, Admin text `#111827`, dark green `#243300`, secondary green `#5B8C2A`다.

| 조합 | 대비비 | 사용 규칙 |
|---|---:|---|
| `#B5E30F` 위 `#000000` | **13.97:1** | 활성 탭·강조 버튼·선택 surface에 적합. |
| `#B5E30F` 위 `#FFFFFF` | **1.50:1** | 흰 글자/아이콘 금지. 장식선도 정보 전달에 사용하지 않는다. |
| `#5B8C2A` 위 `#FFFFFF` | **4.01:1** | 14px 이하 본문에는 부족하다. 큰 제목 또는 비텍스트 장식에만 사용하거나 `#243300`으로 내린다. |
| `#243300` 위 `#FFFFFF` | **13.58:1** | 라임 계열 텍스트가 꼭 필요할 때의 기본 텍스트 색으로 사용한다. |

색의 방향은 좋다. 검정/백색/라임의 대비가 강해 키오스크에서 빠르게 인식된다. 반대로 밝은 라임을 문장 텍스트에 쓰면 제품 UI보다 장식 보드처럼 보이고 읽기성이 떨어진다. 라임은 면적·선택·포커스, `#111827` 또는 `#243300`은 텍스트로 역할을 고정한다.

### 타이포그래피

정의된 스타일은 다음 14개다.

| 계열 | size / line-height | 화면 적용 |
|---|---|---|
| Display XL / L | 64/76, 48/58 | 시작·완료 같은 1개 메시지 화면에만 |
| Heading 1 / 2 / 3 | 36/44, 28/36, 22/28 | 키오스크 섹션 제목, 관리자 페이지 제목 |
| Body L / M / S | 20/28, 16/24, 14/20 | 설명·목록 본문 |
| Label L / M / S | 20/24, 16/20, 12/16 | 버튼·필드·상태 라벨 |
| Number XL / L / M | 48/56, 34/40, 26/32 | 결제금액·KPI 수치 |

Foundation 자체도 273개 텍스트 중 259개가 Text Style ID에 연결되지 않았다. 토큰 보드는 설명용 텍스트가 많아 일부 예외가 가능하지만, 최소한 위 14개 예시와 화면에 사용할 대표 텍스트는 Style을 붙여야 개발 전달 수치가 흔들리지 않는다.

## 4. Shared Components — `145:2`

### 페이지 수치

- Component Set 8개, Component 56개, Text 355개
- Text Style ID 미연결: 117 / 355 (**33.0%**)
- Auto layout: 461개, non-auto layout: 4개
- 대표 spacing: 12px gap, 버튼 세로 padding 14px, ConfirmDialog 내부 gap 20px

### 컴포넌트별 피드백

| 컴포넌트 | 현재 Variant / 크기 | 반영 피드백 |
|---|---|---|
| `Shared/Modal` | type: paymentError / timeout / information, 각 480×196 | 화면 모달의 base 폭을 480으로 고정한 점은 관리자에 적합하다. 버튼 48px 높이를 유지하고, 키오스크에는 이 컴포넌트를 그대로 재사용하지 말고 최소 64px CTA를 별도 Variant로 둔다. |
| `Shared/ConfirmDialog` | type 6개, tone 2개, state 2개, component 440×248 | 속성값은 6×2×2지만 실제 사용 가능한 조합이 전부 존재한다는 보장이 없다. `allowed combinations`을 컴포넌트 설명에 적어 개발자가 없는 Variant를 고르지 않게 한다. |
| `Shared/Toast` | tone 5개 × size 2개, 299×76 | 화면의 toast는 76px 높이로 충분하다. 본문은 14/20, 아이콘은 20px, 좌우 padding 16~20px으로 고정한다. longMessage는 2줄을 넘기지 않는다. |
| `Shared/EmptyState` | type 7개, 400×216 또는 400×280 | `orders`, `sales`, `searchResult`처럼 216px인 유형과 280px인 유형의 차이를 의도적으로 문구/CTA 유무로 설명한다. 단순한 높이 차이면 240px 또는 280px으로 통일한다. |
| `Shared/ErrorState` | type 4개, layout page/section/inline, 280~480×172~248 | type와 layout의 모든 조합이 존재하지 않는다. 가능한 조합표를 컴포넌트 설명에 붙이고, retry CTA는 page/section에서 48px으로 통일한다. |
| `Shared/LoadingState` | card 300×184, table 600×120, page 400×300, button 120×40 | Button loading 높이 40px은 관리자 웹에만 허용한다. 키오스크 CTA loading은 `Kiosk/BottomCTA` 64px 이상으로 표현한다. |
| `AllergenTag` | default / warning, 61×32 | 32px은 정보 배지 크기다. 버튼처럼 쓰지 않는다. warning은 색만으로 전달하지 말고 알레르겐명과 아이콘을 같이 유지한다. |
| `AllergenNotice` | default / hasAllergen / optionChanged, 480×76 | 76px 안에서 14/20 본문 2줄이 안정적으로 보인다. `optionChanged`에는 변경 전·후 이름을 동시에 넣지 말고 “옵션이 변경됨” + 상세 보기로 분리한다. |
| `Shared/Icon/*` | CaretLeft / CaretRight / Placeholder, 각 32×32 | 32px은 아이콘 box이지 클릭 영역이 아니다. 상위 버튼을 44×44(관리자) 또는 64×64(키오스크)로 만든다. |

`Deprecated/Modal-Confirm`, `Deprecated/Modal-Duplicate`, `Deprecated/ConfirmDialog-Legacy`, `Deprecated/Admin-EmptyState`, `Deprecated/Admin-ErrorState`가 같은 페이지에 남아 있다. 화면 프레임에서 Deprecated instance가 0개인지 확인한 뒤 삭제 후보로 분리한다. 현재 상태 그대로 두면 새 화면에서 잘못 선택될 가능성이 높다.

## 5. Kiosk Components — `150:2`

### 페이지 수치

- Component Set 18개, Text 786개, Auto layout 975개 / non-auto 133개
- Text Style ID 미연결: 777 / 786 (**98.9%**)
- 자주 쓰인 숫자: 16/24 100개, 24/auto 92개, 20/28 73개, 20/auto 76개
- 8px 기준 밖 수치: gap 2px 95개, gap 14px 66개, gap 10px 61개, padding 30px 54개

`auto` 줄간격은 키오스크에서 줄바꿈 시 높이가 달라질 수 있다. 화면으로 나가는 텍스트는 `24/30`, `20/28`, `16/24`, `14/20`, `12/16`처럼 line-height를 명시한다.

### 컴포넌트별 피드백

| 컴포넌트 | 현재 Variant | 반영 피드백 |
|---|---|---|
| `Kiosk/PaymentMethodCard` | method 4, selected true / false / none, size L / S | `false`와 `none`의 의미가 겹친다. `state=default/selected/disabled`로 합치고 payment method는 `method`로 유지한다. |
| `Kiosk/QuantityStepper` | default / minusDisabled / menuLimitReached / cartLimitReached / pressed | 버튼 시각 상태와 수량 제한 사유가 한 축에 섞였다. `state=default/pressed/disabled`, `limitReason=none/menu/cart` 2축으로 분리한다. |
| `Kiosk/OrderSummaryInfo` | `상태=접힘/펼침` | 속성명을 `state=collapsed/expanded`로 통일한다. 화면 코드와 Figma property를 같은 영문 값으로 맞춘다. |
| `Kiosk/OrderDetailRow` | default / disabled / pressed / error / minusActive / minusDefault / selected | minus의 표현은 버튼 상태이지 row 상태가 아니다. Row는 selection/error/disabled만 두고 stepper를 내부 instance로 분리한다. |
| `Kiosk/StepIndicator` | step 1 / 2 / 3 / start / step5 | 숫자와 단어가 섞였다. `currentStep=0/1/2/3/4` 또는 `stage=start/menu/cart/payment/complete` 중 하나만 사용한다. |
| `Kiosk/BottomCTA` | layout 3, state default / disabled / loading | 키오스크 핵심 CTA다. 모든 Variant의 실제 클릭 면적을 **1080px frame 기준 높이 112px 이상**, 내부 텍스트 24/30 이상으로 유지한다. |
| `Kiosk/CartItemCard` | State Default / Disabled / SoldOut | property 대문자 `State`를 `state`로 바꾸고, SoldOut에는 편집 CTA/결제 차단 문구가 있는 화면 Variant와 연결한다. |
| `Shared/CartFooterBar` | cartState ready / empty / loading | Kiosk 페이지에만 있는 자산이다. 다른 도메인 재사용 의도가 없으면 `Kiosk/CartFooterBar`로 rename한다. |
| `Kiosk/MenuCard` | default / soldOut | soldOut은 overlay opacity만으로 처리하지 말고 이미지·이름·가격·CTA의 상태를 한 Variant 안에 명시한다. 화면에는 sold-out 프레임이 이미 존재한다. |
| `Kiosk/CategoryTab` | active / inactive / disabled | `Kiosk/CategoryTap`도 별도로 존재한다. `Tap`은 오타 또는 중복이므로 한 컴포넌트만 남긴다. |
| `Kiosk/Category` | page K / A | `K/A`는 개발자가 의미를 알기 어렵다. `surface=kiosk/admin` 또는 도메인 분리가 더 명확하다. |
| `Kiosk/HomeActionButton` | eatIn / takeOut | 두 선택지는 키오스크 첫 행동이다. 실제 터치 영역을 **최소 240×240px**, 라벨 28/36 이상으로 둔다. |
| `Kiosk/CategoryTap` | Size s / L, active none / active | `Kiosk/CategoryTab`과 합친 뒤 property는 `size=sm/lg`, `state=default/active/disabled`로 고정한다. |
| `Kiosk/MenuDetailSummary` | default / optionSelected / quantityChanged / loading / MenuDetailSummary | `MenuDetailSummary`는 state가 아니다. 제거하고 나머지 4개만 유지한다. |
| `Kiosk/OptionGroup` | default / disabled | 필수/선택/다중선택은 화면 동작에 필요하므로 `selectionType` 또는 `required` property를 추가한다. |
| `Kiosk/OptionSelectionRow` | selectionType 3, state 5 | 구조가 가장 명확한 편이다. 현재 indicator는 20×20px이므로 row 전체를 72px 이상 클릭 가능하게 하고 indicator 자체를 클릭 target으로 쓰지 않는다. |
| `Kiosk/AllergyAccordion` | collapsed / expanded | accordion header는 72px 이상, 내부 칩은 정보용 32~40px으로 제한한다. |
| `Kiosk/SoldOutBadge` | tone=soldOut, size 3 | tone 값이 1개뿐이므로 tone property를 제거한다. size만 남기거나 badge를 하나의 fixed component로 둔다. |

### 실제 작은 컨트롤 후보

| 노드 | 현재 크기 | 조치 |
|---|---:|---|
| `tab-side` | 83×38px | 키오스크에서는 상위 탭 영역을 높이 64px 이상으로 확장. |
| `selection-indicator` | 20×20px | row 전체(최소 64px 높이)를 선택 target으로 만든다. |
| `Admin/MenuButton`가 Kiosk 카드 내부에 노출 | 28×28px | 키오스크 화면에서는 재사용 금지 또는 wrapper 64×64px로 확장. |
| option selection value | 높이 28~32px | 표시용 칩이면 유지, 클릭용이면 64px row로 분리. |

## 6. Admin Components — `150:2860`

### 페이지 수치

- Component Set 41개, Component 188개, Text 1409개
- Text Style ID 미연결: 1339 / 1409 (**95.0%**)
- `day` Component Set `389:44743`은 Variant property 읽기 오류가 발생한다.

### 컴포넌트별 피드백

| 컴포넌트 | 현재 속성 | 반영 피드백 |
|---|---|---|
| `Admin/MenuButton` | type `+ / Variant4 / side / x` | `Variant4`를 의미 있는 `remove` 또는 `close`로 rename. 실제 16×16 아이콘은 40×40 또는 44×44 wrapper 필요. |
| `Admin/OrderMenuOptionItem` | type `+ / - / base / drink / set / side / sourse` | `sourse` 오타를 `sauce`로 수정. action(+/-)과 item type을 서로 다른 property로 분리. |
| `Admin/DataTableRow` | state default / hover / selected | row 높이는 최소 48px, 데이터가 조작 대상이면 56px을 권장. hover와 selected의 배경색은 동시에 구분되어야 한다. |
| `Admin/SalesMetricCard` | metric 4, state default/loading/empty | KPI는 Number XL/L/M Style만 사용. 값 0, `-`, loading skeleton의 폭을 같은 baseline에 맞춘다. |
| `Admin/OrderCard` | `포장여부`, `열` | property를 `fulfillment`, `columns`로 통일하고, 값도 `dineIn/takeOut`, `one/two`로 명시한다. |
| `Admin/Navbar` | Model Desktop / Tablet / Mobile / Mobile Back / logo / error | breakpoint와 상태가 한 property에 섞였다. `viewport=desktop/tablet/mobile`, `mode=default/back`, `state=default/error`로 분리. |
| `Admin/DataTableRow-Active` | status 4 | DataTableRow의 selected와 역할이 겹친다. row 기본 컴포넌트의 `status` property로 병합 여부를 결정한다. |
| `Admin/FilterDropdown` | default/active/open | `active`와 `open`을 구분한다. focus ring은 `ASAK/Focus Ring`, open은 menu visible로 정의한다. |
| `Admin/OrderActionButtons` | detail/refund | 위험 행동 refund는 primary CTA와 같은 라임을 쓰지 않고 danger token을 사용한다. |
| `Admin/SalesPeriodFilter` | default/loading | DateSelector와 기능이 중복될 수 있다. 날짜 범위/월 단위의 책임을 component description으로 분리한다. |
| `Admin/StatusBadge` | Role 13개 | 역할·상태·재료분류가 한 property에 섞였다. `category`, `availability`, `required`로 분리한다. |
| `Admin/SoldOutCard` | Selected false/true | 선택뿐 아니라 `soldOut/available` 데이터 상태를 별도 property로 둔다. |
| `Admin/SaveBar` | dirty/saving/success/error | 좋은 상태 축이다. success는 2~3초 toast와 중복하지 않도록 SaveBar에는 완료 문구만 유지한다. |
| `Admin/TopHeaderItem` | Last/active/inactive | `Last`는 위치, 나머지는 상태다. `position=last/default`, `state=active/inactive`로 분리. |
| `Admin/PaymentMethodSettingRow` | enabled/disabled/maintenance | disabled와 maintenance의 설명/CTA가 달라야 한다. maintenance는 회색 + 이유 문구, disabled는 사용자 설정 off로 구분. |
| `Deprecated/Admin-ConfirmDialog` | 2 type | Shared/ConfirmDialog 사용 여부 확인 후 제거 후보. |
| `Admin/NavItem` | Default/Active/Sub | navigation level과 selection state가 섞였다. `level=primary/sub`, `state=default/active`로 분리. |
| `Admin/MenuCard` | selected true/false | menu card가 클릭 가능하면 카드 전체 44px 이상 affordance, 선택은 border + check 중 1개로 제한. |
| `Deprecated/Admin-Badge` | Role 13개 | `Admin/StatusBadge`로 교체 후 제거 후보. |
| `Admin/IngredientCard` | Default/Sold Out | SoldOut의 정보 대비를 4.5:1 이상으로 보장하고, 라임을 품절 상태에 쓰지 않는다. |
| `Admin/OptionItemCard` | Default/Sold Out | IngredientCard와 공통 shell/card token을 공유한다. |
| `Admin/IngredientTableRow` | Status 3, Selection 3 | 상태와 선택 축 분리는 적절하다. 3×3 조합 중 허용 조합을 명시한다. |
| `Admin/IngredientTypeFilterChip` | Type 7, State 2 | chip 높이 32px은 웹 정보 필터에 가능하지만 태블릿 조작에서는 wrapper 44px을 둔다. |
| `Deprecated/Admin-EmptyState` | Type 2 | Shared/EmptyState로 교체 후 제거 후보. |
| `Admin/SelectionSummaryBar` | State 3 | `Includes Sold Out`은 데이터 조건이므로 selection 개수와 함께 문구로 노출. |
| `Deprecated/Admin-AddResultToast` | Type 4 | Shared/Toast로 교체 후 제거 후보. |
| `Admin/Checkbox` | unchecked/checked, 실제 20×20 | box는 20px 유지 가능. label 포함 클릭 영역을 40px(웹) / 44px(태블릿)으로 만든다. |
| `Admin/DetailPanel` | default/empty/status3 | `status3`를 의미 있는 상태명으로 변경. |
| `Admin/ModalActionBar` | mode/style/status | `style=green/red`은 색 이름 대신 `tone=primary/danger` 사용. |
| `Deprecated/Admin-Toast` | 4 status | Shared/Toast로 교체 후 제거 후보. |
| `Admin/DatePicker` | single/range × default/active/disabled/open | 상태 구조는 적절하다. 날짜 셀 선택 면적은 40×40px 이상, 태블릿은 44×44px 이상. |
| `day` | Variant property 오류 | P0. component set을 열어 누락된 Variant property/충돌 값을 해소한다. |
| `Admin/DateSelector` | Date/Month, 232×35 | 실제 클릭 높이를 40px(웹), 44px(태블릿)로 올린다. 35px은 시각 높이로만 유지해도 된다. |
| `Admin/AnalyticsMetricCard` | Large/Compact/Compact Peak | Large와 Compact의 숫자 Style을 Number L/M으로 고정한다. |
| `Admin/AnalyticsDetailTable` | Sales Day/Calendar Day/Hour | 시간 축 전환은 filter action으로, table row는 48~56px으로 고정한다. |
| `Admin/PaymentMethodRow Final Master` | enabled/disabled | 기존 PaymentMethodSettingRow와 소유권을 하나로 정한다. Final Master만 새 화면에 사용. |
| `Admin/PaymentSaveBar Final Master` | dirty/saving/error | 기존 SaveBar와 중복. payment 전용이면 이름을 `Admin/PaymentSaveBar`로 짧게 정리. |
| `Admin/IngredientEditRow Final Master` | 핵심·품절 / 베이스·기본 / 일반·기본 | 데이터 조합은 property 값보다 `importance`, `availability` 2축으로 표현. |
| `Admin/IngredientCategoryGroup Final Master` | 핵심/베이스/일반 | 제목·설명·행 수의 spacing을 24 / 16 / 8px로 고정. |
| `Admin/OptionGroupSummary Final Master` | 드레싱/베이스 | amount/required/selected count가 추가되면 Text Style과 상태 규칙을 별도 property로 둔다. |
| `Admin/MenuIngredientSummaryRow` | core/base | `tone=core/base`는 적절하다. 식별 색만으로 core/base를 구분하지 말고 라벨도 유지. |

### 관리자 visual direction

Navbar의 넓은 버전은 메뉴 문구와 3D 채소 홍보 카드가 함께 있고, compact 버전은 아이콘 중심이다. 이 대비 자체는 좋다. 다만 주문·매출·품절처럼 밀도 높은 업무 화면은 **라임 active surface 1개 + 중립 배경 + 정보색 1개**만 쓰고, 3D 장식은 Navbar 하단의 보조 카드처럼 한 화면에 0~1개만 유지한다. 표·그래프·KPI에 같은 장식을 반복하면 업무 도구가 아닌 AI 생성 보드처럼 보인다.

## 7. Kiosk Screens — `134:7720`

### 페이지 수치

- 전체 `SCR-*` 프레임: 66개
- 실제 기기 프레임: 57개가 **1080×1920px**, 나머지는 annotation/spec 보드
- 화면 Text 2536개 중 Style ID 미연결 2470개 (**97.4%**)
- Auto layout 4749개 / non-auto 455개
- 반복 수치: 24/30 텍스트 645개, 좌우 padding 18px 각 645개, gap 4px 690개

`18px`은 프로젝트의 8px spacing scale에 없다. 키오스크 화면의 일반 content padding이라면 16px 또는 24px으로 선택한다. 18px을 꼭 유지할 이유가 있다면 `space2_25=18`을 token으로 명시하고 즉흥값으로 두지 않는다.

### 프레임별 상태 점검

아래 줄의 각 이름은 실제 Figma 프레임이다. 전부 1080×1920이고, 특별히 표기하지 않은 프레임은 `clipsContent=true`다.

| Screen | 현재 프레임 | 화면 반영 피드백 |
|---|---|---|
| SCR-001 Home | Default, High Contrast | High Contrast까지 존재한다. Default와 High Contrast에서 버튼·설명·로고 외의 장식 색이 바뀌지 않는지 비교한다. HomeActionButton은 최소 240×240px. |
| SCR-003 Menu List | Default, Empty, Loading, Items Added, Empty Cart Toast, Sold-out, Error, Category Disabled | 목록의 8개 상태가 있다. Empty/Loading/Error은 메뉴 card grid의 기본 좌우 기준선과 footer 위치를 동일하게 둔다. Category Disabled는 disabled 색만이 아니라 클릭 불가 cursor/label을 포함한다. |
| SCR-004 Menu Detail | Default, Option Selected, Loading, Error, Allergy Expanded, Menu Sold-out, Menu Limit Toast, Cart Limit Toast, Edit Cart Item, Edit Cart Item/Changed, Save Loading, Save Error, Discard Confirm, Ingredient Sold-out, Base Sold-out | 가장 상태가 많은 화면이다. Option 선택 row의 내부 indicator 20px을 click target으로 쓰지 말고 row 전체를 64px 이상으로 한다. Sold-out/limit/error는 서로 다른 문구와 CTA를 유지한다. |
| SCR-005 Cart | Default, Empty, Delete Confirm, Menu Quantity Limit Toast, Cart Quantity Limit Toast, Quantity Changed, Last Item Deleted→Empty, Item Deleted, Clear Cart Confirm, Clear Cart Success/Empty, Option Updated Toast, Item Sold-out, Edit Required, Checkout Blocked, Last Item Delete Confirm | `Checkout Blocked`가 있어 핵심 예외가 커버된다. 모든 confirm CTA의 높이를 64px 이상, destructive secondary/primary 순서를 Shared ConfirmDialog와 동일하게 맞춘다. |
| SCR-007 Payment | Summary Collapsed, Summary Expanded, Processing, Loading, Method Selected, All Methods Disabled, Load Network Error | 결제 요약 접힘/펼침은 같은 content start 기준을 유지한다. Processing은 재탭 방지를 위해 CTA가 loading/disabled 상태임을 명확히 보여야 한다. |
| SCR-008 Complete | Default | Display XL/L는 이 한 화면처럼 단일 결과 메시지에만 쓴다. 주문번호·완료시간은 Number style로 분리한다. |
| SCR-012 Payment Error | Payment Declined, Network Failure, Retry Loading | Declined와 network failure의 재시도 가능 여부가 달라야 한다. declined에는 결제수단 변경, network에는 재시도 CTA를 우선 배치한다. |
| SCR-013 Timeout | Expired, Warning Countdown, Continue Order | Warning Countdown에 숫자 색만 변하지 않게 한다. 남은 시간은 Number L/M, 안내는 Body M으로 분리한다. |
| SCR-014 Accessibility | Default, High Contrast, Reverted | 접근성 설정 완료 후 Reverted까지 존재한다. 선택 항목의 상태는 색 + check/icon + 텍스트 중 최소 2개로 표시한다. |

별도 annotation/spec 프레임은 화면 구현 대상과 섞이지 않게 이름 앞에 `DOC/` 또는 별도 page로 이동한다.

- `SCR-004 / Implementation Annotation` 800×3493
- `SCR-005 / Implementation Annotation` 800×2798
- `SCR-003 / Empty Cart Toast / Annotation` 600×360
- `SCR-004 / Edit Cart Item /* / __spec` 500×319~427 (5개)
- `SCR-005 / Last Item Delete Confirm Annotation` 600×251

## 8. Admin Screens — `134:10606`

### 페이지 수치

- 전체 `SCR-*` 프레임: 72개, 모두 **1920×1080px**
- Text 6002개 중 Style ID 미연결 5868개 (**97.8%**)
- Auto layout 10908개 / non-auto 1799개
- 자주 쓰인 크기: 14/auto 1653개, 12/auto 1175개, 13/auto 956개, 10/auto 295개, 9/auto 119개

관리자 웹/태블릿에서 9px과 10px은 정보 우선순위가 낮아도 작다. 최솟값을 **12/16**으로 정하고, 표의 보조 정보도 12px 아래로 내리지 않는다. 13px은 13/20, 14px은 14/20으로 line-height를 고정한다.

### 프레임별 상태 점검

| Screen | 현재 프레임 | 화면 반영 피드백 |
|---|---|---|
| SCR-009 Live Order | Default, Loading, Empty, Error, Detail Open, Status Change Confirm, Saving, Success Toast, Save Error, TTS Failure Toast, New Order Notification | 실시간 주문은 상태 coverage가 가장 좋다. New Order/TTS Failure는 toast만으로 끝내지 말고 접근성용 텍스트 로그 또는 새 주문 배지를 유지한다. |
| SCR-010 Order Management | Default, Detail Open, Filter Applied, Loading, Empty, Error | filter applied에서 filter chip/결과 수를 함께 표시한다. DataTable row click target은 최소 48px, 태블릿 56px. |
| SCR-011 Sold-out Management | Default, Empty, Error, Loading, Save, Item Changed, Disable-all Confirm, Saving, Success Toast, Save Error | Item Changed와 Saving/Save Error가 분리되어 있다. `전체 해제`·checkbox 20px은 실제 label row를 44px로 확장한다. |
| SCR-015 Login | Default, Unauthorized, Validation Error, Authentication Error, Submitting | Validation과 Authentication error가 분리되어 좋다. input은 height 48px 이상, 오류문은 12/16 이상, red text는 4.5:1 이상. |
| SCR-016 Menu Management | Default, Detail Add, Detail Edit, Validation Error, Delete Confirm, Save Loading, Save Success, Save Error, Empty, Loading | Detail Add/Edit의 field spacing과 SaveBar 기준선을 동일하게 유지한다. `clip=false` 화면이 많으므로 드로어가 화면을 넘겨야 하는지 확인한다. |
| SCR-018 Payment Methods | Default, Toggle Changed, Save Confirm, Saving, Save Success, Save Error, All Disabled Warning, Loading, Load Error | All Disabled Warning은 부정적 결과를 명확히 경고한다. toggle 자체가 44px hitbox인지 확인한다. |
| SCR-019 Sales Summary | Default, Loading, Empty, Error, Filter Applied, Partial Data | Partial Data에는 누락 범위/마지막 갱신 시간을 텍스트로 표시한다. `clip=false`가 의도된 overlay인지 확인한다. |
| SCR-020 Monthly Sales | Default, Month Changed, Loading, Empty, Error | month selector는 40px 웹 / 44px 태블릿. 차트 tooltip은 본문 12/16 미만 금지. |
| SCR-021 Daily Sales | Default, Date Changed, Loading, Empty, Error | Date changed 후 KPI와 차트 skeleton이 같은 32px content padding을 유지하는지 확인한다. |
| SCR-022 Dashboard | Default, Loading, Error, Empty Data, Partial Data | Default와 Partial Data는 KPI 카드 수·카드 폭이 바뀌지 않아야 한다. 데이터 없는 카드도 제목/설명 baseline을 유지한다. |

`clip=false`인 화면은 매출 요약군과 메뉴 관리군에 집중되어 있다. base screen 자체는 `clipsContent=true`로 두고, dialog/toast/drawer만 page-level overlay로 올리는 편이 반응형·스크롤 구현에서 안전하다. `clip=false`가 실제 외부 popover를 위한 것인지 프레임마다 확인한다.

## 9. 화면 반영용 고정 규칙

### 키오스크

1. 화면 기준: 1080×1920.
2. 주 CTA: 높이 112px 이상, 라벨 24/30 이상.
3. 일반 선택 row/탭: 클릭 높이 64px 이상.
4. 아이콘만 보이는 버튼: 아이콘 24~32px, wrapper 64×64px.
5. 본문: 16/24 이상. 14/20은 보조 설명에만, 12px은 법적/비조작 보조문구에만.
6. 밝은 라임 `#B5E30F` 위 텍스트는 `#000000`, white 금지.
7. `Loading`, `Empty`, `Error`, `Disabled`, `SoldOut`은 Default와 동일한 header/footer/content start 좌표를 유지.

### 관리자 웹/태블릿

1. 화면 기준: 1920×1080 desktop. Tablet Variant는 Desktop 스타일을 축소하지 말고 sidebar·toolbar·table 밀도를 별도 조정.
2. 페이지 제목: 24/32 또는 28/36. 카드 제목: 16/20 또는 16/24. 표 본문: 최소 12/16.
3. 클릭 target: 웹 40×40px 이상, 터치 가능 태블릿 44×44px 이상.
4. table row: 기본 48px, 조작/상태 전환 row 56px.
5. 라임은 active navigation, primary CTA, selected surface에 한정. 매출 상태·품절·오류·경고는 Success/Warning/Danger semantic token을 분리.
6. permanent sidebar에는 장식 이미지 1개 이하. KPI·table·chart 영역에는 장식 이미지/gradient를 반복하지 않는다.

## 10. 구현 전 체크리스트

- [ ] Foundations 표지의 80/47을 실제 83/51과 일치시켰다.
- [ ] `day` (`389:44743`) Component Set Variant 오류를 해결했다.
- [ ] Kiosk/CategoryTab와 Kiosk/CategoryTap의 중복을 하나로 정리했다.
- [ ] `Variant4`, `sourse`, `status3`, `MenuDetailSummary`처럼 의미 없는/오타 값의 이름을 고쳤다.
- [ ] 화면 텍스트가 named Text Style에 연결되었다.
- [ ] product screen에서 `auto` line-height와 9~10px 텍스트를 제거했다.
- [ ] Kiosk 조작 UI의 실제 hit target이 64px 이상이다.
- [ ] Admin Checkbox/MenuButton/DateSelector의 wrapper가 웹 40px, 태블릿 44px 이상이다.
- [ ] `#B5E30F` 위 white 텍스트가 없다.
- [ ] Deprecated component가 새 화면 instance에 사용되지 않는다.
- [ ] Screen frame의 clip=false가 overlay 목적임을 확인했다.
- [ ] 66개 Kiosk와 72개 Admin 상태 프레임에 Default/Loading/Empty/Error/Disabled 흐름이 누락 없이 연결된다.

## 11. 검토 범위와 남은 위험

- Figma 노드의 구조·크기·Variant·텍스트 style 연결·spacing·색상은 정량 추출했다.
- Foundation cover, Shared Modal, Admin Navbar의 시각 샘플도 읽었다.
- Figma MCP 사용량 제한이 발생하여 모든 프레임의 고해상도 screenshot 육안 비교는 완료하지 못했다. 따라서 이 문서의 모든 프레임 평가는 노드 구조와 수치 기반이며, 최종 반영 전에는 대표 화면별로 100% scale에서 한 번 더 육안 확인한다.

## 12. 공부 포인트

- Figma 변수는 “만든 것”보다 실제 node에 binding된 것이 중요하다.
- Text Style은 px 값이 같아도 Style ID가 없으면 화면 간 수정이 동시에 반영되지 않는다.
- 16px 아이콘은 정상일 수 있지만 16px 클릭 영역은 아니다.
- 화면 상태를 많이 만든 것은 강점이다. 이제는 state마다 같은 component·same token·same baseline을 재사용해 drift를 막는 단계다.
