# 추적성(Traceability) 매트릭스

> Baseline 매트릭스. 링크는 문서 매핑이며, MCP가 link mutation을 노출하지 않아 DevCopilot relation을 만들지 않았습니다.

| 요구사항 | 시나리오 | 화면 | API 목표 | DB 목표 | WBS 2.0 작업 흐름 | QA |
|---|---|---|---|---|---|---|
| FWD-ORDER-001 | SC-014 | SCR-001, SCR-005 | POST `/api/kiosk/orders` | orders, order_item | 키오스크 데이터 I/O | TC-001 |
| FWD-MENU-001 | SC-001 | SCR-003 | GET `/api/kiosk/menuList` | menu, category | 키오스크 데이터 I/O | TC-002 |
| FWD-MENU-004 | SC-010 | SCR-004 | menu detail contract | allergen, ingredient_allergen | 키오스크 UI | Allergy QA (신규) |
| FWD-CART-002 | SC-009 | SCR-005 | order validation | order_item | 키오스크 Store | Cart limit QA (신규) |
| FWD-PAY-002 | SC-005 | SCR-007, SCR-012 | POST `/api/kiosk/payments` | payment | 키오스크 결제 | TC-004 |
| FWD-SYS-001 | SC-012 | SCR-013 | client state | — | 키오스크 타임아웃 | TC-007 |
| LMIS-MENU-001 | SC-007 | SCR-011 | PATCH `/api/admin/soldOut` | menu/ingredient/option policy | Admin + 백엔드 | TC-006 |
| LMIS-ORDER-001/003 | SC-008 | SCR-009, SCR-010 | Admin order API (TBD) | orders, payment | Admin + 백엔드 | TC-014 |
| LMIS-ORDER-005 | SC-018 | SCR-019–021 | sales API (TBD) | sales views | Admin 매출 | Sales QA (신규) |
