# DB Audit Plan

## 현재 결정

DevCopilot Modeler에는 legacy backup 테이블 2개를 포함해 30개 model(26 tables, 4 views)이 있습니다. ASAK-back에는 현재 schema SQL, migration, entity, repository, persistence dependency evidence가 없습니다. 따라서 DB 구현 상태는 `TODO`입니다.

## 감사 순서

1. DevCopilot Modeler table·relation metadata를 export/read합니다.
2. backend `schema.sql`, migration, Entity, Repository, Enum, seed, FK, index, constraint evidence를 생성 시 수집합니다.
3. 약어 이름 변경 없이 table·column 단위로 비교합니다.
4. 각 항목 분류: Modeler-only, backend-only, matched, name mismatch, relation mismatch, legacy/deprecated.
5. schema 변경 전 변경 제안을 검토합니다.

## Legacy models

`menu_option_group_legacy_20260710`과 `menu_option_legacy_20260710`은 Legacy/Deprecated backup model로 보존됩니다. 현재 MVP dashboard 후보에서 제외되며, 이번 작업에서 삭제·이름 변경하지 않습니다.
