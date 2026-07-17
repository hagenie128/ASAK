# FRONTEND 80% 실행 계획 (2026-07-16)

> 목적: 금요일~수요일 동안 사람이 직접 React(JavaScript) 코드를 작성할 수 있도록, 현재 Figma·Product Bible·Screen Registry·API/DB 문서·저장소를 대조한 단일 실행 계획이다. 이 문서는 구현 코드가 아니다.
>
> 기준 우선순위: 실제 Git/코드 → `ASAK/docs` → Product Bible → Figma. TypeScript와 Tailwind는 사용하지 않는다.

## 1. 현재 상태

### 조사 결과

| 영역 | 현재 확인 결과 | 판단 |
|---|---|---|
| Git | 루트에서 `ASAK`, `ASAK-Admin`, `ASAK-Kiosk`, `ASAK-back` 변경이 이미 존재 | 기존 변경을 덮어쓰지 말고 담당자가 확인 후 작업한다. |
| Figma | 문서에는 `kiosk_design`(`iqao...`)와 7/14 MCP 점검 대상 `ASAK`(`o9mx...`)가 함께 존재한다. 두 파일의 직접 메타데이터 조회는 각각 최상위 한 페이지만 반환했다. 7/14 점검 문서는 Button/MenuCard/OptionCategory/CartItem/PaymentMethodCard 등의 데이터 Property 추가를 기록한다. | 프론트 구현 전 **현재 사용 중인 Figma 파일과 SCR별 Frame**을 팀이 확정해야 한다. 확정된 Figma Property는 목업 DTO의 필수 필드로 반영한다. |
| Kiosk | React Router 7, Zustand 5, Axios, Vite, CSS가 설치되어 있다. `/`, `/menu`, `/menu/:menuId`만 실제 라우팅됨. Menu List는 mock, Detail은 mock+옵션+수량 초안까지 부분 구현. Cart/Payment/Complete는 자리표시자다. | P0의 시작점은 있으나 핵심 흐름 완성 전이다. |
| Admin | 별도 Vite 앱과 sidebar shell은 있으나 페이지/API/store가 거의 placeholder다. | 수요일에는 P1 중 Live Order/Sold-out의 mock 화면만 목표로 제한한다. |
| Backend | Spring Boot 4.1.0, Java 25, Gradle. 실제 business API는 없고 `/api/health`만 구현됨. | 모든 business 연결은 `SPEC_ONLY` 또는 mock adapter다. `IMPLEMENTED`로 표시하면 안 된다. |
| 계약 | REST 문서는 canonical 후보를 `/api/kiosk/*`, `/api/admin/soldOut`로 override했지만 기존 상세 명세는 `/api/menus`, `/api/orders`, `/api/admin/sold-out-items`다. Figma에는 화면 표시용 속성이 추가되고 있다. | 목업은 최종 API envelope·camelCase·필드명을 먼저 따른다. Figma 전용 표시 속성은 API 응답을 바꾸지 않고 mapper가 만드는 View Model로 분리한다. |

### 80%의 현실적 정의

수요일까지의 80%는 **최종 백엔드 계약과 같은 필드명의 목업 기반 P0 Kiosk end-to-end 흐름 + 공통 상태 + 품절/장바구니 규칙 + P1 Admin 두 화면의 skeleton**이다. 실제 API 연결은 포함하지 않지만, 이후 mock source만 real source로 교체할 수 있는 adapter 구조를 갖춘다. TTS, 매출, 영수증, 멤버십 및 픽셀 단위 Figma polish는 이후 범위다.

## 2. P0 누락 로직 감사

판정: `부분`은 문서 또는 현재 코드 한쪽에만 있어 실제 사용자 흐름으로는 아직 구현 불가한 상태다. 아래의 `누락/모호` **22건**을 P0 누락으로 집계한다.

### A. 장바구니

| 기능 | 현재 정의 위치 | 누락 여부 | React 구현 영향 | 필요한 State / Action / API | 우선순위 |
|---|---|---|---|---|---|
| 개별 제품 삭제 | SCR-005, CART-006; `removeItem`만 존재 | UI·확인 모달 누락 | CartItem/ConfirmDialog | `pendingDeleteId`, `removeCartItem` | P0 |
| 수량 증가/감소 | `quantityLimits.js`, Detail 수량만 부분 구현 | Cart line action/UI 누락 | CartItem/total 동기화 | `increaseQuantity`, `decreaseQuantity` | P0 |
| 수량 1 minus 정책 | CART-004: 비활성·자동삭제 금지 | Detail만 `Math.max`; Cart 미구현 | minus disabled | `quantity===1` selector | P0 |
| 전체 비우기 | 없음 | 누락 | Header/Cart CTA | `clearCart`, 확인 모달 | P0 |
| 마지막 삭제 후 Empty | CART-007 | Page state 누락 | EmptyState 전환 | `items.length===0` | P0 |
| 중간 항목 삭제 총액 재계산 | CART-003/007 | 계산 action 누락 | Footer 총액 | derived `calculateCartTotal` | P0 |
| 옵션 수정 | SCR-005/CART-005 | 편집 진입·draft·저장 누락 | Detail 재사용 또는 modal | `editingCartItemId`, `updateCartItem` | P0 |
| 옵션 수정 취소 | CART-005 원본 불변 | UI/state 누락 | draft 폐기 | `cancelEdit` | P0 |
| 옵션 수정 저장 | CART-005 | line 교체·총액 재계산 누락 | 기존 item만 갱신 | `updateCartItem(cartItemId, patch)` | P0 |
| 옵션 수정 실패 | SCR-005 validationError | 실패 contract/표시 누락 | 입력 보존/Toast | `editError`; cart validate adapter | P0 |
| 수정 후 Cart 복귀 | SCR-005 | route state 규칙 누락 | Detail의 신규추가 방지 | `mode=edit&cartItemId` | P0 |
| 동일 menuId 최대 9 | `quantityLimits.js` | 다중 옵션 line 합산은 부분 구현; update/set 검증 없음 | add/edit/increase 모두 같은 정책 | `validateMenuLimit(items, menuId, nextQty)` | P0 |
| 전체 최대 30 | `quantityLimits.js` | add 외 모든 경로 검증·직원 안내 누락 | line update/add | `validateCartLimit` | P0 |
| 초과 Toast·상태 유지 | Detail increase에서만 부분 | Cart/option edit 누락 | Toast host | `toastQueue`; mutation 전 validation | P0 |
| 30개 이상 직원 문의 | 요구사항 | 9개 메시지와 30개 메시지 정책 혼재 | 문구 분리 | `CART_LIMIT` 전용 Toast | P0 |
| 초과 시도 때만 30개 안내 | 요구사항 | 상시 노출 방지 조건 미정 | Conditional toast | 실패 순간만 enqueue | P0 |

