# ASAK Product Decision Log

> Status: Current

## 2026-07-16 — Pretendard Variable 채택

### 결정

Premium Figma와 React 공식 폰트를 Pretendard Variable로 사용한다.

### 이유

- 한글·숫자 균형이 좋다.
- 관리자 KPI와 테이블 가독성이 좋다.
- Apple 계열의 정돈된 인상과 어울린다.
- 웹 적용이 간단하다.

### 영향

- Foundations
- Figma Text Styles
- CSS font-family
- React Design Tokens

---

## 2026-07-16 — Apple + Salady 방향

### 결정

Apple의 절제와 샐러디의 친근하고 신선한 이미지를 결합한다.

### 이유

- 과도한 장식 없이 제품 완성도를 높일 수 있다.
- 음식 이미지와 데이터에 집중할 수 있다.
- 키오스크와 관리자 화면의 성격 차이를 유지할 수 있다.

### 금지

- 라임 glow
- 과도한 3D 채소
- 모든 요소 초록 강조

---

## 2026-07-16 — Admin Dashboard 추가

### 결정

로그인 직후 주문 목록이 아닌 SCR-022 Dashboard를 제공한다.

### 이유

관리자는 주문뿐 아니라 매출, 품절, 인기 메뉴, 진행 중 주문을 동시에 판단해야 한다.

### 영향

- Admin route `/`
- Navbar Home
- Dashboard Page
- Dashboard aggregate API 또는 API 조합
- PrototypeMap

---

## 2026-07-16 — 예상 조리시간 대신 대기 주문 수

### 결정

주문 완료 화면에서 예상 조리시간 대신 `waitingOrderCount`를 표시한다.

### 이유

예상시간은 오차가 크고 신뢰를 떨어뜨릴 수 있다. 대기 주문 수는 계산이 단순하고 고객이 혼잡도를 직접 판단할 수 있다.

### 영향

- Payment/Order response
- Complete Page
- Figma SCR-008
- API UI Contract

---

## 2026-07-16 — TTS 주문 완료 호출

### 결정

관리자가 주문을 COMPLETED로 변경한 후 Admin 브라우저에서 TTS를 실행한다.

### 이유

- 직원 반복 호출 감소
- 실제 운영 흐름 표현
- 별도 음성 서버 없이 구현 가능

### 정책

- 서버 성공 후 호출
- 10초 중복 방지
- queue 방식
- mute 지원
- 실패해도 주문 상태 유지

---

## 2026-07-16 — 저장소 역할 유지

### 결정

별도 문서 저장소를 만들지 않고 ASAK Root Repository가 Product Bible을 관리한다.

### 이유

이미 ASAK가 문서·설정·데이터·운영 허브 역할을 수행한다.

---

## 2026-07-16 — Spring Boot 4.1.0 / Java 25 유지

### 결정

프로젝트 시작 시 확정된 환경을 유지한다.

### 이유

- 팀 환경이 이미 해당 버전으로 설정됨
- 현재 scaffold 단계에서 버전 변경 이점 없음
- 변경 시 검증 비용만 증가

### 금지

AI가 일반적인 안정성 이유만으로 다운그레이드를 제안하지 않는다.
