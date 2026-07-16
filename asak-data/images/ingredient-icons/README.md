# ingredient-icons — ASAK 재료 심벌(SVG)

직접 그린 **stroke 심벌**입니다. 샐러디 사진(`ingredient-salady`)과 별개로 UI 아이콘용입니다.

## 사용
- 경로: `svg/{icon_key}.svg`
- 색: CSS에서 `color` / `currentColor` (예: 라임 악센트)
- 매핑: `mapping.json`의 `ingredient_id` → `icon_key`

## 다시 생성
```bash
python3 ../scripts/generate_ingredient_icons.py
```

## 미리보기
브라우저로 `preview.html` 열기.
