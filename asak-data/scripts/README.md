# ASAK data scripts

이 폴더는 현재 DevCopilot·Notion·DB 보조 스크립트의 실행 위치입니다. `notion_raw/`, JSON report/snapshot, batch 입력은 일부 Python 파일이 직접 참조하므로 cleanup에서 경로를 바꾸지 않았습니다.

- 현재 운영 스크립트: 이 폴더의 `.py` 파일
- 이동 완료 산출물: `../reports/generated/`의 `_gs_*.md`
- 향후 `active/`·`archive/` 분리는 호출 경로를 갱신하고 Python syntax/실행 dry-run으로 검증한 뒤 수행합니다.

```powershell
python asak-data/scripts/sync_current_docs_devcopilot.py --help
python asak-data/scripts/load_seed_sqlite.py --help
```
