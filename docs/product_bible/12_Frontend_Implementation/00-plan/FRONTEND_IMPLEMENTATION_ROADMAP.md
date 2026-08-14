# Frontend Implementation Roadmap

## 1단계 — 기존 코드 동결 및 파악

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

## 2단계 — 기존 코드 재사용 지도

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

## 3단계 — Kiosk 핵심 흐름

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

## 4단계 — 공통 상태

- loading
- empty
- error
- disabled
- processing
- modal
- toast

---

## 5단계 — Admin

- Login
- Dashboard
- Live Order
- Order Management
- Sold-out
- Menu Management
- Payment Settings
- Sales

---

## 6단계 — API 교체

Mock과 API adapter를 분리하고 화면 코드는 최소 변경한다.

---

## 7단계 — 회귀·디자인 QA

기존 팀원 작업이 깨지지 않았는지 먼저 확인한다.
