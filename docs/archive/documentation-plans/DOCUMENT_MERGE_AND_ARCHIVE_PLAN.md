> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Completed cleanup plan.
> Canonical Replacement: `docs/governance/REPOSITORY_CLEANUP_INVENTORY_2026-07-16.md`
> Original Path: `docs/documentation-management/DOCUMENT_MERGE_AND_ARCHIVE_PLAN.md`

# Document Merge and Archive Plan

## Human decisions applied

- The canonical Product Bible path is `docs/product_bible`; do not rename it.
- ASAK-Admin is the canonical admin implementation repository. Kiosk Admin scaffolds are Legacy Reference and remain in place.
- `kiosk.json` and `asak-admin-data.json` remain MVP Demo Data source assets in their current locations.
- Do not delete `DELETE_CANDIDATE` documents; retain them as Legacy or Archived.

## 통합·보관 원칙

- Product Bible은 최신 정본으로 유지하며 다른 저장소에 복제하지 않는다.
- 기존 문서의 고유한 실행 절차, 팀 기록, Figma 링크, WBS 맥락은 삭제하지 않고 reference로 보존한다.
- `_archive` 및 과거 Notion export는 현재 구현 판단에서 제외한다.

## 후보

| 대상 | 상태 | 보존할 고유 내용 | 후속 조치 |
|---|---|---|---|
| `_archive/**` | ARCHIVE | 이전 결정·변경 이력 | 현 위치 유지, 현재 기준 표기 |
| Kiosk/Admin `IMPLEMENTATION_PLAN.md` | MERGE 후보 | 작성자별 진행 맥락 | Pack 11/12와 비교 후 링크 중심으로 통합 제안 |
| Kiosk/Admin `contracts/**` | CONFLICT 후보 | 현재 프런트의 예상 data shape | canonical API 계약과 field/path 비교 |
| Notion WBS/회의록 | REFERENCE/ARCHIVE 후보 | 과거 합의와 일정 | 최신 Decision Log와 연결 |
| design/screens 문서 | UPDATE 후보 | Figma 노드/시각 자산 | Screen Registry ID·최신 Figma 기준 표기 |

## Delete candidate

현재 확정된 삭제 후보는 없다. 중복처럼 보이는 문서도 고유한 이력·작성자 맥락이 있을 수 있어 승인 전 삭제하지 않는다.

## 사람 확인 후에만 가능한 조치

1. API 계약의 정본 경로와 DTO field 확정.
2. 기존 Kiosk 내부 Admin 스캐폴드의 보관/이관 소유자 결정.
3. 각 Notion export를 reference와 archive 중 어디에 분류할지 결정.
4. 중앙 docs README를 추가하고 각 저장소 README에 링크할지 결정.
