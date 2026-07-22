# ASAK Current Status Baseline

> 기준일: **2026-07-23** · 소스 코드(실제 구현)를 재감사했습니다.  
> **화면별 상세:** [구현 맵](../planning/current-implementation-map-2026-07-16.md) ← SCR 상태표  
> 문서 입구: [START_HERE](../START_HERE.md) · WBS: [wbs-v2](wbs-v2-2026-07-16.md) · [상태 메모](wbs-status-notes.md)  
> 이 문서는 **요약 baseline**이며 **완료(DONE) 주장이 아닙니다.**  
> 원칙: **1차 mock 연결 ≠ DONE** (필터 고도화·실패 fixture·실 API·QA evidence 남으면 IN_PROGRESS).

## Evidence 기반 상태

| 영역 | 검증된 상태 | Status |
|---|---|---|
| Figma foundation/shared/component structure | 0718 파일 기준 UI 이식; design QA는 별도 트랙 | DESIGN_DONE only |
| Kiosk | 라우트 10개 연결. Home→메뉴→상세→장바구니까지 mock 동작. 가격(`priceCalculation`)·수량한도(`quantityLimits` 9/30) 적용. 결제/완료/타임아웃은 UI shell만 | **IN_PROGRESS** |
| Admin | Figma 라우트 + **전 화면 Page↔mock 1차 바인딩** (Live·주문·품절·메뉴·결제·매출 3·대시보드). Shared `AdminAsyncState`/`AdminConfirmDialog` P1. 셸 1920×1080+scale. **실 business API·실패 fixture·P2 polish·QA evidence 미완** | **IN_PROGRESS** (mock 1차 연결) |
| Backend | Spring Boot skeleton + `GET /api/health`만 | business API **BLOCKED** / TODO |
| DB | DevCopilot model 26 tables·4 views; backend schema/entity/repository 없음 | **TODO** |
| QA | 테스트 케이스 16건, 실행 evidence 없음 | **TODO** |

## 저장소 baseline

| Local folder | Current remote | Intended role | Decision |
|---|---|---|---|
| `ASAK` | `hagenie128/ASAK` | 정본 docs/data/Product Bible | 현재 정본 문서 소스 |
| `ASAK-Kiosk` | `hagenie128/ASAK-front` | 고객 React 앱 | BLOCKED — 로컬 remote와 목표 `ASAK-Kiosk` 불일치; 자동 변경 금지 |
| `ASAK-Admin` | `hagenie128/ASAK_Admin` | 관리자 React 앱 | 현재 정본 admin 구현 대상 · 작업 브랜치 `feature/admin-mock-figma-parity` (main 미머지) |
| `ASAK-back` | `hagenie128/ASAK-back` | Spring Boot API | Skeleton only |

## 코드 기준 프론트 진척 (2026-07-23)

### Kiosk (`ASAK-Kiosk`)

| 항목 | 실제 | Status |
|---|---|---|
| `/` `/menu` `/menu/:id` `/cart` | mock 데이터로 동작 | DONE~IN_PROGRESS |
| `/payment` `/complete` `/payment-error` `/timeout` | 라우트+UI shell, flow 미연결 | IN_PROGRESS / TODO |
| `priceCalculation.js` / `quantityLimits.js` | 단일 기준 적용 | DONE (한도 toast UX는 TODO) |
| API adapter | stub / 미연결 | IN_PROGRESS |
| 결제수단 개수 | mock/UI에 **8종** 잔존 가능 | Admin(4종)과 **불일치** → 계약 재확인 필요 |

### Admin (`ASAK-Admin`)

| 경로(코드) | 화면 | 데이터 (2026-07-23 실측) |
|---|---|---|
| `/` | 주문 현황(Live) | **mock 연결** (`getLiveOrders` · 완료/취소 stub · AsyncState/Confirm). 페이징 UI 등 잔여 |
| `/dashboard` | 대시보드 | **mock 연결** (`useDashboard`). 최근 주문 ← `getDashboard().recentOrders`. 전주 대비 등 일부 정적 |
| `/orders` | 주문 관리 | **mock 연결** (`useOrdersQuery` · 목록 표시/필터 · 상세 · 환불/영수증 Confirm). **목록에 상태 변경 UI 없음**(시안 범위). 필터 고도화 잔여 |
| `/sold-out` | 품절 관리 | **mock 연결** (`useSoldOutDraft` · draft/저장 stub · Confirm). 카드 **2줄 clamp**·카테고리 배지 정합. 저장이 `menus.isSoldOut` 미갱신 · 검색/탭·실패 fixture TODO |
| `/menus`, `/menus/new\|edit` | 메뉴 관리/편집 | **mock 연결** (`useMenusQuery`). Page=조립(`MenuListPanel`+Detail/Edit) · `IngredientSelectModal`. 저장 stub toast |
| `/payment-methods` | 결제수단 | **mock 연결** (`usePaymentMethodDraft`). Figma SCR-018 **4종** (`card`→`kakao`→`naver`→`zero`). 실패 fixture·점검 뱃지 TODO |
| `/sales`, `/sales/monthly`, `/sales/daily` | 매출 3화면 | **mock 연결** (`useSalesQuery` · `AdminDatePicker` single/range). SCR-019~021 |

