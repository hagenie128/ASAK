# ASAK AI 스킬 및 코드 그래프 사용 가이드

> 상태: **Current** · 갱신: 2026-07-24
> 제품·API·화면의 정본은 [Product Bible](../product_bible/product-bible-hub.md)과 Screen Bible이다. 이 문서는 AI 도구를 언제 어떤 범위에서 사용할지 정한다.

> **바로 쓰는 요청문:** 기존 ASAK 스킬별 짧은 복사·붙여넣기 예시는 [13-ai-skill-prompt-examples.md](13-ai-skill-prompt-examples.md)를 본다.
> **팀원 설치:** 다른 PC에서 스킬·코드 그래프를 설치할 때는 [14-team-ai-tools-setup.md](14-team-ai-tools-setup.md)를 따른다.

## 1. 기본 원칙

- AI는 팀원의 구현을 대신하지 않는다. 분석, 질문, 코드 리뷰, 오류 원인 추적, 테스트 항목과 인수인계를 돕는다.
- 시작 전 Screen ID, Figma Frame/Node, Default·Loading·Empty·Error 상태, 화면 이동, 데이터 필드, 재사용 컴포넌트를 확인한다.
- AI 요청에는 `코드 수정하지 마`, `파일 생성하지 마` 또는 승인된 수정 범위를 함께 적는다.
- 자동 생성 코드·문서·Git 변경은 팀원이 검토한 뒤에만 반영한다. AI가 commit, push, merge, branch를 만들게 하지 않는다.

## 2. 공통 공학 스킬

| 스킬 | 설치 대상 | 사용할 때 | ASAK 안전 요청 |
|---|---|---|---|
| `grill-with-docs` | Codex, Claude Code, Cursor, Antigravity | 구현 전 요구사항·용어·예외 확정 | `질문과 체크리스트만 작성해. 코드·문서 파일은 수정하거나 만들지 마.` |
| `grilling` | Codex, Claude Code, Cursor, Antigravity | `grill-with-docs` 의존 / 질문만 필요할 때 | `한 번에 질문 하나씩. 코드·문서 파일은 만들지 마.` |
| `domain-modeling` | Codex, Claude Code, Cursor, Antigravity | `grill-with-docs` 의존 / 용어·결정 정리 | `채팅에만 용어·결정을 정리해. CONTEXT.md·ADR 파일은 만들지 마.` |
| `diagnosing-bugs` | Codex, Claude Code, Cursor, Antigravity | 오류·실패·성능 저하 원인 추적 | `재현·근거·원인 후보만 정리해. 명령 실행이나 코드 수정은 하지 마.` |
| `handoff` | Codex, Claude Code, Cursor, Antigravity | 세션·작업 인수인계 | `채팅에만 확인됨·미확인·다음 파일을 정리해. handoff 파일은 만들지 마.` |

`grill-with-docs`는 내부적으로 `grilling` + `domain-modeling`을 호출한다. **세 개를 함께 설치**해야 한다. 의존 스킬 없이 `grill-with-docs`만 있으면 동작하지 않는다. 설치 명령은 [14-team-ai-tools-setup.md](14-team-ai-tools-setup.md)를 따른다.

`diagnosing-bugs`는 설치 도구의 외부 보안 평가에서 High Risk 표시가 있었다. 이 스킬은 **진단 전용**으로 사용하며, 자동 수정·파일 생성·명령 실행을 허용하지 않는다.

`handoff` / `grill-with-docs`는 수동 호출용(`disable-model-invocation`)이라 에이전트가 자동으로 고르지 않는다. 필요할 때 `/grill-with-docs`, `/handoff`로 직접 호출하거나, 요청문에 스킬 이름을 적는다.

## 3. 코드 그래프

`code-review-graph`는 Git 추적 코드의 호출·의존 관계를 만들어 AI가 우선 읽을 파일을 좁히는 도구다. Product Bible, Screen Bible, Figma의 정본 여부나 문구·상태 정책을 대신 판단하지 못한다.

| 저장소 | 그래프 결과 | 그래프 DB |
|---|---:|---|
| `ASAK-Admin` | 85개 파일 · 297개 노드 · 1,760개 관계 | `C:\ASAK-workspace\.code-review-graph-data\ASAK-Admin` |
| `ASAK-Kiosk` | 80개 파일 · 167개 노드 · 533개 관계 | `C:\ASAK-workspace\.code-review-graph-data\ASAK-Kiosk` |
| `ASAK-back` | 48개 파일 · 150개 노드 · 341개 관계 | `C:\ASAK-workspace\.code-review-graph-data\ASAK-back` |

