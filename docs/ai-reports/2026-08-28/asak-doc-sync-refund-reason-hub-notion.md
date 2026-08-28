# ASAK 문서·DevCopilot Hub·Notion 동기화 — 환불 사유·main 머지

- 동기화 일시: 2026-08-28
- 범위: 환불·환불 사유 API/FE/DB seed와 Hub·Notion 반영
- 제외: 소스코드, 실제 DB seed 실행, Git commit/push

## 기준 커밋

| 저장소 | HEAD |
|---|---|
| ASAK-back | `494baef` |
| ASAK-Admin | `4f0c9cd` |
| ASAK (문서) | `46740ea` (+ 이번 로컬 수정) |

## 확인한 코드

| 구분 | 경로 |
|---|---|
| 환불 PATCH | `AdminOrderController.refundOrder`, `OrderRefundRequest` |
| 환불 사유 GET | `AdminRefundReasonController`, `AdminRefundReasonService` |
| Mapper | `AdminPaymentMapper.xml`, `AdminCommonCodeMapper.xml` |
| seed SQL | `ASAK-back/docs/migrations/20260828_refund_reason_codes.sql` |
| Admin FE | `ordersApi.orderRefund`, `refundReasonsApi`, `OrderManagePage` |
| 주문 상세 | `AdminOrderMapper` `paymentMethod` association (`methodName`) |

## 갱신한 로컬 문서

| 문서 | 변경 |
|---|---|
| `docs/wiki/rest-api-spec.md` | main 머지 반영, refund/refund-reasons 구현 표 추가, body `refundReasonCode`/`refundReasonDetail`, FE 계약 일치, Hub id 449/457 |
| `docs/wiki/db-table-definition.md` | `REFUND_REASON` seed 표 추가 |
| `docs/planning/admin-todo-2026-08-24.md` | branch→main 정정, TODO-038/039/039a 완료(검증 대기) |

## DevCopilot Hub (workspace 2)

| 대상 | 결과 |
|---|---|
| 환불 PATCH id **449** | body·응답·설명 갱신 (`refundReasonCode`/`refundReasonDetail`) |
| 환불 사유 GET id **457** | **신규** `GET /api/admin/refund-reasons` |
| API-024 cancel id **291** | refund 분리·사유 body 안내 갱신 |

재조회: id 449·457·291 저장 확인.

## Notion

| 페이지 | 결과 |
|---|---|
| [06. API 명세](https://app.notion.com/p/34651ef04f0b838ca3a481e55eebfb2b) | `## 2026-08-28` 섹션 추가 (main 머지·사유 API·FE 계약 일치) |
| [05. DB 설계](https://app.notion.com/p/1d951ef04f0b83019b4281f04c7b12cc) | `REFUND_REASON` seed 표 추가 |

Notion 인라인 API DB 개별 행 upsert는 이번 범위에서 하지 않음.

## 검증

- Hub/Notion 쓰기 후 fetch로 본문 반영 확인.
- `git diff --check` (수정 문서): 통과 예정.
- HTTP/Bruno/실PG/seed DB 적용: **미실행**.

## 남은 불일치 · 결정 필요

| 상태 | 내용 |
|---|---|
| `구현 불일치` | `findRefundTarget`에 `providerPaymentKey` SELECT 없음 |
| `구현 불일치` | `insertPaymentRefund` `#{cancelTransactionKey}` vs `providerCancelTransactionKey` |
| `미검증` | seed SQL DB 적용, HTTP E2E, 실PG |
| `결정 필요` | Hub/Notion 정본 API 번호 (id 449/457은 번호 미배정 카드) |

## 수정하지 않은 범위

- ASAK-back / ASAK-Admin 소스코드
- Git commit/push
- 채팅 JWT·토큰 (파일·보고서에 미기록)

## 관련 보고서 (2026-08-28 추가)

- WBS·완료 기능·QA: `docs/ai-reports/2026-08-28/asak-doc-sync-wbs-qa-completed-features.md`
