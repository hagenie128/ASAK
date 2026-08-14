# Backend Common Implementation

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `COMMON_RESPONSE_IMPLEMENTATION.md`
- `EXCEPTION_IMPLEMENTATION.md`
- `NAMING_AND_PACKAGE_GUIDE.md`

---

## 원문: `COMMON_RESPONSE_IMPLEMENTATION.md`

### Common Response Implementation

#### ApiResponse

권장 구조:

```java
public record ApiResponse<T>(
    boolean success,
    String message,
    T data
) {
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, "OK", data);
    }

    public static ApiResponse<Void> success() {
        return new ApiResponse<>(true, "OK", null);
    }
}
```

#### Error Response

공통 envelope를 유지한다.

```java
public record ErrorData(
    String code,
    String field,
    Long targetId,
    Boolean canRetry
) {}
```

#### 원칙

- HTTP Status와 ErrorCode를 함께 사용한다.
- 사용자용 한국어 문구는 Frontend에서 매핑한다.
- Backend message는 code 역할로 유지한다.

---

## 원문: `EXCEPTION_IMPLEMENTATION.md`

### Exception Implementation

#### ErrorCode

```java
public enum ErrorCode {
    MENU_NOT_FOUND(HttpStatus.NOT_FOUND),
    MENU_SOLD_OUT(HttpStatus.CONFLICT),
    INVALID_OPTION_SELECTION(HttpStatus.BAD_REQUEST),
    ORDER_PRICE_CHANGED(HttpStatus.CONFLICT),
    ORDER_NOT_FOUND(HttpStatus.NOT_FOUND),
    INVALID_ORDER_STATUS_TRANSITION(HttpStatus.CONFLICT),
    PAYMENT_METHOD_DISABLED(HttpStatus.CONFLICT),
    PAYMENT_ALREADY_APPROVED(HttpStatus.CONFLICT),
    PAYMENT_FAILED(HttpStatus.BAD_REQUEST);

    private final HttpStatus status;
}
```

#### BusinessException

```java
public class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.name());
        this.errorCode = errorCode;
    }
}
```

#### GlobalExceptionHandler

처리 대상:

- MethodArgumentNotValidException
- ConstraintViolationException
- BusinessException
- Exception

#### 로그

- BusinessException: WARN 또는 INFO
- 예상하지 못한 Exception: ERROR

---

## 원문: `NAMING_AND_PACKAGE_GUIDE.md`

### Naming and Package Guide

#### 클래스

```text
MenuController
MenuService
MenuRepository
MenuCreateRequest
MenuDetailResponse
```

#### 메서드

```text
getMenuList
getMenuDetail
createOrder
updateOrderStatus
calculateTotalAmount
```

#### 패키지

현재 scaffold를 우선한다.

권장 예:

```text
com.asak
├─ common
├─ menu
├─ ingredient
├─ option
├─ order
├─ payment
├─ admin
└─ sales
```

전면 이동은 금지한다.
