# Foundation Decisions

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `DECISION_LOG.md`
- `ADR-001-DASHBOARD.md`
- `ADR-002-WAITING-ORDER-COUNT.md`

---

## 원문: `DECISION_LOG.md`

### ASAK Product Decision Log

> Status: Current

#### 2026-07-16 — Pretendard Variable 채택

##### 결정

Premium Figma와 React 공식 폰트를 Pretendard Variable로 사용한다.

##### 이유

- 한글·숫자 균형이 좋다.
- 관리자 KPI와 테이블 가독성이 좋다.
- Apple 계열의 정돈된 인상과 어울린다.
- 웹 적용이 간단하다.

##### 영향

- Foundations
- Figma Text Styles
- CSS font-family
- React Design Tokens

---

#### 2026-07-16 — Apple + Salady 방향

##### 결정

Apple의 절제와 샐러디의 친근하고 신선한 이미지를 결합한다.

##### 이유

- 과도한 장식 없이 제품 완성도를 높일 수 있다.
- 음식 이미지와 데이터에 집중할 수 있다.
- 키오스크와 관리자 화면의 성격 차이를 유지할 수 있다.

##### 금지

- 라임 glow
- 과도한 3D 채소
- 모든 요소 초록 강조

---

#### 2026-07-16 — Admin Dashboard 추가

##### 결정

로그인 직후 주문 목록이 아닌 SCR-022 Dashboard를 제공한다.

##### 이유

관리자는 주문뿐 아니라 매출, 품절, 인기 메뉴, 진행 중 주문을 동시에 판단해야 한다.

##### 영향

- Admin route `/`
- Navbar Home
- Dashboard Page
- Dashboard aggregate API 또는 API 조합
- PrototypeMap

---

#### 2026-07-16 — 예상 조리시간 대신 대기 주문 수

##### 결정

주문 완료 화면에서 예상 조리시간 대신 `waitingOrderCount`를 표시한다.

##### 이유

예상시간은 오차가 크고 신뢰를 떨어뜨릴 수 있다. 대기 주문 수는 계산이 단순하고 고객이 혼잡도를 직접 판단할 수 있다.

##### 영향

- Payment/Order response
- Complete Page
- Figma SCR-008
- API UI Contract

---

#### 2026-07-16 — TTS 주문 완료 호출

##### 결정

관리자가 주문을 COMPLETED로 변경한 후 Admin 브라우저에서 TTS를 실행한다.

##### 이유

- 직원 반복 호출 감소
- 실제 운영 흐름 표현
- 별도 음성 서버 없이 구현 가능

##### 정책

- 서버 성공 후 호출
- 10초 중복 방지
- queue 방식
- mute 지원
- 실패해도 주문 상태 유지

---

#### 2026-07-16 — 저장소 역할 유지

##### 결정

별도 문서 저장소를 만들지 않고 ASAK Root Repository가 Product Bible을 관리한다.

##### 이유

이미 ASAK가 문서·설정·데이터·운영 허브 역할을 수행한다.

---

#### 2026-07-16 — Spring Boot 4.1.0 / Java 25 유지

##### 결정

프로젝트 시작 시 확정된 환경을 유지한다.

##### 이유

- 팀 환경이 이미 해당 버전으로 설정됨
- 현재 scaffold 단계에서 버전 변경 이점 없음
- 변경 시 검증 비용만 증가

##### 금지

AI가 일반적인 안정성 이유만으로 다운그레이드를 제안하지 않는다.

---

## 원문: `ADR-001-DASHBOARD.md`

### ADR-001: Admin Dashboard를 별도 홈으로 둔다

- Status: Accepted
- Date: 2026-07-16

#### Context

기존 Admin 구조는 주문 현황을 첫 화면으로 사용했다. 그러나 관리자 역할은 실시간 주문 처리뿐 아니라 매출, 품절, 인기 메뉴, 운영 이상을 함께 판단하는 것이다.

#### Options

##### A. 주문 목록을 홈으로 유지

장점:
- 구현이 단순하다.
- 기존 구조를 유지한다.

단점:
- 매장 전체 상태를 파악하기 어렵다.
- Navbar Home과 주문관리 역할이 겹친다.

##### B. Dashboard를 별도 홈으로 추가

장점:
- 운영 상태를 한 화면에서 확인한다.
- 실시간 주문 보드와 주문 관리의 역할을 분리한다.
- 포트폴리오 제품 완성도가 높아진다.

단점:
- 신규 화면과 데이터 집계가 필요하다.

#### Decision

B를 채택한다.

#### Dashboard Minimum Data

- 오늘 매출
- 주문 수
- 평균 객단가
- 진행 중 주문
- 실시간 주문 요약
- 품절
- 인기 메뉴

#### Consequences

- SCR-022 추가
- `/` route는 Dashboard
- 주문관리는 별도 route
- 로그인 성공 후 Dashboard 이동
- Dashboard API 또는 기존 API 조합 필요

---

## 원문: `ADR-002-WAITING-ORDER-COUNT.md`

### ADR-002: 주문 완료 화면에 대기 주문 수를 표시한다

- Status: Accepted
- Date: 2026-07-16

#### Context

주문 완료 후 고객에게 준비 상황을 안내해야 한다.

#### Options

##### A. 예상 조리시간

문제:
- 메뉴별 조리 난이도 차이
- 매장 인력과 혼잡도 반영 어려움
- 오차가 발생하면 신뢰 저하

##### B. 대기 주문 수

장점:
- 데이터 계산이 단순하다.
- 혼잡도를 직관적으로 보여준다.
- 시간 약속을 하지 않는다.

#### Decision

`waitingOrderCount`를 사용한다.

#### API Contract Draft

```json
{
  "orderNo": "1225",
  "paymentStatus": "APPROVED",
  "waitingOrderCount": 3
}
```

#### UI Copy

- 주문이 접수되었습니다.
- 현재 대기 주문 3건
- 맛있게 준비하고 있습니다.

#### Consequences

- 결제 승인 또는 주문 완료 응답에 필드 추가
- SCR-008 수정
- Mock data와 API fixture 수정
