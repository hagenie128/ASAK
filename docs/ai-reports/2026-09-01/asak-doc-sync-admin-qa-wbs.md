# Admin QA WBS/TODO 동기화 (2026-09-01)

## 범위

- 대상: Admin·backend의 주문 상태/취소, 환불, 품절, 결제수단, 매출 합계
- 제외: 고객(Kiosk) 코드와 고객 화면 E2E, 실제 PG 환불

## 확인 근거

| 항목 | 실DB QA 결과 |
| --- | --- |
| 주문 상태 | `RECEIVED → PREPARING → COMPLETED` 확인 |
| 승인 결제 직접 취소 | `409 ORDER_PAYMENT_APPROVED_CANCEL_NOT_ALLOWED` 확인 |
| 환불 | 가상 CARD 환불 후 주문 `CANCELED`, 결제 `REFUNDED` 확인 |
| 품절 | INGREDIENT 9816을 `true → false`로 저장·복구 확인 |
| 결제수단 | CARD `active: true → false → true` PATCH·GET 재조회·복구 확인 |
| 매출 | 2026-08-28: `951100 - 60800 = 890300`을 daily/summary API에서 확인 |

## 갱신 문서

- `docs/wiki/wbs.md`: WBS-042, 044/062, 046, 047~049/064, 071의 근거와 남은 조건을 QA 결과로 교체했다.
- `docs/wiki/wbs-status-notes.md`: Admin/backend QA 완료 범위와 미검증 범위를 분리했다.
- `docs/wiki/qa-test-cases.md`: TC-012, TC-013, TC-014, TC-017에 실제 QA 근거와 잔여 케이스를 기록했다.

## 결정 필요 및 미완료

1. `READY` 미승인 주문 취소 성공 케이스를 별도 테스트 데이터로 검증한다.
2. 환불 중복 409, OTHER 사유 detail 누락 400, 동시성 실패를 검증한다.
3. 실제 PG 취소 키·외부 취소 호출은 현재 가상 카드 환불과 별도 범위로 결정한다.
4. 고객 화면 품절/결제수단 반영과 Kiosk production build는 이번 근거에 포함하지 않는다.
