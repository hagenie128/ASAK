# 저장소 정리 인벤토리 — 2026-07-16

> **⚠️ HISTORICAL — 실행에 쓰지 마세요.**  
> → 대신 [**START_HERE**](../START_HERE.md) · [DOC_INVENTORY_SLIM](../DOC_INVENTORY_SLIM.md) · [DOCUMENT_STATUS_MANIFEST](DOCUMENT_STATUS_MANIFEST.md)  
> 범위: `ASAK` 문서/데이터만. 앱 소스 이동 계획 없음. 파일 삭제 없음.
>
> 상태: 읽기 전용 인벤토리 완료 후 Batch A만 실행했습니다. 파일은 삭제하지 않았습니다. `docs/wiki/` 아래 현재 DevCopilot/WBS 미추적(untracked) 파일은 보호 대상이며 모든 이동에서 제외합니다.

## 방법 및 범위

인벤토리는 저장소 전체 파일 열거(`.git` 제외), SHA-256 중복 그룹, 현재 텍스트 참조 검색, 스크립트 입출력 점검, JSON 매니페스트, 최근 Git 이력을 사용했습니다. 아래 "마지막 사용"은 현재 가이드/README 참조, 내부 스크립트 의존성, 또는 명시적으로 날짜가 있는 이력 기록 중 하나를 의미합니다. 외부 API가 최근에 실행되었다는 **증거는 아닙니다**.

| 지표 | 결과 |
| --- | ---: |
| 검사한 파일(`.git` 제외) | 1,240 |
| `docs/` | 683 |
| `asak-data/` | 461 |
| `worklog/` | 47 |
| `data-pipeline/` | 23 |
| 기타 루트/설정/도구 파일 | 26 |
| 정확 중복 해시 그룹 | 128 |
| 해당 그룹의 추가 파일 | 142 |
| 보호된 미추적 DevCopilot/WBS 파일 | 8개 경로(`docs/wiki/snapshots/` 포함) |
| 확인된 자격 증명(credential) 시그니처 | 0 |

### 폴더 인벤토리

