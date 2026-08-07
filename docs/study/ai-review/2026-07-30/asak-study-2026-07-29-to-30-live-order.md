# 7월 29~30일 Live 주문·상태 변경 학습 기록

- 날짜: 2026-07-29 ~ 2026-07-30
- 학습 대상: ASAK-Admin / ASAK-back / ASAK-Kiosk
- 기준: 실제 Git 커밋, 현재 코드, Screen Bible, Figma 0718 기준 문서
- 목적: “무슨 파일을 바꿨는지”가 아니라 **주문이 화면에 보이고 상태가 바뀌기까지 데이터가 어떻게 흐르는지** 이해한다.

> 이 문서는 공부용 설명이다. 소스 코드·API 계약·DB를 수정하지 않는다.
> 실제 API, DB, 브라우저 동작은 코드 존재와 별도로 검증해야 한다.

---

## 0. 이번 이틀 작업에서 배울 것

| 순서 | 주제 | 한 줄 설명 |
|---|---|---|
| 1 | Live 주문 조회 | 관리자 화면이 진행 중 주문을 받아 카드로 표시하는 흐름 |
| 2 | 화면 상태 | Loading·Empty·Error를 주문 카드와 분리하는 이유 |
| 3 | 주문 행동 | 준비중/완료/취소 버튼이 프론트와 backend를 어떻게 지나가는지 |
| 4 | DB 상태 | `PREPARING`, `COMPLETED`, `CANCELED`가 DB에 어떻게 저장되는지 |
| 5 | mock 경계 | 메뉴 옵션·Kiosk 카테고리는 왜 아직 mock 계약으로 읽어야 하는지 |
| 6 | 취소와 환불 | 주문 상태와 결제 상태를 같은 값으로 섞으면 안 되는 이유 |
| 7 | Figma 토큰 | CSS 값을 무조건 통일하지 않고 역할까지 보는 이유 |
| 8 | 검증 | lint/build가 통과해도 API 완료가 아닌 이유 |

---

## 1. 한 줄 결론

7월 29일에는 관리자 Live 주문 보드가 `/api/admin/orders/live` 조회 결과를 화면에 표시하도록 연결했고, 7월 30일에는 주문 상태 변경·취소 요청을 frontend와 backend에 추가했다. 하지만 실제 HTTP·DB·브라우저 검증은 끝나지 않았고, backend 전체 컴파일도 다른 주문 생성 코드의 오류로 실패한 상태다.

---

## 2. 날짜별로 무엇을 했나

| 날짜 | 저장소 | 작업 | 코드에서 확인한 결과 | 미검증 범위 |
|---|---|---|---|---|
| 7/29 | ASAK-back | 활성 주문 조회 명칭을 Live 주문 조회로 정리 | Bruno 요청과 `/live` 조회 흐름 변경 | 실제 DB 결과, Bruno 호출 |
| 7/29 | ASAK-Admin | Live 주문 보드 조회 연결 | `ordersApi.listLiveOrders()`와 `LiveOrderPreview` 연결 | 실제 API 응답, 브라우저 상태 |
| 7/29 | ASAK-Admin | 옵션 그룹 카탈로그 | mock 메뉴의 옵션 그룹을 `groupId`별로 중복 제거 | 실제 메뉴 API 저장 |
| 7/29 | ASAK-Kiosk | 카테고리 mock 계약명 통일 | `categoryId`, `categoryName`을 탭 컴포넌트와 맞춤 | 실제 Kiosk API |
| 7/30 | ASAK | Figma 0718·취소/환불 정책 문서 정리 | 화면 기준 파일과 도메인 용어 정리 | 정책의 실제 DB 반영 |
| 7/30 | ASAK-Admin | Live 주문 카드·상태 변경·취소 UI | 조회 상태, 확인 다이얼로그, 요청 함수 추가 | 버튼 클릭 후 HTTP 결과 |
| 7/30 | ASAK-back | 상태 변경·취소 Controller/Mapper | PATCH mapping과 `orders` update SQL 추가 | 전체 컴파일, Spring context, DB transaction |
| 7/30 | ASAK-Kiosk | Figma 토큰·간격 정리 | 값·역할이 맞는 CSS token 적용 | 화면별 시각 QA, Variable 바인딩 |

---

## 3. 전체 그림: Live 주문은 어디를 지나가나

