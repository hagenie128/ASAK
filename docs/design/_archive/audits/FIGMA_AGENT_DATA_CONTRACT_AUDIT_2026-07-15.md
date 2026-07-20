> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Completed data-contract audit.
> Canonical Replacement: `docs/design/FIGMA_GUIDE.md`
> Original Path: `docs/design/FIGMA_AGENT_DATA_CONTRACT_AUDIT_2026-07-15.md`

# ASAK Figma Agent 작업 지시문 — 실제 화면·데이터 계약 감사

> 작성일: 2026-07-15
> Figma 파일: `VXKyzoNdsgM4oN57mrECxb` — ASAK Design System & Product UI
> MCP 직접 점검 대상: `05. Screens / Kiosk` (page `2:6`), `06. Screens / Admin` (page `2:7`)
> 수정 범위: Figma Agent가 화면과 컴포넌트를 직접 수정하되, 코드·DB·API 근거 없는 데이터/기능은 `__manual-check`로 남긴다.

## A. 프로젝트 데이터 구조 요약

### 실제 구현과 계약의 구분

- Spring backend(`ASAK-back`)는 `GET /api/health`와 공통 `ApiResponse`만 구현된 골격이다. 메뉴·주문·결제 Entity, DTO, Repository, Service, Controller는 아직 없다.
- Kiosk 프런트는 API client와 Zustand `orderSessionStore`는 존재하지만, 메뉴 상세·장바구니·결제·완료 페이지 및 다수 컴포넌트는 placeholder다.
- 따라서 아래 API/DTO는 실행 완료된 백엔드가 아니라 `ASAK-Kiosk/src/contracts/api-data-contract.md`, `ASAK/docs/wiki/rest-api-spec.md`, `public/mocks/kiosk.json`의 최신 구현 계약이다. Figma는 이 계약을 데이터 표시 기준으로 사용한다.

### 명명 규칙

| 대상 | 규칙 | 예시 |
| --- | --- | --- |
| 백엔드·프런트 URL, API JSON 필드, Figma Property | `camelCase` | `categoryId`, `orderNo`, `paymentStatus`, `extraPrice` |
| DB 테이블·컬럼 | `snake_case` | `order_item`, `total_price`, `is_sold_out` |
| Java 클래스·React 컴포넌트·Figma Component Set | `PascalCase` | `OrderResponse`, `MenuCard`, `OrderDetailRow` |
| 상수·토큰 | `UpperCamelCase` | `OrderStatus`, `PaymentStatus`, `OrderSessionResetReason` |

기존 `ORDER_SESSION_RESET_REASON`, `API_ENDPOINTS`, `Property 1`, `sourse`, `menu-itme`, `Frame 1`은 이 규칙과 다른 기존 자산이다. Figma Agent는 정상 인스턴스 연결을 깨지 않는 범위에서 이름과 Variant Property를 위 규칙으로 정리한다.

### 주요 DB·API·상태

| 영역 | DB/응답 필드 | 화면 의미 |
| --- | --- | --- |
| 메뉴 | `menu.name,price,image_url,description,is_sold_out`; API `menuId,name,price,imageUrl,baseKcal,isSoldOut,hasSoldOutIngredient,soldOutBadges` | 메뉴 카드·상세·품절 |
| 영양 | `menu_nutrition.kcal`, `ingredient.kcal`; API `baseKcal`, option `extraKcal` | 기본/예상 칼로리 |
| 재료/알레르기 | `menu_ingredient.can_remove,role_id`, `ingredient.is_sold_out`, `ingredient_allergen`; API `ingredients,allergens,allergyText,isOrderable,soldOutReason` | 기본·제외 재료, 알레르기, 핵심/일반 품절 |
| 옵션 | `option_group.min_select,max_select`, `option_item.extra_price,is_sold_out`, 정책의 `is_recommended,is_default`; API `optionGroupId,selectType,minSelect,maxSelect,isRequired,items[]` | 베이스·드레싱·토핑·추가 금액 |
| 주문 | `orders.order_no,total_price,created_at`; `order_item.quantity,price`; `order_item_option.quantity,price`; `item_exclusion` | 장바구니·주문 목록·상세 |
| 결제 | `payment.method_id,status_id,amount,paid_at`; API `paymentId,orderId,orderNo,amount,paymentStatus,paidAt` | 결제·완료·관리 |

