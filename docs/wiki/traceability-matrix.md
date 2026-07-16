# Traceability Matrix

> Baseline matrix. Links are documentary mappings; no DevCopilot relation was fabricated because the MCP does not expose link mutation.

| Requirement | Scenario | Screen | API target | DB target | WBS 2.0 workstream | QA |
|---|---|---|---|---|---|---|
| FWD-ORDER-001 | SC-014 | SCR-001, SCR-005 | POST `/api/kiosk/orders` | orders, order_item | Kiosk data I/O | TC-001 |
| FWD-MENU-001 | SC-001 | SCR-003 | GET `/api/kiosk/menuList` | menu, category | Kiosk data I/O | TC-002 |
| FWD-MENU-004 | SC-010 | SCR-004 | menu detail contract | allergen, ingredient_allergen | Kiosk UI | Allergy QA (new) |
| FWD-CART-002 | SC-009 | SCR-005 | order validation | order_item | Kiosk Store | Cart limit QA (new) |
| FWD-PAY-002 | SC-005 | SCR-007, SCR-012 | POST `/api/kiosk/payments` | payment | Kiosk payment | TC-004 |
| FWD-SYS-001 | SC-012 | SCR-013 | client state | — | Kiosk timeout | TC-007 |
| LMIS-MENU-001 | SC-007 | SCR-011 | PATCH `/api/admin/soldOut` | menu/ingredient/option policy | Admin + backend | TC-006 |
| LMIS-ORDER-001/003 | SC-008 | SCR-009, SCR-010 | Admin order API (TBD) | orders, payment | Admin + backend | TC-014 |
| LMIS-ORDER-005 | SC-018 | SCR-019–021 | sales API (TBD) | sales views | Admin sales | Sales QA (new) |
