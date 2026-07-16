# Menu Architecture

> Status: Current  
> Domain: Menu

## 1. 목적

Menu 도메인은 고객이 주문 가능한 상품 단위를 정의한다.

ASAK에서 Menu는 이름과 가격만 가진 단순 상품이 아니다.

Menu는 다음 요소의 조합이다.

- 카테고리
- 기본 가격
- 이미지
- 칼로리 및 영양정보
- 포함 재료
- 제외 가능한 재료
- 옵션 그룹
- 추천 옵션
- 태그
- 알레르기 정보
- 판매 상태
- 품절 영향

---

## 2. Canonical Menu Model

```json
{
  "menuId": 1,
  "menuName": "멕시칸 랩",
  "description": "신선한 채소와 단백질을 담은 랩",
  "categoryCode": "WRAP",
  "basePrice": 7200,
  "imageUrl": "...",
  "calories": 430,
  "isActive": true,
  "isSoldOut": false,
  "tags": ["BEST"],
  "ingredients": [],
  "optionGroups": [],
  "allergens": []
}
```

---

## 3. Menu Category

권장 code:

```text
SALAD
SANDWICH
WARM_BOWL
WRAP
SIDE
DRINK
```

카테고리명은 Figma·API·DB에서 동일하게 유지한다.

주의:

- `웜볼`
- `웜 보울`
- `Warm Bowl`

처럼 표기가 흔들리지 않도록 displayName과 code를 분리한다.

예:

```json
{
  "categoryCode": "WARM_BOWL",
  "displayName": "웜볼"
}
```

---

## 4. Menu Status

### isActive

- 고객에게 노출할 수 있는지
- 관리자가 숨김 처리할 수 있음

### isSoldOut

- 현재 주문 가능한지
- 직접 품절 또는 전파 품절 가능

### 상태 조합

| isActive | isSoldOut | 의미 |
|---|---|---|
| true | false | 판매 중 |
| true | true | 노출되지만 품절 |
| false | false | 숨김 |
| false | true | 운영상 비활성 + 품절 |

관리 화면에서는 상태를 하나의 toggle로 뭉치지 않는다.

---

## 5. Ingredient Role

Menu와 Ingredient의 관계는 역할을 가진다.

권장 role:

```text
CORE
BASE
STANDARD
OPTIONAL
```

### CORE

핵심 재료.

품절 시 메뉴 품절로 전파될 수 있다.

### BASE

메뉴의 기반.

품절 시 메뉴 또는 해당 기반 카테고리 주문 불가.

### STANDARD

기본 포함 재료.

제외 가능 여부를 가질 수 있다.

### OPTIONAL

추가 옵션 또는 선택 재료.

---

## 6. Option Structure

```text
Menu
└─ Option Group
   └─ Option Item
```

Option Group fields:

```text
optionGroupId
optionGroupName
isRequired
minimumSelection
maximumSelection
sortOrder
isActive
```

Option Item fields:

```text
optionItemId
optionItemName
additionalAmount
isRecommended
isSoldOut
sortOrder
```

---

## 7. Nutrition

Nutrition은 두 수준으로 나눈다.

### Base Nutrition

메뉴 기본 구성 기준.

### Calculated Nutrition

선택 옵션과 제외 재료를 반영한 추정값.

MVP 권장:

- Figma/React는 계산 가능 구조를 유지
- 실제 자동 계산은 추가 구현 범위
- 계산되지 않은 값은 확정값처럼 보여주지 않는다

---

## 8. Allergen

알레르기 정보는 메뉴에 직접 수기 입력하는 방식보다 재료 기반 집계를 권장한다.

```text
Ingredient
→ IngredientAllergen
→ MenuIngredient
→ Menu Allergen Summary
```

관리 화면은 집계 결과를 보여주되, 관리자가 예외를 확인할 수 있어야 한다.

---

## 9. Tags

권장 tags:

```text
BEST
NEW
VEGAN
```

Tag는 UI 장식이 아니라 검색·필터·운영에 활용 가능한 code로 관리한다.

---

## 10. Figma Mapping

### Kiosk

- SCR-003 Menu List
- SCR-004 Menu Detail
- SCR-005 Cart option summary

### Admin

- SCR-016 Menu Management
- IngredientSelectModal
- MenuCard
- OptionGroup
- SaveBar

---

## 11. React Mapping

### Kiosk

```text
MenuListPage
MenuDetailPage
MenuCard
CategoryTabs
OptionGroup
OptionItem
AllergenNotice
NutritionSummary
```

### Admin

```text
MenuManagementPage
MenuForm
IngredientSelectModal
OptionGroupEditor
NutritionPanel
AllergenPanel
TagSelector
SaveBar
```

---

## 12. Backend Mapping

```text
menu/
ingredient/
option/
allergen/
nutrition/
tag/
```

권장 domain package 기준으로 분리하되 실제 프로젝트 구조에 맞춘다.

---

## 13. Implementation Checklist

- [ ] category code 통일
- [ ] Menu active/sold-out 분리
- [ ] ingredient role
- [ ] option group min/max
- [ ] recommended option
- [ ] nutrition source 구분
- [ ] allergen aggregation
- [ ] tags
- [ ] Kiosk sold-out state
- [ ] Admin validation
