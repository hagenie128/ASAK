# TTS Bible

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `TTS_ARCHITECTURE.md`
- `TTS_EDGE_CASE_AND_QA.md`
- `TTS_IMPLEMENTATION_GUIDE.md`

---

## 원문: `TTS_ARCHITECTURE.md`

### TTS Architecture

> Status: Current
> Scope: Admin MVP

#### 1. 목적

관리자가 주문을 COMPLETED로 변경한 후 매장 브라우저에서 주문번호를 음성 안내한다.

```text
주문번호 {orderNo}번, 주문이 완료되었습니다.
```

#### 2. 기술

- Web Speech API
- SpeechSynthesis
- SpeechSynthesisUtterance

외부 AI TTS 서버는 MVP에서 사용하지 않는다.

#### 3. 정확한 Trigger

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

#### 4. 구조

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

#### 5. 설정

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

#### 6. Queue

연속 완료 주문은 SpeechSynthesis queue 순서대로 발화한다. 새 요청마다 cancel하지 않는다.

#### 7. 중복 방지

동일 orderNo는 10초 이내 재호출 금지.

방어:
1. 버튼 loading
2. Backend idempotency
3. recent order map

#### 8. 실패 정책

TTS 실패는 주문 상태를 되돌리지 않는다.

- Order COMPLETED 유지
- console 또는 Toast
- 미지원 브라우저도 주문 처리는 정상

#### 9. Mute

Admin 상단:
```text
주문 호출 [켜짐/꺼짐]
```

상태:
- enabled
- muted
- speaking
- unsupported

#### 10. 체크리스트

- [ ] support check
- [ ] message builder
- [ ] queue
- [ ] duplicate map
- [ ] mute
- [ ] localStorage
- [ ] success trigger
- [ ] failure isolation
- [ ] test speech

---

## 원문: `TTS_EDGE_CASE_AND_QA.md`

### TTS Edge Cases and QA

#### Edge Cases

- 동일 주문 완료 두 번 → 1회 발화
- 여러 주문 연속 완료 → queue 유지
- 미지원 브라우저 → 주문 성공 유지
- muted → 발화 없이 주문 성공
- 로그아웃 → queue cancel
- 새로고침 → 자동 발화 금지
- polling → trigger 금지

#### Test Cases

##### TTS-001
Given enabled, When PREPARING → COMPLETED 성공, Then 1회 발화.

##### TTS-002
Given same orderNo within 10s, Then duplicate blocked.

##### TTS-003
Given muted, Then no speech and order success.

##### TTS-004
Given unsupported browser, Then no crash.

##### TTS-005
Given three completed actions, Then queue order preserved.

#### QA

- [ ] TTS control
- [ ] enabled/muted/speaking/unsupported
- [ ] API success only
- [ ] duplicate map
- [ ] localStorage
- [ ] no order rollback

---

## 원문: `TTS_IMPLEMENTATION_GUIDE.md`

### TTS Implementation Guide

#### Message Builder

```js
export const createOrderCompletedMessage = (orderNo) =>
  `주문번호 ${orderNo}번, 주문이 완료되었습니다.`;
```

#### Service

```js
const DefaultTtsOptions = {
  lang: "ko-KR",
  rate: 0.95,
  pitch: 1,
  volume: 1,
};

export const isTtsSupported = () =>
  typeof window !== "undefined" &&
  "speechSynthesis" in window &&
  "SpeechSynthesisUtterance" in window;

export const speak = (text, options = {}) =>
  new Promise((resolve, reject) => {
    if (!isTtsSupported()) {
      reject(new Error("TTS_NOT_SUPPORTED"));
      return;
    }

    const config = { ...DefaultTtsOptions, ...options };
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = config.lang;
    utterance.rate = config.rate;
    utterance.pitch = config.pitch;
    utterance.volume = config.volume;
    utterance.onend = resolve;
    utterance.onerror = (event) =>
      reject(new Error(event.error || "TTS_PLAYBACK_FAILED"));

    window.speechSynthesis.speak(utterance);
  });
```

#### 완료 연결

주문 성공과 TTS 실패를 같은 catch로 묶지 않는다.

```js
const orderResult = await updateStatus();
showSuccessToast();

const ttsResult = await announceOrderCompleted(orderResult.orderNo);
if (!ttsResult.success) {
  logTtsFailure(ttsResult.reason);
}
```

#### cancel 사용 시점

- logout
- user stop
- test replay
- application shutdown

화면 unmount마다 cancel하지 않는다.
