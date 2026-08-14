# Frontend Engineering Rules

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `API_CLIENT_RULES.md`
- `FRONTEND_ARCHITECTURE.md`
- `REACT_COMPONENT_RULES.md`
- `STATE_MANAGEMENT_RULES.md`

---

## 원문: `API_CLIENT_RULES.md`

### Frontend API Client Rules

> Status: Current

#### 1. Axios Client

공통 설정:

- baseURL
- timeout
- JSON headers
- response unwrap
- error normalization

---

#### 2. Page에서 URL 직접 작성 금지

나쁜 예:

```js
axios.get("/api/kiosk/menuList");
```

권장:

```js
const data = await kioskApi.getMenuList(params);
```

---

#### 3. API Module

```js
export const kioskApi = {
  getMenuList: (params) =>
    apiClient.get("/api/kiosk/menuList", { params }),

  createOrder: (payload) =>
    apiClient.post("/api/kiosk/orders", payload),
};
```

---

#### 4. Response Envelope

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

Frontend는 공통 함수로 `data`를 unwrap한다.

---

#### 5. Error Normalization

```js
{
  code: "MENU_SOLD_OUT",
  message: "MENU_SOLD_OUT",
  field: null,
  canRetry: true,
  originalError: error
}
```

사용자 문구는 `errorMessageMap`에서 결정한다.

서버 raw message를 직접 노출하지 않는다.

---

#### 6. Request Cancellation

검색·필터처럼 빠르게 바뀌는 요청은 AbortController 또는 최신 요청 우선 정책을 사용한다.

---

#### 7. Duplicate Request

- 결제
- 주문 생성
- 저장
- 상태 변경

은 `isSubmitting`으로 중복 방지한다.

---

## 원문: `FRONTEND_ARCHITECTURE.md`

### Frontend Architecture

> Status: Current

#### 1. 목적

ASAK Frontend는 Kiosk와 Admin을 별도 애플리케이션으로 유지하되, 동일한 설계 원칙을 사용한다.

핵심 목표:

- 화면과 상태를 명확히 분리
- API 교체 가능
- Figma 컴포넌트와 React 컴포넌트 매핑
- 반복 UI 제거
- 구현 중인 scaffold 보호

---

#### 2. 실제 저장소 기준 구조

##### ASAK-Kiosk

```text
src/
├─ api/
├─ apps/
├─ components/
├─ constants/
├─ contracts/
├─ entries/
├─ features/
├─ hooks/
├─ layouts/
├─ mocks/
├─ pages/
├─ router/
├─ store/
├─ styles/
├─ types/
└─ utils/
```

##### ASAK_Admin

```text
src/
├─ api/
├─ apps/
├─ components/
├─ constants/
├─ contracts/
├─ hooks/
├─ layouts/
├─ mocks/
├─ pages/
├─ store/
└─ styles/
```

문서를 이유로 현재 구조를 강제로 바꾸지 않는다.

---

#### 3. Layer Responsibility

##### apps

- App root
- Router composition
- Provider 연결
- Layout 연결

넣지 않는다:

- 비즈니스 계산
- API 세부 로직
- 반복 UI markup

##### pages

- Route 단위 화면
- API 호출 orchestration
- 페이지 상태 조합
- Section 구성

넣지 않는다:

- 재사용 가능한 공통 Button/Card 구현
- API URL 직접 문자열
- 복잡한 비즈니스 계산

##### components

- 재사용 UI
- 명확한 props
- 화면과 독립된 표현

##### features

하나의 기능 단위:

- TTS
- timeout
- cart validation
- sold-out policy
- payment flow

##### hooks

- 여러 컴포넌트에서 재사용되는 React 로직
- DOM/event lifecycle
- API state abstraction

##### store

- 여러 화면에서 공유되는 client state
- Cart
- Order session
- Accessibility
- TTS settings

##### api

- Axios client
- endpoint function
- response unwrap
- error normalization

##### contracts

- Figma/API/화면 계약
- 구현 전 scaffold 문서
- 상태·필드 매핑

---

#### 4. Dependency Direction

권장:

```text
apps
→ pages
→ features/components
→ hooks/store/api
→ constants/utils
```

금지:

```text
utils → pages
common component → specific page
api → React component
store → DOM element
```

---

#### 5. Page Composition

```text
Page
├─ Page Header
├─ Section
│  ├─ Feature Component
│  └─ Common Component
└─ State View
```

예:

```text
CartPage
├─ CartItemList
│  └─ CartItemCard
├─ OrderSummary
├─ BottomCTA
└─ DeleteConfirmDialog
```

---

#### 6. Component Split Rule

분리 기준:

- 다른 화면에서도 사용
- 자체 state가 있음
- 독립된 책임
- 조건 분기가 많음
- 테스트 단위가 됨

분리하지 않는 경우:

- 한 화면에서만 쓰이는 단순 wrapper
- 두세 줄 markup
- props 전달만 늘어나는 경우

`200줄`은 절대 기준이 아니라 분리 검토 신호다.

---

#### 7. Server State와 Client State

##### Server State

- Menu
- Order
- Payment
- Sales
- Sold-out

##### Client State

