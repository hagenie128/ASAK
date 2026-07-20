> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Completed inventory superseded by the cleanup manifest.
> Canonical Replacement: `docs/governance/DOCUMENT_STATUS_MANIFEST.md`
> Original Path: `docs/documentation-management/DOCUMENT_INVENTORY.md`

# Document Inventory

> 갱신: 2026-07-17. 삭제는 하지 않고, 태그·보관 이동으로 정리했다.  
> 실사용: [문서 태그 인덱스](../../document-tag-index-2026-07-18.md) · [README.md](../../README.md)
> 결정: [Canonical Contract](../../governance/CANONICAL_CONTRACT_DECISIONS.md) · [Status Manifest](../../governance/DOCUMENT_STATUS_MANIFEST.md)

| 현재 위치 | 목적 | 태그 | 분류 | 조치 (2026-07-17) |
|---|---|---|---|---|
| `docs/product_bible` Pack 01~12 | 제품 정본 | `#canonical` | KEEP | 유지 |
| `docs/product_bible/_archive` | 이전 Pack | `#archive` | ARCHIVE | 유지 |
| `docs/governance` | 계약·상태 | `#canonical`/`#reference` | KEEP | Manifest·Index 갱신 |
| `docs/planning`, `architecture`, `implementation_guide`, `operations` | 구현 기준 | `#current` | KEEP | 폴더 README 추가 |
| `docs/design` 활성 QA/명세 | Figma | `#current`/`#wip` | KEEP | README·태그 |
| `docs/design/_archive` | QA 원본·일회 프롬프트·구 DS | `#archive` | ARCHIVE | 이동 완료 |
| `docs/screens` | SCR·DevCopilot | `#reference` | KEEP | README; 구 figma 요약 → `_archive` |
| `docs/guides`, `wiki` | 온보딩·Wiki | `#reference` | KEEP | 태그 배너 |
| `docs/team` | hub sync | `#reference` | KEEP | 감사 md → `_archive/team-audits` |
| `docs/notion` | Notion export | `#legacy`/`#archive` | REFERENCE | README만 (대량 이동 없음) |
| `docs/_archive` | 중앙 보관 | `#archive` | ARCHIVE | 신설 |
| `docs/documentation-management` | 문서 관리 계획 | `#reference` | KEEP | README |
| `ASAK-Kiosk` / `Admin` / `back` docs | 저장소 실행 | `#repo-local` | KEEP | 중앙에서 링크만 |
| Kiosk Admin scaffolds | 이전 Admin | `#legacy` | LEGACY | 삭제·이동 없음 |

## 집계

| KEEP | UPDATE(README/태그) | ARCHIVE 이동 | DELETE |
|---:|---:|---:|---:|
| 정본·가이드·저장소 문서 | 허브·폴더 README·Manifest | design/_archive, docs/_archive | 0 |

`MERGE`/`DELETE`는 사람 승인 후에만. 현재 확정 삭제 후보 없음.
