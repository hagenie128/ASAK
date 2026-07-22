# Current Implementation Map

> 기준일: **2026-07-23** · **코드 실측** 정본 (7/20 감사 + 7/21~23 Admin mock·Figma 정합 반영).  
> 문서 입구: [START_HERE](../START_HERE.md)  
> 이전 07-16 버전은 Cart/Admin을 MISSING으로 적어 **과소평가**되어 폐기 수준으로 대체됨.  
> Canonical(미코드 반영): [canonical-contract-decisions-2026-07-16.md](../governance/canonical-contract-decisions-2026-07-16.md)  
> 요약 baseline: [current-status-baseline.md](../wiki/current-status-baseline.md)  
> WBS: [wbs-v2-2026-07-16.md](../wiki/wbs-v2-2026-07-16.md) · [wbs-status-notes.md](../wiki/wbs-status-notes.md)  
> Admin 필드 대조: [`ASAK-Admin/public/mocks/README.md`](../../../ASAK-Admin/public/mocks/README.md)  
> 원칙: **1차 mock 연결 ≠ DONE**

## 상태 범례

| 코드 | 의미 |
|---|---|
| `IMPLEMENTED` | 코드로 동작 확인 |
| `PARTIAL` | UI·로직 일부만 |
| `MOCK_WIRED` | mock으로 화면까지 연결 |
| `MOCK_READY` | mock/repository만 있고 페이지 미연결 |
| `UI_ONLY` | Figma 정적/shell, 데이터·flow 없음 |
| `PLACEHOLDER` | 파일만 존재 |
| `MISSING` | 없음 |
| `BLOCKED` | 의존성(백엔드 등) 때문에 진행 불가 |
| `CONFLICT` | 문서 Canonical과 코드 불일치 |
| `FUTURE` | MVP 밖 |

## Decision overlay (Canonical vs 코드)

| 항목 | 상태 | 코드 현실 | Canonical 목표 |
|---|---|---|---|
| Kiosk API path | `CONFLICT` / DECIDED_PENDING | `/api/menus`, `/api/orders`… | `/api/kiosk/menuList` 등 |
| Admin routes | `CONFLICT` / DECIDED_PENDING | `/`, `/sold-out`, `/payment-methods` | `/orders/live`, `/soldOut`, `/paymentMethods` |
| 금액 필드 | DECIDED_NOT_IMPLEMENTED | store `totalPrice` 등 | adapter → `totalAmount` 등 |
| Admin 소유권 | 확정 | `ASAK-Admin` 정본 | Kiosk 내 Admin = Legacy Reference |

---

## Kiosk (`ASAK-Kiosk`)

| 화면 | 경로 | 상태 | 근거 / WBS |
|---|---|---|---|
| SCR-001 Home | `/` | `IMPLEMENTED` | 유형 선택 → `/menu` · WBS2-017 DONE |
| SCR-003 Menu List | `/menu` | `MOCK_WIRED` | `kiosk.json` 직접 import · WBS2-018 |
| SCR-004 Detail | `/menu/:menuId` | `MOCK_WIRED` | 옵션·담기·가격 · WBS2-019~021 |
| SCR-005 Cart | `/cart` | `MOCK_WIRED` | 수량·삭제·합계 · WBS2-025 |
| SCR-007 Payment | `/payment` | `UI_ONLY` | 수단/결제 disabled · WBS2-026 |
| SCR-008 Complete | `/complete` | `UI_ONLY` | 주문번호 미연결 · WBS2-028 |
| SCR-012 Pay Error | `/payment-error` | `UI_ONLY` | flow 미연결 · WBS2-027 |
| SCR-013 Timeout | `/timeout` | `UI_ONLY` | 타이머 stub · WBS2-029~030 |
| SCR-014 A11y | `/accessibility` | `UI_ONLY` | 정적 |
| SCR-023 Receipt | `/receipt` | `FUTURE` | 향후 범위 |

| 자산 | 상태 | 비고 |
|---|---|---|
| `priceCalculation.js` | `IMPLEMENTED` | **단일 기준 — 복제 금지** |
| `quantityLimits.js` | `IMPLEMENTED` | 9/30 적용 · 4초 toast는 TODO (WBS2-024) |
| `orderSessionStore` / cart 호환 | `IMPLEMENTED` | |
| `api/*` + adapters | `PLACEHOLDER` / `PARTIAL` | 페이지 미사용 |
| `public/mocks/kiosk.json` | `MOCK_WIRED` | 정본 mock |

---

## Admin (`ASAK-Admin`)

