# Menu Entity Implementation

## 최소 Entity

- MenuCategory
- Menu
- Ingredient
- MenuIngredient
- OptionGroup
- OptionItem
- MenuOptionGroup
- Allergen
- IngredientAllergen
- MenuTag

## Menu 주요 필드

```text
id
menuName
description
basePrice
imageUrl
calories
isActive
directSoldOut
derivedSoldOut
createdAt
updatedAt
```

## effectiveSoldOut

DB 컬럼으로 저장할지 계산할지 결정해야 한다.

MVP 권장:

```java
public boolean isEffectiveSoldOut() {
    return directSoldOut || derivedSoldOut;
}
```

## Ingredient Role

```text
CORE
BASE
STANDARD
OPTIONAL
```

## 주의

Ingredient는 여러 Menu에서 공유한다.
Menu 삭제 cascade로 Ingredient를 삭제하지 않는다.
