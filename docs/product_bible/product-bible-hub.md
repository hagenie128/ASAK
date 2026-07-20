# Product Bible — 읽기 허브

> **Pack 12개·문서 200개+를 번호 순서로 읽지 마세요.**  
> 이 페이지 **한 곳**에서 역할별로 바로 엽니다.  
> 코드 현실: [baseline](../wiki/current-status-baseline.md) · 구현 작업 카드: [implementation_guide](../implementation_guide/00-start-here.md)

---

## 1. 지금 뭘 하고 있나? (30초 선택)

| 하고 있는 일 | 먼저 열 문서 |
|---|---|
| **키오스크 주문·장바구니·결제** | [Pack 2 README](02_Order_Cart_Payment/README.md) → 아래 §2 |
| **메뉴·옵션·품절** | [Pack 3 README](03_Menu_Inventory_SoldOut/README.md) → §3 |
| **화면(SCR) 하나 고치기** | [SCREEN_REGISTRY](07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md) → §4 |
| **관리자 주문·품절·대시보드** | [Pack 4 README](04_Dashboard_Sales_Kitchen_TTS/README.md) · SCR-009~022 (§4) |
| **타임아웃·오류·접근성** | [Pack 5 README](05_Accessibility_Timeout_Error/README.md) |
| **API·DTO·엔지니어링 규칙** | [Pack 6 README](06_Engineering_Bible/README.md) |
| **컴포넌트·Figma 매핑** | [FIGMA↔React Map](08_Component_Bible/docs/08-components/04-maps/FIGMA_REACT_COMPONENT_MAP.md) |
| **백엔드 슬라이스 구현** | [Backend Roadmap](11_Backend_Implementation/docs/12-backend-implementation/00-plan/BACKEND_IMPLEMENTATION_ROADMAP.md) |
| **프론트 구현·라우트** | [Frontend Roadmap](12_Frontend_Implementation/docs/13-frontend-implementation/00-plan/FRONTEND_IMPLEMENTATION_ROADMAP.md) |
| **정본·원칙 충돌** | [CANONICAL_SOURCE](01_Foundation/docs/00-product-bible/CANONICAL_SOURCE.md) · [DECISION_LOG](01_Foundation/docs/00-product-bible/DECISION_LOG.md) |

---

## 2. MVP 필수 링크 (15개만)

스프린트에서 **이것만** 먼저 읽어도 됩니다.

### 원칙·정본
- [Product Principles](01_Foundation/docs/00-product-bible/PRODUCT_PRINCIPLES.md)
- [Canonical Source](01_Foundation/docs/00-product-bible/CANONICAL_SOURCE.md)
- [Screen Registry](07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md)

### 키오스크 흐름 (정책)
- [Cart Architecture](02_Order_Cart_Payment/docs/09-features/cart/CART_ARCHITECTURE.md)
- [Order Flow](02_Order_Cart_Payment/docs/09-features/order/ORDER_FLOW_AND_STATE.md)
- [Payment Flow](02_Order_Cart_Payment/docs/09-features/payment/PAYMENT_FLOW_AND_STATE.md)
- [Menu API Contract](03_Menu_Inventory_SoldOut/docs/09-features/menu/MENU_API_CONTRACT.md)
- [Sold-out Management](03_Menu_Inventory_SoldOut/docs/09-features/sold-out/SOLD_OUT_MANAGEMENT.md)

### 화면 정본 (대표 SCR)
- [SCR-003 Menu List](07_Screen_Bible/docs/07-screens/SCR-003-KIOSK-MENU-LIST.md)
- [SCR-004 Menu Detail](07_Screen_Bible/docs/07-screens/SCR-004-KIOSK-MENU-DETAIL.md)
- [SCR-005 Cart](07_Screen_Bible/docs/07-screens/SCR-005-KIOSK-CART.md)
- [SCR-007 Payment](07_Screen_Bible/docs/07-screens/SCR-007-KIOSK-PAYMENT.md)
- [SCR-011 Sold-out Admin](07_Screen_Bible/docs/07-screens/SCR-011-ADMIN-SOLD-OUT-MANAGEMENT.md)

### 공통 상태
- [Timeout Session](05_Accessibility_Timeout_Error/docs/09-features/timeout-session/TIMEOUT_SESSION_ARCHITECTURE.md)
- [Error Recovery](05_Accessibility_Timeout_Error/docs/09-features/error-recovery/ERROR_RECOVERY_ARCHITECTURE.md)

