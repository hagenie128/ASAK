# Database Engineering Rules

> Status: Current

## 1. Naming

```text
snake_case
```

### Table

```text
order_item
order_item_option
payment_method
ingredient_category
```

### Column

```text
created_at
updated_at
menu_id
order_status
```

---

## 2. Key

PK:

```text
id
```

FK:

```text
menu_id
order_id
ingredient_id
```

---

## 3. Index Naming

```text
idx_order_created_at
idx_order_status
idx_menu_category_id
```

Unique:

```text
uk_menu_name
uk_payment_method_code
```

---

## 4. Common Columns

필요 시:

```text
created_at
updated_at
created_by
updated_by
```

모든 테이블에 무조건 넣지 않고 운영 필요에 따라 선택한다.

---

## 5. Status Storage

API/Java enum과 동일한 UPPER_SNAKE_CASE code.

예:

```text
RECEIVED
PREPARING
COMPLETED
```

---

## 6. Money

정수 단위 원화:

```text
INT 또는 BIGINT
```

소수 floating type 금지.

---

## 7. Historical Integrity

과거 OrderItem은 당시 메뉴명·가격을 snapshot으로 보관하는 것을 권장한다.

메뉴 이름이 바뀌어도 과거 주문이 변하면 안 된다.

---

## 8. Foreign Key

관계는 명확히 하되 삭제 정책을 신중히 설정한다.

Menu 삭제가 Order history를 cascade delete하면 안 된다.

---

## 9. Migration

스키마 변경은 문서만 수정하지 않는다.

- migration
- seed
- API contract
- Figma field
- QA

를 함께 갱신한다.
