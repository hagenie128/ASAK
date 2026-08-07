# ASAK 공부 — 관리자 주문 완료 TTS(음성 안내) 흐름

## 0. 문서 기본 정보와 한 줄 결론

| 항목 | 내용 |
| --- | --- |
| 공부 주제 | 관리자 실시간 주문 화면에서 "완료 처리" 성공 후 주문번호를 음성으로 안내하는 TTS 흐름 |
| 대상 화면 | `SCR-009` (관리자 실시간 주문 보드) |
| 확인 기준일 | 2026-08-05 |
| 확인한 범위 | Frontend 코드 / TTS Bible(명세) / Git 이력 · (Backend는 TTS 자체가 아닌 상태변경 경로만) |
| 정본 형식 기준 | `ASAK/docs/study/ai-review/ASAK_STUDY_EXAMPLE_CANONICAL.md` |

### 한 줄 결론

TTS는 서버가 아니라 **브라우저 Web Speech API로 동작**하며, 관리자가 주문을 `COMPLETED`로 바꾸는 상태변경 API가 성공한 뒤에만 `speak(...)`가 호출되어 "주문번호 N번, 주문이 완료되었습니다."를 읽어 준다. 단, TTS 성공/실패는 주문 상태와 분리되어 있어 음성이 실패해도 주문 완료는 유지된다.

> 주의: 명세(TTS Architecture)가 요구하는 **중복 방지(10초)·Queue 관리·Mute·localStorage 설정·`TtsControl` UI**는 현재 코드에 **아직 없다**. 아래 8·11절의 검증 상태를 함께 읽어야 한다.

---

## 1. 기능의 목적과 사용자 관점 동작

### 사용자 관점
관리자가 조리를 마친 주문의 "완료 처리" 버튼을 누르면, 매장 브라우저에서 주문번호가 음성으로 안내되어 고객 호출을 돕는다.

### 개발 관점
- TTS는 **외부 AI TTS 서버 없이** 브라우저 내장 `SpeechSynthesis`로 재생한다(명세 2절).
- 트리거는 **상태변경 API의 `COMPLETED` 성공 응답 이후 한 지점**뿐이다. 버튼 클릭 직후·polling·새로고침·조회 API에서는 발화하면 안 된다(명세 3절).
- 음성 실패가 주문 처리 실패로 번지지 않도록 **주문 성공과 TTS 실패를 같은 catch로 묶지 않는다**(명세 8절, 구현가이드 "완료 연결").

---

## 2. 학습 범위

- 포함: `ttsMessages.js`(메시지 빌더 + 발화), `LiveOrderPreview.jsx`(완료 성공 후 TTS 호출), `ordersApi.js`/`apiClient.js`(상태변경 요청 경로), TTS Bible 3종(명세 대조).
- 제외: 실제 브라우저 발화 재생 확인(스크립트 실행/수동 QA 미수행), 백엔드 TTS 로직(존재하지 않음 — TTS는 100% 클라이언트).

---

## 3. 확인한 파일과 읽은 이유

| 순서 | 파일 | 왜 읽었는가 | 공부한 핵심 |
| --- | --- | --- | --- |
| 1 | `ASAK-Admin/src/utils/ttsMessages.js` | 발화 로직·메시지 문구의 정본 | `isTtsSupported`, `speak`, `createOrderCompletedMessage` |
| 2 | `ASAK-Admin/src/components/admin/LiveOrderPreview.jsx` | TTS를 언제·어디서 호출하는지 | `runOrderAction`의 `COMPLETED` 분기, 실패 격리 |
| 3 | `ASAK-Admin/src/api/ordersApi.js` | 완료 처리가 어떤 요청을 보내는지 | `changeOrderStatus(orderId, status)` |
| 4 | `ASAK-Admin/src/api/apiClient.js` | 성공 응답을 화면이 어떻게 받는지 | envelope 해제(`unwrapResponse`) |
| 5 | `ASAK/docs/.../tts/TTS_ARCHITECTURE.md` 외 2종 | 명세와 코드 대조 | 트리거·중복방지·Mute·실패정책 |
| 6 | `ASAK/docs/planning/admin-todo-checklist-2026-08-05.md` | TODO-013 진행 상태 대조 | 체크리스트 vs 실제 코드 불일치 |

---

## 4. 전체 호출·데이터 흐름

