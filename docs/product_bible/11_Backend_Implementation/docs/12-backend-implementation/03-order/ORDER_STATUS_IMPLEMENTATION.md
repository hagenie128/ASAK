# Order Status Implementation

## Endpoint

```http
PATCH /api/admin/orders/{orderId}/status
```

## 허용 전이

```text
RECEIVED → PREPARING
PREPARING → COMPLETED
```

## 중복 완료

이미 COMPLETED면:

- 현재 상태를 idempotent하게 반환
- 완료 event 중복 생성 금지

## TTS

Backend는 음성을 실행하지 않는다.

Frontend는 상태 변경 성공 응답 후 TTS를 실행한다.

## Response

```json
{
  "orderId": 128,
  "orderNo": "1225",
  "previousStatus": "PREPARING",
  "status": "COMPLETED",
  "updatedAt": "..."
}
```
