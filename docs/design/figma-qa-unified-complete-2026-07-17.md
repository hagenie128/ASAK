# ASAK Figma QA 의견 통합본 (출처별 + 종합)

**작성일:** 2026-07-17 · **파일:** `JSrjOy668zhfkiLplCkreh` · **쓰기:** 0회  
**규칙:** 주제별 → **문제→개선(출처 권장)** → 출처별 표(**A→B→C→D→E**) → 종합. 통합자 사견 없음.
**문제→개선**의 ‘개선하면’은 출처 A~E 원문에 적힌 권장·목표값만 모은 것이며, 통합자가 새로 만든 수치가 아니다.

---

## 📖 읽는 법 · 칩 범례

| 칩 | 의미 (원문에서 온 것) |
|---|---|
| ✅ | OK / 통과 (주로 E, 일부 C) |
| ⚠️ | 주의 · 권고 |
| 🔴 / 🔴🔴 | 심각 / E 최고심각 |
| **P0** **P1** **P2** | 우선순위 (A·B·C) |
| FAIL / PASS | 터치·크기 판정 (A·C) |
| 🟩 🟦 🟪 🟥 🟨 ⬛ ⬜ 🩶 | hex 스와치 (원문 색만, 신규 없음) |

| 부호 | 문서 | 역할 |
|---|---|---|
| **A** | Cursor 스크린 실측 | 05-C 57 · 06-C 72 프레임 수치표 |
| **B** | Cursor 컴포넌트 | Shared / Kiosk / Admin Master |
| **C** | Claude v2 | Foundations + 화면 교차검증 |
| **D** | Codex 정량 | 변수 · Text Style · Variant |
| **E** | Figma DS QA | 시각 · 터치 · lh · ✅⚠️🔴 |

### 🔄 문제 → 개선 한눈에 (출처 권장만 · 사견 없음)

> 원문(B 실측→권장, E 현재→권장, A 피드백, C 권장, D 반영 피드백)에 **적혀 있던** As-Is / To-Be만 모음. 출처 To-Be가 다르면 병기.

| # | 대상 | 문제 (지금 / As-Is) | 개선하면 (To-Be · 출처) |
|---|---|---|---|
| 1 | Foundations 표지 | Primitive/Semantic 표지 **80/47** | 실제 **83/51**로 맞추거나 집계 기준 명시 (**D**) |
| 2 | Green 스텝 | 문서 스텝명 ≠ 파일 Variable hex | Foundations 정합성 재검증 · 판정은 hex 실측 (**C**) |
| 3 | 라임 CTA 대비 | Confirm warning 🟩+⬜ 흰 텍스트 | 🟩+⬛ `#0D0D0D`/`#292D30` (Modal과 통일) (**B·C·D·E**) |
| 4 | Allergen Warning | 🟨 `#FBBF24` on 🟨 `#FFFBEB` ≈1.5:1 | WarningText 토큰(예 `#92400E`) (**C**) · Tag r4→8 (**E**) · desc 12→16 (**B**) |
| 5 | ConfirmDialog | Master **440×248** · Cart Clear440 / Delete**680** 혼용 · title 16 Medium | 키오스크 **560~680** · 버튼≥56 (**B·A**) · title **18 Bold** (**E**) · warning 다크텍스트 (**B**) |
| 6 | Toast | **299×76** · 키오스크 본문 12~14 · 스펙420≠실측 | 폭≥400 · 본문≥16 · size=kiosk (**B·A**) · 높이80+ (**E**) · 스펙 정합 (**C**) |
| 7 | Empty/Error | 「새로고침」· radius **0** · raw `#ccc` · 14px | type별 CTA (**B·A**) · radius **12** (**E**) · Semantic border (**C**) · CTA≥16~18 (**A**) |
| 8 | BottomCTA / SCR-008 | SCR-008 **`940×200`** · r15 · loading15 · opacity 모순 | **`1080×180`** (**A·B·C**) · r12/16(**B**) 또는 pill r20(**E**) · loading≥16 · opacity 제거(**C**) |
| 9 | CartItemCard | 🟦 Blue · 액션 **13px** · MenuButton · gap10/14/22 | Blue 제거 (**B·C·A**) · ≥16 · 48 pill (**E**) · wrap64 (**D**) |
| 10 | CategoryTap | **25×11** · Tap×4 · Deprecated 미정리 | **CategoryTab만** (**전원**) · Tab 52(B/C) 또는 **64**(**E**) · page=A 분리 |
| 11 | MenuCard | r0 · kcal**28** · AUTO · soldOut 텍스트 동일 | r**16** · kcal 20~24(**B**) 또는 16(**E**) · lh명시 · 텍스트 다운톤 (**B**) · AL (**E**) |
| 12 | MenuDetailSummary | 11~13px · 🟦 · legacy 1080×320 | 뱃지≥14~16 · 이름28+ · 가격24+ (**E·B**) · Blue제거 · legacy 분리 (**C·D**) |
| 13 | OptionGroup/Row | 12~15px · selected stroke 없음 | **16+** · label18 · price16 · border 3px 🟩 · 체크 (**B·E·C**) |
| 14 | StatusBadge | 「핵심 재료」오라벨 · 🟪 | Role별 라벨/Property (**B·C**) · 11→12 (**B·E**) · 긴급도↓는 **C** 병기 |
| 15 | SaveBar 3벌 | ⬛ `#292D30` / ⬛ `#262626` / Sticky흰 · 🟥풀백 | 라이트 dirty (**B**) · 3벌 통합 (**C·D**) · SCR-011 이중 제거 (**C**) |
| 16 | SoldOutCard | **9px** · 130×134 | 9금지 · 이름≥13 · **150×160** (**A·B·C·E**) |
| 17 | SearchInput | Master **150×39** | Master **240~320** (**B·C**) |
| 18 | Checkbox | ✓없음 · 18px | ✓추가 (**C**) · hit 40/44 (**D**) |
| 19 | MenuButton | **16×16** · accents · 키오스크 혼입 | wrap 40/44·64 · Foundations색 · Blue제거 |
| 20 | OrderCard / Live | gap**218** · 본문12 · 총액**0원** | gap재검토 · 본문**14** · priceCalculation (**A·B·C**) · 취소 링크 (**E**) |
| 21 | Text Style / AUTO | Style 미연결 **97%+** · AUTO | 14 Style 연결 (**D**) · E lh 매핑 |
| 22 | `day` | Variant 읽기 오류 | Variant 해소 (**D** P0) |

---

## 0. 환경 · 반영 원칙

### 키오스크 vs 관리자