**결정 필요:** 같은 메뉴·같은 옵션은 합산할지(권장: 합산), 같은 menuId·다른 옵션은 별도 line을 유지할지(CART-002 기준: 유지)를 확정한다. `cartItemId`만 line 식별자로 사용한다.

### B. 품절

| 기능 | 현재 정의 위치 | 누락 여부 | React 구현 영향 | 필요한 State / Action / API | 우선순위 |
|---|---|---|---|---|---|
| 메뉴 품절 | 메뉴 API 예시의 `isSoldOut`; SCR-003 | UI/선택 차단 누락 | MenuCard | `isOrderable`, `soldOutReason` | P0 |
| 핵심재료 품절 | API 예시 `hasSoldOutIngredient` | 메뉴 주문불가 규칙 미정 | Detail CTA | `soldOutReason=CORE_INGREDIENT` | P0 |
| 일반재료 품절 | Detail ingredient `isSoldOut` | 제거/대체 가능 규칙 미정 | Ingredient/option row | `unavailableOptionIds` | P0 |
| 베이스 품절 | Option API `isSoldOut` | 필수 베이스 대체·CTA 규칙 미정 | OptionGroup validation | `unavailableOptionIds`, required validation | P0 |
| 카테고리 품절 | 없음 | 누락 | CategoryTabs/EmptyState | `categoryStatus` 또는 menu aggregate | P0 |
| List/Detail 표시 | SCR-003 badge 원칙, SCR-004 states | Badge 문구·선택 불가 기준 누락 | SoldOutBadge, disabled CTA | normalized sold-out selector | P0 |
| 다른 메뉴 정상 사용 | 요구사항 | store 갱신 범위 미정 | stale cache 방지 | menu별 immutable update | P0 |

**권장 정규화 계약:** `isOrderable`, `soldOutReason`, `unavailableOptionIds`를 Menu Detail mapper의 필수 출력으로 둔다. 메뉴/핵심재료는 메뉴 진입 또는 CTA를 막고, 일반재료/옵션은 해당 항목만 disabled한다. 카테고리는 모든 메뉴가 orderable=false일 때만 ‘주문 가능한 메뉴 없음’ Empty를 보인다.

### C. 결제

| 기능 | 현재 정의 위치 | 누락 여부 | React 구현 영향 | 필요한 State / Action / API | 우선순위 |
|---|---|---|---|---|---|
| No Method Selected | SCR-007 collapsed | Page/state 누락 | CTA disabled | `selectedMethodId=null` | P0 |
| Method Selected | SCR-007 expanded | 목록/선택 상태 누락 | PaymentMethodList | `selectPaymentMethod` | P0 |
| Processing | SCR-007/PAY-006 | 상태 전이 누락 | overlay/CTA/back guard | `status=processing` | P0 |
| All Methods Disabled | PAY-005 | Empty/안내 규칙 누락 | disabled list + support CTA | `methods.every(!enabled)` | P0 |
| Load Error/Retry | Screen requires states | API/Retry 누락 | ErrorMessage | `loadStatus`, `retryLoadMethods` | P0 |
| Payment Error/Retry | SCR-012, PAY-003 | error overlay/재시도 계약 누락 | Error modal/Cart 유지 | `paymentError`, `retryPayment` | P0 |
| Timeout processing 중 비활성 | SCR-007/PAY-006 | `useKioskTimeout` 연결 정책 누락 | timeout guard | `isInteractionLocked` | P0 |
| waitingOrderCount | SCR-008 | response field/API 미정 | CompletePage | `complete.waitingOrderCount` | P0 |
| 완료 후 Home 복귀 | SCR-008 | reset 타이밍 누락 | timer + navigate | `resetSession` after display | P0 |

## 3. React 구조

### 원칙

- Kiosk와 Admin은 현재처럼 독립 앱을 유지한다. 공통 코드는 각 앱의 `components/common`, `api/client`, `constants`에서 먼저 재사용하고, 두 저장소를 억지로 합치지 않는다.
- Page는 route·조합·screen state만 맡고, Axios 호출은 API module → mapper/repository → hook/store로 흐르게 한다.
- 금액은 state에 중복 저장하지 않고 `items`에서 selector로 계산한다. 서버 응답 total은 검증/표시용 snapshot으로만 둔다.

### 화면별 Component Tree

| Screen | Page / Layout | Component Tree | Store·API |
|---|---|---|---|
| SCR-001 | `HomePage` / `KioskLayout` | Header → OrderTypeSelector → BottomCTA | `orderSessionStore.setOrderType` |
| SCR-003 | `MenuListPage` / KioskLayout | Header → CategoryTabs → (LoadingSpinner | ErrorMessage+Retry | EmptyState | MenuCardGrid) → CartFooterBar → Toast | `menuStore`; `menuApi.getMenuList` |
| SCR-004 | `MenuDetailPage` / KioskLayout | Header → MenuDetailSummary → SoldOutNotice → OptionGroup[] → QuantityStepper → BottomCTA → Toast | `menuStore`, `cartStore`; `menuApi.getMenuDetail` |
| SCR-005 | `CartPage` / KioskLayout | Header → (EmptyState | CartItemCard[]) → OrderSummary → BottomCTA → DeleteConfirmDialog / EditOptionsModal → Toast | `cartStore`; `orderApi.validate/create` |
| SCR-007/012 | `PaymentPage` / KioskLayout | Header → PaymentMethodList → PaymentProgress → BottomCTA → PaymentErrorModal → Toast | `paymentStore`, `orderStore`; `paymentApi` |
| SCR-008 | `OrderCompletePage` / KioskLayout | Header → OrderNumber → WaitingOrderCount → ReceiptActions(optional) → AutoReturnTimer | `orderStore`, `paymentStore` |
| SCR-009 | `LiveOrderBoardPage` / `AdminLayout` | AdminSidebar → StatusSummary → (Loading/Empty/Error | OrderCard[]) → TtsControl | `adminOrderStore`; admin order API/mock |
| SCR-010 | `OrderListPage` / AdminLayout | Sidebar → FilterBar → OrderTable → Pagination → OrderDetailPanel | `adminOrderStore` |
| SCR-011 | `SoldOutManagePage` / AdminLayout | Sidebar → TargetTabs → FilterChips → SoldOutRow[] → SaveBar → ConfirmDialog | `adminMenuStore`; `adminApi.soldOut` |
| SCR-016/018/019 | existing Admin pages / AdminLayout | Sidebar → page-specific list/form/chart + shared states | `adminMenuStore` / `paymentStore` / `salesStore` |