| 폴더 | 파일 수 | 주 역할 | 분류 | 권장 위치 / 근거 | 위험도 |
| --- | ---: | --- | --- | --- | --- |
| `docs/product_bible/01_*`–`12_*` | 212 | 제품, 화면, 컴포넌트, QA 및 구현 표준 | KEEP_CANONICAL | 그대로 유지; 거버넌스 색인이 현재 기준으로 명명 | 낮음 |
| `docs/product_bible/_archive/` | 58 | 이전 Bible Pack 스냅샷(Pack 3/4/7 사본 포함) | MOVE_TO_ARCHIVE | 사람 승인 후 `docs/_archive/project-history/` 통합 전까지 기존 `_archive` 유지 | 중간 |
| `docs/notion/` | 268 | 스크립트 기반 DevCopilot 소스 입력 및 연결 참조 그래프 | ACTIVE_REFERENCE | 실행 입력 유지; 명시적 이력 Archive/일일 내보내기 20건은 `docs/_archive/notion-export/`로 이동 | 높음 |
| `docs/design/` | 68 | Figma 가이드, 플러그인, 프롬프트, 날짜별 감사 및 에셋 | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION | 활성 가이드/플러그인 유지; 날짜 기준 완료 감사는 `docs/design/_archive/audits/`로 이동 가능 | 중간 |
| `docs/wiki/` | 20 추적 + 8 보호 미추적 경로 | DevCopilot 동기화 소스 및 요약 | KEEP_ACTIVE_TOOL | 그대로 유지; 보호된 현재 WBS 작업은 절대 덮어쓰지 않음 | 높음 |
| `docs/screens/` | 6 | 화면 내보내기/소스 및 DevCopilot 페이로드 | NEEDS_CONFIRMATION | `screens.json`은 활성 소스; 생성된 local-storage/import 페이로드는 보존 여부 결정 필요 | 높음 |
| `docs/team/` | 5 | 팀 결정, 동기화 기록, 날짜별 감사 | MIXED | 2026-07-06 종료 감사 2건은 Batch A에서 이동; 현재 피드백/변경 등록 문서는 유지 | 중간 |
| `docs/guides/`, `operations/`, `planning/`, `architecture/` | 21 | 팀 운영, 설정, 현재 계획, 갭 분석 | KEEP_ACTIVE_TOOL | 그대로 유지하고 Product Bible에 링크 | 낮음 |
| `asak-data/seed/` | 19 | README 및 SQLite/MySQL 로더가 사용하는 현재 긴 이름 샘플 seed | KEEP_CANONICAL | 그대로 유지 | 높음 |
| `asak-data/seed-v3/` | 22 | 짧은 이름 스키마 마이그레이션/로더 코퍼스 | NEEDS_CONFIRMATION | DB 담당자가 정본 스키마를 선택할 때까지 `seed` 옆에 유지 | 높음 |
| `asak-data/images/menu/` | 84 | Kiosk 경로 이미지 에셋 | KEEP_CANONICAL | 그대로 유지; seed 이미지 URL이 경로를 소비 | 높음 |
| `asak-data/images/original/` | 84 | 소스/참조 메뉴 이미지 | KEEP_CANONICAL | 그대로 유지; 배포 메뉴 이미지의 의도적 사본 | 중간 |
| `asak-data/scripts/*.py` | 77 | 이미지, seed, Notion/DevCopilot, 감사 및 마이그레이션 도구 | MIXED | 스크립트 인벤토리 참고; 경로 업데이트 승인 전 호출자 이동 금지 | 높음 |
| `asak-data/scripts/notion_raw/` | 151 | 저장된 Notion 응답 스냅샷 | GENERATED_ARTIFACT / SNAPSHOT | 목표 `asak-data/snapshots/notion/`; Python 경로 업데이트 필요 | 중간 |
| `asak-data/scripts` JSON/Markdown 출력 | 22 | 보고서, 요청 배치, 스냅샷 및 임시 청크 | GENERATED_ARTIFACT / NEEDS_CONFIRMATION | 보고서는 `asak-data/reports/` 목표; 현재 스크립트 출력 경로는 `scripts/` | 중간 |
| `asak-data/schema-backups/` | 1 | 짧은 이름 마이그레이션 전 스키마 증거 | MOVE_TO_ARCHIVE | Batch A에서 Markdown 참조 업데이트와 함께 `asak-data/archive/schema/`로 이동 | 낮음 |
| `worklog/` | 47 | 일일/항목 이력, 템플릿, 캘린더 및 동기화 스크립트 | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION | 캘린더 및 스크립트를 함께 마이그레이션할 때까지 경로 유지 | 높음 |
| `data-pipeline/phase1/` | 23 | 데이터 수집/변환 소스 및 출력 | KEEP_ACTIVE_TOOL | 그대로 유지; 이 단계에서 정리 이동 없음 | 높음 |

### 대량 파일 규칙(기계적으로 동일한 파일의 완전 커버리지)