```text
브라우저 관리자 화면
  → OrderListPage.jsx
    → LiveOrderPreview.jsx
      → ordersApi.js
        → /api/admin/orders/live
          → AdminOrderController.java
            → AdminOrderService.java
              → AdminOrderMapper.java
                → AdminOrderMapper.xml
                  → orders 등 DB 조회
                    → 응답 DTO
                      → LiveOrderPreview의 orders 상태
                        → OrderCard 목록
```

각 계층은 역할이 다르다.

| 계층 | 파일 예시 | 하는 일 | 하면 안 되는 일 |
|---|---|---|---|
| Page | `OrderListPage.jsx` | URL에 맞는 화면 조각을 조립 | DB SQL 작성 |
| Component | `LiveOrderPreview.jsx`, `OrderCard` | 카드 표시, 버튼 클릭, 화면 상태 렌더링 | Mapper XML 직접 호출 |
| API 모듈 | `ordersApi.js` | URL과 HTTP method를 한 곳에 모음 | JSX 작성 |
| Controller | `AdminOrderController.java` | HTTP 요청을 받아 Service 호출 | SQL 문자열 직접 작성 |
| Service | `AdminOrderService.java` | 상태 전이 규칙과 데이터 변환 | 화면 표시 결정 |
| Mapper/XML | `AdminOrderMapper.java`, XML | DB 조회·수정 | 사용자 버튼 처리 |

이렇게 나누면 “화면이 이상하다”와 “DB가 안 바뀐다”를 다른 위치에서 찾을 수 있다.

---

## 4. 7월 29일: Live 주문 조회 흐름

### 4-1. 프론트 요청 시작점

파일: `ASAK-Admin/src/api/ordersApi.js`

```js
listLiveOrders: () => apiClient.get("/admin/orders/live")
```

`ordersApi`는 화면이 URL 문자열을 여기저기 직접 쓰지 않게 해 준다. Live 주문 URL을 바꿔야 하면 우선 이 파일을 확인한다.

### 4-2. 화면 상태를 나누는 이유

파일: `ASAK-Admin/src/components/admin/LiveOrderPreview.jsx`

`refresh()`는 Live 주문을 요청한 뒤 결과에 따라 화면 상태를 바꾼다.

```text
요청 시작             → loading
요청 성공 + 주문 있음  → ready
요청 성공 + 주문 없음  → empty
요청 실패             → error
```

`empty`와 `error`를 분리하는 이유는 사용자에게 주는 의미가 다르기 때문이다.

| 상태 | 사용자에게 보이는 의미 | 재시도 버튼이 필요한가 |
|---|---|---|
| `empty` | “지금 들어온 주문이 없습니다” | 보통 필요 없음 |
| `error` | “주문을 불러오지 못했습니다” | 필요함 |

### 4-3. Figma와 React 상태 연결

SCR-009의 Figma 0718 기준은 아래와 같다.

| Figma 상태 | Node | 코드에서 대응해야 할 상태 |
|---|---|---|
| Default | `134:10607` | `ready` + 주문 카드 있음 |
| Loading | `134:11447` | `loading` |
| Empty | `134:11452` | `empty` |
| Error | `134:11468` | `error` |

코드에는 `AdminAsyncState`가 있어 카드가 없을 때 Loading·Empty·Error 공통 UI를 표시한다. 하지만 실제 브라우저로 Figma와 대조한 검증은 아직 하지 않았다.

### 4-4. 카드 데이터는 무엇을 쓰나

`OrderCard`는 Live 주문의 `orderId`, 주문 상태, 생성 시각, `menus[]` 같은 표시용 데이터를 사용한다.

여기서 주의할 점은 일반 주문 목록/상세의 `items[]`, `optionItems[]`와 Live 카드의 `menus[]`를 억지로 하나로 합치면 안 된다는 것이다. 두 화면은 목적이 다르다.

- 주문 관리 화면: 상세 확인·필터·금액 근거가 중요하다.
- Live 주문 보드: 조리 중인 주문을 빠르게 처리하는 것이 중요하다.

---

## 5. 7월 30일: 상태 변경과 취소 흐름

### 5-1. 카드 버튼을 누르면

```text
OrderCard 버튼 클릭
  → handleOrder(orderId, status)
  → 취소면 AdminConfirmDialog 열기
  → 확인 후 runOrderAction(orderId, status)
  → ordersApi 호출
  → 성공 toast
  → refresh({ showLoading: false })
  → 최신 주문 목록 다시 표시
```

취소는 파괴적 행동이므로 바로 처리하지 않고 확인 다이얼로그를 거친다. 이것은 SCR-009의 “destructive action은 확인 단계를 둔다”는 규칙과 연결된다.

