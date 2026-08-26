# 토스 Payment 객체 기반 결제·환불 이력 데이터 모델 제안

> 작성일: 2026-08-26
> 상태: **설계 제안 — DB migration 적용 완료, API·실제 PG 연동·통합 검증 미완료**
> 기준: 토스 Payment/결제 취소 API에서 제공하는 `Payment` 객체와 `cancels[]` 취소 이력

## 1. 결론

환불 사유와 환불 정보를 `payment` 한 행의 `refunded_at`·상태만으로 관리하면, 환불을 누가·언제·얼마나·어떤 PG 거래 키로 처리했는지 남길 수 없다. 부분 취소 또는 재시도까지 고려하면 `payment`와 별도로 **`payment_refund` 이력 테이블**이 필요하다.

토스의 `Payment.cancels[]` 배열은 결제 한 건에 취소가 여러 건 연결되는 구조다. ASAK도 같은 관계로 모델링한다.

```text
orders 1 ── 0..N payment 1 ── 0..N payment_refund
                         └── 0..1 payment_receipt (선택)
```

- `payment`: 승인된 원 결제와 현재 잔액을 보관한다.
- `payment_refund`: 전액/부분 환불 각각의 요청·PG 결과·금액·사유를 보관한다.
- `payment_receipt`: 매출전표·현금영수증을 실제로 조회/관리할 때만 별도 도입한다. v1 필수 테이블은 아니다.

## 2. 현재 확인된 ASAK 상태

문서상 현재 `payment`에는 `id`, `order_id`, `method_id`, `status_id`, `amount`, `paid_at`, `refunded_at`, `idempotency_key`가 있다. 승인 시각과 최종 환불 시각은 남길 수 있지만, 환불 사유·환불 거래 키·여러 환불 이력·PG 상태를 충분히 보관하지 못한다.

현재 프로젝트의 확정 정책은 다음과 같다.

- 주문 상태는 환불 후 `CANCELED`, 결제 상태는 `REFUNDED`를 사용한다.
- 환불 API는 클라이언트가 금액/결제상태를 보내지 않고 `refundReason`만 보낸다.
- 실제 토스 연동은 아직 범위 밖이며, 가상 카드 승인/환불 흐름도 통합 검증 전이다.

따라서 아래 구조는 현재 스키마를 수정했다는 뜻이 아니라, 팀 논의 후 migration으로 구현할 후보안이다.

## 3. `payment`에 보관할 원 결제 정보

기존 금액·상태·시각은 유지하고, 실제 PG 연동 시 아래 필드를 추가 후보로 둔다.

| 필드 | 용도 | 토스 Payment 대응 | 비고 |
|---|---|---|---|
| `provider` | 결제 제공자 | 토스/가상카드 등 | 예: `TOSS`, `VIRTUAL_CARD` |
| `provider_payment_key` | PG 결제 식별자 | `paymentKey` | 결제 취소/조회에 필요, 제공자별 UNIQUE |
| `provider_order_id` | PG에 보낸 주문번호 | `orderId` | 내부 `orders.id`와 구분 |
| `provider_status` | PG 원본 상태 | `DONE`, `CANCELED` 등 | 내부 `status_id`와 별도로 보관 |
| `currency` | 통화 | `currency` | 초기값은 `KRW` |
| `original_amount` | 최초 승인 금액 | `totalAmount` | 환불 뒤에도 변하지 않음 |
| `remaining_amount` | 현재 환불 가능 잔액 | `balanceAmount` | 환불 완료 뒤 0 또는 부분 잔액 |
| `approved_at` | PG 승인 시각 | `approvedAt` | 기존 `paid_at`와 의미를 통일한 뒤 하나만 사용 여부 결정 |
| `last_provider_transaction_key` | 마지막 승인/취소 거래 키 | `lastTransactionKey` | 마지막 PG 거래 추적용 |
| `receipt_url` | 매출전표/결제 영수증 URL | `receipt.url` | URL은 바뀔 수 있어 조회 시 재확인 가능 |

카드 승인번호·발급사 코드는 관리자 화면에 꼭 필요할 때만 최소 저장한다. 카드번호, 가상계좌번호, 환불계좌번호, 웹훅 `secret`, PG 인증 헤더/시크릿 키는 저장하거나 로그에 남기지 않는다.

## 4. 필수 제안: `payment_refund` 이력 테이블

