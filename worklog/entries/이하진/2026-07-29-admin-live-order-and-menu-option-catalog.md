# 2026-07-29 관리자 Live 주문 보드 및 메뉴 옵션 카탈로그 기록

> 일일 기록: [2026-07-29.md](../../daily/이하진/2026-07-29.md)
> 기준 화면: [SCR-009 Admin Live Order Board](../../../docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-009-ADMIN-LIVE-ORDER-BOARD.md) · Figma 0718 Default `134:10607`, Loading `134:11447`, Empty `134:11452`, Error `134:11468` · [SCR-016 Admin Menu Management](../../../docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-016-ADMIN-MENU-MANAGEMENT.md) · Figma 0718 Detail Edit `134:12668`

---

## 1. 기본 정보

- 작업 일자: 2026-07-29
- 담당자: 이하진 (`hagenie128` Git 사용자 매핑 기준)
- 저장소: ASAK-back / ASAK-Admin
- 반영 이력: `952555a`(Live 주문 조회 API 통일), `96c88de`(Live 주문 보드 조회 연결), `b3fd9f0`(메뉴 옵션 그룹 추천 카탈로그 추가)
- 관련 화면/계약: SCR-009 `GET /api/admin/orders/live`, SCR-016 메뉴 옵션 그룹 카탈로그
- 작업 유형: `feature`
- 완료 판정: 코드 변경 커밋은 확인했다. Spring 기동, Bruno 실호출, 실제 API 응답, 브라우저와 Figma 상태 대조는 수행하지 않았으므로 화면·API 통합 완료로 판정하지 않는다.

## 2. 작업 목적

- Live 주문 보드가 목록용 활성 주문 계약이 아닌, 메뉴·옵션·경과시간을 포함하는 전용 Live 조회 계약을 사용하도록 연결한다.
- 메뉴 편집에 필요한 옵션 그룹을 메뉴별 상세 데이터에서 ID 기준으로 한 번씩만 추출해 재사용 가능한 목록으로 만든다.

## 3. 화면·상태·재사용 범위

| 구분 | 기준 | 이 날짜의 범위 | 남은 확인 |
|---|---|---|---|
| SCR-009 Live 주문 보드 | Default `134:10607`, Loading `134:11447`, Empty `134:11452`, Error `134:11468` | Live 조회 경로와 카드 목록 데이터 연결 | 각 화면 상태 렌더링, polling, 접근성, 주문 액션 |
| SCR-016 메뉴 관리 | Detail Edit `134:12668`, Saving `241:17178`, Error `241:17719` | 목업 메뉴 상세의 옵션 그룹 카탈로그 추출 | 실제 메뉴 API, 저장, validation, 오류 상태 |

재사용한 기존 구성요소는 `ordersApi`, `LiveOrderPreview`, `AdminAsyncState`, `AdminConfirmDialog`, `AdminSidebar`, `useMenusQuery`다. 이 날짜에는 새 UI 컴포넌트나 Screen Bible을 수정하지 않았다.

## 4. 직접 구현 영역

### ASAK-back

- Bruno 요청 파일을 `01-active-orders.bru`에서 `01-live-orders.bru`로 변경했다.
- `AdminOrderController`, `AdminOrderService`에서 Live 주문 조회 경로의 응답 처리를 정리했다.
- `AdminOrderMapper`와 `AdminOrderMapper.xml`에서 목록 DTO 전환 과정에 남아 있던 관련 선언을 제거했다.

### ASAK-Admin

- `ordersApi.listActiveOrders()`를 `ordersApi.listLiveOrders()`로 바꾸고 `GET /api/admin/orders/live`를 호출하게 했다.
- `LiveOrderPreview`가 목업 저장소의 Live 조회 대신 `ordersApi.listLiveOrders()`의 `content` 배열을 사용해 ready/empty/error 상태를 정하도록 변경했다.
- 메뉴 카드에서 `base` 값이 있는 경우에만 베이스 행을 표시하고, 옵션 행 key에 index를 추가해 중복 key 가능성을 줄였다.
- `useMenusQuery`의 옵션 그룹 중복 제거 로직을 `getOptionGroupCatalog(menus)` 순수 함수로 분리했다. 이 함수는 각 메뉴의 `detail.optionGroups`를 순회해 `groupId`별 첫 그룹만 반환한다.

