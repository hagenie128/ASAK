# 2026-08-07 WBS 통합·공부 레포트 경로·RTOS 노트

> **일일 기록:** [2026-08-07 daily](../../daily/이하진/2026-08-07.md)
> **같은 날 백엔드:** [MySQL 스키마·CORS](2026-08-07-mysql-schema-cors.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-07
- 담당자: 이하진
- 저장소: `ASAK`
- 브랜치: `docs/wbs-sync` · `docs/study-ai-review-move` → `main` merge (`f23bae5`, `92aea1c` 구간)
- 관련 이슈/PR: WBS 문서 정본화 · study 경로 분리 · RTOS 학습 노트 (Issue 번호 미기재)
- 작업 유형: `docs`
- 구현 근거: `2b6b201`, `b5ebf9b`, `ee7e613` (및 이후 인코딩/워크로그 보강 커밋은 별도)
- Figma 기준: 문서 작업. `Figma 미확인`(해당 없음).
- 완료 판정: 문서 경로·원격 main 반영 확인. **Hub DONE 승격·Notion sync·실기능 검증과는 무관.**

## 2. 작업 목적

- 분산돼 있던 WBS 일정/상태 문서를 `docs/wiki/wbs.md` 정본(`WBS-001`~`085`)으로 모은다.
- 공부 레포트를 `docs/ai-reports`에서 `docs/study/ai-review`로 분리해, 운영 보고서와 학습 산출물을 섞지 않는다.
- RTOS 학습 노트 `docs/study/RTOS/RTOS.md`를 저장소에 남겨 키오스크 장치/서버 분리 맥락을 복습 가능하게 한다.
- START_HERE·status-notes·index 링크가 삭제된 `wbs-v2`/`wbs-schedule`가 아니라 `wbs.md`를 가리키게 한다.

## 3. 직접 구현 영역

### WBS 통합 — `2b6b201`

- `docs/wiki/wbs.md` 추가/정본화, 관련 wiki·START_HERE·상태 메모 갱신.
- 8/7 ai-reports 근거(JSON/MD) 추가.
- 구 `wbs-schedule`·`wbs-v2`는 정본에서 제거하고 리다이렉트/링크 정리 방향으로 맞춤.

### study 경로 이동 — `b5ebf9b`

- study 성격 레포트 rename: `docs/ai-reports` → `docs/study/ai-review`.
- guides·asak-study 스킬 템플릿 경로 수정.

### RTOS 노트 — `ee7e613`

- `docs/study/RTOS/RTOS.md` 추가(장문 학습 메모).

## 4. 구현 로직 / 적용한 방식

- **정본 원칙:** Hub 상태 변경 없이 “문서 정본”만 맞춘다. 코드 있음 ≠ DONE 원칙을 문서에도 명시적으로 유지한다.
- **경로 분리:** 운영/Hub sync 보고(`ai-reports`)와 개인·팀 공부 산출물(`study/`)을 나눈다.
- **링크 일관성:** START_HERE·wiki index·status-notes가 한 WBS 파일을 보게 해 진입점 혼란을 줄인다.
- **깃반영:** 기능 브랜치 → 한글 커밋 → main merge → 작업 브랜치 정리 순서를 따랐다.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: WBS 통합, study 이동, RTOS 추가, 깃반영, 이후 UTF-8 깨짐 복구.
- AI가 도움 준 내용: 문서 이동·링크 일괄 수정·커밋 메시지·merge 절차.
- 그대로 사용한 부분: 경로 rename, 링크 치환.
- 수정해서 사용한 부분: Hub DONE 승격 금지, 포함할 파일 범위, 인코딩 복구 시 PowerShell 쓰기 금지.

## 6. 발생 이슈

### 이슈 1 — 초기 깃반영에서 RTOS 누락

- 증상: study 이동 커밋 후 RTOS 파일이 빠져 있었다.
- 원인: 포함 파일 범위를 한 번에 못 맞췄다.
- 해결: `ee7e613`로 RTOS를 추가 커밋·merge했다.

### 이슈 2 — UTF-8 깨짐이 main에 들어갈 뻔함/들어감

- 증상: PowerShell 기본 인코딩으로 한글 md가 손상됐다.
- 원인: `Set-Content`/`WriteAllText` 기본 코드페이지.
- 해결: Python `Path.write_bytes(utf-8)`로 복구하고, 이후 워크로그/문서 쓰기에 동일 규칙을 적용했다.

### 이슈 3 — 문서 작업으로 Hub DONE을 올리면 안 됨

- 증상: WBS 문서가 정리되면 완료율처럼 보일 수 있다.
- 원인: 문서 정합과 기능 DoD를 혼동하기 쉽다.
- 해결: DONE/PASS 점검 문서와 워크로그에 “문서 ≠ DONE”을 명시했다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| WBS 정본 | `docs/wiki/wbs.md` | START_HERE · status-notes 링크 |
| study 이동 | `docs/study/ai-review/**` | guides·asak-study 경로 |
| RTOS | `docs/study/RTOS/RTOS.md` | 해당 파일 UTF-8 |
| 원격 | merge `f23bae5` / `92aea1c` 포함 | `origin/main` |
| Hub 상태 | 이 작업만으로 DONE 일괄 승격 없음 | DevCopilot WBS |

## 8. 이번 작업에서 배운 점

1. 일정 문서는 파일이 여러 개일수록 “어느 것이 정본인지”가 팀 혼선의 원인이 된다.
2. 학습 산출물을 운영 보고서 폴더에 두면 검색·동기화 범위가 계속 오염된다.
3. Windows에서 한글 문서는 쓰기 API를 고정하지 않으면 git 이력 자체를 오염시킨다.
4. 문서 정리와 기능 완료 판정은 워크로그에서 문장으로 분리해야 한다.

## 9. 개선사항 / TODO

- [ ] Notion/Hub wiki와 로컬 `wbs.md` 재대조(필요 시)
- [ ] 워크스페이스 `.cursor/skills/asak-study` 경로 수정분 깃반영 여부 확정
- [ ] 회의록 참고 문서·워크로그 링크가 `wbs.md`를 가리키는지 주기 점검
- [ ] RTOS 노트와 키오스크 장치 연동 범위의 학습→구현 연결 고리 보강

## 10. 검증 내용

- 실행한 명령어:
  - `git show --stat` (`2b6b201`, `b5ebf9b`, `ee7e613`)
  - 경로 grep·`git diff --check`
- 테스트한 시나리오:
  - 문서 존재·링크·원격 main 포함 여부
  - 기능 E2E/Hub DONE 변경은 **미실행·미수행**
- 확인 결과:
  - WBS 정본·study 이동·RTOS 추가가 main에 반영됐다.
  - 인코딩 복구·워크로그 보강은 후속 커밋으로 이어졌다.

## 11. 포트폴리오용 요약

ASAK 문서 저장소에서 WBS를 단일 정본으로 모으고, 공부 레포트를 `study/ai-review`로 분리한 뒤 RTOS 학습 노트를 추가했다. 원격 main 반영까지 마쳤지만 Hub 완료 상태 변경이나 기능 검증으로 과장하지 않았다.

## 12. 첨부하면 좋은 자료

- 일일: [2026-08-07 daily](../../daily/이하진/2026-08-07.md)
- WBS: `docs/wiki/wbs.md`
- study: `docs/study/ai-review/`
- RTOS: `docs/study/RTOS/RTOS.md`
- 커밋: `2b6b201`, `b5ebf9b`, `ee7e613`
