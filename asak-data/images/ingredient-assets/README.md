# ingredient-assets — 재료 아이콘 + 사진 통합팩

## 어디에 두나

이 폴더는 재료 이미지의 원본·가공 소스입니다. 실행 앱의 URL 정본은 메뉴 이미지와 같이 **Cloudinary가 연결된 DB `media_asset.url`**로 전환합니다.

| 역할 | 경로 |
|---|---|
| 원본·가공 소스 | `asak-data/images/ingredient-assets/` |
| 실행 URL 정본 | `media_asset.url` (Cloudinary) |
| 메뉴 연결 | `menu.image_asset_id` → `media_asset.id` |
| 프론트 표시 | API `imageUrl` |
| 기존 backend static / frontend public | 전환·복구 참고용, 신규 정본 아님 |

메뉴·재료 자산 모두 새 기능에서 `/assets/menu/{id}.png` 같은 로컬 경로를 정본으로 저장하지 않습니다.

## React
```jsx
<img src={imageUrl} alt="" />
```

## 다시 빌드
```bash
python3 asak-data/scripts/build_ingredient_assets.py
```

## 통계: 재료 90 · 아이콘 90 · 사진 51
