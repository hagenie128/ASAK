# Entity and JPA Rules

> Status: Current

## 1. Entity Naming

```text
Order
OrderItem
OrderItemOption
Menu
Ingredient
OptionGroup
OptionItem
Payment
```

Class는 PascalCase.

DB는 snake_case.

---

## 2. PK

권장:

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
```

기존 DB 전략이 있으면 우선한다.

---

## 3. Fetch Type

To-One:

```text
LAZY 권장
```

Collection:

```text
LAZY
```

EAGER 남용 금지.

---

## 4. Cascade

부모 lifecycle과 완전히 일치할 때만 사용한다.

적합 가능:

```text
Order → OrderItem
OrderItem → OrderItemOption
```

주의:

```text
Menu → Ingredient
```

Ingredient는 공유 자원이므로 remove cascade 금지.

---

## 5. Setter

무분별한 public setter 금지.

권장:

```java
order.changeStatus(OrderStatus.PREPARING);
```

상태 변경 의도를 method 이름으로 표현한다.

---

## 6. Constructor / Builder

필수값을 보장한다.

Builder가 유효하지 않은 Entity 생성을 허용하지 않도록 주의한다.

---

## 7. equals/hashCode

연관관계를 포함하지 않는다.

JPA Entity에서는 ID 기반 구현을 신중하게 사용한다.

---

## 8. Soft Delete

Menu·Ingredient처럼 과거 주문 이력에 참조되는 데이터는 soft delete를 우선한다.

필드 예:

```text
is_deleted
deleted_at
```

기존 `isActive`/status와 의미 중복 여부를 먼저 확인한다.

---

## 9. N+1

해결 방법:

- fetch join
- EntityGraph
- DTO projection
- query 분리

모든 관계를 EAGER로 바꾸는 방식은 금지.