### 파일 책임

| 분류 | 권장 위치 | 책임 |
|---|---|---|
| Shared | `src/components/common` | Button, Modal, ConfirmDialog, LoadingSpinner, EmptyState, ErrorMessage, ToastHost |
| Kiosk | `src/components/kiosk` | MenuCard, OptionGroup, QuantityStepper, CartItemCard, PaymentMethodList, CartFooterBar |
| Admin | `ASAK-Admin/src/components/admin` | Sidebar, OrderTable/Card, StatusBadge, SoldOutRow, SalesChart |
| Hook | `src/hooks` | `useAsync`, `useKioskTimeout`, `useMenu`, `useOrder`; 추가 hook은 API lifecycle에만 사용 |
| Utility | `src/utils` | currency, priceCalculation, apiError, quantityLimits, cartLineKey |
| Constant | `src/constants` | routes, status, order, API paths, toast messages |
| Mock | `public/mocks` 또는 `src/mocks` | API envelope를 흉내 낸 screen state별 fixture |
| API | `src/api` | Axios client, endpoint, mapper/repository. Page Axios 직접 호출 금지 |

## 4. Zustand 구조

### Store별 범위

| Store | 최소 State | 최소 Action | 비고 |
|---|---|---|---|
| `cartStore` | `items`, `editingCartItemId`, `pendingDeleteId`, `toast` | 아래 표 action, `start/cancelEdit` | 현재 `orderSessionStore`에 합쳐져 있으므로 당장 분리보다 compatibility export 유지 후 action 보강을 권장 |
| `menuStore` | `categories`, `menusByCategory`, `detailsById`, `loadStatus`, `error` | fetch/retry/invalidate | 품절 normalized data 소유 |
| `orderStore` | `order`, `createStatus`, `createError` | create/reset | cart snapshot으로 주문 생성 |
| `paymentStore` | `methods`, `selectedMethodId`, `status`, `error` | load/select/submit/retry/reset | processing 단일 진입점 |
| `adminOrderStore` | `orders`, `filters`, `selectedOrder`, `status` | fetch/select/changeStatus | polling 최신 요청만 반영 |
| `adminMenuStore` | `soldOutTargets`, `draftChanges`, `saveStatus` | toggle/save/revert | optimistic update 금지, 성공 후 반영 |
| `salesStore` | `range`, `summary`, `status` | fetch/setRange | P2 우선 |

### cartStore State Shape (제안)

```js
{
  items: [{
    cartItemId, menuId, menuName, imageUrl, unitPrice, quantity,
    optionItems: [{ optionItemId, optionGroupId, name, extraPrice, quantity }],
    excludedIngredientIds: []
  }],
  editingCartItemId: null,
  pendingDeleteId: null,
  toast: null
}
```

### cartStore Action 계약

| Action | 입력 → 반환 | 실패 조건 | Toast | 총액 재계산 |
|---|---|---|---|---|
| `addCartItem` | draft item → `{ok, cartItemId}` | menu 9/전체 30, menu not orderable, 필수 옵션 미충족 | 제한/품절/검증 실패 | 성공 직후 selector |
| `removeCartItem` | cartItemId → `{ok}` | ID 없음 | 없음(취소 시 없음) | 성공 직후 |
| `clearCart` | 없음 → `{ok}` | 없음 | 확인 후만 ‘비워짐’ 선택 | 성공 직후 0 |
| `updateCartItem` | cartItemId, draft → `{ok}` | ID 없음, limit/option validation 실패 | 실패 사유 | 성공 직후; 새 item 추가 금지 |
| `setItemQuantity` | cartItemId, qty → `{ok, reason?}` | qty<1, menu 9, cart 30 | limit 시만 | 성공 직후 |
| `increaseQuantity` | cartItemId → `{ok, reason?}` | menu/cart limit | `MENU_LIMIT`/`CART_LIMIT` | 성공 직후 |
| `decreaseQuantity` | cartItemId → `{ok:false, reason:'MINIMUM'}` | quantity=1 | 없음; minus disabled가 기본 | 성공 시 |
| `calculateCartTotal` | items → `{totalQuantity,totalAmount}` | 없음 | 없음 | mutation 후 selector가 호출 |
| `validateMenuLimit` | items, menuId, nextQty → `{valid, reason}` | 동일 menuId 합계>9 | 호출자가 표시 | mutation 전 |
| `validateCartLimit` | items, delta → `{valid, reason}` | 전체>30 | 호출자가 표시 | mutation 전 |

## 5. 화면별 API 연결

`ASAK-back`에는 business endpoint가 없으므로 아래는 모두 `SPEC_ONLY` 또는 `CANONICAL_PROPOSED`다. mock은 동일 envelope와 mapper 결과를 반환해야 한다.

### 목업 우선 계약 규칙 (확정)

