# ASAK 전역 정리 근거 (삭제·병합·라벨링)

## 1. 대상과 기준

- 대상 저장소: `ASAK`
- 작업일: 2026-08-14
- 기준: 활성 정본 경로 보존 · 스크립트 하드코딩 경로 유지 · 중복 이력은 Git history로 회수 가능하게 삭제

## 2. 삭제한 것

| 항목 | 근거 |
|---|---|
| `docs/_archive/**` | Notion export·구 감사·중복 계획 등 대형 이력 |
| `docs/design/_archive/**` | 완료 감사·중복 프롬프트·구 디자인 사본 |
| `docs/product_bible/_archive/**` | 활성 Pack과 겹치는 과거 사본 |
| Product Bible 원문 181개 | 46개 통합 문서에 원문별 구획으로 내용 보존 |

## 3. 보관한 것 (삭제 아님)

| 항목 | 새 위치 |
|---|---|
| PPT 원본·수정1·수정2 | `docs/00_presentation/_archive/00_ppt/` |
| 이미지 백업 `260813_backup` | `asak-data/archive/images-260813-backup/` |
| data-pipeline 감사 v1·v2 | `data-pipeline/phase1/_archive/` |
| 향후 범위 정본 | `docs/wiki/future-scope.md` |
| API 피드백 기준 | `docs/wiki/api-feedback-resolution-2026-07-14.md` |
| Figma 플러그인·토큰·체크리스트 | `docs/design/` 활성 경로 |

## 4. 병합·역할 분리 (라벨링)

| 주제 | 정리 |
|---|---|
| 태그 인덱스 | `07-18` → stub, 정본 `07-20` |
| 회의록 | `operations/meeting-minutes` = 파일 정본 · `wiki/meeting-minutes-weekly` = Hub 통합본 · `worklog/weekly` = 개인 rollup |
| 발표 PPT | 활성은 수정3만, 이전 버전 archive |
| 스킬 템플릿 | guides 사본에 README, 정본은 ASAK-skill / `.cursor/skills` |
| wiki README | Current / Historical / 회의 / 리다이렉트 구간으로 재라벨 |
| Product Bible | Pack 12개 유지, 도메인별 반복 문서 병합 |
| 시점 문서 | baseline·구현 맵·Gap·Admin TODO·Figma 완료 기록을 `Historical Snapshot`으로 표시 |

## 5. 건드리지 않은 것

- `docs/notion`, `worklog/daily`, `asak-data/seed`, `asak-data/seed-v3`
- `asak-data/scripts/notion_raw`, `scripts/output` (스크립트 고정 경로)
- `images/menu-trimmed` (동기화 입력)
- Product Bible 원문의 사실·표·체크리스트
- 사용자가 수정 중인 `planning/platform-delivery-expansion-plan-2026-08-14.md`

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
- 병합 전 경로를 새 통합 문서로 치환
- 삭제 archive를 가리키던 활성 안내를 Git history 또는 승격 경로로 교정
- 커밋·푸시: 하지 않음