### 5-2. 현재 코드의 HTTP 경로

```text
GET   /api/admin/orders/live
PATCH /api/admin/orders/{orderId}/{status}
PATCH /api/admin/orders/{orderId}/cancel
```

`status`에는 현재 `PREPARING`, `COMPLETED`가 들어가도록 작성돼 있다.

### 5-3. backend에서는 무엇을 하나

파일: `ASAK-back/src/main/java/com/asak/admin/controller/AdminOrderController.java`

1. Controller가 URL에서 `orderId`, `status`를 받는다.
2. 먼저 주문 상세를 조회한다.
3. 이미 `COMPLETED` 또는 `CANCELED`이면 거부한다.
4. Service에 상태 변경 또는 취소를 맡긴다.
5. 성공/실패를 `ApiResponse`로 돌려준다.

파일: `ASAK-back/src/main/java/com/asak/admin/service/AdminOrderService.java`

```text
PREPARING → statusId 12
COMPLETED → statusId 13
그 외 값   → 0 반환 = 유효하지 않은 상태 전이
```

파일: `ASAK-back/src/main/resources/mappers/AdminOrderMapper.xml`

```sql
UPDATE orders
SET status_id = #{statusId}
WHERE id = #{orderId};
```

취소 SQL은 주문 상태 ID를 `43`으로 바꾸고 `canceled_at = NOW()`를 기록한다.

### 5-4. 코드와 문서가 다른 부분

Screen Bible은 상태 변경 경로를 다음처럼 적고 있다.

```text
PATCH /api/admin/orders/{orderId}/status
```

하지만 현재 frontend와 Controller는 `/{orderId}/{status}`를 사용한다. 프론트와 백엔드는 서로 맞춰져 있어도 문서·Bruno·다른 소비자가 문서를 따를 수 있으므로, 팀이 정본 경로를 하나로 정해야 한다.

---

## 6. 취소와 환불을 한국어로 이해하기

영문 정책 문서를 그대로 외우기보다, 먼저 상태가 어디에 남는지 구분한다.

| 구분 | 언제 쓰나 | 주문 상태 | 결제 상태 | 시각 |
|---|---|---|---|---|
| 취소 | 상품 전달 전 (`RECEIVED`, `PREPARING`) | `CANCELED` | 승인된 결제면 `REFUNDED`가 되어야 함 | `canceled_at`, `refunded_at` |
| 완료 후 환불 | 상품 전달 후 (`COMPLETED`) | `COMPLETED` 유지 | `REFUNDED` | `refunded_at` |

### 왜 둘을 구분해야 하나

- 취소는 “주문 이행을 중단”한다.
- 완료 후 환불은 “상품 제공 이력은 남기고 결제만 되돌린다.”
- 그래서 완료 후 환불에 `OrderStatus.REFUNDED`를 추가하면 주문 이행 상태와 결제 상태가 섞인다.

### 현재 코드와 정책의 차이

현재 취소 SQL은 `orders.status_id`와 `canceled_at`만 갱신한다. 승인 결제의 `payment.status = REFUNDED`, `payment.refunded_at` 갱신은 이 코드에서 확인되지 않는다.

따라서 “취소 버튼이 있다”와 “취소·환불 정책이 DB까지 완성됐다”는 서로 다른 말이다.

---

## 7. mock을 공부하는 두 작업

### 7-1. 메뉴 옵션 그룹 카탈로그

파일: `ASAK-Admin/src/hooks/useMenusQuery.js`

```text
menus
  → menu.detail.optionGroups
  → Map(groupId)
  → optionGroupCatalog
```

`getOptionGroupCatalog(menus)`는 같은 `groupId`가 여러 메뉴에 있어도 첫 그룹만 남긴다.

이 값은 `menus`에서 바로 계산할 수 있다. 그래서 별도 `useState`에 중복 저장하지 않는다. 이미 있는 데이터를 두 군데에 저장하면 한쪽만 바뀌는 버그가 생길 수 있다.

현재 메뉴 데이터는 mock repository가 제공하는 값이다. 옵션 그룹을 화면에서 재사용할 수 있다는 것까지는 확인됐지만, 실제 메뉴 저장 API가 완성됐다는 뜻은 아니다.

### 7-2. Kiosk 카테고리 계약

파일: `ASAK-Kiosk/src/components/kiosk/CategoryTabs.jsx`

```text
categoryId    → React key, 선택 비교, 클릭 시 전달
categoryName  → 탭에 표시하는 문구
```

파일: `ASAK-Kiosk/public/mocks/kiosk.json`

