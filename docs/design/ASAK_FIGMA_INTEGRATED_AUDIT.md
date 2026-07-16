# ASAK Figma 05-C/06-C 통합 감사 — 시각 복구 · 컴포넌트 정본 · 유저플로우/정책 갭 · Admin 인사이트

> **작성일:** 2026-07-17 (Cursor 실측 + Claude 교차검증, 2026-07-17 4개 문서 병합)
> **역할:** Product/UX 분석 + Design Director 지시 + QA 검수 기준 + 컴포넌트 정본 + 유저플로우/정책/핸드오프 갭 + Admin 데이터 위젯 제안
> **범위:** Figma·코드 직접 수정 없음. `C:\ASAK-workspace\figma` PNG/PDF 실측 + Figma MCP 실측 + Product Bible + ASAK-Kiosk/ASAK-Admin/ASAK-back 코드 + 대화 분석 통합
> **목표 명칭:** Commercial Food Kiosk Visual System Refinement (리브랜딩 금지)
> **통합 이력:** 원래 4개 문서(`ASAK_FIGMA_VISUAL_RECOVERY_FULL_AUDIT.md`, `ASAK_COMPONENT_CANONICAL_INVENTORY.md`, `ASAK_FLOW_POLICY_IMPLEMENTATION_GAP.md`, `ASAK_ADMIN_INSIGHT_SECTIONS.md`)로 나뉘어 있었으나 2026-07-17에 이 파일 하나로 병합했다. 원본 4개 파일은 삭제됐다.

---

## 이 문서 구성 (Part A~D)

| Part | 제목 | 핵심 내용 |
|---|---|---|
| Part A | 시각 복구 전체 감사 | 화면별 시각 문제, Batch 실행 지시서, 코드 재검증, UX/Edge Case, Handoff 체크리스트 |
| Part B | 컴포넌트 정본 · Instance Swap 매핑 | Figma MCP 실측 Legacy→Final 매핑, 메뉴 이미지 Instance Swap 계획 |
| Part C | 유저플로우 · 정책 · 핸드오프 갭 | 정책 vs 구현 vs 시안 충돌, 구현 백로그(Wave), 실무 트리아지 통합 우선순위 |
| Part D | Admin 데이터 위젯 제안 | 신규 데이터 계약 없이 가능한 Admin Dashboard/화면별 위젯 제안 |

**시작점:** 급하면 Part C §12 "실무 트리아지 기준과 통합 우선순위"부터 본다(문서 내 검색: `## 12. 실무 트리아지`). Figma Agent에게 실행 지시서를 던질 때는 Part A §12 "Figma Agent 복사 블록"부터 순서대로 던진다(검색: `## 12. Figma Agent 복사 블록`).

---

# Part A: 시각 복구 전체 감사


> **작성일:** 2026-07-17  
> **역할:** Product/UX 분석 + Design Director 지시 + QA 검수 기준  
> **범위:** Figma 직접 수정 없음. `C:\ASAK-workspace\figma` PNG/PDF 실측 + Product Bible + 클로드 대화 분석 통합  
> **목표 명칭:** Commercial Food Kiosk Visual System Refinement (리브랜딩 금지)

---

## 0. 이 문서 쓰는 법

1. **Figma Agent에게는** §12 복사 블록부터 배치 순서대로 던진다.
2. **검수할 때는** §11 QA 검수표로 PASS/FAIL 판정한다.
3. **화면 단위로 고칠 때는** §5~§8 페이지별 수정표를 본다.
4. **시스템 근본 원인은** §9를 먼저 이해한다.

### Source of Truth

| 구분 | 정본 |
|---|---|
| Visual | 기존 승인 화면(B) + Product Bible |
| Logic / State | 05-C / 06-C 최신 State + ASAK 정책 |
| Component | **02-C / 03-C / 04-C만** — 사용 실측·Legacy→Final 매핑은 Part B (아래) |
| Token | **01-C Variable만** (Color, Type, Spacing, Radius, Effect) |
| Font | **Pretendard Variable만** |

> **컴포넌트:** “써야 한다”만 적지 말고, 05-C/06-C에 **실제로 쓰인** Instance까지 공식 인벤토리에 기록한다. 정본은 구분선(`---`) 위 C 페이지만.

### 금지 (절대)

- Instance Detach  
- Production에서 Legacy/Deprecated Component 사용  
- 02~04-C 밖·다른 파일 Component 참조 유지  
- Hardcoded hex (01-C 미연결)  
- Selected에 Blue  
- 카드/옵션/카트 전체 Dark Charcoal Fill  
- 품절 = 카드 전체 검정·블러·과도 opacity  
- 새 Component Set 중복 생성  
- Receipt / Membership / Coupon / QR / Delivery 추가  
- 07-C 구조 변경(Deprecated 표기만 허용)  
- Frame 크기 변경 (Kiosk 1080×1920 / Admin 1920×1080)  
- Apple / Linear / Vercel 복제, Glass / Neon / Gradient 추가  
- C 폐기 후 B 복구

### 화면 크기 정본

| Domain | Size | BottomCTA |
|---|---|---|
| Kiosk | 1080 × 1920 Portrait | y=1740, h=180, bottomEdge=1920 |
| Admin | 1920 × 1080 Landscape | Kiosk BottomCTA 사용 금지 |

### Touch Target

- Kiosk: **≥ 64px** (가능하면 Bible 기준 80×80)  
- Admin: Desktop 밀도 유지, Kiosk 초대형 버튼 복제 금지

---

## 1. 프로젝트 이해 (짧게)

### Bible 핵심 원칙 (8)

1. Product Before Decoration  
2. One Screen, One Decision  
3. State Is Part of the Product  
4. Recovery Over Blame  
5. Server Is the Price Authority  
6. Lime/Green Is Accent only (CTA·Selected·Active)  
7. Food(Kiosk) / Data(Admin) are Heroes  
8. No Hidden Business Logic + Scope Discipline  

### C버전을 만든 이유 (5)

1. Screen State 확장 (loading/empty/error/soldOut/processing 등)  
2. Cart·Option·Sold-out 로직·데이터 계약 반영  
3. Component/Variant 정본화  
4. Prototype·Handoff·`__spec` 보완  
5. 01-C~04-C + 07-C QA Matrix 연결  

### B vs C

| | B | C |
|---|---|---|
| 역할 | 승인된 시각 시안 | 구현·상태·정책 정본 |
| 유지 | 밝음·음식 중심·White/Warm Neutral/Lime | State·로직·정책 |
| 이번 작업 | 시각 레퍼런스 | 기능 유지 + 시각 복구 |

### 주문 흐름 정본

```text
Home → 매장 식사/포장 선택 → orderType 저장 → Menu List 직접 이동
```

재확인 Modal/화면은 **제거 대상**. React(`OrderTypeSelector`)도 선택 즉시 `/menu` 이동.

### Cart 정책 요약

- qty≥2: Minus로 1 감소 / qty=1: Minus disabled / 삭제 별도  
- qty 0 금지 / 동일 menuId 최대 9 / Cart 전체 최대 30  
- **직원 문의 문구는 전체 30 초과 시도에만** (코드 MENU_LIMIT에도 직원 문구 있음 → 카피 정합 필요)  
- 옵션 수정 = `cartItemId` + `updateCartItem` / 수정 중 `addCartItem` 금지  
- 전체 비우기 제공  

### Sold-out 정책 요약

| 유형 | List | Detail | Cart |
|---|---|---|---|
| 메뉴/핵심재료 | soldOut | 전체 주문 불가 | edit=false, delete=true, CTA disabled |
| 일반재료/옵션 | 정상 | 해당 옵션만 disabled | edit=true, delete=true, CTA disabled |
| Base 일부 | 정상(전원 품절 시 soldOut) | 해당 Base만 disabled | — |
| 담은 후 품절 | — | — | 자동삭제 금지, 해결 전 결제 차단 |

### 기타 정책

- Processing 중 Timeout 비활성  
- TTS 실패 → 주문 상태 Rollback 금지  
- 주문방식: EAT_IN / TAKE_OUT만  

### 찾지 못한 것

- 별도 파일명 `Implementation Final`, `Kiosk/Admin Screen Bible` 단독 문서  
- 이번 export에 **01-C Foundations** 폴더 없음 → Variable 하드코딩 여부는 Figma Agent 확인  
- Node ID `150:*`, `4:*` Legacy는 문서 텍스트에 없음 → Figma 전수 확인  
- Admin `Checkbox.png`, `Deprecated/Admin-EmptyState.png` 투명 export → 재export 필요  

---

## 2. 총괄 결론 (두 분석 합의)

1. **“로직만 늘고 시각이 무너졌다”는 진단은 맞다.**  
2. **“모든 품절이 검다”는 과장**이다. Menu List/Detail 일부·Admin Ingredient는 Badge 방향이 맞다.  
   진짜 다크 문제는 **Confirm scrim 불투명 검정, OrderCard 캔버스, SaveBar/TopHeaderItem, OptionSelectionRow default 다크, Home 다크 캔버스**에 집중.  
3. **가장 반복적인 시스템 실패는 Lime Accent 붕괴** (amber/olive/red/blue/black이 Primary에 혼용).  
4. **두 번째는 Legacy/Deprecated 혼용** (CategoryTab/Tap, Badge, Deprecated MenuCard).  
5. **세 번째는 Text Clip / Overlap / BottomCTA 높이 불일치**.  
6. C State·정책은 유지하고, **02~04-C 밝은 정본 + 01-C 토큰**으로 Production만 다시 꽂는다.

---

## 3. 전체 문제 목록 (문제군)

### [P0] 주문방식 재확인 중복 + Layer Overlap

- **분류:** 주문 흐름 / Prototype 잔재  
- **위치:** SCR-001 Home / Order Type Selection (`224:10766` 후보), Modal (`224:10870` 후보), Home `134:7721`, 버튼 `134:7788`  
- **PNG 실측:** 모달 뒤 Ghost 카드 겹침, Selected=Blue, 포장 영문 "Eat In"  
- **Bible/코드:** Home에서 orderType 확정 후 `/menu` 직행. 재확인 정책 없음.  
- **권장:** Prototype 직결, Selection Frame Archive, Ghost 제거, Lime Selected, Take Out 카피  
- **영향:** SCR-001, SCR-003 진입  
- **확실도:** 정책·PNG **확인 완료** / Node 실물은 Figma 전수  

### [P0] 품절·다크 Surface 위반 (선택적 위치)

- **분류:** Sold-out / Surface  
- **위치:** MenuCard soldOut(블러·회색), SCR-003 Sold-out(다크 오버레이), CartItemCard soldOut(연두 워시·비가독), OptionSelectionRow default 다크, Discard/Disable-all Confirm **불투명 검정 scrim**, Admin OrderCard 검정 캔버스, SaveBar/TopHeaderItem 다크  
- **권장:** White Surface 유지 + 이미지만 채도↓ + Badge. Scrim=반투명. 대형 Dark Fill 금지  
- **확실도:** PNG **확인 완료**

### [P0] Menu Detail 옵션명 잘림 + kcal 겹침 + 위계 붕괴

- **분류:** Text Clipping / Hierarchy  
- **위치:** SCR-004 Default / Option Selected / Ingredient·Base·Menu Sold-out  
- **실측:** 오리엔/탈, 아보카/도, 훈제연/어, 두부큐/브; 0kcal 오버랩; 0g/000원 하드코딩  
- **권장:** Name FILL max 2줄, Price 고정폭, kcal 전용 슬롯, 03-C Option 밝은 Set  
- **확실도:** PNG **확인 완료**

### [P0] CartItemCard 과복잡 + 품절 비가독 + 작은 터치

- **분류:** Cart Component  
- **위치:** 03-C CartItemCard, SCR-005 Default/Sold-out/Edit Required/Checkout Blocked  
- **실측:** 6단 정보, 아보카도 중복, edit/delete 과소, stepper 스타일 불일치, 연두 워시  
- **권장:** summary 3줄, touch≥64, State별 showEdit 정책 시각 일치  
- **확실도:** PNG **확인 완료**

### [P0] Payment Processing / Error State 충돌

- **분류:** Payment  
- **위치:** SCR-007 Processing, SCR-012 Declined/Network Failure  
- **실측:** Processing인데 CTA 활성 톤; Error인데 “처리 중” 카피 잔존; 모달 버튼 소형; 재시도=Red(의미 충돌)  
- **권장:** Processing CTA Disabled; Error 카피 정리; Retry=Lime/Charcoal; Modal touch≥64  
- **확실도:** PNG **확인 완료**

### [P0] Admin Dashboard KPI Clip + Sold-out Disable-all 검정 Scrim

- **분류:** Admin Clip / Modal  
- **위치:** SCR-022 Default, SCR-011 Disable-all Confirm  
- **실측:** KPI 잘림·4카드 vs Partial Data 5카드 불일치; Confirm 불투명 검정+amber 버튼  
- **확실도:** PNG **확인 완료**

### [P0] Admin OrderCard / SaveBar / TopHeaderItem 다크 + StickyActionBar 중복

- **분류:** Admin Component Dark / 중복  
- **위치:** 04-C OrderCard, SaveBar, TopHeaderItem, StickyActionBar  
- **권장:** Light Surface, SaveBar 통합, OrderCard CTA Admin 사이즈  
- **확실도:** 클로드 PNG 분석 **확인 완료**

### [P1] Lime Accent 전역 붕괴

- **위치:** Login 올리브, Confirm amber/red, Payment Retry red, SalesPeriodFilter 검정, Navbar promo 검정, DatePicker/Toggle 올리브, Home Selected blue, OptionSelectionRow selected blue, Menu List 가격 전부 Lime  
- **권장:** Primary/Selected/Active = 01-C Lime Variable만. Hardcoded hex 제거  
- **확실도:** 다수 화면 **확인 완료** / 01-C Variable 정의는 Figma 확인  

### [P1] Legacy / Deprecated / 이름 중복 혼용

- **위치:** Deprecated MenuCard; CategoryTab / CategoryTap / Category; Admin-Badge ≈ StatusBadge; Legacy BottomCTA/OrderDetailRow 후보 `4:*` vs `150:*`  
- **권장:** Production 연결 0, Deprecated annotation, 단일 정본만  
- **확실도:** 일부 PNG **확인 완료** / Instance 전수는 Figma  

### [P1] BottomCTA 높이·Variant 불일치 + Toast가 CTA 가림

- **위치:** SCR-003/005/007/012, Showcase BottomCTA 4종, Save Error / Checkout Blocked Toast  
- **권장:** y=1740 h=180 전수; Toast는 CTA 위 ≥16px  
- **확실도:** 패턴 **확인 완료** / 전 Frame 좌표는 Figma  

### [P1] Menu List 데이터·Footer 불일치 + 하드코딩

- **위치:** SCR-003 Default — 주문내역 2개 vs Footer 0개/0원; 9장 동일 메뉴; 이미지-이름 불일치  
- **확실도:** PNG **확인 완료**

### [P1] Admin Nav Active 오류 + Detail 0원 + Refund/영수증 Future

- **위치:** SCR-010/011 Sidebar Home Active; Detail 총액 0원; Refund/Print Receipt  
- **확실도:** PNG **확인 완료**

### [P1] Admin Enum 밖 상태 (취소/환불/결제완료)

- **위치:** SCR-009/010 Status Badge  
- **권장:** RECEIVED/PREPARING/COMPLETED + READY/APPROVED/FAILED만. 나머지는 `__manual-check`  
- **확실도:** 문서·화면 **확인 완료**

### [P1] Sales KPI 미확정 + 헤더/표 비동기 + Loading 레이아웃 오류

- **위치:** SCR-019/020/021  
- **확실도:** 감사문서 + 클로드 PNG **확인 완료**

### [P1] Shared Toast 상태 구분 불가 + 다크 통일 필

- **위치:** 02-C Toast; SCR-011/016 이중 Toast  
- **권장:** 톤별 아이콘/좌측 바 + 밝은 Surface; Production 단일 Toast  
- **확실도:** 클로드 PNG **확인 완료**

### [P1] OptionSelectionRow / HomeActionButton / QuantityStepper

- **OptionSelectionRow:** default 다크 + selected Blue  
- **HomeActionButton:** 포장 영문 Eat In  
- **QuantityStepper:** 48px 문서화 → Kiosk 64+로 상향  
- **확실도:** PNG **확인 완료**

### [P1] Admin SoldOutCard 정본 부재

- **위치:** 04-C SoldOutCard — dim/Badge 없음  
- **확실도:** 클로드 PNG **확인 완료**

### [P2] SCR-001 Home 다크 히어로 Canvas 무게

- 음식 히어로는 유지 가능하나 **전체 Dark Theme로 읽히면 Fail**. Light Neutral + 음식 영역 제한.  
- **확실도:** PNG **확인 완료**

### [P2] SCR-008 Complete 양호 / receipt State 메타 Future

- 시각 PASS에 가까움. receiptPrint는 Future Scope 표기.  

### [P2] SCR-015 Unauthorized Empty 오용 / Login 올리브 Primary

### [P2] SCR-016 네온 글로우 export 잔존

### [P2] Cart/Payment 금액·결제수단 하드코딩·미확정 수단 (과거 감사)

### [P2] Sold-out 저장 문구 오타 가능 (“저장 변경할까요?”)

### [P2] Spec/Route annotation Production 노출 (다수)

### [P2] Live Order KDS 초대형 + placeholder menu name / 0원

### [P2] QA 수치 vs 실제 Node 불일치 (Figma Agent 전수)

### 시각 항목 — 추가 전수 필요

Text clip 전 Frame, BottomCTA 전 좌표, Instance source 전수, 01-C Variable bind, Non-Pretendard, Checkbox/EmptyState 재export.

---

## 4. 디자인 시스템 개선 방향 (각 최대 3줄)

- **Surface:** Canvas=밝은 Neutral, Card=White. 대형 Dark/풀라운드 SaaS 패널 금지.  
- **Typography:** Pretendard Variable만. Charcoal 본문. 옵션명 max 2줄. 임의 축소 금지.  
- **Spacing:** 01-C 토큰만 (예: 4/8/16/24/32/48). 화면별 임의 padding 금지.  
- **Card:** flat, 과도 radius/shadow 금지. 음식/행동이 있을 때만.  
- **Selected:** Lime subtle fill + Lime stroke/indicator. Blue 금지. 전체 Lime fill 금지.  
- **Disabled:** Neutral light + 대비↓ + 이유. 수동 opacity로 정보 죽이기 금지. 검정 Fill 금지.  
- **Sold-out:** Surface 유지 + 이미지 채도↓ + Badge + 문구. 카드 전체 검정/블러/워시 금지.  
- **BottomCTA:** y=1740 h=180. 03-C Instance만. loading/disabled 정식 Variant.  
- **Admin Table:** dense row, zebra, Enum Badge만. 금액 clip 0.  
- **Sidebar:** Active=현재 페이지. Lime Active Nav. 검정 CTA 남용 금지.  
- **Status Badge:** order/payment/soldOut 구분. 색+텍스트. 미계약 상태 `__manual-check`.  

---

## 5. Kiosk 05-C — 화면별 수정표 (+ 디렉터 의견)

### SCR-001 Home

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default | 다크 풀블리드 Canvas | 음식 히어로 유지하되 Light Neutral로 무게 완화; 카드 White | B의 “신선함”이 다크에 먹힘. 카드 대비만 살리지 말고 Canvas도 밝게 |
| Default | 포장 영문 Eat In | Take Out | HomeActionButton Master도 동시 수정 |
| Order Type Selection | 재질문 Modal + Ghost overlap + Blue selected | Archive Frame, Prototype Home→Menu List, Lime selected, overlap 0 | **배치1 최우선**. 여기 안 고치면 이후 전부 의미 없음 |
| High Contrast | (전수) 다크 풀테마로 떨어지지 않는지 | Contrast≠Dark Theme | Figma Agent 확인 |
| 공통 | `__spec` 노출 | Annotation 전용 영역 | Production 스크린샷에 안 나오게 |

### SCR-003 Menu List

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default | 가격 전부 Lime | 가격 Charcoal, Lime=CTA/Active Tab만 | Accent 남용이 “네온 가격표”처럼 보임 |
| Default | 9장 동일 하드코딩·이미지 불일치 | MenuCard Property로 서로 다른 샘플 | 상용 키오스크 신뢰도 직결 |
| Default | 주문내역 2개 vs Footer 0개/0원 | 동일 소스 바인딩 | 데이터 정합성 P1 |
| Default | Footer 높이/Variant 들쭉 | BottomCTA cartSummary, y=1740 h=180 | |
| Default | spec와 합계 겹침 | spec 이동 | |
| Sold-out | 카드 전체 다크 오버레이 | MenuCard soldOut: White+이미지 dim+Badge, 텍스트 가독 | **정책 위반 확정** |
| Sold-out | (양호) 일부 Badge 방향 | 유지 | 다크 오버레이만 제거하면 됨 |
| Loading/Empty/Error | Lime 남용·Footer 동일 이슈 | Default와 동일 규칙 | State마다 Footer 좌표 재확인 |
| Category Disabled | CategoryTab disabled | 03-C 단일 CategoryTab만 | CategoryTap 오탈자 정리 후 |
| Empty Cart Toast | Toast 위치 | CTA 위 ≥16px | |

