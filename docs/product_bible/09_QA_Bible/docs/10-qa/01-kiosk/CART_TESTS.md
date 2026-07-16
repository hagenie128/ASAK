# Cart Tests

## CART-001 — 동일 메뉴 동일 옵션

Expected:

- 정책에 따라 quantity 증가
- 중복 item 생성 여부 일관

## CART-002 — 동일 메뉴 다른 옵션

Expected:

- 별도 cartItemId

## CART-003 — 수량 증가

Expected:

- lineAmount와 totalAmount 갱신

## CART-004 — 수량 1에서 감소

Expected:

- minus disabled
- 자동 삭제 금지

## CART-005 — 옵션 수정

Expected:

- 기존 선택 preload
- 저장 전 original 불변
- 저장 후 해당 cartItemId만 갱신

## CART-006 — 삭제 취소

Expected:

- item 유지

## CART-007 — 마지막 항목 삭제

Expected:

- Empty state
- total 0

## CART-008 — 품절 검증 실패

Expected:

- 문제 item 강조
- 수정/삭제 제공

## CART-009 — 결제 실패 복귀

Expected:

- Cart 유지
