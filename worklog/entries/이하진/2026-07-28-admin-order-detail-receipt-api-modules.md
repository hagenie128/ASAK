# 2026-07-28 관리자 주문 상세 금액 내역 및 API 모듈 정리

> 일일 기록: [2026-07-28.md](../../daily/이하진/2026-07-28.md)

---

## 1. 기본 정보

- 작업 일자: 2026-07-28
- 담당자: 이하진
- 저장소: ASAK-Admin / ASAK-back
- 최종 브랜치: ASAK-Admin / ASAK-back `main` 반영 완료
- 관련 이슈/PR: 별도 Issue/PR 없음. Admin 기능 브랜치 2개와 백엔드 기능 브랜치 1개를 각각 `main`에 fast-forward 병합
- 작업 유형: `feature` / `refactor`

## 2. 작업 목적

- 관리자 주문 상세에서 메뉴 기본 금액만 보이던 문제를 개선해, 옵션별 추가금과 제외 재료 및 메뉴 합계를 함께 확인한다.
- 영수증 출력 화면에서도 재사용할 수 있는 주문 금액 표시 구조를 만든다.
- API 파일명을 역할이 드러나는 `*Api.js` 형식으로 통일하고 기존 주문 호출부를 새 모듈에 연결한다.
- 활성 주문 목록을 주문 목록 DTO로 일관되게 반환하고, 주문 목록 개수와 판매 분석이 실제 테이블·뷰 기준으로 조회되도록 정비한다.

## 3. 직접 구현 영역

- `src/api/`의 API 모듈 7개를 `adminApi.js`, `apiClient.js` 등 `*Api.js` 형식으로 변경
- `useOrdersQuery.js`, `OrderManagementPreview.jsx`의 주문 목록·상세 호출을 `ordersApi`로 연결
- `OrderDetailPanel.jsx`에서 옵션별 금액, 제외 재료, 메뉴 합계를 각각 표시
- `orders.css`에 옵션/제외 블록, 금액 정렬, 메뉴 합계 스타일 추가
- `AdminOrderController`, `AdminOrderService`, `AdminOrderMapper`, `AdminOrderMapper.xml`에서 활성 주문 조회 DTO와 목록 집계 쿼리 정비
- `docs/view.sql`에 주문 옵션·제외 재료 뷰 정의와 일/시간별 판매·상위 메뉴 집계 뷰 반영

## 4. 구현 로직 / 적용한 방식

- 메뉴 첫 줄은 기존 `unitPrice`와 메뉴 수량을 유지한다.
- 옵션 행 금액은 `옵션 가격 × 메뉴 수량 × 옵션 수량`으로 계산한다.
- 메뉴 합계는 `기본 메뉴 단가 × 메뉴 수량 + 모든 옵션 행 금액`으로 계산한다.
- 옵션과 제외 재료를 별도 블록으로 나누고, 옵션이 없거나 제외 재료가 없을 때는 `없음`을 표시한다.
- 변경을 API 모듈 정리와 주문 상세 UI 개선으로 분리해 각각 기능 브랜치·한글 커밋·원격 푸시·`main` 병합으로 처리했다.
- 활성 주문 조회는 `OrderListResponse`를 반환하고, XML `getActiveOrders` 쿼리도 같은 DTO 필드에 맞춰 `vw_order_list_summary`에서 RECEIVED·PREPARING 주문을 조회한다.
- 주문 목록 개수는 뷰 의존 대신 `orders`, `payment`, `common_code`, `order_item`, `menu` 기준으로 필터를 동일하게 적용한다.
- 판매 분석은 취소·환불 금액을 분리해 일/시간별 순매출과 상위 메뉴 집계를 제공한다.

## 5. AI 지원 영역

- 사용자 요청: 옵션과 제외 재료 분리 표시, 주문 상세의 영수증형 금액 확인, 기능별 Git 분리 배포
- AI가 지원한 내용: 옵션 금액 계산 기준 검토, 변경 파일 범위 확인, JSX/CSS 구조 제안 및 검증 명령 실행
- AI가 지원한 내용: 활성 주문 API의 Controller·Service·Mapper·XML DTO 일치 확인, 원격 main 차이와 Java 컴파일 검증
- 그대로 사용한 부분: 주문 상세의 옵션·제외·메뉴 합계 표시 구조
- 수정해서 사용한 부분: 기존 작업 트리 변경을 보존하며 API 모듈 변경과 UI 변경을 별도 커밋으로 분리

## 6. 발생 이슈

- 이슈 1: GitHub CLI 인증 토큰 만료
  - 증상: `gh auth status`에서 기본 계정 토큰이 유효하지 않다고 표시
  - 원인: GitHub CLI의 로컬 인증 토큰 만료
  - 해결: PR 생성은 사용하지 않고, 사용자 요청 범위에서 기능 브랜치를 푸시한 뒤 `main`에 fast-forward 병합 및 Git 원격 푸시로 완료
