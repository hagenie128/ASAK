# Frontend Test and Handoff

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `FRONTEND_REGRESSION_PLAN.md`
- `FRONTEND_TEST_CHECKLIST.md`
- `FRONTEND_CODEX_PROMPT.md`
- `FRONTEND_DEFINITION_OF_DONE.md`
- `TWO_PERSON_TEAM_WORKFLOW.md`

---

## 원문: `FRONTEND_REGRESSION_PLAN.md`

### Frontend Regression Plan

기존 팀원이 만든 코드를 보호한다.

#### 매 변경 후

- Home
- Menu
- Detail
- Cart
- Payment
- Complete
- 기존 route
- 기존 store action
- 기존 CSS
- component import
- build/lint

#### 비교

변경 전 화면 캡처와 변경 후 화면을 비교한다.

---

## 원문: `FRONTEND_TEST_CHECKLIST.md`

### Frontend Test Checklist

#### Unit 후보

- price formatter
- total calculator
- option validation
- error mapper
- comparison calculator

#### Component

- Button
- MenuCard
- CartItemCard
- ConfirmDialog
- StatusBadge

#### Flow

- order
- payment failure
- timeout
- TTS
- sold-out save

---

## 원문: `FRONTEND_CODEX_PROMPT.md`

### Frontend Codex Prompt

ASAK-Kiosk와 ASAK_Admin의 기존 코드를 먼저 읽는다.

반드시:

1. 기존 Page/Component/Store/API 목록 작성
2. 재사용 가능 항목 표시
3. 새 파일 생성 전 중복 검색
4. 기존 팀원 코드 삭제 금지
5. 기능별 작은 commit
6. 변경 이유와 영향도 보고

우선순위:

- 기존 Kiosk 흐름 유지
- 누락 state
- API adapter
- Admin 핵심 화면
- 회귀 테스트

---

## 원문: `FRONTEND_DEFINITION_OF_DONE.md`

### Frontend Definition of Done

- [ ] 기존 화면 유지
- [ ] 기존 컴포넌트 재사용
- [ ] route 정상
- [ ] state 정상
- [ ] Mock/API 교체 가능
- [ ] loading/empty/error
- [ ] amount 정합성
- [ ] accessibility
- [ ] build/lint
- [ ] regression
- [ ] Figma 비교

---

## 원문: `TWO_PERSON_TEAM_WORKFLOW.md`

### Two-Person Team Workflow

#### 원칙

문서는 추가 업무가 아니라 구현 기준이다.

#### 기존 Frontend 작성자

- 현재 고객용 코드 유지
- 맡은 흐름 계속 구현
- 필요한 계약 문서만 참고

#### 전체 구조·Admin·Backend 담당

- API/DB 계약
- Admin
- 통합
- QA
- 문서 유지

#### 공통

- 기존 코드 합의 없이 전면 변경 금지
- 공통 파일 수정 전 공유
- 충돌 가능 파일 확인
- 새 기능은 MVP 합의 후 추가