1. mock JSON도 실제 응답처럼 `{ success, status, code, message, data }` envelope와 **camelCase API 필드명**을 사용한다. Page/컴포넌트는 mock인지 실제 API인지 알면 안 된다.
2. API DTO와 Figma 표시 Property를 구분한다. 예를 들어 API의 `price`, `isSoldOut`, `soldOutReason`, `unavailableOptionIds`는 그대로 받고, Figma `MenuCard`의 `recommended`, `image`, `calories`, `disabled` 같은 표시값은 `mapMenuToCardViewModel`이 만든다.
3. Figma에서 새 Property가 추가되면 다음 표에 먼저 기록한다. **API 계약 필드인지, 화면 전용 derived field인지**와 null/disabled 상태를 정한 뒤 mock fixture에 추가한다. 임의의 snake_case나 Figma 레이어명은 JSX/store에 직접 넣지 않는다.

| Figma 컴포넌트 Property | API DTO 원본 필드 | View Model 규칙 | 상태 |
|---|---|---|---|
| MenuCard: `menuName`, `price`, `calories`, `soldOut`, `recommended`, `ingredientSoldOut` | `name`, `price`, `baseKcal`, `isSoldOut`, `hasSoldOutIngredient`, `soldOutBadges` | `isOrderable`와 reason으로 CTA/Badge 결정 | Figma 최신 Frame 확인 필요 |
| OptionCategory: `title`, `required`, `maxSelectable`, `status` | `name`, `isRequired`, `maxSelect`, `items[].isSoldOut` | `status`는 required validation/품절에서 derived | Figma 최신 Frame 확인 필요 |
| CartItem: `menuName`, `optionSummary`, `quantity`, `unitPrice`, `soldOut`, `expanded` | cart line fields + detail validation | `optionSummary`, `lineAmount`, `expanded`는 local derived | mock 구현 대상 |
| PaymentMethodCard: `methodName`, `selected`, `disabled`, `icon` | payment method DTO (명세 확정 필요) | `selected`는 paymentStore, `disabled`는 API enabled/maintenance에서 derived | mock 구현 대상 |
| Complete: `orderNo`, `paidAt`, `paymentStatus`, `waitingOrderCount` | order/payment DTO | waiting count는 canonical 응답에 추가 확인 | P0 계약 확인 필요 |

### 권장 목업 파일 경계

```text
public/mocks/                # raw API envelope fixture (final DTO field names)
src/api/*.js                 # Axios 또는 mock repository 선택
src/api/mappers/*.js         # API DTO -> 화면 View Model
src/mocks/handlers/*.js      # status별 fixture 선택/지연/실패 시뮬레이션 (필요 시)
```

`kiosk.json`처럼 Page가 직접 읽는 형태는 이번 구현에서 점진적으로 repository 뒤로 숨긴다. 기존 mock 필드가 final DTO와 다르면 **mock을 먼저 계약에 맞게 변경하고 mapper 테스트 표본을 추가**한다. 이것은 실제 backend 연결 작업이 아니라 목업 기반 프론트 구현의 선행 조건이다.

| Screen | API / 상태 | Request | Response 핵심 | Loading / Empty / Error / Retry | Mock 필요 |
|---|---|---|---|---|---|
| SCR-003 | GET `/api/kiosk/menuList` — CANONICAL_PROPOSED | `categoryId` | categories, menu cards, soldOut fields | 모두 필요 | 예 |
| SCR-004 | GET `/api/kiosk/menuDetail/{menuId}` — CANONICAL_PROPOSED | menuId | menu, groups, `isOrderable`, `unavailableOptionIds` | loading/error/soldOut; retry | 예 |
| SCR-005 | POST `/api/kiosk/orders` — CANONICAL_PROPOSED; cart validate는 SPEC_ONLY | items/orderType | orderId, orderNo, totalPrice | orderCreating/error/retry; empty는 local | 예 |
| SCR-007 | POST `/api/kiosk/payments` — CANONICAL_PROPOSED; methods GET은 SPEC_ONLY | orderId, method, amount | payment status, orderNo | load/error/retry/processing/all-disabled | 예 |
| SCR-008 | payment approved response — SPEC_ONLY | - | orderNo, totalAmount, `waitingOrderCount` | success/auto-return; count field 확인 | 예 |
| SCR-009/010 | admin orders GET/PATCH — SPEC_ONLY | filter/status | orders, status | loading/empty/error/retry | 예 |
| SCR-011 | PATCH `/api/admin/soldOut` — CANONICAL_PROPOSED; GET SPEC_ONLY | target type/id/isSoldOut | changed target, affected menus | loading/empty/save error/retry | 예 |
| SCR-016/018/019 | admin menu/payment/sales — SPEC_ONLY | page별 | page별 | P1/P2 공통 상태 | 예 |

**Adapter 규칙:** `API_ENDPOINTS`의 기존 `/menus` 등 legacy 값과 canonical 후보를 한 번에 바꾸지 않는다. `menuRepository` 같은 mapper에서 `VITE_USE_MOCK`으로 source만 교체하고, backend 계약 확정 PR에서 endpoint만 바꾼다.

## 6. 4일 구현 일정

| 날짜 | 하진 Primary | 나연 Primary | 공통 검토 | 완료 기준 | 위험 |
|---|---|---|---|---|---|
| 금요일 | 기존 파일 inventory, AdminLayout/route map, Figma Component Property inventory | Kiosk route map, cart action 계약, **final API 필드명과 동일한** mock fixture/envelope, Menu List/Detail 품절 selector 설계 | Figma Property→DTO/View Model 표, 22개 P0 owner 확정 | Screen ID·Frame·상태·문구·Property가 표로 확정되고 mock 전환 규칙 합의 | Figma 파일/노드 불일치 |
| 월요일 | SCR-009/011 mock skeleton + Admin shared layout | SCR-001/003/004 연결, cartStore action을 담당자가 구현, SCR-005 기본/empty/delete | Cart QA 001~007 pair review | Home→Menu→Detail→Cart로 이동, limits와 delete가 mock에서 동작 | store action 충돌 |
| 화요일 | Sold-out save draft/error mock, Admin order list 선택적 지원 | option edit/cancel/save, order create mock, SCR-007 수단 선택/processing/error | 품절·결제 상태 표본 QA | Cart→Payment 실패/재시도까지 Cart 보존 | option edit가 새 line 추가 |
| 수요일 | Admin visual QA/문서·Figma MCP 적용 후 연결 후보 정리 | SCR-008 complete/auto return, timeout guard, 전체 Kiosk regression | 80% demo script, unresolved API gap sign-off | 성공/실패/empty/loading/error 핵심 시나리오 통과 | 실제 API 부재, waiting count 미정 |

