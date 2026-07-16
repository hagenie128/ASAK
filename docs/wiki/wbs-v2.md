# ASAK WBS 2.0

> 2026-07-16 Legacy semantic-overlap audit: the authoritative 37-record mapping is [legacy-wbs2-mapping-audit-2026-07-16.md](legacy-wbs2-mapping-audit-2026-07-16.md). `DevCopilot Dashboard WBS progress is not operationally reliable`: its observed denominator includes `EXCLUDED` records. Use active-scope progress separately for team operation.

> 기준일: 2026-07-16 · Legacy `WBS-*` records are preserved. `WBS2-*` is the execution plan and does not imply source-code completion.

## Field contract

Every task uses: WBS2 ID, Phase, Epic, Work Package, Detailed Task, Deliverable, Repository, Primary Owner, Support Owner, Review Owner, QA Owner, Dependency, Handoff Condition, Start/Target Date, Status, Definition of Done, Evidence, Requirement, Scenario, SCR, API, DB, QA, and Notes. In the compact table below, **Handoff condition + Evidence / linked scope is the row-level Definition of Done**: a row can be DONE only when its handoff condition is met and its evidence is concrete. `—` means not applicable; `NEEDS_CONFIRMATION` means evidence or ownership is not yet available.

## Execution backlog

| ID | Phase / work package | Detailed task | Repository | Primary / support | Status | Handoff condition | Evidence / linked scope |
|---|---|---|---|---|---|---|---|
| WBS2-001 | P1 Baseline / Snapshot | Preserve MCP baseline and metric values | ASAK | 하진 / — | DONE | Snapshot reviewed | Snapshot, DEV-SYS-002 |
| WBS2-002 | P1 Baseline / Repository | Record four-repository actual/target map | ASAK | 하진 / — | DONE | Map reviewed | current-status-baseline |
| WBS2-003 | P1 Baseline / Kiosk remote | Confirm ASAK-front vs ASAK-Kiosk canonical repository | ASAK-Kiosk | 나연 / 하진 | BLOCKED | Owner confirms migration plan | NEEDS_CONFIRMATION |
| WBS2-004 | P1 Baseline / Kiosk remote | Compare branch and uncommitted work before migration | ASAK-Kiosk | 나연 / 하진 | BLOCKED | Na-yeon provides evidence | NEEDS_CONFIRMATION |
| WBS2-005 | P1 Baseline / Docs | Audit requirement, scenario, screen ID conflicts | ASAK | 하진 / — | IN_PROGRESS | Findings linked | traceability-matrix |
| WBS2-006 | P1 Baseline / Docs | Separate MVP and future scope | ASAK | 하진 / — | IN_PROGRESS | Scope document reviewed | future-scope |
| WBS2-007 | P1 Baseline / API | Publish legacy-to-target API gap table | ASAK | 하진 / 나연 | IN_PROGRESS | Backend review requested | rest-api-spec |
| WBS2-008 | P1 Baseline / DB | Prepare non-destructive DB audit plan | ASAK | 하진 / 나연 | TODO | Backend artifacts available | db-audit-plan |
| WBS2-009 | P2 Design / Foundation | Verify 01-C token evidence and modes | Figma / ASAK | 하진 / — | DONE | Design QA record | DESIGN_DONE |
| WBS2-010 | P2 Design / Shared | Verify shared state components documentation | Figma / ASAK | 하진 / — | IN_PROGRESS | Cover/visual QA reviewed | DESIGN_DONE |
| WBS2-011 | P2 Design / Kiosk | Record 03-C component structure mapping | Figma / ASAK | 하진 / 나연 | IN_PROGRESS | Mapping accepted | SCR-003–008 |
| WBS2-012 | P2 Design / Admin | Record 04-C component structure mapping | Figma / ASAK | 하진 / — | IN_PROGRESS | Mapping accepted | SCR-009–022 |
| WBS2-013 | P2 Design / Kiosk screens | Record 05-C screen instance-apply gap | Figma / ASAK | 하진 / 나연 | TODO | Figma owner confirms | DESIGN_DONE only |
| WBS2-014 | P2 Design / Admin screens | Record 06-C active-work conflict boundary | Figma / ASAK | 하진 / — | IN_PROGRESS | No conflict with active agent | SCR-019–022 |
| WBS2-015 | P2 Design / Accessibility | Define high-contrast review checklist | ASAK | 하진 / 나연 | TODO | Design and implementation evidence | FWD-UI-001 |
| WBS2-016 | P2 Design / Prototype | Record prototype/instance swap as pending | Figma / ASAK | 하진 / — | TODO | Figma owner evidence | NEEDS_CONFIRMATION |
| WBS2-017 | P3 Kiosk / Route | Preserve and assess home/menu/detail routes | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Route review complete | SCR-001,003,004 |
| WBS2-018 | P3 Kiosk / Menu | Validate menu-list response adapter contract | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Contract reviewed | FWD-MENU-001, API target |
| WBS2-019 | P3 Kiosk / Detail | Validate menu-detail response adapter contract | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Contract reviewed | SCR-004 |
| WBS2-020 | P3 Kiosk / Options | Implement/verify option selection validation | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Interaction evidence | FWD-MENU-002 |
| WBS2-021 | P3 Kiosk / Allergy | Implement conditional allergy disclosure | ASAK-Kiosk | 나연 / — | TODO | UI and QA evidence | FWD-MENU-004 |
| WBS2-022 | P3 Kiosk / Store | Enforce same-menu maximum quantity 9 | ASAK-Kiosk | 나연 / — | TODO | Store test evidence | cart policy |
| WBS2-023 | P3 Kiosk / Store | Enforce cart total maximum 30 | ASAK-Kiosk | 나연 / — | TODO | Store test evidence | cart policy |
| WBS2-024 | P3 Kiosk / Store | Add limit-specific four-second toast behavior | ASAK-Kiosk | 나연 / — | TODO | Interaction evidence | cart policy |
| WBS2-025 | P3 Kiosk / Cart | Integrate cart route and item edit/delete | ASAK-Kiosk | 나연 / 하진 | TODO | SCR-005 route works | FWD-CART-002 |
| WBS2-026 | P3 Kiosk / Payment | Integrate payment-method route and display | ASAK-Kiosk | 나연 / — | TODO | SCR-007 route works | FWD-PAY-001 |
| WBS2-027 | P3 Kiosk / Payment | Handle payment failure and cart retention | ASAK-Kiosk | 나연 / — | TODO | Error-flow evidence | SCR-012, TC-004 |
| WBS2-028 | P3 Kiosk / Complete | Render order number, amount, waiting count, home action | ASAK-Kiosk | 나연 / — | TODO | Completion evidence | SCR-008 |
| WBS2-029 | P3 Kiosk / Timeout | Implement 30s, 20s warning, 10s countdown | ASAK-Kiosk | 나연 / — | TODO | Timer QA evidence | SCR-013 |
| WBS2-030 | P3 Kiosk / Timeout | Disable timeout while payment is PROCESSING | ASAK-Kiosk | 나연 / — | TODO | Payment-state evidence | SCR-013 |
| WBS2-031 | P3 Kiosk / States | Add loading, empty, error states to core flow | ASAK-Kiosk | 나연 / — | TODO | State QA evidence | FWD-MENU-001 |
| WBS2-032 | P3 Kiosk / QA | Touch target and responsive review | ASAK-Kiosk | 나연 / 하진 | TODO | QA execution | 48px target |
| WBS2-033 | P4 Admin / Route | Align route metadata with Screen Registry | ASAK-Admin | 하진 / — | TODO | Registry review | SCR-022,009–021 |
| WBS2-034 | P4 Admin / Dashboard | Implement Dashboard shell at `/` | ASAK-Admin | 하진 / — | TODO | Route and state evidence | SCR-022 |
| WBS2-035 | P4 Admin / Live order | Implement Live Order shell at `/orders/live` | ASAK-Admin | 하진 / — | TODO | Route evidence | SCR-009 |
| WBS2-036 | P4 Admin / Orders | Implement order-management list at `/orders` | ASAK-Admin | 하진 / — | TODO | Screen evidence | SCR-010 |
| WBS2-037 | P4 Admin / Orders | Implement order status update UI and TTS policy | ASAK-Admin | 하진 / — | TODO | PATCH/TTS evidence | LMIS-ORDER-003 |
| WBS2-038 | P4 Admin / Sold-out | Implement `/soldOut` page and save state | ASAK-Admin | 하진 / — | TODO | UI state evidence | SCR-011 |
| WBS2-039 | P4 Admin / Menu | Implement menu-management shell | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-016 |
| WBS2-040 | P4 Admin / Payments | Implement payment-method shell | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-018 |
| WBS2-041 | P4 Admin / Sales | Implement sales summary shell | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-019 |
| WBS2-042 | P4 Admin / Sales | Implement monthly sales screen | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-020 |
| WBS2-043 | P4 Admin / Sales | Implement daily sales screen | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-021 |
| WBS2-044 | P4 Admin / States | Add loading/empty/error/navbar states | ASAK-Admin | 하진 / — | TODO | State QA evidence | Admin common |
| WBS2-045 | P4 Admin / QA | Verify date filter, totals, and active navigation | ASAK-Admin | 하진 / 나연 | TODO | QA execution | Sales/Admin QA |
| WBS2-046 | P5 Backend / Baseline | Add persistence implementation decision record | ASAK-back | 하진 / 나연 | TODO | Team decision | DB audit |
| WBS2-047 | P5 Backend / Schema | Select schema/migration/seed approach | ASAK-back | 하진 / 나연 | TODO | Review approval | DB audit |
| WBS2-048 | P5 Backend / Menu | Implement Menu List controller/service/repository slice | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API test evidence | GET menuList |
| WBS2-049 | P5 Backend / Menu | Implement Menu Detail controller/service/repository slice | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API test evidence | GET menuDetail |
| WBS2-050 | P5 Backend / Orders | Implement order validation and transaction slice | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API test evidence | POST orders |
| WBS2-051 | P5 Backend / Payments | Implement payment approval/failure slice | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API test evidence | POST payments |
| WBS2-052 | P5 Backend / Admin | Implement sold-out slice | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | API test evidence | PATCH soldOut |
| WBS2-053 | P5 Backend / Admin | Implement order-query/status slice | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | API test evidence | Admin orders |
| WBS2-054 | P5 Backend / Sales | Define and implement sales aggregation source | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | Sum validation | sales views |
| WBS2-055 | P5 Backend / Common | Add error envelope and validation evidence | ASAK-back | NEEDS_CONFIRMATION / — | TODO | Contract tests | API common |
| WBS2-056 | P5 Backend / DB | Compare Modeler, schema, entity, FK, index, constraints | ASAK / ASAK-back | 하진 / 나연 | TODO | Audit report | db-audit-plan |
| WBS2-057 | P6 Integration / Contracts | Define adapter mapping for canonical fields | ASAK-Kiosk / ASAK-Admin | 나연 / 하진 | TODO | Contract review | totalAmount etc. |
| WBS2-058 | P6 Integration / Kiosk | Integrate kiosk against approved backend contract | ASAK-Kiosk | 나연 / — | BLOCKED | Backend contract exists | Kiosk API |
| WBS2-059 | P6 Integration / Admin | Integrate admin against approved backend contract | ASAK-Admin | 하진 / — | BLOCKED | Backend contract exists | Admin API |
| WBS2-060 | P6 Integration / Sales | Validate payment/order/time totals | All | 하진 / 나연 | BLOCKED | Sales source exists | Sales QA |
| WBS2-061 | P7 QA / Requirement | Run requirement-based tests; record actual result | All | 나연 / 하진 | TODO | Executed evidence | QA suite |
| WBS2-062 | P7 QA / Accessibility | Run high-contrast, keyboard, touch tests | All | 나연 / 하진 | TODO | Executed evidence | Accessibility QA |
| WBS2-063 | P7 QA / Regression | Run kiosk/admin integration regression | All | 나연 / 하진 | BLOCKED | Integrated app available | Regression QA |
| WBS2-064 | P8 Docs / Handoff | Sync evidence, WBS, traceability, demo checklist | ASAK | 하진 / 나연 | IN_PROGRESS | Human review | DevCopilot sync |
| WBS2-065 | P8 Release / Readiness | Check branch/PR state, repository builds, environment configuration, release checklist, and Release Candidate | All repositories | 하진 / 나연 | BLOCKED | All repository checks pass; deployment environment and responsible party are confirmed; Release Candidate is reviewed | Definition of Done: checklist approved and RC evidence attached. Evidence: [Release Checklist](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/RELEASE_CHECKLIST.md); environment/RC evidence is not yet available. |
| WBS2-066 | P8 Presentation / Demo | Prepare slides, demo order, Kiosk/Admin scenario, script, contingency, and final rehearsal | All repositories | NEEDS_CONFIRMATION / Team | TODO | Slides, script, Demo 1–5 sequence, fallback, and final rehearsal record are reviewed by the team | Definition of Done: team review complete with rehearsal evidence. Evidence: 2026-07-03 meeting assigns presentation/demo jointly to 하진·나연; [Demo Scenario](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/DEMO_SCENARIO.md). Representative Primary Owner is not agreed. |

## Ownership and review

- Primary owner is the accountable current lead; support is recorded only where planned.
- Review owner: 하진 for structure, Admin, DevCopilot and documentation; 나연 for Kiosk data I/O; shared review for integration decisions.
- QA owner: 나연 for Kiosk flows, 하진 for Admin/data-documentation flows, and both for integration QA.
- Target dates are intentionally deferred until repository migration and backend ownership are confirmed. This prevents a fabricated schedule.
