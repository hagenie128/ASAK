# ASAK 파일·문서 네이밍 규칙

> 갱신: **2026-07-20**  
> **파일명만 보고** 종류·역할·시점을 추측할 수 있게 하는 규칙입니다.  
> 검사 스크립트: [`asak-data/scripts/check-filename-convention.ps1`](../asak-data/scripts/check-filename-convention.ps1)

---

## 1. 한 줄 요약

| 항목 | 규칙 |
|---|---|
| 기본 | **`kebab-case`** (소문자 + 하이픈) |
| 날짜 | 스냅샷·감사·WBS 정본 → **접미사 `-YYYY-MM-DD`** |
| 정렬 | 순서가 중요한 폴더 → **`NN-` 접두** (두 자리) |
| 도메인 | Figma/design → **`figma-` 접두** 권장 |
| 언어 | 파일명 **영문만** · 본문 H1은 한국어 가능 |

---

## 2. 파일명 문법 (읽는 법)

```text
[NN-][domain-]{topic}[-{qualifier}][-{YYYY-MM-DD}].{ext}
```

| 조각 | 필수 | 예 | 의미 |
|---|---|---|---|
| `NN-` | 선택 | `02-`, `00-` | 폴더 안 읽는 순서 |
| `domain-` | 선택 | `figma-`, `wbs-` | 주제 영역 (폴더와 맞출 것) |
| `topic` | **필수** | `kiosk-implementation` | 무엇에 관한 파일인지 |
| `qualifier` | 선택 | `unified-corrective-execution-plan` | 세부 종류 |
| `YYYY-MM-DD` | 선택 | `2026-07-17` | **그날 기준 스냅샷** (living doc에는 붙이지 않음) |
| `ext` | **필수** | `.md`, `.json`, `.css` | 형식 |

### 파일명만 보고 판단하기

| 파일명 패턴 | 추론 |
|---|---|
| `README.md` | 그 **폴더 입구** |
| `START_HERE.md` | 전체 문서 **단일 진입** |
| `00-start-here.md` | implementation_guide **첫 번째** |
| `figma-*.md` | design / Figma 실행·QA |
| `wbs-v2-2026-07-16.md` | **WBS 정본** (날짜 = 그 버전 기준일) |
| `current-implementation-map-2026-07-16.md` | **코드 실측 스냅샷** |
| `*-2026-07-18.md` | 7/18 시점 기록·감사·handoff |
| `document-*-2026-07-20.md` | **문서 메타** (인벤토리·태그·네이밍) |
| `_archive/` 아래 | **실행 금지** 이력 |

---

## 3. 폴더별 규칙

### `docs/` (중앙)

| 폴더 | 패턴 | 예 |
|---|---|---|
| 루트 | `START_HERE.md`, `document-{role}-{date}.md` | `document-inventory-slim-2026-07-20.md` |
| `design/` | `figma-{topic}[-date].md` | `figma-guide.md`, `figma-token-report.md` |
| `wiki/` | `{topic}.md` 또는 `wbs-{ver}-{date}.md` | `wbs-v2-2026-07-16.md` |
| `planning/` | `{topic}[-{date}].md` | `app-implementation-hub.md` |
| `governance/` | `{topic}-{date}.md` | `canonical-contract-decisions-2026-07-16.md` |
| `implementation_guide/` | `NN-{topic}.md`, `feature-lookup.md` | `02-kiosk-implementation.md` |
| `guides/` | `NN-{topic}.md`, `09-11-moved.md` | `01-team-setup.md` |
| `operations/setup/` | `{topic}.md` | `getting-started.md` |
| `architecture/` | `{topic}-{date}.md` | `document-code-gap-report-2026-07-16.md` |
| `screens/` | `{topic}.{json\|md}` | `screens.json` |
| `_archive/` | **rename 최소** · 배너로 Historical | |

### 저장소 로컬 (`#repo-local`)

| 위치 | 패턴 | 예 |
|---|---|---|
| `{Kiosk,Admin}/docs/` | `{topic}-{YYYY-MM-DD}.md` | `figma-ui-handoff-2026-07-18.md` |
| 루트 | `IMPLEMENTATION_PLAN.md`, `STRUCTURE_GUIDE.md` | 저장소 실행 관례 (고정) |
| 워크스페이스 루트 | `ui-index.md`, `ROOT_FOLDER_MAP.md` | living index · 지도 |

