> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Completed Notion merge and synchronization audit.
> Canonical Replacement: `docs/wiki/DEV_COPILOT_WBS2_2026-07-16.md`
> Original Path: `docs/archive/design-audits/notion-merge-sync-audit-2026-07-06.md`

# Notion 병합·6단계·DS-02 반영 감사 — 2026-07-06

> **감사일**: 2026-07-06  
> **재감사 완료**: 2026-07-06 (후속 MCP + Git)  
> **근거**: [screen-design-changes-2026-07-06.md](../design/meetings/screen-design-changes-2026-07-06.md) · `docs/screens/screens.json`  
> **결론**: Notion 시나리오·매트릭스·Git 체크리스트 반영 완료. **Figma frame 실작업만** 디자이너 수동.

## 회의 확정 사실 (정본)

| 항목 | 내용 |
|------|------|
| SCR-002 | SCR-001「홈 (매장·포장)」에 병합 · DB 상태 `병합됨` |
| SCR-006 | SCR-005「장바구니·주문확인」에 병합 · 컨펌 팝업 · DB 상태 `병합됨` |
| 고객 UI | **6단계** (홈·매장/포장 → 메뉴 → 옵션 → 장바구니·주문확인 → 결제 → 완료) |
| DS | **DS-02 Modern Minimal** 프로덕션 채택 |
| ID 체계 | SCR 21개 ID 유지 (002·006 참조용) |

---

## 감사 결과 요약 (재감사 후)

| 영역 | 반영 여부 | 조치 |
|------|:--------:|------|
| **04. 화면 설계 Hub** | ✅ OK | 이미 반영 |
| **SCR DB** | ✅ OK | 002/006 `병합됨` |
| **시나리오 DB — 핵심·잔여** | ✅ 수정 완료 | SC-005 `관련 화면` SCR-006→005 반영. 나머지 행 샘플 점검 — SCR-002/006 활성 참조 없음 |
| **Figma SCR×매트릭스** | ✅ 수정 완료 | 체크리스트 표 + 회의 매트릭스 001/002/005/006 병합 상태 갱신 |
| **브랜드 · Trend 컬러** | ✅ 안내 추가 | 병합 callout (벤치마크 표 SCR-002/006은 패턴 참고용) |
| **Git SCR_FIGMA_CHECKLIST** | ✅ 수정 완료 | 6단계·병합·DS-02·Archive |
| **figma-rename-scr-plugin** | ✅ 수정 완료 | 병합됨/Archive 스킵 · 레거시 이름 매핑 |
| **figma-merge-scr-guide.md** | ✅ 신규 | Figma 수동 병합 단계 |
| **sync_figma_links.py** | ⏸️ 미실행 | `.env`에 FIGMA_TOKEN 없음 |
| **Figma kiosk_design 파일** | ❌ 수동 필요 | frame 통합·DS-02 적용 — [가이드](../design/figma-merge-scr-guide.md) |
| **DevCopilot Wiki** | ⏸️ 미실행 | `upload_screens_api.py` (repo는 반영됨) |

---

## MCP로 수정한 페이지 (후속 2026-07-06)

| 페이지 | page_id | 변경 |
|--------|---------|------|
| SC-005 결제 실패 흐름 | `39151ef04f0b8136afedfbe033869bc0` | `관련 화면` SCR-006→SCR-005 |
| Figma SCR×매트릭스 | `39451ef04f0b81849dc7d81f8106b5ad` | 체크리스트·회의 매트릭스 002/005/006 |
| 브랜드 · Trend 컬러 | `39451ef04f0b814a9447f6fbf171b3b7` | 병합 안내 callout |

---

## 아직 Figma에서만 필요 (디자이너 클릭)

1. **SCR-001** — `OrderTypeTile`로 매장/포장 통합 (002 내용 흡수)
2. **SCR-005** — `ModalConfirm` 컨펌 팝업 (006 기능 흡수)
3. **SCR-002·006** — Archive 이동 + `[병합됨→…]` 이름
4. **DS-02** 컴포넌트 인스턴스 적용 (`figma-create-ds02-components-plugin`)
5. (선택) `FIGMA_TOKEN` 설정 후 `sync_figma_links.py --all`

상세: [figma-merge-scr-guide.md](../design/figma-merge-scr-guide.md)

---

## 검색 키워드 (감사에 사용)

- `SCR-002` 별도 화면 · `먹고가기/포장 선택`
- `SCR-006` 주문 확인 별도
- `8단계` · `8 UI`
- `DS-02` · `Modern Minimal`

**재감사**: Figma 수동 작업 완료 후 `sync_figma_links.py --all` 1회.