### SCR-004 Menu Detail ★ Pilot

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default | 옵션명 mid-word 줄바꿈 | Name FILL max2, 단어 경계 | Pilot 합격 기준의 핵심 |
| Default | 0kcal 이름 겹침 | kcal 전용 슬롯, Absolute overlap 금지 | |
| Default | 0g/단백질/000원 과밀 | 위계: 이름>가격>meta 1줄 | 영양은 축소해도 됨(Pilot 우선) |
| Default | Option 회색 Fill 무거움 | White/Warm Neutral | |
| Default | Quantity stepper 작음 | ≥64 | Master QuantityStepper도 |
| Option Selected | 동일 clip + 단가/CTA 배수 혼란 | 수량 표시와 CTA 금액 관계 명시 | 16,800×2=33,600이면 qty 노출 |
| Menu Sold-out | CTA disabled 양호, clip 동일 | CTA Disabled Variant + clip 수정 | 카드 다크화 금지 |
| Ingredient Sold-out | 옵션만 품절 + 배너/CTA 뒤섞임 | 배너 상단 / CTA 하단 분리 ≥16px | |
| Base Sold-out | 현미밥 disabled + 노란 로직 메모 노출 | 메모 숨김; 다른 Base 선택 가능 유지 | Production에 노란 sticky 금지 |
| Edit Cart Item | “항목명” placeholder | 실제 옵션명 Property | |
| Discard Confirm | **불투명 검정 scrim** + amber 버튼 | Shared Modal 반투명 scrim + Lime primary | **P0. SCR-011과 동일 버그군** |
| Save Error Toast | Toast가 옵션 행 가림 | Toast CTA/콘텐츠와 겹침 0 | |
| Allergy Expanded | (전수) clip/겹침 | Detail과 동일 타이포 규칙 | |

**Pilot 유지:** 1080×1920, Header, 메뉴 정보, Group 순서, State 의미, Lime selected, BottomCTA 담기  
**Pilot 금지:** 07-C, Master 전면 재설계(배치2 범위만), 타 화면 자동 전파  

### SCR-005 Cart

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default | 카드 과복잡 | CartItemCard summary 3줄, 트리 제거 | Default는 상대적으로 밝아서 **시각 레퍼런스 후보** — 복잡도만 줄이면 됨 |
| Default | edit/delete 소형 | ≥64 | |
| Default | Lime footer tint 반복 | Neutral 최소화, 합계 바 단순화 | |
| Default | BottomCTA dual | y=1740 h=180 | Menu List와 Variant만 다르고 높이는 동일해야 함 |
| Item Sold-out | 연두 워시 + 저대비 | White + Badge/문구 + 가독 | |
| Edit Required | showEdit=true 정책 맞음, 시각 Fail | Amber banner + White card | stepper 스타일 정상 카드와 통일 |
| Checkout Blocked | showEdit=false 정책 맞음, 워시 Fail | 이미지 dim + 문구 + delete only | Toast가 주문하기 버튼 가림 수정 |
| Clear/Delete Confirms | (대체로 양호 scrim) | Discard와 동일 패턴인지 확인 | 불투명 검정 있으면 즉시 수정 |
| Quantity/Menu Limit Toast | 직원 문의 카피 | **30 초과만** 직원 문의; 9는 메뉴 한도 문구 | 정책 충돌 정리 |
| Empty / Clear Success | EmptyState 02-C | Instance | |

### SCR-007 Payment

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Method Selected | Progress 1/4처럼 보임 | 결제 단계에 맞는 step | |
| Method Selected | 삼성페이/카카오 확정 노출 | CARD 확정, 나머지 Mock/`__manual-check` | Scope Discipline |
| Processing | CTA 활성 톤 vs UI locked | **양쪽 Disabled** | 중복 결제 P0 |
| Processing | CTA 대비 약함 | Disabled Neutral | |
| Summary Collapsed/Expanded | BottomCTA 좌표 | y=1740 | |
| Loading / All Disabled / Network | State 카피·CTA | 02-C Error/Loading | |

### SCR-008 Complete

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default | 시각 양호 | 유지 | **밝은 완성 레퍼런스**로 다른 화면 톤 맞춤 |
| States 메타 receipt* | Future | Extension 표기, MVP 강조 금지 | |

### SCR-012 Payment Error

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Declined | “처리 중” 카피 + 실패 모달 동시 | Processing 카피 제거 | State 충돌 P0 |
| Declined | 모달 버튼 소형 | ≥64 | |
| Declined | 다시 시도=Red | Lime 또는 Charcoal outline; Red=destructive만 | |
| Network Failure | 동일 색 의미 | 동일 규칙 | |
| Retry Loading | CTA/Spinner | BottomCTA loading Variant | |

### SCR-013 Timeout

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Warning/Continue/Expired | (대체로 양호) | Processing과 Prototype 연결 0 확인 | **Processing 중 Timeout 금지** 재검증 |

### SCR-014 Accessibility

| 상태 | 문제 | 수정 | 내 추가 의견 |
|---|---|---|---|
| Default/HC/Reverted | (대체로 양호) | HC≠전체 Dark Theme; Pretendard 유지 | |

### 05-C 기타

| 항목 | 수정 | 의견 |
|---|---|---|
| Sold-out 5종 Matrix | 로직 정본 유지, 시각만 정책 준수 | 문서와 MenuCard 시각이 어긋난 것이 문제 |
| Deprecated/Future Scope | Production 혼입 금지 | |
| Kiosk Core Flow overview | Prototype이 중복 Order Type을 타면 수정 | |
| Toast specimens | 02-C Toast 정본 사용 | |

---

## 6. Kiosk Components 02-C / 03-C — 수정표 (+ 의견)

### 02-C Shared

| Component | 문제 | 수정 | 의견 |
|---|---|---|---|
| Toast | 5종 동일 다크 필·회색 점 | 밝은 Surface + 톤별 아이콘/좌측 바 (success Lime, error Red, warning Amber, info Charcoal) | “색만으로 구분 금지”의 **반대 실패**(색이 없어서 구분 불가) |
| Modal / ConfirmDialog | Discard 등 불투명 검정 | scrim 반투명 gray Variable | Admin Disable-all과 동일 Master |
| Empty/Error/Loading | 정본 존재 | Production이 이걸 쓰는지 확인 | |
| Deprecated Do Not Use | 삭제 미확정 | Production 연결 0 후 유지 | |

### 03-C Kiosk

| Component | 문제 | 수정 | 의견 |
|---|---|---|---|
| MenuCard soldOut | 회색+텍스트 블러 | White+이미지 dim+Badge, 블러 금지 | List Sold-out의 근원 |
| Deprecated MenuCard | 교체 예정이나 잔존 | Production 0, annotation | Default List가 이 스타일일 가능성 |
| OptionSelectionRow | default 다크, selected Blue | White default, Lime selected, soldOut Badge+텍스트, row≥80, name 2줄, price≥120 | **SCR-004 전역 영향 P0** |
| CartItemCard | 과복잡·워시·소형 버튼·아보카도 중복 | summary 3줄, State 표 §3, touch≥64 | MenuCard 품절 패턴과 통일 |
| BottomCTA | 4 Variant 높이 불일치 위험 | outer h=180 고정, screen y=1740 | Variant는 유지, 높이만 통일 |
| QuantityStepper | 48px | ≥64 | |
| HomeActionButton | Eat In 오타 | Take Out | SCR-001과 동시 |
| CategoryTab / Tap / Category | 삼중·오탈자·깨진 파일 | CategoryTab 단일화, 나머지 Deprecated | |
| PaymentMethodCard | (대체로 양호) | selected Lime, disabled 정식 | 미확정 수단은 화면에서 Mock |
| SoldOutBadge / StepIndicator / MenuDetailSummary | 양호 | 유지 | |
| OrderDetailRow | Property 1=Normal 등 이름 | state=default 등으로 정리 | Legacy `4:12652` 연결 0 |

---

## 7. Admin 06-C — 화면별 수정표 (+ 의견)

### SCR-015 Login

| 문제 | 수정 | 의견 |
|---|---|---|
| Primary 올리브그린 | Lime Variable | Accent 드리프트 시작점 |
| Unauthorized가 Empty 문구 | 401/403 전용 카피 | P2 |

### SCR-022 Dashboard

| 문제 | 수정 | 의견 |
|---|---|---|
| KPI clip, 4카드 vs Partial 5카드 | Partial과 동일 5카드 Auto Layout, clip 0 | **Admin P0** |
| SaaS형 여백·카드 | 밀도 약간↑, 불필요 장식↓ | 리브랜딩 말고 정리 |
| Sidebar 3D+검정 CTA | CTA Light/Lime 정책으로 | 귀여움은 유지, 검정 버튼만 조정 |

### SCR-009 Live Order

| 문제 | 수정 | 의견 |
|---|---|---|
| placeholder menu/item, 0원 | 실데이터 Property | |
| 초대형 Kiosk형 CTA | Admin 버튼 스케일 or “KDS” Annotation | 주방 모니터면 예외 명시 |
| Status Change Confirm amber | Lime primary | |
| TTS Failure Toast | Toast 정본, 주문 Rollback UI 금지 | 정책 일치 |

### SCR-010 Order Management

| 문제 | 수정 | 의견 |
|---|---|---|
| Sidebar Home Active | 주문관리 Active | 전 Admin 공통 버그군 |
| Detail 총액 0원 | 라인 합과 일치 | P0 데이터 |
| Refund / 영수증 Primary | Future면 약화/`__manual-check` | |
| 취소 Badge | Enum 밖이면 제거/manual | |
| Logout과 spec 겹침 | spec 이동 | |

### SCR-011 Sold-out Management

| 문제 | 수정 | 의견 |
|---|---|---|
| Disable-all Confirm 불투명 검정+amber | 반투명 scrim+Lime | SCR-004 Discard와 동일 P0 |
| Nav Home Active | 품절관리 Active | |
| 품절 카드 표현 | Badge 방향 양호 → 유지 | 키오스크보다 나음 |
| Save Error 이중 Toast | Toast 하나 | |
| 저장 문구 오타 | “변경 내용을 저장할까요?” | Bible 명시 이슈 |

### SCR-016 Menu Management

| 문제 | 수정 | 의견 |
|---|---|---|
| 네온 글로우 | export 잔상 제거 | Neon 금지 |
| Save Error 이중 Toast | 단일 | |

### SCR-018 Payment Methods

| 문제 | 수정 | 의견 |
|---|---|---|
| Save Confirm amber | Lime | |
| All Disabled Warning | 카피·배너 위계 | |

### SCR-019/020/021 Sales

| 문제 | 수정 | 의견 |
|---|---|---|
| 미확정 KPI 확정처럼 표시 | Mock/`__manual-check`/제거 | Scope |
| Filter 시 헤더만 갱신·표 고정 | 한 State로 동기화 | Node-State 오류 가능 |
| Loading이 스켈레톤 아닌 별 레이아웃 | Loading Variant 교정 | |

### Admin 공통

- 04-C Instance만  
- Kiosk BottomCTA 금지  
- Active Nav = 현재 페이지  
- Primary = Lime Variable  

---

## 8. Admin Components 04-C — 수정표 (+ 의견)

| Component | 문제 | 수정 | 의견 |
|---|---|---|---|
| OrderCard | 검정 캔버스 + 과대 Lime CTA | Light canvas + Admin 버튼 사이즈 | Live Order 근원 |
| SaveBar | 다크 기본/저장중 | White/Light + Charcoal text | |
| StickyActionBar | SaveBar와 역할 중복 | 통합 또는 동일 Light 언어 | |
| TopHeaderItem | 다크 pill 기본 | Lime bg + Charcoal text (활성) | |
| StatusBadge vs Deprecated Admin-Badge | 거의 동일 | Production→신규만, Deprecated 연결 0 | |
| SoldOutCard | 품절 시각 없음 | 이미지 dim + 품절 Badge | 정본 역할 회복 |
| NavItem | (Lime Active 양호) | 유지, 페이지 Active 매핑 | |
| SalesPeriodFilter / DatePicker / Toggle | 검정·올리브 Active | Lime | |
| DetailPanel | 12,800×3인데 총액 0 | 합계 정합 | SCR-010과 동일 |
| Navbar promo CTA | 검정 버튼 | Charcoal outline 또는 Lime secondary | |
| Checkbox / Deprecated EmptyState | 투명 export | 재export 후 재검 | |
| DataTable* | clip 여부 | Admin Table 규칙 | Dashboard와 함께 |

---

## 9. 시스템 Top 원인 (우선 수정 순서)

1. **Lime Accent 미바인딩(하드코딩 추정)** → 01-C Variable 전수 연결  
2. **다크가 “테마”가 아니라 특정 Component/Confirm에 잔존** → 5곳 집중 제거  
3. **Deprecated/중복 Set** → Production 연결 0  
4. **Auto Layout FILL/HUG 오류** → clip/overlap  
5. **State Frame 불일치** → Sales Loading, Dashboard Default vs Partial  

---

## 10. 배치 실행 순서 (Figma Agent)

```text
BATCH 0  수정 전 감사 표 (문제 코드)
BATCH 1  P0 주문방식 중복 (SCR-001)
BATCH 2  P0 Component Masters (MenuCard, OptionSelectionRow, CartItemCard, BottomCTA, Modal scrim, Toast)
BATCH 3  P0 SCR-004 Menu Detail Pilot → 통과 후 형제 State
BATCH 4  P0 SCR-003 Sold-out + MenuCard 연결 + Footer 정합
BATCH 5  P0 SCR-005 Cart Sold-out 가독
BATCH 6  P0 SCR-007/012 Payment State
BATCH 7  P0/P1 Lime 통일 + Dark Surface 5곳 (Confirm×2, OrderCard, SaveBar, TopHeaderItem)
BATCH 8  P1 BottomCTA y=1740 전수 + Toast 간격
BATCH 9  P1 Admin Clip/Nav/0원/Sales/Enum
BATCH 10 Component 정리 (Category*, Deprecated, SoldOutCard, Badge)
BATCH 11 Annotation 숨김 + Pretendard/Variable 전수 + Screenshot 리포트
```

**지금 바로:** BATCH 1만.  
**BATCH 1 통과 후:** BATCH 2.  
**BATCH 2 없이 BATCH 3 금지** (다크 Option이 다시 붙음).

---

## 11. QA 검수표

### 11-A Menu Detail Pilot

| # | 항목 | PASS/FAIL/확인불가 |
|---|---|---|
| 1 | B 단순 복제 아님 | |
| 2 | AI SaaS Template 아님 | |
| 3 | 음식 중심 | |
| 4 | 정보 위계 | |
| 5 | 2~3초 이해 | |
| 6 | 옵션명·가격 잘림 0 | |
| 7 | Touch ≥64 | |
| 8 | Selected/Disabled 구분 (Lime/Badge) | |
| 9 | BottomCTA y=1740 h=180 | |
| 10 | 밝은 Surface | |
| 11 | 과도 Radius/Shadow 없음 | |
| 12 | State·기능 보존 | |
| 13 | 02~04-C Instance | |
| 14 | Detach 0 | |
| 15 | 타 Production/07-C 미변경 | |

### 11-B 전역

| # | 항목 | PASS/FAIL |
|---|---|---|
| 1 | Lime만 Primary/Selected/Active | |
| 2 | 대형 Dark Surface 0 | |
| 3 | Sold-out=dim+Badge (전체 검정/블러/워시 0) | |
| 4 | Text clip 0 (대상 Frame) | |
| 5 | Toast/Banner가 CTA와 겹침 0 | |
| 6 | CategoryTab 단일화 | |
| 7 | Deprecated Production 연결 0 | |
| 8 | CartItemCard 정보량 축소 | |
| 9 | OptionSelectionRow 기본 밝음 | |
| 10 | SoldOutCard 품절 시각 있음 | |
| 11 | Pretendard only | |
| 12 | Home→Menu List 1클릭, 재질문 0 | |
| 13 | Processing CTA disabled | |
| 14 | Admin Nav Active 정확 | |
| 15 | KPI/금액 clip 0 | |

---

## 12. Figma Agent 복사 블록

### 12-1 BATCH 1 only (지금 실행)

```text
FIGMA AGENT — BATCH 1 ONLY: 주문방식 중복 흐름 수정

이번 요청은 BATCH 1만 실행한다. BATCH 2 이후는 실행하지 마라.
리브랜딩 금지. Detach 금지. Frame 크기 유지(1080×1920).

대상:
- SCR-001 Home Default (후보 node 134:7721)
- 주문방식 버튼 (후보 134:7788)
- Order Type Selection (후보 224:10766)
- 중복 Modal (후보 224:10870)
실제 node는 이름으로 재확인한다. 없는 ID를 추측 생성하지 마라.

작업:
1. Order Type Selection / 중복 Modal로 가는 Prototype 전부 해제.
2. Home의 매장에서 먹기 / 포장하기 → SCR-003 Menu List Default 직접 Navigate.
3. Note: onSelect → orderType=EAT_IN|TAKE_OUT 저장 → /menu.
4. Order Type Selection Frame 이름을 ARCHIVED_duplicate_orderType_selection 으로 바꾸고 Archive. 삭제 금지.
5. Ghost overlap / 같은 좌표 State 쌓임 → Visible false 또는 Archive. Production overlap 0.
6. 포장 카드 영문 Eat In → Take Out. HomeActionButton Master도 동일 수정.
7. Selected Blue stroke/fill 제거 → 01-C Lime Selected.
8. `__spec`이 본문과 겹치면 Annotation 영역으로 이동.
9. Home/Menu List 레이아웃 대규모 변경 금지(연결·카피·Selected·overlap만).

완료 조건:
[ ] 클릭 1회로 Menu List
[ ] 재질문 화면 Prototype 참조 0
[ ] overlap 0
[ ] Take Out 카피 정확
[ ] Selected = Lime
[ ] Screenshot: Home → Menu List

보고: 변경 node, before/after screenshot, residual issues.
```

### 12-2 BATCH 2+3 (배치1 통과 후)

```text
FIGMA AGENT — BATCH 2 Masters + BATCH 3 Menu Detail Pilot

선행: BATCH 1 완료 후에만. 리브랜딩 금지. Detach 금지. Pretendard Variable만. Color는 01-C Variable bind. Component는 02-C~04-C만.

A. BATCH 2 — Masters
1. MenuCard soldOut: White surface, 이미지 채도만 ↓, 텍스트 블러 금지, 품절 Badge, Dark fill 금지. Deprecated MenuCard Production 연결 0.
2. OptionSelectionRow: default Dark charcoal 삭제→White/Warm Neutral. selected Blue→Lime. soldOut=Badge+텍스트. name FILL max 2 lines. price min-width≥120 right. row min-height≥80.
3. CartItemCard: 옵션 트리→summary max 3 lines. 전체 연두/올리브 워시 금지. edit/delete ≥64. qty ≥64. 아보카도 중복 샘플 제거.
   - menu/core soldOut: showEdit=false, showDelete=true, White+이미지 dim+문구
   - option soldOut: showEdit=true, showDelete=true, White+Amber banner
4. BottomCTA: outer height=180. loading/disabled 정식 variant.
5. Shared Modal scrim: 불투명 검정 금지 → 반투명 gray. Primary 버튼 Lime (amber 금지).
6. Toast: 단일 밝은 Surface + 톤별 아이콘/좌측 바. 다크 통일 필 금지.

B. BATCH 3 — SCR-004 Menu Detail / Default만 Pilot
1. Frame 1080×1920. BottomCTA Instance y=1740 h=180.
2. 옵션명 테스트: 오리엔탈, 아보카도, 훈제연어, 양배추 라이스, 파마산칩 → mid-word 1글자 줄바꿈 0, max 2 lines.
3. 0kcal↔이름 overlap 0. price clip 0.
4. Option fill White/Warm Neutral. selected Lime only. soldOut Badge+disabled, 카드 다크/블러 금지.
5. 노란 로직 메모 Production 숨김.
6. 통과 시에만 Option Selected / Menu·Ingredient·Base Sold-out / Edit Cart Item에 동일 규칙 복제.
7. Discard Confirm: 반투명 scrim + Lime primary (불투명 검정/amber 금지).

금지: 07-C 변경, Master 전면 재설계 확장, 타 SCR 자동 전파, Future Scope 추가.
보고: checklist, screenshots, residual.
```

### 12-3 Lime + Dark 5곳 (배치2와 병행 가능)