그래프는 Git 추적 파일만 읽는다. `ASAK-back`처럼 미추적 파일이 있으면 추가·커밋되기 전에는 그래프에 포함되지 않는다. 문서 중심 `ASAK` 저장소는 코드 의존 그래프 효용이 낮아 적용하지 않는다.

| 도구 | MCP 연결 위치 | 사용 범위 |
|---|---|---|
| Codex | 사용자 Codex 설정의 `code-review-graph`, `code-review-graph-kiosk`, `code-review-graph-back` | Admin·Kiosk·Backend |
| Claude Code | 각 저장소의 `.mcp.json` | Admin·Kiosk·Backend |
| Cursor | 각 저장소의 `.cursor/mcp.json` | Admin·Kiosk·Backend |
| Antigravity | 사용자 Antigravity MCP 설정의 세 서버 | Admin·Kiosk·Backend |

## 4. 작업 순서

```text
정본·Figma 확인
  → grill-with-docs: 빠진 조건 질문
  → code-review-graph: 읽을 관련 파일과 영향 범위 찾기
  → 팀원이 직접 구현
  → diagnosing-bugs: 오류 원인과 증거 확인
  → 팀원이 직접 수정·테스트
  → handoff: 채팅용 작업 인수인계 정리
```

## 5. 기존 ASAK 보조 스킬

| 주제 | 스킬 | 예시 요청 |
|---|---|---|
| API 계약·연결 | `asak-api` | `API 연결을 수정하지 말고 요청·응답 필드와 상태를 비교해줘.` |
| React 구조·컴포넌트 | `asak-react-review` | `React 화면 흐름과 재사용 컴포넌트만 점검해줘.` |
| Figma 화면 QA | `asak-figma-review` | `SCR-009 Figma와 코드의 상태·문구 차이만 찾아줘.` |
| 백엔드/Spring | `asak-backend-review` | `백엔드 API 구현 순서와 영향 파일만 설명해줘.` |
| DB·스키마 | `asak-db` | `DB 필드와 DTO 매핑만 검토해줘.` |
| 버그 원인 | `asak-debug` 또는 `diagnosing-bugs` | `버그 원인과 재현 절차만 알려줘.` |
| 주문·가격·수량 | `asak-order-review`, `asak-price-review`, `asak-quantity-review` | `주문 상태 전이와 가격 계산 위험만 점검해줘.` |
| 테스트·QA | `asak-test-plan` | `Default·Loading·Empty·Error 테스트 항목만 작성해줘.` |
| 설명·학습 | `asak-explain` | `이 코드의 데이터 흐름을 초보자용으로 설명해줘.` |
| 오늘 작업·이어가기 | `asak-today`, `asak-continue`, `handoff` | `오늘 확인한 것과 다음 파일을 채팅에만 정리해줘.` |

## 6. 바로 쓰는 프롬프트

### 구현 전

```text
SCR-009 작업 전 정본을 확인해줘.
Product Bible, Screen Bible, Figma Frame/Node, 기존 React 구조를 읽고
Screen ID, 상태(Default·Loading·Empty·Error), 데이터 필드, 재사용 컴포넌트,
미확인 질문만 표로 정리해. 코드·문서 파일은 수정하거나 만들지 마.
```

### 큰 저장소에서 관련 파일 찾기

```text
ASAK-Admin에서 code-review-graph로 이번 변경의 영향 범위를 분석해줘.
먼저 읽어야 할 파일, 호출/의존 관계, 관련 테스트만 보여줘.
정본 문서와 Figma는 별도 근거로 구분하고 코드 수정은 하지 마.
```

### 오류 원인만 찾기

```text
이 오류를 diagnosing-bugs 방식으로 분석해줘.
재현 조건, 확인한 파일과 로그, 원인 후보, 다음 확인 명령만 제시해.
파일 수정, 자동 수정, Git 명령은 실행하지 마.
```

### 작업 인수인계

```text
이번 작업을 handoff 형식으로 채팅에만 정리해줘.
확인됨, 미확인, 수정한 파일(팀원 직접 구현 여부 포함), 테스트 결과,
다음 담당자가 볼 첫 파일을 300자 안팎으로 작성해. 파일을 만들지 마.
```

## 7. 시작 전 체크

- AI 도구를 재시작해 새 MCP·스킬을 불러온다.
- 작업 대상에 맞는 Admin·Kiosk·Backend 그래프 서버를 선택한다.
- Figma·Screen Bible·Product Bible을 먼저 읽게 하고, 그래프 결과만으로 구현 결정을 내리지 않는다.
- 실제 수정은 팀원이 직접 수행하고, AI는 그 뒤 코드 리뷰와 테스트 항목 확인에 사용한다.
