# 2026-07-20 문서 정본 재편·코드 실태 재감사·DevCopilot WBS2 재동기화

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-20.md](../../daily/이하진/2026-07-20.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-20
- 담당자: 이하진
- 저장소: ASAK (모노레포 docs) / ASAK-Kiosk / ASAK-Admin / ASAK-back
- 브랜치: `main`
- 관련 이슈/PR: WBS2-017, WBS2-022, WBS2-023 (DONE 반영) · 이슈/PR 없음(로컬 문서 + DevCopilot MCP)
- 작업 유형: `docs` / `audit` / `mcp`

## 2. 작업 목적

- 7/16 문서 정리(`f9349ba`, `671e486`) 이후 문서만 보고 진행률을 판단하면 실제 코드 상태와 어긋날 위험이 있어, **코드를 1차 정본**으로 다시 확인한다.
- Kiosk·Admin·Backend 3개 저장소의 실제 구현 범위를 재확인하고, 그 결과를 로컬 문서와 DevCopilot workspace/2 양쪽에 일관되게 반영한다.
- 문서 진입 구조가 여러 위치에 흩어져 있던 문제를 `START_HERE`/`PROJECT_HUB` 단일 진입점으로 정리한다.

## 3. 직접 구현 영역

- **문서 정본 구조:** `docs/START_HERE.md`, `PROJECT_HUB.md`, `docs/DOCUMENT_NAMING.md`, `docs/DOC_INVENTORY_SLIM.md`, `docs/product_bible/README.md` 신규 작성.
- **코드 실태 반영 문서:** `docs/planning/CURRENT_IMPLEMENTATION_MAP.md`, `docs/architecture/DOCUMENT_CODE_GAP_REPORT.md`, `docs/wiki/wbs-status-notes.md`, `docs/wiki/current-status-baseline.md`, `docs/wiki/wbs-v2.md`, `docs/wiki/screens.json` 갱신.
- **앱별 구조 문서:** `ASAK-Kiosk/src/STRUCTURE_GUIDE.md`, `ASAK-Admin/src/STRUCTURE_GUIDE.md`, `ASAK-Kiosk/IMPLEMENTATION_PLAN.md`, `ASAK-Admin/IMPLEMENTATION_PLAN.md`, `ASAK-back/IMPLEMENTATION_PLAN.md` 갱신.
- **루트 안내:** `README.md`, `ASAK/README.md`, `UI-INDEX.md` 상단에 `START_HERE` 링크·코드-정본 안내 배너 추가.
- **DevCopilot MCP:** WBS2-001~066 제목 한글화, WBS2-017/022/023 상태 `DONE` 반영, LMIS 요구사항 8건 `IN_PROGRESS` 반영, SCR-020~024 정의 정리, Target API 4건 신규 create.
- **동기화 보고서:** `docs/wiki/devcopilot-sync-report.md`에 Before/After 표, API mismatch record, Dashboard 재계산, Safety controls 기록.

## 4. 구현 로직 / 적용한 방식

- **정본 우선순위 고정:** "코드 → Canonical/Product Bible → DevCopilot → 구 문서" 순서를 문서화하고, 이번 재감사부터 이 순서로 확인했다. 문서에 쓰여 있어도 코드 evidence가 없으면 DONE으로 인정하지 않았다.
- **DONE 판정 기준 명확화:** 정적 UI만 있으면 `IN_PROGRESS`, 실제 동작하는 코드·mock evidence가 있어야 `DONE`. 예: Kiosk 라우트 10개 연결(WBS2-017)과 `quantityLimits` 코드로 확인되는 수량 9/장바구니 30 제한(WBS2-022·023)은 DONE, Admin 정적 화면(WBS2-034~043)은 mock repository는 준비돼 있지만 Page 연동이 0건이라 IN_PROGRESS로 유지.
- **비파괴 원칙:** DevCopilot MCP가 API update/archive를 지원하지 않아 기존 레코드는 그대로 두고, 목표 경로는 `[TARGET]` 접두를 붙여 신규 create만 했다. Legacy WBS도 status/title 메모로만 표시하고 레코드 자체는 삭제하지 않았다.
- **대시보드 지표와 운영 지표 분리:** DevCopilot 대시보드가 노출하는 WBS 진행률 공식(분모에 EXCLUDED 포함)은 그대로 두고, 실행 추적용 별도 공식(`8 DONE / 72 Active = 11.1%`)을 로컬 문서에만 기록했다. 시스템 지표는 임의로 고치지 않았다.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (DevCopilot MCP 연동)
- 어떤 질문/요청을 했는지: 저장소별(Kiosk/Admin/back) 실제 라우트·컴포넌트·mock repository·API 엔드포인트를 코드에서 스캔하고, WBS2 상태를 코드 근거와 대조해 재조정하도록 요청. DevCopilot MCP로 WBS/Requirements/Screens 조회 및 update 실행을 요청.
- AI가 도움 준 내용: 저장소 전체 스캔 결과 요약, 문서 경로 후보와 상호 링크 구조 제안, WBS2 상태 재조정 초안, DevCopilot MCP 호출 실행.
- 그대로 사용한 부분: 코드 스캔으로 확인된 사실(라우트 수, mock repository 존재 여부, API 엔드포인트 목록), WBS2 제목 한글화 결과.
- 수정해서 사용한 부분: DONE/IN_PROGRESS 판정 기준과 실제 상태 값, 문서 간 링크 구조와 우선순위 문구, Target API 표기 방식(`[TARGET]`).

## 6. 발생 이슈

- 이슈 1:
  - 증상: 문서(7/16 정리본) 기준으로는 여러 항목이 진행 중/완료로 보였으나, 코드를 직접 열어보니 Admin은 정적 UI만 연결되고 실제 데이터 연동이 0건이었다.
  - 원인: 문서가 마지막 갱신 시점의 스냅샷이라 이후 코드 변화(또는 애초에 정적 UI만 만든 상태)를 반영하지 못했다.
  - 해결: `CURRENT_IMPLEMENTATION_MAP.md`·`DOCUMENT_CODE_GAP_REPORT.md`를 코드 재스캔 결과로 갱신하고, WBS2 상태도 코드 evidence 기준으로 재조정했다.
- 이슈 2:
  - 증상: DevCopilot 대시보드의 WBS 진행률(%)이 실제 활성 작업 대비 지나치게 낮게 보였다(예: 5.4%).
  - 원인: 대시보드 계산 공식의 분모에 `EXCLUDED`(중복·보류) 레코드 다수가 포함되어 있었다.
  - 해결: 시스템 지표는 수정하지 않고, `EXCLUDED`를 제외한 운영용 공식(`DONE / Active`)을 별도로 계산해 `devcopilot-sync-report.md`에 남겼다.
- 이슈 3:
  - 증상: API 경로를 최신 목표 경로(`/api/kiosk/*` 등)로 갱신하려 했으나 DevCopilot MCP가 update/archive를 지원하지 않았다.
  - 원인: MCP capability 제한(`MCP_UNSUPPORTED`: native backup/export, 명시적 traceability-link mutation 등도 동일하게 미지원).
  - 해결: 기존 레코드를 유지한 채 목표 경로를 `[TARGET]` 접두 신규 레코드로 create하고, API mismatch record 표로 비교·의사결정 대기 상태를 명시했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: 없음 (MCP 호출은 정상 응답, 문제는 로그 에러가 아니라 "지원 범위" 확인 필요였음).
- 의심했던 지점: DevCopilot 대시보드 진행률이 실제 코드 상태보다 낮게/다르게 보이는 것이 우리 쪽 판정 오류인지, 시스템 계산 방식 문제인지 구분이 필요했다.
- 실제 원인: `legacy-wbs2-mapping-audit-2026-07-16.md`에서 이미 확인된 것처럼, EXCLUDED(중복·보류) 레코드가 분모에 포함되는 시스템 계산 방식 때문이었다 — 우리 판정 오류가 아니었다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어:
  - `ASAK/docs/wiki/devcopilot-sync-report.md` (Dashboard 재계산, MCP_UNSUPPORTED 섹션)
  - `ASAK/docs/wiki/wbs-v2.md` (실행 정본 표)
  - `ASAK/docs/wiki/wbs-status-notes.md` (코드 근거 요약)

## 8. 이번 작업에서 배운 점

- 문서 정리(링크·구조 재배치)와 내용 진위 확인(코드 재감사)은 서로 다른 작업이며, 전자만 하고 후자를 건너뛰면 문서가 "깔끔하지만 틀린" 상태가 될 수 있다.
- 외부 트래커(DevCopilot)의 대시보드 지표는 계산 공식이 노출되지 않으면 그대로 신뢰하지 말고, 근거를 확인할 수 있는 자체 지표를 별도로 유지해야 한다.
- MCP 도구의 capability 경계(`MCP_UNSUPPORTED`)를 먼저 확인해야 "왜 안 되는지"를 헤매지 않고 바로 우회 전략(비파괴 신규 create)을 선택할 수 있다.

## 9. 개선사항 / TODO

- 아직 임시 처리한 부분: API-002~006, API-009의 canonical path 결정이 `[TARGET]` create로만 남아 있고 팀 승인 전까지는 확정이 아니다.
- 다음 스프린트에서 개선할 부분: Admin `adminMockRepository`를 실제 Page(Dashboard/Orders/SoldOut/PaymentMethod)에 연동해 WBS2-034~043을 DONE으로 끌어올린다.
- 성능/구조적으로 아쉬운 부분: DevCopilot 대시보드 진행률 공식을 시스템 쪽에서 EXCLUDED 제외 옵션으로 제공하면 로컬 이중 계산이 필요 없어진다 (기능 요청 후보).

## 10. 검증 내용

- 실행한 명령어/도구 호출: DevCopilot MCP `update_wbs_task`(WBS2-001~066 제목·상태), `get_requirements`/`get_screens`(LMIS, SCR-020~024 확인), 코드 스캔(Kiosk `src/` 라우트, Admin `adminMockRepository`, Backend 엔드포인트).
- 테스트한 시나리오:
  - Kiosk Home → 메뉴 → 옵션 → 장바구니 흐름이 mock 데이터로 끝까지 이어지는지 확인.
  - Admin 화면에서 `adminMockRepository`의 데이터가 실제 화면에 반영되는지(=연동 여부) 확인.
  - Backend에서 `/api/health` 외 응답 가능한 엔드포인트가 있는지 확인.
  - DevCopilot workspace/2에서 WBS2-017·022·023이 `DONE`, LMIS 8건이 `IN_PROGRESS`로 표시되는지 확인.
- 확인 결과: Kiosk는 Home→장바구니 mock 동작 확인(결제/타임아웃은 shell), Admin은 Page 연동 0건 확인, Backend는 health 엔드포인트만 확인. DevCopilot 상태 갱신은 반영됨(대시보드 %는 EXCLUDED 포함 계산이라 별도 운영 공식으로 병기).

## 11. 포트폴리오용 요약

문서만 보고 진행률을 판단하지 않고 코드를 1차 근거로 재감사해, Kiosk·Admin·Backend의 실제 구현 범위를 확인하고 그 결과를 로컬 문서와 DevCopilot 원격 트래커 양쪽에 비파괴적으로 동기화했다. 신뢰할 수 없는 대시보드 지표 대신 근거 기반 운영 지표를 별도로 설계해 팀 의사결정에 쓸 수 있게 했다.

## 12. 첨부하면 좋은 자료

- [`docs/START_HERE.md`](../../../docs/START_HERE.md)
- [`docs/planning/CURRENT_IMPLEMENTATION_MAP.md`](../../../docs/planning/CURRENT_IMPLEMENTATION_MAP.md)
- [`docs/architecture/DOCUMENT_CODE_GAP_REPORT.md`](../../../docs/architecture/DOCUMENT_CODE_GAP_REPORT.md)
- [`docs/wiki/devcopilot-sync-report.md`](../../../docs/wiki/devcopilot-sync-report.md)
- [`docs/wiki/wbs-v2.md`](../../../docs/wiki/wbs-v2.md) · [`docs/wiki/wbs-status-notes.md`](../../../docs/wiki/wbs-status-notes.md)
- 오늘 일일 워크로그: [`daily/이하진/2026-07-20.md`](../../daily/이하진/2026-07-20.md)
