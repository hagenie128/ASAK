# ASAK Figma 종합 수정 계획 — 사람 중심 + AI 보조

**작성일:** 2026-07-17 (출처 역할 §1 추가: 2026-07-18)  
**근거:** [FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md](./FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md)  
**파일:** `JSrjOy668zhfkiLplCkreh`  
**목표:** AI만으로 전체를 돌리지 않는다. **사람이 결정·손을 대는 일**과 **AI가 측정·일괄·검증하는 일**을 나눠, 제자리걸음을 끊는다.  
**출처 규칙:** 진행 = **C+B+A** / 검증 = **A+D+E** / 병기 = **§3 잠금만** (출처 재투표 금지)

---

## 0. 왜 지금까지 제자리걸음이었나

| 원인 | 결과 |
|---|---|
| AI에게 “전체 QA → 전체 수정”을 반복 | 같은 화면을 다시 측정만 하고, Master는 안 건드림 |
| 출처 A~E **병기(갈등)** 를 AI가 매번 재해석 | 숫자·우선순위가 세션마다 흔들림 |
| 스크린만 고치고 Master는 그대로 | override 재발 (SCR-008이 대표) |
| “문서만 늘리기” | 파일에 쓰기 0회인 채로 계획만 쌓임 |

**이번 계획의 원칙**

1. **결정은 사람** — 병기·브랜드·문구·레이아웃 감각
2. **측정·목록·일괄 치환은 AI** — Blue hex 찾기, Style 미연결 목록, 실측표
3. **한 배치 = 한 Master(또는 한 스크린 override)만** — 끝나면 사람이 눈으로 PASS/FAIL
4. **다음 배치로 가기 전에 문서에 ✅ 표시** — 다시 QA 전체를 돌리지 않음

---

## 1. 출처 적합성 · 실행 기준 · 검증 담당

> 통합본의 A~E는 **전부 쓸모없지만**, 역할이 다르다.  
> “가장 맞는 한 출처”만 고르면 다시 흔들린다. **실행 1개 + 검증 1~2개**로 고정한다.

### 1.1 출처가 뭔지 (한 줄)

| 부호 | 문서 | 한 줄 |
|---|---|---|
| **A** | Cursor 스크린 실측 | 05-C / 06-C **프레임에 실제로 찍힌 숫자** |
| **B** | Cursor 컴포넌트 | Shared / Kiosk / Admin **Master 방향** |
| **C** | Claude v2 | Foundations + **화면 교차** · “Master P0인데 화면엔 0건” 재배치 |
| **D** | Codex 정량 | Variable · Text Style · Variant · hit 수치 |
| **E** | Figma DS QA | 브랜드·터치 감·lh·즉시수정 톤 |

### 1.2 어디가 가장 적합했나 (영역별)

**전체 1등 한 개는 없다.** 아래가 이번 통합본 기준 적합성이다.

| 영역 | 가장 적합 | 왜 |
|---|---|---|
| **스크린 override·실측 FAIL** (008 CTA 940, Toast 299, Dialog 680/440, Modal 400) | **A** | 화면 숫자로 고정. “느낌”이 아니라 W×H |
| **Master 먼저 / 컴포넌트 To-Be** (Blue 금지, Option 스케일, Confirm 키오스크 크기) | **B** | Master→스크린 전파 원칙이 가장 명확 |
| **우선순위 재배치·허위 긴급도 걸러내기** (Badge 실사용0, SalesMetric 미재현, 008·011·018 화면 P0) | **C** | 컴포넌트 QA와 화면 체감을 갈라서 **제자리걸음 방지**에 핵심 |
| **토큰·Style·Variant 구조** (83/51, day, Text Style 97%, hit64) | **D** | 전수 정량. 사람이 빠뜨리기 쉬운 축 |
| **브랜드·즉시 시각 polish** (Summary 스케일, SoldOut 9px, lh 매핑, Confirm 18 Bold) | **E** | “당장 눈에 띄는 것” 목록이 짧고 실행하기 좋음 |

#### 종합 판정 (계획용)

