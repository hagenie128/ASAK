# ASAK Documentation

## 문서 진입 순서

1. [Product Bible Index](governance/PRODUCT_BIBLE_INDEX.md)
2. [Canonical Contract Decisions](governance/CANONICAL_CONTRACT_DECISIONS.md)
3. [Current Implementation Map](planning/CURRENT_IMPLEMENTATION_MAP.md)
4. [Implementation Guide Start](implementation_guide/00_START_HERE.md)
5. [API·응답 구현 가이드](implementation_guide/04_API_DB_IMPLEMENTATION.md)
6. [Implementation Priority](planning/IMPLEMENTATION_PRIORITY.md)
7. [Document–Code Gap Report](architecture/DOCUMENT_CODE_GAP_REPORT.md)
8. [Product Bible Pack 1~12](product_bible/)
7. [Operations setup](operations/setup/)
8. [Design](design/)
9. [Screens](screens/)
10. [Guides](guides/)
11. [Team](team/)
12. [Wiki](wiki/)
13. [Notion](notion/)
14. [Documentation management](documentation-management/)

## 정본과 범위

- `docs/product_bible`이 현재 Product Bible 정본이다. 실제 폴더명 `product_bible`을 유지한다.
- `docs/product_bible/_archive`는 현재 구현의 기준에서 제외한다.
- 기존 Notion export, 회의록, WBS는 고유 맥락을 보존하는 Reference 또는 Archive이며 Product Bible을 대체하지 않는다.
- Product Bible 문서 수는 구현 범위를 뜻하지 않는다. 구현은 MVP와 `FUTURE_SCOPE`를 구분해 승인된 Vertical Slice만 진행한다.
- 계약 결정은 [Canonical Contract Decisions](governance/CANONICAL_CONTRACT_DECISIONS.md), 과거 문서의 분류는 [Legacy and Reference Index](governance/LEGACY_AND_REFERENCE_INDEX.md)를 따른다.
- 화면 구현은 승인된 Figma `00-C`(파일 맵), `05-C`(Kiosk), `06-C`(Admin), `07-C`(상태 QA)을 함께 확인한다. 화면의 Default만 보고 구현 완료로 판단하지 않는다.
- 구현 가이드는 Product Bible을 대체하지 않는다. 화면별 API 요청·응답·오류 형태는 [04 API·응답 구현 가이드](implementation_guide/04_API_DB_IMPLEMENTATION.md)와 기능별 원본 API Contract를 함께 사용한다.

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
| `notion` | Preserved Notion-export source documents. |
| `documentation-management` | Documentation inventory, structure, and archival-management records. |

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