## 5. 구현 로직 / 적용한 방식

### Live 주문 조회 흐름

1. `LiveOrderPreview`가 마운트될 때 `refresh()`를 호출한다.
2. `ordersApi.listLiveOrders()`가 `/admin/orders/live`를 요청한다.
3. 성공 응답의 `content`를 주문 카드 목록으로 저장하고, 길이가 0이면 empty, 아니면 ready 상태로 설정한다.
4. 요청 실패는 주문 목록을 비우고 error 상태로 설정한다.

이 흐름은 코드와 커밋 diff로 확인한 정적 근거다. 실제 `ApiResponse` envelope의 unwrap 결과와 `content[]` 데이터 형식은 네트워크 호출로 검증하지 않았다.

### 옵션 그룹 카탈로그 흐름

1. `useMenusQuery`가 목업 메뉴 목록을 `menus` 상태로 가진다.
2. `getOptionGroupCatalog(menus)`가 메뉴별 `detail.optionGroups`를 읽는다.
3. `Map`의 key를 `groupId`로 사용해 같은 옵션 그룹을 한 번만 보관한다.
4. 반환 배열은 메뉴 수정 화면에서 선택 가능한 옵션 그룹 목록의 기반으로 사용한다.

## 6. AI 도움 영역

- 사용한 AI 도구: Codex
- 요청 범위: 실제 Git 이력·변경 파일·Screen Bible을 대조하고 일일/상세 작업 로그 초안을 작성하는 보조.
- AI가 제공한 내용: 완료와 미검증 범위 분리, 화면 상태 및 Figma Node 근거 정리, API·UI·목업 경계 기록.
- 사람이 결정·확인한 부분: 실제 구현 내용, 커밋 반영, 작업 범위와 후속 우선순위.
- AI가 직접 구현하거나 변경한 범위: 소스코드 변경 없음. 이 기록 문서 작성만 수행.

## 7. 발생 이슈 및 미완료 상태

### 이슈 1 — Live 주문 액션 계약 미연결

- 증상: `LiveOrderPreview`에는 완료·취소 액션의 TODO가 남아 있으나 `ordersApi`에 대응 메서드와 백엔드 URL/HTTP 메서드가 확정되어 있지 않다.
- 영향: Live 주문 조회가 되더라도 주문 상태 변경을 완료 기능으로 볼 수 없다.
- 필요한 해결: 상태 변경 API 계약, 확인 단계, 성공 후 TTS, 중복 클릭 방지와 실패 시 이전 상태 유지 기준을 확정한다.

### 이슈 2 — 가로 이동 동작 검증 필요

- 증상: 이전/다음 화살표의 가로 스크롤 구현이 TODO 단계이며, 다음 버튼 비활성 조건은 실제 페이지 객체가 아닌 배열을 기준으로 작성돼 있다.
- 영향: 주문이 여러 장일 때 이동 UX가 화면 요구와 다를 수 있다.
- 필요한 해결: 보드 ref와 카드 폭 기준의 scroll 동작을 팀원이 구현하고, 키보드·터치·빈 목록 상태를 브라우저에서 확인한다.

### 이슈 3 — 실제 API 및 Figma 상태 미검증

- 증상: 이 기록에서 확인한 근거는 Git 커밋과 코드 diff다.
- 영향: `/live` 응답의 실제 필드, loading/empty/error 렌더링, stale response 방지, 접근성 요구 충족 여부를 보장할 수 없다.
- 필요한 해결: Spring context와 Bruno로 응답을 확인한 후 SCR-009의 네 상태를 Figma 정본과 대조한다.

### 이슈 4 — 옵션 카탈로그의 데이터 원천

- 증상: `getOptionGroupCatalog`는 현재 목업 메뉴의 `detail.optionGroups`에서 파생한다.
- 영향: 실제 메뉴 관리 API가 다른 `groupId` 중복·누락 규칙을 가지면 카탈로그가 달라질 수 있다.
- 필요한 해결: SCR-016의 실제 메뉴 조회/저장 계약에서 옵션 그룹 식별자와 정렬 정책을 확정하고 default/detailEdit/saving/error를 검증한다.

