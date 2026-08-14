# Payment Method Implementation

## Current Code Status (2026-08-06)

- `AdminPaymentMethodController`는 `@RequestMapping("/api/admin/paymentMethods")`만 있고 메서드는 없다.
- `AdminPaymentMethodService`, `AdminPaymentMethodMapper`, `AdminPaymentMethodMapper.xml`도 구현 스텁 상태다.
- Admin 프론트 화면은 존재하지만 현재 `usePaymentMethodDraft` + mock repository로만 동작한다.
- 따라서 아래 필드/규칙은 현재 서버 구현 사실이 아니라 **구현 목표/초안**이다.

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

현재 프론트 저장 상태는 `methodId`, `isActive`, `sortOrder` 중심이며, `receiptMessage`, `failureRetentionMinutes`는 정적 정책 카드로만 노출된다.

## 주의

전체 결제수단 비활성화는 ConfirmDialog와 Server validation이 필요하다.

## Decision Needed

- 경로 표기를 `/paymentMethods`로 유지할지 kebab-case로 바꿀지
- 저장 방식을 개별 PATCH 순차 호출로 할지, 일괄 저장 endpoint로 둘지
- `MAINTENANCE` 상태와 키오스크 미리보기의 노출 규칙을 어디서 판정할지
