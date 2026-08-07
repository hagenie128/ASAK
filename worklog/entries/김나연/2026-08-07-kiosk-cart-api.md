# 2026-08-07 키오스크 장바구니·결제 · 고객 장바구니 검증 API

> **일일 기록:** [2026-08-07 daily](../../daily/김나연/2026-08-07.md)
> **근거:** Git 커밋·`git show --stat`·변경 파일. **코드 커밋 ≠ 통합 검증 완료.**

---

## 1. 기본 정보

- 작업 날짜: 2026-08-07
- 담당자: 김나연
- 저장소: `ASAK-Kiosk` / `ASAK-back`
- 브랜치: `main` / `ny/api-connection` (Kiosk `2d4068f`는 origin/ny/api-connection·main에 포함)
- 관련 이슈/PR/화면: API-004
- 작업 유형: `feature` / `fix`
- 구현 근거: `f250230`, `2d4068f` (Merge 참고: `d9deebd`, `47c7792`)
- Figma 기준: 당일 커밋에 Figma 노드 추가/변경 evidence가 명시되지 않음 → `Figma 미확인`. UI 상태별(Frame/Loading/Empty/Error) 재대조는 별도 검증이다.
- 완료 판정: 커밋 반영은 확인. **Gradle/npm/Bruno/브라우저/실DB 통합 결과는 이 기록에서 재실행하지 않음.**

## 2. 작업 목적

- ASAK-Kiosk / ASAK-back에서 확인된 당일 작업을 **키오스크 장바구니·결제 · 고객 장바구니 검증 API** 단위로 정리한다.
- 장바구니 검증 DTO/서비스에 메뉴별 id를 맞추고, 키오스크 Cart/Payment가 검증 API를 호출할 수 있게 한다.
- mock/화면/API/문서 중 실제로 손댄 경계를 커밋·파일로 구분해, 다음 실연동·검증 범위를 남긴다.
- 완료 판정은 코드 반영과 분리한다. 통합 테스트·브라우저·실DB 증거가 없으면 미검증으로 둔다.

## 3. 직접 구현 영역

Git 커밋 이력으로 다음 직접 작업을 확인했다.

- **고객 API·장바구니 검증:**
  - `f250230` fix: api-004장바구니로직 수정 & 장바구니메뉴별id 추가 로직
  - 주요 파일: `CartValidateItemRequest.java`, `CartValidateItemResponse.java`, `CartValidateResponse.java`, `UserOrderService.java`
- **키오스크 장바구니·결제:**
  - `2d4068f` update: api-004 장바구니 검증 api 추가
  - 주요 파일: `src/api/cart.js`(신규), `src/constants/api.js`, `CartPage.jsx`, `PaymentPage.jsx`, `orderSessionStore.js`, `payment.css`
- **Merge (기능 범위 아님):**
  - `d9deebd`, `47c7792` Merge branch 'ny/api-connection'

## 4. 구현 로직 / 적용한 방식

- **근거 순서:** Git 커밋·변경 파일 → 현재 코드 경로 → (있으면) Screen/API 문서. Product Bible과 코드가 다르면 코드/실측을 우선하고 문서는 별도 TODO로 남긴다.
- **저장소 경계:** ASAK-Kiosk / ASAK-back. 프론트·백엔드 커밋이 같은 날이면 영역별로 나눠 기록한다.
- **고객 API·장바구니 검증:** Request/Response DTO와 `UserOrderService`에서 메뉴별 id를 다루는 방향으로 수정됐다. 대표 파일: `UserOrderService.java`.
- **키오스크 장바구니·결제:** `cart.js` API 모듈을 추가하고 Cart/Payment 페이지·세션 스토어에서 검증 호출 경로를 연결했다. 대표 파일: `src/api/cart.js`, `CartPage.jsx`, `PaymentPage.jsx`.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: `2026-08-07` 작업을 2026-07-23 API 계약 entry 수준의 12섹션 상세 기록으로 재작성하도록 요청했다.
- AI가 도움 준 내용: 커밋·파일 목록 수집, 영역 분류, 이슈/TODO/검증 문장 구조화.
- 그대로 사용한 부분: 커밋 해시, 메시지, 변경 파일 경로, stat 요약.
- 수정해서 사용한 부분: 서술 문장·영역 묶음. 원 구현 시점의 AI 사용 여부와 런타임 로그는 커밋만으로 복원하지 않았다.

