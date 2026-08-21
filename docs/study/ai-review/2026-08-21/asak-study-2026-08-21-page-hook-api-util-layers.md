# ASAK-Admin 레이어 공부 — Page / Hook / Api / Util / Constants가 하는 일

- 날짜: 2026-08-21
- 계기: 오늘 만든 "Admin 영수증 출력" 기능(`OrderManagePage.jsx` ↔ `usePrintReceiptQuery.js` ↔
  `ordersApi.js` ↔ `receiptFormat.js` ↔ `constants/api.js`)이 왜 파일 5개로 쪼개져 있는지 헷갈려서 정리함.
- 목적: 규칙 암기가 아니라 "이 파일이 없으면 무슨 문제가 생기는지"로 이해하기.

## 1. 한 장 그림

```text
[Page]        화면 하나. 사용자가 보고 클릭하는 곳. 상태(state)를 들고 있음.
  │  "영수증 출력 버튼 눌렀다" 같은 이벤트만 앎. HTTP나 URL은 모름.
  ▼
[Hook]        "이 화면에 필요한 데이터/동작"을 캡슐화. useState + useEffect 묶음.
  │  로딩/성공/실패 상태, 폴링 같은 시간 흐름을 다룸. 화면(JSX)은 모름.
  ▼
[Api]         "서버 주소로 이런 요청을 보낸다"만 앎. 함수 하나 = 요청 하나.
  │  React를 모름. axios/apiClient만 씀.
  ▼
[Constants]   Api가 쓰는 URL 문자열들을 한곳에 모아둠.
  │  로직 없음. 그냥 값.
  ▼
[Util]        상태 없는 순수 계산/변환 함수. 같은 입력 → 항상 같은 출력.
              누구나(Hook도 Page도 Api도) 갖다 쓸 수 있음.
```

핵심 규칙 한 줄: **아래로 갈수록 "React를 모르는 코드"가 된다.**
Page는 React 없이 못 사는 코드, Util은 React가 뭔지도 모르는 코드.

## 2. 오늘 만든 기능으로 실제 대조

영수증 출력 버튼을 눌렀을 때 실제로 벌어지는 일:

```text
OrderDetailPanel.jsx (버튼)
  onClick={() => onPrintReceipt(selectedOrder.orderId)}
        │
        ▼
OrderManagePage.jsx (Page)
  handlePrintReceipt(orderId) → 확인창 띄움 → printReceipt(selectedOrder) 호출
        │
        ▼
usePrintReceiptQuery.js (Hook)
  printReceipt(order): ordersApi.printReceipt(order) 호출 → eventId 저장 → status="pending"
  useEffect: eventId가 있는 동안 1초마다 ordersApi.listDeviceEvents() 재호출
             → COMPLETED/FAILED 되면 status 갱신하고 폴링 스스로 멈춤
        │
        ▼
ordersApi.js (Api)
  printReceipt(order) = apiClient.post(API_ENDPOINTS.printReceipt(order.orderId), {...})
  listDeviceEvents()  = apiClient.get(API_ENDPOINTS.deviceEvents)
        │
        ▼
constants/api.js (Constants)
  printReceipt: (orderId) => `${API_BASE_PATH}/orders/${orderId}/receipt-print`
  deviceEvents: `${API_BASE_PATH}/device-events`
        │
        ▼
receiptFormat.js (Util)
  buildReceiptText(order) — order 객체를 받아서 영수증 텍스트(줄바꿈 포함 문자열)만 리턴.
  fetch도 useState도 없음. order를 넣으면 항상 같은 문자열이 나옴.
  ordersApi.printReceipt 안에서 payload를 만들 때 사용됨.
```

## 3. 계층별로 자주 헷갈리는 것 Q&A

### Q. Hook이랑 Util이 뭐가 다른데? 둘 다 함수잖아.

- **Util**은 상태가 없다. `buildReceiptText(order)`를 100번 불러도 매번 같은 문자열이 나온다.
  React 컴포넌트 밖에서도, Node.js 콘솔에서도 그냥 실행된다.
- **Hook**은 상태(`useState`)와 생명주기(`useEffect`)를 갖는다. `usePrintReceiptQuery()`는
  부를 때마다 "지금 몇 번째 폴링 중인지"를 기억한다. React 컴포넌트 안에서만 부를 수 있다.

시험 방법: 함수 안에 `useState`/`useEffect`가 있으면 Hook, 없으면 Util.

### Q. 왜 `ordersApi.js`(Api)를 따로 두고 Hook 안에서 바로 `fetch`를 안 써?

오늘 처음 만든 `usePrintReceiptQuery.js` 초안이 정확히 이 실수를 했었다 — RTOS 예제를 복붙하면서
`fetch(API)`처럼 URL을 Hook 안에 직접 박아놓고, `useState`/`useEffect` import도 빠져서 컴파일 자체가
안 됐음. Api 계층을 분리하면:

- URL이 바뀌어도 `ordersApi.js` 한 곳만 고치면 된다 (Hook·Page는 그대로).
- 같은 API를 여러 Hook/Page에서 재사용할 수 있다.
- Hook 코드가 "무엇을 언제 부르나"에만 집중하고, "어디로 어떻게 부르나"는 신경 안 써도 된다.

