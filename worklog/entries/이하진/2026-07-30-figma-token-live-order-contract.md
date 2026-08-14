# 2026-07-30 Figma 토큰 정리 및 Live 주문 계약 기록

> 일일 기록: [2026-07-30.md](../../daily/이하진/2026-07-30.md)
> Figma 정본: [`ASAK — Design System + Product UI 0718`](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/ASAK-%E2%80%94-Design-System---Product-UI-0718?node-id=134-10606) · Admin 캔버스 `134:10606` · Kiosk 캔버스 `134:7720`
> 기준 화면: [SCR-009](../../../docs/product_bible/07_Screen_Bible/SCR-009-ADMIN-LIVE-ORDER-BOARD.md) · [SCR-011](../../../docs/product_bible/07_Screen_Bible/SCR-011-ADMIN-SOLD-OUT-MANAGEMENT.md) · [SCR-016](../../../docs/product_bible/07_Screen_Bible/SCR-016-ADMIN-MENU-MANAGEMENT.md)

---

## 1. 기본 정보

- 작업 일자: 2026-07-30
- 담당자: 이하진 (`hagenie128` Git 사용자 매핑 기준)
- 저장소: ASAK / ASAK-Admin / ASAK-Kiosk
- 반영 이력: `e9786c5`(최신 Figma 기준과 환불 계약 정리), `565cf59`·`2cec7e6`(관리자 Live 주문 UI와 액션 API 수정), `5bd6427`·`00d9f19`(backend 상태 변경·취소 처리), `5932a55`(키오스크 Figma 토큰과 간격 정리)
- 관련 화면/계약: SCR-009 Live 주문 보드, SCR-011 품절 관리, SCR-016 메뉴 관리, Kiosk 공통 UI; `GET /api/admin/orders/live`, 상태 변경/취소/환불 계약
- 작업 유형: `docs` / `feature` / `style`
- 완료 판정: 문서·코드·스타일 커밋, Admin lint/build, Kiosk build는 확인했다. backend 전체 compileJava는 기존 UserOrderService의 누락 심볼 18건으로 실패했다. API/DB 통합, 브라우저 동작, Figma 화면별 픽셀 대조는 미완료다.

## 2. 작업 목적

- 구현 문서와 Figma 원본을 0718 정본 한 곳으로 맞추고, 취소와 완료 후 환불의 상태 의미를 구분한다.
- Admin Live 주문 보드가 조회 결과에 따라 loading/empty/error를 표시하고 상태 변경 UX를 준비하도록 한다.
- Kiosk CSS는 Figma Variable의 값과 역할이 모두 일치할 때만 토큰을 사용하고, 불확실한 디자인 결정은 코드 변경 대신 문서에 남긴다.

## 3. 화면·상태·재사용 범위

| 구분 | Figma/Screen 기준 | 이 날짜의 범위 | 남은 확인 |
|---|---|---|---|
| SCR-009 Live 주문 | Default `134:10607`, Loading `134:11447`, Empty `134:11452`, Error `134:11468` | 조회 상태, 카드 배치, 취소 확인 UI, 공통 토큰 | 실제 상태 변경·취소 API, polling stale response, 브라우저 상태 대조 |
| SCR-011 품절 관리 | Default `39:8577`, Loading `51:13887`, Empty `51:14020`, Error `51:14181`, Save `39:8653` | 화면 CSS/관련 UI 정리 | 저장 API·실데이터 검증 |
| SCR-016 메뉴 관리 | Default `134:12137`, Detail Add `134:12328`, Detail Edit `134:12668`, Saving `241:17178`, Error `241:17719` | 메뉴 편집 패널/스타일 정리 | 메뉴 저장·validation·오류 동작 |
| Kiosk 공통 화면 | 실제 Figma Kiosk 캔버스 `134:7720` | 색·spacing 토큰과 미바인딩 목록 정리 | 각 화면 스크린샷 대조, Variable 재바인딩 |

Figma MCP로 0718 정본의 Admin·Kiosk 캔버스 메타데이터를 읽어 파일·캔버스 접근을 확인했다. 메타데이터는 구조와 프레임 존재 확인 근거이며, 화면별 브라우저 시각 QA 또는 Figma Variable 변경의 근거는 아니다.

## 4. 직접 구현 영역

### ASAK 문서

