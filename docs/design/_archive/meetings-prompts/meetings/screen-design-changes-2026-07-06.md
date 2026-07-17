# 화면 설계 변경 이력 — 2026-07-06 회의 반영

> **근거**: [screen-design-meeting-minutes-2026-07-06.md](./screen-design-meeting-minutes-2026-07-06.md)  
> **적용일**: 2026-07-06  
> **범위**: SCR-001~021 (ID 유지, 병합 2건)

---

## 한 줄 요약

**DS-02 Modern Minimal** 채택. **SCR-002→001**, **SCR-006→005** 기능 병합(ID 유지·`병합됨` 표기). 고객 흐름 8단계→6단계 UI. 총 SCR **21개 유지**.

---

## 화면 구조 Before / After

### Before (회의 전)

| 순서 | ID | 화면명 | 비고 |
|:--:|-----|--------|------|
| 1 | SCR-001 | 홈 화면 | 주문 시작만 |
| 2 | SCR-002 | 먹고가기 / 포장 선택 | 별도 화면 |
| 3 | SCR-003 | 메뉴 선택 | |
| 4 | SCR-004 | 메뉴 상세 / 옵션 선택 | |
| 5 | SCR-005 | 장바구니 | |
| 6 | SCR-006 | 주문 확인 | 별도 화면 |
| 7 | SCR-007 | 결제 | |
| 8 | SCR-008 | 주문 완료 | |

**고객 흐름**: 홈 → 먹고가기/포장 → 메뉴 → 옵션 → 장바구니 → 주문확인 → 결제 → 완료 (8 UI 단계)

### After (회의 후)

| 순서 | ID | 화면명 | 상태 | 비고 |
|:--:|-----|--------|------|------|
| 1 | **SCR-001** | **홈 (매장·포장)** | 활성 | SCR-002 흡수 |
| — | SCR-002 | 먹고가기 / 포장 선택 | **병합됨** | → SCR-001 |
| 2 | SCR-003 | 메뉴 선택 | 활성 | |
| 3 | SCR-004 | 메뉴 상세 / 옵션 선택 | 활성 | 알레르기·칼로리 표시 |
| 4 | **SCR-005** | **장바구니·주문확인** | 활성 | SCR-006 흡수, 컨펌 팝업 |
| — | SCR-006 | 주문 확인 | **병합됨** | → SCR-005 |
| 5 | SCR-007 | 결제 | 활성 | 로딩 필수 |
| 6 | SCR-008 | 주문 완료 | 활성 | 주문번호 표시 |

**고객 흐름**: 홈(매장·포장) → 메뉴 → 옵션 → 장바구니·주문확인(팝업) → 결제(로딩) → 완료 (6 UI 단계)

> Week 5 MVP 범위는 여전히 **SCR-001~008 ID** 기준이며, 002·006은 참조용으로 DB에 남깁니다.

---

## 번호 체계 결정

| 옵션 | 채택 | 이유 |
|------|:----:|------|
| ID 재번호(18개로 축소) | ✗ | Notion URL·Hub·TC 추적성 파손 |
| 병합 ID `병합됨` 유지 | **✓** | 21개 유지, 회의「유지·증가」 방향, 하위 호환 |

---

## 화면별 변경 상세

| ID | 변경 내용 |
|----|-----------|
| SCR-001 | 제목·출력·REQ 병합. 매장/포장 선택 UI 통합 |
| SCR-002 | `병합됨` — SCR-001로 리다이렉트 |
| SCR-004 | 알레르기·칼로리 표시 위치 명시 (장바구니 아님) |
| SCR-005 | 주문확인 통합, 추가 제안 하단, API-005·주문 생성 |
| SCR-006 | `병합됨` — SCR-005로 리다이렉트 |
| SCR-007 | 결제 승인 로딩 상태 필수 |
| SCR-012 | 팝업·토스트 오버레이 (전체 화면 대안) |
| SCR-011 | 품절 변경 후 메뉴 상태 목록 |
| SCR-019 | 매출 평균·시간대별·판매 제품 통계 확장 |
| SCR-020, 021 | Phase 2 후순위 (변경 없음, 명시 유지) |

---

## 디자인 시스템

| 항목 | Before | After |
|------|--------|-------|
| 프로덕션 DS | 미정 (02·04 교차) | **DS-02 Modern Minimal** |
| DS-08 | — | 02+04 하이브리드 **미채택 참고안** |
| 고객/관리자 DS | 분리 검토 | **일단 통합** |

---

## 수정된 파일

| 영역 | 파일 |
|------|------|
| 화면 정본 | `docs/screens/screens.json`, `screens.md`, `screens-wiki.md`, `screens-devcopilot-*.json` |
| REQ 매핑 | `asak-data/scripts/req_link_maps.py` |
| Export | `asak-data/scripts/export_screens.py`, `screens_notion_snapshot.json` |
| Wiki 생성 | `asak-data/scripts/gen_wiki_markdown.py` → `docs/wiki/*.md` |
| DS | `docs/design/kiosk-design-system-index.md` (기존 반영) |
| Figma 플러그인 | `docs/design/figma-rename-scr-plugin/code.js` |
| 아이콘 프롬프트 | `docs/design/prompts/kiosk-icon-pack-prompt.md` |
| 회의록 | 본 문서, `meeting-deliverables-checklist.md` |
| **문서 감사** | [design-doc-merge-audit-2026-07-06.md](../../team/design-doc-merge-audit-2026-07-06.md) |

---

## Hub / Notion 상태

| 대상 | 상태 | 비고 |
|------|------|------|
| DevCopilot Screens API | 스크립트 실행 후 확인 | `upload_screens_api.py` |
| DevCopilot Wiki #16 | 동일 스크립트 | `screens-wiki.md` |
| Notion 04 SCR DB | **수동 필요** | MCP/스크립트로 페이지 본문 미동기화 |
| Figma | **수동 필요** | 아래 § |

---

## Figma 수동 작업

1. **DS-02** 프레임을 SCR-001~008 와이어에 적용
2. SCR-002 프레임 내용을 SCR-001에 통합 후 002는 Archive 또는 `[병합됨]` 라벨
3. SCR-006을 SCR-005에 통합 — **컨펌 팝업** 컴포넌트 추가
4. SCR-005 하단 **추가 제안 상품** 섹션
5. SCR-007 **결제 로딩** 오버레이
6. SCR-012 **팝업/토스트** 패턴 (전체 화면 대신)
7. `figma-rename-scr-plugin` 재실행으로 레이어 이름 정리

---

## 테스트 케이스 영향

| TC | 변경 |
|----|------|
| TC-001 | SCR-002 → SCR-001, 주문확인 → SCR-005 컨펌 팝업 |
| TC-002 | 장바구니·주문확인 통합 흐름 |
| TC-004 | 실패 안내 팝업/토스트 |
