# Payment Bible

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `PAYMENT_API_CONTRACT.md`
- `PAYMENT_ARCHITECTURE.md`
- `PAYMENT_EDGE_CASE_AND_QA.md`
- `PAYMENT_FLOW_AND_STATE.md`
- `PAYMENT_WHY.md`

---

## 원문: `PAYMENT_API_CONTRACT.md`

### Payment API Contract

> Status: Draft

#### 1. Start Payment

```http
POST /api/kiosk/payments
```

##### Request

```json
{
  "orderId": 128,
  "paymentMethodCode": "CARD",
  "idempotencyKey": "uuid"
}
```

##### Approved Response

```json
{
  "success": true,
  "data": {
    "paymentId": 900,
    "orderId": 128,
    "orderNo": "1225",
    "paymentStatus": "APPROVED",
    "approvedAmount": 16800,
    "waitingOrderCount": 3,
    "approvedAt": "2026-07-16T03:20:00"
  }
}
```

##### Failed Response

```json
{
  "success": false,
  "message": "PAYMENT_FAILED",
  "data": {
    "orderId": 128,
    "paymentStatus": "FAILED",
    "failureCode": "CARD_DECLINED",
    "canRetry": true
  }
}
```

---

#### 2. Active Payment Methods

```http
GET /api/kiosk/payment-methods
```

##### Response

```json
{
  "success": true,
  "status": 200,
  "code": "KIOSK_PAYMENT_METHOD_LIST_SUCCESS",
  "message": "결제수단 목록 조회 성공",
  "data": {
    "methods": [
      {
        "methodCode": "CARD",
        "methodName": "카드·삼성페이",
        "isEnabled": true,
        "sortOrder": 1
      },
      {
        "methodCode": "KAKAO_PAY",
        "methodName": "카카오페이",
        "isEnabled": false,
        "sortOrder": 2
      },
      {
        "methodCode": "NAVER_PAY",
        "methodName": "네이버페이",
        "isEnabled": false,
        "sortOrder": 3
      }
    ]
  }
}
```

`CARD`는 카드 단말 결제이며 삼성페이를 포함한다. `KAKAO_PAY`, `NAVER_PAY`는 현재
비활성 상태여도 화면에는 표시하고 선택만 막는다.

---

#### 3. Admin Settings

```http
GET /api/admin/payment-methods
PATCH /api/admin/payment-methods/{methodId}
```

##### Fields

```text
isEnabled
sortOrder
methodName
receiptMessage
```

---

#### 4. Error Codes

```text
ORDER_NOT_FOUND
ORDER_AMOUNT_MISMATCH
PAYMENT_METHOD_DISABLED
PAYMENT_ALREADY_APPROVED
PAYMENT_IN_PROGRESS
PAYMENT_FAILED
PAYMENT_TIMEOUT
```

---

## 원문: `PAYMENT_ARCHITECTURE.md`

### Payment Architecture

> Status: Current

#### 1. 목적

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

#### 2. MVP Scope

현재 MVP는 실제 PG가 아니라 가상 결제 흐름을 우선한다.

권장:

- CARD 활성
- 기타 결제수단은 Mock 또는 disabled
- 실제 연동처럼 보이되 `연동 예정` 또는 시연용임을 문서화

---

#### 3. Payment State

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

#### 4. Figma Mapping

##### SCR-007

- Collapsed
- Expanded
- Loading
- Processing

##### SCR-012

- Payment Error
- retry
- cart return

##### SCR-008

- approved result
- orderNo
- waitingOrderCount

---

#### 5. Duplicate Payment Prevention

세 계층에서 막는다.

##### UI

- isSubmitting
- button disabled

##### API

- 동일 orderId에 대한 active payment 확인

##### Backend

- APPROVED payment 존재 시 재승인 금지
- idempotency key 검토

---

#### 6. Failure Recovery

결제 실패 시:

- Cart 유지
- Order draft 유지
- 다른 결제수단 선택 가능
- retry 가능
- 처음부터 주문하지 않음

---

#### 7. Receipt

실물 영수증 출력은 MVP 확장으로 둔다.

현재 완료 화면에서 버튼을 둘 경우:

- mock
- disabled
- demo only