- 구현 가이드, 상태 체크리스트, Product Bible의 Figma 링크를 0718 파일 `yHhvn5RKjBd91U8BJUQz7F`로 통일했다.
- SCR-009의 조회 계약을 `/active`에서 `/live`로 정리했다.
- 취소는 `RECEIVED`/`PREPARING` 주문의 이행 중단이고, 완료 주문 환불은 주문 상태를 `COMPLETED`로 보존한 채 결제 상태를 `REFUNDED`로 전환하는 별도 동작으로 문서화했다.

### ASAK-Admin

- `ordersApi`에 Live 조회, 상태 변경, 취소 요청 메서드를 추가했다.
- `LiveOrderPreview`에서 Live 목록 조회 결과를 `orders` 상태에 저장하고, 결과 길이에 따라 ready/empty, 실패 시 error로 나누도록 했다.
- 주문 카드의 경과 시간을 갱신하고 카드 높이를 계산해 배치하며, 취소는 `AdminConfirmDialog`에서 확인한 뒤 요청하도록 구성했다.
- `MenuEditPanel`, `SoldOutManagePage`, Admin 공통 스타일과 `tokens.css`를 함께 갱신했다. 이 변경이 메뉴 저장·품절 저장 API를 구현했다는 뜻은 아니다.
- 후속 커밋에서 `cancelOrder`가 `/cancel`을 호출하도록 고쳤고, 상태 변경 인자의 이름을 `status`로 정리했다.

### ASAK-back 후속 반영

- `AdminOrderController`에 `PATCH /api/admin/orders/{orderId}/{status}`와 `PATCH /api/admin/orders/{orderId}/cancel` mapping을 추가했다.
- Service·Mapper·XML에 상태 ID 갱신과 취소 시 `status_id=43`, `canceled_at=NOW()`를 반영하는 update를 추가했다.
- 이 SQL은 결제 상태나 `refunded_at`을 변경하지 않는다. 승인 결제 취소의 환불 처리는 코드·DB 통합 검증 전까지 완료로 기록하지 않는다.

### ASAK-Kiosk

- 공통, 접근성, 홈, 메뉴, 메뉴 상세, 장바구니, 결제, 완료, 영수증 스타일에서 Figma 값과 역할이 일치하는 색·spacing 토큰을 적용했다.
- `docs/figma-unbound-colors-2026-07-30.md`에 Figma Variable 미바인딩 값, 역할 충돌, Kiosk에 없는 Semantic 토큰을 표로 기록했다.

## 5. 구현 로직 / 적용한 방식

### Live 주문 조회와 행동 흐름

1. `LiveOrderPreview`가 마운트될 때 `refresh()`를 호출한다.
2. `ordersApi.listLiveOrders()`가 `GET /api/admin/orders/live`를 요청한다.
3. 반환 데이터의 `content[]`를 카드 목록으로 저장하고, 목록 길이로 ready/empty를 결정한다. 요청 실패는 error 상태로 전환한다.
4. 카드의 상태 변경·취소 클릭은 확인 절차 후 API 요청을 시도하고, 성공 toast 뒤 `refresh({ showLoading: false })`로 목록을 다시 읽도록 구성돼 있다. 현재 frontend와 backend 구현은 `/{orderId}/{status}` 및 `/{orderId}/cancel` 경로에서 서로 맞는다.

이 흐름은 코드·커밋·빌드로 확인한 정적 근거다. HTTP 요청을 실제로 보내 결과를 확인하지 않았으므로, 행동 성공을 완료로 판정하지 않는다.

### Kiosk 토큰 선택 기준

1. 코드의 색 또는 spacing 값이 Figma Variable 값과 정확히 같은지 확인한다.
2. 값이 같더라도 배경·텍스트·상태처럼 역할이 다르면 토큰으로 바꾸지 않는다.
3. Figma Variable이 없거나 Admin 전용 토큰이 연결된 경우에는 원래 값을 유지하고 `Figma 직접값 · Variable 미바인딩` 주석 및 문서 근거를 남긴다.

## 6. AI 도움 영역

- 사용한 AI 도구: Codex, Figma MCP 읽기
- 요청 범위: 실제 Git 이력·코드·문서·Figma 캔버스 메타데이터 대조, 검증 명령 실행, 일일/상세 워크로그 작성.
- AI가 제공한 내용: 구현·정적 검증·미검증 API를 분리한 기록, 상태/환불 계약 대조, API URL 위험과 Figma 토큰 미바인딩 사항의 정리.
- 사람이 결정·확인한 부분: 소스 코드·문서 구현, 커밋 범위, 디자인 토큰 적용 및 도메인 정책.
- AI가 직접 구현하거나 변경한 범위: 소스 코드 및 Git 원격 변경 없음. 이 워크로그 문서만 작성.