```text
[관리자: PREPARING 주문의 "완료 처리" 클릭]
    │ onAction(orderId, "COMPLETED")
    ▼
[handleOrder] ── CANCELED 아님 ──▶ [runOrderAction(orderId, "COMPLETED")]
    │ setActionPending(true)
    ▼
[ordersApi.changeOrderStatus(orderId, "COMPLETED")]
    │ PATCH /api/admin/orders/{orderId}/COMPLETED
    ▼
[AdminOrderController → AdminOrderService → AdminOrderMapper → DB]   (상태 전이 검증·optimistic update)
    │ 성공 응답(envelope 해제)
    ▼
[toast.success("호출이 완료되었습니다.")]
    ▼
[status === "COMPLETED" 분기]
    │ orders.find(orderId) → order.orderNo 존재 시
    ▼
[speak(createOrderCompletedMessage(order.orderNo))]  ◀── 브라우저 Web Speech API(로컬, 서버 무관)
    │  성공: 발화        실패: catch → toast.error(음성 안내 실패) — 주문은 이미 성공 유지
    ▼
[refresh({ showLoading: false })]  → 최신 목록 재조회로 카드 갱신
```

핵심: **DB 상태변경(백엔드)** 과 **발화(브라우저)** 는 서로 다른 계층이며, 발화는 상태변경 성공 뒤에만 시작된다.

---

## 5. 파일별 복습

### 5-1. `ttsMessages.js` — 발화 엔진 + 메시지

핵심 export 3개:

```8:27:ASAK-Admin/src/utils/ttsMessages.js
export const speak = (text, options = {}) =>
  new Promise((resolve, reject) => {
    if (!text) {
      reject(new Error("TTS_EMPTY_TEXT"));
      return;
    }
    if (!isTtsSupported()) {
      reject(new Error("TTS_NOT_SUPPORTED"));
      return;
    }
    const config = { ...DefaultTtsOptions, ...options };
    const utterance = new SpeechSynthesisUtterance(text);
```

- `isTtsSupported()`: `window`·`speechSynthesis`·`SpeechSynthesisUtterance` 존재를 확인해 미지원 브라우저를 걸러낸다.
- `speak(text, options)`: Promise로 감싸 `onend→resolve`, `onerror→reject`. 기본값 `{ lang:"ko-KR", rate:0.95, pitch:1, volume:1 }`.
- `createOrderCompletedMessage(orderNo)`: `"주문번호 {orderNo}번, 주문이 완료되었습니다."` — 명세/구현가이드 문구와 **일치**.
- 입력 → 처리 → 출력: (문자열, 옵션) → utterance 구성·재생 → 재생 완료 시 resolve / 실패·미지원·빈 문자열 시 reject.
- 초보자 주의점: `speak`는 **재생 완료까지 기다리는 비동기**다. `await speak(...)`는 음성이 끝나거나 실패할 때까지 다음 줄로 넘어가지 않는다.
- 명세 대비 추가점: 명세 구현가이드에는 없는 `TTS_EMPTY_TEXT` 빈 문자열 방어가 코드에 더 있다(코드가 정본).

### 5-2. `LiveOrderPreview.jsx` — 트리거 지점

`runOrderAction`의 성공 경로:

```279:290:ASAK-Admin/src/components/admin/LiveOrderPreview.jsx
      toast.success(SUCCESS_MESSAGE[status]);
      if (status === "COMPLETED") {
        try {
          const order = orders.find((o) => o.orderId === orderId);
          if (status === "COMPLETED" && order?.orderNo) {
            await speak(createOrderCompletedMessage(order.orderNo));
          }
        } catch (err) {
          toast.error(err.message || "음성 안내에 실패했습니다."); // 주문은 이미 성공
        }
      }
```

- 상태(state): `actionPending`(중복 클릭 방지), `orders`(카드 목록), `cancelOrderId` 등.
- 트리거 조건: `status === "COMPLETED"` 성공 후에만. → 명세 3절 "COMPLETED 성공 응답 → TTS"와 **일치**.
- 실패 격리: `speak`의 실패는 별도 `try/catch`로 잡아 `toast.error`만 내고 주문 성공은 유지. → 명세 8절 "주문 상태 롤백 없음"과 **일치**.
- 초보자 주의점 1: 발화 대상 orderNo는 `orders.find(...)`로 **로컬 목록에서** 찾는다(응답이 아니라 화면 상태 기준). 목록에 해당 주문이 없거나 `orderNo`가 없으면 조용히 발화를 건너뛴다.
- 초보자 주의점 2: 카드 헤더에 보이는 번호(`liveOrderNo`)는 `orderNo`의 **뒤 4자리**지만, 음성은 **전체 `orderNo`** 를 읽는다(표시값과 발화값이 다름).
- 초보자 주의점 3: 안쪽 `if (status === "COMPLETED" && ...)`는 바깥 `if`와 조건이 겹치는 중복 검사다(동작엔 무해).