| 경로 집합 | 개수 | 유형 / 목적 | 참조 또는 실행 상태 | 분류 | 권장 처리 | 이유 / 위험 |
| --- | ---: | --- | --- | --- | --- | --- |
| `asak-data/images/menu/*.png` | 84 | PNG 배포 이미지 | 메뉴 seed URL이 참조 | KEEP_CANONICAL | 유지 | 많은 original과 동일 해시는 의도적 경로별 에셋; 어느 경로든 삭제 시 소비자 깨질 수 있음. 높은 위험. |
| `asak-data/images/original/*.png` | 84 | PNG 소스 이미지 | `apply_original_images.py` 워크플로 사용 | KEEP_CANONICAL | 유지 | 이미지 출처 및 재생성 소스 보존. 중간 위험. |
| `asak-data/scripts/notion_raw/*.json` | 151 | API 응답 스냅샷 | `scripts/notion_raw`를 사용하는 스크립트가 생성/소비 | GENERATED_ARTIFACT | Batch B: Python 경로 업데이트 후 `snapshots/notion/`으로 이동 | 재생성 가능하나 감사 증거로 유용; 현재 경로는 하드코딩됨. |
| `docs/product_bible/_archive/**` | 58 | 아카이브된 Product Bible Pack | 거버넌스 색인에서 명시적 제외 | MOVE_TO_ARCHIVE | 현재 `_archive` 유지; 참조 확인 후 중복 제거만 검토 | 34+ 정확 문서 중복 그룹은 삭제 대상이 아닌 이력 증거. |
| `docs/notion/**` | 268 | 현재 DevCopilot 동기화 입력 및 연결 참조 그래프 | 실행 입력 전용; 정책 정본 아님 | ACTIVE_REFERENCE | Python 동기화 스크립트 및 Export 상대 링크가 이 경로를 읽으므로 유지 | 명시적 Archive/일일 내보내기는 `docs/_archive/notion-export/`로 이동. |
| `worklog/daily/**`, `worklog/entries/**` | 23 비템플릿 기록 | 팀원 작업 이력 | 캘린더, README 및 동기화 도구가 현재 레이아웃에 의존 | KEEP_ACTIVE_TOOL | Batch A에서 이동하지 않음 | 이동 시 현재/아카이브 참여자 결정 및 코드/README 업데이트 필요. |
| `docs/wiki/current-status-baseline.md`, `db-abbreviation-glossary.md`, `db-audit-plan.md`, `devcopilot-sync-report.md`, `future-scope.md`, `traceability-matrix.md`, `wbs-v2.md`, `snapshots/**` | 8 미추적 경로 | 진행 중 DevCopilot/WBS 작업 | 사용자 지시로 보호 | NEEDS_CONFIRMATION | 건드리지 않고 커밋하지 않음 | 현재 작업 파일은 이 정리 커밋에 덮어쓰거나 흡수하면 안 됨. |

## 중복 점검

### 정확히 동일한 콘텐츠 그룹

| 그룹 | 정본 후보 | 중복 | 차이 | 참조 상태 | 권장 처리 |
| --- | --- | --- | --- | --- | --- |
| Product Bible Pack 3 | `docs/product_bible/03_Menu_Inventory_SoldOut/**` | `docs/product_bible/_archive/ASAK_Product_Bible_Pack3/**` | 중복 파일은 정확 일치 | 현재 Pack이 정본; 아카이브는 이력 | 현재 유지; 사람이 아카이브 통합 승인 전까지 아카이브 보존. |
| Product Bible Pack 4 | `docs/product_bible/04_Dashboard_Sales_Kitchen_TTS/**` | Pack 4 아카이브 사본 2개 | 대부분 architecture/API/README 파일 정확 일치 | 현재 Pack이 정본 | 전체 참조 확인 후 이력 아카이브 위치 하나만 유지; Batch C 결정. |
| Product Bible Pack 7 | `docs/product_bible/07_Screen_Bible/**` | `docs/product_bible/_archive/ASAK_Product_Bible_Pack7_Screen_Bible/**` | 19개 screen/registry 파일 정확 일치 | 현재 Pack이 정본 | 아카이브 증거 유지; 이 단계에서 삭제 없음. |
| 메뉴 이미지 | `images/menu/{id}.png` 및 `images/original/{id}_*.png` | 의도적 동일 콘텐츠 경로 95개(4파일 그룹 3개 포함) | 이름/소비 경로 다름 | Seed/README 이미지 워크플로가 두 위치 사용 | 둘 다 KEEP; 삭제 후보 아님. |
| `seed-v3/menu_opt_override.json` / `opt_item_comp.json` | 둘 다 아님 | 각각 빈 배열 | 스키마에서 역할 다름 | 매니페스트에 둘 다 명명 | 해시 기준 병합 금지; DB 스키마 검토 필요. |

SHA-256 그룹 128개(추가 경로 142개). 대부분 의도적 이미지 경로 쌍 또는 Product Bible 아카이브 사본입니다. 사람의 아카이브 보존 결정 없이 안전하게 삭제할 수 있는 정확 중복은 없습니다.

### 유사/역할 중복 그룹

