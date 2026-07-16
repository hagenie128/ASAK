# Kitchen and TTS Tests

## KIT-001 — 상태 전이

```text
RECEIVED → PREPARING → COMPLETED
```

## KIT-002 — 잘못된 전이

Expected:
- 서버 차단
- 사용자 안내

## KIT-003 — 완료 중복 클릭

Expected:
- 1회 처리
- TTS 1회

## KIT-004 — Polling stale response

Expected:
- 최신 updatedAt 우선

## KIT-005 — 네트워크 실패

Expected:
- 기존 card 유지
- Error Toast

## TTS-001 — 완료 성공

Expected:
- orderNo 발화

## TTS-002 — 같은 주문 10초 이내

Expected:
- 중복 차단

## TTS-003 — 음소거

Expected:
- 주문 완료 정상
- 발화 없음

## TTS-004 — 브라우저 미지원

Expected:
- crash 없음

## TTS-005 — 연속 완료

Expected:
- queue 순서 유지
