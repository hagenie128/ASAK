# TTS Architecture

> Status: Current  
> Scope: Admin MVP

## 1. 목적

관리자가 주문을 COMPLETED로 변경한 후 매장 브라우저에서 주문번호를 음성 안내한다.

```text
주문번호 {orderNo}번, 주문이 완료되었습니다.
```

## 2. 기술

- Web Speech API
- SpeechSynthesis
- SpeechSynthesisUtterance

외부 AI TTS 서버는 MVP에서 사용하지 않는다.

## 3. 정확한 Trigger

금지:
- 버튼 클릭 직후
- polling 발견
- 새로고침
- 조회 API

허용:
```text
상태 변경 API COMPLETED 성공 응답
→ TTS
```

## 4. 구조

```text
src/
├─ features/tts/
│  ├─ ttsService.js
│  ├─ ttsMessages.js
│  └─ README.md
├─ hooks/useOrderCompletionTts.js
├─ store/ttsSettingsStore.js
└─ components/admin/TtsControl.jsx
```

실제 프로젝트 구조를 우선하며 중복 폴더를 만들지 않는다.

## 5. 설정

```js
{
  enabled: true,
  rate: 0.95,
  pitch: 1,
  volume: 1,
  lang: "ko-KR"
}
```

localStorage 저장.

## 6. Queue

연속 완료 주문은 SpeechSynthesis queue 순서대로 발화한다. 새 요청마다 cancel하지 않는다.

## 7. 중복 방지

동일 orderNo는 10초 이내 재호출 금지.

방어:
1. 버튼 loading
2. Backend idempotency
3. recent order map

## 8. 실패 정책

TTS 실패는 주문 상태를 되돌리지 않는다.

- Order COMPLETED 유지
- console 또는 Toast
- 미지원 브라우저도 주문 처리는 정상

## 9. Mute

Admin 상단:
```text
주문 호출 [켜짐/꺼짐]
```

상태:
- enabled
- muted
- speaking
- unsupported

## 10. 체크리스트

- [ ] support check
- [ ] message builder
- [ ] queue
- [ ] duplicate map
- [ ] mute
- [ ] localStorage
- [ ] success trigger
- [ ] failure isolation
- [ ] test speech