상태 계약은 `orderStatus = RECEIVED | PREPARING | COMPLETED`, `paymentStatus = READY | APPROVED | FAILED`, `orderType = EAT_IN | TAKE_OUT`, 품절 대상 `targetType = MENU | INGREDIENT | OPTION_ITEM`이다.

### 가격·영양 계산

```text
lineTotal = (unitPrice + Σ(option.extraPrice × option.quantity)) × item.quantity
orderTotal = Σ(lineTotal)
payment.amount = 결제 요청·승인 금액
estimatedKcal = baseKcal + Σ(선택 option.extraKcal) - Σ(제외 재료 kcal)
```

- 현재 API/DDL에는 `discountAmount`, 환불금, 취소 사유, 결제 실패 사유, 원가, 주문 영양 스냅샷이 없다.
- `estimatedKcal`은 옵션 선택 화면의 예상값만 가능하며 완료/관리 화면에서 확정값처럼 표시하면 안 된다.
- 주문 당시 가격 보존은 `order_item.price`, `order_item_option.price`를 사용해야 하나 단가/행합계 의미가 아직 확정되지 않았다. Figma에는 `unitPrice`, `additionalPrice`, `lineTotal`을 각각 분리한다.

## B. 실제 Figma 화면 점검과 불일치

### 페이지 인벤토리

- `05. Screens / Kiosk`에는 `SCR-001`, `SCR-003`, `SCR-004`, `SCR-005`, 결제 접힘/펼침/처리/오류, timeout, 완료, 접근성 3상태, 메뉴·장바구니·결제의 Empty/Loading 상태가 있다.
- `06. Screens / Admin`에는 Login, 주문 목록/상세, 품절 관리, 결제수단, 매출 요약/월별/일별, 주문·품절·메뉴·결제수단·매출의 Loading/Empty/Error 상태가 있다.
- `00. START HERE`의 QA checklist에는 모든 화면의 `__spec`, 반복 UI의 Auto Layout + Component Instance, loading/empty/error, 불확정 데이터의 `데이터 연결 예정`/`Mock settings` 표기가 미완료로 남아 있다.

### 확인된 화면별 핵심 이슈

| Figma Frame ID | 실제 화면 관찰 | 데이터 계약 기준 수정 |
| --- | --- | --- |
| `2:4704` SCR-003 Menu List | 모든 카드가 ‘불고기 랩 / 7,900원 / 410 kcal’로 반복되고 일부만 BEST/NEW다. 하단은 `0개`인데 CTA 구조가 남아 있다. | `menus[]` 반복 Property와 image/soldOut/tag 상태를 만들고, 빈·로딩 상태와 실제 itemCount/totalAmount를 분리 |
| `2:4775` SCR-004 Menu Detail | 메뉴명/이미지/베이스/드레싱/토핑이 placeholder다. 알레르기와 필수·최대 선택 안내는 있다. | `ingredients`, `allergens`, `optionGroups.items`를 배열 구조로 연결; `extraPrice`, `extraKcal`, `isRecommended`, `isSoldOut` 표시 보완 |
| `2:4791` SCR-005 Cart | 두 항목의 상품별 합계는 각 7,200원인데 하단은 `2개 27,000원`이다. 할인 `0개/0원` 행과 560kcal 표시가 있다. | lineTotal/orderTotal을 한 기준으로 통일; 할인 행은 API가 생길 때까지 `__manual-check`; 최종 kcal는 `예상`으로만 표기 |
| `2:4816/2:4828` SCR-007 Payment | 카드·삼성페이와 카카오페이 결제수단이 실제 화면에 있다. | 현재 seed/API에서 확정된 수단은 CARD뿐이다. 활성 방법 API 결과 기반으로 표시하고 미확정 수단은 Mock settings 처리 |
| `2:4851` SCR-012 Payment Error | 실패 프레임은 존재한다. | 오류 code/message, 재시도, 장바구니 복귀, 금액 불일치 처리 Property를 추가 |
| `2:4877` SCR-008 Complete | 주문번호 1225, 바코드, 영수증 출력, 5초 자동 초기화가 있다. 결제금액·수단·시간은 없다. | `orderNo,amount,paymentMethod,paidAt,paymentStatus,receiptState`를 추가하고 timeout 상수는 수동 확인 |
| `2:8162` SCR-009/010 Order List + Detail | 표/상세가 한 화면에 있고, `취소`, `환불`, `결제완료` 상태가 있다. | API Enum 밖인 취소·환불·결제완료 문구를 `RECEIVED/PREPARING/COMPLETED`, `READY/APPROVED/FAILED`와 분리. 옵션과 제외 재료도 별도 섹션으로 표시 |
| `29:12269` SCR-011 Sold-out | 메뉴/재료/옵션 탭, 저장 Modal/Toast, 검색/카테고리 필터는 있다. | `targetType,targetId,name,isSoldOut,reasonType`를 Component Property로; 핵심 재료 품절과 일반 재료/옵션 품절의 영향 문구 분리 |
| `2:8726` SCR-019 Sales Summary | 고객 수, 취소·환불, 승인 결제금액, 시간대/카테고리/인기메뉴 TOP 5 KPI가 있다. | API-015는 기간별 일별 매출·메뉴별 판매량만 확정. 미지원 KPI/환불 수치는 확정 데이터처럼 두지 말고 `Mock settings` 또는 제거 |