```text
FIGMA AGENT — Lime Accent 통일 + Dark Surface 제거

1) Primary/Selected/Active Fill이 Lime Variable인지 확인하고 Hardcoded면 교체:
- SCR-015 Login
- SCR-009 Status Change Confirm
- SCR-011 Disable-all / Save
- SCR-018 Save Confirm
- SCR-012 Retry (Red→Lime 또는 Charcoal outline; Red는 destructive만)
- Admin SalesPeriodFilter 활성
- Admin Navbar promo CTA
- Admin TopHeaderItem 활성
- Admin DatePicker / Toggle-on / OrderTotalPrice
- Home Selected, OptionSelectionRow selected (Blue→Lime)
- Menu List 가격 전면 Lime → 가격 Charcoal (Lime은 CTA/Tab만)

2) Dark 제거:
- SCR-004 Discard Confirm scrim
- SCR-011 Disable-all Confirm scrim
- Admin OrderCard canvas
- Admin SaveBar (StickyActionBar와 언어 통일)
- Admin TopHeaderItem default dark

3) Before/After Screenshot + Variable bind 여부 보고.
금지: 로직/State 수 변경, Detach, 07-C 구조 변경.
```

### 12-4 Text Clip / Overlap / BottomCTA

```text
FIGMA AGENT — Text Clip + Overlap + BottomCTA 전수

1. SCR-004 옵션명 Auto Layout Fill, 자연 줄바꿈, max 2 lines, ellipsis는 3줄 이상일 때만.
2. Ingredient/Base Sold-out: 안내 배너와 CTA 분리, 간격 ≥16.
3. SCR-022 Default KPI: Partial Data와 동일 5카드, clip 0.
4. 좌하단 Route/Data/States 주석: Production 밖 Annotation으로 이동 (SCR-003 합계, SCR-010/011 Logout과 겹침 해소).
5. SCR-004/005 Toast: BottomCTA 위 ≥16, 버튼 가림 0.
6. 05-C BottomCTA 있는 모든 Production: y=1740 h=180, 수동 Footer→Kiosk/BottomCTA Instance.
보고: Frame | before y/h | after y/h | clip remaining | overlap remaining.
```

### 12-5 Component 정리 + Admin P1

```text
FIGMA AGENT — Component 정리 + Admin P1

1. CategoryTap→CategoryTab 단일화. Category/깨진 Tab은 Deprecated. Production 연결 0.
2. StatusBadge로 Production 전수 교체. Deprecated Admin-Badge 연결 0.
3. SoldOutCard에 이미지 dim + 품절 Badge 추가.
4. SCR-010 Detail 총액 0원 수정. Nav Active=현재 페이지(전 Admin).
5. SCR-019/020/021: 미확정 KPI Mock 표기. Filter 시 표/차트 동기 State. Loading=skeleton Variant.
6. Enum 밖 취소/환불/결제완료는 production Variant에서 제거 또는 __manual-check.
7. QuantityStepper min touch ≥64.
금지: Instance Detach, Future Scope 기능 추가, Kiosk BottomCTA를 Admin에 사용.
```

---

## 13. 작업지시서 1 — P0 주문방식 중복 (요약본)

- **대상:** Home `134:7721`, 버튼 `134:7788`, Selection `224:10766`, Modal `224:10870` (이름 재확인)  
- **현재:** Home → (재질문) → Menu List  
- **해제:** Selection/Modal로 가는 연결 전부  
- **새 연결:** 버튼 → SCR-003 Default  
- **유지:** orderType EAT_IN/TAKE_OUT  
- **영향:** SCR-001, SCR-003, Prototype  
- **완료:** 1클릭 도달, Archive, overlap 0, Screenshot  
- **금지:** 레이아웃 대규모 변경, 확인 없는 삭제  

---

## 14. 작업지시서 2 — Menu Detail Visual Pilot (요약본)

### 유지
콘텐츠(메뉴·옵션그룹·알레르기·CTA), 정보구조(필수→선택→CTA), ASAK Light+Lime selected, State 의미  

### 변경
Layout Auto Layout, Typography 2줄, Surface White, Option Name/Price/kcal, Selected Lime, Disabled Badge, Spacing 토큰, BottomCTA y=1740 h=180, clip 0  

### 변경 금지
Production 전체, Master 전면, 타 화면 전파, Prototype 전체, 07-C  

### 정량
1080×1920; padding 60; content≤960; CTA y=1740 h=180; touch≥64; name max 2; price min-width≥120  

### 완료 체크
긴 옵션명 5종 테스트; overlap 0; Lime selected; CTA 좌표; Detach 0; Screenshot  

---

## 15. 증거 파일 인덱스 (figma 폴더)

### 05-C 핵심 PNG
- `SCR-001/Home/Default.png`, `Order Type Selection.png`, `High Contrast.png`
- `SCR-003/Menu List/Default.png`, `Sold-out.png`, …
- `SCR-004/Menu Detail/Default.png`, `Option Selected.png`, `Menu Sold-out.png`, `Ingredient Sold-out.png`, `Base Sold-out.png`, `Edit Cart Item/*`, `Discard Confirm.png`
- `SCR-005/Cart/Default.png`, `Item Sold-out.png`, `Edit Required.png`, `Checkout Blocked.png`, …
- `SCR-007/Payment/*`, `SCR-008/Order Complete/Default.png`, `SCR-012/*`, `SCR-013/*`, `SCR-014/*`
- `SCR-003/004/Sold-out 5종 Matrix.png`

### 02-C / 03-C
- `Kiosk/MenuCard.png`, `CartItemCard.png`, `OptionSelectionRow.png`, `BottomCTA.png`, `Showcase_*.png`, `Deprecated.png`, `Shared/Toast.png`, …

### 06-C / 04-C
- `SCR-022/.../Default.png`, `Partial Data.png`
- `SCR-009~021` 각 State
- `Admin/OrderCard.png`, `SaveBar.png`, `TopHeaderItem.png`, `SoldOutCard.png`, `StatusBadge.png`, `Deprecated/*`

---

## 16. 디렉터 최종 코멘트 (페이지 넘기며 본 의견)

1. **배치1을 미루면 안 된다.** Order Type Selection은 정책·코드·PNG가 모두 “지우라”고 말한다.  
2. **품절을 검게 칠한 곳이 전부가 아니다.** 검게/무거워 보이는 체감은 Confirm scrim·Home Canvas·Option dark default·Cart 워시·SaveBar가 합쳐진 결과다. **5곳 타격**이 효율적이다.  
3. **SCR-005 Default와 SCR-008은 살릴 레퍼런스**다. 전체를 다시 그리지 말고 이 톤으로 맞춘다.  
4. **SCR-004는 Pilot로 끊어야** 한다. 옵션 그리드 clip이 Master(OptionSelectionRow/카드) 문제라 Master 먼저.  
5. **Admin은 Lime 통일 + KPI clip + Nav Active + 0원**만 고쳐도 “AI Dashboard 티”가 크게 줄어든다.  
6. **01-C가 export에 없다.** Agent 첫 질문에 “이 Fill이 Variable인가 Hardcoded인가”를 의무화한다.  
7. **직원 문의 토스트**는 Bible/요청=30만, 코드=9에도 직원 문구 → Figma 카피는 30만 따르고, 코드는 별도 티켓.  
8. **완료의 정의는 State 개수가 아니다.** Screenshot에서 2~3초 안에 행동이 보이고, clip/overlap/dark sold-out/Blue selected/Detach가 0일 때 완료다.

---

## 17. Claude 교차검토 — 누락 보완 + 구조적 의견 (2026-07-17 추가)

> Cursor 실측(Instance 카운트) + 이 문서 통합본을 다시 대조한 결과. 시각 문제 자체보다 **실행 순서와 우선순위 구조**에 초점.

### 17-1. 1차 통합에서 빠진 항목 (화면/컴포넌트별)

**Kiosk**

| 위치 | 누락 항목 |
|---|---|
| 02-C `AllergenNotice` | `hasAllergen`/`optionChanged` 두 State가 배경·문구까지 완전히 동일 — 구분 불가 |
| 02-C `AllergenTag` | warning 칩이 색상만으로 구분, 아이콘 없음 |
| 02-C `ConfirmDialog` | danger 톤 3종(red/orange/red)이 버튼 색상만으로 구분, 아이콘 없음 |
| 03-C `QuantityStepper` | `limitReached` 도달 시 컨트롤 자체는 그대로고 일회성 Toast로만 알림 — 지속 시각 신호 없음 |
| 03-C `OrderDetailList` | export 내용이 실제로는 Menu Detail 옵션 화면(베이스/드레싱/토핑) — 컴포넌트명과 콘텐츠 불일치, 오export 의심 |
| SCR-009 Status Change Confirm | 모달 본문 "#1225" vs 배경 하이라이트 카드 "#1325" — 주문번호 불일치 |
| SCR-009 Save Error / TTS Failure Toast | 토스트 폭이 좁아 "실패했습니 다"처럼 음절 중간 줄바꿈 |
| SCR-018 Load Error | 재시도 버튼만 Lime, 다른 화면(009/019/020/021) 재시도 버튼은 dark — 화면마다 재시도 버튼 기준색이 다름 |
| SCR-018 Save Error | Toast 안에 실제 문구 대신 placeholder `"알림 메시지"` 그대로 노출 |

**Admin**

| 위치 | 누락 항목 |
|---|---|
| 04-C `IngredientTypeFilterChip` | 칩 10개가 서로 다른 채도 높은 색(초록/민트/핑크/빨강/보라/청록/노랑/파랑), 라벨은 placeholder "전체" 그대로 — Lime 단일 accent에서 가장 크게 벗어난 컴포넌트 |
| 04-C `PaymentMethodSettingRow` | "점검 중" 경고가 노란 테두리 — 다른 곳의 빨강 경고와 다른 세 번째 경고색 |
| 04-C `DataTableRow` | white/off-white/light-green 3가지 밝은 배경이 범례 없이 반복 — default/hover/selected 구분 불가 |
| 04-C `Component Index` vs `Cover` | Deprecated 개수가 문서마다 5개/7개로 다르게 적힘 |

### 17-2. 구조적 의견 (가장 중요)

1. **"Swap"과 "Visual Fix"가 실행 순서상 분리돼 있다.** Part B §9(Instance Swap)와 이 문서 §12(BATCH 1~11)가 서로 다른 트랙으로 남아있으면, BATCH 2에서 Master를 고쳐도 05-C Production은 여전히 Legacy(`4:12652` 등)를 참조해 화면에 반영되지 않는다. **BATCH 2를 2-A(Master 시각 수정) → 2-B(Header/SearchInput 등 Master 승격) → 2-C(Kiosk→Admin 교차 사용 28건 Swap) → 2-D(전체 Legacy→Final Swap)로 쪼개고, BATCH 3(Pilot)보다 반드시 앞에 둔다.**
2. **OptionSelectionRow(`160:1831`)는 05-C 사용 0건이라 지금은 안전해 보이지만, Swap 실행 순간 598개 인스턴스가 한꺼번에 이 컴포넌트로 바뀐다.** 지금 이 컴포넌트의 default가 다크인 채로 Swap을 실행하면 Menu Detail 전체가 한 번에 다크로 뒤집힌다. **OptionSelectionRow 시각 수정은 Swap 실행 전 선행 조건이다.**
3. **"Legacy 문제"와 "Final Master 자체 결함"은 다른 문제다.** `MenuCard`(150:678)·`CartItemCard`(150:404)·`SaveBar`(150:5115)는 이미 Final을 쓰는데도 시각 문제가 있었다 — 이건 Swap으로 안 고쳐지고, Master 자체 수정 또는 Instance별 Override 제거가 필요하다. Figma Agent에게 "Fill이 Variable 바인딩인지"뿐 아니라 **"Instance Override가 남아있는지"도 같이 보고**하게 해야 한다.
4. **Instance 볼륨 기준으로 보면 우선순위가 달라진다.** `OrderMenuOptionItem` Legacy(Admin, 576건), `OrderDetailRow` Legacy(Kiosk, 598건), `MenuButton` Legacy(Admin, 384건) 순으로 전체 Legacy 잔존을 가장 크게 줄인다. 지금 배치 순서(Kiosk 우선)는 체감 기준으로는 맞지만, "전체 Legacy 잔존율 감소" 효율 기준으로는 Admin의 두 항목이 더 크다 — 두 기준 중 무엇을 우선할지 팀에서 한 번은 정해야 한다.
5. **Kiosk↔Admin 교차 오염이 숫자로 확인된다.** `Kiosk/PaymentMethodCard`(4:11051)가 Admin 06-C에서 **28건** 쓰인다. 규모가 작아 독립된 "Quick Win" 배치(BATCH 2-C)로 먼저 처리할 수 있다 — `Admin/PaymentMethodSettingRow`(150:5142)로 교체.
6. **Touch Target 기준이 3곳에서 다르다.** Bible 80px, candidate-B 44px, 이 문서 "≥64, 가능하면 80". **01-C Variable에 `size-touch-min` 토큰 하나로 확정**해서 QuantityStepper/BottomCTA/체크박스가 전부 그 값을 참조하게 해야 한다.
7. **Header/SearchInput/DataTableHeader/Pagination은 "Swap 대상"이 아니라 "먼저 만들어야 할 대상"이다.** 03-C/04-C 구분선 위에 정식 Master가 아직 없다(Instance만 존재). §7 매핑표에 다른 Swap 항목과 나란히 두면 Figma Agent가 "매핑 대상 없음"으로 건너뛰기 쉽다 — Promote-to-Master 작업을 별도 단계로 분리한다.

### 17-3. 수정된 배치 순서

```text
BATCH 0    수정 전 감사표 (기존)
BATCH 1    P0 주문방식 중복 (기존, 최우선)
BATCH 2-A  Master 시각 결함 수정: OptionSelectionRow default(다크→밝게, Swap 전 필수),
           MenuCard/CartItemCard/SaveBar의 Override vs Master 원인 구분 후 수정,
           Modal scrim, Toast 톤 구분, AllergenNotice 상태 구분 보강
BATCH 2-B  Header/SearchInput/DataTableHeader/Pagination → 03-C/04-C Master로 승격
BATCH 2-C  Kiosk/PaymentMethodCard→Admin 28건 Swap (Quick Win, 독립 실행)
BATCH 2-D  05-C 전체 Legacy→Final Swap (§7 표, OrderDetailRow 598건 포함,
           Menu Detail 옵션 행은 OptionSelectionRow로, Cart/Payment 요약 행은 Final OrderDetailRow로 분기)
BATCH 3    SCR-004 Pilot (Swap 완료 후 진행 — 순서 변경 핵심)
BATCH 4~6  기존 유지
BATCH 7    Lime 통일 + Dark Surface 5곳 (기존)
BATCH 8    BottomCTA 좌표 + Toast 간격 (기존) + SCR-009 Toast 줄바꿈 추가
BATCH 9    Admin Clip/Nav/0원/Sales/Enum + IngredientTypeFilterChip 색상 정리
           + SCR-009 주문번호 불일치, SCR-018 placeholder 문구 수정
BATCH 10   Component 정리 (기존) + Admin 06-C Legacy Swap 576/384건 (볼륨 기준 우선 검토)
BATCH 11   Annotation 숨김 + Pretendard/Variable + Override 전수 확인 + Screenshot 리포트
```

### 17-4. QA 체크리스트 추가

| # | 항목 |
|---|---|
| 16 | Legacy→Final Swap 후 mainComponent id가 `4:*`/`31:*`/`36:*`/`39:*`/`45:*`/`52:*` 0건인가 |
| 17 | Final Master 자체 Fill이 Variable 바인딩인가, Instance Override가 남아있는가 |
| 18 | AllergenNotice의 hasAllergen/optionChanged가 시각적으로 구분되는가 |
| 19 | Admin IngredientTypeFilterChip 색상이 Lime 중심으로 정리됐는가 |
| 20 | Header/SearchInput/DataTableHeader/Pagination이 정식 Master로 등록됐는가 |
| 21 | Kiosk/PaymentMethodCard가 Admin 화면에서 0건인가 |
| 22 | Toast/ConfirmDialog placeholder 문구("알림 메시지", "항목명")가 실제 콘텐츠로 대체됐는가 |

---

## 18. 코드 재검증 — 실제 정책·흐름 문제 (2026-07-17 추가)

> **범위 확인 방법:** `ASAK-Kiosk/src` 전체 파일을 열어 실제 로직이 있는지 직접 읽음(주석만 있는 자리표시자 여부는 grep이 아니라 파일 내용을 직접 확인). Figma 시각 문제와 별개로, **실제로 동작하는 흐름과 정책이 어디까지 구현됐는지**를 재확인했다.

### 18-1. 실제 구현 상태 (파일 단위 확인)

| 영역 | 상태 | 근거 |
|---|---|---|
| SCR-001 Home / OrderTypeSelector | **구현됨** | `HomePage.jsx`, `OrderTypeSelector.jsx` — orderType 저장 후 `/menu` 직행 |
| SCR-003 Menu List | **구현됨** | `MenuListPage.jsx`(79줄), `MenuCard.jsx`, `CategoryTabs.jsx`, `OrderList.jsx`(136줄, 장바구니 미니 목록) |
| SCR-004 Menu Detail | **구현됨(가장 완성도 높음)** | `MenuDetailPage.jsx`(189줄) — 수량 제한, 옵션 선택, 필수값 검증, 가격 계산, addItem까지 실동작 |
| SCR-005 Cart | **미구현** | `CartPage.jsx` = 주석 1줄뿐 |
| SCR-007 Payment | **미구현** | `PaymentPage.jsx`, `PaymentMethodList.jsx` = 주석 1줄뿐 |
| SCR-008 Complete | **미구현** | `OrderCompletePage.jsx` = 주석만 |
| SCR-014 Accessibility | **미구현** | `AccessibilityPage.jsx` = 주석만 |
| 공통 컴포넌트 | **미구현** | `Button`, `Modal`, `ConfirmDialog`, `EmptyState`, `ErrorMessage`, `LoadingSpinner`, `Footer`, 공용 `Header` 전부 주석만 |
| `cartRules.js` / `soldOutPolicy.js` / `useKioskTimeout.js` | **미구현** | 파일 내용이 정책 설명 주석 1줄뿐, 실제 함수 없음 |
| Admin 전체(로그인/주문/품절/메뉴/결제수단/매출) | **100% 미구현** | 페이지·컴포넌트 전부 주석 1줄 |

**결론: 실제로 동작하는 흐름은 Home → Menu List → Menu Detail(장바구니 담기)까지다. Cart 이후(결제, 완료)와 Admin 전체는 코드가 전혀 없다.** Figma는 07-C QA Matrix까지 State를 정교화하고 있는데, 그 상태들을 검증할 실제 화면이 코드에는 없는 화면이 더 많다 — **Figma 상태 설계 속도와 프론트 구현 속도의 간극**을 팀이 인지하고 있어야 한다.

### 18-2. 확인된 구체적 로직 버그 (모두 파일을 직접 읽어 확인)

**[P0] 라우터에 `/cart`, `/payment`, `/complete`가 아예 없다**

- 근거: `src/apps/kiosk/KioskApp.jsx`의 `<Routes>`에 `/`, `/menu`, `/menu/:menuId` 3개뿐.
- 영향: 페이지 컴포넌트를 나중에 채워도 라우트 자체가 없으면 이동할 수 없다. **체크아웃 흐름이 UI 문제가 아니라 라우팅 자체가 끊겨 있다.**
- 권장: Route 3개(`/cart`, `/payment`, `/complete`)를 먼저 등록하고, 빈 페이지라도 라우트부터 연결한다.

**[P0] Menu List에서 Cart로 이동하는 버튼이 없다**

- 근거: `OrderList.jsx`(136줄, 장바구니 미니 목록)를 전부 읽었으나 "장바구니로 이동/주문하기" 같은 이동 액션이 없다. `MenuListPage.jsx`에도 없다.
- 영향: 위 라우터 문제와 합쳐지면 사용자가 메뉴에 담아도 결제로 갈 방법이 현재 코드상 전혀 없다.
- 권장: `OrderList.jsx` 하단에 Bible/03-C `BottomCTA`(`150:385`, cartSummary layout)에 대응하는 이동 버튼을 추가한다.

**[P0] Menu Detail — 품절 메뉴여도 "장바구니에 담기" 버튼이 비활성화되지 않는다**

- 근거: `MenuDetailPage.jsx`에서 `MenuDetailFooter`의 `disabled` prop은 `!isRequiredSatisfied`만 검사한다. `menuDetail.isSoldOut`/`menuDetail.hasSoldOutIngredient`를 확인하는 코드가 없다.
- 위반: Bible Sold-out 정책 "메뉴/핵심재료 품절 → 전체 주문 불가, CTA disabled"에 정면 위반.
- 권장: `disabled={!isRequiredSatisfied || menuDetail.isSoldOut || menuDetail.hasSoldOutIngredient}`로 수정.

**[P1] 동일 메뉴 + 동일 옵션 재선택 시 수량이 합쳐지지 않고 새 줄이 생긴다**

