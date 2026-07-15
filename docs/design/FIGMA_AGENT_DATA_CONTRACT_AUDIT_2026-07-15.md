# ASAK Figma Agent 데이터 계약 감사 및 작업 지시문

> 작성일: 2026-07-15
> 대상 Figma: `ASAK — Design System / Product UI — 2026-07-14` (`node-id=2:6`)
> 우선 대상 페이지: `💻 05. 관리자 웹 와이어프레임`, `🖼️ 06. Hi-fi 디자인`
> 근거 우선순위: 실제 코드 → 최신 API/프론트 계약 → DB 백업 DDL·seed-v3 → 요구사항/기존 Figma 점검 문서.
> 한계: 연결된 Figma 파일은 이 감사 환경에서 읽기 전용으로도 열리지 않아, 프레임의 실제 픽셀/레이어 존재 여부는 기존 2026-07-14 Figma 점검 보고서의 인벤토리를 기준으로 했다. Figma Agent는 수정 전 페이지 05·06을 다시 스캔하여 이 문서의 ‘확인 필요’를 확정해야 한다.

## A. 프로젝트 데이터 구조 요약

### 구현 성숙도와 정본

- `ASAK-back`은 `GET /api/health`와 `ApiResponse`만 구현된 Spring Boot 골격이다. Entity/DTO/Repository/Service/주문 Controller는 현재 없다.
- `ASAK-Kiosk`는 API 클라이언트, Zustand 주문 세션, 일부 메뉴 목록/카테고리 mock 연결만 존재한다. 메뉴 상세·장바구니·결제·주문완료·관리자 페이지와 대부분의 컴포넌트는 자리표시자다.
- 그러므로 API-001~020의 DTO/응답 필드는 **현재 실행 코드가 아니라** `ASAK-Kiosk/src/contracts/api-data-contract.md`, `ASAK/docs/wiki/rest-api-spec.md`, `public/mocks/kiosk.json`에 정의된 구현 계약이다. Figma에는 이 계약의 필드명/상태를 쓰되, 지원하지 않는 값을 실데이터처럼 고정하지 않는다.

### 주요 테이블·관계

| 목적 | 테이블/핵심 컬럼 | 화면 조합 |
| --- | --- | --- |
| 메뉴 | `category(id,name,sort_order,is_active)` → `menu(id,category_id,name,price,image_url,description,is_sold_out)` | 카테고리·메뉴 카드 |
| 태그/영양 | `menu_tag(menu_id,tag_id)` → `tag(code,name,color_hex)`; `menu_nutrition(menu_id,kcal,protein_g,carb_g,...)` | BEST/NEW/저당, 기본 영양 |
| 재료/알레르기 | `menu_ingredient(menu_id,ingredient_id,role_id,quantity,unit_id,is_default,can_remove)` → `ingredient(kcal,protein_g,is_sold_out)` → `ingredient_allergen` → `allergen` | 기본/제외 재료, 핵심·일반 품절, 알레르기 |
| 옵션 | `option_group(min_select,max_select)`; `option_item(option_group_id,ingredient_id,name,extra_price,original_price,amount,unit_id,is_sold_out)`; 현재 seed-v3은 `menu_opt_policy`/`opt_policy`/`opt_policy_item`로 메뉴별 선택정책·기본/추천을 연결 | 베이스·드레싱·토핑·세트, 추가금/품절/추천 |
| 주문 | `orders(order_no,order_type_id,status_id,total_price,created_at)` → `order_item(order_id,menu_id,quantity,price)` → `order_item_option(order_item_id,option_item_id,quantity,price)`, `item_exclusion(order_item_id,ingredient_id)` | 장바구니, 관리자 주문 목록/상세 |
| 결제 | `payment(order_id,method_id,status_id,amount,paid_at)` (주문당 unique), `payment_method_config(method_id,name,is_active,sort_order)` | 결제수단/승인/관리 |

### API·상태·세션 계약

