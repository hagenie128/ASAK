# 2026-07-14 피드백 반영 기준

이 문서는 API, 화면 식별자, 프론트 상태 경계의 단일 기준이다. 구현·Figma·DevCopilot 문서를 수정할 때 이 규약을 우선 적용한다.

## 1. API 계약

- 모든 공개 서비스 API의 base path는 **`/api`** 다. 예: `GET /api/menus`. 제공된 `.../api/mcp/mcp?...` 주소는 DevCopilot **MCP 연결 주소**이며 서비스 API base path가 아니다.
- 요청·응답 JSON 필드명은 **camelCase** 다. 예: `menuId`, `orderType`, `paymentStatus`, `createdAt`.
- DB 테이블·컬럼은 기존 **snake_case** 를 유지한다. DB 명칭을 API DTO에 노출하지 않는다.
- 응답은 항상 `{ success, status, code, message, data }` envelope를 사용한다. 업무 payload는 `data`에만 둔다.
- 백엔드 구현과 Mock은 `/api/*`에 맞춘다.

## 2. 화면 식별자 정본

| ID | 정식 화면명 | 처리 |
| --- | --- | --- |
| SCR-001 | 키오스크 홈 (매장·포장) | 주문 유형을 한 화면에서 선택 |
| SCR-002 | 먹고가기 / 포장 선택 | SCR-001에 병합, 독립 화면 없음 |
| SCR-005 | 장바구니·주문확인 | SCR-006에 있던 최종 확인을 ConfirmDialog로 병합 |
| SCR-006 | 주문 확인 | SCR-005에 병합, 독립 화면 없음 |
| SCR-007 | 결제 | 결제 진행·대기 화면 |
| SCR-008 | 주문 완료 | 승인된 결제의 주문번호 표시 |
| SCR-012 | 결제 실패 / 재시도 | SCR-007 위의 팝업·토스트 오버레이, 독립 라우트 없음 |
| SCR-013 | 타임아웃 안내 / 자동 초기화 | 초기화 전 안내 및 확정 액션 |
| SCR-015 | 관리자 로그인 | 관리자 화면, SCR-001이 아님 |

DevCopilot에서 `SCR-001=로그인`처럼 이 표와 다른 레코드를 발견하면 위 매핑으로 제목·구분·설명·관련 화면을 수정한다. 병합 화면(SCR-002, SCR-006)은 삭제하지 않고 `병합됨` 상태와 대상 SCR을 유지해 기존 링크를 보존한다.

## 3. 전역 상태 경계

전역 Zustand state는 고객의 **주문 세션 하나**만 둔다.

```text
orderSession
  orderType
  items (메뉴·옵션·수량·제외 재료)
  order (생성된 주문 정보)
  payment / paymentError
```

메뉴 목록·카테고리·메뉴 상세·관리자 주문 목록·매출·결제수단은 서버 데이터다. 각 페이지/API 훅에서 조회·로딩·오류를 관리하며 주문 세션 store에 저장하지 않는다.

## 4. 세션 초기화 단일 정책

`resetOrderSession(reason)`만 활성 주문 세션을 비울 수 있다.

| 이벤트 | 세션 처리 |
| --- | --- |
| 결제 실패 (`FAILED` 또는 오류 응답) | 장바구니, 선택 옵션, `orderType`, 생성 주문을 유지하고 `paymentError`만 저장 |
| 결제 성공 (`APPROVED`) | 주문 완료 표시용 결과를 별도 보존한 뒤 활성 주문 세션 초기화 |
| 타임아웃 감지 | 즉시 초기화하지 않고 안내(SCR-013)를 표시 |
| 타임아웃 확정 | `TIMEOUT_CONFIRMED`로 활성 주문 세션 초기화 |
| 고객이 타임아웃 안내에서 계속하기 선택 | 세션 유지, 타이머 재시작 |

프론트 구현은 `src/store/orderSessionStore.js`의 `handlePaymentResult`, `confirmTimeout`, `resetOrderSession`을 사용한다. 각 페이지에서 장바구니를 직접 비우지 않는다.

## 5. DevCopilot 동기화 체크

1. 화면 DB의 SCR-001~021을 이 문서의 식별자와 대조한다.
2. API DB의 URL을 `/api`로, request/response property를 camelCase로 맞춘다. MCP 연결 URL은 API DB에 기록하지 않는다.
3. SCR-002·SCR-006은 `병합됨`, SCR-012는 `오버레이`로 표시한다.
4. 화면 설계, 사용자 시나리오, QA의 관련 화면/API 링크를 다시 생성하거나 검증한다.
5. 동기화 후 화면 DB export를 `asak-data/scripts/screens_notion_snapshot.json`으로 갱신하고, 로컬 문서와 diff를 검토한다.
