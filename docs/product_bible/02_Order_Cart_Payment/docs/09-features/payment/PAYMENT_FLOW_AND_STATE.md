# Payment Flow and State

## 1. Main Sequence

```text
Order created
→ Payment method selected
→ Payment start
→ Processing
→ Approved or Failed
```

---

## 2. Approved Flow

```text
PaymentPage
→ POST payment
→ Backend verifies order
→ Backend verifies amount
→ payment APPROVED
→ response orderNo/waitingOrderCount
→ CompletePage
→ auto return
→ reset session
```

---

## 3. Failed Flow

```text
PaymentPage
→ POST payment
→ FAILED
→ Payment Error
→ retry or cart
```

실패 시:

- orderId 유지
- cart 유지
- selected payment method는 정책에 따라 유지/초기화

---

## 4. Back Navigation

Processing 중 뒤로가기 금지.

Ready 상태에서는 Cart 복귀 가능.

Approved 후 뒤로가기 금지.
CompletePage는 history replace 권장.

---

## 5. Timeout During Payment

### READY

일반 timeout 적용 가능.

### PROCESSING

timeout reset 금지.

사용자 session을 유지하고 결과를 기다린다.

### FAILED

retry 화면에서 warning 가능.

---

## 6. Amount Rule

모든 화면:

```text
16,800원
```

현재 수정 대상:

- Payment Error 17,100원
- Timeout 17,100원

---

## 7. Method Availability

Admin config:

```text
ENABLED
DISABLED
MAINTENANCE
```

Kiosk UI:

- ENABLED: selectable
- DISABLED: hidden 또는 disabled
- MAINTENANCE: disabled + 점검 중
