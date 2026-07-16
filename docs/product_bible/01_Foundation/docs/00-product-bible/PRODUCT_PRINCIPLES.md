# ASAK Product Principles

> Status: Current

## 1. Product Before Decoration

화면을 화려하게 만드는 것보다 사용자가 행동을 완료하게 만드는 것이 우선이다.

판단 순서:

1. 사용자 목적
2. 정보 우선순위
3. 오류·복구
4. 데이터 정합성
5. 컴포넌트 재사용
6. 시각적 완성도
7. 모션과 장식

---

## 2. One Screen, One Decision

각 화면은 사용자가 내려야 하는 하나의 결정에 집중한다.

| Screen | Main Decision |
|---|---|
| Home | 어디에서 먹을 것인가 |
| Menu List | 어떤 메뉴를 고를 것인가 |
| Menu Detail | 어떻게 구성할 것인가 |
| Cart | 이 주문으로 결제할 것인가 |
| Payment | 어떤 방식으로 결제할 것인가 |
| Complete | 주문이 정상 접수되었는가 |
| Dashboard | 지금 매장 상태는 어떤가 |
| Order Board | 어떤 주문을 먼저 처리할 것인가 |
| Sales | 매장 성과가 어떻게 변했는가 |

---

## 3. State Is Part of the Product

Default 화면만 디자인된 기능은 완료된 기능이 아니다.

주요 화면은 필요에 따라 다음 상태를 가진다.

- default
- loading
- empty
- error
- disabled
- selected
- processing
- success
- validationError

---

## 4. Recovery Over Blame

오류 메시지는 사용자의 잘못을 지적하지 않는다.

잘못된 예:

- 잘못 입력했습니다.
- 선택이 틀렸습니다.

권장:

- 필수 옵션을 선택해주세요.
- 결제가 완료되지 않았어요. 다시 시도하거나 다른 결제수단을 선택해주세요.

---

## 5. Server Is the Price Authority

클라이언트가 전달한 금액은 신뢰하지 않는다.

- 화면은 예상 금액을 계산한다.
- 서버는 메뉴·옵션 가격을 다시 계산한다.
- 불일치 시 결제를 진행하지 않는다.
- 사용자에게 변경된 금액을 명확히 안내한다.

---

## 6. Green Is an Accent

브랜드 초록은 다음에만 사용한다.

- 주요 CTA
- 선택 상태
- 성공 상태
- 핵심 그래프 강조
- 활성 Navigation

사용하지 않는다.

- 모든 KPI 숫자
- 삭제·취소
- 모든 카드 배경
- 라임 glow
- 의미 없는 장식

---

## 7. Food and Data Are the Heroes

Kiosk에서는 음식이 주인공이다.

Admin에서는 데이터가 주인공이다.

UI는 음식과 데이터의 해석을 돕는 역할만 한다.

---

## 8. Design Must Survive Implementation

Figma에서만 가능한 표현은 지양한다.

모든 디자인은 다음 질문을 통과해야 한다.

- React 컴포넌트로 분리 가능한가?
- 상태를 props로 표현 가능한가?
- API 응답으로 채울 수 있는가?
- 데이터가 길어져도 깨지지 않는가?
- 모바일이 아니라 고정 Kiosk/Admin 캔버스에서 안정적인가?

---

## 9. No Hidden Business Logic

정책은 UI 안에 암묵적으로 숨기지 않는다.

예:

- 품절 전파
- 타임아웃
- 결제 실패 시 장바구니 유지
- TTS 중복 호출
- 매출 비교 기준
- 취소·환불 상태 전이

모든 정책은 Feature 문서와 상태 계약에 기록한다.

---

## 10. Scope Discipline

MVP와 확장 기능을 구분한다.

확장 기능을 화면에 보여줄 경우:

- Mock
- 연결 예정
- 비활성
- 확장 설계

중 하나임을 명확히 한다.

실제 API가 없는 기능을 완성된 기능처럼 표현하지 않는다.