| 순위 | 출처 | 이번 계획에서의 위치 |
|---|---|---|
| ★★★ | **C + A** | **실행 나침반** — C로 “뭐가 진짜 급한지”, A로 “숫자 To-Be” |
| ★★★ | **B** | **Master 수정 기준서** — 컴포넌트 고칠 때 기본 문서 |
| ★★☆ | **D** | **구조·Style 배치(Batch 8) + 회귀 체크리스트** |
| ★★☆ | **E** | **즉시 polish 메뉴** · lh 표 · 단, 병기 숫자는 잠금 후에만 |
| ★☆☆ | (단독 E/D로 전체 진행) | E만 따르면 Tab64·kcal16 등 **병기 과잉** / D만 따르면 화면 체감 P0를 놓침 |

**한 줄:**  
> **진행(무엇을 고칠지) = C가 가리킨 화면 우선 + B Master 규칙 + A 실측 To-Be**  
> **검증(고쳤는지) = A 숫자 재실측 + D 구조 체크 + E 육안/브랜드 샘플**

### 1.3 앞으로 어떤 출처로 계속 진행할지

| 단계 | 주 기준 (Source of Truth) | 보조 | 쓰지 말 것 |
|---|---|---|---|
| 우선순위·배치 고르기 | **C** (화면 재현·하향 반영) | A의 P0 칩 | E 즉시7만으로 전체 순서 바꾸기 |
| Master 수치·정책 | **B** | A(스크린에서 깨진 값), C(토큰 오용) | D hit 64를 모든 버튼에 강제 |
| 스크린 override 수정 | **A** | C(008 3중 override) | B만 보고 스크린 안 열기 |
| Shared size / Toast·Confirm | **B + A** | E(title 18 Bold 등 polish) | D Admin OK를 키오스크 PASS로 착각 |
| Foundations / Style / Variant | **D** | C(Green 스텝≠hex) | E lh를 Style 연결 전에 전 파일 적용 |
| 브랜드·위험동작 polish | **E** | B(라임+다크) | E를 Master 구조 개편의 1순위로 |

**진행 시 고정 문장 (AI·사람 공통)**

```text
이번 배치 Source of Truth = (B|A|C|D|E 중 하나)
검증 = (아래 1.4 표)
병기 충돌 시 = 이 문서 §3 병기 잠금표 (출처 재투표 금지)
```

### 1.4 어떤 출처한테 검증받을지

수정 **끝난 뒤**에만 부른다. 수정 전에 전체 QA 다시 돌리지 않는다.

| 검증 종류 | 담당 출처 (방법) | PASS 조건 예 |
|---|---|---|
| **숫자 회귀** | **A 방식** (프레임 W×H·폰트 px 표) | SCR-008=1080×180 · Toast 키오스크≥400 · Dialog 크기 통일 |
| **긴급도·허위 P0 방지** | **C 방식** (화면에서 재현되나?) | Badge를 화면 P0로 다시 올리지 않음 · 011 이중 바 0 |
| **구조·토큰·Style** | **D 방식** (Variable/Style/Variant 체크리스트) | 라임+흰 0 · Tap 인스턴스 0 · day 오류 해소 |
| **브랜드·터치 감** | **E 방식** (육안 ✅⚠️🔴 + lh 샘플) | Summary/Option/SoldOut 샘플 3화면 PASS |
| **Master 전파** | **B 원칙** + A 실측 | Master 고친 뒤 스크린 override로 다시 깨지지 않음 |

#### 배치별 검증 짝 (복붙용)

| Batch | 실행 기준 | 1차 검증 | 2차 검증(선택) |
|---|---|---|---|
| B1 SCR-008 | **A + C** | **A** 실측 | B(Master 일치) |
| B2 Blue·대비 | **B + C** | **D**(hex 전수) | E(대비 육안) |
| B3 Tap→Tab | **A·B·C·E 합의** | **D**(인스턴스 0) | A(List 화면) |
| B4 Shared size | **B + A** | **A** | E(title/높이) |
| B5 Kiosk Master | **B** | **A**(Detail/Cart/List) | E(즉시 polish) |
| B6 Admin Master | **B + C** | **A**(011 등) | D(wrapper hit) |
| B7 Admin Content | **C + A** | **C**(0원·018 동기) | E(취소 링크 등) |
| B8 Style/AUTO | **D** | **D** | E(lh 샘플 50) |

### 1.5 출처별 “믿되 조심”

