# Live Order and TTS Implementation

## Polling

- 5초
- 중복 요청 방지
- unmount cleanup
- stale response 방지

## 상태 변경

```text
button loading
→ PATCH
→ success UI
→ Toast
→ TTS
```

## TTS

- API 성공 후
- same orderNo 10초 block
- mute localStorage
- queue 유지

## 금지

렌더링 또는 polling response만으로 발화하지 않는다.
