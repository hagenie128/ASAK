# ingredient-salady — 샐러디 공식 토핑·드레싱 썸네일

> **용도:** ASAK 학습/참고용 재료 이미지  
> **출처:** [샐러디 토핑](https://salady.com/menu/list_2?type=topping) · [드레싱](https://salady.com/menu/list_2?type=dressing)  
> **원본 CDN:** `https://salady.com/superboard/data/topping/thumb/...`  
> **주의:** 샐러디 저작물입니다. 상업 배포·앱스토어 제출 전 권리 확인이 필요합니다. (`asak-data` 가이드의 상업적 사용 금지와 동일)

## 파일
| 파일 | 설명 |
|---|---|
| `topping_*.jpg/png` | 토핑 원본(~397px, `/topping/` 경로) |
| `dressing_*.png` | 드레싱 원본 |
| `mapping.json` | 샐러디 항목 + ASAK `ingredient_id` 매칭 |
| `match_report.json` | 매칭 통계·미매칭 목록 |

목록 페이지의 `/topping/thumb/`(60px)가 아니라 **같은 파일명의 `/topping/` 원본**을 저장합니다.

## 다시 받기
```bash
python3 ../scripts/download_ingredient_images_salady.py
```

## 한계
- 공식 사이트에 **토핑·드레싱 사진**은 있음 (SVG 아이콘 세트는 없음).
- ASAK seed의 **베이스(채소볼 등)·스프·복합 문구 재료**는 사이트에 개별 썸네일이 없어 미매칭.
- UI용 SVG 아이콘이 필요하면 이 PNG를 바탕으로 별도 아이콘을 만들거나, 타입(채소/단백질/…) 공통 아이콘을 쓰면 됩니다.
