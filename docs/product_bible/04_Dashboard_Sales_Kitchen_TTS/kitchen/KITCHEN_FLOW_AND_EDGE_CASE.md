# Kitchen Flow and Edge Cases

## Main Flow

```text
Payment APPROVED
→ Order RECEIVED
→ Live Order Board
→ PREPARING
→ COMPLETED
→ TTS
→ Dashboard active count 감소
```

매출은 Payment APPROVED 기준으로 집계하고 Order COMPLETED와 혼동하지 않는다.

## Polling

- 이전 요청이 끝나지 않았으면 새 요청 금지
- unmount 시 interval clear
- 오류 시 기존 카드 제거 금지

## Edge Cases

### 상태 변경 중 Polling 충돌
- updatedAt 또는 request timestamp 비교
- 최신 응답 우선

### 완료 버튼 중복
- loading disabled
- backend idempotent
- TTS duplicate block

### 다른 관리자가 먼저 완료
- 현재 상태 반환 후 UI 동기화

### 네트워크 실패
- 기존 카드 유지
- Error Toast

### 주문 취소
- MVP 포함 전 Live Board action에 넣지 않는다

## QA

- [ ] oldest first
- [ ] status transition
- [ ] duplicate click
- [ ] polling clear
- [ ] stale response
- [ ] error preserves data
- [ ] completed removed
- [ ] TTS once
