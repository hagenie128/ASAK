# Repository Cleanup Inventory — 2026-07-16

> Scope: `ASAK` documentation/data repository only. `ASAK-Kiosk`, `ASAK-Admin`, `ASAK-back`, and implementation source code were not changed or included in a move plan.
>
> Status: Batch A executed only after this read-only inventory. No file has been deleted. Current DevCopilot/WBS untracked files under `docs/wiki/` are protected and excluded from all moves.

## Method and scope

The inventory used repository-wide file enumeration (excluding `.git`), SHA-256 duplicate groups, current-text reference searches, script input/output inspection, JSON manifests, and recent Git history. “Last used” below means either a current guide/README reference, an internal script dependency, or an explicitly dated historical record; it does **not** prove that an external API was recently run.

| Metric | Result |
| --- | ---: |
| Files inspected (non-`.git`) | 1,240 |
| `docs/` | 683 |
| `asak-data/` | 461 |
| `worklog/` | 47 |
| `data-pipeline/` | 23 |
| Other root/config/tool files | 26 |
| Exact duplicate hash groups | 128 |
| Additional files in those groups | 142 |
| Protected untracked DevCopilot/WBS files | 8 paths (including `docs/wiki/snapshots/`) |
| Confirmed credential signatures | 0 |

### Folder inventory

| Folder | Files | Primary role | Classification | Recommended location / rationale | Risk |
| --- | ---: | --- | --- | --- | --- |
| `docs/product_bible/01_*`–`12_*` | 212 | Product, screen, component, QA and implementation standards | KEEP_CANONICAL | Keep in place; governance index names these as current | Low |
| `docs/product_bible/_archive/` | 58 | Prior Bible pack snapshots, including Pack 3/4/7 copies | MOVE_TO_ARCHIVE | Keep under the existing `_archive` until a human approves consolidation into `docs/archive/project-history/` | Medium |
| `docs/notion/` | 288 | Notion export/reference and historic work records | NEEDS_CONFIRMATION | Keep in place now; split only after page-level ownership review | High |
| `docs/design/` | 68 | Figma guides, plugins, prompts, dated audits and assets | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION | Keep active guides/plugins; date-based completed audits may move to `docs/archive/design-audits/` | Medium |
| `docs/wiki/` | 20 tracked + 8 protected untracked paths | DevCopilot sync source and summaries | KEEP_ACTIVE_TOOL | Keep in place; never overwrite the protected current WBS work | High |
| `docs/screens/` | 6 | Screen export/source and DevCopilot payloads | NEEDS_CONFIRMATION | `screens.json` is active source; generated local-storage/import payloads need retention decision | High |
| `docs/team/` | 5 | Team decisions, sync records, dated audits | MIXED | Two concluded 2026-07-06 audits move in Batch A; current feedback/change-register documents stay | Medium |
| `docs/guides/`, `operations/`, `planning/`, `architecture/` | 21 | Team operation, setup, current plan, gap analysis | KEEP_ACTIVE_TOOL | Keep in place and link to Product Bible | Low |
| `asak-data/seed/` | 19 | Current long-name sample seed used by README and SQLite/MySQL loaders | KEEP_CANONICAL | Keep in place | High |
| `asak-data/seed-v3/` | 22 | Short-name schema migration/loader corpus | NEEDS_CONFIRMATION | Keep beside `seed` until DB owner chooses a canonical schema | High |
| `asak-data/images/menu/` | 84 | Kiosk path image assets | KEEP_CANONICAL | Keep in place; paths are consumed by seed image URLs | High |
| `asak-data/images/original/` | 84 | Source/reference menu images | KEEP_CANONICAL | Keep in place; intentional copies of deployed menu images | Medium |
| `asak-data/scripts/*.py` | 77 | Image, seed, Notion/DevCopilot, audit and migration tools | MIXED | See script inventory; do not move callers before path updates are approved | High |
| `asak-data/scripts/notion_raw/` | 151 | Saved Notion response snapshots | GENERATED_ARTIFACT / SNAPSHOT | Target `asak-data/snapshots/notion/`; requires Python path update | Medium |
| `asak-data/scripts` JSON/Markdown outputs | 22 | Reports, request batches, snapshots and temporary chunks | GENERATED_ARTIFACT / NEEDS_CONFIRMATION | Reports target `asak-data/reports/`; script output paths currently point to `scripts/` | Medium |
| `asak-data/schema-backups/` | 1 | Pre-short-name migration schema evidence | MOVE_TO_ARCHIVE | Moved in Batch A to `asak-data/archive/schema/` with the Markdown reference updated | Low |
| `worklog/` | 47 | Daily/entry history, templates, calendar and sync scripts | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION | Keep paths until calendar and scripts are migrated together | High |
| `data-pipeline/phase1/` | 23 | Data collection/transformation source and output | KEEP_ACTIVE_TOOL | Keep in place; no cleanup move in this phase | High |

