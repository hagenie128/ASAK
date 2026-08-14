# ASAK 전역 정리 근거 (삭제·병합·라벨링)

## 1. 대상과 기준

- 대상 저장소: `ASAK`
- 작업일: 2026-08-14
- 기준: 활성 정본 경로 보존 · 스크립트 하드코딩 경로 유지 · 이력은 삭제 대신 `_archive`

## 2. 삭제한 것

| 항목 | 근거 |
|---|---|
| `**/__pycache__/` | gitignore 생성물, 추적되지 않음 |

## 3. 보관한 것 (삭제 아님)

| 항목 | 새 위치 |
|---|---|
| PPT 원본·수정1·수정2 | `docs/00_presentation/_archive/00_ppt/` |
| 이미지 백업 `260813_backup` | `asak-data/archive/images-260813-backup/` |
| data-pipeline 감사 v1·v2 | `data-pipeline/phase1/_archive/` |
| wiki DevCopilot 스냅샷 17개 | `docs/_archive/wiki-secondary/snapshots/` |
| 구 태그 인덱스 본문 | `docs/_archive/doc-mgmt-plans/document-tag-index-2026-07-18.md` |

## 4. 병합·역할 분리 (라벨링)

| 주제 | 정리 |
|---|---|
| 태그 인덱스 | `07-18` → stub, 정본 `07-20` |
| 회의록 | `operations/meeting-minutes` = 파일 정본 · `wiki/meeting-minutes-weekly` = Hub 통합본 · `worklog/weekly` = 개인 rollup |
| 발표 PPT | 활성은 수정3만, 이전 버전 archive |
| 스킬 템플릿 | guides 사본에 README, 정본은 ASAK-skill / `.cursor/skills` |
| wiki README | Current / Historical / 회의 / 리다이렉트 구간으로 재라벨 |

## 5. 건드리지 않은 것

- `docs/notion`, `worklog/daily`, `asak-data/seed`, `asak-data/seed-v3`
- `asak-data/scripts/notion_raw`, `scripts/output` (스크립트 고정 경로)
- `images/menu-trimmed` (동기화 입력)
- Product Bible 활성 Pack 본문 영문 번역
- `product_bible/_archive` 이력 Pack 사본

## 6. 허브·README 갱신

- `docs/README.md` 폴더 역할표 + 태그
- `asak-data/README.md` 한글화
- `data-pipeline/README.md` 한글화
- `design`, `planning`, `ai-reports`, `images`, `scripts` README 추가/정비
- 발표·보관함 README

## 7. 검증

- 활성 경로에서 `260813_backup` 참조: 문서 README만 남음
- PPT 스크립트 SRC를 archive로 갱신
- 상태 매니페스트·구현 허브·project-flow의 `wbs-v2` → `wbs.md` 드리프트 교정
- archive wiki-secondary 깨진 상대 링크 교정
- 커밋·푸시: 하지 않음
