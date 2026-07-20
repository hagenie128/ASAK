# ASAK Current Status Baseline

> 기준일: **2026-07-20** · 소스 코드(실제 구현)를 1차 정본으로 재감사했습니다.  
> **화면별 상세:** [구현 맵](../planning/current-implementation-map-2026-07-16.md) ← SCR 상태표  
> 문서 입구: [START_HERE](../START_HERE.md) · WBS: [wbs-v2](wbs-v2-2026-07-16.md) · [상태 메모](wbs-status-notes.md)  
> 이 문서는 **요약 baseline**이며 **완료(DONE) 주장이 아닙니다.**

## Evidence 기반 상태

| 영역 | 검증된 상태 | Status |
|---|---|---|
| Figma foundation/shared/component structure | 0718 파일 기준 UI 이식; design QA는 별도 트랙 | DESIGN_DONE only |
| Kiosk | 라우트 10개 연결. Home→메뉴→상세→장바구니까지 mock 동작. 가격(`priceCalculation`)·수량한도(`quantityLimits` 9/30) 적용. 결제/완료/타임아웃은 UI shell만 | **IN_PROGRESS** |
| Admin | Figma 정적 화면 10+ 라우트 연결. mock JSON·`adminMockRepository`는 준비됐으나 **Page 연동 0**. api/hook/adapter는 placeholder | **IN_PROGRESS** (UI shell) |
| Backend | Spring Boot skeleton + `GET /api/health`만 | business API **TODO** |
| DB | DevCopilot model 26 tables·4 views; backend schema/entity/repository 없음 | **TODO** |
| QA | 테스트 케이스 16건, 실행 evidence 없음 | **TODO** |

## 저장소 baseline

| Local folder | Current remote | Intended role | Decision |
|---|---|---|---|
| `ASAK` | `hagenie128/ASAK` | 정본 docs/data/Product Bible | 현재 정본 문서 소스 |
| `ASAK-Kiosk` | `hagenie128/ASAK-front` | 고객 React 앱 | BLOCKED — 로컬 remote와 목표 `ASAK-Kiosk` 불일치; 자동 변경 금지 |
| `ASAK-Admin` | `hagenie128/ASAK_Admin` | 관리자 React 앱 | 현재 정본 admin 구현 대상 |
| `ASAK-back` | `hagenie128/ASAK-back` | Spring Boot API | Skeleton only |

## 코드 기준 프론트 진척 (2026-07-20)

### Kiosk (`ASAK-Kiosk`)

| 항목 | 실제 | Status |
|---|---|---|
| `/` `/menu` `/menu/:id` `/cart` | mock 데이터로 동작 | DONE~IN_PROGRESS |
| `/payment` `/complete` `/payment-error` `/timeout` | 라우트+UI shell, flow 미연결 | IN_PROGRESS / TODO |
| `priceCalculation.js` / `quantityLimits.js` | 단일 기준 적용 | DONE (한도 toast UX는 TODO) |
| API adapter | stub / 미연결 | IN_PROGRESS |

### Admin (`ASAK-Admin`)

| 경로(코드) | 화면 | 데이터 |
|---|---|---|
| `/` | 주문 현황(Live) 정적 | 하드코딩 |
| `/dashboard` | 대시보드 정적 | 하드코딩 |
| `/orders` | 주문 관리 정적 | 하드코딩 |
| `/sold-out` | 품절 관리 정적 | 하드코딩 |
| `/menus`, `/menus/new\|edit` | 메뉴 관리/편집 | 정적/placeholder |
| `/payment-methods` | 결제수단 | 정적·disabled |
| `/sales`, `/sales/monthly`, `/sales/daily` | 매출 3화면 | 정적 |

> Canonical 문서 경로(`/orders/live`, `/soldOut`, `/paymentMethods`)와 **코드 kebab-case가 불일치**. 다음 작업: mock 바인딩 + route 정렬.

## 적용 규칙

- Design/정적 UI 완료는 코드·mock 연동·QA evidence 없이 implementation DONE이 되지 않습니다.
- DevCopilot에 문서화된 API·DB model은 backend evidence가 있을 때까지 명세입니다.
- **정본 우선순위:** 코드 증거 → 구현 맵/baseline → Product Bible / Canonical → DevCopilot → 구 문서.
- Kiosk 저장소 마이그레이션은 `NEEDS_CONFIRMATION`; pull, remote rewrite, reset, rebase는 허용되지 않습니다.

## 2026-07-20 동기화 메모

- DevCopilot `WBS2-001`~`066` 제목을 한글로 통일하고, P3/P4 상태를 코드 증거에 맞게 조정했습니다.
- `screens.json`의 SCR-020/021(영수증·멤버십)은 DevCopilot·Admin 구현(월별/일별 매출)과 충돌 → SCR-020/021=매출, SCR-023/024=향후 범위로 재정렬합니다.
