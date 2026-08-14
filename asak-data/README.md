# ASAK Data

> Status: **CURRENT**

## 폴더 역할

| 경로 | 역할 | 태그 |
|---|---|---|
| `seed/` | 현재 로더가 쓰는 **시드 정본 후보** | `CANONICAL-candidate` |
| `seed-v3/` | 단축명 MySQL 스키마 전용. **seed와 합치지 않음** | `REFERENCE` |
| `images/menu` | 메뉴 이미지 가공·재업로드 소스 (앱 런타임 정본 아님) | `SOURCE` |
| `images/original` | 원본 이미지 | `REFERENCE` |
| `images/menu-trimmed` | 여백 제거 산출물·Cloudinary 업로드 후보 | `SOURCE` |
| `scripts/` | 시드·Notion·동기화 스크립트 | `CURRENT` |
| `archive/` | 이미지 백업·이전 schema | `HISTORY` |
| `archive/frontend-mocks/` | 프론트 미사용 대용량 mock JSON | `HISTORY` |
| `snapshots/` | 스냅샷 자리 | `HISTORY` |

생성물 경로(`scripts/notion_raw`, `scripts/output`, 각종 `*_report.json`)는 스크립트가 고정 경로로 씁니다. 소스 변경 승인 전에는 이동하지 않습니다.

## 메뉴 이미지 런타임 정본

현재 Kiosk/Admin 실행 화면은 이 폴더의 파일 경로를 직접 사용하지 않습니다.

```text
images 원본·가공본 → Cloudinary → DB media_asset.url
→ menu.image_asset_id → API imageUrl → 프론트 화면
```

따라서 `images/**`는 **원본·가공·복구·재업로드 소스**, 실제 앱의 전달 URL 정본은 **Cloudinary가 연결된 DB `media_asset`**입니다. 자세한 전환 근거는 [`../../ASAK-back/docs/MENU_IMAGE_ASSET_FLOW.md`](../../ASAK-back/docs/MENU_IMAGE_ASSET_FLOW.md)를 봅니다.

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
