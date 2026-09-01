# 2026-08-18 API 연동·결제수단 명세 — 김나연

> **일일 기록:** [2026-08-18 daily](../../daily/김나연/2026-08-18.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-18
- 담당자: 김나연
- 저장소: `ASAK-back`, `ASAK-Kiosk`
- 브랜치: `ny/api-connection` → `main` 정렬
- 관련 이슈/PR/화면: API-014, API-006, Cart/Payment
- 작업 유형: `fix` / `docs` / merge

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: DB 컬럼 rename·DTO 필드 불일치로 키오스크 실연동이 깨졌고, API-014 wiki가 DB와 어긋났다.
- 기대 결과: `ny/api-connection`을 main에 맞추고, 결제수단·주문·카트 경로가 **동일 필드명**으로 동작한다.

## 3. 직접 구현 영역

### ASAK-back

- 주문 생성·결제 승인 request body 필드 수정
- API-014 Bruno·wiki — `description`, `imageAssetId`, `media_asset` 조인 설명
- DB 컬럼 rename 반영 (`pay_method_cfg` 등)

### ASAK-Kiosk

- `uuidv4` — `crypto.randomUUID` 미지원 환경 대응
- `CartPage` — 수량 0·장바구니 비우기 `ConfirmDialog`
- API adapter 경로·필드 수정

## 4. 구현 로직 / 적용한 방식

- 어떤 로직을 사용했는지:
  - wiki·Bruno·DTO·mapper를 **DB 컬럼명 기준**으로 재정렬
  - Kiosk adapter에서 응답 필드 `active` 통일
- 왜 그 방식을 선택했는지:
  - 카톡 8/18 합의: `isEnabled` Jackson/Lombok 이슈 회피
- 데이터 흐름:
  - 결제수단 GET → Cart/Payment 표시 → 주문 POST → (이후) PG 승인
- 핵심 예외:
  - 구형 브라우저 UUID — polyfill `uuidv4`

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (DB 정렬·명세 보강 시 사용 추정)
- 어떤 질문/요청을 했는지: api-db-alignment 매트릭스·wiki 동기화
- 그대로 사용한 부분: [api-db-alignment-decision-matrix](../../../docs/ai-reports/2026-08-18/api-db-alignment-decision-matrix.md) 구조
- 수정해서 사용한 부분: Kiosk UX(ConfirmDialog)는 직접 구현

## 6. 발생 이슈

- 이슈 1:
  - 증상: `imageAssetId`만 있어 이미지가 안 보임
  - 원인: `media_asset` JOIN·URL 필드 미연결
  - 해결: mapper·wiki에 조인·필드 설명 추가

- 이슈 2:
  - 증상: AI/DB 작업 후 명세·DTO 불일치
  - 원인: 컬럼 rename 팀 공유 누락 (카톡 8/18)
  - 해결: decision matrix·Bruno로 정본 고정

- 이슈 3:
  - 증상: `isEnabled` 직렬화가 `enabled`로 나감
  - 원인: Lombok+Jackson 조합
  - 해결: 팀 합의로 JSON 키 `active` 통일

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Network 탭 4xx·필드 undefined (당일 상세 미기록)
- 의심했던 지점: adapter 경로, request body 키, pay_method_cfg 컬럼
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `docs/api/rest-api-spec.md` API-014 절
  - `src/api/*.js`, `CartPage.jsx`
  - Bruno `payment-methods` 요청

## 8. 이번 작업에서 배운 점

- DB rename은 **코드·wiki·Bruno·FE adapter**를 같은 날 묶어야 한다.
- 결제수단은 Admin OFF와 Kiosk 목록이 같은 `methodId`를 봐야 한다 (9/2 QA에서 재발).

## 9. 개선사항 / TODO

- Admin 결제수단 토글 → Kiosk 반영 E2E
- 이미지 URL을 응답에 직접 넣을지 `imageAssetId`만 유지할지 정책 확정

## 10. 검증 내용

- 실행한 명령어: `npm run dev`, `./gradlew compileJava` (추정)
- 테스트한 시나리오: 카트 비우기·결제수단 목록 로드 (상세 미기록)
- 확인 결과: **부분 연동** — 전체 E2E·토스 승인은 8/21 이후

## 11. 포트폴리오용 요약

실API 연동 주간에 결제수단 계약을 DB·명세·프론트에 맞추고 카트 UX를 보강했다.

## 12. 첨부하면 좋은 자료

- [api-db-alignment-decision-matrix](../../../docs/ai-reports/2026-08-18/api-db-alignment-decision-matrix.md)
- API-014 Bruno 성공 캡처
- Cart ConfirmDialog 스크린샷