- 고객: `GET /api/categories`, `GET /api/menus?categoryId`, `GET /api/menus/{menuId}`, `GET /api/menus/{menuId}/options`, `POST /api/orders`, `POST /api/payments`.
- 관리자: 주문 조회/상태 변경(API-007/008), 품절 조회/변경(API-009/010), 메뉴(API-011/012), 결제수단(API-013/014), 매출(API-015). 모든 응답은 `{ success, status, code, message, data }`다.
- 화면 상태 Enum 계약: `ORDER_STATUS = RECEIVED | PREPARING | COMPLETED`; `PAYMENT_STATUS = READY | APPROVED | FAILED`; `ORDER_TYPE = EAT_IN | TAKE_OUT`; 결제수단 seed는 현재 `CARD`만 확인된다.
- `orderSessionStore`: `orderType`, `items[]`, `order{orderId,orderNo,orderType,totalPrice,orderStatus,paymentStatus}`, `payment{paymentId,orderId,orderNo,amount,paymentStatus,paidAt}`, `paymentError`를 보관하며 승인 또는 timeout-confirmed 뒤만 reset한다.

### 가격·칼로리 계산 경계

- 화면 표시 계약: `lineTotal = (unitPrice + Σ(option.extraPrice × option.quantity)) × item.quantity`; `orderTotal = Σ(lineTotal)`; `paymentAmount`는 API-006 요청 `amount` 및 승인 응답 `amount`와 일치해야 한다.
- 할인/환불 필드는 현재 주문/결제 DDL과 API-005/006 계약에 없다. 따라서 `discountAmount`, 쿠폰 할인, 환불금, ‘기본가 대비 할인’은 0원으로 임의 표시하거나 확정 금액으로 디자인하면 안 된다. 필요 시 `지원 예정/수동 확인` 상태만 쓴다.
- 기준 메뉴 칼로리는 `menu_nutrition.kcal`/API `baseKcal`; 재료 칼로리는 `ingredient.kcal`; 옵션 API 계약은 `extraKcal`을 제공한다. 옵션 추가·제외에 따른 계산 UI는 가능하지만, 주문 스냅샷 및 API 최종 `totalKcal` 필드는 없다. 수량 포함 최종 칼로리는 서버 계약 확정 전 ‘예상’으로만 표기한다.

## B. 누락 및 불일치 분석

### Figma/계약에서 반드시 보완할 항목

1. 기존 보고서상 05에는 `A-001~A-007`, 06은 비어 있다. 05의 관리자 프레임은 실제 코드 화면명·API 데이터·상태를 명시하고, 06에는 디자인 완료본을 **복제/정리**해 배치해야 한다. 06을 근거 없는 새 기능 화면으로 채우지 않는다.
2. 주문 목록/상세는 `orderNo`, `orderType`, `orderStatus`, `paymentStatus`, `totalPrice`, `createdAt`, `items`, `selectedOptions`, `excludedIngredients`를 구분해 표시해야 한다. 옵션과 제외 재료가 합쳐진 하나의 ‘요청사항’이면 조리 오류가 난다.
3. 품절 관리는 `targetType=MENU|INGREDIENT|OPTION_ITEM`, `targetId`, `name`, `isSoldOut`, `reasonType`을 보여야 한다. 메뉴 자체 품절과 핵심 재료 품절(주문 불가), 일반 재료/옵션 품절(선택 불가·안내)을 같은 빨간 배지 하나로 축소하지 않는다.
4. 관리자 매출은 `from/to` 기간, 요약, 일별 매출·메뉴별 판매량, 로딩/빈/오류를 갖춰야 한다. ‘평균 주문금액’, 결제수단별 통계, 할인·환불은 현 API/DDL에 근거가 없으므로 확정 KPI로 두지 않는다.
5. 메뉴 편집은 현재 계약상 `categoryId,name,price,imageUrl,optionGroupIds`만 확정이다. 원가, 영양 편집, 재료/태그/활성화 저장 UI는 API 계약이 없으므로 `수동 확인`으로 남긴다.
6. 기존 점검의 `Badge` variant에는 `cancelled/refunded`가 제안됐지만 현재 Enum/DDL/API에는 없다. `RECEIVED/PREPARING/COMPLETED`와 `READY/APPROVED/FAILED`만 실제 variant로 제공하고 취소·환불은 planned/hidden으로 분리한다.

### DB/API/코드 불일치와 개발 이슈

