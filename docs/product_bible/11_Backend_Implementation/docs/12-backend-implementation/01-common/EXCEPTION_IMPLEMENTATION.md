# Exception Implementation

## ErrorCode

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

## BusinessException

```java
public class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;

    public BusinessException(ErrorCode errorCode) {
        super(errorCode.name());
        this.errorCode = errorCode;
    }
}
```

## GlobalExceptionHandler

처리 대상:

- MethodArgumentNotValidException
- ConstraintViolationException
- BusinessException
- Exception

## 로그

- BusinessException: WARN 또는 INFO
- 예상하지 못한 Exception: ERROR
