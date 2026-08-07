# ASAK Current Status Baseline

> 기준일: **2026-08-07** (7/28 baseline 위에 실연동 우선순위·Admin 주문 API 진척을 덮어씀).
> **화면별 상세:** [구현 맵](../planning/current-implementation-map-2026-07-16.md) ← SCR 상태표
> 문서 입구: [START_HERE](../START_HERE.md) · WBS: [wbs-v2](wbs-v2-2026-07-16.md) · [상태 메모](wbs-status-notes.md)
> 회의록: [operations/meeting-minutes](../operations/meeting-minutes/README.md) · [Hub wiki/78](https://devcopilot.ai.kr/workspace/2/wiki/78)
> 이 문서는 **요약 baseline**이며 **완료(DONE) 주장이 아닙니다.**
> 원칙: **1차 mock 연결 ≠ DONE** · **코드 있음 ≠ 통합 검증 완료**.

## Evidence 기반 상태

| 영역 | 검증된 상태 | Status |
|---|---|---|
| Figma | 0718 UI 이식 · **7/20 이후 추가 디자인 중지** · 구독 종료 전 백업 공유 | DESIGN_DONE (동결) |
| Kiosk | Home→Cart mock 동작. **우선:** 장바구니 검증→주문 생성→결제수단·승인 실연동(DB 확인). 결제/완료/타임아웃 일부 shell | **IN_PROGRESS** |
| Admin | 주문 Live·목록·상세·상태·취소: BE **구현·미검증**. 메뉴 GET 부분. CRUD·품절·결제수단·매출·대시보드: **mock/스텁** → mock 제거가 강사 순서 | **IN_PROGRESS** |
| Backend | 주문 조회·Live·상태/취소 경로 존재. 메뉴 POST/PATCH/DELETE·품절·결제수단·매출 Controller는 스텁 또는 미완. Kiosk 주문 저장·결제 연동 우선 | **IN_PROGRESS** |
| DB | 외부 MySQL·View 존재. 변경 API·실주문 E2E·뷰 재검증 남음 | **IN_PROGRESS** |
| QA | TC 다수 TODO · 실행 evidence 없음 → PASS 승격 금지 | **TODO** |
| Hub 문서 | 회의록 wiki/78·체크리스트 wiki/15·API wiki/12 갱신(8/6~8/7). req/wbs/qa %는 운영 지표 아님 | **REFERENCE** |

## DevCopilot 전수 점검 (2026-07-30)

- MCP로 요구사항 56건, 시나리오 25건, 화면 24건, WBS 170건, API 24건, DB 테이블/뷰 39건, QA 16건, 버그 0건을 재조회했다.
- 실행 정본 `WBS2-001`~`066`의 원격 상태는 로컬 `wbs-v2`와 **66건 모두 일치**한다. 별도 39건은 `[ARCHIVED DUPLICATE]` 보존 레코드이므로 현재 작업 상태로 집계하거나 수정하지 않는다.
- MCP에는 Wiki 도구가 없으므로 이 페이지의 원격 반영은 정확한 Wiki ID를 사용한 REST fallback으로 처리한다. WBS Evidence와 항목 간 관계(link mutation)는 MCP 미지원이며 로컬 정본 문서에 유지한다.
- API·DB는 원격 상세가 로컬 요약보다 많고, 요구사항·시나리오·QA·화면은 코드/Figma/실행 증거의 추가 확인 없이는 상태를 추정 갱신하지 않았다.

## 저장소 baseline

| Local folder | Current remote | Intended role | Decision |
|---|---|---|---|
| `ASAK` | `hagenie128/ASAK` | 정본 docs/data/Product Bible | 현재 정본 문서 소스 |
| `ASAK-Kiosk` | `hagenie128/ASAK-front` | 고객 React 앱 | BLOCKED — 로컬 remote와 목표 `ASAK-Kiosk` 불일치; 자동 변경 금지 |
| `ASAK-Admin` | `hagenie128/ASAK_Admin` | 관리자 React 앱 | 현재 정본 admin 구현 대상 · 작업 브랜치 `feature/admin-mock-figma-parity` (main 미머지) |
| `ASAK-back` | `nayeon0828/ASAK-backend` | Spring Boot API | 로컬 폴더명은 유지 · API/DB 통합 검증 전 **IN_PROGRESS** |

## Backend 코드 baseline (2026-07-28)

| 구분 | 코드상 확인된 범위 | 검증/제한 |
|---|---|---|
| Kiosk 조회 | `GET /api/kiosk/categories`, `/menuList`, `/menuDetail/{menuId}` → `UserMenuController`·`UserMenuService`·`UserMenuMapper` | MyBatis SQL은 존재하나 실DB 응답 미검증 |
| Kiosk 장바구니 | `POST /api/kiosk/cart/validate` → 메뉴 존재·품절·옵션·제외 재료를 조회하고 서버에서 `totalAmount` 재계산 | Bruno/실DB 미검증 |
| Kiosk 주문·결제 | `POST /api/kiosk/orders` mapping은 있으나 `createOrder()`가 검증 뒤 `null` 반환. `UserPayController`는 mapping 없음 | **미완성** — 저장·결제 성공 응답으로 사용 금지 |
| Admin 조회 | `GET /api/admin/menus`, `/{menuId}`, `/api/admin/orders`, `/{orderId}`, `/live` → Service·Mapper XML 조회 경로 존재 | 목록·상세·빈 결과·필터의 실API/DB 검증 미실행 |
| Admin 변경/통계 | 주문 상태 변경·취소, 품절, 결제수단, 매출/대시보드 Controller mapping 없음. `AdminStatsController`는 빈 클래스 | **미구현** |
| DB 읽기 모델 | `docs/view.sql`에 메뉴·주문·실시간 주문·판매 집계 뷰 정의 | 실제 DB 적용/합계 대조 미검증 |
| 컴파일 | `gradlew.bat compileJava --no-daemon` | **2026-07-28 BUILD SUCCESSFUL**; Spring context/Mapper XML/DB 연결 검증은 별도 |

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
| Backend business API | 조회·장바구니 검증은 코드 경로 존재, 저장·결제·상태변경/취소·품절·매출은 미완성 또는 미구현 |
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