| 등급 | 사실 | 영향 |
| --- | --- | --- |
| 차단 | Spring backend에 주문·메뉴·결제 Entity/DTO/Repository/Service/Controller가 없다. | Figma의 API 연결 메모는 설계 계약일 뿐 실행 검증 불가 |
| 높음 | `constants/order.js`, `constants/status.js`, `cartRules.js`, `soldOutPolicy.js`, `types/menu.js`, `types/order.js`, 주요 화면/컴포넌트가 placeholder다. | 수량 한계, 에러문구, 상태 prop을 코드에서 단일 값으로 보장하지 못함 |
| 높음 | 주문 스냅샷 DDL의 `order_item.price`, `order_item_option.price`는 있으나 가격의 의미(단가/행합계, option 추가단가/행합계)가 명시되지 않았다. | 과거 주문 금액 보존과 재계산 규칙을 백엔드에서 확정해야 함 |
| 높음 | `orders.total_price`/`payment.amount` 외 `discount_amount`, 결제 실패 사유, 취소/환불 상태/금액 컬럼이 없다. | 할인/실패 사유/환불 UI를 실제 값으로 표시 불가 |
| 중간 | 옵션 테이블의 DB 컬럼은 `extra_price`, mock/API는 `extraPrice`; menu seed에는 `is_sold_out`, 일부 v3 자료는 `sold_out`. | DB snake_case → API camelCase 변환을 DTO에서 강제해야 함 |
| 중간 | DB에는 `menu_nutrition` 및 `ingredient.kcal`이 있으나 주문 시점 영양 스냅샷·최종 칼로리 API가 없다. | 완료/관리자 화면의 확정 영양 합계는 표시 금지 |
| 중간 | `payment_method_config` seed 기준 활성 결제수단은 CARD 한 종류다. | 카드/카카오/현금 등 다중 결제수단을 실제 가능 상태로 고정하면 안 됨 |
| 중간 | 문서에는 자동 초기화가 ‘경고 없이 30초 예시’와 별도 timeout 모달 요구로 섞여 있고, 코드에는 시간 상수가 없다. | 시간·모달 문구/계속 주문 동작은 기획 결정 필요 |

### 데이터 조합 판정

- 가능: 메뉴↔재료/알레르기/태그/옵션, 주문↔선택 옵션/제외 재료, 주문↔결제는 FK와 교차 테이블로 조합 가능하다.
- 가능하나 서버 규칙 필요: `CORE` 재료 품절은 메뉴 주문 불가, 일반 재료/옵션 품절은 선택 비활성이라는 계산은 `role_id`와 `is_sold_out`으로 가능하다. 응답의 `hasSoldOutIngredient`, `isOrderable`, `soldOutReason`을 서버가 일관되게 계산해야 한다.
- 불가능/미확정: 할인·환불·실패 사유, 원가, 결제수단별 통계, 주문 스냅샷 기반 최종 칼로리, 주문 당시 메뉴명/이미지/알레르기 보존, 메뉴별 활성 상태(`is_active`)는 현재 확정 구조만으로 안전하게 만들 수 없다.

## C. 화면별 데이터 매핑표

