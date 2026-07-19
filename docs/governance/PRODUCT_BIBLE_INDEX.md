# Product Bible Index

> **입구:** [START_HERE](../START_HERE.md) · **얇은 안내(MVP Pack):** [product_bible/README.md](../product_bible/README.md)  
> Pack **README만** 먼저 읽고, 세부 문서는 필요할 때만. `_archive`는 구현 기준 제외.  
> 분석 기준: `docs/product_bible` Pack 1~12.

## 참조 우선순위

충돌 시 최신 Product Bible의 Decision/ADR, Screen Registry, Feature/API 계약, 최신 Figma, 실제 코드 순으로 판단한다. 실제 코드가 계약과 달라도 이 보고서에서는 수정하지 않고 차이로 기록한다.

| Pack | 목적 | 핵심 문서 | 주 사용 시점 |
|---|---|---|---|
| 01 Foundation | 제품 원칙·정본·결정 | `CANONICAL_SOURCE`, `DECISION_LOG`, ADR | 모든 작업 시작 전 |
| 02 Order/Cart/Payment | 고객 주문 흐름과 결제 상태 | Order/Cart/Payment API·state 문서 | 주문 기능 |
| 03 Menu/Inventory/Sold-out | 메뉴·재료·옵션·품절 정책 | `MENU_API_CONTRACT`, `SOLD_OUT_MANAGEMENT` | 메뉴/관리자 품절 |
| 04 Dashboard/Sales/Kitchen/TTS | 관리자 운영·매출·주문 처리 | Kitchen/Sales/TTS architecture | 관리자 운영 |
| 05 Accessibility/Timeout/Error | 이탈 복구와 접근성 | timeout, error, accessibility 문서 | 키오스크 공통 상태 |
| 06 Engineering | 기술·명명·저장소·API 규칙 | architecture, naming, API rules | 구현 설계/리뷰 |
| 07 Screen | 화면 ID, 라우트, 상태 | `SCREEN_REGISTRY`, SCR 문서 | 화면 구현 전 |
| 08 Component | Figma-React 컴포넌트 매핑 | ownership/map/checklist | 컴포넌트 재사용 판단 |
| 09 QA | 기능/회귀/데모 검증 | QA strategy, smoke/regression | 구현 완료 전 |
| 10 AI Master | AI 작업 거버넌스와 컨텍스트 | source-of-truth, handoff | AI 작업 시작/인수인계 |
| 11 Backend Implementation | Backend 수직 슬라이스 순서 | roadmap, vertical slice, entity/order/payment | ASAK-back 구현 |
| 12 Frontend Implementation | 기존 React 보존·확장 | audit, priority, route/state/API integration | Kiosk/Admin 구현 |

## 기능별 읽는 순서

1. 공통: Pack 01 → 06 → 07 → 08 → 해당 기능 Pack → 11 또는 12 → 09.
2. Kiosk 메뉴/주문: 01 → 07(SCR-001/003/004/005/007/008) → 02 → 03 메뉴 → 12 → 11 → 09.
3. Admin 운영: 01 → 07(SCR-022/009/010/011/016/018/019) → 03/04 → 12 → 11 → 09.
4. AI는 Pack 10의 `SOURCE_OF_TRUTH`와 Pack 01의 `CANONICAL_SOURCE`를 먼저 읽고, 이후 해당 기능 문서를 읽는다.

## MVP 경계

MVP는 메뉴 조회, 메뉴 상세·옵션 검증, 장바구니, 주문 생성, 결제 승인/실패 복구, 관리자 주문 상태 변경 및 기본 품절/매출이다. 영수증 출력, 멤버십/쿠폰, 고급 접근성, WebSocket, 외부 TTS, 고급 차트·영양 재계산은 `FUTURE_SCOPE`로 유지한다.
