# menu-trimmed — UI 표시용 (여백 제거)

원본: `../menu`  
생성: 흰 스튜디오 배경 + 투명 영역을 잘라낸 **표시용** PNG

## 규칙
- 마스터/원본은 `menu`·`original`을 유지한다.
- Figma·키오스크 MenuCard·Detail 썸네일은 **이 폴더**를 우선 사용한다.
- 카드에서는 여전히 `object-fit: cover`를 권장한다 (비율이 메뉴마다 다름).

## 다시 만들기
```bash
python3 scripts/trim_menu_images.py
```
(스크립트 경로: `asak-data/scripts/trim_menu_images.py`)

## 트리밍 기준
- alpha &lt; 12 → 배경
- RGB ≥ 245 (거의 흰색) → 배경
- 밝은 무채색(≥240, 색차 ≤8) → 배경
- 콘텐츠 bbox에 약 4% 패딩 후 crop
