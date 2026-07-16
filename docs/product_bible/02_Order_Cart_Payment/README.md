# ASAK Product Bible Pack 2

## Scope

이 Pack은 고객 주문의 핵심 3개 도메인을 다룬다.

1. Order
2. Cart
3. Payment

각 기능은 다음 관점으로 연결된다.

- Product intent
- UX rule
- Figma screen/state
- React structure
- Zustand/state
- API contract
- Backend responsibility
- DB relation
- Edge case
- QA
- Implementation checklist

## Canonical Flow

Home
→ Menu List
→ Menu Detail
→ Cart
→ Order Create
→ Payment
→ Complete

## Important

- Cart는 아직 주문이 아니다.
- Order는 서버에서 생성된 주문 초안/접수 단위다.
- Payment는 Order와 분리된 상태를 가진다.
- 서버는 가격의 최종 권한을 가진다.
- 결제 실패 시 Cart와 Order draft를 유지한다.
