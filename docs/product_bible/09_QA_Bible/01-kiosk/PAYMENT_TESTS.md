# Payment Tests

## PAY-001 — 승인 성공

Priority: P0

Expected:

- PaymentStatus APPROVED
- Complete 이동
- orderNo 표시
- waitingOrderCount 표시

## PAY-002 — 버튼 연타

Priority: P0

Expected:

- 결제 요청 1회
- 중복 승인 없음

## PAY-003 — 실패 후 재시도

Expected:

- Cart/Order 유지
- 재결제 가능

## PAY-004 — 다른 수단 선택

Expected:

- enabled method만 선택

## PAY-005 — maintenance 수단

Expected:

- disabled + 점검 중

## PAY-006 — Processing 중 Timeout

Priority: P0

Expected:

- timeout 미적용
- session 유지

## PAY-007 — 승인 후 응답 유실

Expected:

- 재조회 또는 idempotent 결과
- 중복 결제 금지

## PAY-008 — 금액 정합성

Expected:

- Cart, Payment, Error, Timeout, Complete 모두 16,800원
