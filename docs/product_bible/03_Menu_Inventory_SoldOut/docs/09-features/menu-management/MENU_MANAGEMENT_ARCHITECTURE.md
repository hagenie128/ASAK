# Menu Management Architecture

> Status: Current  
> Figma: SCR-016

## 1. 목적

관리자가 메뉴의 전체 판매 구성을 추가·수정하고, 저장 전에 유효성을 확인한다.

---

## 2. Form Sections

### Basic

- 메뉴명
- 설명
- 카테고리
- 가격
- 이미지
- 노출 상태
- 판매 상태

### Tags

- BEST
- NEW
- VEGAN

### Ingredients

- ingredient
- role
- quantity
- unit
- canRemove
- sold-out

### Option Groups

- group name
- required
- min/max
- options
- recommended
- additional amount
- active

### Nutrition

- calories
- carbohydrate
- protein
- fat
- sodium

### Allergen

- aggregated result
- warning
- source ingredient

---

## 3. Add and Edit

### Detail Add

새 메뉴 draft.

### Detail Edit

기존 메뉴를 load한 draft.

두 화면은 같은 Form Component를 공유한다.

---

## 4. Draft State

원본 data를 직접 수정하지 않는다.

```text
original
draft
dirtyFields
validationErrors
```

---

## 5. SaveBar

표시 조건:

```text
isDirty = true
```

표시 내용:

```text
변경사항 n개
취소
저장
```

---

## 6. IngredientSelectModal

이미 생성된 Figma component를 재사용한다.

필요 기능:

- 검색
- category filter
- checkbox
- selected count
- 취소
- 추가

---

## 7. Image Upload

MVP 선택지:

### A. 실제 upload API

권장 if backend time available.

### B. Mock URL/preview

포트폴리오 시연 가능.

어느 방식인지 문서에 명확히 표시한다.

---

## 8. Validation

### Required

- menuName
- category
- price
- image or fallback
- at least one valid configuration

### Price

```text
price >= 0
```

### Option Group

```text
0 <= minimumSelection <= maximumSelection
```

### Recommended

추천 option은 active이며 sold-out이 아니어야 한다.

### Ingredient

동일 ingredient 중복 추가 금지 또는 역할 중복 정책 명시.

---

## 9. Delete

삭제는 ConfirmDialog.

실제 DB 정책:

- soft delete 권장
- 기존 order history 보존
- 화면에서는 삭제/숨김 구분

---

## 10. React Mapping

```text
MenuManagementPage
MenuListPanel
MenuForm
BasicInfoSection
TagSelector
IngredientEditor
IngredientSelectModal
OptionGroupEditor
NutritionEditor
AllergenSummary
SaveBar
DeleteConfirmDialog
```

---

## 11. Backend Mapping

```text
MenuController
MenuService
MenuRepository
MenuRequestDto
MenuResponseDto
MenuMapper
```

연관 도메인 service를 무리하게 한 Service에 모두 넣지 않는다.

---

## 12. Implementation Checklist

- [ ] shared add/edit form
- [ ] draft state
- [ ] validation
- [ ] ingredient modal
- [ ] option group
- [ ] nutrition
- [ ] allergen
- [ ] image
- [ ] save bar
- [ ] delete