#### 출처별 (A→E)

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | 기준 | 키오스크: 본문≥16 · 터치≥48 · selected border · Blue 금지 · BottomCTA **1080×180**<br>관리자: 본문≥13 · **9px 금지** · StatusBadge 오라벨 금지 · SaveBar dirty≠거의검정 | — |
| **B** | 기준 | 키오스크 **1080×1920** · 터치≥48 (핵심 56~64)<br>관리자 **1920×1080** · 본문 13~14 · 클릭 32~40 (터치 44+) | — |
| **C** | 기준 | 관리자 **9px 이하 금지** · Touch Min **48** · Comfortable **56** · Large **64**(권장) | — |
| **D** | 기준 | 키오스크 hit **64+** · 보조 56+ · 웹 40+ · 태블릿 44+ · lh 16/24 · 14/20 · 12/16 | — |
| **E** | 환경 | 키오스크 15~27인치 터치 스탠드 · 관리자 웹·태블릿 | — |

#### 📎 종합

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 키오스크=세로 터치·본문 16+ / 관리자=가로·밀도↑·9px 금지 |
| ⚠️ 병기 | 터치 최소: A/B/C=**48**(+권장 56~64) vs D=조작 **64+** |

### Master → 스크린

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | 순서 | Master → override 제거 → 스크린 통일 → Toast size → Content | — |
| **B** | 원칙 | Master 수정 → 05/06 전파. 스크린만 고치면 재발 | — |
| **C** | 실증 | SCR-008: Master 정상인데 화면 **override**로 깨짐 | — |
| **D** | 선행 | 표지 변수수 · `day` Variant · Text Style 연결부터 | — |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Master 먼저 → 스크린 override / Content |

---

## 1. 🎨 Foundations (`148:12745`)

### 자산 수 · 토큰

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 표지 Primitive/Semantic **80/47** | 실제 **83/51** 또는 집계 기준 명시 | **D** |
| Green 스텝명 ≠ 파일 hex | Foundations 재검증 · hex 기준 판정 | **C** |
| Text Style 미연결 · AUTO | 14 Style 연결 · lh 매핑표 적용 | **D** · **E** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **B** | 제안(미적용) | 타입 스케일 제안. 금지: 퍼플 남발 · Blue 선택 · 글로우 · 새 hex · AUTO lh | 🟩 `#B5E30F` · 🟦 `#3B82F6` 금지 · 🟪 `#6D3FC4` 금지 |
| **C** | ⚠️ | 문서 Green **스텝 번호 ≠** 파일 Variable. 판정은 **hex 실측**. Neutral↔CoolGray 혼재 · Focus Ring HC 미대응 · Noto→Pretendard TODO | 문서라 적힌 🟩 `#B5E30F`(Green/300) vs 파일 Green/300=🟩 `#E2FF99` · Green/500=🟩 `#D1FF33` |
| **D** | **P0** | Primitive **83** / Semantic **51** (표지 **80/47** 불일치). Text Style 14 · Effect 3 · ALL_SCOPES. Foundation 텍스트 Style 미연결 259/273 | `83 / 51` |
| **E** | 우선 | AUTO → 명시 lh 매핑 (44→54 … 11→16) | — |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Semantic만 화면 / Style 미연결은 D 수치 |
| ⚠️ 병기 | 표지 80/47 vs 83/51 (**D**) · Green 스텝 어긋남 (**C**) |

### 라임 · 대비

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Confirm warning 🟩+⬜ (1.5:1) | 🟩+⬛ `#0D0D0D`/`#292D30` | **B·C·D** |
| Allergen 🟨 on 🟨 ≈1.5:1 | WarningText 전용 토큰 | **C** |
| 라임을 본문 텍스트에 사용 | 라임=면적/CTA · 본문=다크 | **D·E** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **B** | ⚠️ | CTA=라임+다크텍스트. Confirm warning=라임+**흰** → 대비 문제 | 🟩 `#B5E30F` + ⬛ `#0D0D0D` / `#292D30` · +⬜ 흰 금지 |
| **C** | **P0** | Modal=라임+다크(올바른 CTA). warning=Brand만 재사용(**P1**). Allergen 저대비 ≈1.5~1.7:1 | 🟩 `#B5E30F`+⬛ · Warning 🟨 `#FBBF24` on 🟨 `#FFFBEB` |
| **D** | ✅/금지 | 🟩+검정 **13.97:1** OK · 🟩+흰 **1.50:1 금지** · `#5B8C2A`+흰 4.01 · `#243300`+흰 13.58 | 🟩 `#B5E30F` · 🟫 `#243300` · ⬜ `#FFFFFF` |
| **E** | ✅ | 브랜드 라임·다크·음식 사진 정체성 OK. CTA 대비·위험동작은 정리 대상 | 🟩 `#B5E30F` |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 라임 위 **흰 글자 금지**(D·B·C). 라임=면적/CTA, 본문=다크 |
| 📌 한 출처만 | Allergen 저대비 = Semantic Warning 토큰 결함 (**C**) |

---

## 2. 🧩 Shared (`145:2`)

### Shared/Modal `158:23908`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 스크린 Modal **400×220** | **≥480~560** (Master 480 쪽) | **A** |
| 키오스크에 Admin Modal 그대로 | CTA 높이 **48** 또는 **64** Variant | **E** · **D** |
| Primitive / BG 토큰 오용 | Semantic 재매핑 | **C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | ⚠️ | 스크린 Modal **400×220** → 키오스크 좁음 ≥480~560. Shared 본문 16은 모범 | `400×220` vs Master `480` |
| **B** | ✅방향 | 480×196 · pad32 · r16 · title 22/28 · desc 16 · primary 라임+다크 — Confirm warning보다 올바른 CTA | 🟩 `#B5E30F` + ⬛ `#0D0D0D` · `480×196` |
| **C** | ⚠️ | pad/gap/radius 준수 · Floating. BG 토큰 오용 · Primitive 직접 · 버튼 48 · py14. Purple/Blue 없음. 고위험은 56+ 권장 | 버튼 **48** |
| **D** | 분기 | type 3종 각 480×196. 관리자 OK. 키오스크는 64px CTA Variant 별도 | `480×196` |
| **E** | ✅ / ⚠️ | 사이즈·pad·radius·title·body ✅ · Button text ⚠️ → 키오스크 버튼 높이 48 | ✅ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Master 480 · 라임+다크 CTA 양호 (B·C·D·E) |
| ⚠️ 병기 | A 스크린 **400×220** ≠ Master 480. D=64 Variant · C=48(+56 권장) |