| 그룹 | 정본 후보 | 중복 / 겹침 | 차이 | 참조 위치 | 권장 처리 |
| --- | --- | --- | --- | --- | --- |
| 화면 문서 | Product Bible Pack 7 `SCREEN_REGISTRY.md` | `docs/screens/screens.json`, `screens.md`, `screens-wiki.md`, `docs/wiki/screen-design-figma.md` | Registry는 정책; JSON/내보내기는 도구 및 동기화용 | README, Figma/DevCopilot 스크립트 | 모두 유지; Batch B에서 소스 대 내보내기 라벨 명시. |
| Figma 가이드 | `docs/design/FIGMA_GUIDE.md` + 현재 Product Bible | 날짜별 Figma 감사/프롬프트 및 회의 기록 | 운영 지침 vs 이력 인수 프롬프트 | 디자인 플러그인 및 팀 문서 | Figma 담당자 확인 후 종료된 날짜별 감사/프롬프트만 아카이브. |
| 제품 정책 | `docs/product_bible/**` | `docs/wiki/**`, Notion 내보내기 | Wiki/Notion은 요약/소스 맥락 보유, 드리프트 가능 | DevCopilot/Notion 워크플로 | Product Bible이 정본; 내보내기 삭제 금지. |
| Seed 데이터 | 현재 로더용 `asak-data/seed/` | `seed-v3/` 짧은 이름 코퍼스 | 레거시 레코드 수 동일, 필드 약어/정책 테이블 다름 | 별도 로더 스크립트 | DB 담당자가 스키마 선택 후 병합/이동. |
| 작업 로그 | 기존 `worklog/daily`, `entries` | Notion 일일 작업 로그 내보내기 페이지 | Git 이력 vs Notion 협업 이력 | 캘린더/동기화 스크립트 | 둘 다 유지; 중복 제거 없음. |

## 스크립트 인벤토리 및 제안 분류

명령은 저장소 루트 기준입니다. "Current"는 README/현재 운영 가이드 참조 또는 내부 의존성; "review"는 미사용을 의미하지 않습니다.

| 스크립트 집합 | 명령 / 입력 / 출력 | 현재 상태 | 대체 / 목표 | 분류 |
| --- | --- | --- | --- | --- |
| `download_menu_images.py`, `apply_original_images.py` | `python asak-data/scripts/<name>.py`; 소스 이미지 URL/original → `images/` | README 문서화 | 참조 업데이트 후 `scripts/active/images/` | KEEP_ACTIVE_TOOL |
| `load_seed_sqlite.py`, `load_seed_mysql.py` | `python .../load_seed_*.py`; `seed/*.json` → SQLite/MySQL | SQLite 로더 README 문서화; MySQL 로더는 스키마 도구 | `scripts/active/seed/` | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION |
| `build_short_name_seed.py`, `load_short_name_seed_mysql.py`, `migrate_short_names_mysql.py`, `apply_option_policy_mysql.py`, `create_sales_views_mysql.py` | Python 명령 + DB 인자; `seed`/`seed-v3` → MySQL | 별도 짧은 이름 마이그레이션 체인; 가이드 미문서화 | DB 담당자가 v3 폐기 확인 후에만 `scripts/archive/one-off-migrations/` | NEEDS_CONFIRMATION |
| `verify_notion_token.py`, `create_worklog.py`, `upload_getting_started_to_notion.py` | Python 명령; 환경 `NOTION_TOKEN` 및 Markdown → Notion API | 처음 두 개는 현재 운영 가이드 도구 | `scripts/active/notion/` | KEEP_ACTIVE_TOOL |
| `sync_current_docs_devcopilot.py`, `devcopilot_upload.py`, `upload_wiki.py`, `upload_screens_api.py`, `upload_screens_wiki.py`, `sync_figma_links.py`, `export_screens.py`, `gen_wiki_markdown.py` | Python 명령; docs/screens/seed → DevCopilot/Figma/Notion 출력 | 현재 또는 활성 의존; 일부 참조는 이력만 | `scripts/active/devcopilot/` 또는 `active/images/` | KEEP_ACTIVE_TOOL / NEEDS_CONFIRMATION |
| `full_mapping_audit.py`, `req_link_audit.py`, `req_link_gap_audit.py`, `audit_scenarios.py`, `fix_fk_targets.py` | Python 명령; docs/API 데이터 → `*_report.json` | 감사 유틸; 보고서는 현재 `scripts/`에 출력 | `scripts/active/audit/`, 출력은 `reports/audits/` | KEEP_ACTIVE_TOOL; Python 출력 경로 변경으로 Batch B 이동 |
| `append_fetch_result.py`, `apply_agent_batch.py`, `apply_fetch_batches.py`, `batch_save_notion.py`, `bulk_save_fetch.py`, `compact_to_raw.py`, `decode_b64_batch.py`, `export_batch.py`, `extract_transcript_fetches.py`, `fetch_notion_pages.py`, `fetch_progress.py`, `ingest_mcp_batch.py`, `jsonl_to_raw.py`, `mcp_fetch_all.py`, `merge_fetch_batch.py`, `notion_mcp_http_fetch.py`, `persist_pages.py`, `rebuild_scenario_raw.py`, `run_fetch_save_all.py`, `save_batch_jsonl.py`, `save_fetch_batch.py`, `save_fetches.py`, `save_final_missing.py`, `save_live_notion_batch.py`, `save_mcp_array.py`, `save_mcp_batch.py`, `save_mcp_file.py`, `save_mcp_pages.py`, `save_mcp_stdin.py`, `save_missing26.py`, `save_notion_fetch.py`, `save_one_fetch.py` | 배치/fetch 변환 명령; JSON/JSONL/stdin → `scripts/notion_raw` 및 임시 산출물 | 현재 운영 가이드 없음; 일부는 의존 체인 형성 | 재생 테스트 후 `scripts/archive/deprecated/` 또는 `active/notion/` 통합 | MOVE_TO_ARCHIVE 후보; 체인 매핑 전 이동 금지 |
| `api_format.py`, `extra_apis.py`, `generate_scenario_props.py`, `gen_embedded_pages.py`, `gen_embedded_part2.py`, `gen_embedded_part3.py`, `gen_embedded_qa.py`, `list_missing_notion.py`, `remove_former_members_devcopilot.py`, `req_link_maps.py`, `sync_devcopilot_db_schema.py`, `sync_devcopilot_sales_views.py`, `sync_req_screen_links.py`, `update_column_descriptions.py`, `update_table_descriptions.py`, `upload_tasks_only.py`, `upload_wiki_batch.py`, `verify_devcopilot_upload.py`, `rename_figma_scr_frames.py` | 일회성/유지보수 명령; 로컬 docs/API 데이터 → 외부 API 또는 보고서 | 44개 스크립트는 현재 가이드 참조 없음; 이 19개는 이력 또는 내부 참조 | 명명된 담당자가 마지막 성공 명령 검증할 때까지 유지 | NEEDS_CONFIRMATION |

