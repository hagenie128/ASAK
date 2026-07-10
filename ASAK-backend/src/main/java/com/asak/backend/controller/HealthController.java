package com.asak.backend.controller;

import com.asak.backend.common.dto.ApiResponse;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    @GetMapping("/api/health")
    public ApiResponse<Map<String, String>> health() {
        return ApiResponse.ok(
                "HEALTH_OK",
                "ASAK backend is running",
                Map.of("status", "UP")
        );
    }
}
