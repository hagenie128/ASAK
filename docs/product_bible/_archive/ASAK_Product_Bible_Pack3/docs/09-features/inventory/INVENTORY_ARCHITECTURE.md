# Inventory Architecture

> Status: Current

## 1. 목적

Inventory는 재료와 옵션의 판매 가능 상태를 관리하고, 메뉴 판매 상태에 미치는 영향을 계산한다.

ASAK MVP에서 재고 수량까지 완전한 ERP 수준으로 관리할 필요는 없다.

우선순위는:

- 품절 여부
- 품절 영향
- 관리자 변경
- Kiosk 즉시 반영

---

## 2. Inventory Scope

### MVP

- ingredient sold-out
- option item sold-out
- menu direct sold-out
- affected menu count
- Kiosk disable/badge

### Extension

- stock quantity
- safety stock
- auto sold-out
- purchase order
- supplier
- expiry date

---

## 3. Ingredient Classification

```text
CORE
BASE
STANDARD
OPTIONAL
```

Inventory 영향은 role에 따라 달라진다.

---

## 4. Direct vs Derived Sold-out

### Direct

관리자가 메뉴 자체를 품절 처리.

### Derived

재료 또는 옵션 품절로 메뉴가 판매 불가능해짐.

권장 데이터:

```text
directSoldOut
derivedSoldOut
effectiveSoldOut
```

```text
effectiveSoldOut = directSoldOut OR derivedSoldOut
```

---

## 5. Why Separate Direct and Derived

하나의 boolean만 사용하면:

- 왜 품절인지 알 수 없다.
- 재료가 복구되어도 메뉴를 자동 복구할지 판단하기 어렵다.
- 관리자 화면에서 영향 원인을 설명할 수 없다.

---

## 6. React Mapping

Admin:

```text
SoldOutManagementPage
SoldOutTargetTabs
CategoryFilterChips
SoldOutItemRow
AffectedMenuList
SaveBar
ConfirmDialog
```

Kiosk:

```text
SoldOutBadge
DisabledMenuCard
DisabledOptionItem
```

---

## 7. Backend Mapping

```text
inventory/
soldout/
menu/
ingredient/
option/
```

service responsibility:

- target validation
- affected menu calculation
- save batch changes
- rollback on failure
- effective sold-out calculation

---

## 8. DB Consideration

기존 entity/table 구조를 우선 사용한다.

필요 데이터:

```text
menu.is_sold_out
ingredient.is_sold_out
option_item.is_sold_out
```

추가 권장:

```text
sold_out_reason
updated_at
updated_by
```

단, 기존 schema와 중복이면 새 컬럼을 만들지 않는다.
