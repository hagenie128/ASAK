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

> 2026-08-18 선생님: 08/21까지 RTOS(적어도 Spring+React). 코드 있음 ≠ DONE.

| 묶음 | ID | Hub 권고 |
|---|---|---|
| 장치 이벤트/RTOS | RTOS-DEVICE-001~003 · API-019 | IN_PROGRESS (콘솔·연동 전 DONE 금지) |
| 키오스크 주문·결제 | 031~034, 069 | IN_PROGRESS (실연동 전 DONE 금지) |
| 관리자 주문 | 041~043, 070 | IN_PROGRESS |
| 메뉴·품절·결제·매출 | 044~049 | IN_PROGRESS / TODO · 08/24 기능 마감 전 |
| QA·발표 | 072~085 | 08/24~09/01 · 근거 없이 DONE/PASS 금지 |

계약 키워드: `totalAmount`, `APPROVED`, `EAT_IN`/`TAKE_OUT`, Live=`/orders/live`, `/paymentMethods`.

## 코드 감각

| 영역 | ID | 감각 |
|---|---|---|
| 키오스크 | 023~038 | 라우트 DONE · 메뉴/결제 IN_PROGRESS · 토스트/타임아웃 TODO |
| 관리자 | 039~051 | 대부분 IN_PROGRESS · QA 잔여 |
| 백엔드 | 052~066 | 조회 IN_PROGRESS · 일부 TODO |
| 연동~발표 | 067~085 | DELAYED/TODO 혼재 |

상세 행은 [wbs.md](wbs.md)만 본다.