- 근거: `orderSessionStore.js`의 `addItem`은 항상 `items` 배열에 push만 한다. `MenuDetailPage.jsx`의 `handleConfirm`도 기존 항목과 비교 없이 매번 `addItem`을 호출한다.
- 위반: Cart Edge Case 문서 "동일 메뉴, 동일 옵션: quantity 증가 — MVP 권장"과 다르게 동작한다.
- 권장: `addItem` 호출 전 동일 `menuId`+동일 옵션 조합의 기존 `cartItemId`가 있는지 확인해 있으면 `updateItemQuantity`로, 없으면 `addItem`으로 분기.

**[P1] `excludedIngredientIds`가 항상 빈 배열로 하드코딩**

- 근거: `MenuDetailPage.jsx`의 `addItem` 호출부에 `excludedIngredientIds: []`가 고정값. 재료 제외를 선택하는 UI/state 자체가 이 페이지에 없다.
- 영향: Bible/Figma가 강조하는 "제외 가능 재료" 기능이 실제로는 선택할 방법이 없다.

**[P1] 알레르기 정보가 Menu Detail에 전혀 렌더링되지 않는다**

- 근거: `MenuDetailPage.jsx` 전체에 `allergens`/`allergyText` 참조가 없다. `AllergenNotice`/`AllergenTag` 컴포넌트도 import되지 않음.

**[P1] 장바구니 항목 삭제가 ConfirmDialog 없이 즉시 실행된다**

- 근거: `OrderList.jsx`의 `handleRemove`는 `removeItem(cartItemId)`를 바로 호출한다. 확인 모달이 없다.
- 위반: Bible "삭제는 별도 Action" + Figma의 Delete Confirm State와 불일치. (Cart 화면이 아니라 Menu List의 미니 목록이라도 삭제는 확인 단계가 있어야 한다.)

**[P2] `updateItemQuantity`가 store 레벨에서 자체 검증을 하지 않는다**

- 근거: `orderSessionStore.js`의 `updateItemQuantity`는 값을 그대로 set한다. 9/30/최소1 검증은 오직 호출부(`OrderList.jsx`)에만 있다.
- 위험: 지금은 호출부가 하나뿐이라 문제가 없지만, 나중에 Cart 페이지가 구현되며 다른 경로로 이 액션을 호출하면 검증을 우회할 수 있다. Store 액션 자체에도 최소한의 가드를 넣는 걸 권장(방어 계층 이중화).

**[P1] `quantityLimits.js`의 안내 문구가 Bible 정책과 반대로 붙어 있다**

- 근거: `quantityLimits.js:16` `MENU_LIMIT: "메뉴당 최대 9개까지 주문할 수 있습니다. **대량 주문은 직원에게 문의해 주세요.**"` — 반면 `CART_LIMIT`(30개, 17번째 줄)는 직원 문의 문구가 없다.
- 위반: Bible/요청 정책은 "직원 문의 문구는 전체 30개 초과 시도에만 표시"다. 지금 코드는 정반대로, 메뉴당 9개(더 작은 한도)에 직원 문의가 붙어있고 전체 30개(더 큰 한도)에는 안 붙어있다.
- 권장: 두 문구의 직원 문의 문장을 서로 바꾼다. `MENU_LIMIT`은 "메뉴당 최대 9개까지 주문할 수 있습니다."로 간결하게, `CART_LIMIT`에 "대량 주문은 직원에게 문의해 주세요."를 붙인다.

**[정정] 이전 분석에서 우려했던 `currency.js`는 실제로 정상 구현되어 있음**

- `currency.js`도 파일 맨 위에 "학습용 자리표시자" 주석이 남아있지만, 실제로는 `formatCurrency` 함수가 완성돼 있고 `MenuCard.jsx`/`MenuDetailSummary.jsx`/`MenuDetailFooter.jsx`/`OptionItem.jsx`에서 정상적으로 쓰이고 있다. **"학습용 자리표시자" 주석 = 미구현이 아닐 수 있으니, 배치 작업 시 주석만 보고 판단하지 말고 파일 내용을 직접 확인해야 한다.**

### 18-3. 이미지 렌더링 관련 코드 확인

- `MenuCard.jsx`, `MenuDetailSummary.jsx`, `OrderListItem.jsx` 모두 `<img src={imageUrl}>`만 있고, `commonStyle.css`/`global.css`/`tokens.css`/`reset.css` 어디에도 이미지 크기·`object-fit` 규칙이 없다. §19에서 다루는 이미지 자산 문제와 별개로, **자산이 정규화되더라도 CSS 규칙이 없으면 다시 불균일하게 보인다** — 자산 전처리와 CSS 규칙 추가는 함께 진행돼야 한다.

---

## 19. 메뉴 이미지 자산 문제와 처리 가이드 (2026-07-17 추가)

> 사용자 확인: 실제 서비스에는 `ASAK/asak-data/images/menu`(84개 PNG, menuId 파일명)의 사진을 쓸 예정. PNG 크기는 통일했지만 투명 여백이 사진마다 달라 작아 보이는 문제 발생.

### 19-1. 실측 확인

- 84개 중 78개는 캔버스 474×457로 통일돼 있으나, 6개는 1254×1254~1536×1024 등 제각각이다.
- 실제 음식 사진이 캔버스를 채우는 비율(Fill Ratio)은 **34.6%~99.5%**로 편차가 매우 크다(평균 74.95%). `4185.png`(34.6%), `4056.png`(37.7%), `4450.png`(39.9%), `4317.png`(40.7%)가 가장 심함.
- `original/`(한글 파일명, 후가공 전으로 추정) 폴더도 동일 이미지 기준 Fill Ratio가 거의 같다 — **후가공 단계에서 여백이 생긴 게 아니라 원본 사진 촬영/편집 단계부터 여백 비율이 다르다.**

### 19-2. 왜 Figma·CSS만으로 못 고치는가

- Figma의 이미지 Fill 모드(Fill/Fit/Crop)와 CSS `object-fit`은 **"이미지 파일 전체"**를 기준으로 비율을 계산한다. 여백까지 포함된 이미지는 확대해도 여백이 같이 확대될 뿐, 음식 사진만 골라 확대해주지 않는다.
- 즉 이 문제는 **레이아웃 설정이 아니라 이미지 데이터 자체의 문제**이므로, Figma Agent 지시서나 CSS 클래스 추가만으로는 해결되지 않는다.

### 19-3. 해결 방향 — 자산 전처리(권장)

1. alpha 채널 기준으로 각 이미지의 실제 콘텐츠 영역(bounding box)을 계산해 crop
2. 정사각 표준 캔버스(예: 800×800)에 종횡비를 유지한 채 배치하고, 모든 이미지에 동일한 비율의 여백(예: 6~8%)만 남긴다
3. `menuId` 파일명은 그대로 유지해 코드/DB 매핑을 바꾸지 않는다
4. 처리 후 84개 전수 재측정으로 Fill Ratio가 목표 범위(예: 78~86%) 안에 들어오는지 확인

세부 스크립트 스펙과 Instance Swap 대상 컴포넌트·실행표 템플릿은 Part B §11에 정리했다(중복 방지를 위해 이 문서에는 요약만 둔다).

### 19-4. Figma/코드 반영 순서

```text
1. 이미지 전처리 스크립트 실행 (자산 소유자/개발 쪽 작업, Figma Agent 범위 아님)
2. 정규화된 84개 자산을 Figma에 업로드
3. Kiosk/MenuCard(150:678), Kiosk/MenuDetailSummary(160:1734),
   Admin/MenuCard(150:5194)의 이미지 슬롯을 menuId 기준으로 Instance Swap
4. React 쪽 <img> 컨테이너에 object-fit 규칙을 commonStyle.css/tokens.css에 추가
   (현재 이미지 크기 관련 CSS 규칙이 전혀 없음 — §18-3 참고)
5. Instance Swap 84건 전수를 §11-5 실행표로 보고
```

- 재료(ingredient) 이미지는 `asak-data/images`에 별도 폴더가 없다 — `Admin/IngredientCard`(150:5252) 등 재료 이미지 슬롯은 소스 확보 여부부터 Figma Agent가 확인해야 한다.

---

## 20. 유저플로우·UX 관점 재검토 (2026-07-17 추가)

> 화면 단위 시각 문제와 별개로, "흐름이 자연스러운가"를 다시 짚는다.

### 20-1. 전체 흐름 재확인

```text
Home(orderType) → Menu List → Menu Detail(반복 담기) → Cart* → Payment → Processing → Complete
                                                              ↳ Sold-out(수정/삭제)
                                     ↳ Payment Error(재시도/장바구니 복귀)   ↳ Timeout(경고/계속/초기화)

Admin: Login → Dashboard → Live Order Board / Order Management / Sold-out / Menu / Payment Methods / Sales
```
`*` Cart는 §18에서 확인했듯 코드 라우트 자체가 없다. **Figma 흐름도 상 Cart는 있지만, 실제로는 지금 이 흐름의 절반(Menu Detail→Cart)이 코드에서 끊겨 있다는 걸 디자인 완료 판단 시 감안해야 한다.**

Bible "One Screen, One Decision"은 화면별로 잘 지켜지고 있다(Home=어디서 먹을지, Menu List=뭘 고를지, Cart=이 주문으로 결제할지). 이 구조 자체는 유지 대상.

### 20-2. 새로 짚는 UX 갭

| # | 항목 | 확인 근거 | 심각도 |
|---|---|---|---|
| 1 | **뒤로가기 시 선택 상태 유지 안 됨** | `MenuDetailPage.jsx`의 옵션/수량 선택은 `useState` 로컬 상태다. Menu List로 나갔다가 같은 메뉴에 재진입하면 이전 선택이 초기화된다. Bible "뒤로 가도 선택 상태를 유지한다"(UX_PHILOSOPHY) 위반 가능성. Figma Prototype에도 "이전 화면 복귀 시 데이터 유지 여부"를 표시하는 State가 없다. | P1 |
| 2 | **세션 새로고침/크래시 시 전량 유실** | `orderSessionStore.js`는 zustand 메모리 상태만 쓰고 `localStorage`/`persist` 미들웨어가 없다(코드 전수 검색 결과 0건). 키오스크는 실제 매장에서 화면이 얼어붙거나 브라우저가 재시작될 수 있는데, 그 순간 장바구니 전체가 사라진다. **Figma에도 "세션 복구" 관련 State가 없다.** | P0 (실기기 배포 전 필수 결정) |
| 3 | **카피 확정본이 한 곳에 없음** | "Eat In/Take Out" 오타, `"알림 메시지"`/`"항목명"` placeholder, `"저장 변경할까요?"` 오타 등이 화면마다 산발적으로 발견됐다 — 카피 파이널 패스가 안 끝났다는 신호. 화면별로 따로 고치기보다 **전체 카피를 하나의 시트로 뽑아 한 번에 검수**하는 게 재작업을 줄인다. | P1 |
| 4 | **화면 전환 방식 미정** | Prototype에 전환(즉시/페이드 등) 스펙이 없다(Animation은 이번 범위 밖이라고 이미 합의됨). 다만 "즉시 전환이 기본"이라는 최소 원칙 한 줄은 정해둬야 React 쪽에서 임의로 트랜지션을 넣거나 안 넣는 혼선이 없다. | P2 |
| 5 | **SCR-009 Live Order가 Admin Nav/Header 없이 독립형** | 04-C 감사에서 SCR-009만 Sidebar/Header가 없는 KDS(주방 모니터)형 레이아웃으로 확인됨. 의도된 것이면 `__spec`에 "이 화면은 별도 주방 디스플레이용"이라고 명시해야 다른 Admin 화면과 다른 이유가 핸드오프 때 헷갈리지 않는다. | P2 |
| 6 | **재방문 고객용 빠른 경로는 의도적으로 후순위** | Bible 핵심 사용자에 "빠른 주문을 원하는 재방문 고객"이 있지만 추천 우선 모드는 2026-07-06 회의에서 Phase 2로 이미 결정됨 — 문제 아님, 지금 범위에서 빠진 이유가 명확하니 그대로 진행. | 확인만 |

---

## 21. 키오스크 시스템 Edge Case 카탈로그 (2026-07-17 추가)

> 실제 매장 배포를 가정했을 때 나올 수 있는 시나리오를 분류했다. **"Figma/코드 확인"란이 비어 있으면 지금 어디에도 대응이 없다는 뜻이다.**

### A. 하드웨어·환경

| # | 시나리오 | Figma 상태 | 코드 상태 | 권장 |
|---|---|---|---|---|
| 1 | 메뉴 로딩 중 네트워크 순간 끊김 | SCR-003/004 Error 상태 있음 (양호) | `useMenu.js`, `useAsync.js`는 빈 스텁 — 재시도 로직 없음 | React 전환 시 재시도(retry) 로직 우선 구현 |
| 2 | 결제 중 네트워크 끊김 | SCR-007 Load Network Error 있음 (양호) | `PaymentPage.jsx` 자체가 미구현 | — |
| 3 | 결제 버튼 연타(중복 결제) | SCR-007 Processing에서 CTA가 Disabled 안 되는 문제 이미 §3에서 지적함 | `payment.js`는 API 호출 3줄짜리 thin wrapper — debounce/lock 없음 | **React 전환 시 최우선.** 버튼 disable + 서버 측 idempotency key 둘 다 필요 |
| 4 | 무응답 장시간 방치 | SCR-013 Timeout 있음 (양호) | `useKioskTimeout.js` 완전 빈 스텁 | React 전환 시 최우선 구현 대상 |
| 5 | **브라우저 새로고침/크래시로 세션 소실** | 없음 (신규 발견) | `orderSessionStore.js`에 persist 없음, 확인 완료 | 최소한 `sessionStorage` 스냅샷 저장 + "이전 주문을 이어가시겠어요?" 복구 화면 검토 |
| 6 | 키오스크 재부팅 후 첫 화면 | 확인 안 됨 | 확인 안 됨 | Figma Agent 확인 필요 |
| 7 | 영수증 프린터 용지 부족/고장 | Future Scope로 이미 범위 제외 확정 | — | 재확인만, 문제 아님 |
| 8 | 결제 응답 지연 vs 명시적 실패 구분 | SCR-012가 Network Failure/Payment Declined로 이미 분리돼 있음 (양호) | 미구현 | — |

### B. 동시성·데이터 정합성

| # | 시나리오 | Figma 상태 | 권장 |
|---|---|---|---|
| 9 | 결제 진행 중 관리자가 해당 메뉴/재료를 품절 처리 | Sold-out 정책 문서에 "장바구니 담은 후 품절: 자동삭제 금지, 해결 전 결제 차단"은 있으나, **"결제 Processing 중" 시점의 서버 검증 시점**은 API 계약에 명시 안 됨 | 백엔드 설계 시 결제 승인 직전 서버가 재검증하는 시점을 명문화 |
| 10 | 관리자 2명이 동시에 같은 품절 항목 토글 | 명시 없음 (신규 발견) | Dirty Change 저장 시 낙관적 잠금(버전 체크) 또는 마지막 저장 우선 정책 결정 필요 |
| 11 | 결제 완료 화면 자동 초기화(5초) 전에 다음 손님이 화면을 조작 | SCR-008에 5초 자동 초기화는 있으나 "조기 종료/중간 개입" 케이스는 없음 | 화면 터치 시 카운트다운 리셋할지, 그대로 둘지 정책 결정 |
| 12 | 결제는 PG 승인됐는데 우리 서버 응답 유실(오프라인 성공/온라인 실패) | Bible "결제 성공·실패·재시도·중복 결제 방지"에 개념은 있으나 이 구체 시나리오는 명시 안 됨 | 결제 API에 idempotency key 필수 — Figma보다 백엔드 설계 우선 항목으로 별도 티켓 권장 |

### C. 사용자 행동

| # | 시나리오 | 현재 상태 | 비고 |
|---|---|---|---|
| 13 | 옵션 선택 중 뒤로가기 후 재진입 | §20-2 #1과 동일 (선택 상태 소실) | 이미 위에서 다룸 |
| 14 | 결제 화면에서 마음이 바뀌어 처음부터 다시 시작 | Timeout 모달엔 "처음으로"가 있으나 Payment/Cart 화면 자체에 명확한 "처음으로" 동선이 안 보임 | Figma Agent 확인 필요 |
| 15 | 고령/저시력 고객 | SCR-014 Accessibility(고대비/큰글씨) 있음 | 양호 |
| 16 | 다국어 고객 | Bible/Figma 어디에도 언급 없음 | 지금 범위에 없다면 Future Scope에 명시적으로 등록(현재는 "언급 자체가 없음"이라 애매함) |
| 17 | 아이가 화면을 마구 누름(오탐) | 디자인 범위 밖 | 참고용, 하드웨어/브라우저 레벨 이슈 |

### D. 관리자

| # | 시나리오 | 현재 상태 | 권장 |
|---|---|---|---|
| 18 | 관리자 세션 만료 중 작업 | Figma에 명시적 화면 확인 안 됨 | Figma Agent 확인 필요(SCR-015 Login에 Unauthorized는 있으나, "작업 중 만료"는 다른 시나리오) |
| 19 | 대량 품절 배치 처리 중 일부만 실패 | `SOLD_OUT_MANAGEMENT.md`에 batch API는 있으나 부분 실패 UI 명시 없음 | Figma에 "N건 중 M건 실패" 형태의 부분 실패 상태 추가 검토 |

---

## 22. Figma → React Handoff 준비도 체크리스트 (2026-07-17 추가)

> "얼른 Figma를 끝내고 React로 넘어가고 싶다"는 목표에 맞춰, 무엇이 진짜 핸드오프 전에 끝나야 하고 무엇이 React와 병행 가능한지 구분했다.

### 22-1. 넘어가기 전 반드시 끝나야 하는 것 (Blocking)

| # | 항목 | 이유 |
|---|---|---|
| 1 | BATCH 1(주문방식 중복 제거) + BATCH 2-A~2-D(Master 수정+Swap) | 여기가 안 끝난 채 React로 넘어가면 개발자가 어떤 컴포넌트를 기준으로 만들지 스스로 판단해야 해서 재작업이 커진다 |
| 2 | 화면별 데이터 Property 이름 확정(camelCase, `menuId`/`orderStatus`/`paymentStatus` 등) | React는 이 이름 그대로 props/DTO로 옮긴다 — 나중에 바뀌면 코드도 같이 바뀐다 |
| 3 | `cartRules.js`/`soldOutPolicy.js`/`useKioskTimeout.js`가 요구하는 정확한 상태 이름과 전이 조건 | 이 3개는 코드가 완전히 비어 있어(§18-1) React 개발자가 Figma의 State 이름을 그대로 함수/상수로 옮겨야 한다. 지금 Figma의 State 이름이 확정 안 되면 코드도 확정 못 한다 |
| 4 | 카피(에러 메시지, placeholder 문구) 전체 확정 | §20-2 #3 — 지금처럼 화면마다 나중에 하나씩 발견되면 React 쪽 문자열도 그때마다 바뀐다 |

### 22-2. React와 병행해도 되는 것 (Non-blocking)

| # | 항목 | 이유 |
|---|---|---|
| 1 | 메뉴 이미지 84개 전처리·Instance Swap | 이미지 URL은 API가 내려주는 값이라 React 코드 구조에는 영향 없음. 전처리 스크립트를 별도로 돌리는 동안 React 개발은 placeholder 이미지로 계속 진행 가능 |
| 2 | Admin 04-C의 세부 색상 정리(IngredientTypeFilterChip 등) | 관리자 화면은 지금 코드가 100% 미구현이라 당장 급하지 않다 — Kiosk 핵심 화면부터 넘기고 Admin은 뒤에 병행 |
| 3 | P2급 시각 디테일(네온 글로우 잔재, SCR-008 여백 등) | 기능에 영향 없음 |

### 22-3. 실용적 제안 — 지금 코드 진행 상황에 맞춘 범위 조정

§18-1에서 확인했듯 실제 코드는 **Home~Menu Detail까지만 구현**돼 있고 Cart/Payment/Complete/Admin은 전부 백지 상태다. 이 상황을 고려하면:

- Figma를 "07-C QA Matrix의 모든 State"까지 끝내고 넘기려 하면 시간이 오래 걸린다.
- 대신 **"지금 바로 코드를 이어 쓸 화면" 우선순위로 좁혀서 먼저 확정**하는 걸 제안한다: SCR-005 Cart(default/empty/soldOut 3종) → SCR-007 Payment(default/processing/failed 3종) → SCR-008 Complete(default 1종). 이 7개 State만 §22-1의 Blocking 항목 기준으로 먼저 통과시키면 React 쪽 Cart→Payment→Complete 구현을 바로 시작할 수 있다.
- Admin과 Kiosk의 나머지 State(Loading/Error/Empty 세부, 접근성 등)는 React가 Cart~Complete를 만드는 동안 병행해서 마무리해도 된다.

