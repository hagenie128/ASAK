# ASAK Data

> Status: **Current** · 샘플 데이터·시드·이미지·스크립트

## 폴더 역할

| 경로 | 역할 | 태그 |
|---|---|---|
| `seed/` | 현재 로더가 쓰는 **시드 정본 후보** | `#canonical-candidate` |
| `seed-v3/` | 단축명 MySQL 스키마 전용. **seed와 합치지 않음** | `#reference` |
| `images/menu` | 키오스크용 메뉴 이미지 | `#current` |
| `images/original` | 원본 이미지 | `#reference` |
| `images/menu-trimmed` | 여백 제거 산출물 (스크립트 입력) | `#current` |
| `scripts/` | 시드·Notion·동기화 스크립트 | `#current` |
| `archive/` | 이미지 백업·이전 schema | `#archive` |
| `snapshots/` | 스냅샷 자리 | `#archive` |

생성물 경로(`scripts/notion_raw`, `scripts/output`, 각종 `*_report.json`)는 스크립트가 고정 경로로 씁니다. 소스 변경 승인 전에는 이동하지 않습니다.

## 샘플 DB 만들기

현재 seed JSON으로 로컬 SQLite를 만듭니다.

```powershell
python asak-data/scripts/load_seed_sqlite.py
```

`data-pipeline/phase1/output`에서 seed를 다시 만든 뒤 로드하려면:

```powershell
python asak-data/scripts/load_seed_sqlite.py --rebuild-seed
```

기본 출력: `asak-data/asak_sample.db`

로드 테이블은 `docs/wiki/db-table-definition.md`를 따릅니다. 메뉴·카탈로그와 `payment_method_config`가 채워지고, 주문·결제 테이블은 API 프로토타입용으로 비어 있습니다.