### 5-3. `ordersApi.js` / `apiClient.js` — 상태변경 경로

```8:8:ASAK-Admin/src/api/ordersApi.js
  changeOrderStatus: (orderId, status) => apiClient.patch(`/admin/orders/${orderId}/${status}`),
```

- 실제 요청: `PATCH /api/admin/orders/{orderId}/COMPLETED` (baseURL `/api` 포함).
- `apiClient`는 응답 인터셉터에서 envelope(`{success,status,code,message,data}`)를 풀어 **`data`만** 화면에 준다. 그래서 `runOrderAction`은 성공 여부를 예외 발생 여부로 판단한다.

---

## 6. 화면 상태

이 기능은 "발화"라는 브라우저 동작이라 Loading/Empty 같은 시각 상태보다는 **동작 분기**가 핵심이다. 화면 상태는 SCR-009 보드가 이미 가진 것을 공유한다.

| 상태 | 이 기능에서의 의미 | 코드 근거 |
| --- | --- | --- |
| Default | 완료 처리 성공 → 발화 시작 | `status === "COMPLETED"` 분기 |
| Disabled | 처리 중 버튼 비활성(중복 클릭 방지) | `actionPending` + 버튼 `disabled` |
| Error(음성) | 미지원/재생 실패 → `toast.error`, 주문은 성공 유지 | `speak` catch 블록 |
| Loading/Empty | TTS 고유 상태 아님 → **해당 없음** | (보드 조회 상태를 공유) |
| Mute/speaking/unsupported UI | 명세 9절 요구 → **미구현** | `TtsControl` 없음 |

- Figma·Screen Bible 확인: 상단 문구 "조리 완료 처리 및 TTS 알림을 관리합니다."는 코드에 존재. 그러나 명세 9절의 "주문 호출 [켜짐/꺼짐]" 토글 UI는 코드에서 **미발견(미구현)**.

---

## 7. 데이터 필드와 검증 상태

| 화면/음성에서 쓰는 것 | 필드 | 역할 | 검증 상태 |
| --- | --- | --- | --- |
| 발화 대상 주문 | `orderId` | 로컬 목록에서 주문 찾기 | 코드 확인됨 |
| 음성 문구의 번호 | `orderNo` | 메시지 빌더 입력 | 코드 확인됨 (실제 값 존재 여부는 런타임 미검증) |
| 상태 문자열 | `"COMPLETED"` | 트리거 조건·PATCH 경로 | 코드 확인됨 |
| 발화 옵션 | `lang/rate/pitch/volume` | utterance 설정 | 코드 확인됨(하드코딩 기본값), **localStorage 설정 미구현** |

---

## 8. 확인한 사실

- `ttsMessages.js`에 `isTtsSupported`, `speak`(Promise), `createOrderCompletedMessage`가 실제로 존재한다.
- `LiveOrderPreview.jsx`가 위 두 함수를 import해 `COMPLETED` 성공 후 `await speak(...)`를 호출한다.
- TTS 실패는 별도 `try/catch`로 격리되어 `toast.error`만 내고 주문 성공을 유지한다.
- TTS는 서버 호출이 없다(백엔드에 TTS 코드 없음). Web Speech API 기반이다.
- 메시지 문구가 명세(TTS_ARCHITECTURE 1절, IMPLEMENTATION_GUIDE)와 동일하다.
- 최신 커밋 `5cbf861 feat: 라이브 완료 TTS 및 에러 안내 문구 정리`가 이 기능을 추가했다.

---

## 9. 코드 근거에 따른 해석

- 트리거를 성공 응답 이후 한 곳으로만 둔 것은, 명세의 "버튼 클릭 직후/조회/새로고침 발화 금지" 원칙을 지키기 위한 배치로 보인다.
- `orders.find`로 로컬 목록에서 orderNo를 얻는 방식은, 상태변경 응답 본문(`data`)에 orderNo가 없어도 화면이 이미 가진 값으로 문구를 만들 수 있게 한 선택으로 보인다. 다만 목록·응답이 어긋나면 발화가 조용히 생략될 수 있다.
- 발화를 `await`로 기다린 뒤 `refresh`하므로, 음성이 긴 경우 목록 재조회가 그만큼 지연될 수 있다(체감 UX에 영향 가능).