### Shared/ConfirmDialog `158:23975`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Master **440×248** · Delete **680** / Clear **440** 혼용 | 키오스크 **560~680** · Cart Dialog **크기 통일** | **A** · **B** |
| title **16 Medium** | **18 Bold** lh24 · 키오스크면 **22~24** | **E** · **B** |
| warning 🟩+⬜ 흰 | 🟩+⬛ 다크텍스트 | **B** · **C** |
| 설명 **14px** | 키오스크 **16~18** | **B** · **C** |
| loading = opacity만 | disabled + 스피너 | **C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **FAIL** | Cart Delete/Last **680×242** vs Clear **440×248** 혼용. Admin 440 OK | `680×242` / `440×248` |
| **B** | ⚠️ | Master 전 variant **440×248**. warning=라임+**흰** 대비. lh 명시 모범. 키오스크 560~640 · 버튼≥56 | 🟩+⬜ 흰 문제 · `440×248` |
| **C** | **P0**후보 | Surface/600 오용 · warning=Brand만 · loading=opacity 0.4 · Primitive 다수 · 설명 14=Kiosk 미달 · MCP↔렌더 불일치 미확정 | 설명 **14px** |
| **D** | 문서화 | type×tone×state allowed combinations 명시. `440×248` | `440×248` |
| **E** | 🔴 | Title 16 Medium 🔴 → 18 Bold lh24. `#e5e7eb` ⚠️ → `#f5f5f5`. Modal 22와 위계 | 🔴 · ⬜ `#E5E7EB` → ⬜ `#F5F5F5` |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Master 440×248 · warning 대비/위계 문제 · 키오스크는 더 큰 size (B·A) |
| ⚠️ 병기 | A: Delete=680 / Clear=440. E title 18 vs B 키오스크 22~24 |

### Shared/Toast `158:24049`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| **299×76** · 키오스크 본문 12~14 | 폭 **≥400** · 본문 **≥16** · size=kiosk | **A** · **B** |
| 스펙 420 ≠ 실측 299.4 | 스펙↔실측 정합 | **C** |
| 키오스크 높이 부족 | 높이 **80+** | **E** |
| 닫기 ✕ · hit ~42 | **24×24 Icon** · hit **48** | **E** · **C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **FAIL**(키오스크) | Detail/Cart Toast **299×74~76** + 본문 12~14. Admin 300×76 우상단 OK | `299×74~76` |
| **B** | 분기 | Admin OK. 키오스크 ≥400·≥16. Kiosk 프레임 **920×115**와 스케일 다름 → size=kiosk | `299×76` vs `920×115` |
| **C** | **P0** | 문서 longMessage=420 vs 실측 **299.4**. 메시지 12 · 닫기 hit ~42&lt;48 | `299.4` ≠ `420` |
| **D** | ✅(Admin) | 76 높이 충분 · 본문 14/20 · longMessage 2줄 | `299×76` |
| **E** | ✅ / ⚠️ | 299×76 ✅ · 키오스크 높이 80+ · 닫기 ✕ → 24×24 Icon | ✅ · ⚠️ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | ≈299×76 · Admin 허용 · **키오스크엔 작다** (A·B·C·E) |
| ⚠️ 병기 | D는 Admin 맥락으로 76 OK. C는 스펙 420 P0. B는 920 프레임 |

### EmptyState · ErrorState · LoadingState

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Empty「새로고침」·14px | type별 CTA · 키오스크 **≥16~18** | **A** · **B** |
| radius **0** | radius **12** | **E** |
| raw `#ccc` · 아이콘 64 | Semantic Border · 아이콘 스케일 정리 | **C** |
| Loading 회색 혼용 | 단일 Semantic 스켈레톤 | **C** |
| Error CTA 색 갈림 | E=`#292d30` / A·B=라임 스케일↑ — **병기** | **E** · **A·B** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | ⚠️ | Empty「새로고침」14 · Cart는「메뉴 담으러 가기」+≥18 · Error label 14→18 | **14px** |
| **B** | ⚠️ | Empty 기본「새로고침」·Menu는「새 메뉴 추가」여야. Error inline 12=키오스크 금지. Loading OK | `400×280/216` |
| **C** | **P0** | Empty: Primitive + raw 테두리 · 아이콘 64&gt;XXL48. Loading: CoolGray vs Neutral 행 혼용 | ⬜ `#CCC` raw · ⬜ `#E5E7EB` vs ⬜ `#F5F5F5` |
| **D** | 정리 | 216 vs 280 설명/통일 · Error 조합표 · Loading button 40=Admin만 | `40` Admin |
| **E** | 🔴 | Empty/Error radius **0** 🔴 →12. Empty 아이콘 bg ⚠️. Error CTA 라임→dark. spinner `#6c9700` | 🔴 · ⬜ `#E5E7EB` → `#F5F5F5` · 🟩 `#6C9700` |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Empty CTA·키오스크 스케일 (A·B) · radius 0 (**E**) · Primitive/raw (**C**) |
| ⚠️ 병기 | Error CTA: E=dark vs B/A=라임 스케일 상향 |

### Allergen · Icons

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Notice desc **12** · Warning 저대비 | desc **≥16** · WarningText(예 `#92400E`) | **B** · **C** |
| Tag radius **4** | **8** | **E** |
| Icon 32를 클릭처럼 | 상위 hit **48** / **44** | **B** · **D** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **B** | ⚠️ | Notice desc 12→16. Tag 32=표시용 OK. Caret hit 48+ | **12px** |
| **C** | **P0** | Warning 저대비 Tag·Notice 동시 | 🟨 `#FBBF24` on 🟨 `#FFFBEB` · 🩶 `#E6E6E6` placeholder |
| **D** | 정보 | Tag≠버튼. Icon 32≠클릭영역 | `32×32` |
| **E** | ⚠️ | Tag radius 4→8 | ⚠️ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 알레르기 작음/저대비 (B·C) · Tag=비터치 (D·B) |
| 📌 | Semantic Warning 토큰 결함 (**C**) |

---

## 3. 🖥️ Kiosk Components (`150:2`)

### BottomCTA `150:385` (+ SCR-008 override)

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| SCR-008 **`940×200`** override | **`1080×180`** · override 제거 | **A** · **B** · **C** |
| radius **15** · elevation 없음 | r **12/16** (**B**) 또는 pill r **20** (**E**) | **B** · **E** |
| loading **15px** | **≥16** | **C** |
| disabled = opacity-50 (문서 모순) | opacity 제거 · 정식 disabled 색 | **C** |
| pad T/B **30** | **32** | **B** · **A** |
| D 클릭면 기준 | 높이 **112+** (Master 180과 병기) | **D** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | 대부분 `1080×180`. SCR-008 **`940×200`**. pad 30/40 혼재. loading 높이 180 유지 | `1080×180` vs `940×200` |
| **B** | ⚠️ | Master 180 유지 · override 금지 · pad30→32 · elevation · radius 15→12/16 · lh40 | radius **15** |
| **C** | **P0** | loading 라벨 **15px**. disabled: 문서≠opacity인데 실제 opacity-50 **모순**. SCR-008: 크기·variant·타이포 **3중 override 재발** | 🟩 `#B5E30F` · **15px** · `940×200` |
| **D** | 기준 | 클릭면 높이 **112+** · 내부 텍스트 24/30+ | **112+** |
| **E** | 🔴 | 전체너비 사각·r0 · disabled 문구. 좌우32 · pill r20 · lh44 | 🔴 |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Master **1080×180** · SCR-008 **940×200 FAIL** (A·B·C) |
| ⚠️ 병기 | D 112+ vs 180 · E r20 vs B 12/16 · C opacity 모순 · E disabled 문구 |