### Figma Component/Variant 불일치

- `Admin/OrderCard` 내부에 `menu name`, `item name`, `2000원` placeholder가 남아 있다. `OrderMenuCard`, `orderMenuOptionList`, `Admin/OrderMenuOptionItem`은 API 응답 배열로 치환 가능해야 한다.
- `Admin/DataTableRow-Active`는 `접수/준비중/완료/취소` 한글 Variant를 사용한다. Variant 값은 `received/preparing/completed`처럼 enum 매핑용 값으로 바꾸고 표시 문구만 한국어로 둔다.
- `Property 1=base/sourse/+/-`, `menu-itme`, `Frame 1`은 의미 있는 `PascalCase` Component/`camelCase` Property 이름으로 정리한다. `sourse`는 `source` 또는 실제 역할명으로 수정한다.
- 품절 화면의 `__spec`은 `menuItems[], ingredients[], searchQuery`만 적혀 있다. `optionItems[]`, `targetType`, `reasonType`, `isSoldOut`, `toggleProgress`를 추가한다.

## C. 화면별 데이터 매핑표

| 화면·ID | 표시 항목 | 출처/API 필드 | Property/Variant | 상태/수정 |
| --- | --- | --- | --- | --- |
| SCR-003 `2:4704` | 카드명/이미지/가격/기본 kcal/태그/품절 | API-002 `name,imageUrl,price,baseKcal,isSoldOut,hasSoldOutIngredient,soldOutBadges` | `MenuCard(menuName,image,price,baseKcal,isSoldOut,tags)` | `default/loading/empty/soldOut/imageMissing` |
| SCR-004 `2:4775` | 설명·알레르기·기본/제외 재료·옵션 | API-003/004 `ingredients,allergens,allergyText,optionGroups.items` | `OptionGroup(minSelect,maxSelect,isRequired)`, `OptionItem(extraPrice,extraKcal,isRecommended,isSoldOut)` | `default/requiredError/maxReached/soldOut` |
| SCR-005 `2:4791` | 메뉴·옵션·제외·수량·단가·행합계·주문합계 | session `items[]`, API-005 `totalPrice` | `CartItem(menuName,optionSummary,exclusionSummary,quantity,unitPrice,lineTotal)` | `default/empty/soldOut/quantityMin/quantityMax` |
| SCR-007/012 `2:4816` 등 | 총 결제금액·결제수단·처리/실패 | API-006 `amount,paymentStatus,paidAt`; error `code,message` | `PaymentMethodCard(methodName,selected,disabled)`, `PaymentState` | `default/processing/failed/retry` |
| SCR-008 `2:4877` | 주문번호·결제금액·수단·시간·영수증 | API-006 `orderNo,amount,paymentStatus,paidAt`; API-019 확장 | `OrderComplete(orderNo,paidAmount,paymentMethod,paidAt,receiptState)` | `approved/receiptLoading/receiptFailed/timeout` |
| SCR-009/010 `2:8162` | 주문 목록·상세·상태·옵션·제외 재료 | API-007/008 `orderNo,orderType,orderStatus,paymentStatus,totalPrice,createdAt,items,selectedOptions,excludedIngredients` | `DataTableRow`, `OrderDetailRow`, `OrderStatusBadge` | `default/loading/empty/error/changingStatus` |
| SCR-011 `29:12269` | 품절 대상·이유·저장 결과 | API-009/010 `targetType,targetId,name,isSoldOut,reasonType` | `SoldOutItem`, `SoldOutToggle`, `ConfirmDialog` | `default/loading/empty/toggleProgress/toggleSuccess/toggleError` |
| SCR-018 `2:13336` | 결제수단 활성/정렬 | API-013/014, `payment_method_config` | `PaymentMethodRow(name,isActive,sortOrder,loading)` | `default/saving/error/empty` |
| SCR-019 `2:8726` | 기간·일별 매출·메뉴별 판매량 | API-015 `from,to`, sales/day, menu sales | `SalesMetricCard`, `DateRange`, `SalesChart` | `default/loading/empty/error` |

