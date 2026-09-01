# 2026-08-26 키오스크 칼로리·결제 UX — 김나연

> **일일 기록:** [2026-08-26 daily](../../daily/김나연/2026-08-26.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)  
> **근거:** `b867345`, `b7eda68`, `e7d2654`, `3c21e38`

---

## 1. 기본 정보

- 작업 날짜: 2026-08-26
- 담당자: 김나연
- 저장소: `ASAK-back`, `ASAK-Kiosk`
- 브랜치: `main` / `ny/api-connection`
- 관련 이슈/PR/화면: API-003 영양, Payment/OrderComplete, header 홈
- 작업 유형: `feature` / `fix`

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: 메뉴·옵션 **칼로리/단백질**이 상세·장바구니에 없고, 결제 직후 화면 전환이 어색했다.
- 기대 결과: 옵션 선택·장바구니에서 영양 합계가 보이고, 결제 성공 후 2초 뒤 완료 화면으로 이동하며 세션이 정리된다.

## 3. 직접 구현 영역

| 영역 | 파일(대표) |
|---|---|
| BE API-003 | `UserMenuMapper.xml` 옵션 kcal, cart 합산 service |
| FE 상세 | 옵션 선택 컴포넌트 칼로리 표시 |
| FE 장바구니 | 합계 칼로리 계산 |
| FE 결제 | 성공 팝업 → `OrderCompletePage`, header 홈 시 store reset |
| BE API-006 | 토스 기능 완료 커밋 표시 |

## 4. 구현 로직 / 적용한 방식

- 어떤 로직을 사용했는지:
  - BE: 메뉴·옵션 row에 kcal/protein 컬럼 조회·합산
  - FE: 선택 옵션 배열 기준 합계 표시, 결제 성공 `setTimeout(2000)` 후 navigate
- 데이터 흐름:
  - 메뉴 상세 API → 옵션 kcal 표시 → 장바구니 합산 → 결제 → 완료
- 핵심 예외:
  - header에서 홈 클릭 시 `orderSessionStore` reset

## 5. AI 도움 영역

- 사용한 AI 도구: (당일 기록 없음)
- backfill: Cursor로 커밋 4건 묶어 12섹션 정리

## 6. 발생 이슈

- 이슈 1:
  - 증상: 영양 값 0 또는 미표시 가능성
  - 원인: seed·mapper 필드 누락 (이하진 nutrition seed와 별도 검증 필요)
  - 해결: 당일 커밋만 — 브라우저 E2E **미기록**

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: backfill 미재실행
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `UserMenuMapper.xml`, 장바구니 합산 컴포넌트
  - `PaymentPage.jsx`, `orderSessionStore.js`

## 8. 이번 작업에서 배운 점

- 영양 정보는 **옵션 단위**까지 내려와야 장바구니 합계가 맞는다.
- 결제 완료 UX는 즉시 전환보다 짧은 딜레이가 손님 인지에 유리할 수 있다.

## 9. 개선사항 / TODO

- Product Bible 영양 표기 규칙과 UI 문구 통일
- 칼로리 합산 단위 테스트 (옵션 다중 선택)

## 10. 검증 내용

- 실행한 명령어: `npm run build`, `./gradlew compileJava` (추정)
- 테스트한 시나리오: 미기록
- 확인 결과: **커밋·빌드만** — 브라우저 영양 표시 E2E 없음

## 11. 포트폴리오용 요약

주문 흐름에 영양 정보를 넣고 결제 완료 UX를 다듬었다.

## 12. 첨부하면 좋은 자료

- 메뉴 상세·장바구니 칼로리 스크린샷
- 결제 성공 → 완료 화면 전환 GIF
- 관련 커밋 `b867345` 등 diff