| 화면 | 경로(코드) | 상태 | 근거 / WBS |
|---|---|---|---|
| SCR-009 Live | `/` | `MOCK_WIRED` | `getLiveOrders` · 완료/취소 stub · AsyncState/Confirm · 페이징 UI 잔여 · WBS2-035 |
| SCR-022 Dashboard | `/dashboard` | `MOCK_WIRED` | `useDashboard` · 최근주문 ← `getDashboard().recentOrders` · 전주 대비 일부 정적 · WBS2-034 |
| SCR-010 Orders | `/orders` | `MOCK_WIRED` | `useOrdersQuery` · 목록 표시/필터 · 환불/영수증 Confirm · **목록 상태변경 UI 없음** · 필터 고도화 잔여 · WBS2-036 |
| SCR-011 Sold-out | `/sold-out` | `MOCK_WIRED` | `useSoldOutDraft` · draft/저장 stub · 카드 2줄·카테고리 배지 · `menus.isSoldOut` 미동기화 · 검색/탭·실패 fixture TODO · WBS2-038 · Canonical `/soldOut` CONFLICT |
| SCR-016 Menus | `/menus` | `MOCK_WIRED` | `useMenusQuery` · Page=조립(`MenuListPanel`+Detail/Edit) · `IngredientSelectModal` · 저장 stub · WBS2-039 |
| SCR-017 Menu edit | `/menus/new\|edit` | `MOCK_WIRED` | Edit는 우측 패널 모드 wrapper (별도 빈 페이지 아님) |
| SCR-018 Payments | `/payment-methods` | `MOCK_WIRED` | Figma **4종** card/kakao/naver/zero · 토글/저장 · 실패 fixture·점검 뱃지 TODO · WBS2-040 |
| SCR-019 Sales | `/sales` | `MOCK_WIRED` | `useSalesQuery` · 기간 탭 · `AdminDatePicker` range · WBS2-041 |
| SCR-020 Monthly | `/sales/monthly` | `MOCK_WIRED` | `useSalesQuery` · 월 네비 · DatePicker · WBS2-042 |
| SCR-021 Daily | `/sales/daily` | `MOCK_WIRED` | `useSalesQuery` · `AdminDatePicker` single · WBS2-043 |
| SCR-015 Login | `/login` | `UI_ONLY` / EXCLUDED 성격 | Unauthorized 등 P2 |

| 자산 | 상태 | 비고 |
|---|---|---|
| `AdminLayout` / `AdminSidebar` | `IMPLEMENTED` | **1920×1080 캔버스 + viewport scale** |
| `adminMockRepository.js` | `MOCK_WIRED` | Live·주문·품절·메뉴·결제·매출·대시보드 Page 사용 |
| `asak-admin-data.json` | `MOCK_WIRED` | 결제수단 4종 계약 반영 |
| `hooks/*` (orders/soldOut/payment/dashboard/menus/sales/pagination) | `MOCK_WIRED` / `PARTIAL` | 실패 fixture·실 API 미연결 |
| `api/*`, `adapters/*` | `PLACEHOLDER` / `PARTIAL` | Backend **BLOCKED** |
| Shared | `PARTIAL` | `AdminAsyncState` · `AdminConfirmDialog` P1 · State QA evidence TODO (WBS2-044) |

---

## Backend (`ASAK-back`)

| 계층 | 상태 |
|---|---|
| `GET /api/health` | `IMPLEMENTED` |
| 도메인 Controller/Service/Entity | `MISSING` |
| JPA / migration | `MISSING` |
| 프론트 실연동 | `BLOCKED` (WBS2-058~060) |

---

## 화면 ID 재정렬 (2026-07-20)

| ID | 의미 |
|---|---|
| SCR-020 | **관리자 월별 매출** (구 영수증 → SCR-023) |
| SCR-021 | **관리자 일별 매출** (구 멤버십 → SCR-024) |
| SCR-022 | 관리자 대시보드 |
| SCR-023 | 영수증 (Future) |
| SCR-024 | 멤버십/쿠폰 (Future) |

---

## 다음 작업 (문서 → 코드)

1. Kiosk: 결제 mock 연결 · 한도 toast · 타임아웃 (WBS2-024, 026~030) · **결제수단 개수(8 vs Admin 4) 계약 재확인**  
2. Admin: 실패 fixture · 품절↔`menus.isSoldOut` 동기화 · 주문 필터 고도화 · Live 페이징 · P2 polish · State/QA evidence (`WBS2-044~045`)  
3. Canonical path/상수 정렬 (DECIDED_PENDING)  
4. Backend P5 세로 슬라이스 (WBS2-046+) — **실연동 BLOCKED**

### Admin 실행 순서 메모 (2026-07-21 ~ 2026-07-23 진척 반영)

- ~~주문 운영(`WBS2-035~036`)~~ → Live·주문 목록 **1차 연결**. 목록 **상태변경 UI는 의도적으로 없음**. `037` PATCH/TTS·필터 고도화 잔여.
- ~~운영 설정(`WBS2-038~040`)~~ → 품절·결제수단(4종)·메뉴 **1차 연결**. 실패 fixture·실 저장 API 잔여.
- ~~조회성(`034`, `041~043`)~~ → Dashboard·매출 3화면 **1차 연결** (DatePicker 포함).
- `WBS2-044` Shared Async/Confirm **P1 적용** → State QA evidence·`045` QA 실행은 남음.
- 브랜치: `feature/admin-mock-figma-parity` (main 미머지). **1차 mock ≠ DONE.**
