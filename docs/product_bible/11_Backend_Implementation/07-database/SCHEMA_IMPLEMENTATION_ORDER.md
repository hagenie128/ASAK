# Schema Implementation Order

1. category
2. ingredient_category
3. ingredient
4. allergen
5. option_group
6. option_item
7. menu
8. menu_ingredient
9. menu_option_group
10. order
11. order_item
12. order_item_option
13. payment_method
14. payment

## 이유

참조되는 마스터 데이터부터 만든다.

## 확인

- FK
- unique
- null
- default
- index
- soft delete
