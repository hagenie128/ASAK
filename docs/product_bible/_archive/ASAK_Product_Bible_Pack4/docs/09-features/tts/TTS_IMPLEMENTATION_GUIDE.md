# TTS Implementation Guide

## Message Builder

```js
export const createOrderCompletedMessage = (orderNo) =>
  `주문번호 ${orderNo}번, 주문이 완료되었습니다.`;
```

## Service

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

## 완료 연결

주문 성공과 TTS 실패를 같은 catch로 묶지 않는다.

```js
const orderResult = await updateStatus();
showSuccessToast();

const ttsResult = await announceOrderCompleted(orderResult.orderNo);
if (!ttsResult.success) {
  logTtsFailure(ttsResult.reason);
}
```

## cancel 사용 시점

- logout
- user stop
- test replay
- application shutdown

화면 unmount마다 cancel하지 않는다.
