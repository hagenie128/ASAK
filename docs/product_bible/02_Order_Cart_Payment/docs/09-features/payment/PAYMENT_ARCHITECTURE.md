# Payment Architecture

> Status: Current

## 1. 목적

Payment 도메인은 생성된 Order에 대해 결제 시도를 관리하고 승인·실패 결과를 기록한다.

Payment는 Order와 분리된 상태를 가진다.

```text
OrderStatus != PaymentStatus
```

예:

```text
Order RECEIVED
Payment FAILED
```

---

## 2. MVP Scope

현재 MVP는 실제 PG가 아니라 가상 결제 흐름을 우선한다.

권장:

- CARD 활성
- 기타 결제수단은 Mock 또는 disabled
- 실제 연동처럼 보이되 `연동 예정` 또는 시연용임을 문서화

---

## 3. Payment State

```text
READY
  ↓ start
PROCESSING
  ↓ success
APPROVED

PROCESSING
  ↓ fail
FAILED
```

`PROCESSING`은 UI state로 사용하고 DB enum 포함 여부는 선택 가능하다.

---

## 4. Figma Mapping

### SCR-007

- Collapsed
- Expanded
- Loading
- Processing

### SCR-012

- Payment Error
- retry
- cart return

### SCR-008

- approved result
- orderNo
- waitingOrderCount

---

## 5. Duplicate Payment Prevention

세 계층에서 막는다.

### UI

- isSubmitting
- button disabled

### API

- 동일 orderId에 대한 active payment 확인

### Backend

- APPROVED payment 존재 시 재승인 금지
- idempotency key 검토

---

## 6. Failure Recovery

결제 실패 시:

- Cart 유지
- Order draft 유지
- 다른 결제수단 선택 가능
- retry 가능
- 처음부터 주문하지 않음

---

## 7. Receipt

실물 영수증 출력은 MVP 확장으로 둔다.

현재 완료 화면에서 버튼을 둘 경우:

- mock
- disabled
- demo only

중 하나로 명확히 한다.

장기적으로 SCR-023과 API-019로 분리 가능.

---

## 8. Payment Method Settings

Admin SCR-018에서 관리:

- enabled
- disabled
- maintenance
- sortOrder
- kiosk visibility
- failure retention policy
- receipt message

Kiosk는 활성 결제수단만 조회한다.

---

## 9. Implementation Checklist

- [ ] PaymentStatus
- [ ] READY/APPROVED/FAILED
- [ ] processing UI
- [ ] duplicate prevention
- [ ] retry
- [ ] Cart retention
- [ ] amount consistency
- [ ] method config
- [ ] receipt scope marking
