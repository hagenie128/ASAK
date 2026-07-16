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