한 결제의 전액 취소와 부분 취소를 모두 기록하는 테이블이다. 토스의 `cancels[]` 배열의 한 원소가 ASAK의 한 행에 대응한다.

| 필드 | 제약/예시 | 목적 |
|---|---|---|
| `id` | PK | 환불 이력 식별자 |
| `payment_id` | FK → `payment.id`, NOT NULL | 어느 원 결제의 환불인지 연결 |
| `refund_type` | `FULL` / `PARTIAL` | 전액·부분 환불 구분 |
| `request_amount` | NOT NULL | PG에 요청한 환불 금액 |
| `refunded_amount` | NULL 가능 | PG가 실제 취소 완료한 금액 |
| `remaining_amount` | NULL 가능 | 취소 후 PG 기준 환불 가능 잔액 |
| `refund_reason` | VARCHAR(200), NOT NULL | 관리자 입력 환불 사유; 토스 `cancelReason`에 매핑 |
| `status` | `REQUESTED`, `SUCCEEDED`, `FAILED` | ASAK 환불 처리 상태 |
| `provider_cancel_transaction_key` | NULL, UNIQUE | 토스 `cancels[].transactionKey` |
| `provider_cancel_status` | NULL | 토스 `cancels[].cancelStatus` |
| `provider_request_id` | NULL, UNIQUE 후보 | 토스 `cancelRequestId`; 비동기 결제에만 사용 가능 |
| `failure_code` / `failure_message` | NULL | 실패 원인 기록. 사용자 메시지와 PG 원문은 분리 |
| `requested_by_type` / `requested_by_id` | NULL 가능 | 관리자/시스템 등 요청 주체 추적 |
| `requested_at` | NOT NULL | 환불을 요청한 시각 |
| `completed_at` | NULL 가능 | PG 취소 성공 시각 (`canceledAt`) |
| `created_at` / `updated_at` | NOT NULL | 감사 추적 |

권장 인덱스와 제약은 다음과 같다.

- `INDEX (payment_id, created_at DESC)`: 주문 상세에서 환불 이력 조회
- `UNIQUE (provider, provider_payment_key)`: 동일 PG 결제의 중복 저장 방지 (`payment`)
- `UNIQUE (provider_cancel_transaction_key)`: 동일 PG 취소 거래 중복 기록 방지
- `CHECK (request_amount > 0)` 및 `CHECK (refunded_amount IS NULL OR refunded_amount > 0)`
- 전액 환불만 지원하는 v1이라도 `payment_refund`은 만든다. 이후 부분 환불을 추가할 때 기존 한 행을 덮어쓰지 않는다.

## 5. 상태와 금액 규칙

| 구분 | ASAK 내부 상태 | 토스 원본 상태 예시 | 저장 원칙 |
|---|---|---|---|
| 승인 대기 | `READY` | `READY`, `IN_PROGRESS` | 내부/PG 상태를 혼동하지 않음 |
| 승인 완료 | `APPROVED` | `DONE` | 원 금액과 승인 시각 고정 |
| 전액 환불 완료 | `REFUNDED` | `CANCELED` | `remaining_amount = 0`, 성공 이력 1건 이상 |
| 부분 환불 완료 | 정책 결정 필요 | `PARTIAL_CANCELED` | 내부 `PARTIALLY_REFUNDED` 도입 여부는 팀 결정 후 진행 |
| 환불 요청 실패 | 기존 결제는 `APPROVED` 유지 | 오류 응답 | `payment_refund.status = FAILED` 이력만 추가 |

`payment.amount`의 의미는 현재 계약상 `approvedAmount`다. 토스의 `totalAmount`처럼 최초 승인 금액으로 유지할지, `original_amount`를 별도 두고 `amount`를 유지할지는 migration 전에 하나로 결정해야 한다. 본 제안은 조회 혼동을 막기 위해 `original_amount`와 `remaining_amount`를 명시하는 쪽을 권장한다.

## 6. 환불 처리 데이터 흐름