**개수 해석:** 11개 스크립트는 현재 팀 운영에 직접 문서화, 22개는 활성 의존 또는 감사 후보, 44개는 현재 가이드 참조 부재로 일회성/아카이브 후보입니다. 삭제 목록이 아닙니다.

### 생성 산출물 및 `.gitignore` 제안(미적용)

| 항목 | 증거 / 가치 | 결정 |
| --- | --- | --- |
| `asak-data/scripts/*_report.json` (추적 7개) | 감사/업로드 스크립트로 재생성; 텍스트 참조 없음 | Python 출력 경로 변경과 함께 `reports/audits/` 또는 `reports/upload-results/`로 이동; 날짜 증거로 남기지 않으면 재생성 로컬 보고서는 ignore |
| `asak-data/scripts/notion_raw/*.json` (151) | Fetch/save 워크플로 스냅샷 | 날짜 스냅샷으로 유지, `snapshots/notion/` 이동; 보존 기간 합의 전 ignore 금지 |
| `asak-data/scripts/_gs_*.md` (5) | 임시 생성 청크; 패턴으로 이미 ignore | 추적 중인 사본 먼저 아카이브; 새 파일은 계속 ignore |
| `worklog/scripts/__pycache__/worklog_paths.cpython-313.pyc` | Python 바이트코드; `__pycache__/`는 ignore되나 추적 파일 잔존 | 명시적 승인 후 DELETE_CANDIDATE; 지금 삭제 금지 |
| `docs/screens/screens-devcopilot-localstorage.json` | Local-storage import 페이로드 | NEEDS_CONFIRMATION; 생성물로 보이나 DevCopilot 복구 필요 여부 확인 후 ignore/이동 |
| `asak-data/asak_sample.db` | 재빌드 가능 로컬 DB; `*.db`는 이미 ignore | ignore 유지; 추적 사본 없음 |

