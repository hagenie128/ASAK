# TTS Edge Cases and QA

## Edge Cases

- 동일 주문 완료 두 번 → 1회 발화
- 여러 주문 연속 완료 → queue 유지
- 미지원 브라우저 → 주문 성공 유지
- muted → 발화 없이 주문 성공
- 로그아웃 → queue cancel
- 새로고침 → 자동 발화 금지
- polling → trigger 금지

## Test Cases

### TTS-001
Given enabled, When PREPARING → COMPLETED 성공, Then 1회 발화.

### TTS-002
Given same orderNo within 10s, Then duplicate blocked.

### TTS-003
Given muted, Then no speech and order success.

### TTS-004
Given unsupported browser, Then no crash.

### TTS-005
Given three completed actions, Then queue order preserved.

## QA

- [ ] TTS control
- [ ] enabled/muted/speaking/unsupported
- [ ] API success only
- [ ] duplicate map
- [ ] localStorage
- [ ] no order rollback