---

## 3. 키오스크 주문 — 한 줄 지도

```text
SCR-001 Home → SCR-003 Menu → SCR-004 Detail → SCR-005 Cart
  → Order API → SCR-007 Payment → SCR-008 Complete
```

| 단계 | 화면 (Pack 7) | 정책 (Pack 2·3) |
|---|---|---|
| 홈 | [SCR-001](07_Screen_Bible/docs/07-screens/SCR-001-KIOSK-HOME.md) | — |
| 메뉴 | [SCR-003](07_Screen_Bible/docs/07-screens/SCR-003-KIOSK-MENU-LIST.md) | [Menu Architecture](03_Menu_Inventory_SoldOut/docs/09-features/menu/MENU_ARCHITECTURE.md) |
| 상세 | [SCR-004](07_Screen_Bible/docs/07-screens/SCR-004-KIOSK-MENU-DETAIL.md) | [Menu Detail Flow](03_Menu_Inventory_SoldOut/docs/09-features/menu/MENU_DETAIL_FLOW_AND_VALIDATION.md) |
| 장바구니 | [SCR-005](07_Screen_Bible/docs/07-screens/SCR-005-KIOSK-CART.md) | [Cart State](02_Order_Cart_Payment/docs/09-features/cart/CART_STATE_AND_EVENT_FLOW.md) |
| 결제 | [SCR-007](07_Screen_Bible/docs/07-screens/SCR-007-KIOSK-PAYMENT.md) | [Payment API](02_Order_Cart_Payment/docs/09-features/payment/PAYMENT_API_CONTRACT.md) |
| 완료 | [SCR-008](07_Screen_Bible/docs/07-screens/SCR-008-KIOSK-COMPLETE.md) | [Order API](02_Order_Cart_Payment/docs/09-features/order/ORDER_API_CONTRACT.md) |
| 결제 오류 | [SCR-012](07_Screen_Bible/docs/07-screens/SCR-012-KIOSK-PAYMENT-ERROR.md) | [Error Copy Map](05_Accessibility_Timeout_Error/docs/09-features/error-recovery/ERROR_CODE_AND_COPY_MAP.md) |
| 타임아웃 | [SCR-013](07_Screen_Bible/docs/07-screens/SCR-013-KIOSK-TIMEOUT.md) | [Session Reset](05_Accessibility_Timeout_Error/docs/09-features/timeout-session/SESSION_RESET_POLICY.md) |

---

## 4. SCR 전체 (Pack 7 — 화면 정본)

| SCR | 문서 | MVP |
|---|---|---|
| 001 | [Kiosk Home](07_Screen_Bible/docs/07-screens/SCR-001-KIOSK-HOME.md) | ✅ |
| 003 | [Menu List](07_Screen_Bible/docs/07-screens/SCR-003-KIOSK-MENU-LIST.md) | ✅ |
| 004 | [Menu Detail](07_Screen_Bible/docs/07-screens/SCR-004-KIOSK-MENU-DETAIL.md) | ✅ |
| 005 | [Cart](07_Screen_Bible/docs/07-screens/SCR-005-KIOSK-CART.md) | ✅ |
| 007 | [Payment](07_Screen_Bible/docs/07-screens/SCR-007-KIOSK-PAYMENT.md) | ✅ |
| 008 | [Complete](07_Screen_Bible/docs/07-screens/SCR-008-KIOSK-COMPLETE.md) | ✅ |
| 009 | [Live Order](07_Screen_Bible/docs/07-screens/SCR-009-ADMIN-LIVE-ORDER-BOARD.md) | ✅ |
| 010 | [Order Mgmt](07_Screen_Bible/docs/07-screens/SCR-010-ADMIN-ORDER-MANAGEMENT.md) | ✅ |
| 011 | [Sold-out](07_Screen_Bible/docs/07-screens/SCR-011-ADMIN-SOLD-OUT-MANAGEMENT.md) | ✅ |
| 012 | [Pay Error](07_Screen_Bible/docs/07-screens/SCR-012-KIOSK-PAYMENT-ERROR.md) | ✅ |
| 013 | [Timeout](07_Screen_Bible/docs/07-screens/SCR-013-KIOSK-TIMEOUT.md) | ✅ |
| 014 | [Accessibility](07_Screen_Bible/docs/07-screens/SCR-014-KIOSK-ACCESSIBILITY.md) | ✅ |
| 015 | [Admin Login](07_Screen_Bible/docs/07-screens/SCR-015-ADMIN-LOGIN.md) | 후순위 |
| 016 | [Menu Mgmt](07_Screen_Bible/docs/07-screens/SCR-016-ADMIN-MENU-MANAGEMENT.md) | ✅ |
| 018 | [Payment Settings](07_Screen_Bible/docs/07-screens/SCR-018-ADMIN-PAYMENT-METHOD-SETTINGS.md) | ✅ |
| 019 | [Sales Summary](07_Screen_Bible/docs/07-screens/SCR-019-ADMIN-SALES-SUMMARY.md) | ✅ |
| 020 | [Monthly Sales](07_Screen_Bible/docs/07-screens/SCR-020-ADMIN-MONTHLY-SALES.md) | ✅ |
| 021 | [Daily Sales](07_Screen_Bible/docs/07-screens/SCR-021-ADMIN-DAILY-SALES.md) | ✅ |
| 022 | [Dashboard](07_Screen_Bible/docs/07-screens/SCR-022-ADMIN-DASHBOARD.md) | ✅ |
| 023 | [Receipt](07_Screen_Bible/docs/07-screens/SCR-023-RECEIPT-OUTPUT.md) | FUTURE |
| 024 | [Membership](07_Screen_Bible/docs/07-screens/SCR-024-MEMBERSHIP---COUPON.md) | FUTURE |

