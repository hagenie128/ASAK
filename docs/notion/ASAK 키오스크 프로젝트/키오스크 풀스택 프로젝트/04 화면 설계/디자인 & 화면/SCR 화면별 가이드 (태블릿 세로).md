# SCR 화면별 가이드 (태블릿 세로)

<aside>
✅

**2026-07-06 회의 반영** — SCR-002→SCR-001「홈 (매장·포장)」· SCR-006→SCR-005「장바구니·주문확인」**병합** (`병합됨`). 고객 UI **6단계**. 프로덕션 DS **DS-02 Modern Minimal**.

- 장바구니·주문확인은 **한 화면(SCR-005)** + **컨펌 팝업** (별도 SCR-006 라우트 없음)
- 고객 흐름: `SCR-001 → SCR-003 → SCR-004 → SCR-005(팝업) → SCR-007 → SCR-008`
- SCR-002·006 섹션은 Figma Archive·참조용
</aside>

<aside>
📌

**이 페이지의 역할** — SCR별 **wireframe·UX 패턴**만 기술합니다. 아래는 각 정본을 참고하세요.

- 회의 컨셉·팔레트·Trend → [브랜드 · Trend 컬러](%EB%B8%8C%EB%9E%9C%EB%93%9C%20%C2%B7%20Trend%20%EC%BB%AC%EB%9F%AC.md)
- Figma 파일·Page·Variables → [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md)
- SCR×Figma 매트릭스·체크리스트 → [Figma 가이드](Figma%20%EA%B0%80%EC%9D%B4%EB%93%9C%20+%20SCR%C3%97Figma%20%EB%A7%A4%ED%8A%B8%EB%A6%AD%EC%8A%A4.md)
- 화면 목록·상태·REQ → [04. 화면 설계 SCR DB](../../04%20%ED%99%94%EB%A9%B4%20%EC%84%A4%EA%B3%84.md)
</aside>

<aside>
🔗

**Git 로컬 도구** (정본 아님)

