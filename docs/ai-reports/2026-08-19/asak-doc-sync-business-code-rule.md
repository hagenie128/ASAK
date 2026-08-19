# ASAK 문서 동기화 — 업무 코드 규칙 (2026-08-19)

- 범위: `ApiResponse` 오류 envelope와 문자열 업무 코드 규칙
- 정본: `ASAK-back/docs/implementation_guide/04-api-db-implementation.md`
- 소스코드·실제 DB·Git: 수정하지 않음
- 인증 정보: 기록하지 않음

## 확인 근거

- `ASAK-back/src/main/java/com/asak/common/response/ApiResponse.java`
  - 응답 필드: `success`, `status`, `code`, `message`, `data`
  - `code`는 `String`이며 레거시 숫자 코드를 사용하지 않는다는 주석이 존재
- `ASAK-back/src/main/java/com/asak/common/exception/ErrorCode.java`
  - `code`는 HTTP status와 별도인 문자열 업무 코드

## 반영 내용

1. 중앙 문서 `ASAK/docs/implementation_guide/04-api-db-implementation.md`를 백엔드 재작성본 기준으로 정렬했다.
2. DevCopilot workspace 2의 기존 API 카드 30개에 `response_error` 규칙을 갱신했다.

허브에 반영한 공통 규칙은 다음과 같다.

```json
{
  "success": false,
  "status": "HTTP status",
  "code": "ErrorCode 문자열 상수",
  "message": "...",
  "data": null
}
```

- `status`는 HTTP 전송 결과다.
- `code`는 `ErrorCode.java` enum 상수와 같은 문자열 업무 코드다.
- 레거시 숫자 코드(`0000`, `1001` 등)는 사용하지 않는다.

## 검증 결과

- DevCopilot `get_api_specs(workspace_id=2)` 재조회: API 카드 30개 중 30개가 위 오류 응답 규칙을 보유
- API별 실제 오류 코드·HTTP 응답은 서버 실행 또는 Bruno 검증 전까지 구현 완료로 표기하지 않는다.

## 남은 사항

- 카드별 `response_error`에는 공통 규칙만 넣었다. API별 발생 가능한 `ErrorCode` 목록은 Controller·Service·Bruno 실행 근거가 확보된 API부터 개별 명세에 추가해야 한다.