### CartItemCard `150:404` (+ MenuButton 혼입)

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 🟦 Blue `#3B82F6`/`#0088FF` | Blue **삭제** → 브랜드/뉴트럴 | **B** · **C** · **A** |
| 액션 **13px** | **≥16** · **48 pill** | **B** · **A** · **E** |
| gap 10/14/22 | 8/12/16/24… | **B** · **A** |
| MenuButton 혼입 | 키오스크 금지 또는 wrap **64** | **D** · **A** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Cart 전 상태 blueN≈6~12 · Admin/MenuButton×2~4 · 액션 **13px** · gap 10/14/22 | 🟦 Blue × N |
| **B** | **P0** | 🟦 `#3B82F6` / `#0088FF` 제거 · 13px 금지 · gaps 제거 · Disabled 높이 점프 | 🟦 `#3B82F6` · 🟦 `#0088FF` |
| **C** | **P0** | Blue 재발(체크·SET음료). `#0088FF`≠Foundations Blue. SoldOut 수량 48×48 | 🟦 `#0088FF` · **13px** · `48×48` |
| **D** | 정리 | State→state · SoldOut 화면 Variant · MenuButton 28×28 키오스크 금지/wrap 64 | `28×28` → `64` |
| **E** | ⚠️ | 좌우 pad · 수정/삭제 → 48 pill · 합계 lh34 | **48** pill |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Blue · 13px · MenuButton 혼입 = **P0** (A·B·C·D) |

### Category / CategoryTab / CategoryTap

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Tap **25×11** · Tap×4 | **CategoryTab만** · Tap Deprecated | **전원** |
| Tab 높이 **52** | 유지(B/C) 또는 **64**(E) — 병기 | **B·C** · **E** |
| page=A chip 11px | Admin 전용으로 **분리** | **B** · **C** · **D** |
| 선택 = weight만 | 라임 underline **3px** | **E** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Menu List **CategoryTap×4** → Tab 교체. Category Disabled도 Tap 의존 | Tap×4 |
| **B** | **FAIL** | Tab 128×52 OK. Tap Size=s **25×11** · 오타 Tap/Tab · page=A Admin 혼재 · 레이어명 버그 | **25×11** |
| **C** | **P0** | Tap Deprecated인데 정식 캔버스 · 터치 FAIL 11px(23%). page=A chip 11px FAIL. Tab≈52~59 PASS 추정 | **11px FAIL** |
| **D** | 통합 | Tab+Tap 하나 · size/state · page K/A → surface | — |
| **E** | 🔴🔴 | Tab 52→64. Tap 25×11 🔴🔴 삭제/Deprecated. Category underline 3px | 🔴🔴 `25×11` |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Tap=오타/Deprecated/터치 FAIL → **Tab만** (A·B·C·D·E). page=A 분리 |
| ⚠️ 병기 | Tab 높이: B/C≈52 PASS 추정 vs E=**64** 상향 |

### MenuCard `150:678`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| r **0** · layout NONE | r **16** · Vertical AL | **B** · **E** |
| kcal **28** | **20~24**(B) 또는 **16**(E) | **B** · **E** |
| lh AUTO | lh 명시 | **B** · **E** |
| soldOut 텍스트 동일색 | 텍스트 다운톤 | **B** |
| 가격색 | `#6C9700`(B·C) vs `#4A7A00`(E) — 병기 | **B·C** · **E** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | 재확인 | MenuCard×9. soldOut 텍스트 톤 스크린 재확인 | `305×369` |
| **B** | ⚠️ | r0→16 검토 · 이름30/가격38 AUTO · kcal28→20~24 · soldOut 텍스트 다운톤 없음 | 🟩 `#6C9700` 가격 |
| **C** | ✅방향 | 가격 `#6C9700` OK. soldOut 흑백+배지 병행(정책 준수) | 🟩 `#6C9700` |
| **D** | Variant | soldOut=이미지·이름·가격·CTA를 Variant에 명시 | — |
| **E** | 🔴 | layout NONE · kcal28 과대 · r0. AL · kcal**16** · 가격 `#4A7A00` | 🔴 · 🟩 `#4A7A00`(E 권장) |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | r0 · kcal 큼 · AUTO (B·E) |
| ⚠️ 병기 | 가격색 B/C 🟩 `#6C9700` vs E `#4A7A00` · kcal 목표 B 20~24 vs E 16 |

### MenuDetailSummary `160:1734`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 뱃지11 · desc14 · kcal13 · price18 | 뱃지≥14~16 · 이름28~32 · 설명16~18 · kcal16 · 가격24~28 | **B** · **E** |
| optionSummary 🟦 13px | Blue 삭제 · ≥16 | **B** · **C** |
| legacy state 1080×320 | state 분리/삭제 · 4 state만 | **C** · **D** |
| Stepper 오버플로우 | 부모/자식 64 정합 | **C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **B** | **P0** | 뱃지11 · desc14 · kcal13 · optionSummary **13 Blue** → 16+ · Blue 금지 · variant 스케일 폭주 | 🟦 `#3B82F6` · **11~13px** |
| **C** | 🔴최고 | state=`MenuDetailSummary` legacy(Noto·하드코딩·1080×320) · Blue · Stepper 오버플로우 | 🟦 + legacy `1080×320` vs `480×403` |
| **D** | 제거 | `MenuDetailSummary` state 제거 · 나머지 4만 | — |
| **E** | 🔴🔴 | 즉시1: 뱃지14 · 이름28+ · 가격24+ 스케일업 | 🔴🔴 |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 스케일 작음 · Blue · legacy/이상 variant (B·C·D·E) |
| 📌 | C가 본 QA **최고 심각도**로 표시 |

### Option 선택군 (Group · Row · Card · OrderDetailRow)

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Group 필수12 · 설명13 | **16+** · title 22~24(B) / 20/28(E) | **A·B·C·E** |
| Row 15/14 · stroke 없음 | label **18** · price **16** · border **3px** 🟩 · 체크 · r12 | **B** · **E** |
| indicator 20을 클릭 | row 전체 **≥72~80** | **D** · **B** |
| B: OrderDetailRow×46 vs A·C: OptionCard×46 | 스크린=**OptionCard**(A·C) · legacy Row 별도 | **A·B·C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | ✅구조 / ⚠️타입 | 스크린= **OptionCard×46** + OptionGroup×7 (OrderDetailRow×46 가정 **정정**). 필수12·설명13 · gap6/18 · Blue0 | **12~13px** · Card×46 |
| **B** | **P0**(당시) | Group 12/13→16. Row 15/14 · selected stroke 없음→border3. OptionCard 03-C **missing**. Detail에 OrderDetailRow×46 오용이라 기록 | selected border 없음 |
| **C** | **P0** | Row **15variant 전수** 15/14/11 &lt;16. selected=배경+indicator+굵기(우수). OrderDetailRow 6/7 legacy 팔레트 | **15/14px** · legacy hex |
| **D** | 구조 | Group에 selectionType. Row indicator≠target · row≥72. OrderDetailRow에서 minus 분리 | indicator `20×20` |
| **E** | 🔴 | Group/Row 즉시: 폰트16~20 · r12 · 체크 아이콘 | 🔴 |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 옵션 본문 12~15 → 키오스크 16 미달 · selected 강화 |
| ⚠️ 병기 | **B:** OrderDetailRow×46 vs **A·C:** OptionCard×46. Master missing(B) vs 스크린 사용(A) |

