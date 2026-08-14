# Frontend Architecture

> Status: Current

## 1. 목적

ASAK Frontend는 Kiosk와 Admin을 별도 애플리케이션으로 유지하되, 동일한 설계 원칙을 사용한다.

핵심 목표:

- 화면과 상태를 명확히 분리
- API 교체 가능
- Figma 컴포넌트와 React 컴포넌트 매핑
- 반복 UI 제거
- 구현 중인 scaffold 보호

---

## 2. 실제 저장소 기준 구조

### ASAK-Kiosk

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

### ASAK_Admin

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

## 3. Layer Responsibility

### apps

- App root
- Router composition
- Provider 연결
- Layout 연결

넣지 않는다:

- 비즈니스 계산
- API 세부 로직
- 반복 UI markup

### pages

- Route 단위 화면
- API 호출 orchestration
- 페이지 상태 조합
- Section 구성

넣지 않는다:

- 재사용 가능한 공통 Button/Card 구현
- API URL 직접 문자열
- 복잡한 비즈니스 계산

### components

- 재사용 UI
- 명확한 props
- 화면과 독립된 표현

### features

하나의 기능 단위:

- TTS
- timeout
- cart validation
- sold-out policy
- payment flow

### hooks

- 여러 컴포넌트에서 재사용되는 React 로직
- DOM/event lifecycle
- API state abstraction

### store

- 여러 화면에서 공유되는 client state
- Cart
- Order session
- Accessibility
- TTS settings

### api

- Axios client
- endpoint function
- response unwrap
- error normalization

### contracts

- Figma/API/화면 계약
- 구현 전 scaffold 문서
- 상태·필드 매핑

---

## 4. Dependency Direction

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

## 5. Page Composition

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

## 6. Component Split Rule

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

## 7. Server State와 Client State

### Server State

- Menu
- Order
- Payment
- Sales
- Sold-out

### Client State

- Modal open
- Dropdown
- Form draft
- Accessibility
- Cart
- Timeout countdown

서버 응답을 무조건 Zustand에 복제하지 않는다.

---

## 8. Loading / Empty / Error

모든 서버 데이터 화면은 아래 순서를 고려한다.

```jsx
if (isLoading) return <LoadingState />;
if (error) return <ErrorState />;
if (isEmpty) return <EmptyState />;

return <DefaultView />;
```

Dashboard는 widget별 partialError를 허용한다.

---

## 9. 완료 기준

- [ ] 실제 구조 유지
- [ ] Page와 Component 책임 분리
- [ ] API URL 분리
- [ ] 상태 누락 없음
- [ ] Figma mapping
- [ ] naming 준수
- [ ] build/lint 통과
