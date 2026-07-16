# ASAK Current Status Baseline

> 기준일: 2026-07-16 · Source repositories and DevCopilot workspace 2 inspected. This document is an implementation baseline, not a completion claim.

## Evidence-based status

| Area | Verified state | Status |
|---|---|---|
| Figma foundation/shared/component structure | User-provided Figma evidence; no Figma MCP used | DESIGN_DONE only |
| Kiosk | React/Vite build passes; routes only cover home/menu/detail; data I/O work is active | IN_PROGRESS |
| Admin | React/Vite build passes; screens are placeholders and routes conflict with registry | TODO |
| Backend | Spring Boot 4.1.0 / Java 25 skeleton and `GET /api/health` only | TODO for business APIs |
| DB | DevCopilot model has 26 tables and 4 views; backend has no schema/entity/repository implementation | TODO |
| QA | 16 test cases, no execution evidence | TODO |

## Repository baseline

| Local folder | Current remote | Intended role | Decision |
|---|---|---|---|
| `ASAK` | `hagenie128/ASAK` | canonical docs/data/Product Bible | Current canonical documentation source |
| `ASAK-Kiosk` | `hagenie128/ASAK-front` | customer React app | BLOCKED — local remote and target `ASAK-Kiosk` differ; do not change automatically |
| `ASAK-Admin` | `hagenie128/ASAK_Admin` | administrator React app | Current canonical admin implementation target |
| `ASAK-back` | `hagenie128/ASAK-back` | Spring Boot API | Skeleton only |

## Rules applied

- Design completion never becomes implementation DONE without code, integration, and QA evidence.
- APIs and DB models documented in DevCopilot are specifications until backend evidence exists.
- Kiosk repository migration is `NEEDS_CONFIRMATION`; no pull, remote rewrite, reset, rebase, or source modification is permitted.