| 화면(Figma ID/권장명) | 표시 항목 → 출처/응답 | Figma Property·Variant | 결론/수정 |
| --- | --- | --- | --- |
| 05 `A-001` → `SCR-015 / Admin / Login` | 인증 계약 미확정 | `email`, `password`, `state=default|invalid|loading|unauthorized` | UI 상태만; 성공 사용자/권한 값 하드코딩 금지 |
| 05 `A-002` → `SCR-009 / Admin / Order List` | `orders` + API-007 `content[].orderNo,orderType,orderStatus,paymentStatus,totalPrice,createdAt` | `OrderTable` row text props; `status`; `state=loading|empty|error|default` | 기간/상태/검색/pagination은 response 계약 확정 전 placeholder label로 |
| 05 `A-003` → `SCR-010 / Admin / Order Detail` | `order_item`, `order_item_option`, `item_exclusion`, payment + API-007 items/selectedOptions/excludedIngredients | `OrderDetailRow(menuName,quantity,unitPrice,optionSummary,exclusionSummary,lineTotal)`; two Badge props | 옵션·제외를 분리하고 상태변경 confirm/pending/failed 추가 |
| 05 `A-004` → `SCR-011 / Admin / Sold-out Management` | API-010 `targetType,targetId,name,isSoldOut,reasonType`; API-009 request | `SoldOutToggle(targetType,targetId,checked,disabled,loading)` | MENU/INGREDIENT/OPTION_ITEM filter와 성공/실패 토스트·빈 상태 추가 |
| 05 `A-005` → `SCR-016/017 / Admin / Menu Manage/Edit` | API-011/012 `categoryId,name,price,imageUrl,optionGroupIds`; menu table | `MenuForm` properties; `state=default|invalid|saving|error` | 원가/칼로리/활성화 UI는 근거 없음 표시 또는 숨김 |
| 05 `A-006` → `SCR-018 / Admin / Payment Methods` | `payment_method_config.name,is_active,sort_order`, API-013/014 | `PaymentMethodRow(name,isActive,sortOrder,loading)` | CARD 외 방법을 실사용 가능처럼 표시하지 않음 |
| 05 `A-007` → `SCR-019 / Admin / Sales Summary` | API-015 `from,to`, 일별 매출/메뉴별 판매량 | `DateRange`, `SalesChart`, `state=loading|empty|error|default` | 매출/건수는 지원; 평균/결제수단/환불 KPI는 수동 확인 |
| 06 Hi-fi | 05의 승인된 화면과 같은 API/DTO 계약 | 05와 같은 Component Set 인스턴스 | 새 데이터 구조를 만들지 말고, 05의 확정 상태를 hi-fi로 반영; 빈 페이지면 위 7개를 우선 배치 |
| 키오스크 연계(06에 포함 시) | API-002~006: `baseKcal`, 옵션 `extraPrice/extraKcal`, order `totalPrice`, payment `amount/paidAt` | `MenuCard`, `OptionGroup`, `CartItem`, `PaymentMethodCard`, `BottomCTA` | 가격/칼로리/품절/결제 실패/완료 상태가 관리자 화면과 같은 Enum/문구를 사용해야 함 |

### 명명 계약

```text
orderStatus       → ORDER_STATUS          → Badge.orderStatus=received|preparing|completed
paymentStatus     → PAYMENT_STATUS        → Badge.paymentStatus=ready|approved|failed
isSoldOut         → menu/ingredient/item  → state=soldOut 또는 disabled=true
extraPrice        → option item           → additionalPriceText
totalPrice        → order/API-005          → BottomCTA.totalAmount / OrderTable.amount
payment.amount    → API-006               → OrderComplete.paidAmount
baseKcal/extraKcal→ menu/options API      → nutrition.baseKcal / nutrition.estimatedKcal
```

Figma의 status 값은 API Enum을 소문자 property 값으로만 변환하고, 표시 문구는 별도 text property/문구 사전(`접수`, `준비중`, `완료`, `결제 대기`, `결제 승인`, `결제 실패`)으로 둔다. `Property 1`, `Variant2`, `Frame …`, `sourse` 같은 자동/오탈자 명명은 제거한다.

## D. Figma Agent에 전달할 최종 프롬프트