## D. Figma Agent 최종 프롬프트

```text
대상 파일은 ASAK — Design System & Product UI (fileKey VXKyzoNdsgM4oN57mrECxb)다. 반드시 `05. Screens / Kiosk`와 `06. Screens / Admin`의 기존 Frame/Component Set을 MCP로 읽고 수정한다. 05는 키오스크, 06은 관리자 화면이다.

1. 기준 확인
- API URL/JSON/Figma Property는 camelCase, DB 출처 메모는 snake_case, Component Set/클래스는 PascalCase, 상수/토큰은 UpperCamelCase로 한다.
- 공통 API envelope는 `{ success,status,code,message,data }`다.
- orderStatus는 RECEIVED/PREPARING/COMPLETED, paymentStatus는 READY/APPROVED/FAILED, orderType은 EAT_IN/TAKE_OUT, 품절 targetType은 MENU/INGREDIENT/OPTION_ITEM만 실제 계약으로 간주한다.
- `lineTotal=(unitPrice + Σ(extraPrice×optionQuantity))×itemQuantity`, `orderTotal=Σ(lineTotal)`, `payment.amount=결제 요청/승인 금액`을 모든 화면에 동일하게 적용한다.

2. 05. Screens / Kiosk 수정
- SCR-003 `2:4704`: MenuCard를 메뉴 배열 반복 구조로 만들고 menuName/image/price/baseKcal/tags/isSoldOut/hasSoldOutIngredient를 Property로 둔다. 같은 메뉴·가격·kcal의 하드코딩을 제거하고 default/loading/empty/soldOut/imageMissing을 보완한다.
- SCR-004 `2:4775`: ingredients, allergens, allergyText, optionGroups/items를 표시 가능하게 한다. OptionItem에 extraPrice, extraKcal, isRecommended, isSoldOut을 연결하고 필수 미선택/최대 선택/품절 Variant를 추가한다.
- SCR-005 `2:4791`: CartItem에 메뉴명·선택 옵션·제외 재료·수량·단가·행합계를 분리한다. 두 상품 합계와 장바구니 총액이 불일치하지 않게 고치고, 할인 값은 계약 전에는 확정값으로 표시하지 않는다. kcal는 `예상`으로만 표기한다.
- SCR-007/012: 활성 결제수단은 API 결과로 교체 가능한 리스트여야 한다. 현재 CARD 외 수단은 Mock settings 또는 manual-check로 표기한다. processing/failed/retry 상태와 errorCode/errorMessage 영역을 추가한다.
- SCR-008 `2:4877`: orderNo, paidAmount, paymentMethod, paidAt, paymentStatus, receiptState를 표시한다. 영수증 출력 loading/failure와 자동 초기화 안내를 보완한다. timeout 초는 기획 확정값이 아니므로 상수 Property로 둔다.

3. 06. Screens / Admin 수정
- SCR-009/010 `2:8162`: DataTableRow는 orderNo, createdAt, orderType, itemCount, totalPrice, orderStatus, paymentStatus로 구성한다. 주문 상세는 items, selectedOptions, excludedIngredients를 분리한다. 취소/환불/결제완료는 현재 API Enum 밖이므로 실제 status Variant에서 제거하거나 __manual-check로 남긴다.
- SCR-011 `29:12269`: targetType/targetId/name/isSoldOut/reasonType을 직접 반영한다. MENU·INGREDIENT·OPTION_ITEM 탭, 저장 confirm, pending/success/error toast를 유지하고 핵심 재료 품절=메뉴 주문 불가와 일반 재료/옵션 품절=선택 불가 안내를 구분한다.
- SCR-018 `2:13336`: name/isActive/sortOrder 기반의 결제수단 행, 저장/loading/error/empty 상태를 구성한다.
- SCR-019 `2:8726`: from/to, 일별 매출, 메뉴별 판매량, loading/empty/error만 확정 데이터로 둔다. 고객 수, 취소·환불, 승인 결제금액, 시간대/카테고리/인기메뉴 KPI는 API 근거가 생길 때까지 Mock settings 또는 __manual-check 처리한다.

4. 공통 정리
- `Property 1`, `sourse`, `menu-itme`, `Frame 1` 등 자동/오탈자 명명을 PascalCase Component Set과 camelCase Property로 정리한다. 기존 인스턴스 연결과 Frame ID는 유지한다.
- Button, MenuCard, OptionGroup, CartItem, PaymentMethodCard, DataTableRow, OrderDetailRow, SoldOutItem, SalesMetricCard, EmptyState, ErrorState, LoadingState, ConfirmDialog에 데이터·상태 Property를 추가한다.
- 반복 영역은 Auto Layout과 Component Instance를 사용하고, 텍스트 잘림·겹침·오버플로우·불필요한 absolute position·깨진 instance를 수정한다.
- 각 화면 root에 `__spec`을 두고 Route/Data/States/Actions를 기록한다. 불확정 데이터는 `데이터 연결 예정`, `Mock settings`, 또는 `__manual-check`로 표시한다.

5. 재검증·보고
- 수정 후 05/06 전체의 가격 정합성, 상태 Enum, 품절 처리, loading/empty/error, instance 연결, 오버플로우를 재점검한다.
- Frame ID, 수정 Component Set/Property/Variant, 데이터 근거(API/DB/코드), manual-check 잔여 항목을 표로 보고한다.

제한: DB/API/문서/실제 코드 근거 없이 기능·가격·칼로리·결제수단·KPI를 추가하지 않는다. 가격 계산을 임의 변경하지 않는다. 브랜드 컬러/방향을 재설계하지 않는다. React 코드를 생성하지 않는다.
```

