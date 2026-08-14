# DTO and Mapper Rules

## 1. DTO Naming

```text
OrderCreateRequest
OrderUpdateRequest
OrderDetailResponse
OrderListItemResponse
SalesSummaryResponse
```

`Dto` suffix를 쓸지 여부는 프로젝트 전체에서 하나로 통일한다.

현재 문서에서는 역할이 명확한 이름을 우선한다.

---

## 2. Request와 Response 분리

같은 DTO 재사용 금지.

이유:

- 입력과 출력 필드가 다름
- Validation이 다름
- 보안·노출 정책이 다름

---

## 3. Patch Request

변경 가능한 필드만 포함한다.

```java
public record OrderStatusUpdateRequest(
    @NotNull OrderStatus status
) {}
```

---

## 4. List와 Detail 분리

List에는 필요한 최소 필드.

Detail에는 item·option 등 상세 포함.

---

## 5. Mapper

```java
public final class OrderMapper {
    public static OrderDetailResponse toDetailResponse(Order order) {
    }
}
```

Mapper에 DB 조회나 비즈니스 검증을 넣지 않는다.

---

## 6. Record

Java 25 환경에서 Request/Response DTO는 record 사용을 검토할 수 있다.

단, 팀 수업 방식과 Jackson/Validation 사용 패턴을 맞춘다.