**공통 인프라 (2026-07-23)**

| 항목 | 상태 |
|---|---|
| 셸 | Figma **1920×1080** 캔버스 + viewport `scale` (`AdminLayout`) |
| Shared | `AdminAsyncState` · `AdminConfirmDialog` — 주요 화면 P1 적용 (State QA evidence는 별도) |
| 데이터 흐름 | Page → Hook → `adminMockRepository` → `asak-admin-data.json` |
| 실행 문서 | 루트 `IMPLEMENTATION_PLAN.md` 등은 **삭제됨** → `STRUCTURE_GUIDE` · `public/mocks/README.md` · 중앙 WBS/맵 참고 |

> Canonical 문서 경로(`/orders/live`, `/soldOut`, `/paymentMethods`)와 **코드 kebab-case가 불일치** (WBS2-033).  
> ~~전부 하드코딩 / Page 연동 0~~ → **전 화면 1차 mock 연동**. 상세 필드 대조: `ASAK-Admin/public/mocks/README.md`.

## 적용 규칙

- Design/정적 UI 완료는 코드·mock 연동·QA evidence 없이 implementation DONE이 되지 않습니다.
- **mock 1차 연결만으로 DONE이 되지 않습니다.** 실패 fixture·실 API·계약 정렬·QA 실행 evidence가 남으면 IN_PROGRESS.
- DevCopilot에 문서화된 API·DB model은 backend evidence가 있을 때까지 명세입니다.
- **정본 우선순위:** 코드 증거 → 구현 맵/baseline → Product Bible / Canonical → DevCopilot → 구 문서.
- Kiosk 저장소 마이그레이션은 `NEEDS_CONFIRMATION`; pull, remote rewrite, reset, rebase는 허용되지 않습니다.

## 남은 위험 · 다음 묶음 (Admin)

| 항목 | 상태 |
|---|---|
| Backend business API | **BLOCKED** — 저장/환불 등은 stub |
| Admin↔Kiosk 결제수단 개수 | Admin **4** vs Kiosk **8** 가능 → 계약 재확인 |
| 품절 저장 stub | `menus.isSoldOut` 미동기화 |
| P2 polish | 결제 정책 화면 · Login Unauthorized · 메뉴 이미지 폴백 등 |
| Evidence 원격 | DevCopilot Evidence 필드는 MCP 미지원 → 로컬 `wbs-v2` Evidence만 상세 |
| Live 페이징 · 실패 fixture · QA | 미완 |

## 동기화 메모

### 2026-07-20

- DevCopilot `WBS2-001`~`066` 제목을 한글로 통일하고, P3/P4 상태를 코드 증거에 맞게 조정했습니다.
- `screens.json`의 SCR-020/021(영수증·멤버십)은 DevCopilot·Admin 구현(월별/일별 매출)과 충돌 → SCR-020/021=매출, SCR-023/024=향후 범위로 재정렬합니다.

### 2026-07-22

- 7/21 Admin mock 페이지 바인딩(주문·품절·결제수단·공통 pagination)과 대시보드/Live 연결을 **문서에 반영**.
- baseline의 「Page 연동 0」 문구를 폐기하고, 화면별 mock 연결/잔여 TODO를 분리 표기.
- DevCopilot 원격 상태 재동기화: **2026-07-22 MCP로 Status 재확인 완료** (P4 일치). Evidence 상세는 MCP 미지원 → 로컬 `wbs-v2` Evidence 열 참고.

### 2026-07-23

- Admin **매출 3화면·메뉴** mock 연결, DatePicker, Page=조립, Shared Async/Confirm, 결제수단 4종, 셸 1920×1080+scale, 품절 카드 2줄/배지를 baseline·맵·WBS Evidence에 반영.
- 작업 브랜치: `ASAK-Admin` → `feature/admin-mock-figma-parity` (main 미머지).
- Status는 DoD 미충족으로 **전부 IN_PROGRESS 유지** (1차 mock ≠ DONE).
- 상세 작업 기록: `ASAK/worklog/entries/이하진/2026-07-23-admin-mock-figma-parity.md`.