## E. Figma만으로 해결되지 않는 항목

| 분류 | 필요 작업 |
| --- | --- |
| DB | 할인/쿠폰·환불·실패 사유, 주문 당시 메뉴/옵션명·가격·영양 스냅샷, 원가, 고객·결제수단별 집계 저장 모델 |
| API/DTO | API-005의 항목별 금액/할인, API-006의 실패 code/message·재결제/취소, API-015의 실제 응답·지원 KPI 확정 |
| Backend | menu/order/payment Entity·DTO·Repository·Service·Controller, DB snake_case→API camelCase 변환, 서버 총액 검증, 핵심/일반 품절 계산 |
| Frontend | `cartRules.js`, `soldOutPolicy.js`, `useKioskTimeout.js`, 타입/상수, placeholder 화면과 로딩·오류·빈 상태 구현 |
| 기획 | timeout 시간/모달, 카드 외 결제수단, 취소·환불, 할인, 영수증·바코드·QR, 매출 KPI의 MVP 범위 |

## 근거 파일

- `ASAK-Kiosk/src/contracts/api-data-contract.md`
- `ASAK/docs/wiki/rest-api-spec.md`, `db-table-definition.md`, `requirements-definition.md`, `user-scenarios.md`
- `ASAK/asak-data/archive/schema/short-name-before-20260713-115747.sql`, `ASAK/asak-data/seed-v3/*.json`
- `ASAK-Kiosk/src/store/orderSessionStore.js`, `src/api/*.js`, `src/pages/**/*.jsx`, `src/components/**/*.jsx`
- Figma MCP: page `2:6`, page `2:7`; Frame `2:4704`, `2:4775`, `2:4791`, `2:4816`, `2:4877`, `2:8162`, `29:12269`, `2:8726`
