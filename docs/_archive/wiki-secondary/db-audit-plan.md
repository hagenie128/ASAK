# DB Audit Plan

## Current decision

The DevCopilot Modeler has 30 models (26 tables and 4 views), including two legacy backup tables. ASAK-back currently has no schema SQL, migration, entity, repository, or persistence dependency evidence. Therefore DB implementation status is `TODO`.

## Audit sequence

1. Export/read DevCopilot Modeler table and relation metadata.
2. Collect backend `schema.sql`, migration, Entity, Repository, Enum, seed, FK, index, and constraint evidence when created.
3. Compare by table and column without renaming abbreviations.
4. Classify each item: Modeler-only, backend-only, matched, name mismatch, relation mismatch, or legacy/deprecated.
5. Review a change proposal before any schema mutation.

## Legacy models

`menu_option_group_legacy_20260710` and `menu_option_legacy_20260710` are preserved as Legacy/Deprecated backup models. They are excluded candidates for current MVP dashboards; they must not be deleted or renamed in this work.
