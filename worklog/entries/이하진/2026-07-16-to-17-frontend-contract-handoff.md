# 2026-07-16~17 프론트엔드 계약·Figma 핸드오프 정리

> **일일:** [2026-07-16](../../daily/이하진/2026-07-16.md) · [2026-07-17](../../daily/이하진/2026-07-17.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-16~17
- 담당자: 이하진
- 저장소: ASAK / ASAK-Kiosk / ASAK-Admin
- 브랜치: `main`
- 관련 이슈/PR: WBS2-017~045 / 후속 [Kiosk #5](https://github.com/hagenie128/ASAK-Kiosk/issues/5) · [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- 작업 유형: `docs` / `design-system`

## 2. 작업 목적

- Figma 정적 화면을 다시 제작하지 않고, 화면·라우트·mock·상태·WBS의 구현 기준을 저장소별로 확정한다.

## 3. 직접 구현 영역

- Figma Final 컴포넌트·상태 정책과 Product Bible·WBS·Notion P0 API/DTO/DB 기록을 대조했다.
- Kiosk·Admin 구현 계획과 요구사항 매핑의 링크·정본 관계를 보완했다.
- Kiosk 메뉴 상세의 draft/알레르기 표시 및 Admin 공통 스타일·구조를 정리해 이후 Figma 이식 작업의 기준을 맞췄다.
- 구현 가이드·자산 기준과 팀용 ASAK AI 스킬 설치 패키지의 Git 배포 상태를 정리했다.

## 4. 구현 로직 / 적용한 방식

- 가격은 `priceCalculation.js`, 수량은 `quantityLimits.js`를 단일 기준으로 유지했다.
- Kiosk는 `public/mocks/kiosk.json`, Admin은 mock repository를 이후 페이지 연결의 중간 계층으로 두는 방향을 유지했다.

## 5. AI 도움 영역

- 첫 요청:
  - Codex에게 최근 Git 커밋과 Figma 핸드오프·구현 계획 문서를 대조해, 정적 화면 이식 전에 어떤 계약이 먼저 정리돼야 하는지 추리게 했다.
- 1차 초안에서 부족했던 점:
  - 문서 정리와 실제 구현 계약이 한 문단에 섞여 있어, 무엇이 "정리 작업"이고 무엇이 "다음 구현의 기준"인지 흐렸다.
  - Kiosk와 Admin의 공통점은 보였지만 저장소별로 남은 연결 포인트가 충분히 분리되지 않았다.
- 수정 지시:
  - Figma 정본 링크, mock 연결 기준, WBS 우선순위를 따로 보이게 다시 정리하라고 했다.
  - "정적 UI 이식 전 준비"와 "이후 mock 연결 작업"을 같은 레벨에서 적지 말고 단계로 나누라고 피드백했다.
  - 팀 도구/가이드 정리는 문서 배치가 아니라 팀 재현성 관점에서 써 달라고 다시 요청했다.
- 최종적으로 사용한 부분:
  - 구현 계획과 Figma 핸드오프 사이의 연결 근거
  - Kiosk/Admin 공통 기준과 후속 연결 작업 분리
- 그대로 쓰지 않은 부분:
  - 추상적인 "구조 보완" 표현, 구체 근거 없이 넓게 잡힌 TODO

## 6. 발생 이슈

- 이슈 1:
  - 증상: Figma 화면은 준비됐지만 페이지별 mock·상태 연결 기준이 분산되어 있었다.
  - 원인: 정적 UI 이식과 실제 동작 연결 작업의 범위가 분리되어 있지 않았다.
  - 해결: 저장소별 구현 계획에 mock·상태·WBS 우선순위를 명시했다.

## 7. 디버깅 기록

- 확인한 근거: 7/16~17 Kiosk·Admin의 구현 계획/문서 갱신 및 컴포넌트·스타일 정리 커밋.
- 다시 같은 문제가 생기면 먼저 볼 파일: 각 저장소의 `IMPLEMENTATION_PLAN.md`, `docs/figma-ui-handoff.md`, `src/STRUCTURE_GUIDE.md`.

## 8. 이번 작업에서 배운 점

- 디자인 이식 완료와 사용자 흐름 완료를 구분하려면 mock·상태·검증 조건을 같은 문서에 적어야 한다.
- AI가 문서 후보를 잘 모아도, 사람이 "이 문서가 구현 계약인지 안내 문서인지" 성격을 다시 분류해 주지 않으면 기록이 금방 모호해진다.

## 9. 개선사항 / TODO

- Kiosk 결제·타임아웃·상태 UI와 Admin mock repository 페이지 바인딩을 구현한다.

## 10. 검증 내용

- 실행한 명령어: Git 로그와 구현 계획·Figma 핸드오프 문서 대조.
- 확인 결과: Kiosk와 Admin 모두 정적 UI 이후의 연결 작업이 별도 WBS로 남아 있음을 확인했다.

## 11. 포트폴리오용 요약

- Figma 화면을 단순 시안이 아니라 mock 데이터·상태·테스트 조건이 연결된 프론트엔드 구현 계약으로 정리했다.

## 12. 첨부하면 좋은 자료

- Kiosk·Admin `IMPLEMENTATION_PLAN.md`
- Kiosk `docs/figma-ui-handoff.md`
