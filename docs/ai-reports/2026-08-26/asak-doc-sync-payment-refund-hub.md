# ASAK 문서·DevCopilot Hub·Notion 동기화 — 결제 환불

## 구간 A (오전) — migration·설계 문서화

- 동기화 일시: 2026-08-26 (초기)
- 범위: 로컬 API/DB 문서와 DevCopilot workspace 2의 **기존** 주문 취소 API, `payment` 테이블 설명
- 제외: 소스 코드, 실제 DB migration 실행, Git 작업

### 근거 (당시)

- REST/DB 문서에 환불 API를 설계 제안으로 기록.
- 사용자 확인으로 SQL 초안 전체 실행 완료: `payment_refund` 생성, UNIQUE 제거, `refunded_at`/`provider` DROP.

### Hub (구간 A)

- API-024 (id 291), `payment` (id 62) 설명 갱신.
- 환불 API 카드·`payment_refund` Hub 테이블은 당시 보류.

---

## 구간 B (저녁) — 초안 코드 근거 문서·Hub·Notion 전면 동기화

- 동기화 일시: 2026-08-26 (저녁, 사용자 승인: 문서·허브·노션 / **코드 수정 금지**)
- 기준 커밋(참고): ASAK-back `b867345`(+워킹트리 환불 초안), ASAK-Admin `b9c3ea5`(+워킹트리), ASAK docs `b655037`(+워킹트리)
- MCP: 기존 `user-devcopilot` / Notion 플러그인 사용. 채팅에 붙여 넣은 토큰은 파일·보고서에 **저장하지 않음**.

### 1. 확인한 코드·문서

| 구분 | 경로 |
|---|---|
| Controller | `ASAK-back/.../AdminOrderController.java` `PATCH .../refund` |
| Service | `AdminOrderService.refundOrder`, `PaymentService.cardRefund`, `AdminRefundTransactionService.applyRefund` |
| Mapper | `AdminPaymentMapper.xml` (`findRefundTarget`, `markPaymentRefunded`, `insertPaymentRefund`, `cancelOrderForRefund`) |
| DTO | `OrderRefundRequest.refundReason`, `OrderDetailResponse` |
| Admin FE | `ordersApi.orderRefund(orderId)` body 없음, `OrderManagePage.handleRefund` |
| 정책 | `docs/operations/meeting-minutes/2026-W31.md` — COMPLETED 유지·결제만 REFUNDED |

### 2. 갱신한 로컬 문서

| 문서 | 변경 |
|---|---|
| `docs/wiki/rest-api-spec.md` | 환불: **초안 구현 · 미검증**. ErrorCode·응답·불일치 표기 |
| `docs/wiki/db-table-definition.md` | 중복 문단 정리, 코드/미검증 메모 |
| `docs/planning/admin-todo-2026-08-24.md` | TODO-038~042 상태·계약/구현 불일치 반영 |
| 본 보고서 | 구간 B 추가 |

### 3. DevCopilot Hub (workspace 2)

| 대상 | 결과 |
|---|---|
| API-024 id **291** | cancel만; 승인 결제는 refund로 분리한다고 재기록 |
| 환불 API id **449** | **신규** `PATCH /api/admin/orders/{orderId}/refund` · 제목 `Admin Order Refund (번호 미배정 · TODO-038)` · draft/unverified |
| `payment` id **62** | 실제 스키마(UNIQUE 제거, refunded_at/provider DROP) 설명 |
| `payment.refunded_at` col **842** | Hub에 남기되 description = DROPPED |
| `payment_refund` id **169** | **신규** 테이블 + 컬럼 id/payment_id/amount/reason/provider_cancel_transaction_key/refunded_at/created_at |

재조회: API id 449 endpoint·설명 저장 확인.

### 4. Notion

| 페이지 | 결과 |
|---|---|
| [06. API 명세](https://app.notion.com/p/34651ef04f0b838ca3a481e55eebfb2b) | `## 2026-08-26 문서·Hub 동기화 (환불)` 추가. API-024 구 규칙을 cancel/refund 분리·`payment_refund` 기준으로 정정 |
| [05. DB 설계](https://app.notion.com/p/1d951ef04f0b83019b4281f04c7b12cc) | `## 2026-08-26 결제·환불 스키마 동기화` 추가 |

### 5. 실행·검증

- Hub/Notion 쓰기 후 재조회: 반영 확인.
- `git diff --check` (수정 문서): 통과.
- HTTP 환불·Bruno·실PG·E2E: **미실행** (통과로 기록하지 않음).
- 소스코드: **미수정** (사용자 지시).

### 6. 남은 불일치 · 결정 필요

| 상태 | 내용 |
|---|---|
| `계약 불일치` | FE `orderRefund(orderId)` body 없음 vs BE `refundReason` `@NotBlank` |
| `구현 불일치` | `findRefundTarget`에 `providerPaymentKey` SELECT 없음 |
| `구현 불일치` | `insertPaymentRefund` XML `#{cancelTransactionKey}` vs Service `providerCancelTransactionKey` |
| `결정 필요` | Hub/Notion **정본 API 번호** (현재 id 449는 번호 미배정) |
| `결정 필요` | `provider` / `provider_payment_key` 재도입 |
| `미검증` | HTTP·실PG·통합 테스트 |

### 7. 수정하지 않은 범위

- ASAK-back / ASAK-Admin / ASAK-Kiosk **소스코드**
- 실제 MySQL DDL 추가 실행
- Product Bible Pack 전량, Screen Bible 전량, WBS/요구사항 DevCopilot 전수
- Git commit / push / branch
- 채팅에 제공된 JWT·MCP URL 토큰 (파일·커밋·본 보고서에 미기록)

### 8. Notion API 명세 DB 행

Notion 인라인「API 명세 데이터베이스」개별 행 upsert는 이번 범위에서 하지 않았다. 페이지 본문·Hub id 449를 정본 포인터로 둔다. 행 추가가 필요하면 API 번호 확정 후 별도 승인.
