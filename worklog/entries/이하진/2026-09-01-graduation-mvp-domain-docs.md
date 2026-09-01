# 2026-09-01 졸업 MVP·도메인 분리 문서 — 이하진

> **일일 기록:** [2026-09-01 daily](../../daily/이하진/2026-09-01.md)  
> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **예시:** [04-sample-work-log-example.md](../../../docs/guides/04-sample-work-log-example.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-09-01
- 담당자: 이하진
- 저장소: `ASAK` (주), `ASAK-back`, `ASAK-Admin`, `ASAK-Kiosk`
- 브랜치: `main`
- 관련 이슈/PR/화면: 종강 시연 MVP, project-completion, 3버전 split
- 작업 유형: `docs` / merge / `fix`
- 구현 근거: `e738d5f`, `17557d4`, `7373a0a`, `2acfc8f`, `8eb59a4`, `dd7cec5`

## 2. 작업 목적

- 이번 작업에서 해결하려고 한 문제: **9/2 종강**에서 말할 범위·검증·Plan B가 문서에 흩어져 있었고, 팀 종료 후 **개인 포트폴리오 repo 분리** 절차가 없었다. 영수증 브랜치 revert 혼선이 main에 남아 있었다.
- 기대 결과: 시연 정본 wiki 한곙, 체크리스트에 「코드 연결 ≠ DONE」, mirror clone 가이드, 영수증·대기번호 main 복구.

## 3. 직접 구현 영역

### 문서 (ASAK)

| 문서 | 내용 |
|---|---|
| `graduation-demo-mvp-2026-09-02.md` | 시연 흐름 5단계, RTOS Plan B, 검증 표 |
| `project-completion-checklist-2026-09-01.md` | §0~9, 완료 판정·FAIL 명시 |
| `asak-three-version-split-guide.md` | mirror clone, `team-original-2026-09-02` 태그 |
| `git-repositories.md` | 클론·submodule·원격 URL |
| `troubleshooting-backend.md` | Gradle·MyBatis·env 이슈 |

### 코드 merge (본인 Admin·BE 도메인)

- Backend: HTTP status advice, soldout catalog scope, mapper restore
- Admin: payment method save baseline, jsconfig alias
- Kiosk: receipt branch **restore merge only** (`2acfc8f` — 김나연 영수증 작업 복구)

## 4. 구현 로직 / 적용한 방식

- 「**코드 연결 ≠ DONE**」— 체크리스트 `[ ]`는 API QA·UI E2E 전까지 미체크
- 3버전 가이드: **파일 복사 금지**, `git clone --mirror` + `push --mirror`
- revert/restore: `git log`로 단일 restore 커밋 고정 후 팀 공유

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- AI가 도움 준 내용: 체크리스트·시연 대본 초안, split 가이드 문장
- 수정해서 사용한 부분: FAIL 항목·Plan B, 「검증됨」과 「연결됨」 구분

## 6. 발생 이슈

- 이슈 1:
  - 증상: 영수증 관련 revert/restore 4회 이상
  - 원인: 병행 브랜치·WIP main 직접 push
  - 해결: `2acfc8f` restore — 시연 전 커밋 고정

- 이슈 2:
  - 증상: `asak.stackroom.cloud` 미연결
  - 원인: DNS·VM 미설정
  - 해결: Vercel URL 병행 (시연)

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: `git log` revert 체인, merge conflict (당일)
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `graduation-demo-mvp-2026-09-02.md`
  - `git log --oneline -20` 각 submodule

## 8. 이번 작업에서 배운 점

- 종강 문서는 **시연 스크립트·QA·FAIL·Plan B**를 한 파일에 모아야 발표 당일 헷갈리지 않는다.
- 팀 repo 분리는 mirror가 history를 가장 안전하게 보존한다.

## 9. 개선사항 / TODO

- 9/2 QA 스크립트 실행·결과 JSON (다음 날 완료)
- stackroom DNS·VM 또는 Vercel 단일 URL 확정
- UI E2E·Cloudinary 업로드 체크리스트 채우기

## 10. 검증 내용

- 실행한 명령어: 문서 빌드 없음 · submodule `git status` (추정)
- 테스트한 시나리오: restore 후 Kiosk receipt 경로 compile (미상세)
- 확인 결과: **문서·merge 정리** — 9/2 API QA는 **다음 날** (`91ca046` 등)

## 11. 포트폴리오용 요약

종강 시연 문서 정본과 팀/개인 Git 분리 가이드를 작성하고, 영수증·대기번호 작업을 main에 복구했다.

## 12. 첨부하면 좋은 자료

- [회의록 W36](../../../docs/operations/meeting-minutes/2026-W36.md)
- [graduation-demo-mvp](../../../docs/wiki/graduation-demo-mvp-2026-09-02.md)
- project-completion-checklist PDF/Notion 링크
- restore merge `git log` 스크린샷