```text
당신은 ASAK Figma 파일 “ASAK — Design System / Product UI — 2026-07-14”의 편집 담당자다. 우선 `💻 05. 관리자 웹 와이어프레임`과 `🖼️ 06. Hi-fi 디자인`을 점검·수정한다. 수정 전 05/06의 모든 Frame, Component Set, 인스턴스 연결, 이름, 레이어, 오버플로우를 스캔하고 아래의 프로젝트 계약과 대조하라.

[근거와 제한]
- 실제 Spring backend는 health endpoint만 구현된 골격이다. API-001~020은 `ASAK-Kiosk/src/contracts/api-data-contract.md`와 `ASAK/docs/wiki/rest-api-spec.md`의 구현 계약이다. DB는 `ASAK/asak-data/schema-backups/short-name-before-20260713-115747.sql`, seed는 `seed-v3`을 근거로 한다.
- DB/API/실제 코드 근거 없이 기능, 숫자, 메뉴명, 가격, 칼로리, 결제수단, KPI를 발명하지 말라. 예시 데이터는 `Sample` 또는 교체 가능한 text property로만 둔다.
- 화면 ID와 주요 Component Set 이름, 브랜드 색/디자인 방향, 정상 인스턴스 연결을 임의로 깨거나 재설계하지 말라. 안전하게 이름을 보완할 때는 기존 ID를 보존하고 alias/description으로 이전 이름을 남긴다.
- React 코드를 생성하지 않는다. 대신 배열 렌더링과 props에 적합한 Auto Layout·Component Property·Variant 구조를 만든다. 불명확한 데이터는 `__manual-check` 메모로 남기고 확정 UI로 만들지 않는다.

1) 프로젝트 기준 확인
- 공통 응답 envelope는 `{ success,status,code,message,data }`, API 필드는 camelCase다.
- 실제 상태: orderStatus=`RECEIVED|PREPARING|COMPLETED`, paymentStatus=`READY|APPROVED|FAILED`, orderType=`EAT_IN|TAKE_OUT`, 품절 targetType=`MENU|INGREDIENT|OPTION_ITEM`.
- 가격: `lineTotal=(unitPrice + Σ(extraPrice×optionQuantity))×itemQuantity`, `orderTotal=Σ(lineTotal)`, `payment.amount=최종 결제 요청/승인 금액`. 현재 discount/refund/원가/결제 실패 사유는 계약에 없다.
- 영양: `baseKcal`, `extraKcal`은 표시 가능하나 최종 주문 영양 스냅샷은 없다. “예상” 표기 외 확정 총칼로리를 만들지 말라.

2) 05 화면과 데이터 대조·직접 수정
- A-001~A-007이 있으면 다음 권장 이름을 description에 추가하고, 안전하면 Frame 이름을 변경한다: `SCR-015 Admin Login`, `SCR-009 Admin Order List`, `SCR-010 Admin Order Detail`, `SCR-011 Admin Sold-out Management`, `SCR-016/017 Admin Menu Manage/Edit`, `SCR-018 Admin Payment Methods`, `SCR-019 Admin Sales Summary`.
- Order List는 `orderNo,orderType,orderStatus,paymentStatus,totalPrice,createdAt` 컬럼과 loading/empty/error/default, 상태 필터, 검색, pagination 영역을 갖춘다.
- Order Detail은 `items`, 선택 옵션(`selectedOptions`/order_item_option), 제외 재료(`excludedIngredients`/item_exclusion), 수량, 단가, 항목 합계, totalPrice, paymentStatus를 구분한다. 상태 변경에는 confirm/pending/failed 상태를 만든다.
- Sold-out Management는 MENU/INGREDIENT/OPTION_ITEM 필터, name, isSoldOut, reasonType, Toggle pending/success/error/empty 상태를 만든다. 핵심 재료 품절=메뉴 주문 불가, 일반 재료/옵션 품절=선택 불가 안내를 구별하는 UI를 만든다.
- Menu Form은 `categoryId,name,price,imageUrl,optionGroupIds`만 확정 필드로 둔다. 원가·영양편집·활성화·태그 저장은 `__manual-check`로 남긴다.
- Payment Methods는 `name,isActive,sortOrder`로 구성하며 현재 CARD 한 종류를 다중 수단처럼 확정 표시하지 않는다.
- Sales Summary는 from/to 기간, 일별 매출, 메뉴별 판매량, loading/empty/error을 만든다. 평균 주문금액·결제수단별 통계·할인/환불 KPI는 확정 카드로 추가하지 않는다.

3) 06 Hi-fi 직접 수정
- 06이 비어 있으면 05에서 검증한 관리자 7개 화면의 hi-fi 버전을 우선 배치한다. wireframe과 hi-fi가 서로 다른 데이터/상태를 요구하지 않게 동일 Component Set 인스턴스를 사용한다.
- 06에 키오스크 화면이 있거나 추가하는 경우: MenuCard=`menuName,image,price,baseKcal,isSoldOut,hasSoldOutIngredient,tags`; OptionGroup=`minSelect,maxSelect,isRequired,extraPrice,extraKcal,isRecommended,isSoldOut`; CartItem=`menuName,optionSummary,exclusionSummary,quantity,unitPrice,lineTotal`; 결제/완료=`totalPrice,payment.amount,paymentStatus,orderNo,paidAt`를 적용한다.
- 할인, 환불, 확정 최종 칼로리, 근거 없는 결제수단은 만들지 않는다.

4) 컴포넌트·Variant·Auto Layout 정리
- `Button(label,leadingIcon,trailingIcon,disabled,loading,variant)`, `OrderStatusBadge(orderStatus,paymentStatus)`, `OrderDetailRow`, `SoldOutToggle`, `PaymentMethodRow`, `DataTable`, `EmptyState`, `ErrorState`, `LoadingState`, `Modal/ConfirmDialog`을 재사용 가능하게 한다.
- `state=default|loading|empty|error|disabled|soldOut|selected|processing`은 실제 해당 컴포넌트에만 만들고, 주문/결제 상태는 위 Enum 범위만 variant/property로 제공한다.
- Auto Layout과 Hug/Fill/Fixed를 정리하고 반복 행은 vertical/horizontal Auto Layout으로 구성한다. 텍스트 잘림, 오버플로우, 겹침, 불필요한 absolute position을 수정한다. 정상 Component Set을 불필요하게 분할하지 않는다.
- Property 이름은 `menuName`, `unitPrice`, `additionalPrice`, `lineTotal`, `totalAmount`, `baseKcal`, `estimatedKcal`, `isSoldOut`, `orderStatus`, `paymentStatus`처럼 API/React prop에 맞춘 camelCase를 쓴다. DB snake_case를 Figma property에 사용하지 않는다.

5) 흐름과 재검증
- 최소 Prototype: 관리자 주문목록 → 주문상세 → 상태변경 confirm → 성공/실패, 품절관리 → 토글 pending/성공/실패, 매출 → 기간필터 → 데이터/빈/오류를 연결한다.
- 키오스크 인스턴스가 있으면 홈 → 메뉴 → 옵션 → 장바구니 → 결제 → 처리중 → 완료와 결제실패·timeout 분기도 확인한다.
- 완료 후 05/06 전체에서 누락, 겹침, 잘림, 오버플로우, 깨진 instance, 자동 이름, enum 밖 상태, 하드코딩 금액/칼로리를 다시 검사한다.
- 마지막으로 수정 보고서를 작성한다: 수정한 Frame/Component ID, 근거 파일/API/DB 필드, 추가한 Property/Variant, 제거 또는 `__manual-check`로 남긴 항목, 확인하지 못한 사항, 깨진 인스턴스 0건 여부.
```

