# ASAK Documentation

> **👉 처음이면 [START_HERE.md](START_HERE.md)만 보세요.** (단일 진입점)  
> **2026-07-20:** 구현 현실은 `planning/current-implementation-map-2026-07-16.md`, 실행 WBS 정본은 [`wiki/wbs-v2-2026-07-16.md`](wiki/wbs-v2-2026-07-16.md)입니다.
> 07-16 cleanup 정책(정본/생성물/Archive 분리)은 유지. `docs/notion`은 DevCopilot 스크립트 입력용.

## 운영 원칙

- **입구:** [START_HERE](START_HERE.md) · [PROJECT_HUB](../PROJECT_HUB.md)
- **정책 정본:** `product_bible/` (먼저 [읽기 허브](product_bible/product-bible-hub.md)) · **계약:** `governance/canonical-contract-decisions-2026-07-16.md`
- **구현 현실:** [baseline](wiki/current-status-baseline.md) · [구현 맵](planning/current-implementation-map-2026-07-16.md) · **앱 허브:** [app-implementation-hub](planning/app-implementation-hub.md)
- **앱 실행 문서:** 각 저장소 `IMPLEMENTATION_PLAN.md`, `src/STRUCTURE_GUIDE.md`
- **Archive:** `_archive/` — 삭제·정본 복귀 금지
- **파일명 규칙:** [document-naming-guide-2026-07-20.md](document-naming-guide-2026-07-20.md) · 검사: `pwsh asak-data/scripts/check-filename-convention.ps1` · 인벤토리: [document-inventory-slim-2026-07-20.md](document-inventory-slim-2026-07-20.md)
- **주의:** `docs/notion`, `worklog/daily` 경로는 스크립트가 읽음 — 무단 이동 금지

```powershell
git status
python asak-data/scripts/sync_current_docs_devcopilot.py --help
python worklog/scripts/build_calendar.py
```

## 문서 진입 순서

1. **[START_HERE](START_HERE.md)** ← 여기부터
2. [Wiki 색인](wiki/index.md) · [baseline](wiki/current-status-baseline.md) · [구현 맵](planning/current-implementation-map-2026-07-16.md)
3. [앱 구현 허브](planning/app-implementation-hub.md) · [WBS 2.0](wiki/wbs-v2-2026-07-16.md)
4. [Canonical Contract Decisions](governance/canonical-contract-decisions-2026-07-16.md)
5. [Current Implementation Map](planning/current-implementation-map-2026-07-16.md)
6. [Document–Code Gap Report](architecture/document-code-gap-report-2026-07-16.md)
7. [Implementation Priority](planning/implementation-priority-2026-07-16.md) *(목표 순서 · 현실은 MAP)*
8. [프론트 3일 WBS](planning/frontend-wednesday-wbs-2026-07-20.md)
9. [Product Bible 허브](product_bible/product-bible-hub.md) · [Pack README](product_bible/README.md) · [Index](governance/product-bible-index-2026-07-16.md)
10. [Design](design/) · [Screens](screens/)
11. [Operations setup](operations/setup/)
12. [Archive](_archive/) — 한물간 문서, 실행에 쓰지 않음

## 정본과 범위

- `docs/product_bible`이 현재 Product Bible 정본이다. 실제 폴더명 `product_bible`을 유지한다.
- `docs/product_bible/_archive`는 현재 구현의 기준에서 제외한다.
- 기존 Notion export, 회의록, WBS는 고유 맥락을 보존하는 Reference 또는 Archive이며 Product Bible을 대체하지 않는다.
- Product Bible 문서 수는 구현 범위를 뜻하지 않는다. 구현은 MVP와 `FUTURE_SCOPE`를 구분해 승인된 Vertical Slice만 진행한다.
- 계약 결정은 [Canonical Contract Decisions](governance/canonical-contract-decisions-2026-07-16.md), 과거 문서의 분류는 [Legacy and Reference Index](governance/legacy-and-reference-index-2026-07-16.md)를 따른다.

## Folder purpose

| Folder | Purpose |
|---|---|
| `governance` | Canonical-source, contract, status, and legacy/reference policy. |
| `planning` | Current implementation state, MVP order, and Vertical Slice plan. |
| `architecture` | Document-to-code gap analysis. |
| `product_bible` | Current Product Bible Pack 1~12; `_archive` is excluded from implementation criteria. |
| `operations/setup` | Installation, onboarding, and MCP setup. |
| `design` | Design system, Figma, and visual design references. |
| `screens` | Screen definitions and screen-level specifications. |
| `guides` | Team development and implementation guides. |
| `team` | Team collaboration and role-related documents. |
| `wiki` | Project knowledge and reference documents. |
| `notion` | Current DevCopilot sync input snapshots only; not a product-policy source. |
| `_archive` | Concluded audits, prompts, plans, generated reports, Notion exports, and project history. |

## Pack 1~12

먼저 [product-bible-hub.md](product_bible/product-bible-hub.md). Pack별 파일 목록은 각 Pack README.

| Pack | 링크 |
|---|---|
| 01 Foundation | [README](product_bible/01_Foundation/README.md) |
| 02 Order / Cart / Payment | [README](product_bible/02_Order_Cart_Payment/README.md) |
| 03 Menu / Inventory / Sold-out | [README](product_bible/03_Menu_Inventory_SoldOut/README.md) |
| 04 Dashboard / Sales / Kitchen / TTS | [README](product_bible/04_Dashboard_Sales_Kitchen_TTS/README.md) |
| 05 Accessibility / Timeout / Error | [README](product_bible/05_Accessibility_Timeout_Error/README.md) |
| 06 Engineering | [README](product_bible/06_Engineering_Bible/README.md) |
| 07 Screen | [README](product_bible/07_Screen_Bible/README.md) |
| 08 Component | [README](product_bible/08_Component_Bible/README.md) |
| 09 QA | [README](product_bible/09_QA_Bible/README.md) |
| 10 AI Master | [README](product_bible/10_AI_Master_Bible/README.md) |
| 11 Backend Implementation | [README](product_bible/11_Backend_Implementation/README.md) |
| 12 Frontend Implementation | [README](product_bible/12_Frontend_Implementation/README.md) |
