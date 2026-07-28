# WBS 상태 메모 (코드 기준)

> 기준일: **2026-07-28**
> 문서 입구: [START_HERE](../START_HERE.md)  
> 실행 정본 표: [wbs-v2-2026-07-16.md](wbs-v2-2026-07-16.md)  
> DevCopilot: workspace 2 · WBS2 제목 **한글** 동기화 완료 (7/20). **7/28**에는 Kiosk/Admin 계약 용어 정렬, Admin 주문 상세 금액 표시·API 연결 환경, Backend 주문 조회·판매 뷰·Bruno 계약 정렬을 코드와 최근 커밋으로 재확인했다. Kiosk/Admin Vite production build와 Backend `compileJava`는 통과했지만, 브라우저·실DB·Bruno 실행 증거는 아직 없으므로 관련 항목은 **IN_PROGRESS**를 유지한다. Evidence 필드는 MCP 미지원 → 로컬 wbs-v2만 상세.
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

**공통:** `adminMockRepository` **전 화면 1차 연동**. 7/28에는 API 모듈 명명과 계약 용어를 정렬하고 주문 상세에 기본 단가·옵션 추가금·제외 재료·메뉴 합계 표시를 보강했다. Kiosk와 Admin production build는 통과했다.
**다음 묶음** = 실패 fixture · 품절↔menus sync · 실제 API 응답/환경변수 연결 확인 · 브라우저 QA evidence. Backend와의 **실연동은 API·DB·Bruno 실행 증거 전까지 BLOCKED**.

## P5~P8 (요약)

| 구간 | ID | 상태 |
|---|---|---|
| Backend | 046~047·052·056 | TODO |
| Backend | 048~051·053~055 | IN_PROGRESS (주문 조회·판매 뷰·Bruno 계약 정렬, `compileJava` 통과; DoD/실API·DB 테스트 남음) |
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
- 2026-07-28: 독립 저장소의 `main...origin/main`과 최근 커밋을 재확인했다. Kiosk 계약 정규화, Admin API 연결 환경·주문 상세 금액 표시, Backend 관리자 주문 조회·판매 뷰·Bruno 요청의 계약 용어 정렬을 반영했다. `npm.cmd run build`(Kiosk/Admin), `gradlew.bat compileJava --no-daemon`(Backend)는 통과했다. 실DB·Bruno·브라우저 상호작용 검증은 미실행이므로 DONE 승격·P6 BLOCKED 해제는 하지 않았다.
- 2026-07-28 (중간점검): 실제 원격 `nayeon0828/ASAK-backend`, Spring context, 외부 MySQL(기본 테이블 25·View 22·FK 39), 읽기 API 9개를 재확인했다. 조회 경로는 실제 DB `200` 근거가 생겼으나, 주문 저장·결제·상태변경/취소·품절·매출은 미완성 또는 미구현이다. 상세 위험과 다음 순서는 [Backend·DB 중간점검](backend-db-midpoint-audit-2026-07-28.md)을 따른다.

## 화면 ID와 WBS

| SCR | 의미 | 관련 WBS |
|---|---|---|
| 020 | 월별 매출 | 042 |
| 021 | 일별 매출 | 043 |
| 022 | 대시보드 | 034 |
| 023/024 | 영수증·멤버십 Future | — |
