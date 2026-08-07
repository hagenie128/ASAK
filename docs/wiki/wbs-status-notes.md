# WBS 상태 메모 (코드 기준)

> 기준일: **2026-08-07**
> **WBS 정본:** [wbs.md](wbs.md) — ID **`WBS-001`~`085`**
> Hub 상태만: TODO · IN_PROGRESS · IN_REVIEW · DONE · DELAYED
> **팀:** 김나연 · 이하진

## 영역 구간

| 영역 | ID | 건수 |
|---|---|---|
| 기획 | WBS-001~013 | 13 |
| 디자인 | WBS-014~022 | 9 |
| 키오스크 | WBS-023~038 | 16 |
| 관리자 | WBS-039~051 | 13 |
| 백엔드 | WBS-052~066 | 15 |
| 연동 | WBS-067~071 | 5 |
| QA | WBS-072~079 | 8 |
| 운영 | WBS-080 | 1 |
| 발표 | WBS-081~085 | 5 |

> WBS는 **백엔드만이 아님.** 키오스크·관리자·디자인·QA·발표가 같은 `WBS-*` 체계.

## 8/7 가속 (DONE으로 올리기 없음)

| 묶음 | ID 감각 | Hub 권고 |
|---|---|---|
| Kiosk 주문·결제 | 키오스크 후반 · 연동 | IN_PROGRESS (실연동 전 DONE 금지) |
| Admin 주문 | 관리자 주문 구간 | IN_PROGRESS |
| Admin 메뉴·품절·결제·매출 | 관리자 중후반 | IN_PROGRESS / TODO |
| Backend 슬라이스 | 백엔드 052~066 | 화면과 같이 수직으로 |
| QA·발표 | 072~085 | 근거 없이 DONE/PASS 금지 |

계약: `totalAmount`, `APPROVED`, `EAT_IN`/`TAKE_OUT`, Live=`/orders/live`, `/paymentMethods`.

## 읽는 법

1. 할 일·로드맵·제외 = [wbs.md](wbs.md)만.
2. mock 1차만으로 DONE 금지.

## 코드 감각

| 영역 | ID | 상태 감각 |
|---|---|---|
| 키오스크 | 023~038 | 라우트 DONE · 메뉴/결제 IN_PROGRESS · 토스트/타임아웃 TODO |
| 관리자 | 039~051 | 대부분 IN_PROGRESS · QA 잔여 |
| 백엔드 | 052~066 | 조회 IN_PROGRESS · 일부 TODO |
| 연동~발표 | 067~085 | DELAYED/TODO 혼재 |

상세 근거는 [wbs.md](wbs.md) 행을 본다.

## 동기화 메모

- **2026-08-07:** 로컬 WBS 통합본 `wbs.md` (85건) + Notion형 상세 필드. Hub 재등록은 로컬 확정 후.
