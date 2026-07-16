# DevCopilot Sync Report

## Legacy semantic-overlap follow-up (2026-07-16)

The 37 active Legacy WBS records were audited against the 64 active WBS2 records by DevCopilot internal record ID. The detailed mapping, replacement reason, and evidence are in [legacy-wbs2-mapping-audit-2026-07-16.md](legacy-wbs2-mapping-audit-2026-07-16.md).

| Metric | Before audit | After audit | Formula / reason |
|---|---:|---:|---|
| Legacy Active | 37 | 7 | 30 replaced/future Legacy records moved to EXCLUDED; no record deleted |
| WBS2 Active | 64 | 64 | WBS2 scope unchanged |
| Active total | 101 | 71 | `7 + 64` |
| DONE | 9 | 8 | Legacy Internal ID 29 had a planned Notion source and no backend evidence; it is not DONE |
| EXCLUDED | 67 | 97 | `67` duplicate records + `30` Legacy superseded/future records |
| Total WBS | 168 | 168 | No creation or deletion |
| Dashboard WBS progress | 5.4% | 4.8% | `8 DONE / 168 total records = 4.76%` |
| Operational WBS progress | n/a | 11.3% | `8 DONE / 71 Active records = 11.27%`; EXCLUDED omitted |

`DevCopilot Dashboard WBS progress is not operationally reliable`. The observed dashboard formula includes `EXCLUDED` records in its denominator. It must remain an unmodified system metric; use the operational formula above for current execution tracking.

### DONE evidence verification

| Internal ID | Task ID | Result | Evidence boundary |
|---:|---|---|---|
| 10 | WBS-001 | Retained DONE | Menu/option design/data definitions exist; no React completion claim. |
| 15 | WBS-003 | Retained DONE | Stack/role documentation exists; no feature completion claim. |
| 16 | WBS-004 | Retained DONE | ERD/API documentation exists; no backend API completion claim. |
| 27 | WBS-024 | Retained DONE | Seed bundle contains menu/ingredient/option data; app migration is still open. |
| 29 | WBS-026 | Changed to EXCLUDED | Source record was planned and no backend implementation evidence exists. |
| 31 | WBS-023 | Retained DONE | Schema constraint artifact exists; it is not a connected application migration. |
| 119 | WBS2-001 | Retained DONE | Baseline snapshot document exists. |
| 120 | WBS2-002 | Retained DONE | Repository actual/target baseline document exists. |
| 127 | WBS2-009 | Retained DONE | Design-system evidence review exists; it is design-only. |

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

## WBS reconciliation (internal record ID basis)

| Category | Record count | Meaning |
|---|---:|---|
| Before: total WBS | 65 | Original DevCopilot records |
| Before: unique Task ID | 37 | `65 - 28` duplicate extra records |
| Before: duplicate Task ID groups | 28 | Each legacy group had one additional record |
| Before: duplicate additional records | 28 | Kept as EXCLUDED, not deleted |
| New intended WBS2 | 64 | Unique active `WBS2-001`–`WBS2-064` records |
| Existing retained Active | 37 | Original representative records |
| Existing EXCLUDED / ARCHIVED | 0 / 0 | No such WBS status at the baseline |
| New EXCLUDED | 67 | 28 legacy duplicate records + 39 accidental WBS2 duplicate records |
| After: total records | 168 | `37 active legacy + 64 active WBS2 + 67 EXCLUDED` |
| After: Active | 101 | TODO 74 / DONE 9 / IN_PROGRESS 12 / BLOCKED 6 |
| After: EXCLUDED | 67 | All marked `[ARCHIVED DUPLICATE]`; no permanent deletion |
| After: other status | 0 | No WBS ARCHIVED record status |

`67` is neither a duplicate Task ID group count nor the Legacy WBS total. It is the total **additional duplicate record** count preserved as EXCLUDED. There are 28 legacy duplicate Task ID groups and zero active duplicate Task ID groups after reconciliation.

`WBS2-006` remains active because it is a documentation task that separates Future Scope; it is not Future Scope implementation work.

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
| WBS progress | 9.2% | 5.4% | `9 DONE / 168 total records = 5.36%`; MCP currently includes 67 EXCLUDED records in the denominator. This is a calculation limitation, not a delivery regression. |
| QA pass | 0.0% | 0.0% | No execution evidence |
| Open bug | 0 | 0 | No test execution occurred |

## MCP_UNSUPPORTED

- Native backup/export
- Member management
- Kanban board management
- Wiki/checklist management
- Explicit traceability-link mutation

## Metric verification limitation

`MCP_UNSUPPORTED`: the dashboard calculation formula and denominator configuration are not exposed. The observed WBS value proves that EXCLUDED is still counted (`9 / 168`), while traceability remains a system-provided 87.7% with no readable numerator/denominator. Do not alter state merely to improve those metrics.

## Safety controls

- Local baseline snapshot precedes all mutation.
- No source-code, Figma, kiosk remote, pull/reset/rebase, or destructive delete operation is in scope.
- Legacy duplicate WBS records are preserved and marked through status/title notes only.
- API/DB specification presence is not used as implementation evidence.
