> Status: **Historical** (2026-07-20)  
> → **정본:** [figma-qa-unified-complete-2026-07-17.md](../figma-qa-unified-complete-2026-07-17.md) (통합됨)

# ASAK Figma 디자인 피드백 — 컴포넌트·스크린 전수 재실측 (v2, 처음부터 재작성)

**작성일**: 2026-07-17 (v2 — 기존 문서 전면 폐기 후 처음부터 재실측)
**파일**: `JSrjOy668zhfkiLplCkreh` (ASAK — Design System · Product UI 0715)
**측정 페이지**: Foundations(148:12745) · Shared(145:2) · Kiosk(150:2) · Admin(150:2860) · Kiosk Screens(134:7720) · Admin Screens(134:10606)
**방법**: Figma Plugin API 읽기 전용 실측(get_metadata/get_design_context/get_screenshot/get_variable_defs), 쓰기 0회. 6개 독립 조사(병렬) 결과를 통합.
**원칙**: "~한 느낌" 금지, 항상 실측값 → Foundations 기준 비교 → 이탈 여부 → 권장값 순으로 기술.

---

## 0. 읽는 법 · 환경 전제

### 0.1 두 제품의 물리 환경이 다름

| | 키오스크 | 관리자 |
|---|---|---|
| 대표 프레임 | **1080×1920**(세로) | **1920×1080**(가로) |
| 입력 | 손가락 터치 | 마우스·트랙패드(+태블릿 보조 터치) |
| 시청 거리 | 팔 길이, 서서 조작 | 책상 앞 40~70cm |
| 최소 터치/클릭 | **48×48 필수**, 반복 핵심 조작 56~64 권장 | 클릭 32~40 가능, 태블릿 보조 시 44+ 권장 |
| 본문 최소 글자 | **16px 이상** 권장 | 13~14px 본문 가능, 11~12px는 caption/badge만, **9px 이하 금지** |
| 밀도 | 여유 우선(터치 실수 방지) | 정보 밀도 높여도 됨 |

### 0.2 판정 표기
**P0** = 즉시 수정 필요(기능 오류·데이터 오류·정책 정면 위반·재발 이력), **P1** = 계획적 수정 권고, **P2** = 참고/저위험.

---

## 1. Foundations — 디자인 토큰 실측 (148:12745)

이 섹션이 이하 모든 컴포넌트·화면 QA의 채점 기준선이다.

### 1.1 색상 — Primitive

| 그룹 | 단계 | Hex |
|---|---|---|
| Green(Brand Primary) | 50/100/200/300/400/500/600/700 | #F5FBE0 / #E2FF99 / #C8F064 / #B5E30F / #9CC600 / #6C9700 / #5B8C2A / #243300 |
| Lime(Accent) | 300/400/500 | #C5FF00 / #B7FF00 / #B3E500 |
| Neutral·CoolGray(혼재) | 50~950 | 50 #F3F4F6(CG) · 100 #F5F5F5 · 200 #E5E7EB(CG) · 300 #D4D4D4 · 400 #9CA3AF(CG) · 500 #888888 · 600 #737373 · 700 #6B7280(CG) · 800 #404040 · 900 #212121 · 950 #111827(CG) |
| Surface(Kiosk Dark) | 50~700 | #383D42 / #33383D / #292D30 / #26292B / #1F2429 / #1A1C1A / #1A1A1A / #0D0D0D |
| Red(Error) | 50/300/400/500 | #FFF0EB / #FF4D4D / #EF4444 / #CC331A |
| Yellow | 50/400 | #FFFBEB / #FBBF24 |
| Blue | 400/500 | #60A5FA / #3B82F6 |
| Success | 50/500/600 | #EBF5EB / #5DA45D / #338033 |
| Purple(Category) | 50/500 | #EEE8FC / #6D3FC4 |
| Absolute | White/Black | #FFFFFF / #000000 |

**정책**: Color는 Paint Style이 아니라 Variable만 사용, Screen은 Semantic만(Primitive 직접 금지). Purple은 `Semantic/Category/Dressing` 전용 — 다른 용도로 쓰면 정책 위반.

**Known TODO(파일 자체에 이미 기록)**: Neutral Pure Gray ↔ CoolGray 혼재 미해결 / Focus Ring이 Green/300 @50% 하드코딩(HC 모드 미대응) / Border Width HC 모드 미변수화 / **컴포넌트·화면 텍스트가 아직 Noto Sans KR — Pretendard Variable Text Style 미적용 다수**.

> **⚠️ 이번 QA에서 새로 확인된 메타 결함**: `get_variable_defs`로 실제 파일을 조회한 결과, **Variable 이름의 스텝 번호가 이 표(문서)와 실제 파일에서 서로 어긋난다.** 예: 문서 Green/300=#B5E30F인데 실제 파일 `Green/300`=#E2FF99(문서상 100), `Green/500`=#D1FF33(문서에 없는 값), `Green/700`=#B7FF00(문서상 Lime/400과 동일 hex). 아래 각 섹션의 "토큰 이탈" 판정은 **hex 실측값 기준**으로 수행했고, 스텝 번호 불일치는 별도 표시했다. Foundations 문서 자체의 정합성 재검증이 필요하다.

### 1.2 Typography Scale (Pretendard Variable)

| Style | Size/LH | Weight | LS |
|---|---|---|---|
| Display/XL | 64/76 | Bold | −2% |
| Display/L | 48/58 | Bold | −1.5% |
| Heading/1 | 36/44 | Bold | −1% |
| Heading/2 | 28/36 | Bold | −0.5% |
| Heading/3 | 22/28 | Bold | 0 |
| Body/L | 20/28 | Regular | 0 |
| Body/M | 16/24 | Regular | 0 |
| Body/S | 14/20 | Regular | 0 |
| Label/L | 20/24 | Medium | 0 |
| Label/M | 16/20 | Medium | 0 |
| Label/S | 12/16 | Medium | 0 |
| Number/XL | 48/56 | Bold | −1% |
| Number/L | 34/40 | Bold | −0.5% |
| Number/M | 26/32 | Bold | 0 |

### 1.3 Spacing / Radius / Touch / Border / Icon / Effect

- **Spacing**: 2·4·6·8·10·12·16·20·24·28·32·40·48·60·80(px)
- **Radius**: 4·8·12·16·20·24·32·Full(px)
- **Touch Target**: Min 48px · Comfortable 48px · Large 56px (공식 최소 48×48. 프로젝트 확정 기준: 일반 56px 권장, 반복 핵심 조작 64px 권장 — 권장사항이지 필수 FAIL 기준 아님)
- **Border**: Thin 1 · Medium 1.5 · Thick 2 · Heavy 3(px)
- **Icon**: SM16·MD20·LG24·XL32·XXL48(px)
- **Effect**: Shadow/Subtle(일반 카드) · Shadow/Floating(Modal/Popover) · Focus Ring
- **사용 규칙**: Semantic만 화면 사용 / Color Paint Style 금지 / 상태는 색상만으로 구분 금지(텍스트·아이콘·패턴 병용 필수) / 최소 터치 48×48

---

## 2. Shared 컴포넌트 — 🧩 02-C. Components / Shared (145:2)

대상: 11개 활성 컴포넌트(Modal, ConfirmDialog, Toast, EmptyState, ErrorState, LoadingState, AllergenTag, AllergenNotice, Icon×3) + Deprecated 5종. 키오스크·관리자 **공용**.

### 2.1 Shared/Modal (158:23908) — 대표 type=paymentError(158:23886)

