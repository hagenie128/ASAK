# Order Status Implementation

## Endpoint

```http
PATCH /api/admin/orders/{orderId}/{status}
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
  "success": true,
  "status": 200,
  "code": "ADMIN_ORDER_STATUS_CHANGE_SUCCESS",
  "message": "관리자 주문 상태 변경 성공",
  "data": null
}
```