### PaymentCard · Summary · Stepper · Header · Home · 기타

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | ✅/⚠️ | Payment selected **4px** 유지 · gap 5/25/35→8/24/32 · Header 48vs62 · CTA pad 30/40 | gap **5/25/35** |
| **B** | ✅모범 | PaymentCard selected 4px=**모범**. Stepper **64 PASS**. Header 비대칭. Home 44→lh52 | 🟩 `#B5E30F` border **4px** · `64×64` PASS |
| **C** | ⚠️ | border 4px=Scale Heavy3 **초과**(권장3). Stepper 64 PASS·문서「파란」오기재. Header≈대칭. Allergy 전부&lt;16 · 헤더~34 FAIL 의심 | **4px** vs Scale **3** · Allergy **12~14** |
| **D** | property | Payment false/none 통합 · Stepper state×limit · Home≥240×240 · Allergy header≥72 | — |
| **E** | ⚠️ | Payment 미선택 border 1px · Stepper **72** 상향 · Header→AL · Home lh54 · Allergy 60 | Stepper `72×72`(E) |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Payment selected 모범 유지(A·B) · Stepper **64 PASS**(B·C) · Home 큼+lh |
| ⚠️ 병기 | Header 대칭 A/B vs C · 4px 모범(B) vs Scale초과(C) · Stepper E만 72 |

---

## 4. 🛠️ Admin Components (`150:2860`)

### StatusBadge `150:5064`

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 「핵심 재료」오라벨 | Role별 라벨 / Property 바인딩 | **B** · **C** |
| 11px · 🟪 | **12+** · 퍼플 처리(B 삭제 / C Category면 준수) | **B·E·C** |
| A/B 화면 P0 vs C 실사용0 | Master 수정 · **긴급도는 C 하향 병기** | **A·B·C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Admin SCR 거의 전부 badgeWrong. Sales에도「핵심 재료」 | 「핵심 재료」 · **11px** |
| **B** | **P0** | 12 Role 대부분 오라벨 · 드레싱 퍼플 · 11→12 | 🟪 `#6D3FC4` · 🟥 `#EF4444` |
| **C** | Master P0 → 실사용 **P2** | 11/12(91.7%) 오표시. **화면 실사용 0건**(고아1) → 긴급도 하향. 화면은 raw tag·텍스트 정확 | 91.7% · 실사용 **0** |
| **D** | 축 분리 | Role에 category/availability/required 혼재 | — |
| **E** | ⚠️ | 11 → 12+ | **11px** |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Master 오라벨은 사실 (B·C·A) |
| ⚠️ 병기 | A/B=화면 위험 P0 vs **C=실사용 0 → 긴급도 하향** |

### SaveBar · StickyActionBar · PaymentSaveBar

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| dirty ⬛ `#292D30` · Payment ⬛ `#262626` | 라이트 dirty(예 `#FFFBEB`) · saving `#F5F5F5` | **B** · **A** |
| SaveBar/Sticky/Payment **3벌** | **하나의 semantic 세트**로 통합 | **C** · **D** |
| SCR-011 다크바+Sticky 동시 | 이중 노출 **제거** | **C** |
| error 🟥 풀백 | `#EF4444`/`#FFF0EB` 계열 · 오류 문구 | **A** · **C** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Sold-out/Menu dirty ⬛ `#292D30`. Payment ⬛ `#262626` · error 🟥 `#E53333` | ⬛ `#292D30` · ⬛ `#262626` · 🟥 `#E53333` |
| **B** | **P0** | dirty/saving 다크 → 라이트 톤. PaymentSaveBar 톤 통일 | ⬛ `#292D30` |
| **C** | **P0**+확산 | 3벌 불일치. 화면 다수 재현. SCR-011에서 SaveBar+Sticky **이중 노출** | SaveBar ⬛ `#292d30` · Payment ⬛ `#262626`+🟩 `#d1ff33` · error 🟥 `#e53333` · Sticky=흰 |
| **D** | 정리 | state축 OK · success↔toast 중복 주의 · PaymentSaveBar 이름 정리 | — |
| **E** | ⚠️ | 저장 버튼 강조 약함 → Bold+배경 | ⚠️ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 다크 dirty / Payment 다크 = P0 · 화면 재현 (A·B·C) |
| 📌 | 3벌+이중 노출 (**C**) |

### SoldOutCard · MenuCard · Search · Checkbox · MenuButton

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| SoldOut **9px** · 130×134 | 9금지 · 이름≥13 · **150×160** | **A·B·C·E** |
| Search Master **150** | Master **240~320** | **B** · **C** |
| Checkbox ✓없음 | ✓추가 · hit **40/44** | **C** · **D** |
| MenuButton 16×16 · accents | wrap 40/44·64 · Foundations색 · Blue제거 | **C·D·B** |
| BEST/NEW 10px · EDITING 빨강 | caption 11~12 · EDITING 파랑/노랑 | **A·B·E** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Sold-out **fs9×26**. MenuCard **10px** BEST/NEW. Detail 9~10 | **9px** · **10px** |
| **B** | **P0** | SoldOut 9 금지 · MenuCard10 · Search **150** 좁음 · Checkbox hit · MenuButton Blue | Search `150×39` |
| **C** | **P0** | Checkbox ✓ **없음** · 18px. Search Master150(화면 수동확대 은폐). MenuButton 16+accents 미등록. FilterChip 3중결함 | ✓없음 · `16×16` · accents 🟦🟧 |
| **D** | wrapper | MenuButton wrap 40/44 · Checkbox 행 40/44 · SoldOut property | `40/44` |
| **E** | 🔴🔴 | SoldOutCard 즉시: 150×160 · 13/12/11. EDITING 빨강→파랑/노랑 | 🔴🔴 **9px** |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | SoldOut **9px P0** · Search 150 · Checkbox 크기 (B·C·D); C만 ✓부재 |