## 8. 디버깅 기록

- 7월 29일 커밋과 7월 30일 현재 작업 트리는 구분해 확인했다. 현재 미커밋 변경은 이 날짜의 완료 증거에 포함하지 않았다.
- 같은 날짜의 다른 팀원 커밋은 작성자 기준 작업 로그에 포함하지 않았다.
- 이 기록을 위한 빌드·테스트는 실행하지 않았다. 이미 변경된 작업 트리에 영향을 주지 않기 위해 Git 상태와 해당 커밋 diff만 읽기 전용으로 확인했다.

## 9. 이번 작업에서 배운 점

- 목록 API와 실시간 보드 API는 모두 주문을 조회하더라도 화면이 요구하는 데이터가 다를 수 있다. Live 보드가 메뉴·옵션·경과 시간을 요구하면 전용 계약 또는 명확한 adapter가 필요하다.
- Hook의 계산값이 상태를 별도로 가질 필요는 없다. 메뉴 목록에서 파생한 옵션 그룹은 순수 함수로 분리하면 데이터 원천과 중복 제거 기준을 읽기 쉽다.
- API 호출 코드가 추가됐다는 사실만으로 기능 완료가 되지는 않는다. 응답 shape, 오류 상태, 사용자 액션, Figma 상태까지 확인해야 한다.

## 10. 검증 내용

| 구분 | 실행/확인 | 결과 | 검증하지 못한 범위 |
|---|---|---|---|
| Git 이력 | `952555a`, `96c88de`, `b3fd9f0` 커밋의 작성자·변경 파일 대조 | 2026-07-29 이하진 작업 커밋을 확인 | 원격 반영·PR/CI |
| API 경로 | `ordersApi.js`, `LiveOrderPreview.jsx`, backend 변경 파일 대조 | 프론트가 `/api/admin/orders/live` 경로를 사용하도록 변경된 것을 확인 | HTTP 응답·에러·빈 결과 |
| 화면 기준 | SCR-009/SCR-016 Screen Bible 대조 | 요구 상태와 Figma Node를 기록 | Figma 파일의 최신 시각 검증·브라우저 렌더링 |
| 옵션 카탈로그 | `useMenusQuery.js` diff 대조 | `groupId` 기반 중복 제거 함수를 확인 | 실제 API 데이터·정렬·저장 연동 |

## 11. 다음 작업 / 검증 체크리스트

- [ ] Spring context와 Bruno로 `GET /api/admin/orders/live` 정상·빈 결과·오류 응답을 확인한다.
- [ ] SCR-009 Default/Loading/Empty/Error를 Figma 노드 `134:10607`/`134:11447`/`134:11452`/`134:11468`과 브라우저에서 대조한다.
- [ ] 완료·취소 API의 경로·HTTP 메서드·응답 계약을 확정하고, 중복 클릭·실패·TTS 실행 조건을 정한다.
- [ ] Live 보드의 여러 카드에서 가로 스크롤, 키보드 focus, 80×80px 터치 타겟을 확인한다.
- [ ] SCR-016 실제 메뉴 API에서 옵션 그룹 ID·정렬·중복 정책을 확인하고 Detail Edit/Saving/Error를 검증한다.

## 12. 포트폴리오용 요약

- 관리자 Live 주문 보드의 조회를 목업 저장소에서 전용 `/api/admin/orders/live` 계약으로 전환하는 기반을 연결했다. 조회 연결과 주문 상태 변경·화면 검증을 분리해 후속 범위를 명확히 남겼다.
- 메뉴별 상세에 흩어진 옵션 그룹을 `groupId` 기준으로 중복 제거해 메뉴 편집에서 재사용할 카탈로그 기반을 마련했다. 실제 메뉴 API 저장 연동은 별도 검증 과제로 남겼다.

## 13. 첨부 / 참고 자료

- ASAK-back: `api/admin/01-live-orders.bru`, `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.java`, `AdminOrderMapper.xml`
- ASAK-Admin: `src/api/ordersApi.js`, `src/components/admin/LiveOrderPreview.jsx`, `src/hooks/useMenusQuery.js`
- 기준 문서: SCR-009, SCR-016
