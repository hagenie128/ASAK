# ASAK 문서 태그 인덱스

> **목적:** 어떤 문서를 “정본/현재/참고/보관”으로 볼지 한눈에 찾기  
> **갱신:** 2026-07-17  
> **삭제 없음:** 중복·구버전은 `_archive`로만 이동

## 태그 뜻

| 태그 | 의미 | 구현에 써도 되나 |
|---|---|---|
| `#canonical` | 제품·계약 **정본** | ✅ 최우선 |
| `#current` | 지금 작업 기준 | ✅ |
| `#wip` | 정리·작성 진행 중 | ⚠️ 초안, UNIFIED와 함께 |
| `#reference` | 온보딩·가이드·위키 | △ 정본과 충돌 시 정본 우선 |
| `#legacy` | 과거 맥락·감사 기록 | ❌ 구현 완료 근거로 쓰지 않음 |
| `#archive` | 보관(삭제 아님) | ❌ |
| `#repo-local` | Kiosk/Admin/back 저장소 안 문서 | ✅ 해당 저장소 실행용 |

---

## 1. 워크스페이스 루트 (`ASAK-workspace/`)

| 경로 | 태그 | 설명 |
|---|---|---|
| [README.md](../../README.md) | `#reference` | 멀티 저장소 작업공간 안내 |
| [AGENTS.md](../../AGENTS.md) / [CLAUDE.md](../../CLAUDE.md) | `#current` | 에이전트 공통 지침 |
| [한국어_명령어_표.md](../../한국어_명령어_표.md) | `#current` | 단축 명령 |
| [ASAK_AGENT_KIT_COMMANDS.md](../../ASAK_AGENT_KIT_COMMANDS.md) | `#reference` | 에이전트 키트 명령 |
| [docs/README.md](../../docs/README.md) | `#reference` | → `ASAK/docs` 포인터 |

---

## 2. 중앙 문서 허브 (`ASAK/docs/`)

진입점: [README.md](./README.md)

### `#canonical` — 정본

| 경로 | 설명 |
|---|---|
| [product_bible/](./product_bible/) Pack 01~12 | 제품·화면·컴포넌트·QA·구현 정본 |
| [governance/canonical-contract-decisions-2026-07-16.md](./governance/canonical-contract-decisions-2026-07-16.md) | API·Admin 경로·필드 계약 |
| [governance/product-bible-index-2026-07-16.md](./governance/product-bible-index-2026-07-16.md) | Bible 인덱스 |

### `#current` — 지금 구현·QA

| 경로 | 설명 |
|---|---|
| [implementation_guide/00_START_HERE.md](./implementation_guide/00_START_HERE.md) | 구현 가이드 시작 |
| [planning/current-implementation-map-2026-07-16.md](./planning/current-implementation-map-2026-07-16.md) | 현재 구현 지도 |
| [planning/implementation-priority-2026-07-16.md](./planning/implementation-priority-2026-07-16.md) | 우선순위 |
| [architecture/document-code-gap-report-2026-07-16.md](./architecture/document-code-gap-report-2026-07-16.md) | 문서↔코드 갭 |
| [design/FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md](./design/FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md) | Figma QA 통합본 |
| [design/ASAK_FIGMA_INTEGRATED_AUDIT.md](./design/ASAK_FIGMA_INTEGRATED_AUDIT.md) | 05-C/06-C 통합 감사 |
| [operations/setup/](./operations/setup/) | 설치·온보딩·MCP |

### `#wip`

| 경로 | 설명 |
|---|---|
| [design/FIGMA_QA_IMPLEMENTATION_FINAL_cluade_2026-07-17.md](./design/FIGMA_QA_IMPLEMENTATION_FINAL_cluade_2026-07-17.md) | Claude 재실측본 (정리 중) |

### `#reference`

| 경로 | 설명 |
|---|---|
| [guides/](./guides/) | 팀 온보딩·개발 가이드 |
| [wiki/](./wiki/) | DevCopilot 산출물·요약 |
| [screens/](./screens/) | SCR 표·DevCopilot import |
| [team/](./team/) | Notion hub 동기화 체크리스트 |
| [documentation-management/](./documentation-management/) | 문서 구조·인벤토리 계획 |
| [governance/legacy-and-reference-index-2026-07-16.md](./governance/legacy-and-reference-index-2026-07-16.md) | 레거시/참고 분류 |
| [governance/document-status-manifest-2026-07-16.md](./governance/document-status-manifest-2026-07-16.md) | 폴더 상태 정책 |

