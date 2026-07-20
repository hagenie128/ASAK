# Current Implementation Map

> 기준일: **2026-07-20** · **코드 실측** 정본.  
> 문서 입구: [START_HERE](../START_HERE.md)  
> 이전 07-16 버전은 Cart/Admin을 MISSING으로 적어 **과소평가**되어 폐기 수준으로 대체됨.  
> Canonical(미코드 반영): [canonical-contract-decisions-2026-07-16.md](../governance/canonical-contract-decisions-2026-07-16.md)  
> 일일 baseline: [current-status-baseline.md](../wiki/current-status-baseline.md)  
> WBS: [wbs-v2-2026-07-16.md](../wiki/wbs-v2-2026-07-16.md) · [wbs-status-notes.md](../wiki/wbs-status-notes.md)

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
| SCR-009 Live | `/` | `UI_ONLY` | Figma 정적 · WBS2-035 |
| SCR-022 Dashboard | `/dashboard` | `UI_ONLY` | WBS2-034 |
| SCR-010 Orders | `/orders` | `UI_ONLY` | WBS2-036 · Detail 라우트 미연결 |
| SCR-011 Sold-out | `/sold-out` | `UI_ONLY` | WBS2-038 · Canonical `/soldOut` CONFLICT |
| SCR-016 Menus | `/menus` | `UI_ONLY` | WBS2-039 |
| SCR-017 Menu edit | `/menus/new\|edit` | `PLACEHOLDER` | |
| SCR-018 Payments | `/payment-methods` | `UI_ONLY` | disabled · WBS2-040 |
| SCR-019 Sales | `/sales` | `UI_ONLY` | WBS2-041 |
| SCR-020 Monthly | `/sales/monthly` | `UI_ONLY` | WBS2-042 |
| SCR-021 Daily | `/sales/daily` | `UI_ONLY` | WBS2-043 |
| SCR-015 Login | `/login` | `UI_ONLY` / EXCLUDED 성격 | |

| 자산 | 상태 | 비고 |
|---|---|---|
| `AdminLayout` / `AdminSidebar` | `IMPLEMENTED` | |
| `adminMockRepository.js` | `MOCK_READY` | **Page 연동 0** |
| `asak-admin-data.json` | `MOCK_READY` | |
| `api/*`, `hooks/*`, `adapters/*` | `PLACEHOLDER` | |
| 공통 admin 컴포넌트 일부 | `PARTIAL` | DataTable 등은 placeholder 혼재 |

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

1. Kiosk: 결제 mock 연결 · 한도 toast · 타임아웃 (WBS2-024, 026~030)  
2. Admin: `adminMockRepository` → Page 바인딩 (WBS2-034~043)  
3. Canonical path/상수 정렬 (DECIDED_PENDING)  
4. Backend P5 세로 슬라이스 (WBS2-046+)