### Q. `constants/api.js`는 왜 `ordersApi.js` 안에 그냥 문자열로 안 쓰고 분리해?

URL 조각(`/api/admin`, `orders/{id}/receipt-print`)이 여러 Api 파일에서 겹쳐 쓰일 수 있어서다.
오늘 추가한 두 줄:

```js
printReceipt: (orderId) => `${API_BASE_PATH}/orders/${orderId}/receipt-print`,
deviceEvents: `${API_BASE_PATH}/device-events`,
```

`API_BASE_PATH`가 나중에 바뀌어도(예: `/api/admin` → `/api/v2/admin`) 이 파일 하나만 고치면
`ordersApi.js`를 포함한 모든 Api 파일이 같이 바뀐다.

### Q. Page(`OrderManagePage.jsx`)에서 왜 직접 `printReceipt(order)`를 호출하면 안 됐어?

원래 코드가 `onConfirm` 콜백 **안**에서 `usePrintReceiptQuery(order)`를 함수처럼 호출했다. 이게
왜 안 되냐면:

- React Hook은 **컴포넌트가 렌더링될 때마다 항상 같은 순서로, 최상위에서만** 불러야 한다는 규칙이
  있다("Rules of Hooks"). 조건문/콜백/반복문 안에서 부르면 React가 이전 상태와 새 상태를 연결하지
  못해서 오작동하거나 에러가 난다.
- 그래서 `usePrintReceiptQuery()`는 컴포넌트 최상위(`OrderManagePage` 함수 몸통 맨 위)에서 딱 한 번
  부르고, 그 결과로 받은 `printReceipt`라는 **일반 함수**를 콜백 안에서 쓴다. Hook 자체와 Hook이
  반환한 함수는 다른 것이다.

### Q. 왜 `printReceipt(order)`를 부른 직후에 바로 "완료됐다"고 못 알려줘?

`printReceipt`는 서버에 "출력해줘" 요청만 보내고 바로 끝난다(응답은 `PENDING` 상태). 실제 RTOS가
영수증을 다 찍는 데는 몇 초가 걸리고, 그 결과는 **나중에 따로** 1초마다 폴링해서 알아내야 한다.
그래서 `onConfirm` 안에서 결과를 바로 못 받고, 대신 `printStatus`라는 상태값을 Hook이 계속
갱신해주고, Page는 별도 `useEffect`로 그 값의 변화를 지켜본다:

```js
useEffect(() => {
  if (printStatus === "completed") { /* 토스트 성공 */ }
  else if (printStatus === "failed") { /* 토스트 실패 */ }
}, [printStatus]);
```

"버튼 클릭 → 즉시 결과"가 아니라 "버튼 클릭 → 상태가 시간이 지나며 바뀜 → 그 변화를 지켜본다"는
비동기 폴링 패턴이라서 이런 구조가 된다.

## 4. 파일 배치 규칙 요약표

| 계층 | 이 프로젝트 위치 | 판별법 | 오늘 예시 |
| --- | --- | --- | --- |
| Page | `src/pages/admin/*.jsx` | 라우트 하나 = 파일 하나. `useState`로 화면 상태를 들고 있음 | `OrderManagePage.jsx` |
| Hook | `src/hooks/use*.js` | 이름이 `use`로 시작. 내부에 `useState`/`useEffect` 있음 | `usePrintReceiptQuery.js` |
| Api | `src/api/*Api.js` | `apiClient.get/post/patch` 호출만 있음. React 없음 | `ordersApi.js` |
| Constants | `src/constants/*.js` | 함수 없이 값·URL 조합만 | `constants/api.js` |
| Util | `src/utils/*.js` | 상태 없는 순수 함수. 입력→출력만 | `receiptFormat.js`, `ttsMessages.js` |

## 5. 직접 해볼 것

1. `usePrintReceiptQuery.js`를 열어서 `useState`가 몇 개 있는지 세어보고, 각각 뭘 기억하는 상태인지
   한 줄씩 적어본다.
2. `ordersApi.printReceipt`에서 `apiClient.post(...)`를 지우고 그 자리에 `fetch(...)`를 직접 넣으면
   어떤 파일들을 고쳐야 하는지 상상해본다 (Api 계층이 없다면 몇 곳을 고쳐야 했을지).
3. `buildReceiptText(order)`를 콘솔에서 `order` 객체 하나 만들어서 직접 호출해보고, React 없이도
   동작하는지 확인한다 (Util의 정의를 몸으로 확인).
4. `printStatus`가 `"pending"`, `"processing"`일 때 화면에서 "완료"라고 잘못 표시되면 안 되는 이유를
   자기 말로 설명해본다.

## 6. 다음에 읽을 파일

1. `ASAK-Admin/src/api/apiClient.js` — Api 계층 아래에서 실제로 envelope(`success/data`)를 해제하는 곳.
2. `ASAK-Admin/src/hooks/useOrdersQuery.js` — `usePrintReceiptQuery`보다 먼저 만들어진, 같은 패턴의
   더 단순한 Hook (폴링 없이 조회만).
3. `ASAK-back/.../AdminDeviceEventController.java` — Api가 호출하는 URL이 백엔드에서 실제로 어떻게
   처리되는지, 왜 `data.eventId`를 이렇게 감싸서 응답하는지.