| 항목 | 실측값 | 판정 |
|---|---|---|
| Padding | 32px 전방향 | 준수(Spacing) |
| Gap | 16px | 준수 |
| Radius | 16px | 준수 |
| Width | 480px 고정 | 정보 |
| Shadow | ASAK/Shadow/Floating(2겹) | Modal=Floating 규칙 준수 |
| 제목 | 22/28 Bold, `Semantic/BG/Page`(#0d0d0d) | 크기=Heading/3 일치. **텍스트에 "BG" 토큰 사용 — 네이밍 오용** |
| 본문 | 16/24 Regular, `Color/Neutral/600`(#737373) | 크기=Body/M 일치. **Primitive 직접 사용 — 정책 위반** |
| 버튼 padding | px24/py14 | 24 준수, **14 비체계**(14+lh20+14=48px 터치 최소값 정합 목적 추정) |
| 보조버튼 | bg `Color/Neutral/100`, text `Color/Neutral/800` | **Primitive 2건 위반** |
| 주버튼 | bg `Semantic/Brand/Primary`(#b5e30f), text `Semantic/BG/Page`(#0d0d0d) | Semantic OK, 네이밍만 오용 |
| 버튼 높이 | 48px | Touch Min 정확히 충족 |

색상 활용도: Primitive 직접 사용 다건, Purple/Blue 없음(양호). 글자 크기: 22/16 스케일 정확 일치, 임의값 없음. 여백: 32/16/24 준수, py-14만 예외(전 Shared 공통 패턴). 행간: 전부 명시, AUTO 없음. 트렌드: 2겹 그림자는 Effect Style 관리라 남발 아님. AI스럽지 않음: Purple/Blue·새 hex 없음 양호, 다만 "BG" 토큰의 텍스트 오용은 복붙 흔적. 구현: Primitive를 그대로 CSS화하지 말 것. 디바이스: 본문 16px는 Kiosk 기준 정확 충족하나 고위험 알림(결제오류 등) 버튼이 딱 48px(최소)뿐 — Kiosk는 Comfortable(56)+ 권장.

### 2.2 Shared/ConfirmDialog (158:23975, 12 variants) — 대표 deleteCartItem·danger·loading + discardChanges·warning·default

| 항목 | 실측값 | 판정 |
|---|---|---|
| Padding/Gap/Radius | 32/20/16 | 준수 |
| Width | 440px 고정 | 정보 |
| 아이콘 | 48px | Icon XXL 준수 |
| 제목 | 16/20 Medium, `Color/Surface/600`(#1a1a1a) | 크기=Label/M 일치. **Kiosk Dark용 Primitive를 라이트 텍스트로 오용** |
| 설명 | 14/20 Regular, `Semantic/Text/Tertiary` | Semantic 정상 |
| 버튼 | px28/py14(비체계) | 보조버튼 `Color/Neutral/*` Primitive 위반 |
| 주버튼(danger) | `Semantic/Status/Error`(#ef4444) | 준수 |
| **tone=warning 주버튼** | `Semantic/Brand/Primary`(#b5e30f) — Modal 확인버튼과 동일색 | **경고 전용색 부재, 위험도 구분 불가** |
| loading | opacity 0.4만 적용, 스피너/텍스트 없음 | "색상만으로 상태 구분 금지" 위반 소지 |

`get_variable_defs` 확정: `Color/CoolGray/400,200`, `Color/Surface/600`, `Color/Neutral/800,100` 등 **Primitive-tier 변수가 실제 바인딩**되어 있음(하드코딩이 아니라 "잘못된 티어 바인딩").

**데이터 이례**: discardChanges 기본 주버튼 텍스트가 코드상 `Semantic/BG/Admin`(흰색 fallback)로 표기되나 스크린샷 렌더는 어두운 텍스트 — 라임 배경+흰 텍스트라면 대비 1.3:1 심각 실패지만 실렌더는 다름(MCP 코드추출-실렌더 불일치, **P0 후보·미확정, Figma 직접 재확인 필요**).

구현: `tone`(danger|warning)과 `type`(비즈니스 식별자) prop 분리, loading은 opacity 외 disabled+시각 스피너 추가. 디바이스: 설명 14px는 Kiosk 최소(16px) 미달 — "취소할 수 없습니다" 류 경고 문구가 14px인 것은 위험. 버튼도 48px뿐 — 장바구니 삭제/결제수단 비활성화 등 고위험 확인은 56px+ 권장.

### 2.3 Shared/Toast (158:24049, 10 variants) — 대표 tone=error·longMessage

| 항목 | 실측값 | 판정 |
|---|---|---|
| 높이 | 76px(10개 variant 전부 동일) | 정보 |
| **너비** | **299.4px**(default·longMessage 동일) | **문서 스펙(longMessage=420 고정, default=hug)과 실측 불일치 — P0** |
| Padding | px16/py14 | 16 준수, 14 비체계 |
| Gap | 10px | 준수 |
| Radius | 12px | 준수 |
| Shadow | Subtle(단일) | Toast 자체는 미분류(Modal급으로 Floating이 더 적절할 수 있음) |
| 아이콘 | 24px | 준수 |
| 제목/메시지 | 14/20, 12/16 | Body/S, Label/S 정확 일치 |
| 텍스트색 | `Semantic/Text/Inverse`(#292d30) | 티어 OK, "Inverse"인데 라이트 배경 기본텍스트로 사용(네이밍 오용) |
| 닫기(✕) | 텍스트 글리프, padding14 전방향 | **가로 히트박스 ~42px로 48px 미달 추정** |

`get_variable_defs`: `Semantic/Text/Inverse,Secondary`, `Color/White`, `Semantic/Status/Error,Warning` — Shared 중 정책 준수도 가장 높음.

구현: Toast 너비는 **문서 스펙 기준**으로 구현(Figma 인스턴스 값 무시). 닫기 버튼 히트박스 48×48 별도 확보. 디바이스: 메시지 12px(Label/S)는 Kiosk 최소치 크게 미달, 닫기 좁은 히트박스는 Kiosk 터치에 취약(Admin은 문제없음).

### 2.4 Shared/EmptyState (158:24093, 7 types) — 대표 type=cart

| 항목 | 실측값 | 판정 |
|---|---|---|
| Padding/Gap | 32/40, 16 | 준수 |
| Width | 400px | 정보 |
| **아이콘** | **64px** | **Icon Scale 최대(XXL 48) 초과 — 미정의 크기** |
| 제목/설명 | 16/20, 14/20, `Color/Neutral/900,500` | 크기 일치, **Primitive 위반 2건** |
| **액션버튼 테두리** | **`border-[#ccc]`** | **변수 자체가 없는 raw hex — 최고 심각도** |
| 버튼 텍스트 | `Color/Neutral/800` | Primitive 위반 |

**P0**: Shared 전체에서 정책 위반 밀도 최고(5개 색상 중 4개 Primitive, 1개 raw hex). 레이아웃은 `showAction` prop으로 216h(버튼無)/280h(버튼有) 합리적 분기. 구현: `#ccc`는 즉시 Semantic Border 토큰으로 교체, 아이콘 64px는 ErrorState(48px)와 통일 검토. 디바이스: 설명 14px는 Kiosk 미달("장바구니가 비었습니다" 등 자주 노출되는 문구).

### 2.5 Shared/ErrorState (158:24161, 7) — 대표 type=load·layout=page

| 항목 | 실측값 | 판정 |
|---|---|---|
| Padding/Gap | 32/16 | 준수 |
| Width | 480px | 정보 |
| 아이콘 | 48px | 준수(EmptyState와 대조적으로 스케일 내) |
| 제목 | 16/20, `Color/Surface/600` | **Primitive+Surface 팔레트 오용(ConfirmDialog와 동일 패턴)** |
| 설명 | 14/20, `Color/Neutral/500` | Primitive 위반 |
| 버튼 | bg Semantic 준수, 텍스트 `Color/Surface/600` | Primitive 재사용 |

`Color/Surface/600`이 제목·버튼텍스트에 반복(ConfirmDialog와 합쳐 **Shared 전체 4회 확인**된 동일 오용 패턴). type×layout 유효조합 문서화 양호(load 3/save 2/payment 1/notFound 1=7/12). 구현: EmptyState와 공통 `StatePanel` 베이스 통합 검토. 디바이스: 설명 14px Kiosk 미달, 버튼 48px뿐 — "다시 시도"류 반복조작은 56px 권장.

### 2.6 Shared/LoadingState (158:24192, 4) — 대표 type=table

| 항목 | 실측값 | 판정 |
|---|---|---|
| Padding/gap | py16, row8, cell16 | 준수 |
| Radius | 4px | 준수 |
| **1행 셀 색** | `Color/CoolGray/200`(#e5e7eb) | Primitive |
| **2~4행 셀 색** | `Color/Neutral/100`(#f5f5f5) | Primitive, **1행과 다른 회색 계열** |

`get_variable_defs` 확정: 두 색 동시 바인딩 확인. **P0**: 단일 컴포넌트 안에서 CoolGray/PureGray가 행마다 혼용 — Foundations Known TODO가 실제 컴포넌트에 구체화된 재현 가능 사례, 육안으로도 미세하게 색이 튐. 여백은 Shared 중 정책 준수도 최고. 구현: 단일 Semantic 스켈레톤 토큰으로 통일.

### 2.7 AllergenTag(158:24215) / AllergenNotice(158:24225)

| 항목 | Tag(warning) | Notice(hasAllergen) |
|---|---|---|
| Padding/Radius | 12/6, 4px | 16, gap8, 8px |
| 배경 | `Semantic/Status/WarningBG`(#fffbeb) | 동일 |
| 텍스트 | 14/20, `Semantic/Status/Warning`(#fbbf24) | 제목 14/20 동일색, 설명 12/16 `Color/Neutral/500`(Primitive) |

**P0(접근성)**: `#FBBF24` 텍스트 on `#FFFBEB` 배경 — 대비비 약 1.5~1.7:1 추정(WCAG AA 4.5:1 크게 미달), 스크린샷에서도 육안으로 흐릿함 확인. **개별 실수가 아니라 Semantic Warning 토큰 자체의 설계 결함**(Tag·Notice 2개 컴포넌트에서 동일 재현). 알레르기 경고라는 안전 직결 정보의 가독성이 Shared 중 최악. 설명문은 Label/S(12px)까지 내려가 Kiosk 기준 대비 "저대비+최소폰트" 이중 위험. 구현: WarningText 전용 토큰(예 amber-700 #92400E) 신설 후 두 컴포넌트 동시 교체(FE 임의 수정 금지, 디자인 토큰 레벨에서 해결).

### 2.8 Shared/Icon (CaretLeft/Right, Placeholder) 및 Deprecated 5종

Icon 32×32px(Icon XL 준수), placeholder bg `#e6e6e6` 하드코딩(실사용 노출 색 아님, 집계만). Deprecated 5종(Modal-Confirm/Duplicate, ConfirmDialog-Legacy, Admin-EmptyState/ErrorState) 전부 "사용 금지" 안내문 보유 — 라벨링 요건 충족, 상세 QA 생략.

### 2.9 Shared 종합

**색상 이슈**

| 이슈 | 해당 | 근거 | 심각도 |
|---|---|---|---|
| Primitive 직접 바인딩 | Modal/ConfirmDialog/EmptyState/ErrorState/LoadingState 거의 전부 | get_variable_defs 확정 | **P0(전반)** |
| 변수조차 없는 hex | EmptyState 버튼 테두리(#ccc), Icon placeholder(#e6e6e6) | var() 자체 없음 | **P0** |
| Kiosk Dark Surface색을 라이트 텍스트로 오용 | ConfirmDialog×2, ErrorState×2 = 4회 | `Color/Surface/600` 재사용 확정 | **P0(반복)** |
| Neutral 혼용(단일 컴포넌트 내) | LoadingState/table | CoolGray/200 vs Neutral/100 동시 바인딩 | **P0(재현가능)** |
| 경고 토큰 저대비 | AllergenTag/Notice | #FBBF24 on #FFFBEB ≈1.5~1.7:1 | **P0(접근성)** |
| Toast 스펙-실측 불일치 | Toast | 문서 420 고정 vs 실측 299.4 동일 | **P0** |
| warning 전용색 부재 | ConfirmDialog | Brand Primary 재사용 | P1 |
| Purple/Blue 오용 | 없음 | 전 컴포넌트 미검출 | 양호 |

**폰트**: 실측(22/16/14/12) 전부 스케일 정확 일치, 임의값 없음(양호). 폰트패밀리 Pretendard Variable 확인(Foundations Noto Sans KR TODO는 이 페이지에선 해소). **Kiosk 관점 핵심**: Body/S(14px)가 광범위 사용 → Kiosk 최소 16px 미달, Admin은 문제없음. AllergenNotice 설명 12px는 Shared 중 최소.

**여백**: 대부분 스케일 준수. **py-14가 5개 컴포넌트(Modal/ConfirmDialog/ErrorState/EmptyState/Toast)에서 반복** — 48px 터치 목표를 위한 의도적 값으로 추정, Foundations에 `button/padding/y=14` 공식 등재 권장.

**행간**: 전부 명시, AUTO 없음(양호). **트렌드/AI스러움**: Purple/Blue·과도한 글로우·화면별 새hex 등 전형적 AI 안티패턴 미관찰. 다만 하드코딩 2건, 스펙-실측 불일치, 컴포넌트 내 색 혼용은 "토큰 시스템은 만들고 적용은 급하게 마감"한 흔적.

**디바이스 종합**: Kiosk는 14px 이하 텍스트가 여러 핵심 컴포넌트 설명에 광범위(16px 기준 미달), 버튼류가 딱 48px(최소)뿐이라 고위험 액션엔 56~64 권장. Admin은 대부분 문제없음.

---

## 3. Kiosk 컴포넌트 — 🖥️03-C. Components / Kiosk (150:2)

측정 완료 19/21(Deprecated/menu-card, AllergyAccordion collapsed는 Figma 호출 한도로 미확인).

### 3.1 Kiosk/PaymentMethodCard (150:3, 24 variants)

| 항목 | size=L | size=S |
|---|---|---|
| 크기 | 920×240 | 440×115 |
| padding | 40 | 40(내부 gap 32) |
| radius | 24 | 24 |
| **border** | **4px**(selected=true `#B5E30F` / false `#E5E7EB`) | 동일 |
| 타이틀/서브 | 36 Bold / 24 Regular | 24 Bold / 18 Medium lh28 |
| fill(selected=none) | `interactive/disabled #33383D` opacity50%+내부40% **이중 중첩** | — |

Green만 사용(PASS). border 4px는 Border Scale 최대(Heavy 3px) **초과 — 스케일 밖**(권장 3px 통일). 터치: L/S 모두 PASS(과잉충족). 구현: selected 무관 항상 4px 고정인 점 재검토. 디바이스: size=S(Admin용 결제 설정 사이즈)가 Kiosk 컴포넌트 페이지에 variant로 혼재.

### 3.2 Kiosk/OrderDetailList (150:165)

카테고리 헤더 26px(스케일 밖, Heading/2 28 근접), "필수" 배지 `#FF4D4D`(Red/300 정확 일치, OK), divider `#E8E8E8`(Foundations에 없는 값, CoolGray/200 #E5E7EB 권장). 3열 그리드 gap 12(4배수, PASS). "빼기" 텍스트 버튼이 버튼 크롬 없이 텍스트만 존재 — hit-area 확장 필요. 구현: 옵션 레이블-값 사이 `gap-[700px]` 매직넘버 발견 — `justify-between`으로 대체 권장(반응형 붕괴 위험).

### 3.3 Kiosk/QuantityStepper (150:166, 5 states)

**터치 64×64px 전 상태 동일 — PASS, 우수 사례.** plus 버튼 실제 Green(#B5E30F)인데 **컴포넌트 문서엔 "파란색"으로 오기재**(구현 자체는 문제없음, 문서 정정 필요). pressed 상태 `border-black` 하드코딩(정책 위반). 수량텍스트 18px(PASS). 구현: limitReached(menu/cart) 2상태 시각 동일 — Toast 메시지만 분기 권장.

### 3.4 Kiosk/OrderSummaryInfo (150:182, 2)

접힘 920×114 / 펼침 920×329. 타이틀 30, 항목 28, 옵션 24px — **Typography Scale 정확 일치값 전무**(스케일 이탈 다수). 항목 구분선 `brand/subtle #F5FBE0` 1.5px h — 거의 안 보일 정도 저대비. border도 `#F5F5F5`로 흰 배경과 대비 거의 없음. 행간 대부분 AUTO.

### 3.5 Kiosk/OrderDetailRow (150:247, 7 states) — Legacy, P0

| state | bg | border | 텍스트 |
|---|---|---|---|
| default/pressed/error/disabled/minusDefault(5종) | `gray/300 #ccc` 등 legacy 넘버링 | 동일 계열 | 동일 |
| selected(1종만) | `semantic/brand/subtle #f5fbe0` | `semantic/brand/primary #b5e30f` | 정식 Semantic |

**P0**: 7 state 중 **6개가 Foundations에 전혀 없는 legacy 팔레트**(`gray/300~1600`, `green/100,1000`, `red/100,500,900` — 표에 없는 hex 다수, 예 #f9ffe6, #80b200, #8c8c8c). selected 1개만 정식 Semantic — **같은 컴포넌트 안에서 토큰 체계 절반씩 혼재**. kcal/단백질 라벨 **전 상태 공통 12px**(16px 미만). 컴포넌트 자체 설명에 "05-C 적용 시 QuantityStepper로 교체 검토, minusActive/minusDefault 제거 권장"이라고 **자체적으로 Legacy 선언**되어 있음. 터치는 행 자체 92px/68px PASS.

### 3.6 Kiosk/StepIndicator (150:359, 5)

pill 채움 `green/800 #b3e500` — hex는 Lime/500과 일치하나 **변수명이 Green 네임스페이스로 오기재**. gap 76px(Spacing Scale 80과 근접 이탈). 비인터랙티브(터치 N/A).

### 3.7 Kiosk/BottomCTA (150:385, 9 variants) — 매우 중요, P0

| variant | 버튼높이 | 폰트 |
|---|---|---|
| twoCTA default | 100(컨테이너180) | 34 Bold |
| cartSummary default | 100 | 금액38 Bold/라벨22 |
| twoCTA loading | 100 | **라벨 15px SemiBold — 16px 미만** |
| singlePrimary disabled | 100, opacity-50 | 34 Bold, `#d4d4d4`(Neutral/300 일치 OK) |

색상: primary `#B5E30F`, disabled텍스트 `#6B7280` 모두 Semantic 정상, Blue/Purple 없음. **터치: 버튼폭 최소~500px — 매우 넉넉함(PASS).**

**P0**: 컴포넌트 설명 문서에 **"Disabled 상태는 opacity 50%가 아닌 정식 Variant"**라고 명시했으나 실제 노드는 **`opacity-50` 클래스가 그대로 적용**되고 그 위에 별도 disabled색까지 이중 적용 — **문서와 구현이 정반대로 모순**. React 구현 시 반드시 확정 필요(권장: opacity 제거, 정식 disabled색만).

### 3.8 Kiosk/Header (150:403/425:54752)

로고 200×68 중앙, 아이콘 60×60(PASS, 56px+ 충족). 좌우 여백 51/967(1080폭 거의 대칭). 히트박스 여유 확장 권장.

### 3.9 Kiosk/CartItemCard (150:404, 3 states) — Blue 재확인, P0

| state | 특이사항 |
|---|---|
| Default | 체크 아이콘 **파란색 원형 테두리**(스크린샷 육안 확인) |
| Disabled | SET 아이콘 보더 **`accents/blue,#08F` 하드코딩**(음료), 사이드=orange #FF8D28 |
| SoldOut | 수량 컨트롤 48×48로 축소(최소 기준 근접, 여유 없음) |

**P0**: `#0088FF`가 Foundations Blue(400/500) 어디와도 불일치하는 **새 blue** — 과거 지적된 "CartItemCard Blue" 문제가 **현재도 재현**, 카드 1개당 최소 2개 지점(체크 아이콘, SET-음료 아이콘). "옵션 수정"/"삭제" 버튼 라벨 **13px — 16px 미만**. Disabled/SoldOut 상태 수량 버튼 48×48(최소 기준 정확히 걸침, 여유 없음). 구현: `mix-blend-darken` CSS 블렌드 모드는 렌더링 편차 위험 — backgroundColor로 대체 권장.

### 3.10 Shared/CartFooterBar (150:655, 이 페이지 소속)

ready/empty/loading 3상태. QuantityStepper nested 64×64 PASS. 헤더 30px(경미한 스케일 이탈). 구현: "empty 상태 결제하기 클릭 시 Route 이동 금지 + aria-disabled 권장" 등 구체적 접근성 지침이 컴포넌트 설명에 존재 — 반드시 반영.

### 3.11 Kiosk/MenuCard (150:678, 2)

가격 `brand/secondary #6C9700`(Green/600 일치, OK). 이름30/가격38/kcal28px — 스케일 정확 일치값 없음. soldOut은 흑백오버레이+배지 병행(정책 준수, 색상 단독 아님).

### 3.12 Kiosk/CategoryTab (150:695, 3) — 정본

active 30px Bold(스케일 밖). 실측 높이 약 52~59px(PASS 추정). active 단독 재확인은 rate limit로 실패 — 흰텍스트가 밝은 배경에서 대비 실패할 가능성(P1, 미확정, 재확인 권장).

### 3.13 Kiosk/Category (150:700, 2) — P0: Admin 혼재

| page | 실측 |
|---|---|
| K(Kiosk) | 탭 높이 53~117, 32px |
| **A(Admin)** | **chip 높이 11px**, 14px, padding 없음 |

**P0**: page=A는 Admin 전용 필터 UI가 그대로 Kiosk 컴포넌트에 혼입된 것이 실측으로 확인. **터치 FAIL: 11px(48px 대비 23%)**. 별도 `Admin/CategoryFilter`로 분리 필요.

### 3.14 Kiosk/HomeActionButton (150:719, 2)

444×450 — 터치 PASS(매우 큼). 타이틀44/서브26px(스케일 밖이나 가독 문제 아님).

### 3.15 Kiosk/CategoryTap (150:737, 4) — P0: Deprecated 미정리

컴포넌트 자체 설명: *"⚠️ DEPRECATED — Kiosk/CategoryTab의 오타 변형, 정본은 CategoryTab"*. Size=s **높이 11px — 터치 FAIL(23%)**. **P0**: 자체 선언 Deprecated임에도 `Deprecated` 프레임이 아닌 정식 캔버스(150:2)에 다른 정식 컴포넌트와 나란히 최상위로 남아 실수 사용 위험.

### 3.16 Kiosk/MenuDetailSummary (160:1734, 5 states) — 최고 심각도 P0

| variant | 크기 | 폰트패밀리 | 색상 |
|---|---|---|---|
| default/optionSelected/quantityChanged/loading(4종) | 480×403 | Pretendard Variable | Semantic |
| **"MenuDetailSummary"**(389:44600) | **1080×320** | **Noto Sans KR** | **하드코딩 legacy**(red/100, yellow/400, gray/1600) |

optionSummary 텍스트 `semantic/status/info #3B82F6` — **Blue 재확인**(13px과 이중위반). "MenuDetailSummary" variant는 title36/price48로 나머지(price18)와 **3배 격차**. **레이아웃 자체가 별개 컴포넌트**(가로세로 비율 다름). QuantityStepper가 부모 h-48에 자식 size-64로 **오버플로우 버그**까지 존재.

**P0(본 QA 최고 심각도)**: variant명이 컴포넌트명과 동일한 `"state=MenuDetailSummary"`인 것 자체가 비정상 — legacy 화면 스냅샷이 실수로 variant 편입된 것으로 추정. 반드시 별도 분리 또는 삭제 필요.

### 3.17 Kiosk/OptionGroup (160:1764, 2)

타이틀16(PASS), 설명13·필수라벨12px(16px 미만). disabled 시 "필수" 라벨이 흐려지지 않고 그대로 유지(활성/비활성 시각 혼란 가능성 확인 필요).

### 3.18 Kiosk/OptionSelectionRow (160:1831, 15 variants) — 핵심, P0

행 min-h **80px**(터치 PASS), width432, indicator20×20. **옵션명 15px·가격14px·soldOut배지11px — 15개 variant 전수(single/multiple/exclude×5states) 동일하게 16px 미만.**

**P0**: "메뉴 상세 옵션 선택의 핵심" 컴포넌트인데 본문 폰트가 예외 없이 전수 위반. Green만 사용(PASS), soldOut은 배지+회색텍스트 병행(정책 준수), selected는 배경+indicator+굵기 3채널 구분(정책 준수 우수 사례).

### 3.19 Kiosk/AllergyAccordion (160:1852, 2) — expanded만 확인

전 요소(14/12/13/12px) **16px 미만**. 헤더 토글 높이 약 34px 추정 — **48px 미만 FAIL 의심(미확정)**, collapsed 미확인(rate limit). 안전정보임에도 최소 폰트군.

### 3.20 Kiosk/SoldOutBadge (311:1789, 3 sizes)

`status/error #EF4444` 배경(Semantic 정상). L사이즈 24px(PASS). 비인터랙티브(터치 N/A).

### 3.21 Kiosk 종합

**터치 타깃 FAIL(48px 미만, 확정)**

| 컴포넌트 | 측정값 | 판정 |
|---|---|---|
| CategoryTap, Size=s | 11px | **FAIL(23%)** |
| Category, page=A | 11px | **FAIL(23%)** |
| AllergyAccordion 헤더 | 약34px 추정 | FAIL 의심(재실측 필요) |

**P0 목록(6건)**: ① CartItemCard Blue 재발 ② MenuDetailSummary 이질적 legacy variant 혼입+Blue+오버플로우 버그 ③ OptionSelectionRow 15variant 전수 폰트 미달 ④ BottomCTA 문서-구현 opacity 모순 ⑤ Category Admin 혼재+터치FAIL ⑥ CategoryTap Deprecated 미정리+터치FAIL

**색상**: Blue 재발 2개 컴포넌트 3지점(CartItemCard 체크·SET음료, MenuDetailSummary optionSummary). Purple 미발견(OK). Green/Lime 대부분 정상이나 StepIndicator 변수명 오기재.

**폰트(16px 미만, 9개 컴포넌트)**: OrderDetailRow(kcal12), BottomCTA(loading라벨15), CartItemCard(버튼13), MenuDetailSummary(14/13/13/11), OptionGroup(13/12), OptionSelectionRow(15/14, 15개variant 전수), AllergyAccordion(12~14), Category page=A(14), CategoryTap size=s(14). → 21개 컴포넌트 중 9개가 체계적 문제 — Typography Scale 재검토(Body/S=14를 보조정보 전용 한정) 권장.

**Legacy 변수 잔존**: OrderDetailRow(gray/green/red 넘버링, 6/7 state), StepIndicator, BottomCTA, MenuDetailSummary legacy variant — Foundations 공식 Semantic과 무관한 구식 팔레트 다수 잔존. OrderDetailRow는 이관 작업이 절반만 진행된 상태로 추정.

**구현 우선순위**: ① MenuDetailSummary 분리 ② OptionSelectionRow 폰트 확대 ③ Blue 하드코딩 제거 ④ BottomCTA 모순 해소 ⑤ Category/CategoryTap 아키텍처 정리 ⑥ OrderDetailRow legacy→Semantic 전환 ⑦ 전사 16px 미만 재검토.

---

## 4. Admin 컴포넌트 — 🛠️ 04-C. Components / Admin (150:2860)

컴포넌트 50개 이상으로 Part A(Navigation+Data Display)/Part B(그 외)로 분할 조사.

### 4-A. Navigation + Data Display

> **선행 경고(메타 발견)**: Navbar를 `get_variable_defs`로 실측한 결과도 §1.1과 동일하게 **Variable 스텝 번호가 Foundations 문서와 어긋난다**(Green/500 실제값 #d1ff33 등). 아래 판정은 hex 실측 기준.

#### 4-A.1 Admin/Navbar (150:4739)

Desktop 240×1080(px20/pb28, 세로gap28, 항목간gap8). Active 메뉴 bg **`Green/500` Primitive 직접 바인딩**(#d1ff33, 정책 위반). 비활성 텍스트 `gray/800 #737373`(CoolGray가 아닌 **제3의 Gray 넘버링 체계** 사용). **Active 메뉴에 DROP_SHADOW×4 + INNER_SHADOW×4 = 총 8겹 중첩 섀도우**(Foundations "4중은 과함" 기준의 2배). Tablet 모델은 90px 아이콘 전용(라벨 없음 — 학습비용 우려).

**P1**: Primitive 직접사용 + 8겹 섀도우("Glass Effect 재검토 후보"라고 컴포넌트 스스로 경고 중).

#### 4-A.2 Admin/NavItem (150:5187, 3 states)

Default/Active/Sub = 41/41/36px, Active bg `semantic/brand/secondary #6c9700`(**Navbar의 #d1ff33과 다른 색** — 컴포넌트 재사용 불일치 의심, Navbar가 NavItem을 인스턴스로 물지 않고 직접 그린 것으로 추정). hover 상태 정의 없음. 클릭 타깃 전부 Admin 기준 충족.

#### 4-A.3 Admin/TopHeaderItem (150:5128, 3) — **P0**

**inactive(150:5129)와 Last(150:5132) 배경이 active(150:5134)와 동일한 `semantic/brand/primary #b5e30f` 라임 채움.** get_design_context 코드 확인 결과 상태 분기 이전에 배경이 무조건 적용되고, active는 그 위에 White Backing+Tint+Glass shadow만 추가되는 구조 — **3개 pill이 실제로 전부 라임으로 렌더링**(스크린샷 확인). **탭 활성 여부를 색만으로 구분 불가.**

active 레이어: White Backing(94%)+Tint+Glass shadow 4겹 스택 — 컴포넌트 설명에 이미 "Glass Effect Decorative, 06-C 재검토/제거 후보"로 자체 경고. 높이 48px(클릭 기준 충분).

> **⚠️ 화면 QA 후속 확인(§6)**: 실제 화면(Order Management)에서는 TopHeaderItem이 탭 그룹이 아니라 **단일 배지로만 1개 사용**되어 색 구분 실패의 실사용 임팩트는 낮음(P2로 하향 조정). 마스터 컴포넌트 결함 자체는 유효.

#### 4-A.4 Admin/DataTableRow(150:2906, 3) / DataTableRow-Active(150:4932, 4) / DataTableHeader(150:5005)

Row h48px 고정, default/hover/selected 전부 Semantic 바인딩 정상. Active 배지(접수/준비중/완료/취소) **텍스트가 상태별로 정확히 일치**(StatusBadge와 달리 정상). 단 "준비중" 배지 `#fbbf24` on `#fffbeb` — 저대비 가독성 우려. **DataTableHeader는 배경`#f8f9fa`·테두리`#e5e7eb`·텍스트`#6b7280`가 전부 var() 없는 raw hex — Part A 유일 완전 미바인딩**, 폰트도 Noto Sans KR. hover는 마우스 전용(태블릿 무의미).

#### 4-A.5 Admin/OrderCard (150:2956, 4 variants)

폰트분포 12/14/16/18/24/32px. "매장" 배지 bg `green/600 #ccff1a`(Foundations 표에 없는 미문서 hex), 시간배지 bg `gray/200 #e6e6e6`(CoolGray #E5E7EB와 미세 불일치). gap분포 4~16px 전부 스케일 준수, **의심했던 200px+ 비정상 gap은 미재현**(1열 off 기준 정상). **총액 표기**: 메뉴3개×12,800원인데 "총액 0원" 정적 플레이스홀더 — 합계 로직 부재.

#### 4-A.6 Admin/SalesMetricCard (150:2928, 10) — **P0 콘텐츠 결함**

240×120, padding20, radius12. **totalSales/orderCount/averageOrderValue 3개 지표의 `state=default`(정상 데이터 상태)가 실제 숫자 대신 "데이터 연결 예정" 문구를 디폴트로 가짐.** currentQueue만 "3건"으로 정상 포맷 — 일관성 붕괴. 구현자가 그대로 카피하면 실서비스에도 노출 위험.

> **⚠️ 화면 QA 후속 확인(§6)**: Admin Dashboard/Sales Summary/Monthly/Daily 4개 실제 화면은 **전부 실제 포맷 숫자 사용, 이 버그 재현 안 됨**(긍정적 대조 — 화면 구현 단계에서는 이미 정상 처리됨).

#### 4-A.7 Admin/StatusBadge (150:5064, 12 Role) — **P0, 라벨 버그**

| Role | fill/텍스트 | 실제 표시 문자 |
|---|---|---|
| 핵심 재료 | errorbg/error | "핵심 재료"(우연히 일치) |
| 베이스재료·일반기본·품절·판매중·기본·추천·필수·선택·토핑추가·드레싱선택·자동(11개) | Role별 정상 분기(success/subtle/warning/dressing 5그룹) | **전부 "핵심 재료"로 오표시** |

**12개 Role 중 11개(91.7%) 오표시.** 원인: `role`과 `label` prop 분리 구조에서 **배경/텍스트색은 Role별로 정확히 분기되나 텍스트 문자 오버라이드가 전부 "핵심 재료"로 방치** — "Property 바인딩처럼 보이나 실제로는 색상만 바인딩, 텍스트는 하드코딩"인 함정. Purple(#6d3fc4)은 "드레싱 선택" 1개 Role에만 사용되어 카테고리색 정책은 준수. 11px 폰트는 캡션 허용범위.

> **⚠️ 화면 QA 최종 확인(§6)**: 전체 72개 실제 관리자 화면을 전수 검색한 결과 **StatusBadge 인스턴스는 파일 전체에 단 1개(247:19761)뿐이고 그마저 화면 밖(y=-8) 고아 레이어로 렌더링 자체가 안 됨. 실사용 0건 — 마스터 결함은 유효하나 사용자 체감 위험은 없음(P0→실사용 P2로 하향).** 실제 화면들은 StatusBadge 대신 별도 raw div(category-tag 등)를 쓰며 그쪽은 텍스트가 정확함.

#### 4-A.8 Admin/DetailPanel (150:5418, 3)

460px, `ASAK/Shadow/Floating`(정책 정확 준수). 총액 "0원" 플레이스홀더(OrderCard와 동일 패턴), status3(환불)는 금액이 음수 표기(-12,800원)인데 강조색 없음. 액션버튼 36px(Admin 충족, 태블릿 44+엔 약간 미달).

#### 4-A.9 Admin/Pagination (150:5046)

32×32px 버튼 — **Admin 최소기준 하한선 정확히 걸침**, 태블릿 44+ 미달(반복 클릭 요소라 확대 권고). 활성 페이지 bg **`#c8f230` raw hex**(Green/200 #C8F064과 근접하나 다른 값) — DataTableHeader와 함께 **완전 미바인딩**.

### 4-A. Part A 종합

**P0(3)**: StatusBadge 91.7% 오표시(실사용 임팩트는 §6에서 낮음으로 재확인) / TopHeaderItem 색반전(§6에서 임팩트 낮음 재확인) / SalesMetricCard "데이터 연결 예정"(§6에서 화면엔 미재현 확인).
**P1**: Navbar Primitive+8겹섀도우 / DataTableHeader·Pagination 완전 미바인딩 / OrderCard·DetailPanel "0원" 플레이스홀더 / 폰트 스케일 이탈 다수(13,18,24,32px) / Neutral 3중 혼용(CoolGray/PureGray/제3넘버링) / DataTableRow-Active "준비중" 저대비.

---

### 4-B. Filters&Inputs / Analytics·Dashboard / Menu&Inventory / Actions&Saving / Empty&Modal / Deprecated

#### 4-B.1 Filters & Inputs

- **Admin/Checkbox(150:5409) — P0**: 18×18px, checked 상태가 **단색 사각형뿐 체크 아이콘(✓) 자체가 없음** — Foundations "색상만으로 상태 구분 금지" 정면 위반(색약/저채도 환경에서 체크 여부 구분 불가). 18px는 Admin 클릭기준(32~44)에 크게 미달.
- **Admin/SearchInput — P0(재확인)**: 마스터 심볼(425:54820) 기본폭 **150×39px**로 "주문번호 / 메뉴명 검색"(약11자) placeholder가 물리적으로 안 들어감. 실제 캔버스 인스턴스(280px)는 수동으로 늘려놔서 괜찮아 보이지만 **라이브러리에서 새로 꺼내면 깨진 150px을 받음**. 배경/테두리/텍스트 전부 raw hex, 폰트 Noto Sans KR.
- FilterDropdown 36~39px, 테두리색+화살표로 활성 표시(색상단독 아님, 양호). DatePicker 8종/day 9종 정상, 셀 40×36px(Admin 충족). Toggle 48×28(높이 28은 32px 기준에 약간 미달, 관례적 허용범위).
- **P1**: SalesPeriodFilter(검정 pill 강조)와 DateSelector(그린 pill 강조)가 같은 "현재 선택된 기간" 개념을 서로 다른 색으로 표현 — Admin 전역 "활성" 색상 언어 불일치의 첫 사례(§4-B.4 SaveBar에서 더 심각하게 반복).

#### 4-B.2 Analytics / Dashboard(13개, 대표 확인)

대부분 정상(AnalyticsMetricCard/BreakdownCard/DailySalesTrendChart 등). **P1**: PaymentPolicyCard "수정" 링크가 **Blue** 사용(액션 CTA로 Blue는 정책상 부적절). OrderStatusSummary/DashboardRecentOrdersPanel에 **Orange 반복**(대기=파랑, 조리중=주황, 완료=그린) — Foundations 0.1 색상표에 **Orange 계열 자체가 없음**, MenuButton(§4-B.3)의 `accents/orange`와 동일 계열 — 문서화 안 된 "accents/*" 팔레트가 Admin 전역에 암묵 사용 중.

#### 4-B.3 Menu & Inventory(11개)

- **Admin/MenuButton(150:2861) — P0**: 16×16px(Admin 최소 32px의 절반, OrderCard 내 반복 사용되는 핵심 수량조작 버튼). 4개 type 색상(`deep/green #5b8c2a`, `red/800 #e50004`, `accents/orange #ff8d28`, `accents/blue #08f`) **전부 Foundations 미등록** — Green/Lime/Neutral/Surface/Red/Yellow/Blue/Success/Purple 명명 규칙과 다른 제3의 팔레트.
- **Admin/IngredientTypeFilterChip(150:5336, 11 symbols) — P0**: (1) 7개 카테고리 중 **4개(전체/채소/단백질/드레싱)만 Selected 상태 존재**, 베이스/사이드/음료는 Selected 디자인 자체가 없음. (2) 드레싱만 정책대로 Category 토큰 사용, 나머지는 **status색(error/warning/info)을 카테고리 구분색으로 전용** — 단백질=에러레드, 사이드=워닝옐로, 음료=인포블루(실제 상태와 무관한 색 재사용, 혼동 소지). (3) **베이스와 채소가 완전 동일색**(successbg/success)으로 구분 불가. (4) 음료 Default만 tint 아닌 solid blue로 패턴 이질적. 13px 폰트(스케일 밖, Admin 전역 반복 관행).
- IngredientTableRow(150:5290) 592×64, semantic 토큰 정상 — Part B에서 가장 토큰화 잘 된 컴포넌트. IngredientCard Sold Out에서 **"핵심 재료" 배지 중복 렌더링**(P1, 버그 의심). SoldOutCard는 체크 아이콘(✓) 실제 존재(Checkbox와 대조적 — 파일 내 "선택됨" 표현이 컴포넌트마다 다름).

#### 4-B.4 Actions & Saving — SaveBar 3벌 불일치(핵심)

| 컴포넌트 | dirty 배경 | 저장버튼 | 비고 |
|---|---|---|---|
| **Admin/SaveBar**(150:5115) | **`#292d30`(하드코딩)** | `#b5e30f`(토큰) | saving 동일배경, success `#f5fbe0`, error `#fff0eb` |
| **Admin/StickyActionBar**(150:5289) | **흰 배경**+주황 경고텍스트 | 진초록 | SaveBar와 완전히 다른 색 언어 |
| **Admin/PaymentSaveBar Final Master**(638:20871) | **`#262626`(제3의 다크그레이, 하드코딩)** | **`#d1ff33`(제4의 라임, 하드코딩)** | **error 상태가 솔리드 레드 `#e53333`인데 문구는 dirty와 동일**(어떤 오류인지 정보 없음) |

**P0(사용자 이력 재현+확산)**: 같은 "저장 안 된 변경사항" 개념의 컴포넌트가 파일에 **최소 3벌**, 색상·토큰화 수준·error 의미까지 전부 다름. 다크톤 3종류 전부 불일치, 라임 버튼 2종류 불일치, PaymentSaveBar는 **일상적 미저장 상태에 순수 error 레드를 풀백그라운드로 사용**(과도한 경고, 기능적 결함).

> **⚠️ 화면 QA 재확인(§6)**: 실제 화면에서 **재현 확정**. Menu Management(Validation Error/Save Loading), Sold-out Management(Item Changed/Saving), Payment Methods(Default/Toggle Changed/Saving)에서 다크 바 노출 확인, Payment의 error는 솔리드 레드까지 실화면 재현. **추가로 Sold-out "Item Changed" 화면에서 다크 SaveBar + 흰색 StickyActionBar가 동시에 겹쳐 노출되는 신규 이중화 버그 발견**(§6.3 참조) — 마스터 단계 불일치가 화면 단계 UI 중복으로 실제 확산됨.

- Admin/ModalActionBar(2): green/red 스타일 각각 내부 일관성 있음(양호). Admin/SelectionSummaryBar(3): "품절 포함" 상태가 문구만 다르고 버튼색은 일반 Selected와 동일(P1, 반대방향 문제 — 색 차별화 없음). Admin/OrderActionButtons — **P0**: "영수증 출력" 버튼이 `green/700 #b7ff00`(Primitive)+`gray/1600 #0d0d0d`(미등록) 직접 사용, MenuButton과 함께 "문서화 안 된 제3의 팔레트" 3번째 사례. Admin/PaymentMethodSettingRow — 상태구분 정책 준수(색+opacity+라벨 병행) 양호하나 15px/13px 스케일 이탈.

#### 4-B.5 Empty&Modal / Sandbox / Final Master

IngredientSelectModal(720×800) 실제 화면 종합 확인 — 검색 실사용폭 592px로 문제없이 넓게 씀(SearchInput 마스터 150px 문제와 대비), 카테고리 필터칩 색상 재사용 문제(§4-B.3)가 그대로 나타남, 품절 안내문 텍스트 병행 양호, 닫기버튼 44×44(Admin 상한 충족). IngredientEditRow/OptionGroupSummary/OptionRuleRow Final Master 3종은 시간 예산상 크기만 확인(정밀 실측 후속 필요).

#### 4-B.6 Deprecated(7개, 1개 스크린샷 확인)

**P1**: Deprecated/Admin-ConfirmDialog 등은 **캔버스 상에 "사용 금지" 시각 표시가 전혀 없음**(레이어 이름에만 표기) — Kiosk의 CategoryTap과 동일한 유형의 리스크. DeleteConfirmDialog(400×10px)·EmptyState(500×10px) 심볼은 높이가 비정상적으로 눌려있어 콘텐츠 collapse 의심(후속 확인 필요).

### 4-B. Part B 종합

| 그룹 | 컴포넌트 수 | P0 | P1+ |
|---|---|---|---|
| Filters & Inputs | 8 | Checkbox 체크아이콘 부재, SearchInput 150px | SalesPeriodFilter/DateSelector 색 불일치 |
| Analytics/Dashboard | 13 | — | PaymentPolicyCard Blue, 미등록 Orange |
| Menu & Inventory | 11 | MenuButton 비표준색+16px타깃, FilterChip 3중결함 | IngredientCard 배지중복, 13px 반복 |
| Actions & Saving | 6 | **SaveBar 3벌 불일치**, OrderActionButtons Primitive | SelectionSummaryBar 무색상구분, 15/13px |
| Empty/Modal/Sandbox/FM | 8 | — | 3개 미실측 |
| Deprecated | 7 | — | 캔버스 표시부재, 크기이상값 |
| **합계** | **~53개** | **6건** | **8건+** |

---

## 5. 키오스크 화면 — 🛒 05-C. Screens / Kiosk (134:7720)

**규모**: top-level 프레임 73개 → 실제 UI 화면 **57개**, 제외(Annotation/스와치/ARCHIVED/PILOT) 16개. 육안 확인 17개 화면 + design_context 1건(Figma 호출 한도로 계획한 20~25개 중 일부만 확보).

**표준 크기(1080×1920) 이탈**: **0건**(57개 전부 프레임 레벨 정상).

### 5.1 홈·목록

SCR-001 Home: HomeActionButton 444×450 6개 인스턴스 완전 일관. SCR-003 Menu List: MenuCard 305×369 45개 인스턴스 완전 일관, 플레이스홀더 데이터("메뉴이름","0,000원") 잔존(실데이터 교체 필요). Empty/Loading/Error 3화면이 동일 아이콘·톤 패턴 재사용(시스템 일관성 우수). **Loading 화면에서 BottomCTA가 "결제하기" 활성 상태 유지** — 메뉴 로딩 중 총액 상태 불분명(P2).

### 5.2 메뉴 상세(15개 중 5개 육안 확인)

Default: OptionCard 292×128 수백 인스턴스 완전 일관. **Loading 화면은 CTA까지 스켈레톤 처리하는데 Menu List Loading은 CTA 그대로 유지** — 로딩 상태의 CTA 처리 정책이 화면마다 들쭉날쭉(판정기준 5 근거). Menu Sold-out: 옵션 선택 UI는 그대로 노출된 채 담기 버튼만 비활성 — 옵션까지 비활성화할지 정책 확인 필요.

### 5.3 카트(15개 중 4개 육안 확인)

Default: 카드별 요약가 8,400원×2=합계16,800원 **산술 정합**(priceCalculation 관점 양호). Empty: Menu List Empty와 아이콘·톤 동일(일관성 우수). Delete Confirm: 파괴적 액션에 Red 사용(정책 부합). Item Sold-out: 정상항목과 나란히 표시되어 부분품절 상태 명확 구분(우수 패턴).

### 5.4 결제·완료·타임아웃

- **Payment Declined**: 모달 내 "다시 시도" + 화면 하단 BottomCTA "다시 결제하기"가 **같은 기능을 이중 제공**(P1 후보, UX 중복).
- **Timeout Expired**: "시간 초과" 모달이 주문취소를 안내했음에도 **하단 BottomCTA "결제하기"가 여전히 활성 상태로 노출**(P1 후보, 상태 불일치).
- **SCR-008 Order Complete — P0(최우선)**: get_design_context 정밀 실측 결과 내부 `Kiosk/BottomCTA` 인스턴스(134:7967)가 **x=71,y=1740,width=940,height=200**(표준 x=0,y=1740,**1080×180**에서 폭−140/높이+20/좌측+71 이탈, **과거 지적과 정확히 동일한 결함값 재발**). **variant 자체가 singlePrimary가 아닌 `secondary-button`(흰배경+outline) 서브노드 단독 렌더링**, 텍스트도 34px Bold로 이례적으로 큼. 스크린샷상 "홈으로 돌아가기" 버튼이 화면 폭을 못 채우고 좌우 여백을 남긴 채 작게 표시 — 주문완료라는 플로우 최종 CTA의 시인성이 다른 모든 화면 대비 현저히 약함. **크기·variant·타이포 3중 override 결함.**

### 5.5 키오스크 화면 종합

**색상**: 육안 확인 범위(17개 화면+1건 정밀)에서 Foundations 밖 hex 미발견 — 단 **호출 한도로 40개 화면은 정밀 색상 미실측**, "이탈 없음"이 아니라 "이번 조사 범위에서 미검출"로 해석할 것.

**P0(1건)**: SCR-008 Order Complete BottomCTA 3중 override.
**P1 후보(3건)**: Payment Declined UX 중복 / Timeout 상태 불일치 / Loading CTA 처리 정책 불일치.

**구현 시사점**: 화면들이 State별 프레임으로 명확히 분리돼 있어 React 상태분기로 옮기기 용이. BottomCTA를 `<BottomCTA variant state />`로 강타입화하면 SCR-008 같은 "잘못된 variant가 잘못된 화면에 꽂히는" 회귀를 컴파일 타임에 방지 가능(이번 P0가 정확히 그 위험을 실증). Loading/Error/Empty 뼈대는 공통 `<StatusScreen>` 프레젠테이션 컴포넌트로 추출 권장.

---

## 6. 관리자 화면 — 📊 06-C. Screens / Admin (134:10606)

**규모**: top-level 프레임 79개 → 실제 UI 화면 **72개**(10개 플로우×5~11 상태), Annotation 7개 제외. **표준 크기(1920×1080) 이탈**: **0건**(72개 전부 표준 준수). 누적 **45/72개 화면 실측 완료(62.5%)**, 정밀 실측(get_design_context) 5건 — 2회 세션에 걸쳐 Figma 호출 한도에 부딪혀 완주하지 못함(§6.4 참조).

### 6.1 3대 컴포넌트 버그의 화면 재현 여부 — 최종 결론

| 버그 | 재현 여부 | 근거 |
|---|---|---|
| StatusBadge 91.7% 오표시 | **재현 안 됨(실사용 0건)** — 전체 72화면 중 인스턴스 단 1개, 그마저 화면 밖(y=−8) 고아 레이어로 비가시 | get_metadata 전수검색 + 스크린샷 확인 |
| SaveBar 계열 다크톤+3벌 불일치 | **재현됨(다수 화면)** — Menu/Sold-out/Payment 관리 다수 화면. Payment error는 솔리드 레드까지 재현. Sold-out "Item Changed"는 다크SaveBar+흰StickyActionBar **동시 노출 이중화 버그**까지 신규 확인 | get_screenshot 다수 + get_design_context 3건 |
| TopHeaderItem 색 반전 | **마스터엔 존재, 실사용 임팩트 낮음** — Order Management에서 탭그룹 아닌 단일 배지로만 1개 사용, 색 비교 대상 자체가 없어 혼동 미발생 | get_screenshot(235:14618) |

### 6.2 화면별 핵심 발견

**Live Order(SCR-009, 6/7 화면)**: **P0 — Detail Open(235:6361)에서 메뉴3건×12,800원인데 "총 결제 금액 0원"**(priceCalculation 핵심 로직 미바인딩 의심). Empty/Error/Success Toast/Save Error 4개 화면에서 **아이콘이 전부 "색만 다른 무의미한 원" placeholder**(Foundations "색상만으로 상태구분 금지" 위반 패턴, 아이콘 미배치로 추정). 상단 중앙 "완료" 배너가 Default/Detail Open/Confirm/Toast 등 **여러 상태에 걸쳐 상시 노출**되어 우측 상단 토스트와 **이중 알림 UI** 형성(P1).

**Menu Management(SCR-016, 9/10 화면)**: Validation Error에 다크 SaveBar 재현. Delete Confirm/Validation Error 화면에 **디자인팀이 남긴 구현 주석**(`COMPONENT_GAP`, `COMPONENT_VARIANT_GAP` 등)이 캔버스에 텍스트로 존재 — 실제 포팅 시 참고 가능한 유용한 자산(긍정 발견). Loading 화면만 스피너뿐 텍스트 없어 다른 Loading과 패턴 불일치(P2).

**Sold-out Management(SCR-011, 10/10 화면)**: **P0 신규 — "Item Changed"(241:14211)에서 다크 SaveBar와 흰색 "변경사항 3건" 알림이 동시에 겹쳐 노출**(Live Order의 토스트 이중화 패턴이 저장 안내 UI로 확산 재현). SoldOutCard(134:11929)의 category-tag는 StatusBadge가 아닌 별도 raw div라 **텍스트 정확**(StatusBadge 버그 무관), 다만 텍스트 **9px**로 최소기준에 정확히 걸림(P2).

**Payment Methods(SCR-018, 9/9 화면)**: 다크 PaymentSaveBar(`#262626`) 재현 확인. **P0 신규 — "Toggle Changed"(243:17279)에서 결제수단 4행이 전부 "카드 / 삼성페이 결제"로 동일 표기**(목데이터 미분기) **+ 좌측 리스트(네이버페이 off)와 우측 미리보기 패널(전부 on) 상태 불일치**. Save Error에서 **솔리드 레드(#e53333급) + 우상단 토스트 동시 노출**(이중 알림 재확인). "All Disabled Warning"은 상태명에 맞는 구체적 경고문구 없이 범용 문구만 노출(P1).

**Login(SCR-015, 5/5 화면)**: 전반적으로 깔끔, 과한 장식 없음. 로그인 유지 체크박스는 **체크마크(✓) 실제 존재**(§4-B.1 Admin/Checkbox 마스터의 "체크아이콘 없음" 버그와 무관한 별도 구현). **P1 — Unauthorized 화면이 일반 Empty State("데이터가 없습니다")를 그대로 재사용** — 미인가 접근 안내로는 문맥 부적절, 전용 문구 필요.

**Dashboard/Sales(SCR-019~022, 5/17 화면, 대체로 우수)**: **긍정 발견** — 4개 화면 전부 실제 포맷 숫자 사용, §4-A.6 SalesMetricCard "데이터 연결 예정" 버그가 **실화면엔 재현 안 됨**. Empty Data 상태도 컴포넌트 정의("—")와 정확히 일치. Sales Summary/Monthly/Daily 3종은 카드+차트+패널 구조로 통일 — **관리자 화면 중 가장 완성도 높은 그룹**.

**Order Management(SCR-010, 1/6 화면)**: 상태 배지(접수/준비중/완료/취소)는 실화면에서도 텍스트 정상(DataTableRow-Active 신뢰 가능 재확인). 총액 "0원" 버그 재확인.

### 6.3 관리자 화면 종합

**표준 크기 이탈**: 0건. **StatusBadge 실사용**: 사실상 0건(무해 판정). **SaveBar 버그**: 다수 화면 재현+신규 이중화 확산 확인.

**P0(3건, 화면 QA 신규)**:
1. SCR-009 Detail Open — 라인아이템 합계 vs "총 결제 금액 0원" 불일치(priceCalculation 관련, 최우선)
2. SCR-011 Sold-out "Item Changed" — 다크 SaveBar + 흰 StickyActionBar 동시 노출 이중 알림
3. SCR-018 Payment "Toggle Changed" — 결제수단 4행 이름 미분기 + 좌우 패널 토글 상태 불일치

**P1(4건)**: Live Order 아이콘 placeholder 4화면 반복 / 상단 배너-토스트 이중 알림 / Payment "All Disabled Warning" 문구 부적절 / Login "Unauthorized" Empty State 오용.
**P2(3건)**: Status Change Confirm 목데이터 주문번호 불일치(#1225) / Default 카드 총액 들쭉날쭉(2000원/0원) / SoldOutCard 9px 텍스트 / Menu Loading 패턴 불일치.

**미실측 잔여(~20~27개)**: SCR-016 Detail Edit, SCR-010 Default 등 4개, SCR-019~022의 Loading/Empty/Error/변경계열 다수 — 대부분 이미 확인된 Loading/Empty/Error 반복 패턴이라 우선순위 낮음, 후속 세션에서 마무리 권장.

### 6.4 조사 한계

Figma MCP 호출이 "Professional 플랜 Full seat 한도"에 두 차례 도달(1회차 6개 화면 후 완전 중단, 2회차 39개 화면 후 자연 종료). 6개 QA 에이전트가 동시에 같은 Figma 계정에 요청을 보낸 것이 원인으로 추정 — 향후 이 파일에 대규모 병렬 조사를 할 때는 순차 진행이나 세션 간격 확보를 고려할 것.

---

## 7. 전체 종합

### 7.1 전체 P0 결함 통합 (컴포넌트+화면 교차검증 반영)

| # | 위치 | 결함 | 화면 재현 여부 |
|---|---|---|---|
| 1 | Kiosk/CartItemCard, MenuDetailSummary | **Blue(#0088FF, #3B82F6) 재발** — 과거 지적 이력 미해결 | 컴포넌트 확정, 화면 육안 범위 미검출(정밀 조사 필요) |
| 2 | Kiosk/MenuDetailSummary | 이질적 legacy variant 혼입(다른 폰트·색·1080×320 vs 480×403) + QuantityStepper 오버플로우 | 화면 미조사(컴포넌트 단계 확정) |
| 3 | Kiosk/OptionSelectionRow | 핵심 옵션선택 15 variant 전수 16px 미만 폰트 | 컴포넌트 확정 |
| 4 | Kiosk/BottomCTA | "opacity 아님" 문서 vs `opacity-50` 구현 모순 | 컴포넌트 확정 |
| 5 | Kiosk/Category, CategoryTap | Admin 컴포넌트 혼재 + 터치 타깃 FAIL(11px) + Deprecated 미정리 | 컴포넌트 확정 |
| 6 | Shared 전반 | Primitive 직접 바인딩(정책 위반), 하드코딩 hex 2건, Kiosk Dark Surface색 텍스트 오용 4회, Neutral 혼용, Toast 스펙불일치 | 컴포넌트 확정 |
| 7 | AllergenTag/Notice | 경고 토큰 저대비(≈1.5~1.7:1, 접근성) | 컴포넌트 확정 |
| 8 | **SCR-008 Order Complete** | BottomCTA 크기(940×200)·variant·폰트 3중 override, **과거 결함값 정확히 재발** | **화면 실사례로 확정, 최우선** |
| 9 | Admin/Checkbox | 체크 아이콘(✓) 자체 부재 — 색상만으로 상태구분 | 컴포넌트 확정 |
| 10 | Admin/SearchInput | 마스터 기본폭 150px, placeholder 문구 물리적으로 안 들어감 | 컴포넌트 확정, 화면은 수동 확대로 은폐 |
| 11 | Admin/MenuButton | 비표준 색(4종 미등록 hex) + 16px 클릭타깃(최소 32의 절반) | 컴포넌트 확정 |
| 12 | Admin/IngredientTypeFilterChip | Selected 4/7만 존재, 카테고리색 status색 전용, 베이스=채소 동일색 | 컴포넌트 확정, 실제 화면(Menu Detail Add)에서도 재현 |
| 13 | Admin/OrderActionButtons | Primitive 직접 사용(제3의 미등록 팔레트) | 컴포넌트 확정 |
| 14 | **SaveBar/StickyActionBar/PaymentSaveBar 3벌** | 색상·토큰화·error 의미 전부 불일치, 일상 미저장에 솔리드 레드 오용 | **화면 다수 재현 + 신규 이중화 확산 확인** |
| 15 | **SCR-011 Sold-out Item Changed** | 다크SaveBar+흰StickyActionBar 동시 노출 이중 알림 | **화면 신규 발견** |
| 16 | **SCR-018 Payment Toggle Changed** | 결제수단 4행 이름 미분기 + 좌우 패널 상태 불일치 | **화면 신규 발견** |
| 17 | **SCR-009 Detail Open** | 라인아이템 합계 vs "총 결제 금액 0원" | **화면 신규 발견(가격계산 로직 관련)** |
| ~~18~~ | ~~Admin/StatusBadge~~ | ~~91.7% 오표시~~ | **화면 재검증 결과 실사용 0건 — 하향 조정, 마스터만 수정하면 충분(급하지 않음)** |
| ~~19~~ | ~~Admin/TopHeaderItem~~ | ~~색 반전~~ | **화면 재검증 결과 실사용 임팩트 낮음 — 하향 조정** |
| ~~20~~ | ~~Admin/SalesMetricCard~~ | ~~"데이터 연결 예정" 플레이스홀더~~ | **화면 재검증 결과 실제 화면엔 미재현 — 하향 조정, 마스터만 정리하면 충분** |

→ **실질 최우선 P0 17건**(컴포넌트 12건 + 화면 신규 5건), **컴포넌트 P0였으나 화면 교차검증으로 긴급도 하향된 것 3건**(마스터 정리는 필요하나 사용자 체감 리스크는 낮음). 이 하향 조정 자체가 이번 재실측의 핵심 가치 — **"마스터 컴포넌트 결함"과 "실제 사용자가 보는 화면의 결함"을 분리해서 우선순위를 매길 수 있게 됨.**

### 7.2 색상 활용도 — 종합

| 이슈 | 실측 | 키오스크 | 관리자 |
|---|---|---|---|
| Blue 오용 | CartItemCard, MenuDetailSummary | 삭제 필요 | 해당 없음(단 PaymentPolicyCard 링크에 별도 Blue 발견) |
| Purple | StatusBadge 드레싱 1개 Role만(정책 준수), IngredientTypeFilterChip 드레싱(정책 준수) | 해당 없음 | 정책 준수 확인, 남용 없음 |
| "제3의 팔레트"(accents/*, gray/NNN, green/NNN) | MenuButton, OrderActionButtons, OrderDetailRow, Navbar, OrderCard, Pagination, DataTableHeader 등 **파일 전역에 광범위 산재** | OrderDetailRow(6/7 state) | MenuButton, OrderActionButtons, Navbar 등 다수 |
| Primitive 직접 바인딩(Semantic 미사용) | Shared 거의 전부, Navbar, OrderActionButtons | 해당 | 해당 |
| SaveBar 계열 다크톤 불일치 | 3벌 각기 다른 hex | — | **최다 발견 이슈, 화면 재현+확산 확인** |
| 저대비 경고색 | AllergenTag/Notice(#FBBF24 on #FFFBEB), DataTableRow-Active "준비중" | 해당 | 해당 |
| Neutral 혼용 | LoadingState, 다수 컴포넌트 | 해당 | 해당(CoolGray/PureGray/제3넘버링 3중) |

### 7.3 글자 크기·행간 — 종합

- **Kiosk**: 21개 컴포넌트 중 **9개**에서 16px 미만 본문 발견(체계적 문제). OptionSelectionRow(핵심 컴포넌트) 15variant 전수 위반이 가장 심각. AUTO(미명시 line-height) 컴포넌트 다수.
- **Admin**: 9px 이하는 SoldOutCard category-tag(9px, 화면 재확인) 1건 외 대체로 회피됨. 11~13px 캡션/배지는 허용범위. **13px가 SearchInput·FilterChip·PaymentMethodSettingRow 등에서 반복 등장** — 사실상 관행화된 미문서 값(Typography Scale에 정식 등재 검토 권고).
- **Shared**: 폰트 크기 자체는 스케일 준수 우수, 다만 Body/S(14px)가 Kiosk 맥락 다수 컴포넌트에 쓰여 Kiosk 기준으로는 미달.
- **공통**: 대부분 컴포넌트가 line-height를 AUTO(100%)로 방치 — Foundations가 정의한 명시적 line-height 값을 인스턴스 레벨에서 적용하지 않은 경우가 많음.

### 7.4 여백·레이아웃 — 종합

- **비체계 gap 반복값**: py-14(Shared 5개 컴포넌트, 48px 터치 목표용 의도적 값으로 추정 — 정식 토큰화 권고), gap 76(StepIndicator, 80 근접), gap 200+(OrderCard 우려했으나 **미재현**).
- **Border**: PaymentMethodCard 4px(Border Scale 최대 3px 초과), QuantityStepper pressed `border-black` 하드코딩.
- **완전 미바인딩(raw hex, var() 자체 없음)**: EmptyState 테두리(#ccc), Icon placeholder, DataTableHeader, Pagination, SearchInput, SaveBar 3벌 — **8개 지점에서 확인**, Figma 파일 내 토큰화 커버리지의 실제 구멍.
- **화면 레벨 유일한 크기 override**: SCR-008 BottomCTA(940×200) — 129개 화면(Kiosk 57+Admin 72) 중 **유일한 프레임/인스턴스 크기 이탈**, 나머지는 전부 표준(1080×1920 / 1920×1080) 정확 준수.

### 7.5 트렌드함 · AI스럽지 않은 느낌 — 종합

**Do(유지·확산할 것)**: PaymentMethodCard의 tint+4px 브랜드 border 선택패턴(OptionSelectionRow에도 확산 권장) / IngredientTableRow·DetailPanel의 정확한 Semantic 바인딩 / Empty·Error 화면의 아이콘+제목+설명+버튼 뼈대 재사용(단 실제 아이콘 배치는 필수) / Dashboard·Sales 화면군의 일관된 카드+차트+패널 구조(관리자 화면 중 최우수 사례).

**Don't(제거할 것)**: Navbar Active 메뉴의 8겹 중첩 섀도우(Foundations 기준의 2배) / TopHeaderItem의 White Backing+Tint+Glass 4겹 레이어(컴포넌트 스스로 "Decorative, 제거 후보" 자인) / Blue/Purple을 상태색과 무관하게 카테고리·CTA색으로 전용하는 패턴(IngredientTypeFilterChip, PaymentPolicyCard) / 여러 화면에서 반복되는 "색만 다른 무의미한 원" 아이콘 placeholder(Empty/Error/Toast 다수, 실제 아이콘 미배치 상태를 장식으로 오인하기 쉬움).

**AI스러움 판정**: 과도한 네온 글로우·다층 그라데이션 같은 전형적 "AI 생성물" 안티패턴은 전반적으로 관찰되지 않음(플랫 디자인 유지, 담백한 카드 위주). 대신 이 파일의 실제 문제는 "AI스러운 과잉 장식"보다 **"토큰 시스템은 설계했지만 실제 적용이 급하게 마감된 흔적"**(Primitive 직접 사용, 하드코딩 hex, 컴포넌트 간 색상 언어 불일치, 문서-구현 모순)에 가깝다 — 이는 오히려 여러 사람/세션이 병렬로 빠르게 작업한 실제 협업 흔적으로 해석하는 것이 더 정확하다.

### 7.6 스크린 구현 시 공통 고려사항

1. **Master 우선 수정 원칙 유지**: Master를 고치면 05-C/06-C Production Instance에 자동 전파된다. 스크린만 고치면 재발한다(과거 원칙, 이번 조사로 재확인 — SCR-008이 정확한 반례: Master는 정상인데 화면 인스턴스에서 override로 깨짐).
2. **BottomCTA류를 강타입 props로 구현**: `variant`×`state` 조합을 컴파일 타임에 강제하면 SCR-008 같은 "잘못된 variant 적용" 회귀를 원천 차단할 수 있다.
3. **SaveBar 계열 3벌을 하나의 semantic 토큰 세트로 통합**: 어느 컴포넌트를 정본으로 삼을지 먼저 결정 후 통합.
4. **알림/토스트 UI를 단일 컴포넌트로 통합**: 현재 "상단 중앙 배지"와 "우측 토스트"가 여러 화면에서 이중 노출되는 패턴이 반복 확인됨 — 하나의 알림 시스템으로 합칠 것.
5. **가격 합산 로직을 디자인 목업과 분리해서 반드시 구현**: OrderCard·DetailPanel·SCR-009 Detail Open 등 "총액 0원" 플레이스홀더가 여러 곳에서 반복 발견 — Figma 문구를 그대로 카피하지 말고 `priceCalculation.js` 기준 실계산 로직을 반드시 붙일 것.
6. **StatusBadge의 role→label 매핑은 프론트엔드에서 별도 테이블로 구현**: Figma 텍스트 레이어를 그대로 읽지 말 것(색상 매핑 로직은 정상이므로 그대로 가져와도 됨).
7. **Primitive 변수를 그대로 CSS 변수화하지 말 것**: Semantic 토큰으로 재매핑 후 구현.
8. **Empty/Error 아이콘은 실제 아이콘 컴포넌트로 교체**: 현재 다수 화면에서 "색만 다른 무의미한 원"으로 나타나는 것은 디자인 의도가 아니라 미배치 상태로 판단됨.

### 7.7 작업 배치 제안

**Batch V-Kiosk(마스터 수정, 05-C 자동 전파)**: ① CartItemCard/MenuDetailSummary Blue 제거 ② MenuDetailSummary legacy variant 분리 ③ OptionSelectionRow 폰트 15/14→16px+ ④ BottomCTA opacity 모순 해소 ⑤ Category/CategoryTap 아키텍처 정리(Admin 분리, Deprecated 이동) ⑥ OrderDetailRow legacy 변수→Semantic 전환.

**Batch V-Admin(마스터 수정, 06-C 자동 전파)**: ① SaveBar/StickyActionBar/PaymentSaveBar 3벌 통합(최우선, 화면 확산 확인됨) ② Checkbox 체크아이콘 추가 ③ SearchInput 마스터 기본폭 확대 ④ MenuButton 색상+크기 표준화 ⑤ IngredientTypeFilterChip Selected 3종 추가+카테고리색 재설계 ⑥ OrderActionButtons Semantic 전환.

**Batch V-Screen(화면 전용, Master 밖)**: ① SCR-008 BottomCTA override 제거(최우선, 이미 정확한 원인 특정됨) ② SCR-009/SCR-011/SCR-018 신규 발견 3건(가격계산, 이중알림, 목데이터 미분기) ③ 가격 합산 로직 전체 재검토(우선순위 상향 권고) ④ Live Order 등 아이콘 placeholder 실제 아이콘으로 교체.

**Batch V-Shared(마스터 수정)**: ① ConfirmDialog warning 전용색 신설 ② AllergenTag/Notice 경고 텍스트색 재설계(접근성) ③ Toast 스펙-실측 정합화 ④ EmptyState 하드코딩 hex 제거 ⑤ LoadingState 회색 통일.

**하향 조정(급하지 않음, 마스터만 정리)**: StatusBadge 라벨(실사용 0건), TopHeaderItem 색반전(단일 사용), SalesMetricCard 플레이스홀더(실화면 미재현).

---

## 8. 메타

| 항목 | 값 |
|---|---|
| 측정일 | 2026-07-17 |
| 방법 | Figma Plugin API 읽기 전용(get_metadata/get_design_context/get_screenshot/get_variable_defs), 쓰기 0회 |
| 조사 구성 | 6개 병렬 서브 에이전트 + Foundations 직접 정리 |
| Shared 컴포넌트 | 9종 + Deprecated 5종, 실측 완료 |
| Kiosk 컴포넌트 | 21개 중 19개 실측(Deprecated/menu-card, AllergyAccordion collapsed 미확인 — Figma 호출 한도) |
| Admin 컴포넌트 | 약 53개(Part A 11 + Part B ~42), 대부분 실측·일부 대표 스크린샷 |
| Kiosk 화면 | 73프레임 중 실제화면 57개, 육안확인 17개+정밀1건(호출한도로 전수 미완) |
| Admin 화면 | 79프레임 중 실제화면 72개, 실측완료 45개(62.5%), 정밀 실측 5건 |
| 주요 제약 | Figma MCP "Professional 플랜 Full seat 한도"에 복수 회 도달 — 병렬 조사량이 원인으로 추정, 향후 재조사 시 순차 진행 권고 |
| 남은 과제 | Admin 화면 잔여 ~20~27개(대부분 반복 Loading/Empty/Error, 우선순위 낮음), Kiosk 화면 정밀 색상 실측 40개, Blue 재발 지점의 화면 단 재확인 |

---

## 9. 결론

- **키오스크**: 컴포넌트 단계에서 "작은 폰트(9/21 컴포넌트 16px 미만)·AUTO 행간·Blue 재발·Legacy 팔레트 잔존"이 광범위. 화면 단계에서는 **표준 크기 이탈 0건**으로 구조 자체는 안정적이나, **SCR-008 Order Complete만 정확히 과거와 동일한 방식으로 깨져 있음** — 이 1건이 실사용자가 가장 먼저 체감할 결함.
- **관리자**: 컴포넌트 단계 결함(StatusBadge/TopHeaderItem/SalesMetricCard)이 **화면 교차검증 결과 실사용 임팩트가 낮은 것으로 재확인**된 반면, **SaveBar 계열 3벌 불일치는 오히려 화면에서 확산·심화**되어 발견됨(이중 알림 UI로까지 번짐) — "컴포넌트 문서만 보고 우선순위를 매기면 안 되고 실제 화면까지 봐야 한다"는 것을 이번 조사가 직접 증명.
- **Shared**: 폰트 크기·행간 정책 준수는 가장 우수하나, **Primitive 직접 바인딩과 하드코딩 hex가 시스템 전반에 구조적으로 퍼져 있어** 컴포넌트 개수 대비 결함 밀도는 오히려 가장 높음.
- **공통 근본 원인**: "디자인 토큰 시스템은 정교하게 설계돼 있으나(Foundations 문서 자체는 훌륭함), 실제 컴포넌트 인스턴스 단계에서 절반 정도만 적용되고 나머지는 급하게 하드코딩/legacy 값으로 마감된 상태" — AI스러운 과잉 장식 문제가 아니라 **토큰화 적용률의 문제**로 요약된다.

---

*끝. 수정 적용은 별도 승인 후 위 Batch 순서로 진행 권장.*