| 출처 | 믿어도 되는 것 | 조심 (과신 금지) |
|---|---|---|
| **A** | 스크린에 있는 숫자, Dialog/Toast/CTA FAIL | Master To-Be·브랜드 감각까지 A가 정하진 않음 |
| **B** | Master 규칙, Blue 금지, size 분기 | OptionCard “missing” 등은 이후 A가 정정 → **최신 A와 교차** |
| **C** | 화면 교차로 긴급도 하향/상향, 토큰 적용률 | MCP 한도·일부 미재현 → A로 숫자 재확인 |
| **D** | Style %, Variant, hit 기준, 표지 83/51 | Admin 맥락 OK를 키오스크 PASS로 확장하지 말 것 |
| **E** | 즉시7, lh 표, Confirm 18 Bold, SoldOut 9px | Tab64·kcal16·가격 `#4A7A00` 등은 **잠금 전 단독 채택 금지** |

### 1.6 AI에게 출처를 시키는 말 (복붙)

| 목적 | 프롬프트 |
|---|---|
| 진행 | `Source of Truth는 C(우선순위)+B(Master). A 수치로 To-Be. E/D로 전체 순서 바꾸지 마.` |
| 검증(숫자) | `A 방식으로만 재실측. 표만. 쓰기 0. 새로운 P0 목록 만들지 마.` |
| 검증(구조) | `D 체크리스트: Blue/흰글자/Tap/9px/Style샘플. PASS/FAIL만.` |
| 검증(체감) | `E 즉시7 해당분만 ✅⚠️. 파일 전체 QA 금지.` |
| 금지 | `A~E 전부 다시 통합 QA해서 계획 새로 짜줘` ← **금지** |

### 1.7 파트너 고정 배정 (누가 “나랑 하자”고 해도 이 표만)

> **합치기는 한다. 다만 파트너는 미리 정해 둔다.**  
> 표에 없는 출처가 “전체 메인 할게”라고 하면 → **거절**하고 이 표로 돌려보낸다.

#### 역할 이름

| 역할 | 하는 일 | 한 배치에 몇 명 |
|---|---|---|
| **메인 파트너** | 그 배치의 Source of Truth · To-Be 기준 | **항상 1명만** |
| **검증 파트너** | 끝난 뒤 PASS/FAIL만 | **1명** (필요 시 2명까지) |
| **참견 금지** | 메인이 아닌데 순서·숫자 바꾸려는 출처 | 전부 |

#### 배치별 고정 파트너 (이게 최종)

| 순서 | Batch | 메인 파트너 | 검증 파트너 | 사람이 할 일 |
|---|---|---|---|---|
| 0 | B0 잠금 | **👤 사람** | — | L1~L12 ✅ |
| 1 | B1 SCR-008 | **A** | **C** (화면 재현만) | Figma에서 override 제거 |
| 2 | B2 Blue·대비 | **B** | **D** (hex 전수) | Master에서 색/텍스트 수정 |
| 3 | B3 Tap→Tab | **A** | **D** (인스턴스 0) | Tap 교체·Deprecated |
| 4 | B4 Shared size | **B** | **A** | Toast/Confirm/Modal size |
| 5 | B5 Kiosk Master | **B** | **A** → 샘플만 **E** | Option·Summary·MenuCard·Cart |
| 6 | B6 Admin Master | **B** | **C** → 숫자 **A** | SoldOut·SaveBar·Search |
| 7 | B7 Admin Content | **C** | **A** | 0원·018·문구·gap218 |
| 8 | B8 Style/AUTO | **D** | **E** (lh 샘플) | 샘플 승인 후 확대 |

#### “나랑 하자” 거절 멘트 (복붙)

```text
이 배치는 메인이 (A/B/C/D/E)로 고정이야.
너는 검증만 / 이번 배치 아님.
표: FIGMA_FIX_PLAN §1.7
```

#### 합칠 때 파트너 규칙

| 상황 | 어떻게 |
|---|---|
| A와 B가 숫자 다름 | **메인 파트너 숫자 승** · 그래도 이상하면 사람이 §3 잠금 추가 |
| C가 “긴급도 바꿔” | **B7·우선순위만** C 말 들음. B5 Master 숫자는 B |
| E가 “전체 다시” | **거절**. E는 B5 샘플·B8 lh만 |
| D가 “hit 64 전부에” | **B8·검증만**. B1~B5 순서 바꾸지 않음 |
| 둘 다 메인 하겠다고 함 | **표의 메인만**. 두 번째는 검증이거나 다음 배치 |

#### 한 줄

> **한 배치 = 메인 1 + 검증 1.**  
> 합치기는 **메인이 쓴 To-Be + 검증 PASS**만 L2에 반영. 나머지 의견은 L0 보관.

### 1.8 이후 취합 어떻게 하면 좋은가 (운영 의견)