---

## 23. 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-07-17 | Cursor 실측 PNG 분석 + 클로드 대화 분석 + 배치 지시서 + 페이지별 디렉터 의견 통합 최초본 |
| 2026-07-17 (추가) | Claude 교차검토(누락 12건·구조적 의견 6건·배치 순서 수정) + 코드 재검증(라우터 누락, Cart 이동 버튼 없음, 품절 CTA 미차단, 동일옵션 병합 누락, 재료제외/알레르기 미구현, 삭제 컨펌 없음, 문구 정책 반전 등) + 메뉴 이미지 84개 실측·전처리 가이드 추가 |
| 2026-07-17 (추가2) | 유저플로우·UX 재검토(뒤로가기 상태 유실, 세션 새로고침 시 전량 소실 등) + 키오스크 Edge Case 카탈로그(하드웨어/동시성/사용자행동/관리자 4개 분류 19건) + Figma→React Handoff 준비도 체크리스트(Blocking vs Non-blocking 구분, 범위 축소 제안) 추가 |

---

*이 문서는 Figma/코드를 수정하지 않는다. Figma Agent 실행과 QA 검수의 단일 체크리스트로 사용한다.*

---

# Part B: 컴포넌트 정본 · Instance Swap 매핑


> **작성일:** 2026-07-17  
> **근거:** Figma MCP 실측 (`use_figma` instance → mainComponent 집계)  
> **파일:** [ASAK — Design System & Product UI 0715](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715)  
> **fileKey:** `JSrjOy668zhfkiLplCkreh`  
> **원칙:** 쓰인 컴포넌트는 전부 이 문서에 기록한다. 화면에서 쓰는 정본은 **구분선 위 C 페이지**만 허용한다.

---

## 0. 페이지 구분선 규칙 (절대)

| 위치 | 페이지 | 역할 |
|---|---|---|
| **구분선 위 = 정본** | `00-C` ~ `08-C` | Variable·Component·Screen·QA. **새 생성·수정·Production 연결은 여기만** |
| **구분선** | [`---`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=233-30019) (`233:30019`) | 경계 |
| **구분선 아래 = Legacy/참고** | `01.`~`06.`(C 없음), `99. Archive`, `05-B`/`06-B`, Pilot 페이지 | 읽기·Archive만. **05-C/06-C Production이 여기 Instance를 쓰면 Fail** |

### 정본 페이지 링크

| Page | node-id | URL |
|---|---|---|
| 00. START HERE | `0:1` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=0-1) |
| 00-C Cover | `174:8727` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=174-8727) |
| **01-C Foundations** | `148:12745` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=148-12745) |
| **02-C Shared** | `145:2` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=145-2) |
| **03-C Kiosk** | `150:2` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2) |
| **04-C Admin** | `150:2860` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2860) |
| 05-C Kiosk Screens | `134:7720` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=134-7720) |
| 06-C Admin Screens | `134:10606` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=134-10606) |
| 07-C QA Matrix | `190:2` | [링크](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=190-2) |

---

## 1. 핵심 결론 (실측)

**05-C / 06-C Production은 Implementation Final Component를 거의 안 쓰고, 구분선 아래 Legacy(`4:*`, `31:*`, `36:*`, `39:*`, `45:*`, `52:*` …)를 대량 참조한다.**

| 화면 | Instance 총수 | 대표 문제 |
|---|---|---|
| 05-C | **938** | OrderDetailRow Legacy 598건 / BottomCTA Legacy 45 vs Final 6 / Option* Final **0건** |
| 06-C | **1571** | OrderMenuOptionItem Legacy 576 / MenuButton Legacy 384 / SoldOutCard·StatusBadge·Navbar도 Legacy 우세 |

따라서 “없는 컴포넌트를 새로 만든다”가 아니라 **이미 있는 02-C~04-C Final을 화면에 Swap**하는 것이 정답이다.

---

## 2. 05-C에서 실제로 쓰인 컴포넌트 (공식 기록)

> 집계 기준: Instance → `getMainComponentAsync` → Component Set/Component name+id  
> **쓰인 것은 전부 아래 표에 남긴다.** Legacy는 “현재 사용 중”으로 기록하되 **교체 대상**.

### 2-A. 사용량 Top (05-C)

| # | 현재 연결 name | 현재 node | 건수 | 정본(Final) | Final node | 조치 |
|---|---|---|---:|---|---|---|
| 1 | Kiosk/OrderDetailRow | `4:12652` | **598** | Kiosk/OrderDetailRow | [`150:247`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-247) | **Swap → Final** |
| 2 | Kiosk/Header | `4:12808` | 52 | 03-C에 Header Component Set 없음(페이지에 Instance만) | — | Final Header **Master를 03-C 구분선 위 Section에 승격** 후 Swap |
| 3 | Kiosk/BottomCTA | `4:12790` | **45** | Kiosk/BottomCTA | [`150:385`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-385) | **Swap → Final** (현재 Final 사용 6건뿐) |
| 4 | Kiosk/CategoryTap | `45:821` | 32 | Kiosk/CategoryTab | [`150:695`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-695) | Tap 폐기, **Tab으로 통일 Swap** |
| 5 | Kiosk/StepIndicator | `4:12764` | 29 | Kiosk/StepIndicator | [`150:359`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-359) | **Swap → Final** |
| 6 | Kiosk/MenuCard | `150:678` | 27 | 동일 Final | [`150:678`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-678) | 유지 (soldOut 시각만 수정) |
| 7 | Kiosk/CartItemCard | `150:404` | 23 | 동일 Final | [`150:404`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-404) | 유지 (State 시각 수정) |
| 8 | menu-card | `52:5` | 18 | Kiosk/MenuCard | `150:678` | **Swap → MenuCard** |
| 9 | Kiosk/SoldOutBadge | `311:1789` | 16 | 동일 Final | [`311:1789`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=311-1789) | 유지·품절 카드에 적극 사용 |
| 10 | Kiosk/QuantityStepper | `150:166` | 16 | 동일 Final | [`150:166`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-166) | 유지 (touch≥64 권장) |
| 11 | Shared/Icon/Placeholder | `171:4843` | 13 | 02-C Final | [`171:4843`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=171-4843) | 유지 |
| 12 | Kiosk/Category | `31:11021` | 8 | Kiosk/Category `150:700` 또는 CategoryTab | [`150:700`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-700) | Legacy Category → Final |
| 13 | Shared/Toast | `158:24049` | 8 | 동일 Final | [`158:24049`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24049) | 유지 (톤별 아이콘 보강) |
| 14 | Kiosk/PaymentMethodCard | `4:11051` | 7 | Kiosk/PaymentMethodCard | [`150:3`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-3) | **Swap** (Final 사용 1건뿐) |
| 15 | Kiosk/BottomCTA | `150:385` | 6 | Final | `150:385` | 유지·비중 확대 |
| 16 | Admin/MenuButton | `4:12035` | 6 | Admin/MenuButton | [`150:2861`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2861) | **Kiosk에 Admin 버튼 금지** → 제거 또는 Kiosk IconButton으로 |
| 17 | Kiosk/HomeActionButton | `31:11077` | 4 | Kiosk/HomeActionButton | [`150:718`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-718) | Legacy→Final (이미 Final 4건도 있음) |
| 18 | Kiosk/HomeActionButton | `150:718` | 4 | Final | `150:718` | 유지 |
| 19 | Kiosk/OrderSummaryInfo | `4:12564` | 4 | Kiosk/OrderSummaryInfo | [`150:182`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-182) | **Swap → Final** |
| 20 | Shared/Modal | `4:12238` | 4 | Shared/Modal | [`158:23908`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-23908) | **Swap → Final** |
| 21 | Shared/EmptyState | `4:10961` | 4 | Shared/EmptyState | [`158:24093`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24093) | **Swap → Final** |
| 22 | Shared/ConfirmDialog | `158:23975` | 4 | Final | [`158:23975`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-23975) | 유지 |
| 23 | Shared/CartFooterBar | `150:655` | 3 | Final | [`150:655`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-655) | 유지 |
| 24 | Shared/CartFooterBar | `4:13063` | 2 | → `150:655` | 동일 | Swap |
| 25 | Shared/LoadingState | `4:11035` | 2 | Shared/LoadingState | [`158:24192`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24192) | Swap |
| 26 | Kiosk/PaymentMethodCard | `150:3` | 1 | Final | `150:3` | 유지·확대 |
| 27 | Shared/ErrorState | `158:24161` | 1 | Final | [`158:24161`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24161) | 유지·확대 |
| 28 | Kiosk/AllergyAccordion | `160:1852` | 1 | Final | [`160:1852`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=160-1852) | 유지·Detail에 확대 |

---

## 3. 03-C에 있는데 05-C에서 **거의/전혀 안 쓰인** Final (활용 필수)

| Final Component | node | Variant/Property 요약 | 어디에 써야 함 | 현재 |
|---|---|---|---|---|
| **Kiosk/OptionSelectionRow** | [`160:1831`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=160-1831) | selectionType=single\|multiple\|exclude × state=default\|selected\|disabled\|soldOut\|pressed | SCR-004 옵션 행 전부 | **05-C 사용 0** → OrderDetailRow Legacy가 대체 중 |
| **Kiosk/OptionGroup** | [`160:1764`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=160-1764) | state=default\|disabled + title/required/selectionRule | SCR-004 그룹 헤더 | **0** |
| **Kiosk/MenuDetailSummary** | [`160:1734`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=160-1734) | default / optionSelected / quantityChanged / loading + Text props | SCR-004 상단 요약 | **0** |
| **Kiosk/CategoryTab** | [`150:695`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-695) | active\|inactive\|disabled | SCR-003 카테고리 | **0** (CategoryTap Legacy 32건) |
| **Kiosk/OrderDetailRow Final** | [`150:247`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-247) | state 7종 + name/price/kcal props | Detail/요약 행 | **0** (Legacy 598) |
| **Kiosk/BottomCTA Final** | [`150:385`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-385) | layout=twoCTA\|singlePrimary\|cartSummary × state=default\|disabled\|loading | 003/004/005/007/012 Footer | Final 6 vs Legacy 45 |
| **Kiosk/PaymentMethodCard Final** | [`150:3`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-3) | method×selected×size | SCR-007 | Final 1 vs Legacy 7 |
| **Kiosk/OrderSummaryInfo Final** | [`150:182`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-182) | 접힘\|펼침 | SCR-007 Summary | Final 0 / Legacy 4 |
| **Kiosk/StepIndicator Final** | [`150:359`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-359) | step=1\|2\|3\|start\|step5 | Cart/Payment/Complete | Final 0 / Legacy 29 |
| Shared/Modal Final | [`158:23908`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-23908) | paymentError\|timeout\|information | Error/Timeout | Final 0 / Legacy Modal 4 |
| Shared/EmptyState Final | [`158:24093`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24093) | cart\|orders\|… | Empty 화면 | 일부만 Final |
| Shared/LoadingState Final | [`158:24192`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24192) | card\|table\|page\|button | Loading | Legacy 혼용 |
| AllergenTag / AllergenNotice | [`158:24215`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24215) / [`158:24225`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=158-24225) | default/warning, hasAllergen… | SCR-004 알레르기 | **05-C 사용 0** (AllergyAccordion만 1) |
| Kiosk/CategoryTap Final | [`150:737`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-737) | Size×active | — | **Deprecated 후보** (CategoryTab으로 대체). Production 연결 0 유지 |

---

## 4. 06-C에서 실제로 쓰인 컴포넌트 (공식 기록)

### 4-A. 사용량 Top (06-C)

| # | 현재 연결 | node | 건수 | Final 정본 | Final node | 조치 |
|---|---|---|---:|---|---|---|
| 1 | Admin/OrderMenuOptionItem | `4:12048` | **576** | Admin/OrderMenuOptionItem | [`150:2878`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2878) | Swap (property `sourse`→`source` 정리) |
| 2 | Admin/MenuButton | `4:12035` | **384** | Admin/MenuButton | [`150:2861`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2861) | Swap |
| 3 | Admin/MenuCard | `36:3752` | 84 | Admin/MenuCard | [`150:5194`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5194) | Swap |
| 4 | Admin/SoldOutCard | `4:15232` | 83 | Admin/SoldOutCard | [`150:5089`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5089) | Swap (Final 8건만) + 품절 시각 보강 |
| 5 | Admin/Navbar | `4:13733` | 63 | Admin/Navbar | [`150:4739`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-4739) | Swap (Final 5건) |
| 6 | Admin/StatusBadge | `4:14013` | 51 | Admin/StatusBadge | [`150:5064`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5064) | Swap (Final 9건). Deprecated Badge 금지 |
| 7 | Admin/OrderCard | `4:13567` | 32 | Admin/OrderCard | [`150:2956`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2956) | Swap + Dark canvas 수정 |
| 8 | Admin/DataTableRow-Active | `4:13791` | 30 | Admin/DataTableRow-Active | [`150:4932`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-4932) | Swap · status Enum 정리 |
| 9 | Kiosk/PaymentMethodCard | `4:11051` | 28 | Admin/PaymentMethodSettingRow 또는 Final PaymentMethodCard | [`150:5142`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5142) / `150:3` | **Admin에 Kiosk 카드 혼용 금지** → SettingRow로 |
| 10 | Admin/Toggle on/off | `39:15877` / `39:15879` | 23+5 | 04-C Toggle Final로 승격·단일 Set | (04-C에 on/off 분리되어 있으면 Set으로 통합) | Legacy→Final |
| 11 | Admin/FilterDropdown | `4:13883` | 18 | Admin/FilterDropdown | [`150:5007`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5007) | Swap |
| 12 | Admin/Checkbox | `39:15876` | 16 | Admin/Checkbox | [`150:5409`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5409) | Swap |
| 13 | Admin/SalesMetricCard | `150:2928` | 13 | Final | [`150:2928`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2928) | 유지 (Legacy `4:13539` 4건 Swap) |
| 14 | Shared/Toast | `158:24049` | 10 | Final | `158:24049` | 유지 · Deprecated Admin-Toast 금지 |
| 15 | Shared/LoadingState | `158:24192` | 9 | Final | `158:24192` | 유지 |
| 16 | Admin/SaveBar | `150:5115` | 7 | Final | [`150:5115`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5115) | 유지 · Dark 시각 수정 |
| 17 | detail-panel | `51:13018` | 6 | Admin/DetailPanel | [`150:5418`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5418) | Swap (Final 1건뿐) |
| 18 | Admin/SearchInput | `4:13881` | 6 | 04-C에 SearchInput Master 확인·없으면 Final로 승격 | — | Legacy 사용 중 → 04-C 위 Section에 정본화 |
| 19 | Admin/DataTableHeader | `4:13864` | 6 | 동일 | — | 04-C 위 승격 후 Swap |
| 20 | Admin/Pagination | `4:13929` | 3 | 04-C 승격 | — | |
| 21 | Shared/EmptyState / ConfirmDialog / ErrorState | Final 다수 | — | `158:*` | 이미 Final 사용분 유지, Legacy Empty/Error Swap |
| 22 | Deprecated Admin-Badge 등 | — | — | StatusBadge `150:5064` | Production 연결 0 |

### 4-B. 04-C Final인데 화면에서 덜 쓰인 것 (활용)