- 이슈 2: ASAK-back 로컬 `main`이 원격 `origin/main`보다 4커밋 뒤
  - 증상: 원격 사용자 API-003~005 변경이 로컬 관리자 주문 변경보다 앞서 있음
  - 원인: 별도 사용자 API 작업이 원격 main에 먼저 병합됨
  - 해결: 관리자 주문 변경을 `agent/admin-order-query-sales-views`로 분리하고, 최신 `origin/main` 위로 rebase한 뒤 `main`에 fast-forward 병합·푸시 완료

## 7. 디버깅 기록

- 확인한 로그/오류 메시지: `gh auth status` 토큰 만료 메시지, Vite 번들 크기 경고
- 의심했던 지점: GitHub CLI 인증 실패가 Git 원격 푸시까지 막는지 여부
- 실제 원인: GitHub CLI 인증과 HTTPS Git 원격 인증은 별도 상태였으며, Git push는 정상 동작
- 다시 같은 문제가 생기면 먼저 볼 파일/명령: `gh auth status`, `git remote -v`, `git status --short --branch`
- Gradle 최초 실행은 샌드박스 네트워크 제한으로 배포본 다운로드가 막혔으나, 권한 있는 환경에서 재실행해 `compileJava` 성공을 확인했다.

## 8. 이번 작업에서 배운 점

- 관리자 상세는 조리 정보뿐 아니라 결제 금액 검증에도 쓰이므로, 옵션을 요약 문자열로 합치기보다 행 단위로 표시하는 편이 안전하다.
- `unitPrice`는 원본 기본 단가로 보존하고, 화면용 메뉴 합계는 별도 계산값으로 처리해야 금액 근거를 잃지 않는다.
- 혼합된 작업 트리는 파일 단위로 스테이징해 기능별 커밋을 분리해야 병합 이력과 되돌리기 범위가 명확하다.
- 원격 main이 앞서 있을 때는 작업 파일과 원격 커밋의 겹침을 먼저 확인하고, 기능 브랜치를 최신 main 위로 rebase한 뒤 게시해야 한다.

## 9. 개선사항 / TODO

- 실제 주문 응답에서 옵션 가격이 없는 예외 데이터의 표시 정책을 확인한다.
- 옵션 가격 0원, 메뉴 수량 2개 이상, 제외 재료만 존재하는 주문을 브라우저에서 확인한다.
- 영수증 출력 기능 구현 시 현재 주문 상세의 데이터 구조를 공통 포맷으로 재사용할지 결정한다.
- 실제 주문 데이터로 활성 주문·판매 분석 API 응답을 Bruno와 브라우저에서 확인한다.

## 10. 검증 내용

- 실행한 명령: `npm.cmd run lint`
- 테스트한 시나리오: API 모듈 import 변경 후 정적 검사
- 확인 결과: 오류 0건, 기존 미사용 변수 경고 2건
- 실행한 명령: `npm.cmd run build`
- 테스트한 시나리오: 주문 상세 JSX/CSS를 포함한 Vite 프로덕션 빌드
- 확인 결과: 빌드 성공. 기존 번들 크기 경고만 출력
- Git 검증: 각 기능 브랜치에서 `git diff --cached --check` 통과 후 커밋·푸시, `main...origin/main` 일치 확인
- 실행한 명령: `gradlew.bat -p C:\ASAK-workspace\ASAK-back compileJava --no-daemon`
- 테스트한 시나리오: 관리자 활성 주문 Controller·Service·Mapper·XML DTO 정합성 및 Java 컴파일
- 확인 결과: `BUILD SUCCESSFUL`

## 11. 포트폴리오용 요약

- 관리자 주문 상세 화면을 영수증형 금액 내역으로 개선해 메뉴 기본 금액, 옵션별 추가금, 제외 재료, 메뉴 합계를 한 화면에서 검증할 수 있도록 구현했다.
- API 모듈 명명 규칙을 통일하고 주문 조회 호출부를 연결했으며, 변경을 기능 단위 브랜치와 한글 커밋으로 분리해 배포했다.
- 활성 주문과 판매 분석 뷰의 조회 기준을 정비하고, 원격 변경과의 병합 전 Java 컴파일까지 검증했다.

## 12. 첨부 / 참고 자료

- 커밋: `aecf6f8` — `refactor: 관리자 API 모듈 명명 통일`
- 커밋: `96352d9` — `feat: 관리자 주문 상세 금액 내역 표시`
- 브랜치: `agent/api-module-naming`, `agent/order-detail-receipt`
- 백엔드 커밋: `05d6351` — `feat: 관리자 주문 조회와 판매 뷰 정비`
- 관련 화면: SCR-010 Admin Order Management / Figma node `39:7363`