```text
Admin: PATCH /api/admin/orders/{orderId}/refund
body: { "refundReason": "고객 요청" }
        │
        ▼
Server: orderId로 payment를 재조회
        - 내부 상태 APPROVED인지
        - provider_payment_key가 있는지
        - remaining_amount와 환불 정책이 맞는지
        │
        ▼
PG: POST /v1/payments/{paymentKey}/cancel
body: { "cancelReason": "고객 요청" }
        │ 성공
        ▼
DB @Transactional:
  1. payment_refund 성공 이력 INSERT
  2. payment 상태/remaining_amount/refunded_at 갱신
  3. orders 상태/canceled_at 갱신
  4. 각 UPDATE가 정확히 1건인지 확인
        │
        ▼
Admin: DB에서 재조회한 결제·환불 요약 응답
```

PG 취소는 DB 트랜잭션 **밖**에서 먼저 호출한다. PG는 성공했는데 DB 갱신이 실패하면 PG 취소를 되돌릴 수 없으므로, 제공자 결제 키·주문 ID·PG 취소 거래 키·예외를 구조화 로그로 남기고 수동 확인한다. 자동 보상/재시도는 별도 범위다.

## 7. 영수증·현금영수증 범위

토스 `receipt.url`은 결제 한 건의 매출전표 URL이므로, v1에서는 `payment.receipt_url` 하나로 충분하다. 아래 기능이 실제 요구되면 별도 테이블을 추가한다.

- 현금영수증 발행/취소 이력 여러 건 조회: `payment_cash_receipt`
- 가상계좌 환불계좌 정보: 저장 최소화가 원칙이며, 필요한 경우 암호화·접근권한·보존기간이 먼저 확정되어야 함
- PG 원본 응답 보관: 필요한 필드만 정규화하고, 전체 JSON을 저장한다면 마스킹·접근제어·보존기간 정책이 필요함

## 8. 제공 DDL 기반 migration 초안 (미실행)

아래는 팀에서 제공한 SQL을 문서화한 것이다. 아직 실제 DB의 인덱스명·FK·기존 환불 행 수를 확인하지 않았으므로 **그대로 실행하지 않는다.** 특히 MySQL DDL은 일반적으로 자동 커밋되므로, 실행 전 백업과 단계별 검증이 필요하다.

### 8.1 정방향 적용 순서

```sql
-- 1) 주문 1건당 여러 payment 시도를 허용하도록 조회 인덱스 유지
CREATE INDEX idx_payment_order_id
ON payment(order_id);

-- 주의: 실제 UNIQUE 인덱스명이 order_id인지 SHOW CREATE TABLE로 먼저 확인한다.
ALTER TABLE payment
DROP INDEX order_id;

-- 2) 결제 Provider 추가
ALTER TABLE payment
    ADD COLUMN provider VARCHAR(30)
        COLLATE utf8mb4_unicode_ci
        DEFAULT NULL
        AFTER idempotency_key;

-- 3) 환불 이력 테이블 생성: payment 1 : N payment_refund
CREATE TABLE payment_refund (
    id BIGINT NOT NULL AUTO_INCREMENT,
    payment_id BIGINT NOT NULL,
    amount INT NOT NULL DEFAULT 0,
    reason VARCHAR(255)
        COLLATE utf8mb4_unicode_ci
        DEFAULT NULL,
    provider_cancel_transaction_key VARCHAR(200)
        COLLATE utf8mb4_unicode_ci
        DEFAULT NULL,
    refunded_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_payment_refund_provider_cancel_transaction_key
        (provider_cancel_transaction_key),
    KEY idx_payment_refund_payment_id
        (payment_id),
    CONSTRAINT fk_payment_refund_payment
        FOREIGN KEY (payment_id)
        REFERENCES payment(id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- 4) 기존 전액 환불 행을 이력으로 백필
INSERT INTO payment_refund (
    payment_id,
    amount,
    reason,
    provider_cancel_transaction_key,
    refunded_at
)
SELECT
    id,
    amount,
    NULL,
    NULL,
    refunded_at
FROM payment
WHERE refunded_at IS NOT NULL;

-- 5) 백필 결과 확인
SELECT *
FROM payment_refund
ORDER BY id DESC;

SELECT COUNT(*)
FROM payment
WHERE refunded_at IS NOT NULL;
```

### 8.2 `payment.refunded_at` 삭제 전 필수 확인

아래 SQL은 **백필 성공 뒤 즉시 실행하는 단계가 아니다.** `AdminOrderMapper`, View, DTO, 매출 집계, API 응답이 `payment_refund` 이력을 조회하도록 전환되고, 기존 환불 건수와 이력 행 수가 일치한 뒤 별도 승인으로 실행한다.

