# Menu Management Frontend Implementation

## Shared Form

Add/Edit는 동일 Form.

State:

```text
original
draft
dirtyFields
validationErrors
```

## Sections

- Basic
- Tags
- Ingredients
- Option Groups
- Nutrition
- Allergens

## Modal

IngredientSelectModal 기존 Figma/React 구현 우선.

## Save

- 중복 클릭 방지
- 실패 시 draft 유지
- 성공 후 original 갱신
