# Payment Edge Cases and QA

## P0 Edge Cases

### 1. 결제 버튼 연타

- UI disabled
- idempotencyKey
- approved 중복 방지

### 2. 통신 끊김

결제 결과가 불명확할 수 있다.

MVP:

- 실패 처리 전 status 재조회 고려
- 무조건 새 결제 생성 금지

### 3. 승인 성공 후 응답 유실

재시도 시 `PAYMENT_ALREADY_APPROVED` 또는 기존 승인 결과 반환.

### 4. 금액 불일치

서버 승인 금액 기준.
사용자에게 최신 금액 안내.

### 5. 결제수단 비활성화

선택 이후 Admin에서 비활성화된 경우 서버가 차단.

### 6. Processing 중 Timeout

자동 초기화 금지.

### 7. 결제 실패 후 Cart 수정

기존 orderId 폐기 또는 새 Order 생성.
정책을 코드 전에 확정.

---

## Figma QA

- [ ] Collapsed
- [ ] Expanded
- [ ] Loading
- [ ] Processing
- [ ] Failed
- [ ] retry
- [ ] cart return
- [ ] 16,800원
- [ ] disabled method
- [ ] maintenance method

## React QA

- [ ] no duplicate submit
- [ ] processing lock
- [ ] retry state
- [ ] cart preserved
- [ ] history replace after approved
- [ ] error code mapping

## Backend QA

- [ ] order amount verification
- [ ] approved uniqueness
- [ ] idempotency
- [ ] transaction
- [ ] failure log