### Bulk file rules (complete coverage for mechanically equivalent files)

| Path set | Count | Type / purpose | Reference or execution status | Classification | Recommended handling | Reason / risk |
| --- | ---: | --- | --- | --- | --- | --- |
| `asak-data/images/menu/*.png` | 84 | PNG deployment images | Referenced by menu seed URLs | KEEP_CANONICAL | Keep | Same hashes as many originals are intentional path-specific assets; deleting either path can break consumers. High risk. |
| `asak-data/images/original/*.png` | 84 | PNG source images | Used by `apply_original_images.py` workflow | KEEP_CANONICAL | Keep | Preserve image provenance and regeneration source. Medium risk. |
| `asak-data/scripts/notion_raw/*.json` | 151 | API response snapshots | Produced/consumed by scripts using `scripts/notion_raw` | GENERATED_ARTIFACT | Batch B move to `snapshots/notion/` with Python paths updated | Re-creatable but useful audit evidence; current path is hard-coded. |
| `docs/product_bible/_archive/**` | 58 | Archived Product Bible packs | Explicitly excluded by governance index | MOVE_TO_ARCHIVE | Retain in current `_archive`; assess deduplication only after reference check | 34+ exact-document duplicate groups are historical evidence, not deletion targets. |
| `docs/notion/**` | 288 | Notion exports, pages, meeting/worklog history | Reference content; some unique policy context | NEEDS_CONFIRMATION | Retain; classify page-by-page in a later batch | Filename duplication frequently represents different Notion databases, not duplicate content. |
| `worklog/daily/**`, `worklog/entries/**` | 23 non-template records | Team member work history | Calendar, README and sync tools depend on current layout | KEEP_ACTIVE_TOOL | Do not move in Batch A | Move requires current/archive participant decision plus code/README updates. |
| `docs/wiki/current-status-baseline.md`, `db-abbreviation-glossary.md`, `db-audit-plan.md`, `devcopilot-sync-report.md`, `future-scope.md`, `traceability-matrix.md`, `wbs-v2.md`, `snapshots/**` | 8 untracked paths | Running DevCopilot/WBS work | Protected by user instruction | NEEDS_CONFIRMATION | Leave untouched and uncommitted | Current working files must not be overwritten or absorbed into this cleanup commit. |

## Duplicate inspection

### Exact-content groups

| Group | Canonical candidate | Duplicate | Difference | Reference status | Recommended handling |
| --- | --- | --- | --- | --- | --- |
| Product Bible Pack 3 | `docs/product_bible/03_Menu_Inventory_SoldOut/**` | `docs/product_bible/_archive/ASAK_Product_Bible_Pack3/**` | Exact for duplicated files | Current pack is canonical; archive is historical | Keep current; retain archive until a human authorizes archive consolidation. |
| Product Bible Pack 4 | `docs/product_bible/04_Dashboard_Sales_Kitchen_TTS/**` | Two Pack 4 archive copies | Exact for most architecture/API/README files | Current pack is canonical | Keep one historical archive location only after a full reference check; Batch C decision. |
| Product Bible Pack 7 | `docs/product_bible/07_Screen_Bible/**` | `docs/product_bible/_archive/ASAK_Product_Bible_Pack7_Screen_Bible/**` | Exact for 19 screen/registry files | Current pack is canonical | Retain archive evidence; no deletion in this phase. |
| Menu images | `images/menu/{id}.png` and `images/original/{id}_*.png` | 95 intentional same-content paths, including three four-file groups | Names/consumption paths differ | Seed/README image workflow uses both locations | KEEP both; not a deletion candidate. |
| `seed-v3/menu_opt_override.json` / `opt_item_comp.json` | Neither | Each is an empty array | Roles differ in schema | Manifest names both | Do not merge based on hash; DB-schema review required. |

There are 128 SHA-256 groups (142 additional paths). Most are intentional image path pairs or Product Bible archive copies. No exact duplicate is safe to delete without a human archive-retention decision.

### Similar/role-overlap groups

