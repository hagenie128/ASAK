# 노트북 이어서 작업 — 핸드오프 (2026-07-18)

> **에이전트/사람 공통:** 이 문서를 먼저 읽고 `이어서` 명령을 실행한다.  
> 대답을 기다리지 말고, 아래 **다음 할 일**부터 진행한다.

## 한 줄 상태

Figma **0718** 수치 FAIL은 대부분 반영됨 → 코드는 **SCR-003 메뉴 목록 / SCR-004 상세**까지 손댐 → **다음은 SCR-005 장바구니**.

| 항목 | 값 |
| --- | --- |
| Figma 쓰기 전용 | `yHhvn5RKjBd91U8BJUQz7F` (0718) |
| Brand Primary | `#B5E30F` (쑥색 `#5DA45D` / Blue `#0088FF` 금지) |
| 문서 정본 | `ASAK/docs/design/0718.md` |
| 구현 입구 | `ASAK/docs/implementation_guide/00_START_HERE.md` |
| 가격/수량 단일 기준 | `ASAK-Kiosk/src/utils/priceCalculation.js`, `quantityLimits.js` |
| 브랜치 (문서) | `ASAK` → `handoff/0718-to-kiosk-continue` |
| 브랜치 (키오스크) | `ASAK-Kiosk` → `handoff/0718-to-kiosk-continue` |

## 절대 규칙

1. Figma **쓰기 = 0718만**. 0714/0715/ASAK-1은 읽기 참고.
2. Figma AI로 **hex → Semantic 일괄 재바인딩 다시 하지 말 것**.
3. Admin Dashboard 12~13px·끊긴 Icon/OrderRow는 **사람 판단** (일괄 16px 금지).
4. 커밋은 **하위 저장소별로** (`ASAK`, `ASAK-Kiosk` …). workspace 루트 `git add .`만으로 소스 전체가 안 올라간다.
5. `git push --force` / `reset --hard` / 광범위 삭제 금지.

## 이미 끝난 것 (다시 하지 말 것)

### Figma 0718
- BottomCTA lh 44 / loading 38 / radius 16
- Empty·Error·Modal·Cart·Option·MenuCard r24
- SCR-008 잔여 삭제·타이틀 클리핑·ReceiptCard lh
- Admin 쑥색→Brand Primary, MenuButton hit 48, StickyActionBar
- KEEP AUTO lh ≈ 0, SCR-001 LOGO → `ASAK LOGO` 인스턴스

### 코드 (ASAK-Kiosk)
- `useMenu` + MenuListPage Loading/Empty/Error
- EmptyState / ErrorMessage / LoadingSpinner
- tokens Brand `#B5E30F`, MenuCard r24, MenuListFooter BottomCTA형
- MenuDetailPage: 메뉴 없으면 ErrorMessage
- `npm run build` 통과 확인됨

## 다음 할 일 (우선순위)

1. **SCR-005 장바구니** (`ASAK-Kiosk/src/pages/kiosk/CartPage.jsx`)
   - 가이드: `02_KIOSK_IMPLEMENTATION.md` SCR-005
   - Empty / 삭제 확인 / 품절 차단 / `calculateCartTotal`·`quantityLimits` 유지
2. **홈(SCR-001)** Figma에 맞게 OrderType → `/menu` 흐름 다듬기 (선택)
3. **결제(SCR-007)** 라우트·페이지 연결 (아직 KioskApp에 없음)
4. Backend API는 아직 mock — `GET /api/kiosk/menuList` 목표 계약만 문서에 있음. 실제 연결은 백엔드 준비 후.

## 노트북에서 에이전트에게 붙일 첫 말

```text
이어서

핸드오프: ASAK/docs/handoff/LAPTOP_CONTINUE_2026-07-18.md
브랜치: handoff/0718-to-kiosk-continue
다음: SCR-005 장바구니부터. Figma는 0718만 쓰기. bulk rebinding 금지.
```

또는 단축: **`이어서`** (이 문서를 열라고 하면 됨)