중 하나로 명확히 한다.

장기적으로 SCR-023과 API-019로 분리 가능.

---

#### 8. Payment Method Settings

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

#### 9. Implementation Checklist

- [ ] PaymentStatus
- [ ] READY/APPROVED/FAILED
- [ ] processing UI
- [ ] duplicate prevention
- [ ] retry
- [ ] Cart retention
- [ ] amount consistency
- [ ] method config
- [ ] receipt scope marking

---

## 원문: `PAYMENT_EDGE_CASE_AND_QA.md`

### Payment Edge Cases and QA

#### P0 Edge Cases

##### 1. 결제 버튼 연타

- UI disabled
- idempotencyKey
- approved 중복 방지

##### 2. 통신 끊김

결제 결과가 불명확할 수 있다.

MVP:

- 실패 처리 전 status 재조회 고려
- 무조건 새 결제 생성 금지

##### 3. 승인 성공 후 응답 유실

재시도 시 `PAYMENT_ALREADY_APPROVED` 또는 기존 승인 결과 반환.

##### 4. 금액 불일치

서버 승인 금액 기준.
사용자에게 최신 금액 안내.

##### 5. 결제수단 비활성화

선택 이후 Admin에서 비활성화된 경우 서버가 차단.

##### 6. Processing 중 Timeout

자동 초기화 금지.

##### 7. 결제 실패 후 Cart 수정

기존 orderId 폐기 또는 새 Order 생성.
정책을 코드 전에 확정.

---

#### Figma QA

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

#### React QA

- [ ] no duplicate submit
- [ ] processing lock
- [ ] retry state
- [ ] cart preserved
- [ ] history replace after approved
- [ ] error code mapping

#### Backend QA

- [ ] order amount verification
- [ ] approved uniqueness
- [ ] idempotency
- [ ] transaction
- [ ] failure log

---

## 원문: `PAYMENT_FLOW_AND_STATE.md`

### Payment Flow and State

#### 1. Main Sequence

```text
Order created
→ Payment method selected
→ Payment start
→ Processing
→ Approved or Failed
```

---

#### 2. Approved Flow

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

#### 3. Failed Flow

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

#### 4. Back Navigation

Processing 중 뒤로가기 금지.

Ready 상태에서는 Cart 복귀 가능.

Approved 후 뒤로가기 금지.
CompletePage는 history replace 권장.

---

#### 5. Timeout During Payment

##### READY

일반 timeout 적용 가능.

##### PROCESSING

timeout reset 금지.

사용자 session을 유지하고 결과를 기다린다.

##### FAILED

retry 화면에서 warning 가능.

---

#### 6. Amount Rule

모든 화면:

```text
16,800원
```

현재 수정 대상:

- Payment Error 17,100원
- Timeout 17,100원

---

#### 7. Method Availability

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

---

## 원문: `PAYMENT_WHY.md`

### Why Payment Is Designed This Way

#### 왜 Order와 Payment 상태를 분리하는가

주문은 존재하지만 결제는 실패할 수 있다.

두 상태를 하나로 합치면:

- 재결제 처리
- 실패 이력
- 매출 집계
- 관리자 조회

가 복잡해진다.

---

#### 왜 결제 실패 시 Cart를 유지하는가

고객이 옵션이 많은 샐러드 주문을 다시 구성하는 비용이 크기 때문이다.

실패는 시스템 문제일 수 있으므로 고객에게 다시 입력을 요구하지 않는다.

---

#### 왜 서버가 금액을 다시 계산하는가

클라이언트 값은 변조되거나 오래될 수 있다.

가격·품절·옵션 정책은 서버가 최종 결정한다.

---

#### 왜 Processing 중 타임아웃을 막는가

결제 결과가 처리 중일 때 session을 초기화하면:

- 승인 여부를 잃을 수 있다.
- 중복 결제가 발생할 수 있다.
- 고객과 매장 데이터가 불일치할 수 있다.

---

#### 왜 영수증을 확장 기능으로 두는가

실물 프린터 연동은 브라우저 UI만으로 끝나지 않는다.

- 장치
- 드라이버
- 출력 실패
- 재출력
- 용지 없음

정책이 필요하므로 MVP와 분리한다.
