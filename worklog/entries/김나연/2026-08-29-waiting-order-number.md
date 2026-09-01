# 2026-08-29 고정 대기번호(API-006) — 김나연

> **일일 기록:** [2026-08-29 daily](../../daily/김나연/2026-08-29.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)  
> **근거:** `37fe87a`, `cd5e99a`, `a7ef527`

---

## 1. 기본 정보

- 작업 날짜: 2026-08-29
- 담당자: 김나연
- 저장소: `ASAK-back`, `ASAK-Kiosk`, `ASAK` (docs)
- 브랜치: feature → main (9/1 restore merge는 이하진)
- 관련 이슈/PR/화면: API-006 `waitingOrderNo`, OrderCompletePage
- 작업 유형: `feature` / `docs`

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: 결제 완료 후 손님이 볼 **대기번호**가 없거나 매번 랜덤이었다.
- 기대 결과: 결제 승인 응답에 **날짜별 고정 대기번호**(`waitingOrderNo`)를 넣고 완료 화면에 표시한다.

## 3. 직접 구현 영역

- `UserPayMapper.xml` — 일별 MAX+1 또는 시퀀스 규칙 SQL
- `ApprovePaymentResponse.waitingOrderNo`
- `OrderCompletePage` / `orderSessionStore` 바인딩
- `docs` — 고정 대기 번호 SQL·설명

## 4. 구현 로직 / 적용한 방식

- 어떤 로직을 사용했는지:
  - 매장·일자 단위로 주문 번호 증가 (SQL MAX+1 또는 dedicated sequence)
  - 승인 응답 DTO에 `waitingOrderNo` 추가 → FE store → 완료 UI
- 데이터 흐름:
  - API-006 성공 → `waitingOrderNo` 저장 → OrderComplete 렌더
- 핵심 예외:
  - 동시 승인 시 번호 충돌 — DB 트랜잭션·락 전략 (상세 미기록)

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (SQL·문서 초안 추정)
- 수정해서 사용한 부분: 일별 리셋 규칙·UI 문구

## 6. 발생 이슈

- 이슈 1:
  - 증상: 9/1 main에서 WIP revert 다회
  - 원인: 영수증·대기번호 브랜치 병행 작업
  - 해결: `2acfc8f` restore merge (이하진) — 본인 커밋은 그 전 단계까지

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: 승인 응답에 `waitingOrderNo` null 여부 (미기록)
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `UserPayMapper.xml`, `ApprovePaymentResponse.java`
  - `OrderCompletePage.jsx`

## 8. 이번 작업에서 배운 점

- 대기번호는 **비즈니스 키**라서 API-006과 UI를 동시에 맞춰야 한다.
- main revert/restore가 잦으면 시연 전 `git log`로 단일 커밋을 고정해야 한다.

## 9. 개선사항 / TODO

- 9/1 영수증 출력과 합쳐 RTOS Plan B 리허설
- 동시성 테스트 (연속 결제 2건)

## 10. 검증 내용

- 실행한 명령어: (당일) 로컬 승인 1회 추정
- 테스트한 시나리오: 완료 화면 번호 표시 — 상세 미기록
- 확인 결과: **커밋 반영** — 9/2 QA 스크립트에 대기번호 assertion 여부 별도 확인

## 11. 포트폴리오용 요약

주문 완료 후 대기번호를 일별 시퀀스로 생성·표시하도록 API와 UI를 맞췄다.

## 12. 첨부하면 좋은 자료

- OrderComplete 대기번호 스크린샷
- 고정 대기번호 SQL 문서 링크
- API-006 응답 JSON 샘플
