# Common Response Implementation

## ApiResponse

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

## Error Response

공통 envelope를 유지한다.

```java
public record ErrorData(
    String code,
    String field,
    Long targetId,
    Boolean canRetry
) {}
```

## 원칙

- HTTP Status와 ErrorCode를 함께 사용한다.
- 사용자용 한국어 문구는 Frontend에서 매핑한다.
- Backend message는 code 역할로 유지한다.