| Final | node | 권장 사용처 |
|---|---|---|
| Admin/DataTableRow | [`150:2906`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-2906) | SCR-010 목록 (Active와 역할 정리) |
| Admin/NavItem | [`150:5187`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=150-5187) | Navbar 내부 Active=현재 페이지 |
| Admin/IngredientCard / OptionItemCard / IngredientTableRow | `150:5252` / `150:5274` / `150:5290` | SCR-011 재료·옵션 탭 |
| Admin/IngredientTypeFilterChip | `150:5336` | SCR-011 필터 |
| Admin/SelectionSummaryBar | `150:5377` | SCR-011 선택 요약 |
| Admin/ModalActionBar | `150:5478` | Confirm/Modal 하단 (amber 하드코딩 대신) |
| Admin/DatePicker | `150`→[`388:692`](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=388-692) | Sales 기간 |
| Admin/PaymentMethodSettingRow | `150:5142` | SCR-018 (Kiosk PaymentMethodCard 대체) |
| Admin/DetailPanel | `150:5418` | SCR-010 Detail (0원 버그 수정) |
| Shared/* Final | `158:*` | Admin Empty/Error/Loading/Toast/Confirm — Deprecated Admin-* 대신 |

### 4-C. Broken Component (공식 기록)

| name | node | 문제 |
|---|---|---|
| `day` | `389:44743` | Component Set errors (`type=seleted` 오탈자 등). DatePicker 하위로 재구성하거나 Deprecated |

---

## 5. 02-C Shared Final 목록 (공식)

| Component | node | Variants | 화면 연결 규칙 |
|---|---|---|---|
| Shared/Modal | `158:23908` | paymentError / timeout / information | Legacy Modal `4:12238` 교체. scrim 반투명 |
| Shared/ConfirmDialog | `158:23975` | deleteCartItem / clearCart / discardChanges / saveChanges / disableAll… × tone × loading | Discard/Disable-all 전부 이것 |
| Shared/Toast | `158:24049` | success/error/warning/info/loading × size | Deprecated Admin-Toast 금지 |
| Shared/EmptyState | `158:24093` | general/cart/orders/… | Legacy Empty 교체 |
| Shared/ErrorState | `158:24161` | load/save/payment/notFound × layout | Legacy Error 교체 |
| Shared/LoadingState | `158:24192` | card/table/page/button | Legacy Loading 교체 |
| AllergenTag | `158:24215` | default/warning | SCR-004 |
| AllergenNotice | `158:24225` | default/hasAllergen/optionChanged | SCR-004 |
| Icons | CaretLeft/Right/Placeholder | — | 아이콘만 |

Deprecated(02-C): Modal-Confirm, Modal-Duplicate, ConfirmDialog-Legacy, Admin-Empty/Error — **Production 0**

---

## 6. 03-C Kiosk Final 목록 (공식) + Property

| Component | node | Variant axes | 주요 Property | 흐름 |
|---|---|---|---|---|
| PaymentMethodCard | `150:3` | method, selected, size | click | SCR-007 |
| QuantityStepper | `150:166` | state | quantity, minusEnabled, plusEnabled | Detail/Cart · min1 / menu9 / cart30 |
| OrderSummaryInfo | `150:182` | 접힘/펼침 | menu_amount, menu_price | SCR-007 |
| OrderDetailRow | `150:247` | state×7 | name, addPrice, kcal… | Detail — **OptionSelectionRow와 역할 정리 후 사용** |
| StepIndicator | `150:359` | step | — | 005/007/008 |
| BottomCTA | `150:385` | layout×state | primaryLabel, secondaryLabel, cartCount, cartTotal | y=1740 h=180 |
| CartItemCard | `150:404` | Default/Disabled/SoldOut | showEdit/Delete, optionSummaryText, set… | SCR-005 |
| CartFooterBar | `150:655` | ready/empty/loading | — | List/Cart 하단 보조 |
| MenuCard | `150:678` | default/soldOut | — | SCR-003 |
| CategoryTab | `150:695` | active/inactive/disabled | — | SCR-003 **정본** |
| Category | `150:700` | page K/A | 카테고리 bool들 | Tab으로 수렴 권장 |
| HomeActionButton | `150:718` | eatIn/takeOut | label | SCR-001 |
| CategoryTap | `150:737` | Size×active | — | **Deprecated 예정** |
| MenuDetailSummary | `160:1734` | 5 states | menuName, price, price… | SCR-004 |
| OptionGroup | `160:1764` | default/disabled | title, required, children | SCR-004 |
| OptionSelectionRow | `160:1831` | selectionType×state | label, additionalPrice, soldOutLabel | SCR-004 **필수 활용** |
| AllergyAccordion | `160:1852` | collapsed/expanded | count, notice | SCR-004 |
| SoldOutBadge | `311:1789` | tone×size | label | MenuCard/Cart 품절 |

Header: 페이지 top-level이 Instance(`150:403`)뿐 → **Component Set을 03-C Section Navigation 위(구분선 위)에 Master로 고정** 후 05-C가 그걸 참조.

---

## 7. Legacy → Final 교체 매핑표 (Agent 실행용)

### Kiosk (05-C)

```text
4:12652  OrderDetailRow     → 150:247  (또는 옵션 UI면 160:1831 OptionSelectionRow)
4:12790  BottomCTA          → 150:385
4:12764  StepIndicator      → 150:359
4:11051  PaymentMethodCard  → 150:3
4:12564  OrderSummaryInfo   → 150:182
4:12808  Header             → (03-C Header Master 승격 후 그 ID)
4:12238  Modal              → 158:23908
4:10961  EmptyState         → 158:24093
4:11035  LoadingState       → 158:24192
4:13063  CartFooterBar      → 150:655
45:821   CategoryTap        → 150:695 CategoryTab
31:11021 Category           → 150:695 또는 150:700
31:11077 HomeActionButton   → 150:718
52:5     menu-card          → 150:678 MenuCard
```

### Admin (06-C)

```text
4:12048  OrderMenuOptionItem → 150:2878
4:12035  MenuButton          → 150:2861
36:3752  MenuCard            → 150:5194
4:15232  SoldOutCard         → 150:5089
4:13733  Navbar              → 150:4739
4:14013  StatusBadge         → 150:5064
4:13567  OrderCard           → 150:2956
4:13791  DataTableRow-Active → 150:4932
4:13883  FilterDropdown      → 150:5007
39:15876 Checkbox            → 150:5409
51:13018 detail-panel        → 150:5418
4:11051  Kiosk PaymentCard on Admin → 150:5142 PaymentMethodSettingRow
4:13539  SalesMetricCard     → 150:2928
Legacy Empty/Error/Toast/Confirm → 158:* Shared Final
```

---

## 8. 화면별 “써야 하는 Final” 체크리스트

### SCR-001 Home
- [ ] HomeActionButton `150:718` only  
- [ ] Header Final  
- [ ] Order Type Selection Archive (흐름)  

### SCR-003 Menu List
- [ ] CategoryTab `150:695` (Tap/Legacy 제거)  
- [ ] MenuCard `150:678` (+ SoldOutBadge)  
- [ ] BottomCTA `150:385` layout=cartSummary  
- [ ] CartFooterBar `150:655`  
- [ ] Toast/Empty/Loading/Error = Shared Final  

### SCR-004 Menu Detail ★
- [ ] MenuDetailSummary `160:1734`  
- [ ] OptionGroup `160:1764`  
- [ ] OptionSelectionRow `160:1831` (**카드 수동 Frame 대체**)  
- [ ] AllergyAccordion + AllergenNotice/Tag  
- [ ] QuantityStepper `150:166`  
- [ ] BottomCTA singlePrimary `150:385`  
- [ ] ConfirmDialog Final (Discard)  
- [ ] Legacy OrderDetailRow `4:12652` **598건 제거 목표**  

### SCR-005 Cart
- [ ] CartItemCard `150:404`  
- [ ] QuantityStepper  
- [ ] BottomCTA twoCTA  
- [ ] ConfirmDialog clear/delete  
- [ ] Toast Final  

### SCR-007 / 012 / 013
- [ ] PaymentMethodCard `150:3`  
- [ ] OrderSummaryInfo `150:182`  
- [ ] StepIndicator `150:359`  
- [ ] BottomCTA  
- [ ] Modal/Confirm/Toast Shared Final  

### Admin 공통
- [ ] Navbar `150:4739` + NavItem `150:5187`  
- [ ] StatusBadge `150:5064` only  
- [ ] Shared Toast/Empty/Error/Loading/Confirm  
- [ ] Kiosk Component 0건 (PaymentMethodCard 등)  

---

## 9. Figma Agent — 컴포넌트 활용 일괄 지시

```text
FIGMA AGENT — Legacy Instance → Final Component Swap (구분선 위만)

파일: JSrjOy668zhfkiLplCkreh
규칙:
1. Production(05-C/06-C) Instance의 mainComponent가 구분선 아래(4:*, 31:*, 36:*, 39:*, 45:*, 52:* 등)이면
   §7 매핑표의 Final(02-C~04-C)로 Swap한다.
2. Instance Detach 금지. 새 Component Set 생성 금지(없는 Master만 03-C/04-C 구분선 위 Section에 승격).
3. 이미 Final인 MenuCard/CartItemCard/Toast/Confirm 등은 유지하고 시각만 정책 준수.
4. SCR-004: 수동 Option 카드/Legacy OrderDetailRow를 OptionGroup+OptionSelectionRow로 교체.
5. SCR-003: CategoryTap→CategoryTab.
6. Admin: Kiosk/PaymentMethodCard 제거→PaymentMethodSettingRow.
7. Deprecated/* Production 연결 0.
8. 완료 후 05-C/06-C에서 mainComponent id가 4:* 인 Instance 수를 다시 집계해 보고.
   목표: Kiosk 핵심(BottomCTA/OrderDetailRow/StepIndicator/PaymentMethodCard/CategoryTab/Modal) Legacy = 0.

보고 형식:
| Screen | Legacy name | Legacy id | count before | Final id | count after |
```

---

## 10. 관련 문서

- 시각·배치 전체: Part A (위)  
- 이 문서가 **컴포넌트 공식 정본(사용 실측 + Final 매핑)**  
- Product Bible Component Map은 이 표와 충돌 시 **이 문서(실측)를 우선**하고 Bible은 후속 동기화  

---

## 11. 메뉴 이미지 Instance Swap 계획 (신규)

> **근거:** `C:\ASAK-workspace\ASAK\asak-data\images\menu`(84개), `...\images\original`(84개, 한글명 포함) 실측. PowerShell `System.Drawing`으로 alpha bounding box 직접 측정.

### 11-1. 실측 결과

| 항목 | 값 |
|---|---|
| 총 이미지 수 | 84 |
| 표준 캔버스(474×457) | 78개 |
| 예외 캔버스(1254×1254, 1278×1231, 1287×1222, 1295×1214, 1298×1212, 1536×1024) | 6개 |
| Fill Ratio(실제 음식 사진이 캔버스에서 차지하는 비율) | 최저 34.6% ~ 최고 99.5%, 평균 74.95% |
| 최저 사례 | `4185.png` 34.6%, `4056.png` 37.7%, `4450.png` 39.9%, `4317.png` 40.7% |
| `menu/` vs `original/` 비교 | 동일 파일 기준 fillRatio 거의 동일(예: `10069` 양쪽 다 94.7~96%) → **후가공이 원인이 아니라 원본 사진 자체가 사진마다 여백이 다름** |

### 11-2. 원인 진단 — Figma Scale 모드·CSS `object-fit`만으로 해결 불가한 이유

- 투명 여백은 이미지 **레이어 자체의 픽셀 데이터**다. Figma의 Fill/Crop 모드나 CSS `object-fit: cover/contain`은 "이미지 전체(투명 여백 포함)"를 기준으로 비율을 맞추므로, 여백이 이미 넓게 포함된 이미지는 아무리 Crop/Cover를 걸어도 **음식 사진 자체가 작게 유지**된다.
- 즉 34.6%짜리 이미지와 96%짜리 이미지를 같은 정사각 슬롯에 `object-fit: cover`로 넣으면, 34.6% 쪽은 확대돼도 여백까지 같이 확대되어 여전히 음식이 작아 보인다.
- **결론: Figma·React 어느 쪽에서도 스타일링만으로는 해결이 안 되고, 이미지 자산 자체를 전처리(트림 후 재배치)해야 한다.**

### 11-3. 전처리 파이프라인 (제안)

```text
1. 소스: asak-data/images/menu/{menuId}.png (또는 original/{menuId}_{name}.png)
2. alpha channel bounding box 계산 (투명하지 않은 최소 사각형)
3. bounding box로 crop
4. 목표 캔버스(정사각, 예: 800×800)에 종횡비 유지한 채 contain 배치
   - 여백은 전 이미지 동일 비율로 고정 (예: 상하좌우 각 6~8%)
5. 출력: asak-data/images/menu-normalized/{menuId}.png (파일명은 menuId 유지 — 코드/DB 매핑 그대로 사용 가능)
6. 검증: 출력본 84개 전수의 fillRatio가 목표 범위(예: 78~86%) 안에 들어오는지 재측정
```

- 구현 위치는 Node.js(`sharp`) 스크립트를 권장한다 — Kiosk/Admin이 이미 JS 스택이라 별도 런타임 설치 없이 `asak-data/scripts`에 배치 가능.
- **이 전처리는 Figma 작업보다 먼저 끝나야 한다.** Figma에 이미지를 올리고 나서 나중에 자산을 바꾸면 Instance Swap을 다시 해야 하므로, 순서는 "전처리 → 84개 정규화 자산 확보 → Figma 업로드 → Instance Swap"이다.

### 11-4. Instance Swap 대상 (컴포넌트별)

| Figma Component | node | 현재 이미지 슬롯 | Swap 후 |
|---|---|---|---|
| Kiosk/MenuCard | `150:678` | placeholder/빈 이미지 | menuId별 정규화 이미지로 Instance Swap Property 바인딩 |
| Kiosk/MenuDetailSummary | `160:1734` | placeholder | 동일 |
| Admin/MenuCard | `150:5194` | placeholder | 동일 |
| Admin/IngredientCard | `150:5252` | placeholder | 재료 이미지 세트 별도 확보 필요(현재 `asak-data/images`에는 `menu`/`original`만 있고 재료 이미지 폴더 없음 — **Figma Agent 확인 필요**) |
| Shared/Icon/Placeholder | `171:4843` | 범용 placeholder | 실제 이미지 연결 후에는 데이터 없음(`imageMissing`) 상태 전용으로만 남겨둔다 |

### 11-5. Swap 실행표 (템플릿 — Figma Agent가 84행 채워서 보고)

```text
| menuId | 원본 파일 | 정규화 파일 | 정규화 fillRatio | 연결 컴포넌트 | 연결 완료 |
|---|---|---|---|---|---|
| 10069 | original/10069_시저치킨-랩.png | menu-normalized/10069.png | (측정값) | MenuCard, MenuDetailSummary | [ ] |
| ... 84행 반복 ... |
```

- 코드(`ASAK-Kiosk`)에서는 React `<img>` 컨테이너에 `object-fit: cover`(정규화된 자산 전제) 또는 `object-fit: contain`(음식 잘림 절대 금지가 우선이면) 중 하나를 **먼저 확정**해서 `commonStyle.css`/`tokens.css`에 규칙으로 추가한다. 현재 `MenuCard.jsx`, `MenuDetailSummary.jsx`, `OrderListItem.jsx` 모두 `<img src={imageUrl}>`만 있고 이미지 크기 관련 CSS 규칙이 스타일 파일 어디에도 없다 — 정규화 자산이 들어와도 프레임 크기 규칙이 없으면 다시 불균일하게 보일 수 있다.

---

## 12. 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-07-17 | Figma MCP로 05-C(938)·06-C(1571) Instance 집계. Legacy 대량 사용·Final 미사용 공식화. 교체 매핑·Agent 지시 추가 |
| 2026-07-17 (추가) | 메뉴 이미지 84개 실측(캔버스·fillRatio) 완료. Figma/CSS 스케일 모드만으로 해결 불가 확인. 전처리 파이프라인·Instance Swap 실행표 템플릿 추가 |

---

*쓰인 컴포넌트는 빠짐없이 §2·§4에 기록했다. 앞으로는 구분선 위 Final만 Production에 연결한다.*

---

# Part C: 유저플로우 · 정책 · 핸드오프 갭


> **작성일:** 2026-07-17  
> **목적:** Figma에 “화면/상태가 있다·연결됐다”고 보이는 것과 **실제 제품 구현·핸드오프 가능 여부**를 분리해 기록한다.  
> **관점:** User Flow / UX / Design→Dev Handoff / Policy Consistency  
> **근거:** Product Bible · `implementation_guide` · ASAK-Kiosk / ASAK-Admin / ASAK-back 코드 · Figma 05-C/06-C 실측  
> **관련 문서:**  
> - Part A(위) — 시각·컴포넌트 복구  
> - Part B(위) — 쓰인 컴포넌트 정본  
> - [`../implementation_guide/00_START_HERE.md`](../implementation_guide/00_START_HERE.md)
> - Part D(아래) — Admin 데이터 위젯 제안

---

## 0. 한 줄 결론

**Figma C 페이지는 “구현 정본 시안 + State 카탈로그”이지, “개발 완료”가 아니다.**  
코드는 **Home → Menu List → Menu Detail(+미니 주문목록)** 까지만 부분 동작하고, **Cart·Payment·Complete·Timeout·Accessibility·Admin 전 구간·Backend business API는 미완/스캐폴드**다.  
핸드오프 관점에서는 **정본 충돌(B vs C), Legacy Component 연결, 필드명·route 불일치, 완료 체크 전부 미체크**가 개발자가 “이미 끝난 줄” 착각하게 만드는 위험이다.

---

## 1. 확정 유저플로우 (제품 정본)

### 1-A. Kiosk Happy Path

```text
SCR-001 Home
  └─ orderType 선택 (EAT_IN | TAKE_OUT)  ← 여기서 한 번만
       ↓
SCR-003 Menu List
  ├─ 카테고리 / (태그·검색은 문서상)
  ├─ 메뉴 카드 → SCR-004
  └─ 하단 장바구니 요약 → SCR-005
       ↓
SCR-004 Menu Detail
  └─ 옵션·제외·수량·알레르기 → 담기
       ↓ (계속 쇼핑 가능)
SCR-005 Cart
  └─ 검토·수정·삭제 → POST 주문 생성
       ↓
SCR-007 Payment
  ├─ 수단 선택 → Processing (연타/뒤로가기 차단)
  ├─ 실패 → SCR-012 (장바구니·주문 유지)
  └─ 성공 → SCR-008 Complete → 세션 초기화 → Home
```

**Overlay / Mode (항상 가능해야 함)**

| ID | 역할 | 핵심 정책 |
|---|---|---|
| SCR-012 | Payment Error | 실패 ≠ 장바구니 삭제. retry 가능 시만 재시도 |
| SCR-013 | Timeout | 무조작 경고→계속/초기화. **Processing 중 timeout 금지** |
| SCR-014 | Accessibility | High Contrast에서도 **같은 주문 순서** |

### 1-B. Admin Happy Path (운영)

```text
SCR-015 Login
  → SCR-022 Dashboard (한눈에 판단)
  → SCR-009 Live Order (상태 전이 + TTS는 성공 후)
  → SCR-010 Order Management (검색·필터·상세)
  → SCR-011 Sold-out (메뉴/재료/옵션 draft→저장)
  → SCR-016 Menu Management
  → SCR-018 Payment Methods
  → SCR-019/020/021 Sales
```

### 1-C. Future Scope (MVP 밖 — 구현·Figma Production 강조 금지)

| ID | 기능 | 상태 |
|---|---|---|
| SCR-023 | 영수증 출력 | Extension / API 미확정 |
| SCR-024 | 멤버십·쿠폰 | Extension / API 미확정 |
| — | QR / Delivery / Refund Primary | Future |

---

## 2. 핵심 정책 목록 (구현·시안이 깨면 Fail)

| # | 정책 | 정본 | 코드/시안 상태 |
|---|---|---|---|
| P1 | **주문유형은 Home에서 1회만.** Menu에서 재질문 금지 | Screen Bible + React 의도 | 코드: Home→`/menu` 직행 ✅ / Figma: Order Type Selection 모달 재질문 ❌ |
| P2 | 화면 예상가 ≠ 최종가. **서버가 가격 권한** | Product Principles | FE `priceCalculation`만 있음. BE 재계산 **없음** |
| P3 | 수량: 메뉴당 **최대 9**, 장바구니 **최대 30**, 최소 1 (`−` 비활성), 삭제는 별도 | `quantityLimits.js` + Cart Bible | FE 일부 ✅. **직원 안내 카피가 메뉴 9에도 붙음** (정책: 30+만 직원이면 충돌) |
| P4 | 동일 메뉴+동일 옵션 → **수량 합치기(MVP 권장)** | Cart Edge Case | `addItem`이 매번 새 `cartItemId` — **합치기 없음** ❌ |
| P5 | 옵션 수정은 **draft**. 저장 전 원본 Cart 불변 | Cart State | Cart 페이지·옵션 수정 플로우 **미구현** |
| P6 | 삭제/전체비우기는 **Confirm** | Cart / ConfirmDialog | OrderList `onRemove` **확인 없음** ❌ |
| P7 | 품절: 핵심재료→메뉴 주문불가 / 일반옵션→옵션만 / **자동삭제 금지** / 결제 전 수정 강제 | MenuCard + Sold-out | MenuCard 표시 규칙 ✅ 방향. `soldOutPolicy.js` **자리표시자**. 장바구니 품절 복구 UI ❌ |
| P8 | 결제 **멱등** (`idempotencyKey`), Processing 중 뒤로가기·연타·timeout 금지 | Payment Flow | Payment 페이지 **자리표시자**, route 미연결 |
| P9 | 결제 실패 후 **장바구니·주문 유지** | Payment / Fixed Rules | 미구현 |
| P10 | Complete 후 history **replace**, 재결제 차단, 세션 reset | SCR-008 | 미구현 |
| P11 | Timeout: warning→계속/초기화. Processing 예외 | Timeout Architecture | **미구현** (체크리스트 전부 미체크) |
| P12 | TTS 실패 ≠ 주문 상태 롤백 | Admin Live Order | Admin 기능 스캐폴드 |
| P13 | 주문 상태 MVP: `RECEIVED → PREPARING → COMPLETED` (취소/환불 Enum 밖) | Admin 가이드 + 감사문서 | Figma에 취소/환불 잔존 위험 |
| P14 | Default만 있으면 **미완료**. Loading/Empty/Error/Disabled/Processing 필수 | Product Principles + 09_FIGMA_STATE | Figma State는 많음 / **코드 State UI 대부분 없음** |
| P15 | Component는 **02-C~04-C Final만** Production 연결 | Component Inventory | 05-C/06-C가 Legacy `4:*` 대량 참조 ❌ |

---

## 3. 실제 코드 유저플로우 (2026-07-17 기준)

```text
[구현됨 · mock]
/  HomePage + OrderTypeSelector
     → setOrderType → /menu
/menu  MenuListPage (mock JSON, CategoryTabs, MenuCard, OrderList 미니카트)
/menu/:menuId  MenuDetailPage (옵션·수량·priceCalculation·addItem)
     → replace 로 /menu 복귀

[파일만 있거나 자리표시자 · Router 미연결]
CartPage.jsx, PaymentPage.jsx, OrderCompletePage.jsx,
AccessibilityPage.jsx, ReceiptActions.jsx
→ KioskApp Routes에 없음

[Admin]
ASAK-Admin: 사이드바 + “기능은 일정에 따라…” Empty 스캐폴드만
  routes: /, /sold-out, /menus, /payment-methods, /sales
  누락: /login, /orders/live, /orders, Dashboard≠Live 혼동,
        /sales/monthly, /sales/daily
ASAK-Kiosk 안에 admin pages/components 잔존 (앱 경계 혼선)

[Backend]
GET /api/health 만. 주문·결제·품절·매출 API 없음
```

### 라우트 정합

| Screen | Registry route | 실제 앱 | 판정 |
|---|---|---|---|
| SCR-001 | `/` | Kiosk `/` | 부분 |
| SCR-003 | `/menu` | `/menu` | 부분 (API mock, Footer CTA 약함) |
| SCR-004 | `/menu/:menuId` | 있음 | 부분 (제외재료·알레르기·품절옵션·수정모드 약함) |
| SCR-005 | `/cart` | **없음** | Fail |
| SCR-007 | `/payment` | **없음** | Fail |
| SCR-008 | `/complete` | **없음** | Fail |
| SCR-012/013/014 | overlay / `/accessibility` | **없음** | Fail |
| Admin 전 구간 | Registry 표 | Admin 스캐폴드·route 불일치 | Fail |
| SCR-023/024 | extension | ReceiptActions 자리표시자만 | Future (의도적 보류) |

---

## 4. Figma “있어 보임” ≠ 구현 완료 — 화면별 체크

> 규칙: Figma에 Default/State Frame이 있어도, **Router + 상태머신 + API/mock 계약 + 정책 행동**이 없으면 `디자인만`.  
> `implementation_guide`의 **완료 체크는 전부 `[ ]`**. START_HERE도 “링크 = 구현 완료 아님”을 명시.

| SCR | Figma(05-C/06-C) | 코드 | Backend | UX 완료? | 핸드오프 가능? | 비고 |
|---|---|---|---|---|---|---|
| 001 Home | State 있음. **주문유형 재질문 모달 P0** | 선택→메뉴 직행 | — | 부분 | △ | 시안이 정책(P1)과 충돌 |
| 003 Menu List | Loading/Empty/Error/품절 등 | mock 목록·Empty 일부 | 없음 | 부분 | △ | 검색/태그·Footer BottomCTA·Toast 약함 |
| 004 Menu Detail | State 풍부. 텍스트 잘림·옵션 컴포넌트 미사용 | 담기·수량·옵션 기본 | 없음 | 부분 | △ | 제외재료 `[]` 고정, 합치기 없음, Legacy OrderDetailRow 598건 |
| 005 Cart | State 풍부 | **미연결** | 주문 API 없음 | ❌ | ❌ | OrderList≠Cart 전용 화면 |
| 007 Payment | Processing/수단 등 | **미연결** | 결제 API 없음 | ❌ | ❌ | |
| 008 Complete | 양호에 가깝고 receipt Future | **미연결** | — | ❌ | ❌ | |
| 012 Error | 있음 | 없음 | — | ❌ | ❌ | |
| 013 Timeout | 있음 | 없음 | — | ❌ | ❌ | |
| 014 A11y | 있음 | 자리표시자 | — | ❌ | ❌ | |
| 015 Login | 있음 | Admin 미연결 | 인증 미확정 | ❌ | ❌ | |
| 022 Dashboard | 있음 | Admin `/`가 Live 라벨 | 없음 | ❌ | ❌ | **정보구조 혼동** |
| 009 Live | 있음 | 스캐폴드 | 없음 | ❌ | ❌ | TTS·409 복구 없음 |
| 010 Orders | 있음 | 스캐폴드 | Draft | ❌ | ❌ | |
| 011 Sold-out | 있음 | 스캐폴드 | 없음 | ❌ | ❌ | |
| 016 Menus | 있음 | 스캐폴드 | 없음 | ❌ | ❌ | |
| 018 Pay methods | 있음 | 스캐폴드 | 없음 | ❌ | ❌ | |
| 019–021 Sales | 있음 | `/sales` 하나 | 없음 | ❌ | ❌ | monthly/daily 분리 없음 |
| 023–024 Ext | Registry Draft | Receipt 자리표시자 | 미확정 | Future | 보류 | Production 강조 금지 |

---

## 5. UX · 유저플로우 문제 (정책 대비)

### P0 — 주문 끊김

1. **담기 후 Cart/결제 경로 없음**  
   Detail → Menu만 복귀. 전용 Cart·Payment route 없음 → **주문을 끝낼 수 없음**.
2. **미니 OrderList ≠ Cart 정책**  
   목록 하단 주문내역으로 수량/삭제는 되나, Confirm·옵션수정·주문생성·가격변경 안내·품절 수정 강제가 없음.
3. **Figma Home이 주문유형을 두 번 묻게 보임**  
   코드는 1회 선택인데 시안이 재질문 → 핸드오프 시 개발자가 잘못된 Prototype을 따라갈 위험.

### P1 — 신뢰·복구

4. Loading/Error가 목록·상세에 거의 없음 → 실패가 “빈 화면/깨짐”으로 보임.  
5. 결제 Processing/Timeout/실패 복구 시안은 있으나 코드·프로토타입 연결 불명확.  
6. 품절 후 장바구니에 남은 항목을 **고치게 하는 UX** 없음 (자동삭제 금지 정책과 맞추려면 반드시 필요).  
7. 메뉴 9개 제한 토스트에 **“직원에게 문의”** — 카트 30 정책과 카피 충돌 가능.

### P1 — Admin 판단 3초 원칙

8. Dashboard / Live / Orders route·라벨이 Registry와 어긋남 → 운영자가 “지금 뭐 보는 화면인지” 학습 비용↑.  
9. TTS·409·저장 중 잠금이 없으면 Live Board는 **위험한 버튼 나열**이 됨.

### P2 — 세부 마찰

10. 동일 구성 재담기 시 줄이 늘어남 (합치기 없음).  
11. 제외 재료·알레르기 Accordion 약함/미연결.  
12. High Contrast 미구현 → 접근성 모드 진입만 문서에 존재.  
13. Future 영수증 UI 파일이 Kiosk에 있어 MVP와 혼동.

---

## 6. 핸드오프(Design ↔ Dev ↔ Backend) 문제

### 6-A. Source of Truth 충돌

| 문서 | 말하는 최신 화면 | 문제 |
|---|---|---|
| `implementation_guide` / UI Guide | **05-C / 06-C / 07-C** | 현재 작업 기준 |
| `CANONICAL_SOURCE.md` | 아직 **05-B / 06-B**, C는 Premium 제안 | **핸드오프 혼란 P0** — 문서 동기화 필요 |
| Figma Production | 05-C/06-C지만 **Legacy Instance** | “C 완료”처럼 보여도 Dev 정본 컴포넌트 아님 |

### 6-B. “완료” 오해 지점

| 신호 | 실제 의미 |
|---|---|
| Figma Prototype 연결 | 데모 클릭 가능 ≠ 전 State·정책 통과 |
| 07-C QA Matrix 칸 존재 | 검수 **표**이지 통과 기록 아님 |
| 02~04-C Component Set 존재 | Master 있음 ≠ 05-C/06-C가 그걸 씀 |
| React Page 파일 존재 | **Router 미등록·자리표시자** 다수 |
| API 표가 가이드에 있음 | **목표 계약**. Backend는 health만 |
| Component Map의 `BottomCTA.jsx` 등 | **아직 없거나 이름 다른** 컴포넌트와 매핑됨 |

### 6-C. 계약·이름 불일치 (adapter 필수)

| 목표 API | mock/store 현재 | 위험 |
|---|---|---|
| `menuName` | `name` | 화면/서버 매핑 누락 |
| `basePrice` | `price` | |
| `calories` | `baseKcal` | |
| `additionalAmount` | `extraPrice` | |
| `totalAmount` | `totalPrice` | |
| Admin `/soldOut` | Admin 앱 `/sold-out` | route 문서≠코드 |
| `/paymentMethods` | `/payment-methods` | 동일 |
| `/orders/live` | Admin `/`를 “주문 현황” | SCR-022 vs 009 혼동 |

### 6-D. 앱 경계

- 관리자 페이지·컴포넌트가 **ASAK-Kiosk**에도 있음 / **ASAK-Admin**은 빈 껍데기.  
- 핸드오프 시 “어느 저장소가 정본 React인가”를 먼저 고정해야 함 → Canonical: **Kiosk / Admin 분리**.

### 6-E. Figma → React 핸드오프 차단 요인

1. Production이 Legacy Component를 씀 → 토큰·Variant props가 Final과 다름.  
2. OptionSelectionRow 등 Final이 화면에 0건 → Detail 구현자가 수동 Frame을 복제하기 쉬움.  
3. Visual Recovery 미완(다크 품절, CTA 높이, 텍스트 잘림) → “시안 그대로” 구현하면 **정책·가독성 Fail**.  
4. `__manual-check` / Mock settings / Future를 Production처럼 넘기면 BE에 없는 API를 요구하게 됨.

---

## 7. 정책 vs 구현 vs 시안 — 충돌 티켓

| ID | 충돌 | 권장 결정 |
|---|---|---|
| C1 | Figma 주문유형 재질문 vs 정책·코드 1회 | **시안 Archive + Prototype을 Home 1회만**으로 |
| C2 | CANONICAL_SOURCE B vs Guide C | **CANONICAL_SOURCE를 05-C/06-C로 갱신** |
| C3 | 메뉴9 토스트 직원 카피 vs 30만 직원 | 카피 정책 문서화 후 `TOAST_MESSAGES` 수정 |
| C4 | Cart 합치기 권장 vs 항상 새 line | MVP: 담기 시 merge 로직 추가 |
| C5 | Delete Confirm 필수 vs OrderList 즉시 삭제 | ConfirmDialog 연결 |
| C6 | Registry route vs Admin kebab-case | 한쪽으로 통일 + 가이드 수정 |
| C7 | Admin `/` = Dashboard인데 앱은 Live 라벨 | SCR-022와 SCR-009 분리 |
| C8 | Figma Enum 취소/환불 vs MVP 3상태 | Production Variant 제거/`__manual-check` |
| C9 | Receipt UI 파일 vs Future Scope | Extension 폴더·문서만, MVP route 금지 |
| C10 | Component Map 파일명 vs 실제 소스 | Map을 현행 파일에 맞게 갱신 |

---

## 8. 구현 백로그 (핸드오프 순서 권장)

### Wave 0 — 착각 제거 (문서·Figma, 코드 최소)

1. CANONICAL_SOURCE를 **05-C/06-C**로 맞춤.  
2. Figma BATCH1: 주문유형 중복 제거.  
3. Legacy→Final Component Swap (인벤토리 §7).  
4. Admin route 표 ↔ 앱 path 통일안 확정.

### Wave 1 — 주문을 끝낼 수 있게 (Kiosk P0)

5. `/cart`, `/payment`, `/complete` Route + 페이지 연결.  
6. Cart: Confirm 삭제, 옵션수정 draft, 합치기, 품절 수정 게이트, POST order(mock 가능).  
7. Payment: 수단·Processing·멱등·Error·실패 시 유지.  
8. Complete: replace + `resetSession`.  
9. Timeout + Processing 예외.  
10. 필드 adapter (`name`↔`menuName` …).

### Wave 2 — 상태·품절·접근성

11. Menu List/Detail Loading·Error.  
12. soldOutPolicy 실구현 + Cart 연동.  
13. 제외 재료·알레르기.  
14. Accessibility High Contrast 전 흐름.  
15. 토스트 카피 정책 정리.

### Wave 3 — Admin + Backend

16. Backend: menu/order/payment/soldOut envelope.  
17. Admin Login·권한 계약 확정.  
18. Live Order + 상태전이 + TTS 실패 분리.  
19. Sold-out SaveBar·Confirm.  
20. Dashboard / Sales 기간 API.  
21. Kiosk↔Admin 결제수단 동기화.

### Wave 4 — Extension (의도적 후순위)

22. SCR-023/024 계약 확정 후에만.

---

## 9. 화면 상태 구현 매트릭스 (09_FIGMA_STATE_CHECKLIST 요약)

| 영역 | Figma State 존재 | 코드 반영 | 비고 |
|---|---|---|---|
| Kiosk Default | 많음 | 001/003/004만 | |
| Kiosk Loading/Empty/Error | 많음 | 거의 없음 | Empty 일부만 |
| Kiosk Sold-out 표현 | 많음 | MenuCard 방향만 | 다크 오버레이는 시안 문제 |
| Kiosk Payment/Timeout | 많음 | 0 | |
| Admin 전 State | 많음 | 0 (스캐폴드 문구) | |
| Extension | Draft | 보류 | |

**판정문 (핸드오프용):**  
> “Figma 05-C/06-C에 State가 채워져 있다” = **디자인 카탈로그 준비도**.  
> “구현 완료” = Router + 정책 행동 + (mock 또는) API + QA 체크리스트 PASS.

---

## 10. 개발자·디자이너 체크 질문 (리뷰용)

**디자이너 → Dev 넘기기 전**

- [ ] 이 Frame의 mainComponent가 02~04-C Final인가? (Legacy `4:*`면 Fail)  
- [ ] Prototype이 정책 P1(주문유형 1회)을 따르는가?  
- [ ] Future/Refund/영수증이 Production CTA로 강조되지 않는가?  
- [ ] Loading/Empty/Error/Disabled가 같은 SCR에 있는가?  
- [ ] 카피·Enum이 Bible과 같은가?

**개발자 → “화면 완료” 선언 전**

- [ ] Registry route가 App에 있는가?  
- [ ] 완료 체크(02/03 가이드)를 실제로 통과했는가?  
- [ ] 서버 없으면 mock임을 UI/코드에 명시했는가?  
- [ ] 가격·품절·수량이 단일 유틸/정책을 쓰는가?  
- [ ] 실패 후 장바구니/선택이 유지되는가?

**Backend → Front 연결 전**

- [ ] envelope·error code가 가이드와 같은가?  
- [ ] 가격 재계산·멱등·상태전이가 Service에 있는가?  
- [ ] DTO 필드명이 Front adapter 표와 맞는가?

---

## 11. Claude 재검증 — 확인·정정·신규 발견 (2026-07-17 추가)

> `ASAK-Kiosk`(§18 별도 재검증), `ASAK-Admin`, `ASAK-back`, `CANONICAL_SOURCE.md`를 직접 다시 읽어 이 문서의 핵심 주장을 교차검증했다. **대부분 독립적으로 일치**했고, 3건은 실제로 열어보니 더 심각했다.

### 11-1. 확인됨 (그대로 유지)

- ASAK-back은 정말 `HealthController.java` 하나뿐이다. Menu/Order/Payment/SoldOut 관련 Controller/Service/Repository가 **0개**.
- 코드 유저플로우(§3)와 라우트 정합표(같은 절)는 제가 별도로 `ASAK-Kiosk`를 읽고 검증한 결과(Full Audit §18)와 **완전히 일치**한다: Home→Menu List→Menu Detail만 동작, Cart/Payment/Complete 라우트 없음. 두 검증이 독립적으로 같은 결론에 도달했다는 건 이 판정의 신뢰도가 높다는 뜻이다.

### 11-2. C2(CANONICAL_SOURCE B vs Guide C) — 확인, 원문 인용

`ASAK/docs/product_bible/01_Foundation/docs/00-product-bible/CANONICAL_SOURCE.md` §3을 직접 읽었다. 실제 원문:

```text
현재 최신 기준:
- 05-B Screens/Kiosk
- 06-B Screens/Admin
- 07 User Flows & Prototype

Premium 제안:
- 05-C Screens/Kiosk Premium
- 06-C Screens/Admin Premium
```

같은 문서 §6 "Conflict Resolution Order"의 1순위는 "승인된 Decision/ADR", 2순위가 "Canonical Registry"다. **CANONICAL_SOURCE 자체의 규칙에 따르면, 이 문서가 갱신되지 않는 한 지금은 B가 C보다 공식적으로 우선한다.** 반면 `implementation_guide/05_UI_COMPONENT_GUIDE.md`는 "Screen Registry와 승인된 05-C/06-C가 화면 기준"이라고 명시해 **정반대로 말한다.** 이건 단순 누락이 아니라 **Bible 최상위 문서 두 개가 서로 다른 화면을 정본이라고 주장하는 실제 충돌**이다. 권장(C2)과 동일: CANONICAL_SOURCE §3을 05-C/06-C 기준으로 갱신하는 게 최우선이다 — 이게 안 되면 이 문서 전체("C가 정본")의 전제 자체가 상위 문서와 충돌한 채로 진행되는 셈이다.

### 11-3. ASAK-Admin 실제 구조 — 예상보다 더 심각

`ASAK-Admin/src/apps/AdminApp.jsx`를 직접 읽었다. 이 문서의 "Admin 스캐폴드" 판정은 맞지만, 실제로는 그 이상의 문제가 있다.

- **`AdminApp.jsx`가 실제 라우팅을 전부 자체 inline으로 처리한다.** `pages/admin/*.jsx`(OrderListPage, SoldOutManagePage, MenuManagePage 등)와 `components/admin/AdminSidebar.jsx`, `layouts/AdminLayout.jsx`는 **전부 1줄짜리 주석 파일이고 어디서도 import되지 않는다.** 실제 사이드바/화면은 `AdminApp.jsx` 안에 직접 정의된 `menus` 배열과 `AdminScreen` 컴포넌트가 담당한다.
- 실제 라우트는 `["/","주문 현황","SCR-009"], ["/sold-out","품절 관리","SCR-011"], ["/menus","메뉴 관리","SCR-016"], ["/payment-methods","결제수단","SCR-018"], ["/sales","매출","SCR-019"]` 5개뿐이다.
- **`/`가 "주문 현황"이라는 라벨과 `SCR-009`(Live Order) ID를 달고 있다.** Screen Registry는 `/` = SCR-022 Admin Dashboard로 정의하는데, 실제 앱에는 **Dashboard 라우트 자체가 없다.** 이 문서 C7("Admin `/` = Dashboard인데 앱은 Live 라벨")보다 더 정확히 말하면: **Dashboard 라우트가 없는 게 아니라 존재하지 않는다 — SCR-009와 SCR-022가 같은 경로에 뒤섞인 게 아니라, SCR-022가 아예 없다.**
- `/login`도 라우트에 없다(`LoginPage.jsx` 파일은 있으나 미연결). `useAdminAuth.js` hook 파일도 존재하나 `AdminApp.jsx`에서 쓰이지 않는다.

**신규 위험(이 문서에 없던 내용):** `pages/admin/*.jsx` 폴더 전체가 죽은 코드다. 개발자가 "화면 기능은 일정에 따라 구현한다"는 안내 문구를 보고 `OrderListPage.jsx`를 채워 넣어도, `AdminApp.jsx`가 그 파일을 참조하지 않는 한 화면에 아무 변화가 없다. **Wave 3(Admin) 착수 전에 `AdminApp.jsx`를 `pages/admin/*.jsx` import 구조로 먼저 리팩터링하거나, 반대로 `pages/admin/*.jsx`를 삭제하고 inline 구조를 유지할지 팀이 먼저 정해야 한다.** 이걸 안 정하면 Wave 3 시작부터 "어느 파일을 고쳐야 하는지" 다시 헤매게 된다.

### 11-4. Admin Insight Sections 문서와의 정합성

Part D의 Dashboard 확장안(§2)은 위에서 확인한 대로 **Dashboard 라우트 자체가 없는 상태**에 대한 제안이다. 즉 그 문서의 위젯 우선순위(P0~P3)를 실행하려면 이 문서의 Wave 3 순서(16 Backend → 17 Login → 18 Live Order → 20 Dashboard)보다, **"AdminApp.jsx에 `/` = Dashboard 라우트를 실제로 추가하는 작업"이 먼저** 있어야 한다. Wave 3 목록에 이 항목을 20번 앞에 별도로 추가하는 걸 권장한다.

### 11-5. DB 스키마 대조 — Admin Insight 제안의 실현 가능성

`asak-data/schema-backups/short-name-before-20260713-115747.sql`을 확인했다. `orders.created_at`, `orders.order_type_id`(FK→`common_code`), `payment.method_id`(FK→`common_code`), `category` 테이블 존재를 확인했다 — **Admin Insight Sections가 제안한 시간대별/유형별/카테고리별/결제수단별 집계(A1~A4)는 DB 스키마상 실현 가능**하다. 다만 Controller/Service가 전혀 없으므로(§11-1) "이미 모을 수 있는 데이터"는 정확히는 "**DB에 컬럼은 있으나 API로 꺼내는 코드는 아직 없는 데이터**"로 읽어야 한다 — Admin Insight 문서 자체의 표현("이미 모을 수 있는")이 백엔드 미착수 상태에서는 다소 낙관적으로 들릴 수 있어 짚어둔다.

---

## 12. 실무 트리아지 기준과 통합 우선순위 (2026-07-17 추가)

> 4개 문서(Part A, Part B, 이 문서, Part D)에 흩어진 문제를 **"뭐부터 처리하나"** 하나의 순서로 합친다. "제일 급해 보이는 것"과 "제일 먼저 해야 하는 것"은 다르다 — 아래는 후자 기준이다.

### 12-1. 판단 기준 (5원칙)

1. **결정 비용 0인 것부터.** 작업 시간은 안 드는데 다른 작업 전부를 막고 있는 "미결정" 항목이 항상 1순위다.
2. **"뭐가 진실인지" 충돌부터 없앤다.** 문서·화면이 서로 다른 답을 하면, 개별 항목을 고치기 전에 기준을 하나로 합친다. 안 그러면 같은 걸 두세 번 고친다.
3. **핵심 흐름이 끊긴 곳을 가장 먼저 잇는다.** "이 제품이 하는 단 하나의 일"이 처음부터 끝까지 되는지가 시각 품질보다 우선이다.
4. **영향 범위(blast radius)가 큰 공용 요소를 화면 하나하나보다 먼저 고친다.** 공용 컴포넌트/스토어 하나를 고치는 게 화면 10개를 따로 고치는 것보다 레버리지가 크다.
5. **"지금 안 보인다"와 "안전하다"는 다르다.** 지금 사용 0건이라 조용한데 특정 작업(Instance Swap 등) 순간 한꺼번에 터지는 항목은 순위를 앞으로 당긴다. 돈·수량·중복결제처럼 데이터 정합성에 관련된 버그도 눈에 안 띄어도 앞당긴다.

### 12-2. 통합 우선순위 (전 문서 cross-reference)

| 순위 | 항목 | 근거 문서 | 왜 이 순위인가 (5원칙 매핑) |
|---|---|---|---|
| 1 | **CANONICAL_SOURCE의 B/C 충돌 해결** — §3을 05-C/06-C 기준으로 갱신 | 이 문서 §11-2 (C2) | 원칙 1+2. 문서 한 줄 수정이 전제인데, 안 끝나면 "C가 정본"이라는 이후 모든 작업이 상위 문서와 충돌한 채 진행됨 |
| 2 | **AdminApp.jsx 구조 결정**(inline 유지 vs `pages/admin/*.jsx` 참조로 전환) | 이 문서 §11-3 | 원칙 1. 결정만 하면 끝. Admin 작업(Wave 3) 착수 전 필수 |
| 3 | **Touch Target 토큰 확정**(01-C에 `size-touch-min` 하나로) | Part A §17-2(6) | 원칙 1. Bible 80 / candidate-B 44 / 통합안 64 중 하나로 결정만 하면 QuantityStepper·BottomCTA·체크박스가 전부 그 값을 참조 가능 |
| 4 | **Home 주문유형 재질문 제거**(BATCH 1) | Part A §12(BATCH1), 이 문서 §2(P1) | 원칙 3. 핵심 흐름의 첫 관문. 여기가 안 고쳐지면 이후 화면이 다 맞아도 사용자는 처음부터 막힘 |
| 5 | **Cart/Payment/Complete 라우트 연결 + Menu List 이동 버튼** | 이 문서 §3, §5(P0-1,2) | 원칙 3. 핵심 흐름의 완주. "주문을 끝낼 수 있는가"가 다른 모든 시각 작업보다 먼저 되어야 제품으로서 의미가 생김 |
| 6 | **이미 구현된 코드의 실제 버그**(quantityLimits 문구 반전, 품절 CTA 미차단, addItem 병합 없음, 삭제 컨펌 없음) | Part A §18-2, 이 문서 §2(P3,P4,P6) | 원칙 5(데이터·정책 정합성). 규모는 작아도 신뢰 직결 + 다음 화면(Cart)에 그대로 복사될 위험 |
| 7 | **OptionSelectionRow 기본 상태 수정**(Legacy→Final Swap 실행 전 선행) | Part B §3, Part A §17-2(2) | 원칙 5. 지금 사용 0건이라 조용하지만 Swap 순간 598개 인스턴스가 한 번에 이 상태를 물려받음 |
| 8 | **Legacy→Final 대량 Swap**(OrderDetailRow 598 / OrderMenuOptionItem 576 / MenuButton 384) | Part B §7, §9 | 원칙 4. 화면별로 따로 손대는 것보다 여기 하나 스왑하는 게 전체 Legacy 잔존율을 가장 크게 줄임 |
| 9 | **Lime Accent 통일 + Dark Surface 5곳** | Part A §12(BATCH7) | 규모는 크지만 흐름·데이터에 영향 없는 "보이는 문제" — 위 항목들 다음 |
| 10 | **Admin Dashboard 라우트 신설 + Insight 위젯**(A1~A8) | Part D §2, §12 | Backend API·Dashboard 라우트라는 선행 조건이 있어 후순위. 단 순서 2번(AdminApp 구조 결정)이 끝나면 바로 이어서 진행 가능 |
| 11 | **세부 폴리시**(네온 글로우 잔재, 여백, 카피 오타, 문서 카운트 불일치 등) | Part A §11(P2 다수) | 기능에 영향 없음. 여유 있을 때 |

**한 줄 요약: 결정(1~3) → 흐름 완주(4~5) → 코드 정합성(6) → 숨은 폭탄 선제 제거(7) → 공용 요소 규모 정리(8) → 시각 통일(9) → 후속 확장(10) → 폴리시(11).**

### 12-3. 기존 Wave/BATCH와의 매핑

이 순서는 §8 "구현 백로그(Wave 0~4)"와 Part A §12 "BATCH 0~11"을 대체하지 않는다 — **어떤 Wave/BATCH를 먼저 착수할지 고르는 상위 기준**이다.

```text
순위 1~3 (결정)        → Wave 0 착수 전 선행 조건으로 추가
순위 4    (BATCH 1)    → Wave 0의 2번, Part A BATCH 1
순위 5    (Wave 1)     → 이 문서 Wave 1의 5~8번과 동일
순위 6    (코드 버그)   → Wave 1의 6, 10번과 동일(이미 백로그에 있음, 순서만 위로 당김)
순위 7~8  (BATCH 2-A~2-D) → Part A §17-3 수정 배치와 동일
순위 9    (BATCH 7)    → Part A BATCH 7
순위 10   (Wave 3 일부) → Wave 3의 20번을 앞으로 당김(§11-4 근거)
순위 11   (Wave 2~4 나머지) → 그대로
```

---

## 13. 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-07-17 | 유저플로우·정책·Figma↔코드↔BE 갭·핸드오프 충돌을 별도 문서로 최초 작성 |
| 2026-07-17 (추가) | Claude가 CANONICAL_SOURCE.md 원문·ASAK-Admin 실제 라우팅·ASAK-back·DB 스키마를 직접 재검증. B/C 충돌 원문 확인, AdminApp.jsx가 pages/admin 폴더를 전혀 참조하지 않는 죽은 코드 구조 신규 발견, Admin Insight 문서와의 실행 순서 정합·DB 실현 가능성 확인 추가 |
| 2026-07-17 (추가2) | 실무 트리아지 5원칙 + 4개 문서 통합 우선순위 11단계 추가. 기존 Wave/BATCH 구조와의 매핑표 포함 |

---

*이 문서는 시각 복구(Part A)·컴포넌트 인벤토리(Part B)와 함께 본다. “시안 완료”와 “제품 완료”를 같은 말로 쓰지 않는다.*

---

# Part D: Admin 데이터 위젯 제안


> **작성일:** 2026-07-17  
> **목적:** 관리자 화면에 **새 데이터 소스 없이** 주문·결제·품절·메뉴에서 이미(또는 곧) 쌓이는 값만으로 운영 판단 섹션을 보강한다.  
> **원칙:**  
> - Dashboard 상단 KPI는 Bible대로 **4개 유지** (순매출 / 주문 수 / 객단가 / 진행 중).  
> - “더 볼 정보”는 **본문 위젯·보조 섹션**으로 둔다.  
> - 회원·재방문·목표·전년비·환불률 등 **추가 계약 필요 지표는 넣지 않는다** (`SALES_ARCHITECTURE` §3).  
> - Future Scope(영수증 통계, 쿠폰, QR) 금지.

**관련:** Part C · Dashboard/Sales Bible

---

## 1. 지금 모을 수 있는 원천 데이터

주문·결제·품절·메뉴 CRUD만 있어도 아래는 **서버에서 집계 가능**하다.

| 원천 필드 | 출처 |
|---|---|
| `orderId`, `orderNo`, `createdAt`, `updatedAt` | 주문 |
| `orderType` (`EAT_IN` / `TAKE_OUT`) | 주문 |
| `orderStatus` (`RECEIVED` / `PREPARING` / `COMPLETED`) | 주문 |
| `paymentStatus`, `approvedAmount`, `approvedAt`, `paymentMethodCode` | 결제 |
| `items[].menuId`, `menuName`, `quantity`, `lineAmount` | 주문 항목 |
| `categoryCode` (메뉴 마스터 조인) | 메뉴 |
| `selectedOptionItemIds` / 옵션명 | 주문 항목 |
| `excludedIngredientIds` | 주문 항목 |
| `isSoldOut` + `targetType` (MENU / INGREDIENT / OPTION_ITEM) | 품절 |
| 상태 변경 시각 (`RECEIVED→PREPARING→COMPLETED` 시각) | 주문 이력(권장: status history 또는 `updatedAt` 근사) |

**의도적으로 안 쓰는 것:** 고객 식별자, 멤버십, 쿠폰, 환불 원장(MVP 없음), 키오스크 세션 ID(계약 전).

---

## 2. Dashboard (SCR-022) — KPI 아래 “더 볼 정보”

상단 4 KPI는 유지. 본문에 아래 위젯을 **우선순위 순**으로 배치한다.

### 이미 Bible에 있는 것 (반드시 살릴 것)

| 섹션 | 계산 | 운영자가 보는 이유 |
|---|---|---|
| 상태별 주문 수 | RECEIVED / PREPARING / COMPLETED 오늘 건수 | 주방 부하 |
| 최근 주문 | 최신 N건 요약 → Live로 이동 | 바로 처리 |
| 인기 메뉴 TOP 5 | 오늘 승인 주문의 메뉴 수량 합 | 재고·준비 |
| 품절 현황 | 메뉴/재료/옵션 품절 건수 + 바로가기 | 판매 손실 방지 |
| 운영 알림 | 아래 §2-B “알림 규칙” | 액션 유도 |

### 추가 추천 (데이터만으로 가능 · MVP+)

| 우선 | 섹션 이름 | 데이터 계산 | CTA |
|---:|---|---|---|
| **A1** | **매장 / 포장 비율** | 오늘 승인 주문의 `orderType` 비율 (건수·금액) | Sales 상세 |
| **A2** | **시간대 스냅샷 (오늘)** | 시(hour)별 주문 수 또는 매출 미니 바 | Daily Sales |
| **A3** | **카테고리별 오늘 매출** | menu→category 조인 후 TOP/전체 | Menu·Sales |
| **A4** | **결제수단 비율** | `paymentMethodCode`별 승인 건수·금액 | 결제수단 설정 |
| **A5** | **대기·조리 신호** | 진행 중 주문 중 `RECEIVED` 경과 분(지금−createdAt), `PREPARING` 경과 분 | Live Board 필터 |
| **A6** | **평균 처리 시간 (오늘)** | COMPLETED 주문의 (completedAt−createdAt) 평균·중앙값 | 주방 리듬 |
| **A7** | **품절 영향 힌트** | 품절 재료/옵션이 걸린 **메뉴 수** (affectedMenuCount) | 품절 관리 |
| **A8** | **옵션·제외 인사이트 (오늘)** | 옵션 선택 TOP / 제외 재료 TOP | 메뉴·재고 |

> **KPI 4개 규칙:** A1~A8은 카드/리스트 위젯이지 상단 KPI 슬롯을 늘리지 않는다.  
> **Empty:** 주문 0이면 “오늘 주문 없음” + 객단가 `-`와 동일 톤.

### 2-B. 운영 알림 규칙 (새 데이터 없음)

| 알림 | 조건 (예시 임계는 설정 가능) | 액션 |
|---|---|---|
| 대기 적체 | RECEIVED ≥ N건 또는 최장 대기 ≥ M분 | Live로 |
| 품절 급증 | 오늘 품절 토글 ≥ N회 또는 핵심 메뉴 품절 | 품절 관리 |
| 결제수단 전부 비활성 | Admin 설정상 ENABLED 0 | 결제수단 |
| 피크 임박 | 최근 1시간 주문 수가 오늘 평균 시간대보다 높음 | Live·주방 |

---

## 3. Live Order (SCR-009) — 보드 옆/위 보조 정보

보드 본체는 카드 처리. **옆에 붙일 정보:**

| 섹션 | 계산 | UX |
|---|---|---|
| **지금 대기열** | RECEIVED 건수, 최장 대기 분 | 숫자+색 (색만으로 의미 전달 금지, 분 표기) |
| **조리 중** | PREPARING 건수, 평균 조리 경과 | |
| **오늘 완료** | COMPLETED 오늘 건수 | 동기부여용, 작게 |
| **유형 뱃지 집계** | 진행 중 EAT_IN vs TAKE_OUT | 포장 우선 등 운영 힌트 |
| **방금 들어온 옵션 요약** | 최근 RECEIVED의 옵션/제외 한 줄 | 상세 열기 전 프리뷰 |

TTS 실패는 **주문 상태와 분리된 토스트/배너** (기존 정책 유지).

---

## 4. Order Management (SCR-010) — 목록 위 요약 스트립

필터 위에 **기간 내 집계 스트립** (목록 API와 같은 필터 적용):

| 칩/미니 KPI | 계산 |
|---|---|
| 건수 | 필터된 주문 수 |
| 매출 합 | APPROVED `approvedAmount` 합 |
| 객단가 | 합/건수 |
| 유형 비율 | EAT_IN : TAKE_OUT |
| 상태 분포 | 미니 도넛 또는 텍스트 |

상세 패널 하단 **같은 주문의 라인 인사이트 (선택):**

- 옵션 추가금 합 / 제외 재료 수 (이미 상세에 있는 필드 재사용)
- “이 메뉴 오늘 N번째” (같은 menuId 오늘 count) — 있으면 재고 감각

---

## 5. Sold-out (SCR-011) — 토글 너머 정보

| 섹션 | 데이터 | 가치 |
|---|---|---|
| **영향 메뉴 수** | 재료/옵션 품절 시 affected menus (Bible에 이미 있음) | 저장 전 판단 |
| **품절 중인 항목 요약** | type별 count + 이름 리스트 | Dashboard와 동일 정의 |
| **오늘 품절 변경 로그** | soldOut PATCH 감사 로그(누가/언제/무엇) — **저장 API 성공 시 쌓을 수 있음** | 책임·복구 |
| **인기인데 품절** | 오늘 popular ∩ 현재 soldOut | 매출 기회 손실 |

---

## 6. Sales (SCR-019~021) — Bible “계산 가능”을 섹션으로 고정

문서에 이미 있으나 시안에서 약한 항목을 **필수 섹션**으로 명시한다.

| 화면 | 섹션 | 원천 |
|---|---|---|
| Summary | 매출 추이 | 일별 승인 금액 |
| Summary | **시간대별 주문·매출** | `createdAt` hour |
| Summary | 인기 메뉴 | menu+qty |
| Summary | **카테고리별 매출** | categoryCode |
| Summary | **주문 유형 비율** | orderType |
| Summary | **결제수단 비율** | paymentMethodCode (Admin에 수단 있으면) |
| Summary | 상세표 | 주문 단위 |
| Monthly | 월별 추이·전월 대비·건수·객단가 | 월 집계 |
| Daily | 피크타임·시간대·인기·주문 상세 | 해당일 |

비교 라벨은 preset에 맞게 (전일/전주/전월/직전 동일기간) — 고정 “전월” 금지.

---

## 7. Menu Management (SCR-016) — 가벼운 운영 힌트

메뉴 상세/목록에 **주문 데이터 조인만으로:**

| 힌트 | 계산 |
|---|---|
| 최근 7일 판매 수량 | 해당 menuId qty 합 |
| 오늘 담긴 옵션 TOP | 해당 메뉴의 optionItem 빈도 |
| 자주 제외되는 재료 | excludedIngredient 빈도 |
| 현재 품절 여부 | soldOut 플래그 |

→ 메뉴 수정 화면에 “최근 판매·구성 힌트” 접이식 섹션.

---

## 8. Payment Methods (SCR-018) — 설정 + 사용 실적

| 섹션 | 계산 |
|---|---|
| 수단별 오늘/기간 승인 건수·금액 | paymentMethodCode |
| 비활성 수단에 대한 “최근 7일 비중” 경고 | 끄기 전 확인 카피 |

전체 비활성 시 Dashboard 알림과 동일 메시지.

---

## 9. 넣지 말 것 (지금 데이터로 가짜 완성도 내기)

| 지표 | 이유 |
|---|---|
| 고유 고객 수 / 재방문율 | 식별자 없음 |
| 회원·쿠폰·적립 | Future / API 미확정 |
| 목표 달성률·전년 대비 | 목표·작년 원장 계약 필요 |
| 환불률 | MVP 환불 없음 |
| “만족도” | 수집 채널 없음 |
| 키오스크 이탈률 | 세션 이벤트 계약 전 |

이런 칸이 Figma에 있으면 `__manual-check` / “데이터 연결 예정” 또는 제거.

---

## 10. Figma·API 반영 제안 (작은 범위)

### Dashboard Aggregate 확장 (기존 `GET /api/admin/dashboard`)

```json
{
  "summary": { "netSales": 0, "orderCount": 0, "averageOrderValue": null, "activeOrderCount": 0 },
  "orderStatusCounts": { "received": 0, "preparing": 0, "completed": 0 },
  "orderTypeShare": { "eatInCount": 0, "takeOutCount": 0, "eatInAmount": 0, "takeOutAmount": 0 },
  "hourlyToday": [{ "hour": 11, "orderCount": 0, "salesAmount": 0 }],
  "categorySalesToday": [{ "categoryCode": "SALAD", "salesAmount": 0, "quantity": 0 }],
  "paymentMethodShare": [{ "paymentMethodCode": "CARD", "count": 0, "amount": 0 }],
  "opsSignals": {
    "maxReceivedWaitMinutes": 0,
    "avgHandleMinutesToday": null
  },
  "popularMenus": [],
  "soldOutSummary": {},
  "optionInsights": { "topOptions": [], "topExclusions": [] },
  "alerts": [],
  "recentOrders": [],
  "generatedAt": "..."
}
```

### Figma (06-C) 배치 가이드

1. 상단 KPI 4 유지.  
2. 2열: 왼쪽 실시간(상태·최근·대기 신호) / 오른쪽 성과(인기·유형·카테고리·수단).  
3. 하단: 시간대 미니 + 알림.  
4. 각 위젯 Loading / Empty / Error **개별**.  
5. 새 Component Set 남발 금지 — `SalesMetricCard`·리스트·미니바는 04-C 확장.

### 구현 우선순위 (추천)

```text
P0  Bible 기본 위젯 + 품절 요약 + 최근 주문
P1  A1 유형 비율 · A2 시간대 · A5 대기 신호 · 알림
P2  A3 카테고리 · A4 결제수단 · A6 처리시간
P3  A8 옵션/제외 · 메뉴 화면 힌트 · 품절×인기 교차
```

---

## 11. UX 카피 톤 (짧게)

- “오늘 포장이 62%예요. 포장 용기를 먼저 확인해 주세요.”  
- “대기 최장 8분 · 접수 4건”  
- “인기 2위 메뉴가 품절입니다.”  
- 데이터 없을 때: “아직 오늘 주문이 없어요.” (비난 금지)

---

## 12. Claude 검증 노트 (2026-07-17 추가)

- **DB 스키마 실현 가능성: 확인됨.** `asak-data/schema-backups`를 직접 열어 `orders.created_at`, `orders.order_type_id`(FK→`common_code`), `payment.method_id`(FK→`common_code`), `category` 테이블을 확인했다. A1(유형 비율), A2(시간대), A3(카테고리별), A4(결제수단별) 전부 스키마상 계산 가능한 값이다 — 이 문서의 전제는 DB 설계와 어긋나지 않는다.
- **단, "이미 모을 수 있다"의 의미는 정정이 필요하다.** `ASAK-back`은 `HealthController` 하나뿐이고 Menu/Order/Payment/SoldOut Controller·Service가 전부 없다(Part C §11-1에서 재확인). 즉 이 문서의 원천 데이터는 "DB 컬럼은 존재하나 이를 집계해 내려주는 API 코드는 아직 0%"인 상태다. §10의 Dashboard Aggregate JSON은 지금 당장 붙일 수 있는 기존 엔드포인트 확장이 아니라, **Backend 구현이 시작될 때 함께 설계해야 할 목표 계약**으로 다시 읽어야 한다.
- **Dashboard 라우트 자체가 아직 없다.** `ASAK-Admin/src/apps/AdminApp.jsx`를 직접 읽은 결과, 실제 라우트는 `/`(주문 현황=SCR-009 라벨), `/sold-out`, `/menus`, `/payment-methods`, `/sales` 5개뿐이며 **SCR-022 Dashboard 라우트가 아예 없다.** 이 문서의 §2(Dashboard KPI 아래 위젯) 작업을 시작하려면, 그 전에 "AdminApp.jsx에 `/` 경로를 실제 Dashboard로 연결(현재 `/`가 차지하고 있는 '주문 현황'은 `/orders/live` 등으로 분리)"하는 라우팅 작업이 선행돼야 한다. 이 순서를 Part C Wave 3에 추가해뒀다.
- **결론적으로 이 문서의 위젯 설계·우선순위(P0~P3)는 그대로 유효**하다 — 다만 실행 순서상 "Backend 메뉴/주문/결제/품절 API 구현"과 "Admin Dashboard 라우트 신설"이라는 두 개의 선행 작업이 있다는 것만 함께 인지하면 된다.

---

## 13. 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-07-17 | 수집 가능 데이터만으로 Admin 추가 섹션·알림·API 확장안 정리 |
| 2026-07-17 (추가) | Claude가 DB 스키마·ASAK-back·ASAK-Admin 라우팅을 직접 재검증. 데이터 실현 가능성은 확인, "이미 모을 수 있다"는 표현은 백엔드 미착수 상태 감안해 정정, Dashboard 라우트 부재라는 선행 조건 추가 |

---

*KPI를 늘리지 않고, 같은 주문 데이터로 “지금 뭐 하지?”를 더 빨리 보게 하는 것이 목표다.*

---

## 통합 이력 (문서 병합)

| 날짜 | 내용 |
|---|---|
| 2026-07-17 | Cursor 실측 PNG 분석 + Claude 코드 재검증 + Admin 인사이트 제안을 각각 담은 4개 문서(`ASAK_FIGMA_VISUAL_RECOVERY_FULL_AUDIT.md`, `ASAK_COMPONENT_CANONICAL_INVENTORY.md`, `ASAK_FLOW_POLICY_IMPLEMENTATION_GAP.md`, `ASAK_ADMIN_INSIGHT_SECTIONS.md`)를 작성 |
| 2026-07-17 (병합) | 4개 문서를 이 파일(`ASAK_FIGMA_INTEGRATED_AUDIT.md`) 하나로 통합. Part A~D로 구성하고 문서 간 상호 참조를 Part 표기로 교체. 원본 4개 파일은 `ASAK/docs/design/`와 `C:\ASAK-workspace\figma` 양쪽에서 삭제 |

각 Part 안에 남아있는 개별 변경 이력(Part A 말미, Part B 말미, Part C 말미, Part D 말미)은 병합 이전 각 문서의 작성 히스토리이므로 그대로 보존한다.
