package com.asak.backend.common.dto;

public record ApiResponse<T>(
        boolean success,
        int status,
        String code,
        String message,
        T data
) {
    public static <T> ApiResponse<T> ok(String code, String message, T data) {
        return new ApiResponse<>(true, 200, code, message, data);
    }
}
