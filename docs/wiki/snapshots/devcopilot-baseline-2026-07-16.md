# DevCopilot Baseline Snapshot — 2026-07-16

> Source: DevProject Hub MCP, workspace `2` (`ASAK 키오스크 프로젝트`). Captured before any DevCopilot mutation on 2026-07-16. This is a local audit snapshot because the MCP exposes no Backup/Export operation.

## Dashboard

| Metric | Value |
|---|---:|
| Requirements implementation | 5.3% |
| Traceability | 87.7% |
| WBS progress | 9.2% |
| QA pass rate | 0.0% |
| Open bugs | HIGH 0 / MEDIUM 0 / LOW 0 |

## Inventory

| Area | Count | Status breakdown |
|---|---:|---|
| Requirement | 57 | DONE 3 / TODO 47 / EXCLUDED 7 |
| Scenario | 24 | DRAFT 24 |
| Screen | 21 | WIREFRAME 19 / ARCHIVED 2 |
| WBS | 65 | DONE 6 / TODO 59 |
| API | 39 | status field not exposed |
| DB model | 30 | 26 tables / 4 views |
| QA | 16 | TODO 16 |
| Bug | 0 | — |

## Requirement IDs by status

- DONE: `FWD-MENU-004`, `FWD-MENU-015`, `KSD-ARCH-001`
- EXCLUDED: `ARCHIVE-LMIS-ORDER-005`, `FWD-CART-003`, `KSD-MEMBER-001`, `LMIS-AUTH-001`, `RTOS-DEVICE-004`, `RTOS-DEVICE-005`, `RTOS-SYS-001`
- TODO: all remaining requirement IDs in the workspace.

## Scenario IDs

`SC-001` through `SC-024` are all `DRAFT`.

## Screen IDs

- ARCHIVED: `SCR-002` (merged order-type selection), `SCR-006` (merged order confirmation)
- WIREFRAME: `SCR-001`, `SCR-003`–`SCR-005`, `SCR-007`–`SCR-021`
- Missing from the latest registry: `SCR-022`, `SCR-023`, `SCR-024`

## WBS identity snapshot

- Internal WBS record IDs are MCP integers; external identifiers are `task_id`.
- 28 external task IDs are duplicated: `WBS-001`–`WBS-028` except no separate `WBS-029`/`030` duplicate in this baseline, plus the individual IDs listed below.
- Exact duplicate groups: `WBS-001`, `WBS-002`, `WBS-003`, `WBS-004`, `WBS-005`, `WBS-006`, `WBS-007`, `WBS-008`, `WBS-009`, `WBS-010`, `WBS-011`, `WBS-012`, `WBS-013`, `WBS-014`, `WBS-015`, `WBS-016`, `WBS-017`, `WBS-018`, `WBS-019`, `WBS-020`, `WBS-021`, `WBS-022`, `WBS-023`, `WBS-024`, `WBS-025`, `WBS-026`, `WBS-027`, `WBS-028`.
- DONE records: `WBS-001`, `WBS-003`, `WBS-004`, `WBS-023`, `WBS-024`, `WBS-026` (all require evidence re-audit; see current status baseline).

## API identity snapshot

| Legacy API ID | Method | Path |
|---|---|---|
| API-001 | GET | `/api/categories` |
| API-002 | GET | `/api/menus` |
| API-003 | GET | `/api/menus/{menuId}` |
| API-004 | GET | `/api/menus/{menuId}/options` |
| API-005 | POST | `/api/orders` |
| API-006 | POST | `/api/payments` |
| API-007 | GET | `/api/admin/orders` |
| API-008 | PATCH | `/api/admin/orders/{orderId}/status` |
| API-009 | PATCH | `/api/admin/sold-out-items` |
| API-010–020 | mixed | legacy admin, cart, accessibility, membership, receipt and device paths |
| Internal records 120–138 | mixed | duplicate `/api/v1/**` data-model API set |

## DB model names

Tables: `allergen`, `category`, `code_group`, `common_code`, `ingredient`, `ingredient_allergen`, `item_exclusion`, `menu`, `menu_ingredient`, `menu_nutrition`, `menu_option_group_legacy_20260710`, `menu_option_legacy_20260710`, `menu_option_override`, `menu_option_policy`, `menu_tag`, `option_group`, `option_item`, `option_item_component`, `option_policy`, `option_policy_item`, `order_item`, `order_item_option`, `orders`, `payment`, `payment_method_config`, `tag`.

Views: `vw_sales_daily`, `vw_sales_hourly`, `vw_top_menu_daily`, `vw_top_menu_hourly`.

## QA and bug snapshot

- `TC-001`–`TC-016`: all `TODO`; no PASS or execution evidence.
- MCP has no duplicate QA ID in its current list. A duplicate `TC-001` exists in the local Notion export and remains an audit candidate.
- Bug reports: none.

## MCP capability gap

`MCP_UNSUPPORTED`: native backup/export, member administration, Kanban board, Wiki/checklist, and explicit traceability-link mutations.
