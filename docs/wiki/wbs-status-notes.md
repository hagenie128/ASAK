# WBS 상태 메모 (코드 기준)

> Status: **CURRENT**
> **할 일 정본:** [wbs.md](wbs.md) (`WBS-001`~`085`)
> Hub 상태: TODO · IN_PROGRESS · IN_REVIEW · DONE · DELAYED
> **팀:** 김나연 · 이하진

## 영역

| 영역 | ID | 건수 |
|---|---|---|
| 기획 | 001~013 | 13 |
| 디자인 | 014~022 | 9 |
| 키오스크 | 023~038 | 16 |
| 관리자 | 039~051 | 13 |
| 백엔드 | 052~066 | 15 |
| 연동 | 067~071 | 5 |
| QA | 072~079 | 8 |
| 운영 | 080 | 1 |
| 발표 | 081~085 | 5 |

WBS는 백엔드만이 아니다. 키오스크·관리자·디자인·QA·발표가 같은 `WBS-*`다.

## 이번 주 (DONE으로 올리지 말 것)

> 2026-09-01: Admin/backend 실DB QA를 추가했다. 실행 기록 없는 Hub DONE·TC PASS는 신뢰하지 않는다.

| 묶음 | ID | Hub 권고 |
|---|---|---|
| 장치 이벤트/RTOS | RTOS-DEVICE-001~003 | IN_PROGRESS (콘솔·연동 전 DONE 금지) |
| 키오스크 주문·결제 | 031~034, 069 | IN_PROGRESS · API-001~006·014 **코드 연결**(main) · Hub DONE·E2E 미실행 주의 |
| 키오스크 메뉴·타임아웃 | 024~026, 035~036 | IN_REVIEW · Hub DONE 다수이나 Bruno/E2E 없음 |
| 관리자 주문·환불 | 041~043, 070 | IN_PROGRESS · 상태 전이·승인 결제 취소 차단·가상 카드 환불 실DB 확인, `READY` 취소 성공과 화면 E2E 잔여 |
| 메뉴·품절·결제·매출 | 044~049, 046, 062 | IN_REVIEW · 품절 저장/복구·결제수단 PATCH 롤백·환불 매출 합계 실DB 확인, 고객 연동과 화면 E2E 잔여 |
| 통합 QA | 071, 077~079 | IN_REVIEW/TODO · 가상 카드 환불 1건 합계 대조 완료, 실PG·실패/중복·전 화면 회귀 잔여 |
| QA·발표 | 072~085 | 근거 없이 DONE/PASS 금지 |

계약 키워드: `totalAmount`, `APPROVED`, `refundReasonCode`, `REFUNDED`, Live=`/orders/live`, `/paymentMethods`, `/refund-reasons`.

## 코드 감각

| 영역 | ID | 감각 |
|---|---|---|
| 키오스크 | 023~038 | 라우트 DONE · 메뉴/결제 IN_PROGRESS · 토스트/타임아웃 TODO |
| 관리자 | 039~051 | 대부분 IN_REVIEW · 환불·결제수단 코드 연결 · QA·E2E 잔여 |
| 백엔드 | 052~066 | 품절·결제수단·환불·매출 구현(main) · 검증 미완 |
| 연동~발표 | 067~085 | DELAYED/TODO 혼재 |

상세 행은 [wbs.md](wbs.md)만 본다.
