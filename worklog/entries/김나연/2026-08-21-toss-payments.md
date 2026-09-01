# 2026-08-21 토스페이먼츠·API-006 — 김나연

> **일일 기록:** [2026-08-21 daily](../../daily/김나연/2026-08-21.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-21
- 담당자: 김나연
- 저장소: `ASAK-back`, `ASAK-Kiosk`
- 브랜치: `ny/api-connection` ↔ `main` merge
- 관련 이슈/PR/화면: API-006, PaymentPage, Toss Payments sandbox
- 작업 유형: `feature` / merge

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: 키오스크에서 토스 테스트 결제 후 **서버 승인·주문 상태 확정**이 연결되지 않았다.
- 기대 결과: Toss SDK success → API-006 → `orderSessionStore`에 `orderStatus`, `approvedAmount`, `approvedAt` 반영.

## 3. 직접 구현 영역

- Kiosk `PaymentPage` — Toss SDK, success/fail handler → API-006 호출
- Backend `UserPayService` — `RECEIVED` 등 상태 전이, payment row
- `orderSessionStore` — `orderStatus`, `approvedAmount`, `approvedAt` 매핑
- `ErrorCode` enum 주석 정리
- `ny/api-connection` ↔ main merge 충돌 해결

## 4. 구현 로직 / 적용한 방식

- 어떤 로직을 사용했는지:
  - 클라이언트: Toss 위젯 → paymentKey·orderId·amount 수집 → 백엔드 승인 POST
  - 서버: 금액·주문 id 검증 → 토스 API 호출 → DB 갱신
- 데이터 흐름:
  - 주문 생성 → 결제 화면 → Toss 승인 → API-006 → 완료/실패 UI
- env (로컬, **시크릿 본문 미기록**):
  - `VITE_TOSS_CLIENT_KEY`, `TOSS_SECRET_KEY` (test)
  - `VITE_API_BASE_URL`, `VITE_PAYMENT_PUBLIC_ORIGIN`

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (merge·adapter 수정 시 추정)
- 그대로 사용한 부분: Toss 공식 샘플 흐름
- 수정해서 사용한 부분: ASAK `orderSessionStore` 필드명·에러 코드 매핑

## 6. 발생 이슈

- 이슈 1:
  - 증상: `ny/api-connection` ↔ main merge 충돌
  - 원인: 결제·주문 파일 동시 수정
  - 해결: 당일 merge 완료

- 이슈 2:
  - 증상: 동일 paymentKey 재전송
  - 원인: idempotency 미처리 시 중복 row
  - 해결: 409 처리 — 9/2 QA PASS

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Toss fail URL, API 409/500 (상세 미기록)
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `PaymentPage.jsx`, `UserPayService.java`
  - 브라우저 Network · Toss 개발자 콘솔

## 8. 이번 작업에서 배운 점

- PG는 **클라이언트 성공 ≠ 서버 확정** — 반드시 API-006으로 맞춰야 한다.
- merge 전에 결제 필드명을 store·DTO·wiki에 먼저 고정하는 편이 안전하다.

## 9. 개선사항 / TODO

- 영수증·대기번호 (8/29~9/1, 김나연 담당)
- 주문 중 품절 차단 SQL (종강 후보)
- RTOS 영수증 (이하진 협업, Plan B)

## 10. 검증 내용

- 실행한 명령어: `npm run dev`, sandbox 카드 결제 (추정)
- 테스트한 시나리오: EAT_IN/TAKE_OUT + CARD 승인 1회 이상
- 확인 결과: **로컬 sandbox 연동** — 9/2 스크립트에서 idempotency PASS

## 11. 포트폴리오용 요약

테스트 PG와 Spring 결제 승인 API를 end-to-end로 연결했다.

## 12. 첨부하면 좋은 자료

- Toss sandbox 결제 성공 화면
- API-006 요청/응답 JSON (키 마스킹)
- merge 전후 `git log` 스크린샷
