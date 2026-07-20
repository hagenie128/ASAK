# 디자인·문서 병합 감사 — 2026-07-06

> **근거**: [screen-design-changes-2026-07-06.md](../../../_archive/project-history/design-meetings/screen-design-changes-2026-07-06.md) · `docs/screens/screens.json`
> **감사일**: 2026-07-06

## 회의 정본 (한 줄)

**DS-02 Modern Minimal** 채택 · **SCR-001+002** → 홈 (매장·포장) · **SCR-005+006** → 장바구니·주문확인 + 컨펌 팝업 · 고객 UI **6단계** (001→003→004→005→007→008) · SCR ID **21개 유지** (002·006 `병합됨`)

---

## 감사 결과 요약

| 상태 | 건수 | 설명 |
|------|:----:|------|
| ✅ OK | 28+ | 이미 회의 반영됨 (screens.json, wiki 화면설계, DS 문서, Figma 가이드 등) |
| 🔧 FIXED | 9 | 이번 감사에서 수정 |
| 📦 스냅샷 | 3 | `notion_raw/` — Notion export 원본, 재빌드 시 덮어씀 |
| ⏳ 수동 | 2 | Figma 프레임 통합 · Hub 업로드(네트워크 시) |

---

## 파일별 상태

### ✅ OK (변경 불필요)

| 파일 | 비고 |
|------|------|
| `docs/screens/screens.json` | SCR-002·006 `병합됨`, 001·005 제목·notes 반영 |
| `docs/screens/screens.md`, `screens-wiki.md`, `screens-devcopilot-*.json` | export 정본과 일치 |
| `docs/wiki/screen-design-figma.md` | DS-02 채택, DS-08 미채택, 병합 표기 |
| `docs/wiki/user-scenarios.md` | 6단계 전체 흐름·SC-002/014/024 반영 |
| `docs/wiki/qa-test-cases.md` | TC-001 SCR-001·005 컨펌 팝업 |
| `docs/wiki/wbs-schedule.md` | Week 3 SCR-001 매장·포장 통합 |
| `docs/wiki/rest-api-spec.md` | 화면 병합과 무관 |
| `docs/design/kiosk-design-system-index.md` | DS-02 채택, DS-08 참고안 |
| `docs/design/SCR_FIGMA_CHECKLIST.md` | 병합됨·Archive 가이드 |
| `docs/design/figma-merge-scr-guide.md` | 6 UI 단계 체크리스트 |
| `docs/_archive/project-history/design-meetings/*` (회의록·취합·변경 이력) | Before/After 의도적 기록 |
| `docs/design/prompts/kiosk-icon-pack-prompt.md` | 6단계·병합 주석 |
| `docs/_archive/notion-audits/hub-notion-sync-checklist.md` | 병합·Notion 반영 안내 |
| `docs/_archive/notion-audits/notion-merge-sync-audit-2026-07-06.md` | Notion MCP 동기화 기록 |

### 🔧 FIXED (이번 수정)

| 파일 | 수정 내용 |
|------|-----------|
| `devcopilot/scenarios_import.json` | SC-001/004/011/020 — SCR-002·006 활성 흐름 제거, 6단계·컨펌 팝업 |
| `devcopilot/sync_notion_scenarios.py` | Hub PUT 패치 동일 반영 (SC-001~004, 011, 014, 020, 024) |
| `devcopilot/gen_exports_from_api.py` | 전체 흐름 mermaid 6단계 |
| `devcopilot/import_in_browser.generated.js` | `generate_browser_script.py` 재생성 |
| `asak-data/scripts/notion_data.json` | FWD-CART-001, FWD-PAY-001, TC-001 steps |
| `asak-data/scripts/gen_wiki_markdown.py` | 2026-07-06 회의 § 6 UI 단계 문구 |
| `docs/wiki/requirements-definition.md` | gen_wiki 재생성 |
| `docs/wiki/meeting-deliverables-checklist.md` | gen_wiki 재생성 |
| `docs/wiki/asak-planning-summary.md` | 고객 흐름 6 UI 단계 |

### 📦 스냅샷 (수정 안 함)

| 파일 | 이유 |
|------|------|
| `asak-data/scripts/notion_raw/*.json` | Notion MCP export 캐시 — `build_notion_data.py` 입력 |
| `asak-data/scripts/scenario_props.json` | 레거시 props — `notion_data.json`이 정본 |
| `asak-data/scripts/gen_embedded_pages.py` | embedded 페이지 시드 — 별도 Notion 동기화 시 갱신 |

---

## 검색 패턴 점검

| 패턴 | docs/ 범위 | 결과 |
|------|------------|------|
| `SCR-002` 활성 화면 | wiki·design | ✅ 병합됨 표기만 |
| `SCR-006` 별도 주문확인 | wiki·design | ✅ 병합됨·팝업만 |
| `8 UI` / `8단계` 고객 흐름 | design 변경 이력 Before § | ✅ 의도적 (Before) |
| `DS-08` 채택 | 전체 | ✅ 미채택 참고안만 |
| 구형 mermaid (002→006) | devcopilot | 🔧 FIXED |

---

## Hub / Notion 후속

**2026-07-06 감사 직후 Hub 반영 완료**:
- Wiki #9 요구사항 정의서 (FWD-CART-001·FWD-PAY-001)
- Wiki #15 회의록 및 최종 배포 검증 (6 UI 단계)
- Scenarios SC-001~024 (`sync_notion_scenarios.py` 24/24 OK)

```bash
# Wiki (요구사항·회의록 갱신분)
python asak-data/scripts/upload_wiki.py --title "ASAK 요구사항 정의서" --file docs/wiki/requirements-definition.md
python asak-data/scripts/upload_wiki.py --title "ASAK 회의록 및 최종 배포 검증" --file docs/wiki/meeting-deliverables-checklist.md

# 시나리오 Hub (선택)
python devcopilot/sync_notion_scenarios.py

# 화면 (이미 반영됐다면 생략 가능)
python asak-data/scripts/upload_screens_api.py
```

**Figma 수동**: [figma-merge-scr-guide.md](../legacy-ds02-scr/figma-merge-scr-guide.md) 체크리스트

---

## 관련 문서

- [screen-design-changes-2026-07-06.md](../../../_archive/project-history/design-meetings/screen-design-changes-2026-07-06.md)
- [notion-merge-sync-audit-2026-07-06.md](../../../_archive/notion-audits/notion-merge-sync-audit-2026-07-06.md)