- GitHub: [https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md](https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md)
- [figma-links.template.json](https://github.com/hagenie128/ASAK/blob/main/docs/design/figma-links.template.json)
</aside>

---

> **834 × 1194** portrait · Safe area 상하 24 / 좌우 16 · Touch min **48px**
>

> 팀 정본: [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) · Page 셋업: [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md)
>

---

## 3축 통합 원칙

| 축 | 우선순위 | 역할 |
| --- | --- | --- |
| **회의 컨셉** | ★ 정본 | 팀이 확정한 브랜드·MVP·톤 — 모든 SCR의 출발점 |
| **Figma 레퍼런스** | 근거 | 팀 파일·Community·Courses kit에서 **복사할 패턴** 지정 |
| **프랜차이즈 UX** | 벤치마크 | 버거킹·공차 등 **패턴 이름**만 차용, 브랜드 색·로고 복제 금지 |

> 회의와 모순되는 패턴(과한 자연풍 히어로, 복잡한 다단 메뉴, 고급 무게감 레이아웃)은 **대안**으로만 표기. 회의 컨셉·팔레트·Trend 매핑 → [브랜드 · Trend 컬러](%EB%B8%8C%EB%9E%9C%EB%93%9C%20%C2%B7%20Trend%20%EC%BB%AC%EB%9F%AC.md) · Figma 리소스·매트릭스 → [Figma 가이드](Figma%20%EA%B0%80%EC%9D%B4%EB%93%9C%20+%20SCR%C3%97Figma%20%EB%A7%A4%ED%8A%B8%EB%A6%AD%EC%8A%A4.md)
>

---

## SCR-001 / 홈 (매장·포장)

**회의 반영:**

- **2026-07-06**: SCR-002(먹고가기/포장) 흡수 — 브랜드 안내 + **매장/포장 선택 카드** 한 화면
- Cream `#FFFDF3` 단순 풀스크린, DS-02 Modern Minimal 적용
- orderType(EAT_IN/TAKE_OUT)은 장바구니·결제까지 유지

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `📱 Customer` Page, frame `SCR-001 / 홈`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — 시작 화면·단일 CTA flow
- [Kiosk Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) — 세로형 브랜드 영역 비율

**프랜차이즈 패턴:**

- 맥도날드 — 큰 시작 CTA, 브랜드 로고 중앙 *(색상·로고 복제 X)*
- 샐러디 — 밝은 배경·프레시 톤 *(green-heavy 그리드는 SCR-003으로 분리)*

**Trend:** **Trend-4** (blush bg + forest CTA) · A/B: Trend-1

**Wireframe (834×1194):**

```
┌────────────────────┐
│     [로고 ASAK]     │  ← 상단 40%, 중앙
│   아삭하게, 건강하게   │  ← optional 슬로건
│   [히어로 optional]  │  ← 16:9 crop, 없어도 OK
│                    │
│  ┌──────────────┐  │
│  │  주문 시작하기  │  │  ← thumb zone, h≥56px
│  └──────────────┘  │
│  [접근성 ⚙]         │  ← 좌하단 48px+
└────────────────────┘
```

**CTA / Copy tone:** **「주문 시작하기」** — 친근·빠른주문 · 스크롤 없음

**REQ / SC:** FWD-UI-002 · SC-001 시작

---

## SCR-002 / 먹고가기 · 포장 선택

> **【병합됨】** 2026-07-06 — SCR-001「홈 (매장·포장)」에 통합. 별도 라우트·와이어 없음. Figma frame은 Archive 또는 `[병합됨]` 라벨.
>

**회의 반영 (참고·Archive):**

- Week 5 MVP 필수 — **1탭 빠른 선택**, 화면 단순 유지
- food photo **과다 배치 금지** (회의: 복잡하지 않게)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-002 / 주문유형`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — dine-in / takeaway 분기

**프랜차이즈 패턴:**

- 맥도날드·롯데리아 — 먹고가기/포장 **대형 선택 카드**
- 써브웨이 — 단계 진입 전 **order type** 분기 *(builder는 SCR-004)*

**Trend:** **Trend-5** — Crunch Yellow `#FACC15` 선택 카드 포인트

**Wireframe:**

```
┌────────────────────┐
│ ← 뒤로   어디서 드시나요? │
├────────────────────┤
│  ┌──────────────┐  │
│  │  🍽 먹고가기   │  │  ← 카드 h≥56px
│  └──────────────┘  │
│  ┌──────────────┐  │
│  │  🥡 포장하기   │  │
│  └──────────────┘  │
└────────────────────┘
```

**CTA / Copy tone:** 카드 라벨 **「먹고가기」** / **「포장하기」** — 프레시·편의성

**REQ / SC:** FWD-ORDER-001 · SC-001

---

## SCR-003 / 메뉴 선택

**회의 반영:**

- **photo-first** 카드형 메뉴, 카테고리별 조회
- 직관적 2열 그리드, 품절 표시
- 하단 장바구니 바 (실시간 장바구니 미리보기는 **후순위**)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-003 / 메뉴`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — menu grid·category tabs
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — card radius·shadow 토큰

**프랜차이즈 패턴:**

- **버거킹** — `photo-card` 풀블리드 60~70% + 이름·가격
- **맥도날드** — 카테고리 탭 + 2~3열 그리드 + 하단 장바구니 바
- **샐러디** — 샐러드·볼·랩 카테고리, 신선 톤

**Trend:** **Trend-1** photo 강조 + 회의 Primary `#16A34A` CTA

**Photo:** `/assets/menu/{id}.png` · seed `asak-data/images/menu/{id}.png` · 16:9 cover

**Wireframe:**

```
┌────────────────────┐
│ ←  [카테고리 탭 →]    │
├────────────────────┤
│ ┌────┐ ┌────┐     │
│ │photo│ │photo│    │  ← 2col, card min-h 120px
│ │메뉴 │ │메뉴 │    │
│ └────┘ └────┘     │
│ ┌────┐ ┌────┐     │
│ │품절│ │    │     │
│ └────┘ └────┘     │
├────────────────────┤
│ 🛒 장바구니 (3)     │  ← sticky
└────────────────────┘
```

**CTA / Copy tone:** **「장바구니 (N)」** · 품절 **「품절」** 배지 — 신선·빠른주문

**REQ / SC:** FWD-UI-001, FWD-UI-002 · SC-001, SC-002

---

## SCR-004 / 메뉴 상세 · 옵션 선택

**회의 반영:**

- 옵션 **3단 트리**: 베이스 → 토핑 → 드레싱
- **추천조합 기본값** 선체크, 선택 상태 즉시 표시
- 칼로리·재료 확인 가능 (상세 영양 고도화는 후순위)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-004 / 옵션`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — customization step UI

**프랜차이즈 패턴:**

- **공차** — `option-list` 그룹 헤더 + 체크/라디오 + 실시간 합계
- **써브웨이** — sandwich builder **단계별** 선택
- **샐러디/프레시** — ingredient chips, bowl visual
- **스타벅스** — 커스터마이즈 아코디언·칩 요약

**Trend:** **Trend-4** — forest option row + blush bg

**Photo:** hero 상단 35% — `/assets/menu/{id}.png`

**Wireframe:**

```
 ┌────────────────────┐
│ ←     [hero 35%]    │
├────────────────────┤
│ 메뉴명 · ₩ · kcal   │
│ [기본재료 chips]     │
│ ─ 베이스 ─          │
│ ○ 그린 · ○ 퀴노아    │
│ ─ 토핑 ─            │
│ □ 닭가슴살 +500      │
│ ─ 드레싱 ─          │
│ ○ 발사믹             │
├────────────────────┤
│ ₩12,000    [담기]   │  ← sticky
└────────────────────┘
```

**CTA / Copy tone:** **「담기」** + 합계 — 친근·편의성 (옵션 설명 1줄)

**REQ / SC:** FWD-MENU-001~005, FWD-MENU-015, LMIS-MENU-002 · SC-001, SC-002

---

## SCR-005 / 장바구니·주문확인

**회의 반영:**

- **2026-07-06**: SCR-006(주문 확인) 흡수 — 최종 확인은 **컨펌 팝업**만
- 하단 **추가 제안 상품** 섹션, 알레르기·칼로리는 SCR-004에서 표시 (장바구니 아님)
- 포장 선택 시 **봉투 추가** 옵션 (MVP), 총액 명확

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-005 / 장바구니`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — cart list·quantity

**프랜차이즈 패턴:**

- **맥도날드** — 수량±·항목 리스트·sticky 총액
- **스타벅스** — order summary, pickup 안내 톤

**Trend:** **Trend-4**

**Photo:** 항목 썸네일 소형만 (48×48~64)

**Wireframe:**

```
┌────────────────────┐
│ ←      내 주문       │
├────────────────────┤
│ [thumb] 항목1  ± 🗑  │
│ [thumb] 항목2       │
│ 먹고가기 / 포장       │
│ □ 봉투 추가 +200원    │  ← 포장 시만
├────────────────────┤
│ 알레르기 안내 (접기)   │
│ 총액 ₩XX,XXX         │
│ [주문하기]           │
└────────────────────┘
```

**CTA / Copy tone:** **「결제하기」** — 컨펌 팝업 확인 후 API-005 주문 생성 → SCR-007 결제 진입

**REQ / SC:** FWD-CART-001, FWD-CART-002 · SC-001, SC-004

---

## SCR-006 / 주문 확인

> **【병합됨】** 2026-07-06 — SCR-005「장바구니·주문확인」에 통합. 최종 확인은 컨펌 팝업만. Figma frame은 Archive 또는 `[병합됨]` 라벨.
>

**회의 반영 (참고·Archive):**

- 주문 유형·옵션·제외 재료 **한눈에** 확인
- 결제 전 최종 확인 — 복잡한 upsell 없음

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-006 / 주문확인`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — order review

**프랜차이즈 패턴:**

- **스타벅스** — order confirm, 항목·옵션 요약
- KFC/롯데리아 — combo 요약 *(세트 고도화는 후순위)*

**Trend:** **Trend-4**

**Wireframe:**

```
┌────────────────────┐
│ ←   한 번 더 확인해 주세요 │
├────────────────────┤
│ 먹고가기 · 2품목      │
│ ┌ 샐러드 ×1 ─ 옵션… ┐ │
│ └──────────────────┘ │
├────────────────────┤
│ 총 결제금액 ₩XX,XXX  │
│ [결제하기]           │
└────────────────────┘
```

**CTA / Copy tone:** **「결제하기」** — API-005 주문 생성 후 SCR-007 결제 진입

**REQ / SC:** FWD-CART-001, FWD-CART-002, FWD-ORDER-001, DEV-ORDER-001 · SC-001, SC-004

---

## SCR-007 / 결제

**회의 반영:**

- **가상 결제** (실제 결제수단 설정·멤버십 **보류**)
- 결제수단 카드 크고 명확

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-007 / 결제`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — payment method list

**프랜차이즈 패턴:**

- 맥도날드·버거킹 — 결제수단 **대형 카드** 선택

**Trend:** **Trend-5** — navy card + yellow 선택 상태

**Wireframe:**

```
┌────────────────────┐
│ ←       결제        │
├────────────────────┤
│ 결제금액 ₩XX,XXX    │
│ ┌ 💳 카드      ○ ┐ │
│ ┌ 📱 간편결제   ○ ┐ │
├────────────────────┤
│ [가상 결제 승인]     │
└────────────────────┘
```

**CTA / Copy tone:** **「가상 결제 승인」**

**REQ / SC:** FWD-PAY-001, KSD-PAY-001 · SC-004 *(멤버십 KSD-MEMBER-001 보류)*

---

## SCR-008 / 주문 완료

**회의 반영:**

- **주문번호** 크게 표시, 픽업 안내
- 10초 후 자동 초기화 검토 (SCR-013 연계)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-008 / 완료`
- [Kiosk Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) — success state

**프랜차이즈 패턴:**

- **스타벅스** — pickup name·order number 강조
- 맥도날드 — 완료 체크 + 다음 CTA

**Trend:** **Trend-4** + Fresh Lime `#A3E635` 완료 아이콘

**Wireframe:**

```
┌────────────────────┐
│        ✓           │
│  주문이 완료됐어요!    │
│   주문번호 #1234    │
│   카운터에서 픽업해 주세요 │
│                    │
│    [처음으로]        │
└────────────────────┘
```

**CTA / Copy tone:** **「처음으로」** — 친근·건강메이트

**REQ / SC:** FWD-PAY-002, FWD-ORDER-002, KSD-PAY-002 · SC-001 종료

---

## SCR-009 / 관리자 주문 관리

**회의 반영:**

- Week 5 MVP 관리자 **필수** — 주문 목록·필터
- **표·상태** 중심, food photo 없음

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-009` (`📱 Customer` 관리자 섹션)
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — list row·filter·badge

**프랜차이즈 패턴:**

- *(고객 프랜차이즈 패턴 미적용)* — 매장 POS·KDS 리스트 UX 참고

**Trend:** Courses kit surface + **Trend-5** navy header

**Wireframe:**

```
┌────────────────────┐
│ 주문 관리   [필터▼]  │
├────────────────────┤
│ #123 · 접수 · ₩8,900 │
│ #124 · 조리중 · ₩12k │
│ ...                │
└────────────────────┘
```

**CTA / Copy tone:** row tap → SCR-010 · 상태 뱃지 색 구분

**REQ / SC:** LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-004 · SC-005

---

## SCR-010 / 관리자 주문 상세

**회의 반영:**

- 메뉴·옵션·금액 확인 + **상태 변경** (KVS 전체는 보류, 단순 상태만)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-010`
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — detail card·dropdown

**프랜차이즈 패턴:** Admin 표·상태 UX (프랜차이즈 키오스크 무관)

**Trend:** Courses kit

**Wireframe:**

```
┌────────────────────┐
│ ←  주문 #1234       │
├────────────────────┤
│ 메뉴·옵션·금액       │
│ 상태 [접수 ▼]       │
├────────────────────┤
│ [상태 변경 저장]     │
└────────────────────┘
```

**CTA / Copy tone:** **「상태 변경 저장」**

**REQ / SC:** LMIS-ORDER-001~004 · SC-005

---

## SCR-011 / 관리자 품절 관리

**회의 반영:**

- Week 5 MVP — 메뉴/재료 **품절 토글** → 키오스크 SCR-003 반영
- 메뉴 등록/수정 전체·재고 수량은 **보류**

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-011`
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — toggle row

**프랜차이즈 패턴:** *(없음)* — 회의: 재고 기반 품절은 차별화 **후순위**, MVP는 수동 토글

**Trend:** Courses kit + Success/Error 토큰

**Wireframe:**

```
┌────────────────────┐
│ 품절 관리 [메뉴|재료] │
├────────────────────┤
│ 메뉴A      [품절 ○]  │
│ 재료B      [판매 ●]  │
└────────────────────┘
```

**CTA / Copy tone:** **「품절」** / **「판매 중」** 토글 — hit ≥48px

**REQ / SC:** LMIS-MENU-001, LMIS-MENU-002 · SC-003

---

## SCR-012 / 결제 실패 · 재시도

**회의 반영:**

- FWD-PAY-002 **상** 요건 — Week 5 MVP **최소 안내** 필요
- 친근한 톤, 과도한 경고 디자인 지양

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-012`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — error overlay

**프랜차이즈 패턴:** 맥도날드 결제 실패 — 2 CTA stack *(대안)*

**Trend:** **Trend-3** lime accent on error icon only

**Wireframe:**

```
┌────────────────────┐
│       ⚠           │
│  결제에 실패했어요    │
│  다시 시도해 주세요    │
│  [다시 결제]         │
│  [장바구니로]        │
└────────────────────┘
```

**CTA / Copy tone:** **「다시 결제」** · **「장바구니로」**

**REQ / SC:** FWD-PAY-002, KSD-PAY-001

---

## SCR-013 / 타임아웃 · 자동 초기화

**회의 반영:**

- 키오스크 취소 시 초기화 문제 개선 (SC-001 예외 흐름)
- 카운트다운 + 계속/취소

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-013`
- [Kiosk Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) — idle timeout pattern

**프랜차이즈 패턴:** 공통 키오스크 idle modal

**Trend:** **Trend-4**

**Wireframe:**

```
┌────────────────────┐
│  ⏱ 30초 후 초기화    │
│  [계속 주문] [취소]   │
└────────────────────┘
```

**CTA / Copy tone:** **「계속 주문」** — 친근

**REQ / SC:** FWD-SYS-001

---

## SCR-014 / 접근성 설정

**회의 반영:**

- 글자 크기·고대비 — 고객 화면 단순 유지
- 좌하단 SCR-001 진입

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-014`
- [Moja UI](https://www.figma.com/community/file/1108679668074690379/moja-ui-ultimate-ui-kit-design-system-variables-darkmode) — toggle·segmented control

**프랜차이즈 패턴:** *(없음)*

**Trend:** **Trend-4**

**Wireframe:**

```
┌────────────────────┐
│ ←   접근성 설정      │
│ 글자 크기 [S|M|L]   │
│ 고대비      [토글]   │
│ [적용]              │
└────────────────────┘
```

**CTA / Copy tone:** **「적용」**

**REQ / SC:** FWD-UI-001

---

## SCR-015 / 관리자 로그인

**회의 반영:**

- **후반 확장** (Week 5 MVP 제외) — Week 5 MVP 관리자는 SCR-009~011 직접 진입 가정

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `🛠 Admin` · `SCR-015`
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — form field

**프랜차이즈 패턴:** *(없음)*

**Trend:** Courses kit

**Wireframe:**

```
┌────────────────────┐
│     ASAK Admin     │
│ [아이디]            │
│ [비밀번호]           │
│ [로그인]            │
└────────────────────┘
```

**CTA / Copy tone:** **「로그인」**

**REQ / SC:** LMIS-AUTH-001

---

## SCR-016 / 관리자 메뉴 관리

**회의 반영:** 메뉴 등록/수정/삭제 **전체 보류** — frame만 후반용

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-016`
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — data table

**프랜차이즈 패턴:** *(없음)*

**Trend:** Courses kit

**REQ / SC:** LMIS-MENU-001, LMIS-MENU-004

---

## SCR-017 / 관리자 메뉴 등록·수정

**회의 반영:** 후반 확장 — 옵션 트리 구조는 SCR-004와 동일 3단

**Figma 참고:** [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) · [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410)

**프랜차이즈 패턴:** 공차 option group 구조 *(관리자 폼용 참고)*

**REQ / SC:** LMIS-MENU-004, FWD-MENU-013~015

---

## SCR-018 / 관리자 결제수단 설정

**회의 반영:** 실제 결제수단 설정 **보류**

**Figma 참고:** [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) · [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410)

**REQ / SC:** LMIS-PAY-001

---

## SCR-019 / 관리자 매출 요약

**회의 반영:** 매출 확인 **보류** — Week 5 MVP **제외**, 9주 후반

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-019`
- [Courses kit 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) — chart card

**프랜차이즈 패턴:** *(없음)*

**Trend:** Courses chart + **Trend-5** citrus accent

**REQ / SC:** LMIS-ORDER-005

---

## SCR-020 / 영수증 출력 여부 선택

**회의 반영:**

- Week 5 MVP **제외** — Week 7~8 장치 확장
- SCR-008 주문 완료 직후 분기 또는 오버레이

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-020 / 영수증`
- [Kiosk Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) — success 후속 선택

**프랜차이즈 패턴:** 맥도날드·스타벅스 — 영수증 예/아니오 2버튼

**Trend:** **Trend-4**

**Wireframe:**

```jsx
┌────────────────────┐
│        ✓           │
│  주문이 완료됐어요!    │
│   주문번호 #1234    │
│  영수증을 출력할까요?  │
│  [영수증 출력]       │
│  [출력 안 함]        │
└────────────────────┘
```

**CTA / Copy tone:** **「영수증 출력」** / **「출력 안 함」**

**REQ / SC:** RTOS-DEVICE-001 · SC-015

---

## SCR-021 / 포인트·쿠폰 적립

**회의 반영:**

- Week 5 MVP **제외** — 멤버십/쿠폰 9주 후반 확장
- SCR-007 결제 화면 내 모달·패널 또는 하위 단계
- 적립 확인 **1회만** (결제 전후 이중 확인 금지)

**Figma 참고:**

- [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) → `SCR-021 / 멤버십`
- [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) — loyalty overlay 참고

**프랜차이즈 패턴:** 스타벅스·공차 — 스탬프/쿠폰 스캔·적립 확인

**Trend:** **Trend-5** navy + yellow accent

**Wireframe:**

```jsx
┌────────────────────┐
│ ←       결제        │
│ 결제금액 ₩12,000    │
│ [📱 쿠폰 스캔]       │
│ 스탬프 1개 적립 예정  │
│ [적립하기][건너뛰기]  │
│ [가상 결제 승인]     │
└────────────────────┘
```

**CTA / Copy tone:** **「적립하기」** · **「쿠폰 스캔」** · **「가상 결제 승인」**

**REQ / SC:** LMIS-MEMBER-001, KSD-MEMBER-001, RTOS-DEVICE-002 · SC-006, SC-016

---

## 공통 체크리스트

- [ ]  Frame **834×1194**, safe area 가이드
- [ ]  Touch ≥ **48×48px** · CTA **하단 thumb zone**
- [ ]  회의 팔레트 `#16A34A` / `#FACC15` / `#FFFDF3` Variables 연결
- [ ]  메뉴 사진 `/assets/menu/{id}.png`
- [ ]  frame 이름 `SCR-XXX / 화면명` · URL → `figma-links.template.json`
- [ ]  DS QA → [Design Systems Checklist](https://www.figma.com/community/file/1152167555200057574/design-systems-checklist)
