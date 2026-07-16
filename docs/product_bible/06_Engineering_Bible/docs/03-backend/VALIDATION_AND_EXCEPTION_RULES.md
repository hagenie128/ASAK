# Validation and Exception Rules

## 1. Validation Layer

### Frontend

빠른 UX 피드백.

### Bean Validation

형식·필수값.

### Service Validation

비즈니스 규칙.

### DB Constraint

최종 데이터 무결성.

---

## 2. Bean Validation

```java
@NotBlank
@Size
@NotNull
@Positive
@PositiveOrZero
@Min
@Max
```

예:

```java
public record MenuCreateRequest(
    @NotBlank String menuName,
    @NotNull Long categoryId,
    @PositiveOrZero Integer basePrice
) {}
```

---

## 3. Business Validation

Bean Validation으로 표현하기 어려운 규칙:

- 필수 option min/max
- 품절 메뉴 주문
- 상태 전이
- 가격 불일치
- 결제수단 비활성

Service에서 검증한다.

---

## 4. Exception Structure

권장:

```text
BusinessException
NotFoundException
ConflictException
InvalidStateException
```

프로젝트 규모에 맞춰 하나의 BusinessException + ErrorCode로 단순화 가능.

---

## 5. ErrorCode

```java
public enum ErrorCode {
    MENU_NOT_FOUND,
    MENU_SOLD_OUT,
    INVALID_OPTION_SELECTION,
    ORDER_PRICE_CHANGED,
    PAYMENT_FAILED
}
```

API 코드값은 UPPER_SNAKE_CASE.

---

## 6. GlobalExceptionHandler

책임:

- Exception → HTTP Status
- 공통 Error Response
- Validation field error
- 로그 수준 결정

---

## 7. HTTP Status

| Situation | Status |
|---|---|
| 성공 조회 | 200 |
| 생성 | 201 |
| 잘못된 입력 | 400 |
| 인증 필요 | 401 |
| 권한 없음 | 403 |
| 없음 | 404 |
| 상태 충돌 | 409 |
| 서버 오류 | 500 |