지금처럼 **출처마다 완성본 QA 문서**를 새로 만들면, 취합할 때마다 갈등이 다시 생기고 계획이 리셋된다.  
앞으로는 **역할이 다른 산출물**만 받고, **살아 있는 문서는 2개만** 유지한다.

#### 문서 3층 (이것만 유지)

| 층 | 문서 | 갱신 빈도 | 누가 |
|---|---|---|---|
| **L0 원본** | `_archive/qa-sources-날짜/` 출처별 raw | 배치/검증 때만 **짧게** | AI |
| **L1 스냅샷** | `FIGMA_QA_UNIFIED_*.md` | **주 1회 또는 큰 마일스톤만** | 사람 승인 후 AI 취합 |
| **L2 실행** | `FIGMA_FIX_PLAN_HUMAN_AI_*.md` (이 문서) | **배치마다 ✅만** | 사람 + AI 초안 |

> **일상 작업은 L2만 본다.** L1은 “논쟁 기록 보관소”, L0는 “증거 박스”.

#### 출처별로는 “같은 양식의 장문”을 만들지 말 것

| 출처 | 앞으로 받을 산출물 (짧음) | 받지 말 것 |
|---|---|---|
| **A** | `VERIFY_A_배치N.md` — 대상 프레임 ID · W×H · px · PASS/FAIL 표만 | 전체 스크린 에세이 |
| **B** | `PATCH_B_Master.md` — 고칠 Master 이름 · As-Is → To-Be · 잠금 ID(L#) | 새 우선순위 전체표 |
| **C** | `TRIAGE_C.md` — 이번 배치가 화면에서 재현되는지 · 하향/유지 3줄 | 새 P0 20개 리스트 |
| **D** | `CHECK_D.md` — Blue/흰글자/Tap/9px/Style 샘플 체크 ☐ | Foundations 장문 재작성 |
| **E** | `EYE_E.md` — 샘플 3화면 ✅⚠️🔴 + lh 이슈만 | 즉시7로 전체 순서 재작성 |

**파일명 예:** `_archive/qa-sources-2026-07-18/VERIFY_A_B1_SCR008.md`

#### 취합 규칙 (갈등 안 나게)

```text
1) 출처 산출물은 L0에만 넣고, design/ 루트에 쌓지 않는다
2) 숫자 충돌 → §3 잠금표에 이미 있으면 잠금 승 / 없으면 사람이 L# 추가 후에만 반영
3) 긴급도 충돌 → C 화면재현이 A 숫자보다 “순서”를 이김 (단, To-Be 숫자는 A)
4) 브랜드·polish 충돌 → E는 제안, 채택은 사람이 잠금에 ✅
5) L1 UNIFIED는 “전체 다시 쓰기” 금지 → 변경된 주제 섹션만 diff 패치
6) L2 FIX_PLAN은 배치 DoD·잠금·출처 역할만 고친다 (QA 본문 복사 금지)
```

#### 추천 주기

| 언제 | 무엇을 |
|---|---|
| **배치 끝날 때마다** | A 또는 D 검증 짧은 표 → L2 체크리스트 ✅ |
| **주 1회** | C triage 1장 + A 회귀 핵심 6항 (008, Tap, Blue, 흰글자, 9px, Toast) |
| **마일스톤** (예: Kiosk Master 끝) | L1 UNIFIED에 **해당 챕터만** 패치 · 전체 재생성 금지 |
| **절대** | A~E에게 각각 “FINAL 완결본” 5개 동시 생성 |

#### 취합 담당 (사람 vs AI)

| 일 | Owner |
|---|---|
| L0 짧은 검증 표 생성 | 🤖 |
| 잠금 추가·배치 ✅ | 👤 |
| L1에 섹션 패치 초안 | 🤖 (사람: “이 섹션만 패치해”) |
| L1 통째 재작성 / 새 종합계획 리셋 | ❌ 금지 |

#### 한 줄 운영 철학

> **출처는 의견을 내는 센서고, 취합본은 재판이 아니다.**  
> 센서(A~E)는 짧은 신호만 보내고, **판결은 잠금표 + FIX_PLAN**이 한다.

---

## 2. 역할 분담 (누가 뭐가 빠른가)

### 👤 사람이 고치는 게 더 빠른 것

> Figma에서 **클릭 몇 번·눈 보고 판단**이 핵심인 일. AI에게 맡기면 MCP 왕복·재실측으로 느려짐.

| 유형 | 예시 | 이유 |
|---|---|---|
| **한 프레임 override 제거** | SCR-008 CTA `940×200` → Master `1080×180`로 인스턴스 리셋 | 눈으로 잡고 Detach/Reset이 10초 |
| **병기 숫자 고르기** | Tab 높이 52 vs 64 · kcal 16 vs 20~24 · BottomCTA r12 vs r20 | 브랜드/터치 감각은 사람 |
| **문구·콘텐츠** | Empty「새로고침」→「메뉴 담으러 가기」· Delete 다이얼로그에 메뉴명 | 카피·맥락은 사람 |
| **레이아웃 감각** | gap 218 재배치 · Complete 여백 · Home radius | “예쁘다/답답하다”는 사람 |
| **Deprecated 정리** | CategoryTap 캔버스에서 치우기 · legacy state 숨기기 | 파일 구조 판단 |
| **Quick visual polish** | Confirm title Medium→Bold · radius 0→12 · Tag r4→8 | 단일 프로퍼티 수정 |
| **최종 육안 검수** | 키오스크 1080 프리뷰 · 관리자 1920 훑기 | PASS 도장은 사람 |

### 🤖 AI가 처리하는 게 더 정확·실수 적은 것

> **전수 검색·수치 비교·목록화·일괄 규칙 적용**. 사람이 하면 빠뜨리기 쉬움.

| 유형 | 예시 | 이유 |
|---|---|---|
| **금지색 전수 탐색** | `#3B82F6` `#0088FF` · accents · 라임+흰 텍스트 | hex 빠뜨림 방지 |
| **실측 vs 스펙 표** | Toast 299 vs 420 · Modal 400 vs 480 · SoldOut 9px×N | 숫자 기계가 정확 |
| **Text Style 미연결 목록** | 97%+ AUTO/미연결 노드 ID 리스트 | 수천 노드 사람이 못 함 |
| **Variant/Property 오류** | `day` Variant · 오타 prop · legacy state 목록 | API로 구조 읽기 |
| **토큰 바인딩 점검** | Primitive 직접 사용 · Semantic 누락 · Warning 대비 계산 | 대비비·토큰 이름 |
| **배치 후 회귀 체크** | “이 Master 고친 뒤 인스턴스 N개 수치” 표 | 사람 눈 보조 |
| **체크리스트 갱신** | 배치 끝나면 이 문서의 ✅/⬜ 업데이트 초안 | 문서 동기화 |

### 🤝 같이 (사람 결정 → AI 실행 → 사람 PASS)

| 흐름 | 예 |
|---|---|
| 사람이 **To-Be 숫자 확정** → AI가 Master에 일괄 반영 → 사람 스크린 확인 | CartItemCard Blue 제거 규칙 |
| 사람이 **통합 방향** → AI가 3벌 SaveBar 차이표 → 사람 1벌 디자인 → AI가 인스턴스 교체 목록 | SaveBar |
| AI가 **문제 노드 ID 목록** → 사람이 Figma에서 수정 → AI가 재실측만 | OptionRow 15px 전수 |

---

## 3. 병기 잠금 (다시 논쟁하지 말 것)

출처 A~E가 갈리는 항목은 **아래에서 잠근다.**  
잠그기 전에는 AI에게 “알아서 고치라”고 하지 않는다. **잠근 뒤에만** 수정 배치에 넣는다.

| # | 주제 | 잠금 결정 (2026-07-17 제안) | 확정자 |
|---|---|---|---|
| L1 | CategoryTab 높이 | **일단 52 유지** (B/C PASS). 64는 2차 | ⬜ 사람 |
| L2 | MenuCard kcal | **20** (B 20~24 중간). E의 16은 관리자 denser 때만 | ⬜ 사람 |
| L3 | MenuCard 가격색 | **`#6C9700`** (B·C 합의). E `#4A7A00` 보류 | ⬜ 사람 |
| L4 | BottomCTA radius | **16** (B). pill r20은 E 2차 | ⬜ 사람 |
| L5 | Error CTA 색 | **라임+다크텍스트** (A·B). E dark 단색은 관리자용만 | ⬜ 사람 |
| L6 | Confirm title | **18 Bold** (E). 키오스크 size variant에서만 22 | ⬜ 사람 |
| L7 | StatusBadge 긴급도 | **Master만 고침 · 화면 P0 아님** (C 실사용0) | ⬜ 사람 |
| L8 | gap218 | **사람이 Live Order 레이아웃으로 재배치**. 숫자만 줄이지 않음 | ⬜ 사람 |
| L9 | Payment border 4px | **유지** (B 모범). Scale Heavy3 초과는 문서 메모만 | ⬜ 사람 |
| L10 | Purple | **Category/Dressing만 허용**. 그 외 삭제 | ⬜ 사람 |
| L11 | Warning 텍스트 | Semantic **`#92400E`** (C 예시) 채택 | ⬜ 사람 |
| L12 | Toast 키오스크 | size=`kiosk` **폭≥400 · 본문≥16 · 높이≥80** | ⬜ 사람 |

> **사용법:** 위 표에서 본인이 OK면 ⬜→✅. AI 수정 프롬프트에는 **✅만** 넣는다.

---

## 4. 작업 순서 (절대 규칙)

```text
① Foundations / 잠금결정
② Shared Master
③ Kiosk Master
④ Admin Master
⑤ 스크린 override 제거 (Master 반영이 안 된 곳만)
⑥ Content·문구·데이터(0원 등)
⑦ Text Style / AUTO 일괄 (마지막에 AI 대량)
```

**금지**

- Master 안 고치고 스크린만 AI로 “예쁘게”
- 배치 중간에 전체 QA 재실행
- 잠금 안 된 병기를 AI가 임의 선택

---

## 5. 배치 계획 (실행 단위)

각 배치: **Owner** · **예상 시간** · **완료 조건(DoD)** · **AI에게 시킬 말**

### Batch 0 — 잠금 + 출처 역할 확인 (👤 30분)

| 할 일 | Owner |
|---|---|
| §1.2~1.4 읽기: 진행=C+B+A, 검증=A+D+E | 👤 |
| §3 잠금표 L1~L12 ✅ 찍기 | 👤 |
| Figma 파일 백업/브랜치 또는 버전 히스토리 메모 | 👤 |
| Deprecated CategoryTap 위치 눈으로 확인 | 👤 |

**DoD:** 출처 역할 이해 · 잠금표 ✅ 8개 이상 · “오늘은 Batch 1만” 선언  
**검증 출처:** 없음 (아직 수정 전)

---

### Batch 1 — 화면 최우선 1건: SCR-008 override (👤 15분)

| As-Is | To-Be |
|---|---|
| Complete CTA `940×200` | Master BottomCTA `1080×180` 인스턴스 · override 제거 |

**Owner:** 👤만 (AI 불필요)  
**DoD:** 프레임 실측 1080×180 · variant/타이포 override 없음  
**AI 역할:** 끝난 뒤 “재실측만” 요청 가능 (수정 금지)

---

### Batch 2 — 대비·위험색 (👤 결정 + 🤖 전수)

| 할 일 | Owner |
|---|---|
| ConfirmDialog warning: 라임+**흰** → 라임+**다크** (`#0D0D0D`/`#292D30`) | 👤 Master 수정 |
| Allergen WarningText 토큰 적용 (`#92400E`) | 👤 or 🤖 바인딩 |
| Blue `#3B82F6`/`#0088FF` **전수 목록** | 🤖 |
| 목록 보고 CartItemCard / Summary에서 Blue 제거 | 👤 (또는 🤖 일괄 후 👤 검수) |

**DoD:** 라임+흰 0건 · Cart Blue 0건(목록 기준)  
**AI 프롬프트 예:**  
`읽기만: Blue #3B82F6 #0088FF 노드 ID·컴포넌트명 표로. 쓰지 마.`

---

### Batch 3 — CategoryTap → Tab (👤 구조 + 🤖 인스턴스 목록)

| 할 일 | Owner |
|---|---|
| Tap Deprecated · 캔버스에서 정식 사용 금지 | 👤 |
| Menu List 등 Tap×4 → CategoryTab 교체 | 👤 (화면당 빠름) |
| 남은 Tap 인스턴스 0인지 전수 | 🤖 |

**DoD:** Tap 인스턴스 0 · Tab만 · page=A는 Admin 분리 확인  
**잠금:** L1 (높이 52)

---

### Batch 4 — Shared size 분기 (👤 Master + 🤖 스펙표)

| 컴포넌트 | To-Be (잠금) | Owner |
|---|---|---|
| Toast | Admin 유지 · **kiosk** size ≥400×80 · 본문≥16 | 👤 variant 추가 |
| ConfirmDialog | 키오스크 560~680 통일 · title 18 Bold · Cart Clear/Delete 크기 통일 | 👤 |
| Modal 스크린 400×220 | Master 480 쪽으로 리셋 | 👤 |
| Empty/Error | radius 12 · CTA 문구 type별 · 키오스크 ≥16 | 👤 문구 + radius |

**AI:** 수정 전·후 폭/높이/폰트 표만  
**DoD:** Cart Dialog 한 크기 · Toast 키오스크 FAIL 해소

---

### Batch 5 — Kiosk Master 터치·타이포 (👤 메인)

우선순위 (합의 P0):

1. **OptionGroup/Row** — 본문 16+ · selected border 3px 라임 · 체크  
2. **MenuDetailSummary** — 뱃지14+ · 이름28+ · 가격24+ · Blue 제거 · legacy state 분리  
3. **MenuCard** — r16 · kcal→20 · lh 명시 · soldOut 다운톤  
4. **CartItemCard** — 액션 ≥16 · 48 pill · gap 스케일 · MenuButton wrap/금지  
5. **BottomCTA** — pad32 · r16 · loading≥16 · opacity disabled 제거  

**Owner:** 👤 Master 편집  
**AI:** 각 컴포넌트 “수정 전 실측 1장”만 · 수정은 사람이  
**DoD:** 해당 Master variant 대표 1개씩 사람이 터치 프리뷰 PASS

---

### Batch 6 — Admin Master (선택적 긴급)

| 할 일 | Owner | 비고 |
|---|---|---|
| SoldOutCard 9px → ≥12 · 카드 ~150×160 | 👤 | P0 |
| SaveBar 3벌 → **1 세트** 방향 스케치 | 👤 | AI는 차이표만 |
| SCR-011 SaveBar+Sticky 이중 제거 | 👤 | 화면 |
| Search Master 150 → 240~320 | 👤 | |
| Checkbox ✓ + hit 40/44 | 👤 | |
| StatusBadge 오라벨 | 👤 Master만 (L7) | 화면 P0 아님 |
| Navbar shadow 1겹 | 👤 | |

**AI:** SaveBar 3벌 hex/state 비교표 · 9px 노드 전수  
**DoD:** Sold-out 화면 9px 0 · 011 이중 바 0

---

### Batch 7 — 관리자 화면 Content / 데이터 (👤)

| 화면 | 할 일 | Owner |
|---|---|---|
| SCR-009 | 총액 0원 → 실합계 표시(목데이터) · 이중 알림 정리 · 취소 링크화 | 👤 |
| SCR-018 | Toggle 이름·좌우 동기 · SaveBar 톤 | 👤 |
| SCR-016 | 복붙·메뉴명·Empty CTA「새 메뉴 추가」 | 👤 |
| Live gap218 | 레이아웃 재배치 | 👤 (L8) |

**AI 금지에 가깝다:** 목데이터·레이아웃은 사람이 빠름.  
**AI 가능:** “0원인 텍스트 레이어 ID” 찾기만.

---

### Batch 8 — Foundations / Style 대량 (🤖 메인 + 👤 샘플 검수)

| 할 일 | Owner |
|---|---|
| 표지 80/47 → 83/51 또는 기준 문구 | 👤 한 줄 |
| Green 스텝명 vs hex 문서 정합 | 🤖 표 + 👤 채택 |
| Text Style 14종 연결 대상 목록 | 🤖 |
| AUTO lh → E 매핑표로 **샘플 50노드** 적용 실험 | 🤖 제안 → 👤 승인 후 확대 |
| `day` Variant 오류 해소 | 🤖 진단 → 👤 확인 |

**DoD:** Style 연결률 “목록 기준” 개선 수치 기록 · 전 파일 일괄은 승인 후에만

---

## 6. 하루 루틴 (제자리걸음 방지)

```text
1. 오늘 배치 번호만 고른다 (예: Batch 1+2만)
2. Source of Truth·검증 출처를 §1.4에서 고른다
3. 잠금표에 없는 숫자는 고치지 않는다
4. 사람 수정 30~90분
5. AI에게는 “재실측 / 남은 Blue·Tap·9px 목록”만 (쓰기 금지 기본) — 출처 A 또는 D 방식
6. 이 문서 배치 DoD에 ✅
7. A~E 전체 QA 통합은 다시 돌리지 않는다 (주 1회 회귀만)
```

### AI에게 시키면 안 되는 말

- ❌ “Figma 전체 QA하고 전부 고쳐줘”
- ❌ “병기된 거 알아서 골라서 반영해”
- ❌ “Master랑 스크린 다 맞춰줘”
- ❌ “A~E 다시 통합해서 계획 새로 짜줘”

### AI에게 시키면 되는 말

- ✅ “Batch 2: Blue hex 노드 ID 표만. 쓰기 0. 검증=D”
- ✅ “SCR-008 CTA 지금 실측 W×H만. 검증=A”
- ✅ “SoldOut 9px 이하 텍스트 전수 개수”
- ✅ “Batch 5 OptionRow 수정 후 폰트 실측 표. Source=B, 검증=A”

---

## 7. 우선순위 한눈에 (이번 주 vs 나중)

### 이번 주 (체감·재발 차단)

| 순위 | 항목 | Owner |
|---|---|---|
| 1 | SCR-008 CTA override | 👤 |
| 2 | 라임+흰 / Cart Blue | 👤+🤖목록 |
| 3 | CategoryTap 제거 | 👤+🤖검증 |
| 4 | Toast·Confirm 키오스크 size | 👤 |
| 5 | Option·Summary·MenuCard Master | 👤 |
| 6 | SoldOut 9px · SaveBar 이중 | 👤 |

### 나중 (정확하지만 체감 느림)

| 항목 | Owner |
|---|---|
| Text Style 97% 연결 | 🤖→👤샘플 |
| AUTO lh 전수 | 🤖 |
| StatusBadge Master 라벨 | 👤 (급하지 않음) |
| SalesMetric / TopHeader | 하향 (C) |
| Tab 높이 64 · CTA pill20 | 2차 잠금 후 |

---

## 8. 진행 체크리스트 (복사해서 쓰기)

### 잠금

- [ ] L1 Tab 52
- [ ] L2 kcal 20
- [ ] L3 가격 `#6C9700`
- [ ] L4 BottomCTA r16
- [ ] L5 Error CTA 라임+다크
- [ ] L6 Confirm 18 Bold
- [ ] L7 Badge Master-only
- [ ] L8 gap218 사람 레이아웃
- [ ] L9 Payment 4px 유지
- [ ] L10 Purple Dressing only
- [ ] L11 Warning `#92400E`
- [ ] L12 Toast kiosk size

### 배치

- [ ] B0 잠금·백업
- [ ] B1 SCR-008
- [ ] B2 대비·Blue
- [ ] B3 Tap→Tab
- [ ] B4 Shared size
- [ ] B5 Kiosk Master
- [ ] B6 Admin Master
- [ ] B7 Admin Content
- [ ] B8 Style/AUTO

### 회귀 (주 1회, AI 읽기 전용 · 출처 A+D+E)

- [ ] (A) SCR-008 = 1080×180
- [ ] (D) Tap 인스턴스 0
- [ ] (D) Blue 금지 hex 0 (키오스크 Cart/Summary)
- [ ] (D) 라임+흰 0
- [ ] (A) SoldOut 9px 0
- [ ] (A) Toast 키오스크 ≥400
- [ ] (C) Badge/SalesMetric을 다시 화면 P0로 올리지 않음
- [ ] (E) Summary·Option·SoldOut 샘플 육안 PASS

### 출처 역할 (매 배치 시작 전)

- [ ] 이번 배치 Source of Truth 정함 (B1=A+C / B5=B / B8=D …)
- [ ] 1차 검증 출처 정함 (§1.4 표)
- [ ] A~E 전체 재통합 QA **안 함**

---

## 9. 관련 문서

| 문서 | 역할 |
|---|---|
| [FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md](./FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md) | 문제 근거 (읽기 전용 기준) |
| [FIGMA_QA_IMPLEMENTATION_FINAL_cluade_2026-07-17.md](./FIGMA_QA_IMPLEMENTATION_FINAL_cluade_2026-07-17.md) | Claude 재실측 원본 |
| **이 문서** | **누가·무슨 순서로·멈추는 선** |

---

## 10. 한 줄 요약

> **한 배치 = 메인 파트너 1명 + 검증 1명 (§1.7 표).**  
> 진행 = C+B+A / 검증 = A+D+E / 병기는 잠금만.  
> “나랑 하자”는 표에 없으면 거절.

---

*다음 액션: B0 잠금 → **B1 메인=A, 검증=C** 로 SCR-008만.*
