# 재료 품절 캐스케이드 설계 — 조사한 원본 쿼리 결과

`ingredient-soldout-cascade-design.md` 작성 근거가 된 실제 DB 조회 결과 원본이다.
조회 시점: 2026-08-20, `asak_db` (운영 공용 DB).

## common_code (role/group 코드 전체)

group_id 6 = ing.type_id (재료 자체 분류), group_id 7 = menu_ing.role_id (메뉴 내 역할),
group_id 5 = opt_group.group_type_id (옵션 그룹 종류)

```
(26, 6, 'VEGGIE',   '채소',   16, 1)
(27, 6, 'PROTEIN',  '단백질', 17, 1)
(28, 6, 'DRESSING', '드레싱', 18, 1)
(29, 6, 'BASE',     '베이스', 19, 1)
(30, 6, 'SIDE',     '사이드', 20, 1)
(31, 6, 'BEVERAGE', '음료',   21, 1)

(32, 7, 'CORE',    '핵심 재료',     22, 1)
(33, 7, 'BASE',    '베이스 재료',   23, 1)
(34, 7, 'DEFAULT', '일반 기본 재료', 24, 1)

(20, 5, 'TOPPING',   '토핑 추가',       10, 1)
(21, 5, 'DRESSING',  '드레싱 옵션',     11, 1)
(22, 5, 'BASE',      '베이스 옵션/추가', 12, 1)
(23, 5, 'SET_SIDE',  '세트 사이드 선택', 13, 1)
(24, 5, 'SET_DRINK', '세트 음료 선택',  14, 1)
(25, 5, 'REQUEST',   '빼기/요청사항',   15, 1)
```

## opt_item ↔ ing 연결 현황

opt_item 전체 115행 중 ing_id가 채워진 행 수: 115 (전수)

재료 품절 처리(143 베이컨, 149 에그, 151 두부, 175 드라이토마토, 191 김자반, 210 바베큐소스) 직후
연결된 opt_item과 비교 — **아직 opt_item.sold_out=0으로 안 맞음** (연쇄 처리가 없다는 실증):

```
(341, '단호박크림스프', ing=75,  opt_item.sold_out=0, ing.sold_out=1)
(282, '베이컨',         ing=143, opt_item.sold_out=0, ing.sold_out=1)
(284, '에그',           ing=149, opt_item.sold_out=0, ing.sold_out=1)
(285, '두부',           ing=151, opt_item.sold_out=0, ing.sold_out=1)
(315, '드라이토마토',    ing=175, opt_item.sold_out=0, ing.sold_out=1)
(7641,'드라이토마토 빼기', ing=175, opt_item.sold_out=0, ing.sold_out=1)
(325, '김자반',         ing=191, opt_item.sold_out=0, ing.sold_out=1)
(1844,'김자반 빼기',     ing=191, opt_item.sold_out=0, ing.sold_out=1)
(2974,'바베큐소스 빼기', ing=210, opt_item.sold_out=0, ing.sold_out=1)
```

## "빼기" 옵션은 REQUEST 그룹 — 캐스케이드 제외 대상

```
(282,  '베이컨',         group=242 '토핑 추가',  type=TOPPING)
(284,  '에그',           group=242 '토핑 추가',  type=TOPPING)
(285,  '두부',           group=242 '토핑 추가',  type=TOPPING)
(315,  '드라이토마토',    group=242 '토핑 추가',  type=TOPPING)
(325,  '김자반',         group=242 '토핑 추가',  type=TOPPING)
(1844, '김자반 빼기',     group=246 '재료 빼기', type=REQUEST)
(2974, '바베큐소스 빼기', group=246 '재료 빼기', type=REQUEST)
(7641, '드라이토마토 빼기', group=246 '재료 빼기', type=REQUEST)
```

group_type별 opt_group 존재 현황(전체):
```
('TOPPING',   '토핑 추가',       1개 그룹)
('DRESSING',  '드레싱 선택',     2개 그룹: '드레싱 선택'/'드레싱 추가')
('BASE',      '베이스 선택/추가', 1개 그룹: '베이스 변경')
('SET_SIDE',  '세트 사이드 선택', 1개 그룹)
('SET_DRINK', '세트 음료 선택',  1개 그룹)
('REQUEST',   '빼기/요청사항',   1개 그룹)
```

## "베이스 변경" 옵션의 실체 — 전부 유료(+1,500원)

opt_group 243 '베이스 변경' → opt_policy 18 → opt_policy_item 3개:

```
(policy=18, opt_item=334, name='포케볼',   ing_id=58, add_price=1500, sold_out=0, is_default=0)
(policy=18, opt_item=335, name='메밀면볼', ing_id=61, add_price=1500, sold_out=0, is_default=0)
(policy=18, opt_item=336, name='파스타볼', ing_id=66, add_price=1500, sold_out=0, is_default=0)
```

→ ing_id가 menu_ing role=BASE 재료(367 채소, 771 곡물·채소, 1571 메밀면·채소 등)와 다른 별개 id.
즉 "베이스 변경"은 재료 단위 교체가 아니라 메뉴 자체를 다른 스타일(포케볼/메밀면볼/파스타볼)로
업그레이드하는 옵션이며, 셋 다 무료(add_price=0) 대안이 아니다.

이 policy를 쓰는 메뉴 샘플(15개 중 일부): 랜치 콥 샐러디(2114), 로스트삼겹 포케볼(2534),
탄단지 샐러디(1978), 바베큐삼겹 덮밥(3105) 등.

## menu_ing role=BASE 샘플 (재료 → 그 재료를 쓰는 메뉴)

```
(menu=768,  '그라브락스 연어 포케볼',  ing=771,  '곡물, 채소')
(menu=1568, '우삼겹메밀면 누들볼',    ing=1571, '메밀면, 채소')
(menu=1978, '탄단지 샐러디',          ing=367,  '채소')
(menu=2114, '랜치 콥 샐러디',         ing=367,  '채소')
(menu=2534, '로스트삼겹 포케볼',      ing=771,  '곡물, 채소')
...
```

메뉴 5478(채소볼)의 BASE 재료는 367(채소) 하나뿐이고, 이 메뉴엔 "베이스 변경" 옵션 정책
자체가 연결돼 있지 않음(옵션 쪽 조회 결과 0행) — 대체 옵션이 원천적으로 없는 케이스.

## 참고: 이전에 품절 처리한 항목 (2026-08-20)

```
menu:     1167 칠리베이컨 포케볼, 6811 멜팅치즈 치킨 샌드위치
ing BASE: 1571 메밀면, 채소
ing CORE: 143 베이컨, 151 두부
ing DEFAULT: 175 드라이토마토, 191 김자반, 210 바베큐소스, 149 에그
opt_item DRESSING: 265/266 시저 (선택+추가)
```