### 수요일 80%에 포함 / 이후 이관

- **포함(P0):** SCR-001, 003, 004, 005, 007, 008; Toast/Loading/Empty/Error; 장바구니 limits·edit·delete; 메뉴/옵션 품절 mock; 결제 오류·중복 방지·timeout guard.
- **포함(P1 최소):** SCR-009와 SCR-011의 Figma 구조를 반영한 mock/skeleton 및 공통 상태.
- **수요일 이후:** 실제 backend integration, SCR-010 고급 filter/pagination, SCR-016/018, sales(SCR-019~022), TTS, 영수증, 멤버십/쿠폰, 접근성 세부 polish, Figma pixel QA.

## 7. 파일 생성·구현 순서

| 순서 | 먼저 하는 이유 / 선행 의존성 | 완료 확인 | 예상 오류 |
|---|---|---|---|
| 1. `constants` | route/status/toast 문구를 한 기준으로 고정한다. Screen/문구 확정 필요 | UI가 magic string 없이 state를 분기 | legacy/canonical endpoint 혼용 |
| 2. `mocks` | Backend가 없으므로 화면이 독립적으로 진행된다. API envelope 필요 | success/loading/empty/error fixture 각각 렌더 | 실제 API와 필드명 차이 |
| 3. `utils` | price, cart line key, limits는 Page보다 먼저 검증 가능 | 동일/다른 옵션 line 테스트 통과 | total을 state에 이중 저장 |
| 4. Zustand store | 모든 page action의 단일 진입점 | action 계약 표의 결과 반환 확인 | 현재 compatibility export 파손 |
| 5. shared components | 모든 화면 상태의 모양/문구를 통일 | Loading/Empty/Error/Toast가 독립 렌더 | 상태 동시 표시 |
| 6. page skeleton/layout | Figma Screen ID·Frame 기준을 먼저 고정 | 각 route가 해당 Screen ID 표시 | 잘못된 Frame을 구현 |
| 7. router | 보호/복귀/overlay를 URL과 state로 구분 | 6개 kiosk route + admin route 이동 | 뒤로가기 session 초기화 |
| 8. Kiosk pages | P0 사업 흐름의 본체 | Home→Complete demo | option edit/new add 혼동 |
| 9. Admin pages | mock으로 P1 구조를 확보 | 009/011 Loading/Empty/Error | 범위가 P0를 침범 |
| 10. API adapter | 화면 코드를 고치지 않고 mock↔real을 교체 | `VITE_USE_MOCK` 전환 | Page에서 Axios 직접 호출 |
| 11. integration states | 실패가 성공처럼 보이지 않게 한다 | 각 screen state 1회씩 QA | retry duplicate request |
| 12. integration QA | 수량·금액·품절·결제 전이를 검증 | 아래 bug test matrix 통과 | 테스트 fixture 편향 |

## 8. 예상 버그와 예방

| 버그 | 발생 원인 | 발생 화면 | 예방 방식 | 테스트 방법 |
|---|---|---|---|---|
| 같은 menuId 합산 오류 | option 무시 또는 정책 불일치 | Detail/Cart | menuId 합계는 limit용, line은 cartItemId용 | 동일 옵션/다른 옵션 각 추가 |
| 옵션 다른 line 식별 오류 | menuId를 React key로 사용 | Cart | `cartItemId`를 key·mutation ID로 고정 | 두 line 중 하나만 edit/delete |
| quantity 1 minus 삭제 충돌 | decrease가 remove를 겸함 | Cart | disabled, 자동삭제 금지 | qty=1 minus click |
| 옵션 수정이 새 항목 추가 | Detail confirm이 add만 호출 | Detail/Cart | edit mode와 `updateCartItem` 분기 | edit 후 items 길이 불변 |
| total 재계산 누락 | mutation 뒤 cached total 유지 | Cart/Payment/Complete | items-derived selector | delete/edit/qty 뒤 합계 비교 |
| 품절 뒤 기존 cart item 처리 | 상세만 확인 | Cart/Payment | validate mock에서 item issue 반환, 강조+edit/delete | cart 담은 뒤 soldout toggle |
| API/store 필드 불일치 | snake_case/legacy path 혼용 | 전 화면 | mapper와 contract fixture | fixture와 mapper contract test |
| Router 복귀 state 초기화 | page local state 의존 | Detail/Payment | session은 store, UI draft만 local | back/forward 흐름 |
| useEffect 중복 호출 | StrictMode/dependency 불안정 | List/Payment/Admin | AbortController/requestId | dev mode network 호출 수 |
| Axios race condition | 늦은 응답이 최신 category 덮음 | Menu/Admin | abort 또는 latest request id | A→B 빠른 tab 전환 |
| 결제 중복 클릭 | processing 전 disable 지연 | Payment | synchronous lock + disabled + idempotency key | CTA 연타, 요청 1회 |
| Timeout/Processing 충돌 | timer가 payment 중 reset | Payment | processing이면 timeout pause | processing 중 timer 만료 |
| TTS 실패 rollback | 성공 상태변경과 TTS 결합 | Admin Live | status 성공 후 TTS는 비차단 side effect | TTS throw 후 상태 유지 |
| Loading/Empty/Error 동시 표시 | boolean state 난립 | 전 화면 | `status: idle/loading/success/error` enum | 각 status fixture |
| Admin 저장 실패 서버 상태 오인 | optimistic 반영 후 rollback 없음 | Sold-out | draft와 server data 분리, 성공 후 commit | PATCH 실패 후 UI 원복 |

## 9. 완료 기준