파일 재배치 및 보존 승인 후 제안하는 `.gitignore` 추가:

```gitignore
# Locally regenerated ASAK data-tool output
asak-data/reports/upload-results/*.json
asak-data/reports/audits/*_local.json
asak-data/scripts/notion_raw/
docs/screens/*localstorage*.json
worklog/scripts/__pycache__/
```

## Seed 및 seed-v3 감사

| 영역 | 발견 | 결정 |
| --- | --- | --- |
| 정본 로더 증거 | `asak-data/README.md`, `load_seed_sqlite.py`, `load_seed_mysql.py`, `gen_wiki_markdown.py`가 `asak-data/seed` 사용 | `seed`가 현재 저장소 샘플 seed 후보. |
| v3 로더 증거 | `build_short_name_seed.py`가 `seed-v3` 작성; `load_short_name_seed_mysql.py`가 짧은 이름 마이그레이션 후 소비 | `seed-v3`는 자동으로 더 새로운 정본이 아닌 스키마 마이그레이션 코퍼스. |
| 대응 파일 | 17개 공유 논리 테이블 레코드 수 일치: category 6, menu 84, ingredient/ing 90, menu-option legacy 9,166, option-item 157 등 | DB 담당자가 목표 스키마 확인 전까지 둘 다 보존. |
| 필드 변경 | v3는 이름 단축(`category_id`→`cat_id`, `ingredient_id`→`ing_id`, `option_group_id`→`opt_group_id`, `sort_order`→`sort_no`, `is_active`→`active`) | 파일명으로 이름 변경/병합 금지. |
| v3 전용 정책 파일 | `opt_policy` 82, `opt_policy_item` 734, `menu_opt_policy` 467, `menu_opt_override` 0; 레거시 menu option 파일 유지 | DB 스키마/import 검토 필요. |
| FK 확인 | 각 seed 집합의 명시적 레거시 코퍼스 관계 21개를 참조 `id` 집합과 대조; 잘못된 값: 0 | 참조 데이터는 검사한 관계에서 내부 일관; DB 로드 및 스키마 제약은 담당자 검증 필요. |

## 문서 및 worklog 구조 결정

기존 거버넌스 문서는 이미 `docs/product_bible`을 Product Bible 정본 경로로 선언합니다. 따라서 이 정리는 두 번째 정본 매니페스트를 만들지 않고 `DOCUMENT_STATUS_MANIFEST.md`를 업데이트합니다.

```text
docs/
  product_bible/       current product/Screen/Component/QA standards
  governance/          status, ownership and cleanup inventory
  planning/            current implementation sequence/status
  design/              live Figma guides, plugins and assets
  guides/ operations/  team-facing procedures and setup
  screens/             screen source and tool exports
  wiki/                DevCopilot sync source (protected when active)
  archive/
    design-audits/     concluded dated audits
    prompts/           superseded approved prompts
    migrations/        concluded migration notes
    notion-exports/    frozen exports, after page-level review
    superseded/        replaced non-canonical documents
    project-history/   retained historical evidence
asak-data/
  seed/                current sample-seed candidate
  seed-v3/             short-name migration corpus pending decision
  scripts/active/      documented tools after Batch B path update
  scripts/archive/     one-off/deprecated scripts after replay review
  reports/ snapshots/  generated outputs separated from executable code
  archive/schema/      migration schema evidence
worklog/
  daily/ entries/      preserve existing paths until calendar/sync migration
  templates/ scripts/ weekly/
```

README 추가는 연기: Batch B 경로 변경 승인 후에만 유용하며, 그 전에는 아직 적용되지 않은 구조를 문서화하게 됩니다.

## 배치 및 승인

### Batch A — 안전, 실행 완료