## 6. 발생 이슈

### 이슈 — 프론트·백엔드가 같은 날 움직여도 실연동 증거는 별개

- 증상: 키오스크와 백엔드 커밋이 함께 있어도 Network 탭/Bruno 성공 로그가 없으면 연동 완료로 볼 수 없다.
- 원인: 저장소·실행 환경이 분리되어 있다.
- 해결: `구현 진행`으로 두고 adapter·실DB 검증을 TODO로 분리한다.

### 이슈 — Merge와 기능 커밋을 구분해야 함

- 증상: 같은 날 `ny/api-connection` Merge와 기능 fix/update가 함께 있다.
- 원인: 브랜치 통합과 기능 작업이 연속으로 올라갔다.
- 해결: 기능 근거는 `f250230`·`2d4068f`만 본문으로 두고, Merge는 참고로만 적는다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| 당일 커밋 | non-merge 2건 + Merge 2건 | 각 저장소 `git log --since/--until` |
| 고객 API·장바구니 검증 | `f250230` · 파일 4 | `UserOrderService.java` |
| 키오스크 장바구니·결제 | `2d4068f` · 파일 6 | `src/api/cart.js`, `CartPage.jsx` |
| 실행 검증 | 이 entry 보강 시점에 Gradle/npm/Bruno/브라우저 재실행 없음 | 저장소별 test/build · Network 탭 |

## 8. 이번 작업에서 배운 점

1. 장바구니 검증은 FE adapter와 BE DTO/서비스가 같은 필드(메뉴별 id)를 봐야 한다.
2. 화면이 보이는 것과 API/DB까지 연결된 것은 다른 완료 기준이다. 커밋 수만으로 DONE을 올리지 않는다.
3. Merge 커밋은 동기화 증거일 뿐 기능 완료의 근거가 아니다.

## 9. 개선사항 / TODO

- [ ] Cart → Payment 경로에서 검증 API 성공/실패를 브라우저 Network로 확인
- [ ] Bruno 또는 동등한 도구로 cart validate 요청/응답 envelope 확인
- [ ] `ASAK-back`에서 `./gradlew test` 또는 최소 bootRun 스모크
- [ ] `ASAK-Kiosk` `npm run build` 회귀
- [ ] 실DB fixture로 장바구니 검증→주문 생성 한 사이클 확인
- [ ] Figma Cart/Payment 상태(Loading/Empty/Error)와 화면 문구 재대조

## 10. 검증 내용

- 실행한 명령어:
  - `git log --since/--until` (ASAK-Kiosk / ASAK-back)
  - `git show --stat` / `git diff-tree --name-status` (`f250230`, `2d4068f`)
- 테스트한 시나리오:
  - Git evidence로 영역별 변경 범위 확인
  - 장바구니 검증 실호출·결제 완료·실DB 저장 등은 **미실행**
- 확인 결과:
  - 2026-08-07 작성자 non-merge 커밋 **2건**과 영역별 파일 목록을 확인했다.
  - 이 entry 작성 시점에는 자동 테스트·실서버 호출·E2E 성공 결과를 새로 확보하지 않았다.

## 11. 포트폴리오용 요약

2026-08-07 김나연 작업은 ASAK-Kiosk / ASAK-back에서 API-004 장바구니 검증(메뉴별 id)·키오스크 Cart/Payment 연동을 커밋 2건으로 진행한 기록이다. 변경 파일과 영역 경계를 기준으로 설명하고, 통합 테스트·실DB·브라우저 검증은 완료로 과장하지 않았다.

## 12. 첨부하면 좋은 자료

- 일일 기록: [2026-08-07 daily](../../daily/김나연/2026-08-07.md)
- 관련 커밋: `f250230`, `2d4068f` (Merge: `d9deebd`, `47c7792`)
- 변경이 큰 경로: `UserOrderService.java`, `src/api/cart.js`, `CartPage.jsx`, `PaymentPage.jsx`
