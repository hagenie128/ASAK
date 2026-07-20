# 2026-07-17 구현 가이드·기능 매트릭스·자산 기준 작성 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-17.md](../../daily/이하진/2026-07-17.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-17
- 담당자: 이하진
- 저장소: ASAK
- 브랜치: `docs/notion-web-audit-v1`
- 관련 이슈/PR: PR #8 Frontend 80% Plan Draft
- 작업 유형: `docs` / `design`

## 2. 작업 목적

- Product Bible·Figma·현재 코드의 정보를 실제 구현자가 화면·기능 단위로 찾고 실행할 수 있는 가이드와 체크리스트로 전환한다.

## 3. 직접 구현 영역

- `docs/implementation_guide/`에 시작점, 고정 규칙, Kiosk/Admin, API·DB, UI 컴포넌트, QA·릴리스, 확장 화면, 기능 매트릭스, Figma 상태 체크리스트, 전체 기능 찾기 문서를 추가했다.
- SCR-001~024를 기능·API/데이터·상태/예외·우선 확인 문서에 연결하고, MVP와 Future Scope를 구분했다.
- 메뉴·재료 이미지, 아이콘, 카탈로그, 매핑·미리보기와 관련 스크립트/seed 자산을 추가해 화면에서 사용할 자산 식별 기반을 마련했다.

## 4. 구현 로직 / 적용한 방식

- `00_START_HERE`를 문서 진입점으로 두고, `FEATURE_LOOKUP`에서 작업 목적별 가이드·Screen ID·정본 문서를 바로 찾을 수 있게 했다.
- 기능 매트릭스는 “화면을 만들었다”가 아니라 핵심 행동, API/데이터 기준, Loading/Empty/Error/Disabled·품절 등 예외 상태까지 함께 보도록 구성했다.
- Figma 상태 체크리스트는 Kiosk·Admin 화면별 Default뿐 아니라 처리 중, 오류, 빈 상태, 부분 데이터, 품절·재시도 상태를 빠뜨리지 않도록 작성했다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex, ChatGPT
- 어떤 질문/요청을 했는지: 방대한 Product Bible과 현재 구현 맵을 개발자가 실행할 문서 목차·매트릭스·체크리스트로 바꾸는 구조 초안을 요청했다.
- AI가 도움 준 내용: 화면→기능→API/상태→QA로 이어지는 문서 연결, 누락하기 쉬운 상태 목록, 가이드 파일의 역할 분리를 제안했다.
- 그대로 사용한 부분: Screen ID, 현재 구현 맵의 상태, Product Bible의 계약 문서 경로, 자산 파일명·ID 매핑처럼 저장소에서 확인되는 사실.
- 수정해서 사용한 부분: 구현 우선순위, Future Scope 제외, 팀 작업 순서, 문서 간 링크와 설명 문구는 직접 검토해 정리했다.

## 6. 발생 이슈

- 이슈 1:
  - 증상: 문서와 화면이 많아 구현자가 필요한 규칙·API·QA 항목을 찾기까지 시간이 오래 걸림.
  - 원인: 정본 문서가 도메인별로 분리되어 있고, 현재 코드의 미구현/부분 구현 상태가 한 화면에서 보이지 않음.
  - 해결: 시작점·전체 찾기·기능 매트릭스·Figma 상태 체크리스트를 추가해 탐색 경로를 표준화했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: 현재 구현 맵에서 Cart/Payment/Complete, 다수 Admin 화면, Backend business endpoint가 아직 MISSING/PARTIAL임을 확인했다.
- 의심했던 지점: 가이드에 적힌 API나 화면이 이미 구현된 것으로 오해될 수 있는지, 확장 화면을 MVP 구현 범위로 오인할 수 있는지.
- 실제 원인: 구현 계획 문서와 실제 코드 상태가 별도 문서에 있었기 때문.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: `00_START_HERE.md`, `FEATURE_LOOKUP.md`, `08_FEATURE_IMPLEMENTATION_MATRIX.md`, `09_FIGMA_STATE_CHECKLIST.md`, `CURRENT_IMPLEMENTATION_MAP.md`.

## 8. 이번 작업에서 배운 점

- 구현 가이드는 설명서가 아니라 선택을 줄이는 도구여야 한다. 화면마다 필요한 정본·데이터·상태·테스트를 같이 제시해야 한다.
- 이미지 파일을 많이 추가하는 것보다 ID·카탈로그·매핑이 없으면 실제 화면 연결에서 다시 수작업과 오류가 생긴다.

## 9. 개선사항 / TODO

- 실제 Vertical Slice 구현이 시작되면 가이드의 모든 API·파일 경로·상태를 코드와 함께 갱신한다.
- 이미지/아이콘의 라이선스·출처·상업적 사용 가능 여부와 메뉴·재료 ID 매핑을 팀이 최종 확인한다.
- 확장 화면(SCR-023/024)은 MVP 범위와 API 계약이 확정되기 전까지 구현 완료로 표시하지 않는다.

## 10. 검증 내용

- 실행한 명령어: Git 커밋·변경 파일 확인 및 구현 가이드 상호 링크 검토.
- 테스트한 시나리오: Kiosk 메뉴/옵션/Cart/결제, Admin 주문/품절/매출, API·DTO·DB, QA·릴리스, Figma 상태를 각각 찾을 때 출발 문서가 있는지 확인.
- 확인 결과: 2026-07-17 커밋 `bac0c6e`에서 구현 가이드 10종 이상, 기능 매트릭스, 상태 체크리스트, 자산 카탈로그·매핑이 추가된 것을 확인했다. 런타임·이미지 렌더링 테스트는 이번 문서 작업에서 다시 실행하지 않았다.

## 11. 포트폴리오용 요약

Product Bible과 Figma 설계를 실제 개발자가 바로 실행할 수 있도록 화면·기능·API·상태·QA를 연결한 구현 가이드와 자산 매핑 체계를 만들었다.

## 12. 첨부하면 좋은 자료

- [구현 가이드 시작점](../../../docs/implementation_guide/00_START_HERE.md)
- [전체 기능 찾기](../../../docs/implementation_guide/FEATURE_LOOKUP.md)
- [기능 구현 매트릭스](../../../docs/implementation_guide/08_FEATURE_IMPLEMENTATION_MATRIX.md)
- [Figma 상태 체크리스트](../../../docs/implementation_guide/09_FIGMA_STATE_CHECKLIST.md)