## 7. 발생 이슈 및 미완료 상태

### 이슈 1 — 실행 코드와 문서 endpoint의 계약 불일치

- 확인한 코드: 후속 커밋에서 frontend의 취소 URL은 `/cancel`로 수정됐고, backend Controller도 같은 취소 mapping을 제공한다.
- 확인한 코드: 상태 변경 실행 경로는 frontend/backend 모두 `PATCH /api/admin/orders/{orderId}/{status}`다. 하지만 Screen Bible과 구현 가이드는 `PATCH /api/admin/orders/{orderId}/status`를 기준으로 둔다.
- 영향: 현재 프론트와 백엔드는 서로 호출할 수 있는 형태지만, 정본 문서·Bruno·다른 소비자가 다른 경로를 사용할 위험이 있다.
- 필요한 해결: path variable 방식과 `/status` + body 방식 중 하나를 팀이 확정하고 계약 문서·Bruno·Controller·프론트를 함께 정렬한 뒤 정상/실패를 검증한다.

### 이슈 2 — 취소의 결제 환불 처리 및 API·DB 검증 미완료

- 상태 변경·취소 Controller mapping과 주문 상태 SQL은 추가됐지만, 취소 SQL은 결제의 `REFUNDED`·`refunded_at`을 갱신하지 않는다. 완료 주문 환불 endpoint도 이 작업에서 구현·검증되지 않았다.
- 필요한 해결: Controller → Service → Mapper → DB 순서로 결제 갱신과 트랜잭션을 확인하고, `APPROVED → REFUNDED`, `COMPLETED` 유지, 중복 환불 `409`을 실제로 검증한다.

### 이슈 3 — backend 전체 컴파일 차단

- `gradlew.bat -p C:\ASAK-workspace\ASAK-back compileJava --no-daemon`은 `UserOrderService`의 누락 Mapper 메서드·DTO·ErrorCode·생성자/Setter 때문에 18개 오류로 실패했다.
- `UserOrderService.java`와 해당 ErrorCode 이름들은 이번 Admin 액션 커밋의 변경 파일이 아니며, 액션 코드만 성공적으로 컴파일됐는지는 전체 프로젝트 실패로 분리 증명할 수 없다.
- 필요한 해결: Kiosk 주문 생성 영역을 별도 범위로 복구한 뒤 전체 컴파일과 Spring context를 다시 검증한다.

### 이슈 4 — Kiosk Variable 설계 결정 필요

- `Text/Admin/Primary`가 Kiosk 모달에 연결된 사례, Vegan/New 배지 토큰 부재, 비슷한 검정·빨강·테두리 값의 중복이 남아 있다.
- 필요한 해결: Figma에서 Kiosk 전용 Semantic Variable을 바인딩하거나 의도된 예외인지 디자인 담당자가 결정한다. 코드에서 값만 보고 임의 통합하지 않는다.

### 이슈 5 — Figma 노드 정합과 시각 QA

- 실제 0718 캔버스 메타데이터는 읽었지만, Kiosk Screen Bible의 일부 기존 프레임 ID는 최신 캔버스 프레임과 별도로 확인할 필요가 있다.
- 필요한 해결: 화면별 최신 Node를 확정하고, Default/Loading/Empty/Error/Disabled를 브라우저 화면과 대조한다.

## 8. 디버깅 기록

- Admin lint: 후속 액션 API 수정 뒤에도 오류 0건, 미사용 변수 경고 3건. `LiveOrderPreview`의 `readLiveFixture`도 경고 대상이다.
- Admin build: 후속 액션 API 수정 뒤 Vite 프로덕션 빌드 성공. 500kB 초과 번들 경고가 남았다.
- Kiosk build: Vite 프로덕션 빌드 성공. 500kB 초과 번들 경고가 남았다.
- Backend compile: Gradle 배포본 다운로드 제한은 제한 없는 환경에서 해소했으나, `UserOrderService` 누락 심볼 18건으로 compileJava가 실패했다.

## 9. 이번 작업에서 배운 점