```sql
ALTER TABLE payment
    DROP COLUMN refunded_at;
```

확인 항목:

- [ ] `SHOW CREATE TABLE payment`로 `order_id` UNIQUE 인덱스의 실제 이름과 FK 의존성을 확인한다.
- [ ] 삭제 전 `payment` 및 환불 대상 행 백업을 만든다.
- [ ] `payment.refunded_at IS NOT NULL` 건수와 백필된 `payment_refund` 건수가 일치한다.
- [ ] 기존 Mapper·View·DTO·매출 SQL에서 `payment.refunded_at` 참조를 모두 `payment_refund` 기준으로 바꾼다.
- [ ] 전액 환불·부분 환불·환불 실패·중복 환불의 API/DB 회귀 테스트를 통과한다.

### 8.3 `provider` 삭제는 롤백 전용

```sql
ALTER TABLE payment
DROP COLUMN provider;
```

이 SQL은 정방향 migration의 마지막 단계가 아니라, `provider` 도입을 취소해야 하는 경우의 롤백 후보이다. 이미 `provider` 값을 사용한 payment·API·Mapper가 있으면 먼저 의존성을 제거해야 한다.

### 8.4 초안 보완이 필요한 점

- `payment_refund.amount`는 `DEFAULT 0`보다 0보다 큰 실제 환불 금액만 허용하는 제약이 안전하다.
- 환불 성공/실패를 구분하려면 `status`, `failure_code`, `failure_message`, `requested_at`이 추가로 필요하다. 현재 초안은 성공 이력 중심이다.
- 토스 `cancels[].transactionKey`는 `provider_cancel_transaction_key`에 저장하는 방향이 맞다. 원 결제의 `paymentKey`는 별도로 `payment`에 보관해야 한다.
- 부분 환불을 지원하면 `payment.amount`(최초 승인 금액)는 유지하고, 환불 가능 잔액은 계산하거나 별도 `remaining_amount`로 관리한다.

## 9. 구현 전에 팀이 결정할 항목

- [ ] v1은 가상 카드 전액 환불만 할지, 부분 환불도 시연할지
- [ ] `payment.amount`를 최초 승인 금액으로 유지할지, `original_amount`를 추가할지
- [ ] `paid_at`와 `approved_at`을 하나로 통일할지
- [ ] 실제 토스 연동 시 `provider`, `provider_payment_key`를 `payment`에 추가할지
- [ ] `payment_refund` migration 및 관리자 환불 이력 화면(SCR-010)을 범위에 넣을지
- [ ] PG 성공·DB 실패 수동 확인 로그의 보관 위치와 담당자를 정할지

## 10. 검증 기준

- 전액 환불: `payment_refund` 성공 이력 1건, `remaining_amount=0`, payment/order 상태와 시각이 함께 갱신된다.
- 부분 환불: 환불 이력이 누적되고, 최초 승인 금액은 변하지 않으며 잔액만 감소한다.
- 중복 요청: 동일 PG 취소 거래 키가 두 번 저장되지 않고, 두 번째 요청은 상태 충돌로 반환된다.

## 11. 적용 상태 정정 (2026-08-26)

사용자 확인에 따라 8장의 SQL 초안은 모두 실행 완료됐다. 따라서 현재 DB에는 `payment_refund` 테이블과 `idx_payment_order_id` 인덱스가 존재하고, `payment.order_id` UNIQUE·`payment.refunded_at`은 제거됐다. SQL 마지막 구문도 실행됐으므로 `payment.provider`는 현재 존재하지 않는다.

이 문서의 API·PG 연동·상태/실패 이력 확장 제안은 여전히 미구현이다. 실제 토스 연동 전에는 원 결제 키를 보관할 `provider_payment_key`와 provider 구분 컬럼 재도입 여부를 확정해야 한다.
- PG 실패: `payment`와 `orders` 상태는 바뀌지 않고 실패 이력/오류 근거만 남는다.
- PG 성공 후 DB 실패: DB 상태를 성공으로 표시하지 않고 구조화 로그로 수동 확인할 수 있다.

## 11. 이번 문서에서 하지 않은 것

- 실제 DB 테이블 생성·migration 작성
- 토스 API 호출, 시크릿 키 설정, 웹훅 구현
- 카드/계좌/현금영수증 개인정보 저장
- Backend·Admin·Kiosk 소스 수정 및 API/DB 실행 검증
