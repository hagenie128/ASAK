# ASAK Data

## Cleanup structure and safeguards

- `seed/`: 현재 로더가 사용하는 정본 후보입니다.
- `seed-v3/`: 단축명 MySQL Schema 전용입니다. DB 감사 전에는 두 폴더를 통합·삭제하지 않습니다.
- `reports/generated/`: 실행 코드가 읽지 않는 일회성 Markdown 산출물입니다.
- `scripts/`: 현재 실행 경로를 유지합니다. JSON 보고서·Notion snapshot·batch 파일은 Python 출력 경로가 고정되어 있어 소스 코드 변경 승인과 재검증 전에는 이동하지 않습니다.
- `archive/schema/`: 되돌릴 수 없는 이전 schema 증거입니다.

생성물을 재생성할 때는 기존 파일을 수동 이동하지 말고 해당 스크립트의 출력 경로와 README를 함께 검토합니다.

This folder contains canonical sample data generated from
`data-pipeline/phase1/output`.

## Build Sample DB

Create a local SQLite database from the current seed JSON:

```powershell
python asak-data/scripts/load_seed_sqlite.py
```

Regenerate `asak-data/seed/*.json` from `data-pipeline/phase1/output` first, then
load the DB:

```powershell
python asak-data/scripts/load_seed_sqlite.py --rebuild-seed
```

Default output:

```text
asak-data/asak_sample.db
```

The loaded tables follow `docs/wiki/db-table-definition-2026-07-06.md`. Current sample data
covers the menu/catalog tables plus `payment_method_config`; order/payment tables
are created empty for API prototyping.
