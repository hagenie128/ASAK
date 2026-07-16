> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Historic 2026-07-06 Hub/Notion checklist with superseded SCR-020/021 guidance.
> Canonical Replacement: `docs/wiki/DEV_COPILOT_WBS2_2026-07-16.md`
> Original Path: `docs/team/hub-notion-sync-checklist.md`

# Hub–Notion 동기화 점검 체크리스트

> DevCopilot Hub(workspace 2) ↔ Notion ↔ repo 감사 경고 해소 가이드 (2026-07-06)

## 1. SCR-020/021 Figma URL (19/21)

**증상**: Hub Screens에 Figma 링크 19/21 — SCR-020·021만 비어 있음.

**원인**: `docs/screens/screens.json`에 SCR-020/021은 있으나 `figma_url`이 빈 문자열. Figma `kiosk_design`에 해당 프레임이 아직 없음.

**자동**: repo에서 수정 불가 (Figma 프레임 필요).

**수동**:
1. Figma `kiosk_design`에 `SCR-020 영수증 출력 여부 선택`, `SCR-021 포인트·쿠폰 적립` 프레임 생성
2. 링크 동기화 + Hub 업로드:
   ```bash
   FIGMA_TOKEN=... python asak-data/scripts/sync_figma_links.py --all
   python asak-data/scripts/upload_screens_api.py
   ```
3. Wiki 5·16 반영: `python asak-data/scripts/gen_wiki_markdown.py` 후 `python asak-data/scripts/upload_wiki.py --title "ASAK 화면 설계 및 Figma 연동" --file docs/wiki/screen-design-figma.md`

---

## 2. Hub 화면명 REQ 라벨 (21/21)

**증상**: Screens 탭 `name`에 `(FWD-UI-002)` 등 primary REQ 없음.

**자동 수정됨**:
- `export_screens.py` — DevCopilot export 시 `name`에 REQ suffix 포함
- `upload_screens_api.py` — 업로드 시 `SCR_REQ_MAP` primary REQ 적용

**Hub 반영**:
```bash
python asak-data/scripts/export_screens.py
python asak-data/scripts/upload_screens_api.py
# 또는 REQ+Wiki 일괄:
python asak-data/scripts/sync_req_screen_links.py
```

---

## 3. Wiki DS-01~08 + 회의록 인덱스

**증상**: Wiki 5에 DS 표·회의 인덱스 누락.

**자동 수정됨**: `docs/wiki/screen-design-figma.md`(DS-02 채택·DS-08 참고안), `docs/wiki/meeting-deliverables-checklist.md`(2026-07-06 회의·병합 체크)

**Hub 업로드**:
```bash
python asak-data/scripts/gen_wiki_markdown.py
python asak-data/scripts/upload_wiki.py --title "ASAK 화면 설계 및 Figma 연동" --file docs/wiki/screen-design-figma.md
python asak-data/scripts/upload_wiki.py --title "ASAK 회의록 및 최종 배포 검증" --file docs/wiki/meeting-deliverables-checklist.md
```

---

## 4. 2026-07-06 화면 병합 (SCR-001+002, SCR-005+006)

**결정**: 홈에 매장/포장 통합, 장바구니·주문확인 통합, DS-02 채택.

**자동 반영됨** (2026-07-06):
- `docs/screens/screens.json` · `SCR_REQ_MAP` · Wiki · Hub Screens 21/21
- [screen-design-changes-2026-07-06.md](../design/meetings/screen-design-changes-2026-07-06.md)

**Notion 반영됨** (2026-07-06 MCP 동기화):
- SCR DB `상태` 옵션에 **병합됨** 추가
- SCR-001「홈 (매장·포장)」·SCR-005「장바구니·주문확인」제목·속성·본문
- SCR-002·006 → `병합됨` + 리다이렉트 본문
- SCR-004·007·011·012 회의 메모 반영
- [디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) DS-02 채택 콜아웃
- [회의 인덱스](https://app.notion.com/p/39551ef04f0b8190b76ae4b48b8497ac) 변경 이력 링크

**수동**:
- Figma — DS-02 적용, 002/006 프레임 통합

---

## 5. notion_data.json screens 배열 비어 있음

**증상**: `asak-data/scripts/notion_data.json`에 `"screens": []`.

**자동 수정됨**: `build_notion_data.py`가 `docs/screens/screens.json`에서 21건 로드.

**재생성**:
```bash
python asak-data/scripts/export_screens.py   # screens.json 최신화 (Notion raw 있을 때)
python asak-data/scripts/build_notion_data.py
```

---

## 6. WBS 건수 35→37

**증상**: `wbs-schedule.md` 헤더 35건 — WBS-EXT-001/002 미포함.

**자동 수정됨**: WBS-001~036(**WBS-033 건너뜀**) + WBS-EXT-001/002 = **37건**.

**수동 (Notion)**:
- `[삭제요망] 장바구니 서버 검증` (WBS-EXT-001)
- `[삭제요망] 관리자 결제수단 설정` (WBS-EXT-002)  
→ Notion WBS DB에서 **보관(archive)** 처리 권장 (repo export에는 남아 있음)

**재생성·업로드**:
```bash
python asak-data/scripts/gen_wiki_markdown.py
python asak-data/scripts/upload_wiki.py --title "ASAK WBS 및 일정 계획" --file docs/wiki/wbs-schedule.md
python asak-data/scripts/devcopilot_upload.py --data-only   # tasks Hub 반영
```

---

## 전체 재점검

```bash
python asak-data/scripts/full_mapping_audit.py
python asak-data/scripts/req_link_gap_audit.py
```

Hub API 헤더: `x-user-username: hagenie128` (스크립트 기본값).
