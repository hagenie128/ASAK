# ASAK Product Bible Pack 3

## Scope

이 Pack은 ASAK 메뉴 도메인의 핵심 4개 영역을 다룬다.

1. Menu
2. Inventory
3. Sold-out
4. Menu Management

## Why These Features Belong Together

메뉴는 독립된 상품이 아니라 다음 구조의 결과다.

```text
Menu
├─ Category
├─ Ingredient
├─ Ingredient Role
├─ Option Group
├─ Option Item
├─ Nutrition
├─ Allergen
├─ Tag
└─ Sold-out Policy
```

따라서 메뉴 관리와 품절 관리는 같은 데이터 구조를 공유해야 한다.

## Canonical Principle

- 메뉴 상태는 단순 boolean 하나로 끝나지 않는다.
- 품절은 메뉴·재료·옵션에 따라 전파될 수 있다.
- 핵심 재료와 베이스 품절은 메뉴 판매 가능성에 영향을 준다.
- 일반 재료 품절은 항상 메뉴 전체 품절을 의미하지 않는다.
- Figma와 DB가 같은 역할명과 상태값을 사용해야 한다.
