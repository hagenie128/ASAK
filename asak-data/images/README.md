# asak-data/images

> Status: **CURRENT**

| 폴더 | 역할 | 태그 |
|---|---|---|
| `menu/` | 메뉴 이미지 가공·재업로드 소스 | `SOURCE` |
| `original/` | 원본 보관 | `REFERENCE` |
| `menu-trimmed/` | 여백 제거 산출물·Cloudinary 업로드 후보 | `SOURCE` |
| `ingredient-*` | 재료 아이콘·자산 | `REFERENCE` |

## 앱에서 이미지가 보이는 흐름

```text
이 폴더의 원본·가공본 → Cloudinary 업로드 → DB media_asset
→ menu.image_asset_id → API imageUrl → Kiosk/Admin 화면
```

이 폴더는 소스·복구 자료이며 앱 런타임 URL 정본이 아닙니다. 런타임 정본은 `media_asset.url`입니다.

이미지 백업은 [`../archive/images-260813-backup/`](../archive/images-260813-backup)에 있습니다.