### `#legacy` / `#archive`

| 경로 | 설명 |
|---|---|
| [`notion/`](./notion/) | stub만 — 본문은 [`_archive/notion-export/`](./_archive/notion-export/) |
| [`_archive/wiki-secondary/`](./_archive/wiki-secondary/) | Wiki 부가 문서 |
| [`product_bible/_archive/`](./product_bible/_archive/) | 이전 Pack |
| [`design/_archive/`](./design/_archive/) | Figma 중복·도구·D1·토큰 |
| [`_archive/`](./_archive/) | notion / wiki-secondary / team / screens |

---

## 3. 저장소별 문서 (`#repo-local`)

| 저장소 | 주요 문서 | 중앙 정본 연결 |
|---|---|---|
| **ASAK-Kiosk** | `README.md`, `IMPLEMENTATION_PLAN.md`, `src/contracts/**`, `docs/figma-mcp-implementation-guide.md` | Pack 12 + API Contract |
| **ASAK-Admin** | `README.md`, `docs/**`, `IMPLEMENTATION_PLAN.md`, `src/contracts/**` | Pack 12 Admin + Canonical routes |
| **ASAK-back** | `README.md`, `IMPLEMENTATION_PLAN.md` | Pack 11 |
| **ASAK/worklog** | `worklog/README.md` | guides 03 + Notion 일일 로그 |

> Kiosk 안의 Admin 스캐폴드는 `#legacy` (정본 구현은 ASAK-Admin).

---

## 4. 주제 → 바로 가기

| 하고 싶은 일 | 먼저 열 문서 |
|---|---|
| API/필드 계약 확인 | `#canonical` Canonical Contract → Pack 해당 API |
| 화면 ID·상태 | Pack 07 Screen Registry → design QA UNIFIED → screens |
| Figma 수정 우선순위 | design UNIFIED / INTEGRATED_AUDIT |
| OptionCard D1 | design OptionCard SPEC + D1-B Work Order |
| 키오스크 코딩 | implementation_guide 02 → ASAK-Kiosk README |
| 관리자 코딩 | implementation_guide 03 → ASAK-Admin docs |
| 백엔드 코딩 | implementation_guide 04 → ASAK-back + Pack 11 |
| 팀 온보딩 | operations GETTING_STARTED → guides 01 |
| 학원 Wiki 업로드 | wiki/README |
| 옛 Notion/회의 | notion (`#archive`/`#legacy`) — Bible과 충돌 시 Bible |

---

## 5. 루트·저장소 겹침 (요약)

자세한 표: 워크스페이스 [`ROOT_FOLDER_MAP.md`](../../ROOT_FOLDER_MAP.md)

| 겹침 | 정본 | 나머지 |
|---|---|---|
| guides 07~11 vs implementation_guide | `implementation_guide/` | guides는 stub + `_archive/guides-dev-overlap` |
| screens-wiki vs wiki/screens | Pack 07 + `screens.md` + wiki figma | `_archive/screens-legacy` |
| Kiosk/Admin Figma MCP 가이드 | 저장소별 유지 + 중앙 design UNIFIED 링크 | 서로 화면 범위만 다름 |
| `.agents` vs `.claude` skills (15개 동일) | `asak-agent-kit` 배포 원본 | 루트 실행본 — **삭제 금지** |
| `AGENTS.md` ≈ `CLAUDE.md` | 둘 다 유지 (도구 진입점) | 내용 거의 동일 |
| wiki API vs Bible contracts | Product Bible API Contract | wiki는 학원 산출물 |

## 6. 정리 규칙 (앞으로)

1. **새 분석/QA 초안** → 파일명에 `날짜_작성자` → 합치면 UNIFIED/최종만 루트, 원본은 `_archive`.
2. **일회성 Agent 프롬프트** → 작업 끝 즉시 `design/_archive/`.
3. **삭제 금지** → 무조건 `_archive` 이동. 삭제 필요 시 사람 승인.
4. **정본 복제 금지** → Kiosk/Admin에 Bible 내용을 복사하지 말고 링크.
5. **guides에 구현 상세 추가 금지** → `implementation_guide` / Pack에 쓴다.