- [ ] 각 P0 Screen의 Figma Frame/Node, Default·Loading·Empty·Error·Disabled 상태와 문구를 담당자가 확정했다.
- [ ] Home → Menu List → Detail → Cart → Payment → Complete가 mock으로 한 번에 이동한다.
- [ ] Cart의 delete, qty, min=1, clear, empty, option edit/cancel/save, menu=9/cart=30 규칙이 통과한다.
- [ ] 품절은 메뉴/핵심재료/일반옵션별로 다르게 표현·차단하며 다른 메뉴는 계속 주문할 수 있다.
- [ ] Payment은 미선택/선택/processing/all-disabled/load error/payment error/retry/timeout guard를 가진다.
- [ ] Cart/Payment/Error/Complete의 금액이 동일하고, 결제 요청은 연타해도 한 번이다.
- [ ] API status는 `SPEC_ONLY` 또는 `CANONICAL_PROPOSED`로만 표시하고 Backend 미구현을 숨기지 않는다.
- [ ] Admin 009/011은 mock Loading/Empty/Error와 저장 실패 UI까지 보인다.

## 10. 내일 바로 시작할 첫 작업

### 내일 첫 3시간 작업

1. **0~30분:** 하진·나연이 `SCR_FIGMA_CHECKLIST.md`와 실제 Figma를 열어 SCR-001/003/004/005/007/008의 Frame, 문구, 5개 상태를 체크한다. Figma metadata 불일치가 있으면 node ID를 이 문서의 이슈 목록에 남긴다.
2. **30~90분:** 나연은 cart action 계약 표를 기준으로 현재 `orderSessionStore`에서 유지할 action 이름과 추가 action을 종이에/이슈에 확정한다. 하진은 common state component의 기존 파일과 재사용 가능 여부를 inventory한다.
3. **90~180분:** API fixture의 canonical shape를 하나로 정하고, Home→Menu→Detail에 필요한 mock 상태 표본과 UI mapping TODO를 작성한다. 이 단계는 코드 작성 전 검토 완료가 기준이다.

### 담당자가 직접 작성할 파일 (승인 후)

| 담당 | 우선 파일 |
|---|---|
| 하진 | `ASAK-Admin/src/apps/AdminApp.jsx`, `ASAK-Admin/src/layouts/AdminLayout.jsx`, `ASAK-Admin/src/pages/admin/OrderListPage.jsx`, `ASAK-Admin/src/pages/admin/SoldOutManagePage.jsx`, Admin 공통 컴포넌트/문서 |
| 나연 | `ASAK-Kiosk/src/apps/kiosk/KioskApp.jsx`, `ASAK-Kiosk/src/store/orderSessionStore.js` 또는 승인된 cart store, `pages/kiosk/CartPage.jsx`, `PaymentPage.jsx`, `OrderCompletePage.jsx`, kiosk API adapter·mock·Axios |

### AI에게 맡길 수 있는 검토

- Figma Frame/Screen ID와 JSX component map 대조
- 기존 파일 영향 분석, action signature/props/data shape/의사코드 제안
- API request/response mapper 계약 및 mock fixture 리뷰
- Cart/Payment/품절 edge case 표와 테스트 케이스 리뷰
- 팀원이 작성한 코드의 diff 기반 코드 리뷰와 오류 원인 분석

### AI에게 맡기면 안 되는 실제 코딩

- 담당자 승인 없는 source code 생성·수정·삭제
- 기존 팀원 구현의 일괄 리팩터링 또는 build 통과 목적의 자동 수정
- commit, push, merge, branch 생성
- Figma 수정 및 실제 business API를 구현된 것처럼 표시

## 11. Canonical Figma Reference (최종 검증)

### 판정 원칙

Figma 파일 `JSrjOy668zhfkiLplCkreh`는 MCP에서 직접 확인되었고, `05-C / 06-C / 07-C` 페이지와 2026-07-15 이관·구현 handoff 목적을 가진다. 그러나 Product Bible의 `CANONICAL_SOURCE.md`는 아직 05-B/06-B를 최신으로, 05-C/06-C를 Premium 제안으로 기록한다. 승인 Decision/ADR가 이 충돌을 해소한 증거는 이번 감사 범위에서 찾지 못했다. 따라서 **수요일 프론트 구현용 대표 Frame 후보는 05-C/06-C/07-C로 사용하되, 조직 전체 Figma 정본 확정은 NEEDS_CONFIRMATION**이다. 05-B/06-B를 Final로 사용하지 않는다.

| 항목 | 현재 참조 | 정본 후보 | 근거 | 조치 |
|---|---|---|---|---|
| Figma File Key | Product Bible `MASTER_CONTEXT.md`: `JSrjOy668zhfkiLplCkreh`; 과거 docs에는 `iqao...`, `o9mx...`도 잔존 | `JSrjOy668zhfkiLplCkreh` | MCP 직접 조회: 2026-07-15 이관된 독립 handoff 파일, local component/style/variable 사용 | **NEEDS_CONFIRMATION**: 팀이 파일 URL을 Screen Registry/README에 한 번만 등록 |
| Kiosk 화면 | `05-B` 및 과거 `kiosk_design` 링크 혼재 | `05-C. Screens / Kiosk (Implementation Final)` page `134:7720` | MCP 직접 조회에서 05-C에 SCR-001/003/004/005/007/008/012/013과 상태 frame 존재 | 구현은 05-C 대표 Frame 기준, B는 참조·보존용 |
| Admin 화면 | `06-B`와 과거 Admin wireframe 링크 혼재 | `06-C. Screens / Admin (Implementation Final)` page `134:10606` | MCP 직접 조회에서 06-C page 존재 | 수요일 P1 Admin은 C 기준 후보, 최종 승인 확인 |
| QA/상태 | 문서의 Screen Bible 상태와 Figma state가 분산 | `07-C. QA / Screen State Matrix` page `190:2` | MCP 직접 조회에서 05-C Kiosk State Matrix와 coverage/known issues 존재 | Page 구현 전 Required State를 이 Matrix와 대조 |
| Product Bible 정본 우선순위 | `CANONICAL_SOURCE.md`는 B current/C premium proposal로 기록 | 승인된 C 또는 수정된 Canonical Source | 문서와 실제 handoff file의 상태가 충돌 | 담당자가 Decision/ADR 또는 Canonical Source 갱신 전에는 `NEEDS_CONFIRMATION` 유지 |

## 12. Screen Frame Registry (수요일 구현 기준)

