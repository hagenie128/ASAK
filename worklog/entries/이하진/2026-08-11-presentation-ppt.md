# 2026-08-11 발표 PPT·화면 캡처·작성계획

> **일일 기록:** [2026-08-11 daily](../../daily/이하진/2026-08-11.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-11
- 담당자: 이하진
- 저장소: `ASAK`
- 브랜치: `docs/presentation-ppt` → `main` (`3567fc6`)
- 관련 이슈/PR: Issue 없음
- 작업 유형: `docs`
- 구현 근거: `0c674f0` · merge `3567fc6` · `HEAD == origin/main`
- Figma 기준: 발표용 화면 캡처는 앱 스크린샷 기준. Figma Frame 대조는 안 함 → `Figma 미확인`
- 완료 판정: **docs 트리에 pptx·스크린샷·스크립트·작성계획 반영**. 발표 리허설·팀 문구 확정·워크스페이스 상위 포인터 커밋은 미완.

## 2. 작업 목적

- 결과보고서/발표용 PPT 수정본과 Kiosk·Admin 화면 증거를 `docs/00_presentation`에 모은다.
- 캡처·주입 스크립트를 남겨 재실행 가능하게 한다.

## 3. 직접 구현 영역

커밋 `0c674f0`에서 확인:

- pptx 수정본 3개 (`수정1`~`수정3_20260811`)
- screenshots: kiosk home/list/detail/cart/payment, admin liveOrders/orders/menus
- `capture_screens.mjs`, `inject_screens_to_ppt.py`, `patch_ppt_v2.py`, `package.json`
- `ASAK_PPT_작성계획_초안.md` 대량 갱신, `docs/00_presentation/README.md` 갱신

로컬(미커밋):

- `ASAK/.gitignore`에 `docs/00_presentation/00_ppt/node_modules/` 추가
- 상위 `ASAK-workspace` 루트 PPT 초안 수정·서브모듈 SHA 미커밋

## 4. 구현 로직 / 적용한 방식

- Playwright 등으로 화면 캡처 → Python으로 pptx에 주입하는 파이프라인.
- 작성계획은 “구현·시연 가능한 것만 주장” 톤으로 정리(커밋된 md 기준).

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (co-authored-by)
- 요청: PPT 캡처·작성계획 반영 및 깃반영
- AI 도움: 스크립트·문서 초안
- 사람이 남긴 부분: 미커밋 workspace 상태와 발표 확정 전 구간 분리

## 6. 발생 이슈

### 이슈 1 — 하위 저장소 main ≠ 워크스페이스 포인터

- 증상: ASAK 등 하위는 origin/main과 일치해도 `ASAK-workspace`는 서브모듈 포인터가 이전 SHA.
- 해결: 워크로그에 상위 미커밋으로 기록. 이번 퇴근에서 상위 push/커밋하지 않음(스킬 금지).

### 이슈 2 — ppt node_modules

- 증상: 캡처용 npm 설치물이 untracked로 남을 수 있음.
- 해결: `.gitignore` 로컬 추가(미커밋).

## 7. 디버깅 기록

| 확인 항목 | 사실 | 다음 |
|---|---|---|
| ASAK remote | `3567fc6` | `docs/00_presentation` |
| workspace | 서브모듈 M, 루트 PPT 수정 | 별도 깃반영 요청 시 |

## 8. 이번 작업에서 배운 점

1. 발표 자산은 하위 docs 저장소와 상위 workspace 포인터를 따로 관리해야 한다.
2. 스크린샷은 “구현 증거”이지 “E2E 통과”가 아니다.

## 9. 개선사항 / TODO

- [ ] 팀 문구·시연 범위 확정 후 덱 최종본
- [ ] workspace 서브모듈 포인터·gitignore 커밋 범위 확정
- [ ] node_modules 무시가 remote에 올라갔는지 확인

## 10. 검증 내용

- 커밋 파일 목록·원격 포함 확인.
- 발표 리허설·슬라이드별 팀 승인: 미실행.

## 11. 포트폴리오 요약

발표용 PPT 수정본과 Kiosk/Admin 화면 캡처·자동화 스크립트·작성계획을 ASAK docs에 반영하고 원격 main에 병합했다.

## 12. 연결된 기록

- [일일 2026-08-11](../../daily/이하진/2026-08-11.md)
