# 2026-07-23 API 계약·백엔드 기반 정리

> **일일 기록:** [2026-07-23 daily](../../daily/이하진/2026-07-23.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-23
- 담당자: 이하진
- 저장소: `ASAK` / `ASAK-Admin` / `ASAK-back`
- 브랜치: `main` (ASAK, ASAK-Admin, ASAK-back) · 계약 문서 정리 브랜치 `ai-review/api-contract-alignment-20260723`
- 관련 이슈/PR: API 계약 정리 · SCR-009 Admin Live Order · 키오스크 주문/결제 흐름
- 작업 유형: `docs` / `fix` / `feature`
- Figma 기준: 이번 범위는 API·DB·백엔드 기반 작업이다. 신규 Figma 프레임이나 화면 상태를 추가·변경하지 않았으며, 화면 영향은 SCR-009와 기존 키오스크 주문/결제 화면의 실제 연동 단계에서 확인할 예정이다.

## 2. 작업 목적

- mock 화면과 실제 구현이 다른 규칙을 사용하지 않도록 메뉴·결제 API 계약, 취소·환불 매출 집계 기준, Admin mock 필드를 정리한다.
- Admin 주문 관리/Live Order에 필요한 조회 기반과 API 공통 응답·예외·페이지 응답·헬스체크·업로드 이미지 제공 기반을 마련한다.
- 다음 프론트 실 API adapter 연결 전, 요청·응답의 이름과 상태 의미를 Bruno 컬렉션 및 문서로 확인 가능하게 한다.

## 3. 직접 구현 영역

Git 커밋 이력으로 다음 직접 작업을 확인했다.

- **계약·문서:** 메뉴·결제 API 계약과 취소/환불 매출 규칙을 정리하고, `canonical-contract-decisions`와 주문 아키텍처에 SQL 뷰 기준을 보강했다 (`43dcf96`, `ba4bc8f`).
- **DB 집계:** 취소/환불 주문·결제 상태가 매출 뷰에서 제외되도록 `create_sales_views_mysql.py`를 수정했다 (`a255e24`).
- **API 확인 도구:** Admin 16개·Kiosk 7개 요청을 포함하는 Bruno 컬렉션과 로컬 환경 설정을 추가했다 (`ffb5889`, `0555e31`).
- **백엔드 공통 기반:** `ApiResponse`, `CustomException`, `ErrorCode`, `GlobalExceptionHandler`, `PageResult`, `SecurityConfig`, `HealthController`를 정리했다 (`300c851`, `3333e04`, `da736ab`, `410a897`).
- **도메인/조회 기반:** 주문·결제 상태 enum 정합, 이미지 업로드 및 `/uploads` 정적 제공, Active/Live Order DTO·서비스·매퍼·컨트롤러 흐름을 보강했다 (`b6f7425`, `a4cba77`, `e0221f4`, `5c32687`, `2f71fed`, `d36b88a`).
- **Admin 문서:** mock 데이터와 API 연결 문서에서 `totalAmount`, `CANCELED` 기준을 갱신했다 (`df2cfdb`).

## 4. 구현 로직 / 적용한 방식

- **정본 대조 순서:** 실제 Git 커밋과 현재 코드 → `docs/product_bible`의 API·화면 정본 → 계약/구현 가이드 → Admin mock 문서 순으로 확인했다. Product Bible은 코드 현실과 정책을 구분하며, 충돌 시 코드와 baseline을 우선하도록 안내한다.
- **매출 규칙:** 주문·결제 상태가 취소/환불이면 매출 합계에서 제외해야 한다. 따라서 계약 문서·SQL 뷰·주문 아키텍처를 같은 기준으로 보강했다.
- **API 흐름:** Controller → Service → Mapper → DTO/공통 응답으로 역할을 나누고, 목록 응답은 `PageResult`, 성공/실패 응답은 `ApiResponse`·`ErrorCode`·전역 예외 처리로 통일하는 방향이다.
- **Admin Live Order 흐름:** Controller 요청 → `AdminOrderService.getLiveOrders` → `AdminOrderMapper` 조회 → `ActiveOrderResponse` 및 하위 item/option/excluded-ingredient DTO → 표준 응답 형태로 반환한다.
- **파일 이미지 흐름:** 업로드 유틸이 파일을 저장하고 `WebMvcConfig`가 로컬 uploads 디렉터리를 정적 URL로 제공하도록 구성했다. 배포 환경의 저장소·권한·URL은 별도 검증 대상이다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex
- 어떤 질문/요청을 했는지: 기존 워크로그·Git 이력·Product Bible·현재 문서를 대조하여 오늘의 실제 작업, 영향 화면, 미검증 항목을 빠짐없이 기록하도록 요청했다.
- AI가 도움 준 내용: 커밋 작성자·시각·변경 파일을 대조하고, 기존 daily/entry 템플릿에 맞는 기록 구조와 테스트 체크리스트를 정리했다.
- 그대로 사용한 부분: worklog의 daily 미니 카드, 12섹션 상세 기록, Git/Notion 동기화 대상 표 구조.
- 수정해서 사용한 부분: 구현 코드나 API 계약 내용은 이 워크로그 작성 세션에서 AI가 작성·수정하지 않았다. 기록 문구는 실제 Git 커밋 evidence 기준으로만 작성했다.

## 6. 발생 이슈

### 이슈 1 — 기존 daily의 Backend 블로커 문구가 최신 이력과 불일치

- 증상: 오전 Admin mock 작업 당시의 `Backend business API 없음` 문구가 오후 백엔드 구현 커밋 이후에도 남아 있었다.
- 원인: 화면 mock 작업과 API/백엔드 작업이 시간대와 저장소가 분리되어 기록됐다.
- 해결: daily 상태를 `구현 진행`으로 정정하고, 실 API adapter·통합/회귀 테스트가 아직 미확인이라는 실제 잔여 범위로 바꿨다.

### 이슈 2 — 취소/환불 매출 기준이 여러 계층에 흩어짐

- 증상: 문서·SQL 뷰·프론트 mock 중 한 곳만 상태 기준을 바꾸면 대시보드와 매출 화면 수치가 달라질 수 있다.
- 원인: 주문 상태와 결제 상태가 모두 집계 조건에 관여하며, 계약·DB·표시 계층이 분리돼 있다.
- 해결: 계약 문서, 매출 규칙 문서, SQL 뷰 생성 스크립트, 주문 아키텍처의 변경 이력을 함께 남겼다. 실제 DB 결과는 별도 Bruno/DB 검증으로 확인해야 한다.

### 이슈 3 — 구현 커밋만으로 통합 동작을 증명할 수 없음

- 증상: Controller/Service/Mapper와 공통 응답 코드가 추가됐지만, 프론트가 실제 서버를 호출해 화면 상태까지 바뀌는 증거는 이 기록 시점에 없다.
- 원인: mock 기반 프론트와 backend가 독립 저장소·독립 실행 환경으로 진행됐다.
- 해결: `구현 완료`가 아니라 `실연동·통합 테스트 미확인`으로 기록하고, 다음 검증 명령과 Bruno 시나리오를 TODO로 남겼다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| 오늘 작업 범위 | Git 작성자 `hagenie128`과 7/23 커밋 시각을 대조 | 각 저장소 `git log --since` |
| 매출 제외 기준 | `CANCELED`/`REFUNDED`가 계약·SQL 뷰 작업에 함께 등장 | `create_sales_views_mysql.py`, `SALES_CANCELLATION_REFUND_RULES.md` |
| Admin Live Order | controller/service/mapper/DTO 변경 커밋 존재 | `AdminOrderController`, `AdminOrderService`, `AdminOrderMapper` |
| 프론트 계약 | Admin mock 문서에 `totalAmount`·`CANCELED` 기준 반영 | `ASAK-Admin/public/mocks/README.md`, API integration 문서 |
| 실행 검증 | 이 워크로그 작성 시점에 저장된 Gradle·Bruno·E2E 결과 미확인 | `./gradlew test`, `api/` Bruno 컬렉션, Admin/Kiosk Network 탭 |

## 8. 이번 작업에서 배운 점

1. 화면 mock이 보이는 것과 실제 API가 연동되는 것은 다른 완료 기준이다. 계약·응답·DB 집계·프론트 adapter까지 연결한 뒤에만 화면 단위 완료를 판단할 수 있다.
2. 취소/환불처럼 매출에 영향을 주는 상태는 enum 이름만 맞추는 것으로 끝나지 않는다. API 응답, SQL WHERE/CASE, 대시보드 집계, 문서를 함께 확인해야 한다.
3. API 작업은 Bruno 같은 재현 가능한 요청 모음과 함께 남기면 프론트·백엔드가 같은 요청/응답을 더 빠르게 검증할 수 있다.
4. 백엔드 기반 작업은 기능 구현과 검증 결과를 분리해 기록해야 한다. 코드가 생겼어도 DB 연결, 인증, 업로드 경로, 화면 E2E는 별도 증거가 필요하다.

## 9. 개선사항 / TODO

- [ ] `ASAK-back`에서 `./gradlew test` 실행 및 실패 시 원인 기록
- [ ] Bruno로 health, Kiosk 메뉴/주문/결제, Admin active/live order, 취소/환불 관련 응답을 실제 서버에서 확인
- [ ] Admin/Kiosk axios adapter의 base URL·응답 envelope·`totalAmount`·상태 코드 매핑을 backend와 대조
- [ ] 취소/환불 데이터가 있는 DB fixture로 매출 요약·월별·일별 합계 회귀 확인
- [ ] 업로드 파일의 배포 환경 저장 위치, 권한, URL 노출 정책 확인
- [ ] Figma의 Loading/Empty/Error/Disabled 상태와 실제 API 실패/빈 응답 상태 매핑 확인

## 10. 검증 내용

- 실행한 명령어:
  - `git log --all --since='2026-07-23 00:00:00 +09:00'` (ASAK / ASAK-Admin / ASAK-back)
  - `git show --stat <commit>`으로 각 작업의 변경 파일 대조
- 테스트한 시나리오:
  - Git evidence로 API 계약·SQL 집계·Admin mock 문서·Backend Controller/Service/Mapper 변경 범위 확인
  - 기존 Admin mock 기록의 `npm run build` 성공 이력은 별도 entry에 유지
- 확인 결과:
  - 오늘 오후 API 계약·매출 규칙·Bruno 컬렉션·백엔드 기반·Admin Live Order 조회 구현 커밋을 확인했다.
  - 이 entry 작성 시점에는 Gradle 자동 테스트, 실제 DB 매출 집계, Bruno 실제 호출, 프론트↔백엔드 E2E 성공 결과를 실행·확인하지 않았다.

## 11. 포트폴리오용 요약

ASAK Admin/Kiosk mock 화면의 다음 단계로 메뉴·결제 API 계약과 취소·환불 매출 집계 기준을 문서·SQL 뷰에 맞추고, 표준 응답/예외/페이지 응답·Admin Live Order 조회·업로드 파일 제공 기반을 정리했다. 통합 테스트 범위는 완료로 과장하지 않고 별도 체크리스트로 남겼다.

## 12. 첨부하면 좋은 자료

- 일일 기록: [2026-07-23 daily](../../daily/이하진/2026-07-23.md)
- 같은 날 Admin UI 상세: [Admin mock·Figma 정합](2026-07-23-admin-mock-figma-parity.md)
- API 계약 대조 문서: `ASAK/docs/product_bible/02_Order_Cart_Payment/docs/09-features/payment/PAYMENT_API_CONTRACT.md`
- 매출 규칙: `ASAK/docs/product_bible/04_Dashboard_Sales_Kitchen_TTS/docs/09-features/sales/SALES_CANCELLATION_REFUND_RULES.md`
- Bruno 컬렉션: `ASAK-back/api/`
- 관련 커밋: `43dcf96`, `ba4bc8f`, `a255e24`, `ffb5889`, `b6f7425`, `300c851`, `3333e04`, `da736ab`, `410a897`, `a4cba77`, `e0221f4`, `5c32687`, `2f71fed`, `d36b88a`, `df2cfdb`