## 셋업 명령 (Windows PowerShell)

### 0) 사전 설치
- Git, Node.js 20 LTS, Cursor **또는** VS Code
- (백엔드 할 날만) JDK 17+, 해당 IDE Java 확장

### 1) 클론 / 최신화

```powershell
# 처음이면
git clone https://github.com/hagenie128/ASAK-workspace.git C:\ASAK-workspace
cd C:\ASAK-workspace

# 이미 있으면
cd C:\ASAK-workspace
git fetch origin
git pull
```

하위 저장소는 **각각** pull + 브랜치 checkout:

```powershell
cd C:\ASAK-workspace\ASAK
git fetch origin
git checkout handoff/0718-to-kiosk-continue
git pull

cd C:\ASAK-workspace\ASAK-Kiosk
git fetch origin
git checkout handoff/0718-to-kiosk-continue
git pull
```

### 2) 키오스크 실행

```powershell
cd C:\ASAK-workspace\ASAK-Kiosk
npm install
npm run dev
```

빌드 확인:

```powershell
npm run build
npm run lint
```

### 3) 관리자 / 백엔드 (필요할 때만)

```powershell
cd C:\ASAK-workspace\ASAK-Admin
npm install
npm run dev

cd C:\ASAK-workspace\ASAK-back
.\gradlew.bat bootRun
```

### 4) Cursor / VS Code로 열기

```powershell
# Cursor
cursor C:\ASAK-workspace

# 또는 VS Code
code C:\ASAK-workspace
```

워크스페이스 루트 `C:\ASAK-workspace`를 연다. (하위 폴더만 열면 규칙·공통 설정이 빠질 수 있음)

## Cursor ↔ VS Code 설정 동일하게

레포에 넣은 **워크스페이스 설정**이 기준이다. 두 앱 모두 `.vscode/`를 읽는다.

| 파일 | 역할 |
| --- | --- |
| `.vscode/settings.json` | 에디터·포맷·검색 제외 공통 |
| `.vscode/extensions.json` | **꼭 필요한 확장만** 추천 (불필요 확장 최소화) |

### 확장 설치 (한 번에)

1. 워크스페이스 열기
2. 알림 **“권장 확장 설치”** → Install  
   또는 명령 팔레트: `Extensions: Show Recommended Extensions`
3. **이 목록에 없는 확장은 설치하지 않아도 됨** (예전에 권장이 과해서 안 깔아도 됨 — 맞음)

최소 권장:
- ESLint
- Prettier
- EditorConfig

백엔드 작업할 때만 (선택):
- Extension Pack for Java (`vscjava.vscode-java-pack`) — **평소엔 생략 OK**

### 개인 설정 동기화 (선택)

- Cursor / VS Code 각각 **Settings Sync** 켜기 (같은 GitHub 계정 권장)
- 팀 공통은 무조건 `.vscode/` (이 레포)가 우선

## Figma MCP (노트북에서도)

- 파일: 0718만 write
- KEEP: `✅ KEEP — Code Core` / `✅ KEEP — Admin Code Core`
- 검수 프롬프트·결과: `ASAK/docs/design/0718.md`

## 관련 문서

| 문서 | 용도 |
| --- | --- |
| [0718.md](../design/0718.md) | Figma FAIL 진행 로그 |
| [00_START_HERE.md](../implementation_guide/00_START_HERE.md) | 화면별 구현 입구 |
| [한국어_명령어_표](../../../한국어_명령어_표.md) | `이어서` `주문` `가격` 등 |
| [SETUP_EDITOR.md](../../../SETUP_EDITOR.md) | 에디터·확장 요약 (워크스페이스 루트) |

## 커밋/푸시 시 기억

```powershell
# 문서 변경
cd C:\ASAK-workspace\ASAK
git add docs/
git commit -m "docs: ..."
git push -u origin HEAD

# 키오스크 코드
cd C:\ASAK-workspace\ASAK-Kiosk
git add src/
git commit -m "feat(kiosk): ..."
git push -u origin HEAD
```
