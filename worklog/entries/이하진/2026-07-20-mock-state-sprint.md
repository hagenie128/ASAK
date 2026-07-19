# 2026-07-20 Mock 상태 연결 스프린트 준비

> **일일:** [2026-07-20](../../daily/이하진/2026-07-20.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-20
- 담당자: 이하진
- 저장소: ASAK-Kiosk / ASAK-Admin
- 브랜치: `main`
- 관련 이슈/PR: [Kiosk #5](https://github.com/hagenie128/ASAK-Kiosk/issues/5) / [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- 작업 유형: `feature` / `docs`

## 2. 작업 목적

- 정적 UI 다음 단계인 mock 주문·결제·운영 상태 연결 작업을 실행 이슈와 구현 계획으로 고정한다.

## 3. 직접 구현 영역

- Kiosk에 loading, empty, error, modal 정적 컴포넌트와 결제·영수증·타임아웃 화면 상태 구조를 보강했다.
- Admin에 주문 관리용 정적 UI와 API mock 구조를 보강하고, 두 저장소의 구현 계획을 코드 실측 기준으로 갱신했다.
- Kiosk #5와 Admin #1을 생성해 WBS와 완료 조건을 연결했다.

## 4. 구현 로직 / 적용한 방식

- Kiosk는 수량 한도 토스트 → mock 결제 승인/실패 → 완료/오류 → 타임아웃 순서로 상태 전이를 연결한다.
- Admin은 repository/hook → adapter → Page 구조로 mock 데이터를 연결하고, Page의 직접 JSON import를 피한다.

## 5. AI 도움 영역

- Codex가 현재 구현 계획·최근 커밋·기존 이슈 목록을 확인하고, 중복 없는 실행 이슈와 워크로그를 작성했다.

## 6. 발생 이슈

- 이슈 1: Kiosk 결제·상태 연결 — [#5](https://github.com/hagenie128/ASAK-Kiosk/issues/5)
- 이슈 2: Admin mock 페이지 바인딩·상태 QA — [#1](https://github.com/hagenie128/ASAK_Admin/issues/1)

## 7. 디버깅 기록

- 확인한 근거: Kiosk의 상태 컴포넌트·결제/영수증/타임아웃 구조 커밋, Admin의 주문 관리 UI·API mock 구조 커밋.
- 실제 Backend business API는 아직 없어 P6 실연동은 BLOCKED 상태로 유지한다.

## 8. 이번 작업에서 배운 점

- 이슈는 완료된 화면 묶음보다 다음 실행 단위와 검증 조건을 중심으로 만들면 작업 추적이 쉬워진다.

## 9. 개선사항 / TODO

- Kiosk TC-K01~TC-K06, Admin TC-A01~TC-A06을 실제 mock 흐름으로 점검한다.

## 10. 검증 내용

- 실행한 명령어: Git 로그, 원격 이슈 목록, Kiosk·Admin 구현 계획 대조.
- 확인 결과: 기존 이슈가 없어 Kiosk #5와 Admin #1을 중복 없이 생성했다.

## 11. 포트폴리오용 요약

- Figma 이식 이후 남은 mock 상태 전이와 운영 화면 데이터 연결을 실행 이슈·테스트 기준으로 분해했다.

## 12. 첨부하면 좋은 자료

- Kiosk #5, Admin #1, Kiosk·Admin `IMPLEMENTATION_PLAN.md`