---

## 10. 명세와 코드 불일치 / 미확인 / TODO

### 명세 대비 미구현 (팀 확인 필요)
- **중복 방지(동일 orderNo 10초 재호출 금지)**: 명세 7절 요구, 코드에 recent order map 없음 → 연속 완료 시 중복 발화 가능.
- **Queue 관리 / cancel 시점(logout 등)**: 명세 6절·구현가이드, 전용 처리 코드 없음(브라우저 기본 큐에 의존).
- **Mute 토글·speaking/unsupported UI(`TtsControl`)**: 명세 9절 요구, 미구현.
- **localStorage 설정(enabled/rate/...)**: 명세 5절 요구, 현재 기본값 하드코딩.
- **파일 구조**: 명세 4절은 `features/tts/ttsService.js` 등을 제시하나 실제는 `utils/ttsMessages.js` 한 파일에 통합.

### 문서 간 불일치
- `admin-todo-checklist-2026-08-05.md`의 TODO-013은 "부분 · `speak`/`ttsService.js` 없음"으로 기재. 그러나 실제 코드에는 `speak`가 **구현되어 있음**(커밋 `5cbf861`). → 체크리스트가 코드 진행보다 뒤처져 있음. 체크리스트 규칙(2행: "코드 인라인을 정본")에 따라 **체크리스트를 코드 기준으로 갱신 필요**(담당: Admin FE).

### 미확인
- 실제 브라우저에서 발화가 나는지(수동 QA) 미검증.
- 상태변경 응답에 orderNo가 포함되는지 여부(현재는 로컬 목록에 의존).

---

## 11. 검증 기록

| 항목 | 결과 | 비고 |
| --- | --- | --- |
| lint | 미실행 | 이 공부는 소스 미수정, 정적검사 생략 |
| build | 미실행 | 동상 |
| test | 미실행 | TTS-001~005 자동 테스트 코드 미발견 |
| 브라우저 발화 | 미실행 | 수동 QA 필요(개발서버 `npm run dev` 구동 중) |
| API | 미실행 | 상태변경 경로는 코드로만 확인 |
| DB | 미실행 | TTS는 DB 무관 |
| git | 확인됨 | `git log`로 `5cbf861` TTS 커밋 확인 |

> 실패가 아니라 "이 공부 세션에서 실행하지 않음"이다. 발화 확인은 아래 13절 절차로 직접 검증할 수 있다.

---

## 12. 직접 해 볼 확인 항목

1. 개발자도구 Console에서 `window.speechSynthesis`와 `SpeechSynthesisUtterance`가 있는지 확인한다(미지원 판정 이해).
2. PREPARING 주문의 "완료 처리"를 눌러 실제 음성이 나는지, 안 나면 어떤 toast가 뜨는지 관찰한다.
3. 같은 주문을 짧은 간격으로 두 번 완료 처리 시 발화가 몇 번 나는지 확인한다(중복 방지 미구현 검증).
4. 시스템/브라우저 소리를 끈 상태에서 완료 처리 시 주문 상태는 정상 완료되는지 확인한다(실패 격리 검증).

---

## 13. 연습문제

1. `speak`가 reject하는 세 가지 조건과 각각의 에러 메시지를 표로 정리하라.
2. TTS 발화 트리거가 "성공 응답 이후 한 곳"이어야 하는 이유를, polling/새로고침 발화의 문제와 함께 설명하라.
3. 명세 7절(10초 중복 방지)을 구현한다면 `LiveOrderPreview` 또는 별도 store 중 어디에 recent map을 두는 게 적절할지 근거와 함께 제안하라.
4. 카드에 보이는 번호(뒤 4자리)와 음성이 읽는 번호(전체 orderNo)가 다른 점이 사용자에게 문제될 수 있는지 판단하라.
5. TTS 실패 toast와 주문 성공 toast가 동시에 뜨는 상황을 사용자 관점에서 어떻게 다듬을지 제안하라.

---

## 14. 다음에 읽을 파일 (최대 3개)

1. `ASAK-back/.../AdminOrderService.java` — `COMPLETED` 상태 전이 규칙(발화 전제 조건).
2. `ASAK/docs/.../07-screens/SCR-009-ADMIN-LIVE-ORDER-BOARD.md` — 화면 요구와 Mute UI 명세 대조.
3. (구현 시) 신설 `store/ttsSettingsStore.js` 또는 `components/admin/TtsControl.jsx` — Mute·설정 도입 지점.
