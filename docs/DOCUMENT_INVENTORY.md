# Document Inventory

> Decision update: `docs/product_bible` is the retained canonical path. ASAK-Admin is canonical for admin implementation, Kiosk Admin scaffolds are Legacy Reference, and MVP mock JSON files remain source assets. See [Canonical Contract Decisions](CANONICAL_CONTRACT_DECISIONS.md) and [Document Status Manifest](DOCUMENT_STATUS_MANIFEST.md).

> 파일 삭제·이동·rename 없이 문서 군을 내용과 정본 관계로 분류한 인벤토리다. `_archive`는 현재 기준에서 제외한다.

| 현재 위치 | 목적 | 최신/정본 | Product Bible 중복 | 분류 | 권장 위치 | 조치 이유 |
|---|---|---|---|---|---|---|
| `docs/product_bible/01_Foundation` | 비전, ADR, canonical source | 예 | 기준 자체 | KEEP | 현 위치 | 모든 도메인 정본 |
| `docs/product_bible/02_*`~`05_*` | 기능 정책/API/QA | 예 | 기준 자체 | KEEP | 현 위치 | 기능별 정본 |
| `docs/product_bible/06_*`~`10_*` | 엔지니어링, 화면, 컴포넌트, QA, AI | 예 | 기준 자체 | KEEP | 현 위치 | 구현·검증 정본 |
| `docs/product_bible/11_*`, `12_*` | Backend/Frontend 실행 계획 | 예 | 기준 자체 | KEEP | 현 위치 | 수직 슬라이스 기준 |
| `docs/product_bible/_archive/**` | 이전 Pack 보관 | 아니오 | 일부 | ARCHIVE | 현 위치 | 사용자 지시대로 참고 제외 |
| `docs/design/**`, `docs/screens/**` | Figma/화면 자산 및 기록 | 확인 필요 | 일부 | UPDATE | `docs/design`, `docs/screens` 유지 | Product Bible과 최신 Figma 연결만 보강 |
| `docs/guides/**`, `docs/wiki/**`, `docs/team/**` | 운영/가이드/팀 지식 | 확인 필요 | 일부 | UPDATE | 현 위치 | 각 문서에 정본 링크 필요 |
| `docs/notion/**` | Notion export/회의·WBS 원본 | 과거 기록 포함 | 일부 | ARCHIVE 또는 REFERENCE | `docs/notion` 유지 | 삭제 대신 이력/참조로 구분 |
| `ASAK-Kiosk/README.md`, `src/README.md`, `STRUCTURE_GUIDE.md`, `IMPLEMENTATION_PLAN.md`, `src/contracts/**` | Kiosk 구현 안내/계약 | 일부 구식 가능 | 예 | UPDATE/CONFLICT | Kiosk 유지 | 현재 API/route 기준과 대조 필요 |
| `ASAK-Admin/README.md`, `docs/**`, `IMPLEMENTATION_PLAN.md`, `src/contracts/**` | Admin 구현 안내/계획 | 일부 구식 가능 | 예 | UPDATE/CONFLICT | Admin 유지 | Screen Registry·API와 대조 필요 |
| `ASAK-back/README.md` | Backend 시작 안내 | 부분 | 예 | UPDATE | Backend 유지 | 실제 scaffold와 Pack 11 연결 필요 |

## 분류 집계 (문서 군 기준)

| KEEP | UPDATE | MERGE | MOVE | ARCHIVE | DELETE_CANDIDATE | CONFLICT |
|---:|---:|---:|---:|---:|---:|---:|
| 12 Pack 군 | 5 군 | 0 | 0 | 2 군 | 0 | 3 군 |

`MERGE`, `MOVE`, `DELETE_CANDIDATE`는 상세 내용의 중복 검증과 사람 승인이 필요하다. 현 단계에서 실제 조치는 하지 않는다.
