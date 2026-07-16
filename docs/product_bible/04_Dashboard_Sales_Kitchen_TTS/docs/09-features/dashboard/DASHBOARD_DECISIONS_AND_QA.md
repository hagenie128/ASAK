# Dashboard Decisions and QA

## 왜 별도 Dashboard인가

실시간 주문 처리와 매장 전체 운영 판단은 목적이 다르다. 주문 보드를 홈으로 사용하면 매출·품절·인기 메뉴를 즉시 파악할 수 없고 Navbar의 Home과 주문관리 역할도 겹친다.

## 왜 KPI는 4개인가

핵심 지표가 많아질수록 판단 속도가 느려진다. Dashboard MVP에서는 순매출, 주문 수, 평균 객단가, 진행 중 주문을 우선한다.

매출 화면에서 사용하는 `고객 수`는 고유 방문자 수가 아니라 `결제 승인 건수`로 정의한다. 따라서 회원 식별 정보가 없어도 구현할 수 있다. 다만 Dashboard에서는 주문 수와 고객 수가 같은 기준이 되므로 두 지표를 동시에 배치해 중복시키지 않는다.

## 왜 Partial Error가 필요한가

Dashboard는 여러 도메인의 데이터를 조합한다. 인기 메뉴 한 건 실패 때문에 전체 화면을 막으면 운영에 불리하다.

## Edge Cases

### 주문 0건
- 매출 0원
- 주문 수 0건
- 객단가 `-`
- 인기 메뉴 Empty

### 품절 0건
- `현재 품절 항목이 없습니다.`

### Polling 중 이전 요청 미완료
- 새 요청 중복 금지

## QA

- [ ] KPI 정의 일치
- [ ] active order count 일치
- [ ] popular menu 수량 일치
- [ ] sold-out count 일치
- [ ] generatedAt 표시
- [ ] Home active
- [ ] partial error
- [ ] 0 value
- [ ] unsupported metric 없음
