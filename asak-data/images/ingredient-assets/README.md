# ingredient-assets — 재료 아이콘 + 사진 통합팩

## 어디에 두나 (정본)

메뉴 사진과 같이 **백엔드 static**이 정본입니다.

| 역할 | 경로 |
|---|---|
| **정본 (API URL)** | `ASAK-back/src/main/resources/static/assets/ingredients/` |
| 브라우저 URL | `/assets/ingredients/icons/{id}.svg` · `/assets/ingredients/photos/{id}.ext` |
| 소스 보관 | `asak-data/images/ingredient-assets/` |
| Kiosk/Admin public | Vite mock용 **보조 복사** (백엔드 안 켤 때만) |

메뉴도 같은 규칙: `/assets/menu/{id}.png` → backend `static/assets/menu`.

## React
```jsx
<img src={`/assets/ingredients/icons/${ingredientId}.svg`} alt="" />
```

## 다시 빌드
```bash
python3 asak-data/scripts/build_ingredient_assets.py
```

## 통계: 재료 90 · 아이콘 90 · 사진 51