Kiosk mock도 같은 `categoryId`, `categoryName`을 사용하도록 정리됐다. 이는 Component와 JSON의 필드 약속을 맞춘 작업이다.

---

## 8. Figma 토큰과 간격을 왜 보수적으로 바꿨나

Kiosk CSS 토큰은 “색이 비슷해 보인다”는 이유만으로 바꾸지 않았다.

1. CSS 값과 Figma Variable 값이 정확히 같은지 확인한다.
2. 텍스트·배경·오류처럼 역할도 같은지 확인한다.
3. 둘 중 하나라도 불확실하면 기존 값을 보존하고 문서에 남긴다.

예를 들어 Admin 전용 텍스트 토큰이 Kiosk 모달에 연결된 경우, 값이 비슷해도 자동 치환하면 고대비 상태에서 의미가 달라질 수 있다.

확정하지 못한 값은 `ASAK-Kiosk/docs/figma-unbound-colors-2026-07-30.md`에 기록돼 있다.

---

## 9. 검증 결과를 올바르게 읽기

| 확인 항목 | 결과 | 이 결과만으로 말할 수 없는 것 |
|---|---|---|
| Admin lint | 오류 0건, 경고 3건 | 실제 버튼 클릭·HTTP 성공 |
| Admin build | Vite build 성공 | API 응답과 DB update 성공 |
| Kiosk build | Vite build 성공 | Figma 화면 픽셀 일치 |
| Backend compileJava | 실패 | Live 주문 액션만 단독으로 정상이라는 증명 |

backend `compileJava`는 `UserOrderService`의 누락 DTO·Mapper 메서드·ErrorCode 등 18개 오류로 실패했다. 이 파일들은 이번 Live 주문 액션 커밋의 변경 파일이 아니다. 그래도 전체 프로젝트가 컴파일되지 않으므로 Spring context나 실제 API 테스트는 진행할 수 없다.

---

## 10. 직접 해볼 복습 순서

1. `ordersApi.js`에서 GET 1개, PATCH 2개의 URL을 적어 본다.
2. `LiveOrderPreview.jsx`의 `refresh()`를 읽고 `loading`, `empty`, `error` 조건을 말로 설명한다.
3. `AdminConfirmDialog`가 왜 취소에만 먼저 필요한지 설명한다.
4. `AdminOrderController.java`의 두 `@PatchMapping`을 찾아 프론트 URL과 비교한다.
5. `AdminOrderService.java`에서 문자열 상태가 숫자 상태 ID가 되는 이유를 설명한다.
6. `AdminOrderMapper.xml`에서 취소 SQL에 `payment` update가 있는지 확인한다.
7. `useMenusQuery.js`에서 `Map(groupId)`를 지우면 어떤 중복이 생길지 생각한다.

## 11. 연습문제

1. Live 조회가 성공했지만 `content[]`가 비어 있으면 어떤 화면을 보여야 하는가?
   - 정답: `empty`. 네트워크 오류가 아니므로 `error`가 아니다.

2. 상태 변경 뒤에 바로 화면을 새로고침하지 않고 `refresh({ showLoading: false })`를 호출하는 이유는 무엇인가?
   - 정답 확인 위치: `LiveOrderPreview.jsx`. 기존 카드 전체를 loading으로 깜빡이지 않게 하면서 최신 목록을 다시 읽으려는 의도다.

3. 취소와 완료 후 환불 중 주문 상태가 `COMPLETED`로 남는 것은 어느 쪽인가?
   - 정답: 완료 후 환불.

4. 현재 코드의 상태 변경 URL과 Screen Bible의 상태 변경 URL은 같은가?
   - 정답: 다르다. 코드는 `/{orderId}/{status}`, 문서는 `/{orderId}/status`다.

5. `optionGroupCatalog`을 별도 상태로 저장하지 않는 이유는 무엇인가?
   - 정답: `menus`에서 계산할 수 있는 파생값이어서, 이중 상태를 만들 필요가 없기 때문이다.

---

## 12. 다음에 읽을 파일 3개

1. `ASAK-Admin/src/components/admin/LiveOrderPreview.jsx`
2. `ASAK-Admin/src/api/ordersApi.js`
3. `ASAK-back/src/main/java/com/asak/admin/controller/AdminOrderController.java`

스스로 설명해 볼 질문: “주문 카드에서 취소 버튼을 누른 뒤, 어떤 컴포넌트·API 모듈·Controller·SQL을 지나 화면이 다시 갱신되는가?”
