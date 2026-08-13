# 2026-08-13 사이드·음료 메뉴 반영 및 나머지 CSV 보류 기록

## 반영됨

- 입력: `C:\Users\Administrator\Downloads\salady_menu_full_97.csv`
- DB·`asak-data/seed-v3`에 카테고리 `사이드`(237), `음료`(238)와 단품 메뉴 15개만 반영했다.
- 메뉴 ID: 10776~10790. 목록 SQL의 `menu_nutr` inner join을 통과하도록 영양값은 미확정(null)인 행을 함께 만들었다.
- 제공된 외부 이미지 URL에서 15개 PNG를 내려받아 `ASAK-Kiosk/public/assets/menu`, `ASAK-Admin/public/assets/menu`,
  `ASAK-back/src/main/resources/static/assets/menu`에 각각 `{menuId}.png`로 저장했다. 현재 Kiosk 목록은
  `media_asset`만 사용하므로 DB의 image asset 등록·연결은 별도 작업이다.

## 보류됨

- 원본 97행 중 이번 범위 밖 행: 82행. 기존 시드와의 중복·갱신 여부를 별도 대조하지 않았다.
- `올데이 세트` 37개와 `고추장_제육_간장메밀_누들볼_세트_옵션.csv`의 60개 옵션 행은 반영하지 않았다.
- 세트 옵션은 `opt_group`/`opt_item`/`opt_policy`/`menu_opt_policy`의 정책 모델과 가격·필수·최대선택수 매핑을 먼저 확정한 뒤 별도 transaction으로 반영한다.

## 반영 메뉴

- `10776` 양송이 크림스프 — 4500원
- `10777` 단호박 크림스프 — 4900원
- `10778` 치킨토마토 스튜 — 4900원
- `10779` 포테이토 크림스프 — 4500원
- `10780` 카사바칩 — 1900원
- `10781` [고창] 리얼 수박 주스 — 4500원
- `10782` 아메리카노 (HOT) — 2700원
- `10783` 아메리카노 (ICE) — 2700원
- `10784` 코크제로 355ml — 2400원
- `10785` 스프라이트제로 355ml — 2400원
- `10786` 착즙 주스(그린밀싹) — 4500원
- `10787` 착즙 주스(오렌지당근) — 4500원
- `10788` 착즙 주스(레드클렌즈) — 4500원
- `10789` 생수 330ml — 500원
- `10790` 애사비 사과 스파클링 — 2600원

## 검증

- DB category/menu/menu_nutr 행 수와 `/api/kiosk/categories`, `/api/kiosk/menuList` 응답을 확인한다.