### Navbar · OrderCard · DataTable · TopHeader · OrderAction · 기타

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Navbar shadow 4~8겹 | shadow **1** · Semantic · accent bar | **B·C·E** |
| gap **218** · 본문12 · 총액0원 | gap 재검토 · 본문 **14** · 실합계 | **A·B·C** |
| DataTable AUTO · hover 없음 | lh 18~20 · Hover `#f9fafb` | **B·E·D** |
| TopHeader inactive=라임 | position×state 분리 | **B·C·D** |
| `day` Variant 오류 | Variant 해소 | **D** |
| 환불=일반 버튼 | outline + confirm · danger token | **E** · **D** |

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0**/⚠️ | Live **gap218** · 12×260. Navbar 90×72 vs 240. badgeWrong | gap **218** |
| **B** | **P0**/⚠️ | Navbar shadow4→1. OrderCard gap**218** · 본문12→14. TopHeader inactive인데 라임 | shadow **4** · 🟩 라임 |
| **C** | 재배치 | Navbar Primitive+**8겹** shadow. gap218 **미재현**. 총액0원. TopHeader/SalesMetric **화면 임팩트↓**. OrderAction Primitive P0 | shadow **8** · 총액 **0원** |
| **D** | **P0** | `day` Variant 오류. Navbar viewport 분리. DateSelector 35→40/44. refund=danger | `day` **P0** · `35`→`40/44` |
| **E** | 🔴 | Navbar accent bar. OrderCard 취소→링크. DataTable hover. 환불 outline+confirm. ModalActionBar 12→14 | 🔴 |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Navbar shadow 정리 · 총액0원(C) · DataTable lh/hover |
| ⚠️ 병기 | gap218 A/B vs C 미재현 · Badge/TopHeader/Metric 긴급도 C 하향 |
| 📌 | `day` Variant (**D**) · 환불 outline (**E**) |

---

## 5. 🛒 Kiosk Screens (`05-C` / `134:7720`)

### SCR-001 Home

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 한글 44 lh AUTO | lh **52**(A·B) / **54**(E) · tracking −1% | **A·B·E** |
| HC 바인딩 불명 | Semantic HC 실바인딩·대비 확인 | **A·D** |
| radius 0 | **24** 검토 | **A·B·E** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | ⚠️ | `134:7721`/`224:12713` · 한글44 lh→52 · Display64 tracking−1% · HC 바인딩 확인 · BottomCTA 없음(의도) | **44** / **64** |
| **B** | P1 | HomeActionButton lh · tracking · radius | — |
| **C** | ✅일관 | HomeActionButton 인스턴스 일관 | — |
| **D** | 비교 | Default vs HC 장식색 · hit≥240×240 | `240×240` |
| **E** | ✅ | 다크+음식+라임 아이덴티티 ✅ · lh 명시 | ✅ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | 브랜드 OK · HomeActionButton lh 명시 |
| ⚠️ 병기 | A=flat 흰 배경 실측 vs E=다크 아이덴티티 긍정 |

### SCR-003 Menu List

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| CategoryTap×4 · AUTO100% | **Tab** · lh 명시 | **A·B·E** |
| Empty/Error 14px | CTA≥16~18 · 문구 교체 | **A** |
| Toast299 · kcal28 | Toast 키오스크 size · kcal↓ | **A·E** |
| Loading CTA 활성 | 로딩 CTA 정책 통일 | **C** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0** | CategoryTap×4 · AUTO **100%** · CTA pad30 · Empty「새로고침」14 · Error14→18 · Toast299 | Tap×4 · AUTO100% |
| **B** | Fail if Tap | Category Disabled에 Tap 25면 Fail | `25` |
| **C** | ⚠️/P2 | MenuCard×45 일관 · placeholder · Loading CTA「결제하기」활성 **P2** · Empty/Load/Error 일관 우수 | placeholder |
| **D** | coverage | 8상태 · 기준선 동일 · Disabled=클릭불가 | 8 states |
| **E** | 🔴 | kcal28→16 · 가격 `#4A7A00` · disabled CTA · underline | 🔴 · 🟩 `#4A7A00` |

### SCR-004 Menu Detail

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 필수/설명 12~13 · Toast299 | **16+** · Toast kiosk size | **A·B·C·E** |
| selected 약함 | tint+**3~4px** border | **B·E** |
| Discard 440 vs 680 | 키오스크 **560~680** 통일 | **A·B** |
| Loading CTA 불일치 | List/Detail 정책 하나 | **C** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | ✅구조/⚠️ | OptionCard×46+Group×7 · 12/13→16 · Toast299 **FAIL** · Dialog 560~680 · Allergy→16 · Blue0 | Toast `299×74` |
| **B** | (당시 P0) | 우선순위표 OrderDetailRow 오용(이후 A 정정) | — |
| **C** | ⚠️ | OptionCard 일관 · Loading CTA 스켈레톤 vs List Loading CTA 유지=정책 불일치 | Loading CTA 불일치 |
| **D** | 상태多 | Option row 전체 64+ · SO/limit/error CTA 분리 | `64+` |
| **E** | 🔴 | Summary 스케일업 · Option 폰트 · CTA pill20 | 🔴 |

### SCR-005 Cart

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| Blue · 13px · MenuButton | Blue제거 · ≥16 · MenuButton 정리 | **A·B·C** |
| Dialog 680 vs 440 | **크기 통일** | **A** |
| Empty「새로고침」 | 「메뉴 담으러 가기」+≥18 | **A** |
| 수정/삭제 작음 | **48** pill · 합계 구분 강화 | **E** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0** | Blue+MenuButton+13px · Dialog 680 vs 440 · Toast299 · Empty CTA | 🟦 · `680`/`440` |
| **B** | **P0** | CartItemCard · Confirm 키오스크 크기 | — |
| **C** | ✅산술 | 8400×2=16800 정합 · Delete Red · 부분품절 우수 | ✅ 산술 |
| **D** | coverage | Checkout Blocked 등 · confirm≥64 | `64` |
| **E** | 🔴 | 수정/삭제 터치48 · 합계 border/배경 | 🔴 · **48** |

### SCR-007 · 008 · 012/013 · 014

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| SCR-008 **`940×200`** | **`1080×180`** · 올바른 variant | **A·B·C** |
| Payment gap 5/25/35 | **8/24/32** | **A** |
| Modal **400×220** | **≥480~560** | **A** |
| 이중 CTA · Timeout+결제활성 | CTA 단일 · 상태 일치 | **C** |
| Complete 여백 과다 | 대기/일러스트 (E) | **E** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0**/⚠️ | Payment gap5/25/35 · Complete CTA **940×200 P0** · Modal400 · A11y Inst0 | `940×200` · Modal `400` |
| **B** | **P0** | Complete override 금지 · Modal↔Confirm 통일 · A11y P2 | — |
| **C** | **P0**/P1 | Complete **3중 override 최우선**. Declined 이중 CTA **P1**. Timeout인데「결제하기」활성 **P1** | 3중 override |
| **D** | 상태 | Processing loading/disabled · Declined≠network CTA · Timeout 숫자색 · A11y 2채널 | — |
| **E** | ⚠️ | Payment disabled 명확화 · Complete 여백 과다 · 대기/일러스트 | ⚠️ |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | **SCR-008 CTA override = 최우선** (A·B·C) |
| 📌 | 이중 CTA·Timeout 불일치(**C**) · Complete 여백(**E**) · Modal400(**A**) |

---

## 6. 📊 Admin Screens (`06-C` / `134:10606`)

