# DevCopilot 시나리오 일괄 입력 가이드

Notion `사용자 시나리오 데이터베이스`의 **SC-001 ~ SC-023** (23개)를 DevCopilot 형식으로 변환해 두었습니다.

대상 URL: https://devcopilot.ai.kr/workspace/2/scenarios

---

## 포함 파일

| 파일 | 설명 |
|------|------|
| `scenarios_import.json` | 23개 시나리오 전체 (DevCopilot 필드 매핑 완료) |
| `import_in_browser.generated.js` | 브라우저 콘솔에 붙여넣기용 (아래 생성 명령 실행 후) |
| `import_scenarios_playwright.py` | Playwright 자동 입력 스크립트 |
| `generate_browser_script.py` | JSON → 브라우저 JS 생성기 |

---

## 방법 A — 브라우저 콘솔 (가장 간단)

### 1. JS 파일 생성

```bash
python devcopilot/generate_browser_script.py
```

### 2. DevCopilot 접속

1. https://devcopilot.ai.kr/workspace/2/scenarios 로그인 (Admin)
2. **시나리오 목록** 탭이 보이는 상태에서 F12 → Console

### 3. 스크립트 실행

1. `devcopilot/import_in_browser.generated.js` 파일 내용 전체 복사
2. 콘솔에 붙여넣고 Enter
3. 아래 중 하나 실행:

```javascript
importAllScenarios()   // 23개 전체
importMvpOnly()       // MVP 10개만
```

---

## 방법 B — Playwright 자동화 (반복 입력에 유리)

### 1. 설치

```bash
pip install playwright
playwright install chromium
```

### 2. 로그인 세션 저장 (최초 1회)

```bash
python devcopilot/import_scenarios_playwright.py --login
```

브라우저가 열리면 직접 로그인 후, 터미널에서 Enter.

### 3. 일괄 입력

```bash
# 전체 23개
python devcopilot/import_scenarios_playwright.py

# MVP만 (10개)
python devcopilot/import_scenarios_playwright.py --mvp-only

# 중간부터 재시작 (예: 6번째부터)
python devcopilot/import_scenarios_playwright.py --start 5
```

---

## MVP vs 이후 확장 구분

### 10일 MVP 우선 (권장: 먼저 입력)

| ID | 제목 |
|----|------|
| SC-001 | 신규 고객의 기본 주문 흐름 |
| SC-002 | 재방문 고객의 빠른 주문 |
| SC-003 | 품절 옵션 포함 주문 |
| SC-004 | 결제 성공 흐름 |
| SC-005 | 결제 실패 흐름 |
| SC-007 | 관리자 옵션 품절 처리 |
| SC-008 | 관리자 주문 상태 관리 |
| SC-009 | 장바구니 수정 |
| SC-012 | 자동 초기화 (타임아웃) |
| SC-014 | 매장/포장 선택 |

### 이후 확장

SC-006 (멤버십), SC-010~011 (알레르기/재료제외), SC-013 (접근성), SC-015~016 (영수증/QR), SC-017~018 (관리자 메뉴/매출), SC-019~023 (부하/드레싱/토핑/주문서/API 성능)

---

## DevCopilot 필드 매핑

| DevCopilot | JSON 키 |
|------------|---------|
| 시나리오 ID | `scenarioId` |
| 시나리오 제목 | `title` |
| 시작 조건 | `preCondition` |
| 종료 조건 | `postCondition` |
| 기본 흐름 | `normalFlow` |
| 예외 흐름 | `alternativeFlow` |
| Mermaid 스크립트 | `mermaid` |
| 상태 | `status` (`DRAFT` / `APPROVED`) |

---

## 주의사항

- DevCopilot은 **Admin 로그인**이 필요합니다. 에이전트가 대신 로그인할 수 없어 자동화 스크립트를 제공합니다.
- 폼 UI가 바뀌면 `추가` / `저장` 버튼 셀렉터를 수정해야 할 수 있습니다.
- 중간에 실패하면 `--start N` 또는 콘솔에서 해당 인덱스부터 다시 실행하세요.
- 이미 등록된 시나리오 ID가 있으면 중복될 수 있으니, 목록을 먼저 확인하세요.
