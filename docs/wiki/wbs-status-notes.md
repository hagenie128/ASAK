# WBS 상태 메모 (코드 기준)

> 기준일: **2026-07-20**  
> 문서 입구: [START_HERE](../START_HERE.md)  
> 실행 정본 표: [wbs-v2.md](wbs-v2.md)  
> DevCopilot: workspace 2 · WBS2 제목 **한글** 동기화 완료  
> Legacy 표: [wbs-schedule.md](wbs-schedule.md) (실행에 쓰지 말 것)

## WBS 안내 (초보)

| 보고 싶은 것 | 문서 |
|---|---|
| 오늘 할 일 목록 | [wbs-v2.md](wbs-v2.md) 의 `WBS2-*` |
| 코드로 본 진행률 | **이 메모** |
| 앱별 상세 순서 | Kiosk/Admin/back `IMPLEMENTATION_PLAN.md` |
| 옛 WBS-001~ 표 | `wbs-schedule.md` (Historical) |

## 읽는 법

1. **할 일**은 `wbs-v2.md`의 `WBS2-*`만 본다.  
2. DevCopilot 대시보드 %는 EXCLUDED가 분모에 들어가 **운영용으로 쓰지 않는다**.  
3. DONE은 **코드·mock evidence**가 있을 때만. 정적 UI만 있으면 IN_PROGRESS.

## P3 키오스크 (WBS2-017 ~ 032)

| ID | 한글 제목 (DevCopilot) | 코드 근거 | 상태 |
|---|---|---|---|
| 017 | 키오스크 전체 라우트 연결·흐름 점검 | 10 routes | DONE |
| 018~021 | 메뉴 목록/상세/옵션/알레르기 | mock 동작 | IN_PROGRESS |
| 022~023 | 수량 9 / 장바구니 30 | quantityLimits | DONE |
| 024 | 4초 토스트 | 미완 | TODO |
| 025 | 장바구니 수량·삭제 | CartPage | IN_PROGRESS |
| 026~028 | 결제·완료 | UI shell | IN_PROGRESS / 027 TODO |
| 029~030 | 타임아웃 | stub | TODO |
| 031~032 | 상태 UI·QA | 부분 | IN_PROGRESS / TODO |

## P4 관리자 (WBS2-033 ~ 045)

| ID | 한글 제목 | 코드 근거 | 상태 |
|---|---|---|---|
| 033 | 라우트 Registry 정렬 | kebab vs Canonical | IN_PROGRESS |
| 034~036 | Dashboard·Live·Orders | 정적 UI | IN_PROGRESS |
| 037 | 주문 상태·TTS stub | 없음 | TODO |
| 038~043 | 품절·메뉴·결제·매출 | 정적 UI · mock READY | IN_PROGRESS |
| 044~045 | 상태 UI·QA | 미흡 | TODO |

**공통:** `adminMockRepository`는 준비됨, **Page 연동 0** → 스프린트 핵심.

## P5~P8 (요약)

| 구간 | ID | 상태 |
|---|---|---|
| Backend | 046~056 | TODO (health only) |
| 연동 | 058~060 | BLOCKED |
| QA | 061~063 | TODO / BLOCKED |
| 문서·배포·발표 | 064~066 | IN_PROGRESS / BLOCKED / TODO |

## DevCopilot 동기화 기록

- 2026-07-20: WBS2-001~066 제목 한글화, P3/P4 상태 코드 반영  
- LMIS 요구 8건 → IN_PROGRESS (UI shell)  
- Target API create (`/api/kiosk/*`, `soldOut`, sales…) — MCP API update 불가  
- 상세: [devcopilot-sync-report.md](devcopilot-sync-report.md)

## 화면 ID와 WBS

| SCR | 의미 | 관련 WBS |
|---|---|---|
| 020 | 월별 매출 | 042 |
| 021 | 일별 매출 | 043 |
| 022 | 대시보드 | 034 |
| 023/024 | 영수증·멤버십 Future | — |