### `product_bible/`

- Pack 내부는 **기존 Pack README 규칙** · 대량 rename **금지**
- 신규만 kebab-case 권장

---

## 4. 날짜 접미사 — 언제 붙이나

| 붙인다 | 붙이지 않는다 |
|---|---|
| WBS·구현맵·감사 **정본 스냅샷** | `figma-guide.md` (living) |
| repo handoff·parity log | `app-implementation-hub.md` |
| 1회성 계획·register | `README.md`, `00-start-here.md` |
| document inventory / manifest | `ui-index.md` |

**같은 주제 새 버전** → 새 날짜 파일 추가 + 구 파일 Historical 배너 (구 파일 rename 금지보다 배너 우선).

---

## 5. 고정 예외 (rename 하지 않음)

| 파일 | 이유 |
|---|---|
| `README.md` | 폴더 기본 진입 |
| `START_HERE.md` | 전역 허브 고정명 |
| `IMPLEMENTATION_PLAN.md` | GitHub·팀 관례 |
| `STRUCTURE_GUIDE.md` | 저장소 관례 |
| `AGENTS.md`, `CLAUDE.md` | 도구 진입점 |
| `_archive/**` 본문 | 이력 보존 (링크만 갱신) |

---

## 6. 금지 · 피할 것

| 나쁜 예 | 이유 |
|---|---|
| `FIGMA_GUIDE.md`, `GETTING_STARTED.md` | UPPER_SNAKE / SCREAMING |
| `Admin Mock Binding.md` | 공백 |
| `figma_fix_plan.md` | snake_case |
| `FIGMA-TOKEN-REPORT.md` | 대문자 + 혼합 (→ `figma-token-report.md`) |
| `cluade` 오타 | → `claude` |
| 상태를 파일명에 | `FINAL`, `v2`, `UNIFIED` 남발 → 폴더·배너로 |

---

### 데이터·스크립트·워크로그 (별도 관례)

| 영역 | 관례 | 비고 |
|---|---|---|
| `asak-data/seed*.json` | `snake_case` | DB 시드 · rename 금지 |
| `asak-data/scripts/*_report.json` | `snake_case` | 파이프라인 산출물 |
| `worklog/` | `YYYY-MM-DD-*.md` | 날짜 접두 한국어 파일명 허용 |
| `docs/notion/` | Notion export | 스크립트 입력 · 그대로 유지 |
| `.github/` | GitHub 템플릿 | `PULL_REQUEST_TEMPLATE.md` 등 고정 |

**사람이 읽는 docs/ · repo docs/ 만** 위 kebab-case 규칙 적용.

| 종류 | 규칙 | 예 |
|---|---|---|
| JSON 산출물 | kebab-case | `screens.json`, `figma-links.template.json` |
| CSS 토큰 | kebab-case | `tokens.css`, `commonStyle.css` (기존 코드명 유지) |
| 스크립트 | kebab-case | `check-filename-convention.ps1` |
| 이미지 | `{context}-{desc}-{WxH}.png` | `2026-07-19-kiosk-home-1080x1920.png` |

---

## 8. 새 파일 만들 때 체크리스트

1. **폴더**가 역할을 말하는가? (design / wiki / planning …)
2. **kebab-case**인가?
3. **스냅샷**이면 `-YYYY-MM-DD` 붙였는가?
4. **순서**가 필요하면 `NN-` 붙였는가?
5. **design**이면 `figma-` 접두를 고려했는가?
6. 맨 위 **배너** (`Current` / `Historical` / `→ 대신 X`) 달았는가?
7. [document-inventory-slim](document-inventory-slim-2026-07-20.md) KEEP 목록에 넣을 필요가 있는가?

---

## 9. 2026-07-20 적용 현황

| 영역 | 상태 |
|---|---|
| `docs/design/` active | ✅ kebab-case |
| `docs/implementation_guide/` | ✅ `NN-{topic}.md` |
| `docs/operations/setup/` | ✅ |
| 워크스페이스 `ui-index.md` | ✅ |
| `product_bible/` Pack 본문 | ⏸ 유지 |
| `_archive/` deep history | ⏸ 배너·링크만 |

관련: [document-tag-index-2026-07-20.md](document-tag-index-2026-07-20.md) · [document-inventory-slim-2026-07-20.md](document-inventory-slim-2026-07-20.md)