| Group | Canonical candidate | Duplicate / overlap | Difference | Reference location | Recommended handling |
| --- | --- | --- | --- | --- | --- |
| Screen documentation | Product Bible Pack 7 `SCREEN_REGISTRY.md` | `docs/screens/screens.json`, `screens.md`, `screens-wiki.md`, `docs/wiki/screen-design-figma.md` | Registry is policy; JSON/export files serve tooling and sync | README, Figma/DevCopilot scripts | Keep all; add explicit source-versus-export labels in Batch B. |
| Figma guidance | `docs/design/FIGMA_GUIDE.md` + current Product Bible | dated Figma audits/prompts and meeting records | Operational instructions versus historical handoff prompts | Design plugins and team docs | Archive only concluded dated audits/prompts after Figma owner confirmation. |
| Product policy | `docs/product_bible/**` | `docs/wiki/**`, Notion exports | Wiki/Notion retain summary/source context and may drift | DevCopilot/Notion workflows | Product Bible remains canonical; do not delete exports. |
| Seed data | `asak-data/seed/` for current loaders | `seed-v3/` short-name corpus | Equal legacy record counts, different field abbreviations/policy tables | Separate loader scripts | DB owner must select schema before a merge/move. |
| Worklogs | Existing `worklog/daily`, `entries` | Notion daily-worklog export pages | Git history versus Notion collaboration history | Calendar/sync scripts | Keep both; no de-duplication. |

## Script inventory and proposed classification

Commands are shown relative to the repository root. “Current” means a README/current operations guide reference or an internal dependency; “review” does not mean unused.

| Script set | Command / input / output | Current status | Replacement / target | Classification |
| --- | --- | --- | --- | --- |
| `download_menu_images.py`, `apply_original_images.py` | `python asak-data/scripts/<name>.py`; source image URLs/original images → `images/` | README-documented | `scripts/active/images/` after reference update | KEEP_ACTIVE_TOOL |
| `load_seed_sqlite.py`, `load_seed_mysql.py` | `python .../load_seed_*.py`; `seed/*.json` → SQLite/MySQL | SQLite loader README-documented; MySQL loader remains schema tool | `scripts/active/seed/` | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION |
| `build_short_name_seed.py`, `load_short_name_seed_mysql.py`, `migrate_short_names_mysql.py`, `apply_option_policy_mysql.py`, `create_sales_views_mysql.py` | Python command plus DB arguments; `seed`/`seed-v3` → MySQL | Separate short-name migration chain; not guide-documented | `scripts/archive/one-off-migrations/` only after DB owner confirms v3 retirement | NEEDS_CONFIRMATION |
| `verify_notion_token.py`, `create_worklog.py`, `upload_getting_started_to_notion.py` | Python command; environment `NOTION_TOKEN` and Markdown → Notion API | First two are current operations-guide tools | `scripts/active/notion/` | KEEP_ACTIVE_TOOL |
| `sync_current_docs_devcopilot.py`, `devcopilot_upload.py`, `upload_wiki.py`, `upload_screens_api.py`, `upload_screens_wiki.py`, `sync_figma_links.py`, `export_screens.py`, `gen_wiki_markdown.py` | Python command; docs/screens/seed → DevCopilot/Figma/Notion outputs | Current or active dependency; several references are historic only | `scripts/active/devcopilot/` or `active/images/` | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION |
| `full_mapping_audit.py`, `req_link_audit.py`, `req_link_gap_audit.py`, `audit_scenarios.py`, `fix_fk_targets.py` | Python command; docs/API data → `*_report.json` | Audit utilities; reports are currently emitted into `scripts/` | `scripts/active/audit/`, outputs to `reports/audits/` | KEEP_ACTIVE_TOOL; output move is Batch B because Python output paths change |
| `append_fetch_result.py`, `apply_agent_batch.py`, `apply_fetch_batches.py`, `batch_save_notion.py`, `bulk_save_fetch.py`, `compact_to_raw.py`, `decode_b64_batch.py`, `export_batch.py`, `extract_transcript_fetches.py`, `fetch_notion_pages.py`, `fetch_progress.py`, `ingest_mcp_batch.py`, `jsonl_to_raw.py`, `mcp_fetch_all.py`, `merge_fetch_batch.py`, `notion_mcp_http_fetch.py`, `persist_pages.py`, `rebuild_scenario_raw.py`, `run_fetch_save_all.py`, `save_batch_jsonl.py`, `save_fetch_batch.py`, `save_fetches.py`, `save_final_missing.py`, `save_live_notion_batch.py`, `save_mcp_array.py`, `save_mcp_batch.py`, `save_mcp_file.py`, `save_mcp_pages.py`, `save_mcp_stdin.py`, `save_missing26.py`, `save_notion_fetch.py`, `save_one_fetch.py` | Batch/fetch conversion commands; JSON/JSONL/stdin → `scripts/notion_raw` and temporary artifacts | Not in current operations guides; some form dependency chains | Consolidate after replay test under `scripts/archive/deprecated/` or `active/notion/` | MOVE_TO_ARCHIVE candidate; do not move before chain mapping |
| `api_format.py`, `extra_apis.py`, `generate_scenario_props.py`, `gen_embedded_pages.py`, `gen_embedded_part2.py`, `gen_embedded_part3.py`, `gen_embedded_qa.py`, `list_missing_notion.py`, `remove_former_members_devcopilot.py`, `req_link_maps.py`, `sync_devcopilot_db_schema.py`, `sync_devcopilot_sales_views.py`, `sync_req_screen_links.py`, `update_column_descriptions.py`, `update_table_descriptions.py`, `upload_tasks_only.py`, `upload_wiki_batch.py`, `verify_devcopilot_upload.py`, `rename_figma_scr_frames.py` | One-off/maintenance commands; local docs/API data → external API or report | 44 scripts have no current-guide reference; these 19 have either historic or internal references | Retain until named owner validates the last successful command | NEEDS_CONFIRMATION |