| SCR | Representative Frame | Frame ID | Required States | Implementation Priority |
|---|---|---:|---|---|
| SCR-001 | `SCR-001 / Home / Default` | `134:7721` | default, order type selection, high contrast | P0 |
| SCR-003 | `SCR-003 / Menu List / Default` | `134:7792` | default, loading, empty, error, items added, sold-out, category disabled | P0 |
| SCR-004 | `SCR-004 / Menu Detail / Default` | `134:7810` | option selected, loading, error, menu sold-out, ingredient/base sold-out, edit item/save loading/save error | P0 |
| SCR-005 | `SCR-005 / Cart / Default` | `134:7835` | empty, delete confirm, last item deleted, clear confirm/success, quantity/option updated, limits | P0 |
| SCR-007 | `SCR-007 / Payment / Summary Collapsed` | `134:7861` | expanded, method selected, processing, loading, all methods disabled, network error | P0 |
| SCR-008 | `SCR-008 / Order Complete / Default` | `134:7926` | default, auto-return | P0 |
| SCR-012 | `SCR-012 / Payment Error / Payment Declined` | `134:7900` | network failure, retry loading | P0 overlay |
| SCR-013 | `SCR-013 / Timeout / Expired` | `134:7913` | warning countdown, continue order, expired/reset | P0 overlay |

## 13. API DTO / View Model Contract

### Envelope

기존 REST 명세의 정본 envelope는 `{ success, status, code, message, data }`다. 요청의 간소 예시는 이 구조의 부분집합이므로, 목업은 기존 정본을 우선해 `status`와 `code`를 생략하지 않는다. 성공 시 `data`에는 payload, 오류 시 `data: null`을 둔다.

```json
{ "success": true, "status": 200, "code": "MENU_LIST_SUCCESS", "message": null, "data": {} }
```

```json
{ "success": false, "status": 400, "code": "MENU_SOLD_OUT", "message": "선택한 메뉴는 현재 주문할 수 없습니다.", "data": null }
```

### DTO와 View Model 분리

| 영역 | API DTO (목업도 동일) | Zustand State | Screen View Model / Derived | Figma Display Only |
|---|---|---|---|---|
| Menu List | `menuId`, `menuName`, `basePrice`, `calories`, `imageUrl`, `categoryId`, `categoryName`, `isSoldOut`, `soldOutReason`, `tags`, `allergens` | categories, menu cache, load status | `isOrderable`, badge list, formatted price/calories | card label/아이콘 배치 |
| Menu Detail | 위 menu fields + `description`, `optionGroups`, `ingredients`, `recommendedDressing`, `soldOutIngredientIds`, `soldOutBaseIds` | detail cache, option draft | required-valid, unavailable option/base selector, option additional amount | accordion open/collapse 문구 |
| Cart line | 주문 생성 DTO에는 menuId/quantity/options/exclusions만 전송 | `cartItemId`, items, edit/delete draft | `unitAmount`, `optionAdditionalAmount`, `lineTotal`, `isUnavailable`, `unavailableReason` | ‘옵션 변경’, warning placement |
| Order | `orderId`, `orderNo`, `orderStatus`, `totalAmount`, `waitingOrderCount` | order snapshot/create status | total formatted, order label | ‘2개 메뉴 · 16,800원’ |
| Payment | `paymentId`, `orderId`, `paymentMethod`, `approvedAmount`, `paymentStatus`, `approvedAt` | selected method, processing/error | CTA enabled, retry eligibility | ‘현재 앞에 3개의 주문이 있어요’ |

**명명 충돌(6개):** 기존 계약의 `name/price/baseKcal/totalPrice/amount/paidAt`과 이번 handoff 후보의 `menuName/basePrice/calories/totalAmount/approvedAmount/approvedAt`가 다르다. 목업 기준은 후자 6개를 canonical DTO 후보로 사용하되, Backend DTO 승인 전 `NEEDS_CONFIRMATION`이다. `2개 메뉴 · 16,800원`과 대기 문장은 API DTO에 저장하지 않고 selector에서 조합한다.

## 14. Cart Line Identity

### 확정 정책

- 수정·삭제는 반드시 `cartItemId`로 식별한다. `menuId`는 line key가 아니다.
- 동일 `menuId`라도 옵션이 다르면 별도 line이 가능하다.
- 옵션 수정은 `addCartItem`이 아니라 `updateCartItem(cartItemId, changes)`만 사용한다.
- 취소/실패는 original line을 유지한다. 성공 때 해당 line의 `lineTotal`과 cart total을 다시 계산한다.
- `quantity > 1`일 때만 minus 감소, `quantity = 1`은 minus disabled, 삭제는 별도 action, store에 quantity 0은 저장하지 않는다.
- 동일 menuId의 모든 line quantity 합은 최대 9, cart 전체 합은 최대 30이다.

예: `menuId=101` 샐러드의 A line(기본 드레싱, quantity 2)과 B line(발사믹, quantity 1)은 `cartItemId`가 달라 독립 수정/삭제한다. 하지만 같은 menuId 합계는 3이므로 다음 추가/증가는 총 9까지 허용된다. 즉 **line 분리는 옵션 선택의 문제이고, menuId 합산은 주문 제한의 문제**다.

## 15. Sold-out Revalidation

| 품절 변경 | 메뉴/옵션 정책 | 이미 Cart에 담긴 항목 처리 | 목업 선행 구현 |
|---|---|---|---|
| 일반재료 | 해당 옵션만 선택 불가, 메뉴 주문 가능 | 해당 option이 선택돼 있으면 `isUnavailable=true`, 옵션 변경/삭제 유도 | `unavailableOptionIds` selector |
| 베이스 일부 | 해당 베이스만 선택 불가 | 선택된 베이스가 품절이면 옵션 변경/삭제 유도 | `soldOutBaseIds` selector |
| 필수 베이스 전체 | 메뉴 주문 불가 | line unavailable, 결제 진행 차단 | `isOrderable=false` |
| 핵심재료 | 메뉴 품절로 승격 | line unavailable, 삭제 또는 Cart에서 메뉴 교체 | `soldOutReason=CORE_INGREDIENT` |
| 카테고리 전체 | Category disabled/unavailable | 기존 cart line은 개별 menu revalidation을 따름 | category aggregate selector |