## E. Figma 밖에서 해결할 항목

| 분류 | 필요한 결정/변경 |
| --- | --- |
| DB | 할인/쿠폰·환불·결제 실패 사유, 주문 당시 메뉴/옵션명·가격·영양 스냅샷, 메뉴 활성 상태, 필요 시 원가와 결제수단별 집계의 저장 모델 |
| API | API-005 항목별 금액/할인 필드, API-006 실패 `code/message`와 취소/재결제 계약, API-015 응답 스키마·지원 KPI 확정, 영양 예상/확정의 책임 주체 |
| DTO/백엔드 | menu/order/payment Entity·DTO·Repository·Service·Controller 구현, snake_case DB↔camelCase API 매핑, 핵심/일반 재료 품절 계산, 서버 측 총액 검증·가격 스냅샷 |
| Enum/상수 | `constants/status.js`, `constants/order.js`, 수량 최소/최대, 옵션 최대 선택, timeout, 페이지 크기, 오류/성공 문구를 단일 모듈로 정의 |
| 프런트 | `cartRules.js`, `soldOutPolicy.js`, `useKioskTimeout.js`, 타입 정의, 모든 placeholder 페이지/컴포넌트 구현; API 오류/로딩/빈 상태 연결 |
| 기획 | timeout 경고 여부와 시간, 취소/환불 지원, 할인 정책, 영수증/바코드·QR의 MVP 범위, 매출 KPI와 결제수단 범위 |

## 감사 근거 파일

- `docs/design/ASAK_FIGMA_MCP_REVIEW_2026-07-14.md`
- `docs/wiki/db-table-definition.md`, `docs/wiki/rest-api-spec.md`, `docs/wiki/requirements-definition.md`, `docs/wiki/user-scenarios.md`
- `asak-data/schema-backups/short-name-before-20260713-115747.sql`, `asak-data/seed-v3/*.json`
- `../ASAK-Kiosk/src/contracts/api-data-contract.md`, `src/store/orderSessionStore.js`, `src/features/order/orderFlow.js`, `src/api/*.js`, `src/pages/**/*.jsx`, `src/components/**/*.jsx`
- `../ASAK-back/src/main/java/**` (health-only skeleton 확인)
