# Frontend Plan and Audit

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `FRONTEND_IMPLEMENTATION_ROADMAP.md`
- `FRONTEND_PRIORITY_MATRIX.md`
- `EXISTING_CODE_AUDIT.md`
- `REUSE_DECISION_GUIDE.md`

---

## 원문: `FRONTEND_IMPLEMENTATION_ROADMAP.md`

### Frontend Implementation Roadmap

#### 1단계 — 기존 코드 동결 및 파악

- 현재 branch 확인
- build 확인
- route 목록
- Page 목록
- Component 목록
- Zustand store
- Mock Data
- API module
- CSS/token
- Figma mapping

완료 조건:

- 기존 앱이 정상 실행
- 현재 동작 화면 캡처
- 삭제 없이 Inventory 작성

---

#### 2단계 — 기존 코드 재사용 지도

각 화면별:

```text
이미 있음
부분 구현
Mock 연결
API 연결 필요
신규 필요
```

로 분류한다.

---

#### 3단계 — Kiosk 핵심 흐름

```text
Home
→ Menu List
→ Menu Detail
→ Cart
→ Payment
→ Complete
```

기존 UI를 유지하고 state/API를 연결한다.

---

#### 4단계 — 공통 상태

- loading
- empty
- error
- disabled
- processing
- modal
- toast

---

#### 5단계 — Admin

- Login
- Dashboard
- Live Order
- Order Management
- Sold-out
- Menu Management
- Payment Settings
- Sales

---

#### 6단계 — API 교체

Mock과 API adapter를 분리하고 화면 코드는 최소 변경한다.

---

#### 7단계 — 회귀·디자인 QA

기존 팀원 작업이 깨지지 않았는지 먼저 확인한다.

---

## 원문: `FRONTEND_PRIORITY_MATRIX.md`

### Frontend Priority Matrix

#### P0

- 기존 Kiosk 실행 유지
- 주문 유형
- 메뉴 목록
- 메뉴 상세
- Cart
- Payment
- Complete
- 금액 정합성
- Error recovery

#### P1

- Dashboard
- Live Order
- Sold-out
- Menu Management
- Sales

#### P2

- 고급 접근성
- 영수증
- 멤버십
- 고급 차트
- WebSocket

#### 원칙

문서에 있다고 전부 구현하지 않는다.

---

## 원문: `EXISTING_CODE_AUDIT.md`

### Existing Code Audit

#### 목적

기존 팀원이 작성한 코드를 보호하고 중복 구현을 막는다.

#### 조사 대상

```text
src/apps
src/pages
src/components
src/features
src/hooks
src/store
src/api
src/constants
src/mocks
src/styles
src/router
```

#### 기록 양식

| Item | Existing Path | Status | Reuse | Change |
|---|---|---|---|---|
| MenuCard | ... | implemented | yes | props only |
| CartPage | ... | partial | yes | API/state |
| BottomCTA | ... | implemented | yes | loading state |

#### 금지

- 기존 코드를 확인하지 않고 새 Page 생성
- 이름이 다르다는 이유로 중복 Component 생성
- 전체 폴더 이동
- 기존 스타일 제거

---

## 원문: `REUSE_DECISION_GUIDE.md`

### Reuse Decision Guide

#### 그대로 사용

- UI와 책임이 현재 요구와 일치
- props 추가 없이 사용 가능

#### 확장

- 역할은 같음
- state/props만 부족
- variant 추가로 해결 가능

#### Wrapper

- 기존 컴포넌트를 수정하면 영향이 큼
- 화면별 조합만 다름

#### 신규 생성

- 기존에 같은 역할 없음
- 책임이 명확히 다름
- 재사용 가능성 있음

#### 삭제·교체

최후 수단.
변경 이유와 영향도를 먼저 기록한다.