정본 ID 표: [SCREEN_REGISTRY](07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md)

---

## 5. Pack 1~12 — 전체 목록 (깊이 들어갈 때)

Pack README에 **파일별 링크 표**를 넣었습니다. Pack 번호 순서대로 읽을 필요 없습니다.

| Pack | README | 주제 |
|---|---|---|
| 01 | [Foundation](01_Foundation/README.md) | 원칙·ADR·정본 |
| 02 | [Order/Cart/Payment](02_Order_Cart_Payment/README.md) | 주문·장바구니·결제 |
| 03 | [Menu/Sold-out](03_Menu_Inventory_SoldOut/README.md) | 메뉴·품절 |
| 04 | [Dashboard/Kitchen/TTS](04_Dashboard_Sales_Kitchen_TTS/README.md) | 관리자 운영 |
| 05 | [A11y/Timeout/Error](05_Accessibility_Timeout_Error/README.md) | 공통 상태 |
| 06 | [Engineering](06_Engineering_Bible/README.md) | FE/BE/DB/API 규칙 |
| 07 | [Screen](07_Screen_Bible/README.md) | SCR 정본 |
| 08 | [Component](08_Component_Bible/README.md) | 컴포넌트 |
| 09 | [QA](09_QA_Bible/README.md) | 테스트 |
| 10 | [AI Master](10_AI_Master_Bible/README.md) | AI 거버넌스 |
| 11 | [Backend Impl](11_Backend_Implementation/README.md) | 백엔드 구현 |
| 12 | [Frontend Impl](12_Frontend_Implementation/README.md) | 프론트 구현 |

---

## 6. 왜 Pack이 많나 (읽기 팁)

| 겉으로 보이는 문제 | 실제 읽는 법 |
|---|---|
| `01_Foundation/docs/00-product-bible/...` 깊은 폴더 | **이 허브** 또는 Pack README 표에서 **한 번 클릭** |
| Pack 12개 | **역할 1개**만 고르고 해당 Pack README만 |
| UPPER_SNAKE 파일명 | 본문 H1이 한국어/영문 제목 — **파일명은 ID**로만 보면 됨 |
| Bible vs implementation_guide | Bible=**정책** · guide=**작업 카드** · [app-implementation-hub](../planning/app-implementation-hub.md) |

**FUTURE / MVP 밖:** [future-scope](../_archive/wiki-secondary/future-scope.md) · SCR-023·024

---

## 7. Canonical 충돌 시

1. [Canonical Source](01_Foundation/docs/00-product-bible/CANONICAL_SOURCE.md)
2. [governance/canonical-contract-decisions](../governance/canonical-contract-decisions-2026-07-16.md)
3. [document-code-gap-report](../architecture/document-code-gap-report-2026-07-16.md)
