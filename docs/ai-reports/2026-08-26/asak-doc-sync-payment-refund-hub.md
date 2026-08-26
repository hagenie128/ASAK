# ASAK 문서·DevCopilot Hub 동기화 — 결제 환불 이력 설계

- 동기화 일시: 2026-08-26
- 범위: 로컬 API/DB 문서와 DevCopilot workspace 2의 **기존** 주문 취소 API, `payment` 테이블 설명
- 제외: 소스 코드, 실제 DB migration, 실제 DB 스키마 변경, 새 Hub API/테이블 생성, Git 작업

## 근거

- [REST API 명세](../../wiki/rest-api-spec.md)는 `PATCH /api/admin/orders/{orderId}/refund`를 설계 제안·미구현/미검증으로 표시한다.
- [DB 테이블 정의](../../wiki/db-table-definition.md)는 현재 `payment.order_id`가 UNIQUE이고, `payment_refund`가 아직 DB 미생성인 migration 제안임을 표시한다.
- [토스 환불 데이터 모델 제안](toss-payment-refund-data-model-proposal.md)은 토스 취소 이력과 `payment_refund`의 대응 및 migration 전제 조건을 기록한다.

## 로컬 문서 반영 상태

- `docs/wiki/rest-api-spec.md`: 환불 API의 요청·검증·PG 호출·DB 반영 순서를 **제안**으로 기록했다.
- `docs/wiki/db-table-definition.md`: 현재 `payment` 구조와 목표 `payment_refund` 관계를 구분해 기록했다.
- `docs/ai-reports/2026-08-26/toss-payment-refund-data-model-proposal.md`: migration SQL 초안과 삭제 전 검증 조건을 기록했다.

## DevCopilot Hub 반영 결과

### 기존 API-024 (ID 291) 갱신

- 대상: `PATCH /api/admin/orders/{orderId}/cancel`
- 취소 API는 **미승인** `RECEIVED`/`PREPARING` 주문만 `CANCELED`로 전환한다고 명시했다.
- 승인 결제는 이 API에서 환불하지 않고 `409 ORDER_PAYMENT_APPROVED_CANCEL_NOT_ALLOWED`로 막는 계약을 명시했다.
- 별도 환불 API `PATCH /api/admin/orders/{orderId}/refund`는 설계 제안이며, Hub API 카드·구현·통합 검증이 아직 없다고 명시했다.

### 기존 `payment` 테이블 (ID 62) 설명 갱신

- 현재 테이블은 주문, 결제수단, 상태, 승인 금액/시각, `idempotency_key`, 최종 `refunded_at`을 보관한다고 명시했다.
- 현 스키마의 `order_id UNIQUE` 제약을 명시했다.
- `payment_refund`는 토스 취소 이력을 위한 **migration 제안**이고 실제 DB 및 Hub 스키마에는 아직 생성하지 않았다고 명시했다.

## 의도적으로 반영하지 않은 항목

- 새 환불 API 카드 생성: 구현/API 번호가 확정되지 않아 보류했다.
- `payment_refund` Hub 테이블 생성: 실제 migration 전이므로 보류했다.
- `payment.refunded_at` 삭제 또는 `order_id` UNIQUE 제거: 백필, 참조 전환, 회귀 검증 전이므로 보류했다.

## 검증

DevCopilot MCP 재조회로 API ID 291의 endpoint·설명·성공/오류 계약 및 `payment` 테이블 ID 62의 설명이 저장된 것을 확인했다. 실제 HTTP 환불·PG 취소·DB migration·Bruno 검증은 수행하지 않았다.

## 다음 결정 필요

1. 별도 환불 API의 API 번호와 구현 범위를 확정한다.
2. `payment_refund` migration을 실제 적용할지 승인한다.
3. 승인 결제 환불, PG 실패, PG 성공/DB 실패 수동 확인을 포함한 테스트를 진행한다.

## 적용 상태 정정 (2026-08-26)

이 보고서 최초 작성 뒤 사용자 확인으로 SQL 초안 전체가 이미 실행된 사실을 반영한다. `payment_refund` 테이블 생성, 기존 환불 행 백필, `payment.order_id` UNIQUE 제거와 `idx_payment_order_id` 생성, `payment.refunded_at` 삭제가 완료됐다. 마지막 `DROP COLUMN provider`도 실행됐으므로 현재 `payment.provider` 컬럼은 없다.

Hub의 `payment` 설명과 API-024 설명은 실제 적용된 스키마로 재동기화 완료했다. 환불 API 카드·Controller·PG 연동·통합 검증이 아직 없다는 결론은 변하지 않는다.
