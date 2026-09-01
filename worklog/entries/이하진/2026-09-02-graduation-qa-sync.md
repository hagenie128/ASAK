# 2026-09-02 종강 QA·Admin MVP — 이하진

> **일일 기록:** [2026-09-02 daily](../../daily/이하진/2026-09-02.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-09-02
- 담당자: 이하진
- 저장소: `ASAK`, `ASAK-Admin`, `ASAK-back`
- 브랜치: `main`
- 관련 이슈/PR/화면: 종강 시연 MVP · TC-001~017 · WBS 종강
- 작업 유형: `feature` / `docs` / QA
- 구현 근거: `91ca046`, `6071c68`, `b0718b3`

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: 종강 시연 전 Admin·Kiosk가 같은 DB·API 계약으로 동작하는지 **재현 가능한 근거**가 없었다.
- 기대 결과: PowerShell QA 스크립트로 PASS/FAIL을 남기고, Admin MVP·wiki·발표 대본을 한 커밋 세트로 고정한다.

## 3. 직접 구현 영역

- `scripts/qa-admin-api-2026-09-02.ps1` — 로그인·Live·품절·매출·결제수단 등 24 assertion
- `scripts/qa-kiosk-api-2026-09-02.ps1` — 주문·결제·품절·cart validate 18 assertion
- Admin FE 27파일: Login, LiveOrderBoard, SoldOut, MenuEdit, Sales, PaymentMethod, Dashboard
- Backend 14파일: OptionItemSummary, SoldOut mapper, PaymentMethod, Sales/Dashboard DTO
- wiki: QA 보고서, 체크리스트, 발표 대본, 문서·코드 대조, 회의록 W35/W36

## 4. 구현 로직 / 적용한 방식

- QA 스크립트:
  - `Invoke-RestMethod` + 고정 `storeNumber=0001` · 테스트 주문 생성 · 상태 PATCH · 품절 PATCH 복구
  - 결과를 JSON으로 `docs/wiki/qa-*-results-2026-09-02.json`에 저장
- Admin MVP:
  - `salesDisplay.js` — `fillDailyRows`, 전주 대비, 오늘/주/월 버튼
  - `useSoldOutDraft` — affectedMenus·catalog scope
  - `MenuEditPanel` — Cloudinary 미리보기·재료 role·옵션 items[]
- 데이터 흐름 (시연 핵심):
  - Kiosk 주문·CARD 결제 → Admin Live 목록 → 상태 변경 → (선택) 품절 PATCH → Kiosk `isSoldOut`

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: QA 스크립트 작성·실행, 체크리스트·대본 동기화, entry backfill
- AI가 도움 준 부분: 스크립트 초안, wiki 표 정리, 회의록 초안
- 수정해서 사용한 부분: assertion 필드명, 시연 FAIL 주석, 「코드 연결 ≠ DONE」 체크박스 정책

## 6. 발생 이슈

- 이슈 1:
  - 증상: Admin에서 CARD `active=false` 후에도 Kiosk 결제수단 목록에 CARD 노출
  - 원인: Admin·Kiosk `methodId` 불일치 추정 (QA FAIL)
  - 해결: 시연에서 Admin만 토글 시연 또는 스크립트에 FAIL 명시 — **미수정**

- 이슈 2:
  - 증상: INGREDIENT `ing125` 품절 시 `affectedMenuCount=0`, Kiosk 미반영
  - 원인: 재료 단위 품절 연쇄 미구현
  - 해결: 시연은 **MENU 단위** 품절로 대체

- 이슈 3:
  - 증상: READY 주문 취소 시 HTTP 500
  - 원인: (미추적) — 시연 범위에서 제외

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: QA 스크립트 stdout PASS/FAIL 라인
- 의심했던 지점: 결제수단 mapper JOIN, 품절 catalog view, 일별 매출 response 키(`rows` vs `dailySales`)
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `scripts/qa-admin-api-2026-09-02.ps1`
  - `AdminPaymentMethodMapper.xml`, Kiosk payment-methods API
  - `docs/wiki/demo-tc-execution-sheet-2026-09-02.md`

## 8. 이번 작업에서 배운 점

- API QA 스크립트가 있어야 「어제 PASS」를 다음 날 다시 증명할 수 있다.
- 체크리스트 `[ ]`는 팀 검토·UI E2E 전까지 비우는 게 시연 사고를 줄인다.

## 9. 개선사항 / TODO

- 일별 매출 스크립트 assertion 필드명 정렬
- Admin→Kiosk 결제수단 단일 `methodId` 정본
- UI 브라우저 E2E·Cloudinary 업로드 E2E
- RTOS 영수증 리허설 (Plan B)

## 10. 검증 내용

- 실행한 명령어:
  - `.\scripts\qa-admin-api-2026-09-02.ps1`
  - `.\scripts\qa-kiosk-api-2026-09-02.ps1`
  - `ASAK-Admin` `npm run build`
  - `ASAK-Kiosk` `npm run build`
  - `ASAK-back` `./gradlew compileJava`
- 테스트한 시나리오:
  - Admin 22/24 PASS (로그인, Live, 품절 PATCH, 매출 890300 등)
  - Kiosk 17/18 PASS (EAT_IN/TAKE_OUT, CARD, idempotency, MENU 품절)
- 확인 결과:
  - **API 기준** 대부분 PASS · UI 클릭·RTOS **미검증**

## 11. 포트폴리오용 요약

종강 전 PowerShell API QA로 Admin·Kiosk 계약을 검증하고, Admin 종강 MVP와 wiki·발표 대본을 한 번에 맞췄다.

## 12. 첨부하면 좋은 자료

- [graduation-demo-mvp](../../../docs/wiki/graduation-demo-mvp-2026-09-02.md)
- [demo-tc-execution-sheet](../../../docs/wiki/demo-tc-execution-sheet-2026-09-02.md)
- `qa-admin-api-results-2026-09-02.json`, `qa-kiosk-api-results-2026-09-02.json`
- Admin 매출·품절 화면 스크린샷 (UI E2E 후)
