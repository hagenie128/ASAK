# WBS 상태 메모 (코드 기준)

> 기준일: **2026-07-24**  
> 문서 입구: [START_HERE](../START_HERE.md)  
> 실행 정본 표: [wbs-v2-2026-07-16.md](wbs-v2-2026-07-16.md)  
> DevCopilot: workspace 2 · WBS2 제목 **한글** 동기화 완료 (7/20). **7/24** P5 중 코드/계약 증거가 있는 **048~051·053~055 → IN_PROGRESS** (DONE 아님). 매출 API-017/018/019·대시보드 API-020 예시 보강. Evidence 필드는 MCP 미지원 → 로컬 wbs-v2만 상세.
> Legacy 표: [wbs-schedule.md](wbs-schedule.md) (실행에 쓰지 말 것)

## WBS 안내 (초보)

| 보고 싶은 것 | 문서 |
|---|---|
| 오늘 할 일 목록 | [wbs-v2-2026-07-16.md](wbs-v2-2026-07-16.md) 의 `WBS2-*` |
| 코드로 본 진행률 | **이 메모** |
| 앱별 상세 순서 | Admin: `STRUCTURE_GUIDE` · mocks README (루트 `IMPLEMENTATION_PLAN`은 **삭제됨**) |
| 옛 WBS-001~ 표 | `wbs-schedule.md` (Historical) |

## 읽는 법

1. **할 일**은 `wbs-v2-2026-07-16.md`의 `WBS2-*`만 본다.  
2. DevCopilot 대시보드 %는 EXCLUDED가 분모에 들어가 **운영용으로 쓰지 않는다**.  
3. DONE은 **코드·mock evidence**가 있을 때만. 정적 UI만 있으면 IN_PROGRESS.  
4. mock **1차 연결**만으로는 DONE이 아니다. 필터 고도화·실패 fixture·실 API·QA evidence가 남으면 IN_PROGRESS.

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

| ID | 한글 제목 | 코드 근거 (2026-07-23) | 상태 |
|---|---|---|---|
| 033 | 라우트 Registry 정렬 | kebab vs Canonical | IN_PROGRESS |
| 034 | Dashboard | `useDashboard` · 최근주문=`getDashboard().recentOrders` | IN_PROGRESS |
| 035 | Live 주문 현황 | `getLiveOrders` · 완료/취소 stub · Async/Confirm | IN_PROGRESS |
| 036 | 주문 목록/상세 | 표시/필터 · 환불/영수증 Confirm · **목록 상태변경 UI 없음** · 필터 고도화 잔여 | IN_PROGRESS |
| 037 | 주문 상태·TTS stub | Live 완료/취소만 · 목록 PATCH 의도적 미구현 · TTS 미완 | TODO |
| 038 | 품절 draft·저장 | `useSoldOutDraft` · 2줄 카드·배지 · **`menus.isSoldOut` 미동기화** · 실패 fixture TODO | IN_PROGRESS |
| 039 | 메뉴 관리/편집 | `useMenusQuery` · Page=조립 · 재료 모달 · 저장 stub | IN_PROGRESS |
| 040 | 결제수단 토글·저장 | Figma **4종** · 토글/저장 · 실패 fixture TODO | IN_PROGRESS |
| 041~043 | 매출 3화면 | `useSalesQuery` · `AdminDatePicker` mock 연결 | IN_PROGRESS |
| 044 | 상태 UI (Async/Confirm) | Shared P1 주요 화면 적용 · State QA evidence 남음 | IN_PROGRESS |
| 045 | 날짜·합계·내비 QA | 미실행 | TODO |

**공통:** `adminMockRepository` **전 화면 1차 연동**. 셸 1920×1080+scale. 브랜치 `feature/admin-mock-figma-parity`.  
**다음 묶음** = 실패 fixture · 품절↔menus sync · Admin↔Kiosk 결제 개수 계약 · P2 polish · QA evidence. Backend **BLOCKED**.

## P5~P8 (요약)

| 구간 | ID | 상태 |
|---|---|---|
| Backend | 046~047·052·056 | TODO |
| Backend | 048~051·053~055 | IN_PROGRESS (골격·계약·뷰; DoD/테스트 남음) |
| 연동 | 058~060 | BLOCKED |
| QA | 061~063 | TODO / BLOCKED |
| 문서·배포·발표 | 064~066 | IN_PROGRESS / BLOCKED / TODO |

## DevCopilot 동기화 기록

- 2026-07-20: WBS2-001~066 제목 한글화, P3/P4 상태 코드 반영  
- LMIS 요구 8건 → IN_PROGRESS (UI shell)  
- Target API create (`/api/kiosk/*`, `soldOut`, sales…) — MCP API update 불가  
- 상세: [devcopilot-sync-report.md](../_archive/wiki-secondary/devcopilot-sync-report.md)
- 2026-07-22: 로컬 baseline/맵/이 메모를 7/21 Admin 진척에 맞춤. DevCopilot MCP로 workspace 2 WBS **원격 Status 재확인** → P4(033~045) active 행이 로컬과 일치(034~036·038~043 IN_PROGRESS, 037·044~045 TODO). Evidence는 MCP 미지원이라 로컬 문서만 상세 갱신.
- 2026-07-23: 매출·메뉴·Shared·결제 4종·셸 scale을 로컬 Evidence/이 메모에 반영. **MCP 원격 Status 동기화 성공** — 비교 후 **WBS2-044(pk=162)만 TODO→IN_PROGRESS**(AdminAsyncState/Confirm 적용). 034~036·038~043·037·045는 이미 일치(no-op). DoD 미충족 → DONE 아님. Evidence는 MCP 미지원 → 로컬만. 스냅샷: wiki/snapshots/devcopilot-wbs-live-2026-07-23.json.
- 2026-07-24: 허브 매출 API-017/018/019·대시보드 API-020 응답 예시를 `SALES_API_CONTRACT` 필드(`netSales` 등)로 보강. WBS2-048~051·053~055 → **IN_PROGRESS**(코드/계약 증거). 046·047·052·DONE 처리 없음. 058~060 BLOCKED 유지.

## 화면 ID와 WBS

| SCR | 의미 | 관련 WBS |
|---|---|---|
| 020 | 월별 매출 | 042 |
| 021 | 일별 매출 | 043 |
| 022 | 대시보드 | 034 |
| 023/024 | 영수증·멤버십 Future | — |
