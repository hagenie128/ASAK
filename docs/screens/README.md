# Screen artifacts

`docs/product_bible/07_Screen_Bible/`가 Screen ID·정책의 정본입니다. 이 폴더의 `screens.json`, `screens.md`, `screens-wiki.md`, `screens-devcopilot-*.json`은 DevCopilot 업로드·동기화를 위한 생성물이며 제품 정책 정본이 아닙니다.

`SCR-020/021`은 현재 구현 기준이 아니므로 이 생성물을 구현 요구사항으로 사용하지 않습니다. 생성 경로는 `asak-data/scripts/export_screens.py`와 업로드 도구가 직접 사용하므로 Source Code 변경 승인 전에는 이동하지 않습니다.

```powershell
python asak-data/scripts/export_screens.py
python asak-data/scripts/upload_screens_wiki.py --dry-run
```