- Modal open
- Dropdown
- Form draft
- Accessibility
- Cart
- Timeout countdown

서버 응답을 무조건 Zustand에 복제하지 않는다.

---

#### 8. Loading / Empty / Error

모든 서버 데이터 화면은 아래 순서를 고려한다.

```jsx
if (isLoading) return <LoadingState />;
if (error) return <ErrorState />;
if (isEmpty) return <EmptyState />;

return <DefaultView />;
```

Dashboard는 widget별 partialError를 허용한다.

---

#### 9. 완료 기준

- [ ] 실제 구조 유지
- [ ] Page와 Component 책임 분리
- [ ] API URL 분리
- [ ] 상태 누락 없음
- [ ] Figma mapping
- [ ] naming 준수
- [ ] build/lint 통과

---

## 원문: `REACT_COMPONENT_RULES.md`

### React Component Rules

> Status: Current

#### 1. Component Naming

```text
PascalCase.jsx
```

좋은 예:

```text
MenuCard.jsx
CartItemCard.jsx
SalesMetricCard.jsx
IngredientSelectModal.jsx
```

나쁜 예:

```text
menu-card.jsx
menu_card.jsx
Admin/Nav-Item.jsx
```

---

#### 2. Props Naming

```js
camelCase
```

```jsx
<MenuCard
  menuName="멕시칸 랩"
  isSoldOut={false}
  onSelect={handleSelectMenu}
/>
```

Event prop:

```text
onSelect
onClose
onConfirm
onChange
onRetry
```

Handler:

```text
handleSelect
handleClose
handleConfirm
handleRetry
```

---

#### 3. Boolean Props

긍정형 권장:

```text
isLoading
isDisabled
isSelected
showBackButton
canRemove
```

피한다:

```text
notActive
noHeader
isNotVisible
```

---

#### 4. Controlled vs Uncontrolled

ASAK Form/Modal은 controlled component를 우선한다.

```jsx
<OptionGroup
  selectedOptionIds={selectedOptionIds}
  onChange={handleOptionChange}
/>
```

이유:

- Cart 수정 draft 제어
- validation
- Figma state 재현
- 테스트 용이

---

#### 5. Rendering Rules

배열 key:

```jsx
key={item.id}
```

피한다:

```jsx
key={index}
```

Cart는 `cartItemId`.

---

#### 6. Conditional Rendering

복잡한 삼항 연산자 중첩 금지.

나쁜 예:

```jsx
{isLoading ? <Loading /> : error ? <Error /> : data ? <View /> : null}
```

권장:

```jsx
if (isLoading) return <LoadingState />;
if (error) return <ErrorState />;
return <View />;
```

---

#### 7. Business Logic

Component 안에 넣지 않는다:

- 가격 권한 계산
- 품절 전파
- 상태 전이 검증
- API error mapping

Feature/Hook/Service로 분리한다.

---

#### 8. Figma Mapping

Figma와 React 이름을 무조건 동일하게 만들 필요는 없다.

하지만 mapping 문서에 다음을 기록한다.

```text
Figma: Admin/StatusBadge
React: OrderStatusBadge.jsx
```

같은 역할의 중복 컴포넌트를 새로 만들지 않는다.

---

#### 9. Accessibility

- Button은 실제 `<button>`
- form label 연결
- focus outline 유지
- disabled 이유 표시
- icon-only button에 aria-label

---

## 원문: `STATE_MANAGEMENT_RULES.md`

### State Management Rules

> Status: Current
> Library: Zustand

#### 1. Zustand 사용 기준

여러 화면에서 공유되거나 session lifecycle에 포함되는 상태만 store에 둔다.

적합:

- orderSession
- cartItems
- accessibility
- TTS settings

부적합:

- 한 Modal open
- 한 Input value
- 단일 페이지 filter draft

---

#### 2. Store Structure

```js
export const useOrderSessionStore = create((set, get) => ({
  orderType: null,
  cartItems: [],
  orderId: null,
  orderNo: null,
  orderStatus: null,
  paymentStatus: null,

  setOrderType: (orderType) => set({ orderType }),
  addItem: (item) => {},
  resetSession: (reason) => {},
}));
```

---

#### 3. Action Naming

동사형 camelCase:

```text
addItem
removeItem
updateQuantity
updateItemOptions
setOrderType
resetSession
```

---

#### 4. Derived State

가능하면 저장하지 않고 계산한다.

예:

```js
const totalAmount = cartItems.reduce(...);
```

다만 성능 또는 계약상 store에 저장하면 action마다 일관되게 갱신한다.

---

#### 5. Persistence

localStorage 대상:

- Accessibility
- TTS settings

선택 대상:

- Cart

저장하지 않음:

- 결제 처리 중 임시 state
- error object
- modal open

---

#### 6. Reset Policy

reset은 이유를 받는다.

```js
resetSession("ORDER_COMPLETED");
```

공식 reason:

```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
TIMEOUT_EXPIRED
USER_RESET
SESSION_EXPIRED
```

---

#### 7. Store에서 금지

- API 호출 남발
- DOM 접근
- React component 반환
- 서버 가격 최종 결정
- Router 강결합
