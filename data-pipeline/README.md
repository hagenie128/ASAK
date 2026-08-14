# ASAK Data Pipeline

> Status: **Current** · 데이터 수집·가공 파이프라인

## 폴더 역할

| 경로 | 역할 | 태그 |
|---|---|---|
| `phase1/` | 1차 크롤·가공 코드 | `#current` |
| `phase1/output/` | 생성물 (gitignore) | `#archive` |
| `phase1/audit_20260812_v3/` | 최신 감사 스냅샷 | `#reference` |
| `phase1/_archive/` | 이전 감사 v1·v2 | `#archive` |
| `phase1/db/` | phase1용 SQL 참고 | `#reference` |

## 저장소 경계

- 파이프라인 코드·생성물은 여기
- 시드 정본: `../asak-data/seed/`
- 메뉴 이미지 정본: `../asak-data/images/menu/`
- `seed`와 `seed-v3`를 합치지 않음

## 실행

```powershell
cd data-pipeline\phase1
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_phase1.py
```
