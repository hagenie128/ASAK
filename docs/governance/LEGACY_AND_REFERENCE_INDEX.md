# Legacy and Reference Index

> This index classifies non-canonical documents without deleting, moving, or rewriting their unique content. Canonical product rules are in [Product Bible](../README.md#pack-112).

## Reference

| Document group | Why it is not canonical | Unique information to preserve | Follow-up |
|---|---|---|---|
| `docs/guides/**` | onboarding and work guidance, not product contract | team setup, Git process, work-log formats | link to current Pack where applicable |
| `docs/wiki/**` | exported project summaries | requirements, scenario, DB/API/WBS context | compare with Product Bible before reuse |
| `docs/design/**` (current Figma guides/specs) | Figma support material | Figma nodes, design assets, design process | confirm latest Figma/Screen Registry |
| `docs/notion/**` | script-backed Notion input snapshot | DevCopilot upload source only | compare with Product Bible before reuse |

## Legacy

| Document group | Why not canonical | Unique information to preserve |
|---|---|---|
| `ASAK-Kiosk/src/pages/admin/**`, `components/admin/**`, `api/admin.js`, `api/sales.js` | Admin implementation canonical is ASAK-Admin | prior frontend scaffold and field expectations |
| `docs/team/**`, design meeting opinions | dated collaboration/decision context | authorship, review history, unresolved feedback |
| Notion daily worklogs and prior implementation plans | point-in-time progress records | implementation history and test evidence |

## Archived

| Document group | Why archived |
|---|---|
| `docs/product_bible/_archive/**` | explicitly excluded from current implementation criteria |
| `docs/archive/notion-exports/**` | historical Notion export |
| concluded meetings, dated schedules, completed WBS records | preserved history; not a current requirement |

## Needs Review

- `docs/notion/**` is retained solely where a current script reads it; review any policy intake against Product Bible before use.
- `docs/design/**/prompts/**`, plugin documents, and older design candidates: useful tooling history but must be checked against current Figma and Pack 08.

## Candidate unique information for Product Bible review

1. Device event logs and API performance targets.
2. Korean/English UI switching, QR/barcode scanning, packaging bag options, set discounts, and advanced topping quantity controls.
3. Past requirement rationale and QA evidence that is absent from Pack 09.

These are review candidates only. They are not MVP commitments until a human accepts them into the Product Bible.
