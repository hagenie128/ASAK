# Payment Method Implementation

## 상태

```text
ENABLED
DISABLED
MAINTENANCE
```

## Kiosk 조회

활성/점검 중 수단만 정책에 따라 반환한다.

## Admin 수정

필드:

```text
displayName
status
sortOrder
receiptMessage
failureRetentionMinutes
```

## 주의

전체 결제수단 비활성화는 ConfirmDialog와 Server validation이 필요하다.