| 출발 | 도착 | 참조 업데이트 | 안전한 이유 |
| --- | --- | --- | --- |
| `asak-data/schema-backups/short-name-before-20260713-115747.sql` | `asak-data/archive/schema/short-name-before-20260713-115747.sql` | `docs/design/FIGMA_AGENT_DATA_CONTRACT_AUDIT_2026-07-15.md` | 변경 불가 마이그레이션 전 증거; 실행 호출자 없음. |
| `docs/team/design-doc-merge-audit-2026-07-06.md` | `docs/design/_archive/audits/design-doc-merge-audit-2026-07-06.md` | Worklog/design/team 링크 | 2026-07-06 종료 감사, 이력과 함께 보존. |
| `docs/team/notion-merge-sync-audit-2026-07-06.md` | `docs/_archive/notion-audits/notion-merge-sync-audit-2026-07-06.md` | Worklog/design 링크 | 2026-07-06 동기화 감사, Notion 감사 이력과 함께 보존. |

#### Rebase 후 Batch A 보완 — 완료 (2026-07-16)

`docs/_archive/notion-audits/notion-merge-sync-audit-2026-07-06.md`는 Notion 병합 및 동기화 작업을 감사한 문서였으며, rebase 성공 후 다음 목표로 이동했습니다:

```text
docs/_archive/notion-audits/notion-merge-sync-audit-2026-07-06.md
```

`docs/_archive/migration-audits/`는 선택하지 않았습니다. 이 문서는 스키마, 데이터 또는 코드 마이그레이션을 기록하지 않기 때문입니다. `design-doc-merge-audit-2026-07-06.md`는 `docs/design/_archive/audits/`에 둡니다.

### Batch B — 참조/코드 업데이트 필요; 승인 필요

- `asak-data/scripts/`의 JSON 보고서를 `asak-data/reports/`로 이동: 7개 Python 스크립트가 현재 `scripts/` 내부에 출력 경로를 구성함.
- `notion_raw/` 및 임시 fetch 체인 이동: Python reader/writer가 현재 디렉터리 사용.
- `scripts/active/*` 및 `scripts/archive/*` 도입: README, PowerShell, Markdown, Python 호출 경로 및 재생 테스트된 워크플로 업데이트.
- worklog 재구조: 캘린더 빌더, 캘린더 JSON 생성, Notion 동기화, README 및 기존 링크를 함께 업데이트.
- 실제 경로 승인 후 대상 폴더 README 추가.

### Batch C — 사람 결정 필요

- 향후 DB 작업용 `seed` vs 짧은 이름 `seed-v3` 스키마 선택.
- 현재 DevCopilot/WBS 파일을 덮어쓰지 않고 `docs/wiki` vs Product Bible 콘텐츠 수용 해결.
- `docs/team/2026-07-14-feedback-resolution.md`, `hub-notion-sync-checklist.md`, `notion-sync-change-register-2026-07-14.md`를 현재/참조/아카이브로 확정.
- 날짜별 Figma 프롬프트/감사 및 Notion 내보내기 트리의 담당자 및 아카이브 정책 확정.
- 디렉터리 이름 변경 전 현재 vs 이전 worklog 참여자 확정.

### Batch D — 삭제 후보; 지금은 삭제 제안 없음

- 추적 중인 Python 바이트코드는 명시적 승인 후에만 삭제 후보.
- 정확한 Product Bible 아카이브 사본 및 의도적 이미지 사본은 이 단계에서 **삭제 후보 아님**.
- 시그니처 스캔으로 자격 증명 값 없음; 토큰 파일 삭제 불필요.

## 참조 위험 등록부

| 위험 | 영향 파일 | 필요한 안전장치 |
| --- | --- | --- |
| Python 출력 경로가 내장됨 | 보고서 생성 7개 스크립트 및 Notion 스냅샷 fetch 체인 | Batch B 이동 전 코드 업데이트 및 dry-run |
| 현재 DevCopilot/WBS 파일이 미추적 | `docs/wiki` 8개 경로 | 스테이징에서 제외, 절대 덮어쓰지 않음 |
| Worklog 경로가 실행 설정 | 캘린더/README/Python/PowerShell 링크 | 테스트된 원자적 Batch B 변경으로만 이동 |
| 스키마 스냅샷 링크 | Figma Agent 데이터 계약 감사 | Batch A에서 Markdown 링크 업데이트 |
| 이력 감사 링크 | 2026-07-06 worklog/design/team 문서 | Batch A에서 링크 업데이트 및 저장소 검색으로 확인 |
