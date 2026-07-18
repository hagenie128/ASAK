# ASAK Documentation

> **태그 전체 지도:** [DOCUMENT_TAG_INDEX.md](./DOCUMENT_TAG_INDEX.md)  
> **상태 정책:** [governance/DOCUMENT_STATUS_MANIFEST.md](./governance/DOCUMENT_STATUS_MANIFEST.md)

이 폴더는 ASAK **중앙 문서 허브**입니다. 구현 저장소(Kiosk/Admin/back) 문서는 각 저장소에 두고, 여기는 정본·가이드·이력을 둡니다.

---

## 지금 작업할 때는 이것만

1. 만들 기능 선택 → [구현 작업대](./implementation_guide/00_START_HERE.md)
2. 실제 코드 상태 확인 → [현재 구현 지도](./planning/CURRENT_IMPLEMENTATION_MAP.md)와 해당 저장소 코드
3. 끝난 작업 기록 → [팀 워크로그](../worklog/TEAM_WORKLOG.md)

막히는 경우에만 Product Bible, Figma, 과거 QA를 연다. `#reference`, `_archive`, 날짜가 붙은 회의·감사 문서는 시작점이 아니다.

## 포트폴리오에 남길 것

- 기능별 **문제 → 내 판단 → 직접 구현 → AI 검토 → 검증 → 개선** 기록
- PR, 테스트 결과, 화면 캡처·시연 영상, 해결한 버그의 원인과 결과
- 개인 정리 양식: [포트폴리오 템플릿](./guides/05-personal-portfolio-template.md)

---

## 30초 진입 (추천 순서)

| 순서 | 문서 | 태그 |
|:--:|---|---|
| 1 | [Product Bible Index](./governance/PRODUCT_BIBLE_INDEX.md) | `#canonical` |
| 2 | [Canonical Contract Decisions](./governance/CANONICAL_CONTRACT_DECISIONS.md) | `#canonical` |
| 3 | [Current Implementation Map](./planning/CURRENT_IMPLEMENTATION_MAP.md) | `#current` |
| 4 | [Implementation Guide — Start](./implementation_guide/00_START_HERE.md) | `#current` |
| 5 | [디자인 현재 상태](./design/README.md) | `#current` |
| 6 | [문서 태그 인덱스](./DOCUMENT_TAG_INDEX.md) | `#reference` |

---

## 폴더 한눈에 (태그)

| 폴더 | 태그 | 용도 | 바로 가기 |
|---|---|---|---|
| `product_bible/` | `#canonical` | Pack 1~12 정본 | [폴더](./product_bible/) |
| `governance/` | `#canonical` / `#reference` | 계약·상태·레거시 정책 | [폴더](./governance/) |
| `planning/` | `#current` | 구현 지도·우선순위 | [README](./planning/README.md) |
| `architecture/` | `#current` | 문서↔코드 갭 | [README](./architecture/README.md) |
| `implementation_guide/` | `#current` | 화면·API 구현 절차 | [00_START_HERE](./implementation_guide/00_START_HERE.md) |
| `operations/` | `#current` | 설치·온보딩·MCP | [README](./operations/README.md) |
| `design/` | `#current` / `#wip` | Figma·디자인 QA | [README](./design/README.md) |
| `screens/` | `#reference` | SCR 표·DevCopilot JSON | [README](./screens/README.md) |
| `guides/` | `#reference` | 팀 가이드 | [README](./guides/README.md) |
| `wiki/` | `#reference` | DevCopilot Wiki 산출물 | [README](./wiki/README.md) |
| `team/` | `#reference` | Notion hub 동기화 | [README](./team/README.md) |
| `notion/` | `#legacy` / `#archive` | Notion export 원본 | [README](./notion/README.md) |
| `documentation-management/` | `#reference` | 문서 구조·인벤토리 | [README](./documentation-management/README.md) |
| `_archive/` | `#archive` | 중앙 보관함 | [README](./_archive/README.md) |
| `design/_archive/` | `#archive` | Figma 중복·일회성 | [README](./design/_archive/README.md) |
| `product_bible/_archive/` | `#archive` | 이전 Pack | 구현 기준 제외 |

---

## 정본과 범위

- `docs/product_bible`이 Product Bible **정본**이다. 폴더명 `product_bible`을 유지한다.
- `product_bible/_archive`와 `notion/**/Archive*`는 **현재 구현 기준에서 제외**한다.
- Notion export·회의록·WBS는 고유 맥락을 보존하는 Reference/Archive이며 Bible을 **대체하지 않는다**.
- 화면은 Figma `00-C` / `05-C` / `06-C` / `07-C`와 Pack 07을 함께 본다. Default만 보고 완료로 판단하지 않는다.
- 구현 가이드는 Bible을 대체하지 않는다. API 형태는 [04 API·응답](./implementation_guide/04_API_DB_IMPLEMENTATION.md) + 기능별 API Contract를 함께 쓴다.
- Admin 구현 정본 저장소는 **ASAK-Admin**. Kiosk 내부 Admin 스캐폴드는 `#legacy`.

---

## Pack 1~12

| Pack | 링크 |
|---|---|
| 01 Foundation | [README](./product_bible/01_Foundation/README.md) |
| 02 Order / Cart / Payment | [README](./product_bible/02_Order_Cart_Payment/README.md) |
| 03 Menu / Inventory / Sold-out | [README](./product_bible/03_Menu_Inventory_SoldOut/README.md) |
| 04 Dashboard / Sales / Kitchen / TTS | [README](./product_bible/04_Dashboard_Sales_Kitchen_TTS/README.md) |
| 05 Accessibility / Timeout / Error | [README](./product_bible/05_Accessibility_Timeout_Error/README.md) |
| 06 Engineering | [README](./product_bible/06_Engineering_Bible/README.md) |
| 07 Screen | [README](./product_bible/07_Screen_Bible/README.md) |
| 08 Component | [README](./product_bible/08_Component_Bible/README.md) |
| 09 QA | [README](./product_bible/09_QA_Bible/README.md) |
| 10 AI Master | [README](./product_bible/10_AI_Master_Bible/README.md) |
| 11 Backend Implementation | [README](./product_bible/11_Backend_Implementation/README.md) |
| 12 Frontend Implementation | [README](./product_bible/12_Frontend_Implementation/README.md) |

---

## 저장소 로컬 문서

| 저장소 | 시작점 |
|---|---|
| ASAK-Kiosk | `ASAK-Kiosk/README.md` |
| ASAK-Admin | `ASAK-Admin/docs/README.md` |
| ASAK-back | `ASAK-back/README.md` |
| 워크로그 | `ASAK/worklog/README.md` |
