# ADR-002: 주문 완료 화면에 대기 주문 수를 표시한다

- Status: Accepted
- Date: 2026-07-16

## Context

주문 완료 후 고객에게 준비 상황을 안내해야 한다.

## Options

### A. 예상 조리시간

문제:
- 메뉴별 조리 난이도 차이
- 매장 인력과 혼잡도 반영 어려움
- 오차가 발생하면 신뢰 저하

### B. 대기 주문 수

장점:
- 데이터 계산이 단순하다.
- 혼잡도를 직관적으로 보여준다.
- 시간 약속을 하지 않는다.

## Decision

`waitingOrderCount`를 사용한다.

## API Contract Draft

```json
{
  "orderNo": "1225",
  "paymentStatus": "APPROVED",
  "waitingOrderCount": 3
}
```

## UI Copy

- 주문이 접수되었습니다.
- 현재 대기 주문 3건
- 맛있게 준비하고 있습니다.

## Consequences

- 결제 승인 또는 주문 완료 응답에 필드 추가
- SCR-008 수정
- Mock data와 API fixture 수정