**Count interpretation:** 11 scripts are directly documented for current team operations, 22 are active dependencies or audit candidates, and 44 are one-off/archive candidates by the absence of a current-guide reference. This is not a deletion list.

### Generated artifacts and `.gitignore` proposal (not applied)

| Item | Evidence / value | Decision |
| --- | --- | --- |
| `asak-data/scripts/*_report.json` (7 tracked files) | Re-created by audit/upload scripts; no text references | Move to `reports/audits/` or `reports/upload-results/` only with Python output-path changes; then ignore regenerated local reports unless retained as dated evidence. |
| `asak-data/scripts/notion_raw/*.json` (151) | Fetch/save workflow snapshots | Keep as dated snapshots, move to `snapshots/notion/`; do not ignore until retention period is agreed. |
| `asak-data/scripts/_gs_*.md` (5) | Temporary generated chunks; already ignored by pattern | Archive current tracked copies first; continue ignoring new files. |
| `worklog/scripts/__pycache__/worklog_paths.cpython-313.pyc` | Python bytecode; `__pycache__/` is already ignored but a tracked file remains | DELETE_CANDIDATE after explicit approval; do not delete now. |
| `docs/screens/screens-devcopilot-localstorage.json` | Local-storage import payload | NEEDS_CONFIRMATION; likely generated, but verify DevCopilot recovery needs before ignore/move. |
| `asak-data/asak_sample.db` | Rebuildable local DB; `*.db` is already ignored | Keep ignored; no tracked copy found. |

Proposed future `.gitignore` additions, after the files are relocated and retention is approved:

```gitignore
# Locally regenerated ASAK data-tool output
asak-data/reports/upload-results/*.json
asak-data/reports/audits/*_local.json
asak-data/scripts/notion_raw/
docs/screens/*localstorage*.json
worklog/scripts/__pycache__/
```

## Seed and seed-v3 audit

| Area | Finding | Decision |
| --- | --- | --- |
| Canonical loader evidence | `asak-data/README.md`, `load_seed_sqlite.py`, `load_seed_mysql.py`, and `gen_wiki_markdown.py` use `asak-data/seed` | `seed` is the current repository sample-seed candidate. |
| v3 loader evidence | `build_short_name_seed.py` writes `seed-v3`; `load_short_name_seed_mysql.py` consumes it after short-name migration | `seed-v3` is a schema-migration corpus, not automatically newer canonical data. |
| Corresponding files | 17 shared logical tables match record counts: category 6, menu 84, ingredient/ing 90, menu-option legacy 9,166, option-item 157, etc. | Preserve both until DB owner confirms the target schema. |
| Field changes | v3 shortens names (`category_id`→`cat_id`, `ingredient_id`→`ing_id`, `option_group_id`→`opt_group_id`, `sort_order`→`sort_no`, `is_active`→`active`) | Do not rename or merge by filename. |
| v3-only policy files | `opt_policy` 82, `opt_policy_item` 734, `menu_opt_policy` 467, `menu_opt_override` 0; legacy menu option files remain | Require DB schema/import review. |
| FK check | 21 explicit legacy-corpus relations in each seed set were checked against referenced `id` collections; invalid values: 0 | Referential data is internally consistent for the checked relations; DB load and schema constraints still need owner validation. |

