# DevCopilot Sync Report

> 기준일: 2026-07-16 · Status: IN_PROGRESS

## Supported MCP changes

Requirements, scenarios, screens, WBS tasks, API specs, DB tables/columns, QA test cases, and bug reports can be read or updated.

## Applied changes

| Area | Before | After | Change |
|---|---:|---:|---|
| Requirements | DONE 3 / TODO 47 / EXCLUDED 7 | TODO 33 / IN_PROGRESS 11 / EXCLUDED 13 | Removed unsupported DONE; recorded existing Kiosk scaffolds as IN_PROGRESS; moved explicit future scope out of MVP |
| Scenarios | DRAFT 24 | DRAFT 21 / ARCHIVED 3 | Receipt, membership, and QR scenarios preserved as Future Scope |
| Screens | 21 | 24 | SCR-020/021 migrated to Monthly/Daily Sales; SCR-022 Dashboard and archived SCR-023/024 added |
| WBS | 65 | 168 records | Legacy and accidental duplicate records preserved as 67 EXCLUDED entries; 64 active WBS2 entries created |
| QA | TODO 16 | TODO 16 | No PASS claim; Future Scope tests retitled only |
| Bugs | 0 | 0 | No test execution occurred |

## API mismatch record

| API ID | Existing DevCopilot path | Latest target path | Implementation evidence | Decision needed | Status |
|---|---|---|---|---|---|
| API-002/003/004 | `/api/menus/**` | `/api/kiosk/menuList`, `/api/kiosk/menuDetail/{menuId}` | No backend menu API | Adapter/contract selection | TODO |
| API-005 | `/api/orders` | `/api/kiosk/orders` | No backend order API | Canonical path approval | TODO |
| API-006 | `/api/payments` | `/api/kiosk/payments` | No backend payment API | Canonical path approval | TODO |
| API-009 | `/api/admin/sold-out-items` | `/api/admin/soldOut` | No backend sold-out API | Canonical path approval | TODO |

The MCP exposes API creation/read but no API update/archive operation. This table is the authoritative non-destructive reconciliation record until that capability is available.

## Dashboard recalculation

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Requirement implementation | 5.3% | 0.0% | Three unsupported DONE records were corrected; IN_PROGRESS is not treated as DONE |
| Traceability | 87.7% | 87.7% | No explicit link mutation is exposed by MCP |
| WBS progress | 9.2% | 5.4% | Legacy/duplicate cleanup and WBS2 creation triggered recalculation; this is not a delivery regression |
| QA pass | 0.0% | 0.0% | No execution evidence |
| Open bug | 0 | 0 | No test execution occurred |

## MCP_UNSUPPORTED

- Native backup/export
- Member management
- Kanban board management
- Wiki/checklist management
- Explicit traceability-link mutation

## Safety controls

- Local baseline snapshot precedes all mutation.
- No source-code, Figma, kiosk remote, pull/reset/rebase, or destructive delete operation is in scope.
- Legacy duplicate WBS records are preserved and marked through status/title notes only.
- API/DB specification presence is not used as implementation evidence.
