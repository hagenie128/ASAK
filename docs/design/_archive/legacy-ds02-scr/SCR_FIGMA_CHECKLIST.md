# SCR × Figma 작업 체크리스트 (태블릿 세로)

> **kiosk_design** · 834×1194 portrait · [`figma-links.template.json`](../tools-plugins/figma-links.template.json)
> 팀 파일: [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design)  
> 동기화: `python asak-data/scripts/sync_figma_links.py --all` (FIGMA_TOKEN → Git·Notion·DevCopilot)  
> Notion 정본: [Figma 가이드 + SCR×Figma](https://app.notion.com/p/39451ef04f0b81849dc7d81f8106b5ad) · 화면 목록: [04. 화면 설계 SCR DB](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8)

## 2026-07-06 병합·6단계 요약

| 항목 | 내용 |
|------|------|
| DS | **DS-02 Modern Minimal** 프로덕션 |
| SCR-002 | → SCR-001「홈 (매장·포장)」**병합됨** |
| SCR-006 | → SCR-005「장바구니·주문확인」**병합됨** (컨펌 팝업) |
| 고객 흐름 | 홈(매장·포장) → 메뉴 → 옵션 → 장바구니·확인(팝업) → 결제 → 완료 (**6 UI 단계**) |
| Figma 수동 이력 | [Archive 병합 가이드](./figma-merge-scr-guide.md) |
| 플러그인 | `figma-rename-scr-plugin` — 병합됨/Archive 스킵 · `figma-create-ds02-components-plugin` |

---

| SCR | 화면명 | Page | REQ | Figma URL | 상태 | 담당 |
|-----|--------|------|-----|-----------|------|------|
| SCR-001 | 홈 (매장·포장) | Kiosk Screens | FWD-UI-002, FWD-ORDER-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=61-273 | WIREFRAME | |
| SCR-002 | 【병합됨→SCR-001】먹고가기 / 포장 선택 | Archive (02. User Flow) | FWD-ORDER-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-2 | **병합됨** | |
| SCR-003 | 메뉴 선택 | Kiosk Screens | FWD-UI-001, FWD-UI-002 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-3 | WIREFRAME | |
| SCR-004 | 메뉴 상세 / 옵션 선택 | Kiosk Screens | FWD-MENU-001~005, FWD-MENU-015, LMIS-MENU-002 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-4 | WIREFRAME | |
| SCR-005 | 장바구니·주문확인 (컨펌 팝업) | Kiosk Screens | FWD-CART-001, FWD-CART-002, FWD-ORDER-001, DEV-ORDER-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-6 | WIREFRAME | |
| SCR-006 | 【병합됨→SCR-005】주문 확인 | Archive (02. User Flow) | — | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-7 | **병합됨** | |
| SCR-007 | 결제 | Kiosk Screens | FWD-PAY-001, KSD-MEMBER-001, KSD-PAY-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-8 | WIREFRAME | |
| SCR-008 | 주문 완료 | Kiosk Screens | FWD-PAY-002, FWD-ORDER-002, KSD-PAY-002, RTOS-DEVICE-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-9 | WIREFRAME | |
| SCR-009 | 관리자 주문 관리 | Kiosk Screens | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-004 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-17 | WIREFRAME | |
| SCR-010 | 관리자 주문 상세 | Kiosk Screens | LMIS-ORDER-001~004 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-18 | WIREFRAME | |
| SCR-011 | 관리자 판매 항목 품절 관리 | Kiosk Screens | LMIS-MENU-001, LMIS-MENU-002 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-19 | WIREFRAME | |
| SCR-012 | 결제 실패 / 재시도 | Kiosk Screens | FWD-PAY-002, KSD-PAY-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-10 | WIREFRAME | |
| SCR-013 | 타임아웃 안내 / 자동 초기화 | Kiosk Screens | FWD-SYS-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-11 | WIREFRAME | |
| SCR-014 | 접근성 설정 | Kiosk Screens | FWD-UI-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-12 | WIREFRAME | |
| SCR-015 | 관리자 로그인 | Admin Screens | LMIS-AUTH-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-13 | WIREFRAME | |
| SCR-016 | 관리자 메뉴 관리 | Admin Screens | LMIS-MENU-001, LMIS-MENU-004 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-14 | WIREFRAME | |
| SCR-017 | 관리자 메뉴 등록/수정 | Admin Screens | LMIS-MENU-004, FWD-MENU-013~015 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-15 | WIREFRAME | |
| SCR-018 | 관리자 결제수단 설정 | Admin Screens | LMIS-PAY-001 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-16 | WIREFRAME | |
| SCR-019 | 관리자 매출 요약 | Admin Screens | LMIS-ORDER-005 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-23 | WIREFRAME | |
| SCR-020 | 영수증 출력 여부 선택 | Kiosk Screens | RTOS-DEVICE-001 | | WIREFRAME | |
| SCR-021 | 포인트·쿠폰 적립 | Kiosk Screens | LMIS-MEMBER-001, KSD-MEMBER-001, RTOS-DEVICE-002 | | WIREFRAME | |

**Week 5 MVP**: SCR-001~008 (+ Week 6: SCR-009~011, SCR-012 최소). SCR-020/021은 9주 후반 확장.

## Figma Page 구조 (무료 플랜 3페이지)

> **무료 플랜: 페이지 최대 3개** — Notion 유료 권장 7페이지(00~06)는 아래로 통합.

| Page | SCR | 내용 |
|------|-----|------|
| **02. User Flow** | — | 표지·팀 정보, DS-02 토큰·컴포넌트, 고객·관리자 흐름, 프로토타입, **Archive(002·006 병합됨)** |
| **03. Kiosk Screens** | SCR-001, 003~005, 007~014, 020~021 | 활성 키오스크 고객 + Day10 관리자(009~011) |
| **04. Admin Screens** | SCR-015~019 | 후반 관리자 (로그인·메뉴·결제·매출) |

유료 플랜 확장 시 00 Cover · 01 Design System · 05 Prototype · 06 Archive 분리 가능.

## DS-02 컴포넌트 (병합 화면)

| SCR | 주요 DS-02 인스턴스 |
|-----|---------------------|
| SCR-001 | `OrderTypeTile`, `TopBar` Home, `Button` Primary |
| SCR-005 | `CartLine`, `BottomBar` Confirm, `ModalConfirm`, `Stepper` |
| SCR-007 | `LoadingOverlay`, `PaymentMethod` |

플러그인: `docs/design/figma-create-ds02-components-plugin/` · 과거 상세: [Archive 병합 가이드](./figma-merge-scr-guide.md)

Frame 이름: `SCR-XXX 화면명` · wireframe: [Notion SCR 화면별 가이드](https://app.notion.com/p/39451ef04f0b81109d07c01293d73c6d)
