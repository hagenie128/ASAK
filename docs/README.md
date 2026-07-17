# ASAK Documentation

> 2026-07-16 cleanup: product rules stay in `product_bible`, current delivery state stays in `wiki`, and concluded evidence belongs in `archive`. `docs/notion` retains only script-backed DevCopilot source inputs; historic exports are in `archive/notion-exports`.

## 운영 원칙

- **정본:** `product_bible/`(정책·요구사항·Screen Registry), `wiki/`(현재 상태·WBS2), `design/`(반복 사용하는 Figma 실행 기준), `governance/`(정본·상태 정책).
- **생성물:** `screens-devcopilot-*.json`과 `asak-data` 보고서는 생성 스크립트의 출력 계약을 확인한 뒤에만 위치를 바꾼다.
- **Archive:** 완료 감사·프롬프트·과거 계획·Notion Export는 `archive/`에 보존하며, 삭제하거나 정본으로 되돌리지 않는다.
- **주의:** `docs/notion`과 `worklog/daily`는 현재 Python 동기화 경로가 직접 읽는다. 경로를 바꾸려면 스크립트 변경 승인과 재검증이 필요하다.

```powershell
git status
python asak-data/scripts/sync_current_docs_devcopilot.py --help
python worklog/scripts/build_calendar.py
```

## 문서 진입 순서

1. [Product Bible Index](governance/PRODUCT_BIBLE_INDEX.md)
2. [Canonical Contract Decisions](governance/CANONICAL_CONTRACT_DECISIONS.md)
3. [Current Implementation Map](planning/CURRENT_IMPLEMENTATION_MAP.md)
4. [Implementation Priority](planning/IMPLEMENTATION_PRIORITY.md)
5. [Document–Code Gap Report](architecture/DOCUMENT_CODE_GAP_REPORT.md)
6. [Product Bible Pack 1~12](product_bible/)
7. [Operations setup](operations/setup/)
8. [Design](design/)
9. [Screens](screens/)
10. [Guides](guides/)
11. [Team](team/)
12. [Wiki](wiki/)
13. [Notion script inputs](notion/)
14. [Archive](archive/)

## 정본과 범위

- `docs/product_bible`이 현재 Product Bible 정본이다. 실제 폴더명 `product_bible`을 유지한다.
- `docs/product_bible/_archive`는 현재 구현의 기준에서 제외한다.
- 기존 Notion export, 회의록, WBS는 고유 맥락을 보존하는 Reference 또는 Archive이며 Product Bible을 대체하지 않는다.
- Product Bible 문서 수는 구현 범위를 뜻하지 않는다. 구현은 MVP와 `FUTURE_SCOPE`를 구분해 승인된 Vertical Slice만 진행한다.
- 계약 결정은 [Canonical Contract Decisions](governance/CANONICAL_CONTRACT_DECISIONS.md), 과거 문서의 분류는 [Legacy and Reference Index](governance/LEGACY_AND_REFERENCE_INDEX.md)를 따른다.

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
| `archive` | Concluded audits, prompts, plans, generated reports, Notion exports, and project history. |

## Pack 1~12

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
