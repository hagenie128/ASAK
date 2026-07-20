> Status: **Historical** (2026-07-20)  
> → **정본:** [figma-unified-corrective-execution-plan-2026-07-17.md](../figma-unified-corrective-execution-plan-2026-07-17.md)

# Figma 최소 패스 실행표 (100점 아님 · 코드 직전)

**날짜:** 2026-07-18  
**파일:** `JSrjOy668zhfkiLplCkreh`  
**목표:** 디자인 100점 금지. **아래 순서만** 하고 코드로 이동. 추후 QA 가정.  
**보는 곳:** 이 문서만. UNIFIED / FIX_PLAN 다시 읽지 말 것.

---

## 0. 역할 (이 표가 최종 · “나랑 하자” 거절용)

| 담당 | 쓰는 곳 | 모델 추천 | 맡기는 일 |
|---|---|---|---|
| **당신 (사람)** | Figma 앱 | — | override 리셋, Tap 교체, 최종 눈 확인 |
| **Cursor** | 이 채팅 / Agent | **Composer** 또는 기본 Agent | 목록·실측·한 컴포넌트 수정 지시문 |
| **Claude** | claude.ai 또는 Claude Code | **Sonnet** (빠르면) / **Opus**(막힐 때만) | Master 일괄·토큰/Blue 규칙 적용 |
| **Codex** | Codex CLI / ChatGPT | **codex** 기본 | hex 전수·9px 전수·체크 ☐만 (긴 에세이 금지) |
| **Figma MCP** | Cursor에서 Figma 연결 시 | — | **쓰기**는 배치당 1주제만 |

**금지:** A~E한테 각각 “전체 QA FINAL” 다시 시키기.

---

## 1. 실행 순서 (이 숫자·위치만)

### STEP 1 — SCR-008 CTA (당신 10분 · AI는 재실측만)

| 항목 | 값 |
|---|---|
| 위치 | Kiosk Screens · **SCR-008** · 프레임 `134:7926` |
| Master | BottomCTA `150:385` |
| As-Is | CTA **`940×200`** |
| To-Be | **`1080×180`** · override 제거 · Master 인스턴스 |
| 누가 | **당신** Figma에서 Reset/올바른 variant |
| AI에게 | Cursor에만 ↓ |

**Cursor에 복붙:**
```text
파일 JSrjOy668zhfkiLplCkreh
노드 134:7926 SCR-008 BottomCTA만
실측: 지금 W×H, radius, 텍스트 px
목표: 1080×180
쓰기 금지. PASS/FAIL 한 표만.
```

**PASS:** 실측 `1080×180`

---

### STEP 2 — Cart Blue 제거 (Claude 메인 · Codex 검증)

| 항목 | 값 |
|---|---|
| 위치 Master | CartItemCard `150:404` |
| 위치 화면 | SCR-005 Cart `134:7835` 근처 |
| 지울 hex | **`#3B82F6`**, **`#0088FF`** |
| To-Be | 브랜드/뉴트럴 (라임 선택·다크 텍스트). Blue 0건 |
| 액션 글자 | **≥16px** (여유 있으면 같이) |

**① Codex에 복붙 (목록만):**
```text
Figma 파일 JSrjOy668zhfkiLplCkreh
Kiosk CartItemCard + SCR-005만
#3B82F6 #0088FF 노드 ID·레이어명 표
쓰기 0. 다른 QA 하지 마.
```

**② Claude에 복붙 (수정):**
```text
파일 JSrjOy668zhfkiLplCkreh
Master CartItemCard 150:404 우선, 그다음 SCR-005 인스턴스
Blue #3B82F6 #0088FF 전부 제거 → Semantic/뉴트럴·브랜드만
액션 텍스트 13이면 16 이상
다른 화면 건드리지 마. 끝나면 남은 Blue 개수만.
```

**③ Cursor 검증:**
```text
SCR-005 + CartItemCard에서 #3B82F6 #0088FF 남은 개수.
0이면 PASS. 쓰기 금지.
```

**PASS:** Blue hex **0건**

---

### STEP 3 — CategoryTap → Tab (당신 메인 · Codex 검증)

| 항목 | 값 |
|---|---|
| 위치 화면 | SCR-003 Menu List `134:7792`+ |
| As-Is | **CategoryTap ×4** · Size s 약 **25×11** |
| To-Be | **CategoryTab만** · Tap Deprecated/인스턴스 0 |
| Tab 높이 | **52 유지** (64로 올리지 마 · 나중에 QA) |

**당신:** List 화면에서 Tap 인스턴스 → Tab으로 교체.

**Codex 복붙:**
```text
파일 JSrjOy668zhfkiLplCkreh
페이지 Kiosk Screens
이름에 CategoryTap 또는 Tap 인스턴스 개수
0이면 PASS. 쓰기 0.
```

**PASS:** Tap 인스턴스 **0**

---

### STEP 4 — (여유 있을 때만) SoldOut 9px

| 항목 | 값 |
|---|---|
| 위치 | Admin SoldOutCard · SCR-011 |
| As-Is | **9px** |
| To-Be | 이름 **≥13** · 카드 대략 **150×160** |
| 누가 | **당신** 또는 Claude 한 방 |
| 코드 블로커? | **아님** → 시간 없으면 **스킵** |

**Claude 복붙 (할 때만):**
```text
SoldOutCard Master + SCR-011
9px 텍스트 전부 ≥12(이름은 ≥13)
카드 크기 150×160 근처
다른 Admin 화면 금지.
```

---

## 2. STEP 1~3 끝나면 바로 코드

| 제품 | 폴더 | 첫 명령 |
|---|---|---|
| 키오스크 | `C:\ASAK-workspace\ASAK-Kiosk` | 화면/컴포넌트 구현 시작 |
| 백엔드 | `C:\ASAK-workspace\ASAK-back` | `.\gradlew.bat bootRun` |
| 관리자 | `C:\ASAK-workspace\ASAK-Admin` | STEP 4 스킵해도 시작 가능 |

---

## 3. 나중에 QA할 때 (지금 하지 마)

Toast 400 · Confirm 560~680 · Style 97% · AUTO lh · SaveBar 3벌 · Badge · gap218  
→ 그때는 FIX_PLAN Batch 4~8 · 파트너 표 §1.7

---

## 4. 체크 (복붙)

- [ ] STEP1 SCR-008 = 1080×180 (메인:당신 / 검증:Cursor)
- [ ] STEP2 Blue = 0 (메인:Claude / 목록:Codex / 검증:Cursor)
- [ ] STEP3 Tap = 0 (메인:당신 / 검증:Codex)
- [ ] (선택) STEP4 9px
- [ ] 코드 폴더로 이동

---

*100점 아님. STEP 1~3 PASS면 디자인 최소 패스 완료.*
