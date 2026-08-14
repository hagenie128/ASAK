# Menu Query Implementation

## Kiosk Menu List

```http
GET /api/kiosk/menuList
```

Service 순서:

1. categoryCode 검증
2. active menu 조회
3. effective sold-out 계산
4. list DTO 변환
5. sortOrder 적용

## Kiosk Menu Detail

```http
GET /api/kiosk/menuDetail/{menuId}
```

필요 데이터:

- Menu
- Category
- Ingredients
- Option Groups
- Option Items
- Allergens
- Tags

## N+1 방지

선택지:

- fetch join
- EntityGraph
- DTO projection
- 명시적 query 분리

모든 관계 EAGER 전환 금지.
