# ASAK 문서 안내

> **👉 처음이면 [문서 시작](START_HERE.md)만 보세요.** (단일 진입점)
> **2026-08-14:** 현재 구현 상태 문서는 시점 스냅샷이며, 실행 작업 분해표 정본은 [`wiki/wbs.md`](wiki/wbs.md)입니다.
> 07-16 정리 정책(정본·생성물·보관 문서 분리)은 유지합니다. `docs/notion`은 DevCopilot 스크립트 입력용입니다.

## 운영 원칙

- **입구:** [문서 시작](START_HERE.md) · [프로젝트 허브](../PROJECT_HUB.md)
- **정책 정본:** `product_bible/` (먼저 [읽기 허브](product_bible/product-bible-hub.md)) · **계약:** `governance/canonical-contract-decisions-2026-07-16.md`
- **현재 구현:** [구현 현황 요약](wiki/current-status-baseline.md) · [구현 맵](planning/current-implementation-map-2026-07-16.md) · **앱 허브:** [앱 구현 허브](planning/app-implementation-hub.md)
- **AI 도구 사용:** [AI 스킬 및 코드 그래프 사용 가이드](guides/12-ai-agent-tools-guide.md) · Codex·Claude·Cursor·Antigravity 공통 사용 규칙
- **앱 실행 문서:** `src/STRUCTURE_GUIDE.md` · 키오스크/백엔드는 `IMPLEMENTATION_PLAN.md` · **관리자 계획 파일은 삭제됨** → 가상 데이터 사전·중앙 작업 분해표·구현 맵 사용
- **과거 이력:** 대형 `_archive/` 트리는 제거했습니다. 필요한 과거 자료는 Git 이력에서 조회하며 정본으로 되돌리지 않습니다.
- **파일명 규칙:** [document-naming-guide-2026-07-20.md](document-naming-guide-2026-07-20.md) · 검사: `pwsh asak-data/scripts/check-filename-convention.ps1` · 인벤토리: [document-inventory-slim-2026-07-20.md](document-inventory-slim-2026-07-20.md)
- **주의:** `docs/notion`, `worklog/daily` 경로는 스크립트가 읽음 — 무단 이동 금지

```powershell
git status
python asak-data/scripts/sync_current_docs_devcopilot.py --help
python worklog/scripts/build_calendar.py
```

## 문서 진입 순서

1. **[문서 시작](START_HERE.md)** ← 여기부터
2. [위키 색인](wiki/index.md) · [구현 현황 요약](wiki/current-status-baseline.md) · [구현 맵](planning/current-implementation-map-2026-07-16.md)
3. [앱 구현 허브](planning/app-implementation-hub.md) · [작업 분해표](wiki/wbs.md)
4. [정본 계약 결정](governance/canonical-contract-decisions-2026-07-16.md)
5. [현재 구현 맵](planning/current-implementation-map-2026-07-16.md)
6. [문서–코드 차이 보고서](architecture/document-code-gap-report-2026-07-16.md)
7. [구현 우선순위](planning/implementation-priority-2026-07-16.md) *(목표 순서 · 현재 상태는 구현 맵 기준)*
8. [프론트 3일 WBS](planning/frontend-wednesday-wbs-2026-07-20.md)
9. [제품 기준 문서 허브](product_bible/product-bible-hub.md) · [팩 안내](product_bible/README.md) · [색인](governance/product-bible-index-2026-07-16.md)
10. [디자인](design) · [화면](screens)
11. [운영 환경 설정](operations/setup)
12. 과거 이력은 Git history에서만 조회 — 실행 기준으로 사용하지 않음

## 정본과 범위

- `docs/product_bible`이 현재 제품 기준 문서의 정본이다. 실제 폴더명 `product_bible`은 링크 호환을 위해 유지한다.
- Product Bible은 Pack 1~12의 활성 통합 문서만 구현 기준으로 사용한다.
- 기존 Notion 내보내기, 회의록, 작업 분해표는 고유 맥락을 보존하는 참고 또는 보관 자료이며 제품 기준 문서를 대체하지 않는다.
- 제품 기준 문서 수는 구현 범위를 뜻하지 않는다. 구현은 최소 기능 제품과 `FUTURE_SCOPE`를 구분해 승인된 세로 기능 흐름만 진행한다.
- 계약 결정은 [정본 계약 결정](governance/canonical-contract-decisions-2026-07-16.md), 과거 문서 분류는 [과거·참고 자료 목록](governance/legacy-and-reference-index-2026-07-16.md)을 따른다.

## 폴더 역할

| 폴더 | 역할 | 태그 |
|---|---|---|
| `START_HERE.md` | 단일 문서 진입점 | `#current` |
| `governance` | 정본·계약·상태·과거 자료 정책 | `#canonical` / `#reference` |
| `planning` | 구현 맵·우선순위·앱 허브 | `#current` |
| `implementation_guide` | 화면·도메인 작업 카드 | `#current` |
| `architecture` | 문서–코드 차이 분석 | `#reference` |
| `product_bible` | 제품 기준 팩 1~12 | `#canonical` |
| `operations` | 설치·회의록 정본 | `#current` |
| `design` | Figma 동결 정본과 실행 플러그인 | `#reference` / `#tooling` |
| `screens` | 화면 export/스냅샷 | `#reference` |
| `guides` | 온보딩·AI 도구 가이드 | `#reference` |
| `study` | 공부 레포트·외부 참고 | `#reference` |
| `team` | 팀 협업 stub | `#reference` |
| `wiki` | Hub/DevCopilot 참고·WBS 정본 | Mixed |
| `notion` | DevCopilot 동기화 입력 (이동 금지) | `#reference` |
| `ai-reports` | 일자별 AI 동기화/사인오프 산출 | `#archive`에 가깝게 취급 |
| `00_presentation` | 발표 PPT (최신=수정3) | `#current` |

## 제품 기준 문서 팩 1~12

먼저 [제품 기준 문서 허브](product_bible/product-bible-hub.md)를 봅니다. 팩별 파일 목록은 각 팩의 안내문에 있습니다.

| 팩 | 링크 |
|---|---|
| 01 기반 | [안내](product_bible/01_Foundation/README.md) |
| 02 주문·장바구니·결제 | [안내](product_bible/02_Order_Cart_Payment/README.md) |
| 03 메뉴·재고·품절 | [안내](product_bible/03_Menu_Inventory_SoldOut/README.md) |
| 04 대시보드·매출·주방·음성 안내 | [안내](product_bible/04_Dashboard_Sales_Kitchen_TTS/README.md) |
| 05 접근성·시간 초과·오류 | [안내](product_bible/05_Accessibility_Timeout_Error/README.md) |
| 06 엔지니어링 | [안내](product_bible/06_Engineering_Bible/README.md) |
| 07 화면 | [안내](product_bible/07_Screen_Bible/README.md) |
| 08 컴포넌트 | [안내](product_bible/08_Component_Bible/README.md) |
| 09 품질 검증 | [안내](product_bible/09_QA_Bible/README.md) |
| 10 인공지능 작업 기준 | [안내](product_bible/10_AI_Master_Bible/README.md) |
| 11 백엔드 구현 | [안내](product_bible/11_Backend_Implementation/README.md) |
| 12 프론트엔드 구현 | [안내](product_bible/12_Frontend_Implementation/README.md) |
