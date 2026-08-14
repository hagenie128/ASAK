# Payment Implementation

## Entity

```text
Payment
PaymentMethod
```

## PaymentStatus

```text
READY
APPROVED
FAILED
```

## Endpoint

```http
POST /api/kiosk/payments
```

## Service Flow

1. Order 조회
2. 이미 승인된 Payment 확인
3. PaymentMethod 활성 상태 검증
4. 승인 금액 = Order totalAmount
5. Mock 승인/실패 결정
6. Payment 저장
7. waitingOrderCount 계산
8. response 반환

## 중복 방지

- orderId 기준 승인 Payment unique 검토
- idempotencyKey 저장 검토
- UI isSubmitting과 함께 3중 방어