### SCR-009 Live Order

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| gap **218** · 본문12 | gap 재검토 · 본문 **14** (C는 gap 미재현 병기) | **A·B·C** |
| 총액 **0원** | priceCalculation 실합계 | **C** |
| 원 placeholder 아이콘 · 이중 알림 | 실아이콘 · 알림 단일화 | **C** |
| 취소=완료 동급 | 취소→**텍스트 링크** | **E** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0** | gap**218** · 본문12×260→14 · badgeWrong · Navbar 90 vs 240 | gap **218** |
| **B** | P1 | OrderCard 12→14 · gap218 | — |
| **C** | **P0**/P1 | Detail **총액 0원** vs 라인합. 아이콘「색만 다른 원」. 배너+토스트 이중. Badge 실사용↓ | 총액 **0원** |
| **D** | ✅coverage | New Order/TTS → toast만으로 끝내지 말 것 | coverage 최고 |
| **E** | 🔴 | 옵션 `#888` · 취소→텍스트링크 | 🩶 `#888` · 🔴 |

| 구분 | 내용 |
|---|---|
| ⚠️ 병기 | gap218 A/B vs C 미재현 · **총액0원·이중알림=C** |

### SCR-010 · 011 · 015

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 011 **9px** · SaveBar ⬛ · Sticky 이중 | 9→12+ · 라이트바 · 이중 제거 | **A·E·C** |
| 010 badge · hover 없음 | Badge Master · Hover · 환불 분리 | **A·E** |
| Unauthorized=Empty | 미인가 전용 문구 | **C** |
| Login 에러12 | ≥13 · input48 | **A·D** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0** | 010 badgeWrong · 011 **fs9** · SaveBar ⬛ · Purple2 · 015 에러12 | **9px** · ⬛ `#292D30` · 🟪 |
| **B** | **P0** | StatusBadge · SoldOut9 · 폼40+ | — |
| **C** | **P0**/P1 | 011 SaveBar+Sticky **이중** · Unauthorized=Empty 오용 · Login ✓는 Master와 별도 | 이중 알림 |
| **D** | 터치 | filter+결과수 · row48/56 · checkbox row44 · input48 | `48/56/44` |
| **E** | 🔴 | hover · 환불 분리 · 선택 border/체크 · 9→12 | 🔴 |

### SCR-016 · 018 · 019~022

#### 🔄 문제 → 개선 (출처 권장)

| 문제 (지금) | 개선하면 | 출처 |
|---|---|---|
| 016 10px·복붙·메뉴명없음·다크바 | Content 수정 · 메뉴명 · SaveBar 톤 | **A·B** |
| Empty「새로고침」 | 「새 메뉴 추가」 | **A·B** |
| 018 다크바·미분기·좌우불일치 | SaveBar 통합 · 목데이터·좌우 동기 | **A·C** |
| EDITING 빨강 · 피크 단색 | 파랑/노랑 · 피크 진한색 | **E** |
| SalesMetric「연결 예정」 | Master 정리 (화면은 실숫자 — C) | **C** |

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | **P0**/Content | 016 MenuCard10 · Badge · 복붙 · Delete 메뉴명 · 다크바. 018 ⬛`#262626`/🟥`#E53333`. Sales Metric24 OK | ⬛ · 🟥 |
| **B** | Content | Empty CTA · SaveBar 톤 · Sales AUTO | — |
| **C** | **P0**/✅ | 018 Toggle **이름 미분기+좌우 불일치**. Sales **실숫자**(Metric Master버그 미재현) · Sales군 완성도 최고 | 목데이터 불일치 |
| **D** | clip | Add/Edit SaveBar 기준선 · All Disabled · Partial Data | clip=false 확인 |
| **E** | ⚠️ | EDITING 뱃지색 · 피크색 · 라벨간격 | ⚠️ |

---

## 7. 횡단 · 색 · 타이포 · Style

### Blue / Purple / 팔레트 / Primitive