## Documentation and worklog structure decision

The existing governance documents already declare `docs/product_bible` as the Product Bible canonical path. This cleanup therefore updates `DOCUMENT_STATUS_MANIFEST.md` instead of creating a second canonical manifest.

```text
docs/
  product_bible/       current product/Screen/Component/QA standards
  governance/          status, ownership and cleanup inventory
  planning/            current implementation sequence/status
  design/              live Figma guides, plugins and assets
  guides/ operations/  team-facing procedures and setup
  screens/             screen source and tool exports
  wiki/                DevCopilot sync source (protected when active)
  archive/
    design-audits/     concluded dated audits
    prompts/           superseded approved prompts
    migrations/        concluded migration notes
    notion-exports/    frozen exports, after page-level review
    superseded/        replaced non-canonical documents
    project-history/   retained historical evidence
asak-data/
  seed/                current sample-seed candidate
  seed-v3/             short-name migration corpus pending decision
  scripts/active/      documented tools after Batch B path update
  scripts/archive/     one-off/deprecated scripts after replay review
  reports/ snapshots/  generated outputs separated from executable code
  archive/schema/      migration schema evidence
worklog/
  daily/ entries/      preserve existing paths until calendar/sync migration
  templates/ scripts/ weekly/
```

README additions are deferred: they are useful only after Batch B path changes are approved, otherwise they would document a structure that has not yet been applied.

## Batches and approvals

### Batch A — safe, executed

| From | To | Reference update | Why safe |
| --- | --- | --- | --- |
| `asak-data/schema-backups/short-name-before-20260713-115747.sql` | `asak-data/archive/schema/short-name-before-20260713-115747.sql` | `docs/design/FIGMA_AGENT_DATA_CONTRACT_AUDIT_2026-07-15.md` | Immutable pre-migration evidence; no executable caller. |
| `docs/team/design-doc-merge-audit-2026-07-06.md` | `docs/archive/design-audits/design-doc-merge-audit-2026-07-06.md` | Worklog/design/team links | Concluded 2026-07-06 audit retained with history. |
| `docs/team/notion-merge-sync-audit-2026-07-06.md` | `docs/archive/design-audits/notion-merge-sync-audit-2026-07-06.md` | Worklog/design links | Concluded 2026-07-06 sync audit retained with history. |

### Batch B — reference/code updates required; approval required

- Move JSON reports from `asak-data/scripts/` to `asak-data/reports/`: seven Python scripts currently construct output paths inside `scripts/`.
- Move `notion_raw/` and temporary fetch chains: their Python readers/writers use the current directory.
- Introduce `scripts/active/*` and `scripts/archive/*`: update README, PowerShell, Markdown, Python call paths and replay tested workflows.
- Restructure worklogs: update calendar builder, calendar JSON generation, Notion sync, README and existing links together.
- Add target-folder READMEs after the actual paths are approved.

### Batch C — human decision required

- Select `seed` versus the short-name `seed-v3` schema for future DB work.
- Resolve `docs/wiki` versus Product Bible content intake, without overwriting current DevCopilot/WBS files.
- Confirm `docs/team/2026-07-14-feedback-resolution.md`, `hub-notion-sync-checklist.md`, and `notion-sync-change-register-2026-07-14.md` as current/reference/archive.
- Confirm the owner and archive policy for dated Figma prompts/audits and the Notion export tree.
- Confirm current versus former worklog participants before changing directory names.

### Batch D — deletion candidates; no deletion proposed now

- Tracked Python bytecode is a deletion candidate only after explicit approval.
- Exact Product Bible archive copies and intentional image copies are **not** deletion candidates in this phase.
- No credential value was found by signature scan; no token-file deletion is required.

## Reference-risk register

| Risk | Affected files | Required safeguard |
| --- | --- | --- |
| Python output path is embedded | Seven report-producing scripts and Notion snapshot fetch chain | Update code and run a dry-run before Batch B move. |
| Current DevCopilot/WBS files are untracked | Eight `docs/wiki` paths | Exclude from staging and never overwrite. |
| Worklog paths are executable configuration | Calendar/README/Python/PowerShell links | Move only as a tested atomic Batch B change. |
| Schema snapshot link | Figma Agent data contract audit | Update Markdown link in Batch A. |
| Historic audit links | 2026-07-06 worklog/design/team documents | Update links in Batch A and verify with repository search. |
