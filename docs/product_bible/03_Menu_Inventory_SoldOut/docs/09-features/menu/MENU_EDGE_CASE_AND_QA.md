# Menu Edge Cases and QA

## Edge Cases

### 메뉴 숨김과 품절 동시 적용

관리 화면에서는 두 상태를 분리해서 보여준다.

### 추천 옵션이 품절

추천 badge 제거 또는 다른 추천으로 변경.

### Option Group의 min > active option count

메뉴 판매 차단 또는 관리자 저장 차단.

### 알레르기 자동 집계 누락

재료 기반 집계 실패 시 관리자 경고.

### 메뉴 이미지 없음

Kiosk fallback image.

### 가격 0 또는 음수

서버 validation.

### 동일 메뉴명

정책에 따라 unique 또는 category 내 unique.

---

## Allergy integrity (2026-08-12)

- Source of truth: `asak-data/scripts/input/allergy_260715.csv`; prefer `SALADY` rows.
- Menu allergens are derived by the `menu_ing -> ing_allergen -> allergen` relation. Correct high-confidence omissions at the ingredient relation, not by copying menu values.
- High-confidence links: implemented in seed and live DB, 11 links across 10 ingredients.
- Live checklist: 36 mismatches before, 26 remaining after the change; 10 menu records now match the official sheet.
- Deletion candidates remain `decision required`: shared dressing and sauce ingredients need an impact review before removing any allergen.
- Customer display remains `not connected`: the kiosk detail API and `MenuDetailPage` do not currently pass or render an allergens field.

### Allergy regression QA

- [x] The 11 approved links exist in seed and DB.
- [x] `ing_allergen` has no duplicate `(ing_id, allergen_id)` pairs in seed.
- [x] The original 36-menu checklist was recalculated against live DB.
- [ ] Add `allergens: string[]` to `GET /api/kiosk/menuDetail/{menuId}`.
- [ ] Render the real API data through `AllergenAccordion` in the kiosk detail screen.
- [ ] Browser QA: no allergen, one allergen, and long allergen-list states.

## Figma QA

- [ ] Menu List Error
- [ ] image fallback
- [ ] sold-out badge
- [ ] Detail validation state
- [ ] option sold-out
- [ ] recommendation
- [ ] allergen
- [ ] nutrition note

## Admin QA

- [ ] add/edit 구분
- [ ] required field
- [ ] image state
- [ ] tags
- [ ] ingredient role
- [ ] option min/max
- [ ] save/cancel/delete