- 취소와 환불은 이름이 비슷해도 주문 이행 상태와 결제 상태에 미치는 영향이 다르므로 API·DB·화면에서 분리해야 한다.
- lint/build 성공은 모듈 해석과 번들 생성의 근거이지, 실제 HTTP URL·응답·버튼 동작의 근거는 아니다.
- 디자인 토큰화는 값 일치뿐 아니라 역할·고대비 상태까지 확인해야 한다. 불확실한 값은 통합보다 근거를 남기는 편이 안전하다.

## 10. 검증 내용

| 구분 | 실행/확인 | 결과 | 검증하지 못한 범위 |
|---|---|---|---|
| Git 이력 | `e9786c5`, `565cf59`, `5bd6427`, `00d9f19`, `2cec7e6`, `5932a55`의 작성자·변경 파일·diff 대조 | 7월 30일 이하진 커밋 확인 | 원격 반영·PR/CI |
| Figma | 0718 파일의 Admin `134:10606`, Kiosk `134:7720` 메타데이터 조회 | 캔버스 구조·프레임 존재 확인 | 화면별 최신 Node 확정, 픽셀 비교, Variable 변경 |
| Admin lint | `npm.cmd --prefix C:\ASAK-workspace\ASAK-Admin run lint` | 액션 API 수정 뒤 오류 0건, 경고 3건 | 클릭·네트워크·API 응답 |
| Admin build | `npm.cmd --prefix C:\ASAK-workspace\ASAK-Admin run build` | 액션 API 수정 뒤 성공, 대형 번들 경고 | 브라우저 UI·상태 변경·취소 |
| Backend compile | `gradlew.bat -p C:\ASAK-workspace\ASAK-back compileJava --no-daemon` | UserOrderService 누락 심볼 18건으로 실패 | Admin 액션의 단독 컴파일, Spring context, DB |
| Kiosk build | `npm.cmd --prefix C:\ASAK-workspace\ASAK-Kiosk run build` | 성공, 대형 번들 경고 | 화면별 시각 QA·고대비·Variable 재바인딩 |

## 11. 다음 작업 / 검증 체크리스트

- [ ] `/{status}`와 `/status` + body 중 상태 변경 endpoint 정본을 확정하고 문서·Bruno·Controller·프론트를 통일한다.
- [ ] Kiosk 주문 생성 영역의 18개 compileJava 오류를 별도 범위로 복구하고 backend 전체 컴파일을 재실행한다.
- [ ] Bruno로 Live 조회 정상/빈/오류, 상태 변경, 취소, 완료 주문 환불/중복 환불을 확인한다.
- [ ] SCR-009 Default/Loading/Empty/Error를 실제 브라우저에서 Figma와 대조한다.
- [ ] SCR-011/SCR-016의 저장·오류·disabled 상태를 실제 API/목업 기준으로 확인한다.
- [ ] Kiosk 미바인딩 색, Admin 전용 텍스트, Vegan/New 배지 Semantic Variable을 디자인에서 결정한다.
- [ ] Admin/Kiosk 번들 분할 필요성을 측정하고 기능 안정화 뒤 별도 성능 작업으로 분리한다.

## 12. 포트폴리오용 요약

- 0718 Figma 정본을 구현 문서의 단일 기준으로 연결하고, 취소와 완료 후 환불이 주문·결제 상태에 다르게 반영돼야 함을 계약으로 정리했다.
- 관리자 Live 주문 보드의 조회 상태·카드 배치·확인 UX와 상태 변경·취소 mapping을 커밋 및 Admin 빌드까지 확인했다. 다만 endpoint 정본 통일, 결제 환불 처리, backend 전체 컴파일, Figma 화면별 시각 검증은 별도 단계로 남겼다.

## 13. 첨부 / 참고 자료

- ASAK: `CONTEXT.md`, `docs/implementation_guide/09-figma-state-checklist.md`, `docs/product_bible/04_Dashboard_Sales_Kitchen_TTS/sales/SALES_CANCELLATION_REFUND_RULES.md`, `docs/product_bible/07_Screen_Bible/SCR-009-ADMIN-LIVE-ORDER-BOARD.md`
- ASAK-Admin: `src/api/ordersApi.js`, `src/components/admin/LiveOrderPreview.jsx`, `src/components/admin/MenuEditPanel.jsx`, `src/pages/admin/SoldOutManagePage.jsx`, `src/styles/tokens.css`
- ASAK-Kiosk: `docs/figma-unbound-colors-2026-07-30.md`, `src/styles/tokens.css`, `src/styles/kiosk/*.css`