| 출처 | 판정 | 의견 | 색·수치 칩 |
|---|---|---|---|
| **A** | **P0** | Cart Blue 다량 · Sold-out Purple2 · SaveBar 차콜 | 🟦 · 🟪 · ⬛ |
| **B** | 삭제 | Blue·Purple 삭제 · 뉴트럴 3단 · 추천레드 1토큰 | 🟦🟪 삭제 |
| **C** | **P0** | Blue 재발 · accents/* 전역 · Shared Primitive. Purple=드레싱만이면 정책 준수 가능 | 🟦 · accents · 🟪 조건부 |
| **D** | 금지 | 라임 위 white 금지 · Deprecated 잔존 | 🟩+⬜ 금지 |
| **E** | ⚠️ | 위험동작 구분 약함 | — |

| 구분 | 내용 |
|---|---|
| ✅ 합의 | Blue 제거 · 다크 SaveBar · Primitive/하드코딩 |
| ⚠️ 병기 | Purple: B/A 삭제 vs C=드레싱 Category면 준수 |

### AUTO · Text Style · gap

| 출처 | 판정 | 의견 | 칩 |
|---|---|---|---|
| **A** | — | Menu List AUTO100% · Live12×260 · SO 9×26 · gap5/25/35·14/22·218 · Header62vs48 | AUTO **100%** · **9px** |
| **B** | — | Kiosk AUTO100% · gap5/6/10/14/18/22/31·218 · r15 | — |
| **C** | — | Kiosk 9/21 컴포넌트 &lt;16 · Shared lh명시 모범 · py14 반복 | 9/21 |
| **D** | **P0** | Style 미연결 Kiosk **97.4%** · Admin **97.8%** · Kiosk컴포 **98.9%** · pad18 scale밖 | **97.4% / 97.8%** |
| **E** | 우선 | AUTO→명시 매핑표 | lh 표 |

---

## 8. 작업 목록 · 커버리지 (출처 병기)

### 우선 작업 (출처가 올린 목록)

| 출처 | 판정 | 목록 요지 |
|---|---|---|
| **A** | 순서 | Master(Blue·Badge·SaveBar·Option·Tap) → Complete override → Dialog 통일 → Toast → Content |
| **B** | Batch | Kiosk: Blue·CTA·Option·MenuCard·Summary / Admin: Badge·SaveBar·9px·gap218·Navbar / Shared: Confirm·Toast kiosk·Empty |
| **C** | Batch+하향 | V-Kiosk/Admin/Screen/Shared. 화면 최우선: 008·009/011/018. **하향:** Badge·TopHeader·SalesMetric |
| **D** | 체크리스트 | 83/51 · day Variant · Tab/Tap · 오타 prop · Text Style · AUTO/9~10 · hit64 · wrapper40/44 · 라임+white无 · Deprecated0 · clip · 66+72 |
| **E** | 즉시7 | Summary · Option · MenuCard · SoldOut · OrderAction · BottomCTA · DataTable hover (+AUTO·Tab64·radius·AL·Navbar·Confirm title) |

| 구분 | 내용 |
|---|---|
| ✅ 겹침 | SCR-008 · Cart Blue · CategoryTap · SaveBar · Option 폰트 · SoldOut9 · Toast/Confirm 키오스크 · Style/AUTO |
| ⚠️ 병기 | Badge 긴급도 · gap218 · E즉시7 vs C화면교차 우선 |

### 커버리지 · 한계

| 출처 | 범위 |
|---|---|
| **A** | Kiosk57 전수 표 · Admin72 핵심(+Sales 그룹) · Annotation 제외 |
| **B** | 쓰기0 · OptionCard 03-C missing · SCR 60+/70+ |
| **C** | Kiosk컴포 19/21 · Admin~53 · 화면 육안17+정밀1 · Admin45/72 · **MCP 한도** |
| **D** | 노드 정량 · 전프레임 고해상도 육안 미완 · 100% scale 재확인 필요 |
| **E** | DS 관점 종합 (전수 수치표 아님) |

---

## 9. 출처별 결론 (원문 요지)

| 출처 | 결론 한줄 |
|---|---|
| **A** | 스크린 override·Dialog혼용·Toast·Tap·SaveBar·gap218·Badge를 **수치로 고정** → Master→override→통일→Content |
| **B** | 키오스크=작음·AUTO·selected약·Blue / 관리자=Badge·다크바·9px·퍼플 / Shared=깔끔+size분기 · **Master 우선** |
| **C** | 토큰은 있으나 **적용률** 문제. 화면 교차로 Master P0 긴급도 재배치. 체감=SaveBar·008·009/011/018 |
| **D** | 상태 coverage 충분. 선행=표지·day·**Text Style**·hit |
| **E** | 브랜드 ✅. 웹·모바일 크기·AUTO·절대좌표·위험동작 → 즉시/높은 우선 |

---

## 부록 A — 스크린 프레임 실측표 (출처 A 수치 보존)

### A.0 전역 정정

| 이전 가정 | 2026-07-17 실측 (A) |
|---|---|
| OrderDetailRow×46 | **OptionCard×46 + OptionGroup×7** |
| OptionCard 없음 | Production Instance **사용 중** |
| Delete Confirm 항상 440 | Delete/Last **680×242** · Clear **440×248** |
| Complete CTA = 180 | **`940×200` override FAIL** |

### A.1~A.5 키오스크 (요약표 · ID 유지)

| SCR | 대표 ID | A 핵심 칩 |
|---|---|---|
| 001 Home | `134:7721` | 44 lh · 64 Display · HC 확인 |
| 003 List | `134:7792`+ | **Tap×4 P0** · AUTO100% · Toast299 · Empty14 |
| 004 Detail | `134:7810`+ | OptionCard×46 · 12/13 · Toast **299×74 FAIL** |
| 005 Cart | `134:7835`+ | 🟦×12 · Dialog **680/440** · Toast299 |
| 007 Pay | `134:7861`+ | gap **5/25/35** · selected 4px ✅ |
| 008 Done | `134:7926` | CTA **`940×200` P0** |
| 012/013 | `134:7900`+ | Modal **400×220** |
| 014 A11y | `134:7972`+ | Instance **0** |

### A.6~A.8 관리자

| SCR | A 핵심 칩 |
|---|---|
| 009 Live | gap **218** · 12×260 · badgeWrong · Navbar 90 vs 240 |
| 010 Orders | badgeWrong · Search150 확인 |
| 011 Sold-out | **9px×26** · ⬛ `#292D30` · 🟪×2 |
| 015 Login | 에러12 · Inst0 |
| 016 Menu | MenuCard **10px** · 다크바 · Content |
| 018 PayMethods | ⬛ `#262626` · 🟥 `#E53333` |
| 019~022 | badgeWrong · Metric24 OK |

---

## 부록 C — Claude P0 표 (화면 재현 열)

| # | 위치 | 결함 | 재현 |
|---|---|---|---|
| 1 | CartItemCard / Summary | 🟦 Blue 재발 | 컴포넌트 ✅ · 화면 미검출 |
| 2 | MenuDetailSummary | legacy+오버플로우 | 컴포넌트 |
| 3 | OptionSelectionRow | 15variant &lt;16 | 컴포넌트 |
| 4 | BottomCTA | opacity 모순 | 컴포넌트 |
| 5 | Category/Tap | Admin혼재 · FAIL11 · Deprecated | 컴포넌트 |
| 6 | Shared | Primitive · raw · Toast스펙 | 컴포넌트 |
| 7 | Allergen | 🟨 저대비 | 컴포넌트 |
| 8 | **SCR-008** | `940×200` 3중 | **화면 최우선** |
| 9~13 | Checkbox·Search·MenuButton·FilterChip·OrderAction | (표기 생략 없이 C원문: ✓부재·150·16·Selected4/7·Primitive) | 컴포넌트/일부화면 |
| 14 | SaveBar 3벌 | ⬛ 불일치 | **화면+이중화** |
| 15 | SCR-011 | SaveBar+Sticky | **신규** |
| 16 | SCR-018 | 이름·좌우 불일치 | **신규** |
| 17 | SCR-009 | 총액 0원 | **신규** |
| ~~18~~ | StatusBadge | 91.7% | **실사용0 → 하향** |
| ~~19~~ | TopHeader | 색반전 | **임팩트↓** |
| ~~20~~ | SalesMetric | 「데이터 연결 예정」 | **화면 미재현** |

---

## 부록 D — Codex 체크리스트

- [ ] 표지 **83/51**
- [ ] `day` (`389:44743`) Variant
- [ ] CategoryTab / Tap 통합
- [ ] `Variant4` · `sourse` · `status3` · `MenuDetailSummary` rename
- [ ] Text Style 연결
- [ ] `auto` lh · 9~10px 제거
- [ ] Kiosk hit **64+**
- [ ] Admin wrapper 웹40 · 태블릿44+
- [ ] 🟩 `#B5E30F` 위 ⬜ white **없음**
- [ ] Deprecated 신규 instance **0**
- [ ] clip=false = overlay 확인
- [ ] 66 Kiosk + 72 Admin 상태 연결

---

## 부록 E — 즉시수정 7 · lh 매핑 · ✅⚠️🔴

| # | 대상 | 판정 | 조치 (E) |
|---|---|---|---|
| 1 | MenuDetailSummary | 🔴🔴 | 뱃지14 · 이름28+ · 가격24+ |
| 2 | OptionGroup/Row | 🔴 | 16~20 · r12 · 체크 |
| 3 | MenuCard | 🔴 | AL · kcal28→16 |
| 4 | SoldOutCard | 🔴🔴 | 9→12+ · 카드 확대 |
| 5 | OrderActionButtons | 🔴 | 환불 outline+confirm |
| 6 | BottomCTA | 🔴 | r20 · 좌우여백 |
| 7 | DataTableRow | 🔴 | Hover Variant |

**lh (E):** 44→54 · 38→46 · 34→44 · 32→40 · 30→38 · 28→36 · 26→34 · 24→32 · 22→28 · 20→28 · 18→24 · 16→24 · 15→22 · 14→20 · 13→18 · 12→16 · 11→16

---

*출처 A~E 의견만 주제별로 묶음. 종합=합의/병기/한출처. 스와치·✅⚠️🔴·🧩🖥️🛠️🛒📊 는 원문 표기를 복원한 것.*