재검증은 **Cart 진입 시**와 **주문 생성 직전**에 필수다. 결제 직전은 주문 생성 결과와 cart snapshot이 달라질 수 있으므로 mock 단계에서는 한 번 더 `validateCartForCheckout`을 호출해 차단한다. 실제 Backend가 생기면 주문 생성/결제 API 중 어느 쪽이 authoritative validation인지 확인한다. `unavailableReason`은 API code/reason을 사용자 문구로 바꾼 View Model 값이며, 기술 오류를 그대로 노출하지 않는다.

## 16. P0 22건 재분류

| # | P0 항목 | 분류 | 담당 / Repository | 선행 작업 | 완료 Evidence | 예상 | 차단 |
|---:|---|---|---|---|---|---|---|
| 1 | cartItemId 삭제 식별 | IMPLEMENT_BEFORE_PAGE | 나연 / ASAK-Kiosk | DTO/line 정책 | 해당 line만 삭제 QA | 30분 | 예 |
| 2 | min=1 minus disabled | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | qty action | CART-004 | 20분 | 예 |
| 3 | clear/empty/total | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | cart selector | 마지막 삭제 Empty | 50분 | 예 |
| 4 | option edit/cancel/save | IMPLEMENT_BEFORE_PAGE | 나연 / ASAK-Kiosk | edit mode contract | item count 불변 QA | 90분 | 예 |
| 5 | option edit failure/original 유지 | MOCK_FIRST | 나연 / ASAK-Kiosk | save-error fixture | original 유지 QA | 30분 | 예 |
| 6 | menuId 9/cart 30 validation | IMPLEMENT_BEFORE_PAGE | 나연 / ASAK-Kiosk | limits utility | limit toast QA | 45분 | 예 |
| 7 | 초과 시에만 직원 안내 | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | toast message | 상시 노출 없음 | 15분 | 아니오 |
| 8 | Cart revalidation | MOCK_FIRST | 나연 / ASAK-Kiosk | sold-out selector | entry/pre-order test | 45분 | 예 |
| 9 | menu sold-out 표시/차단 | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | Menu DTO | list/detail QA | 30분 | 예 |
| 10 | 핵심재료 품절 승격 | MOCK_FIRST | 나연 / ASAK-Kiosk | reason enum | CTA disabled QA | 25분 | 예 |
| 11 | 일반재료 품절 | MOCK_FIRST | 나연 / ASAK-Kiosk | option selector | only option disabled | 25분 | 아니오 |
| 12 | 베이스 일부/전체 품절 | MOCK_FIRST | 나연 / ASAK-Kiosk | base field | option/menu case QA | 35분 | 예 |
| 13 | 카테고리 전체 unavailable | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | aggregate selector | tab disabled/empty | 25분 | 아니오 |
| 14 | 다른 메뉴 계속 주문 | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | immutable cache update | unaffected menu QA | 15분 | 아니오 |
| 15 | Payment 미선택/선택 | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | method DTO | CTA state QA | 25분 | 예 |
| 16 | all-disabled/load error/retry | MOCK_FIRST | 나연 / ASAK-Kiosk | method fixtures | each state render | 40분 | 예 |
| 17 | processing 중복결제 방지 | IMPLEMENT_BEFORE_PAGE | 나연 / ASAK-Kiosk | payment status enum | request 1회 QA | 30분 | 예 |
| 18 | payment error/retry/cart 유지 | MOCK_FIRST | 나연 / ASAK-Kiosk | error fixture | retry/cart QA | 40분 | 예 |
| 19 | timeout processing guard | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | lock selector | PAY-006 | 25분 | 예 |
| 20 | waitingOrderCount/complete | BACKEND_CONFIRMATION | 나연 / ASAK-Kiosk | canonical order DTO | mock visible, API TBD | 30분 | 아니오 |
| 21 | complete 후 home reset | IMPLEMENT_WITH_PAGE | 나연 / ASAK-Kiosk | complete timer | session reset timing QA | 20분 | 예 |
| 22 | 최신 Frame/Property 확정 | FIGMA_CONFIRMATION | 하진 / ASAK docs+Figma | 05-C/07-C review | mapping table sign-off | 45분 | 예 |

`DEFER_AFTER_80_PERCENT`: 실제 Backend endpoint/DTO 연결, TTS, 영수증, 멤버십, Sales, 고급 Admin filter/pagination은 위 22건에서 분리해 수요일 이후로 이관한다.

## 17. First 3-Hour Execution Block (금요일)

| 시간 | 하진 (직접 작성) | 나연 (직접 작성) | 완료 확인 |
|---|---|---|---|
| 0:00–0:30 | `ASAK/docs/implementation/FRONTEND_80_PERCENT_EXECUTION_PLAN_2026-07-16.md`의 05-C Frame/Property 표를 팀 검토로 확정. Source는 수정하지 않음 | `ASAK-Kiosk/src/contracts/api-data-contract.md`를 기준으로 mock canonical DTO 표를 확인 | `rg -n 'JSrjOy|134:7721|134:7792' ASAK/docs/implementation/FRONTEND_80_PERCENT_EXECUTION_PLAN_2026-07-16.md` |
| 0:30–1:30 | `ASAK-Kiosk/src/apps/kiosk/KioskApp.jsx`의 Router/Page Skeleton 범위를 담당자가 작성: `/`, `/menu`, `/cart`, `/payment`, `/complete` | `ASAK-Kiosk/src/mocks/` 및 `src/api/`의 mock adapter를 담당자가 작성: envelope/DTO, mock↔Axios 경계 | `npm run lint`, `npm run build` in `ASAK-Kiosk` |
| 1:30–3:00 | Admin은 수정하지 않고 05-C/07-C state checklist로 Kiosk skeleton review | `ASAK-Kiosk/src/store/orderSessionStore.js`의 cart 기본 action과 `HomePage.jsx`, `MenuListPage.jsx` 최소 렌더링을 담당자가 작성 | Home→Menu 이동, mock menu list render, cart action unit/manual QA |

AI는 Figma Frame↔JSX map, DTO/mapper/action signature, mock fixture, diff와 QA 결과만 리뷰한다. AI가 실제 Router/store/page/mock 코드를 대신 작성하거나 수정하지 않는다.
