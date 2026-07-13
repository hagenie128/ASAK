# Figma 가이드 + SCR×Figma 매트릭스

<aside>
✅

**2026-07-06 회의 반영** — SCR-002→001「홈 (매장·포장)」· SCR-006→005「장바구니·주문확인」병합. 고객 UI **6단계**. 프로덕션 DS **DS-02**.

</aside>

<aside>
⚠️

**무료 플랜: 페이지 최대 3개** — Figma Free는 파일당 Page 3개 한도. Notion 유료 권장 7페이지(00 Cover · 01 Design System · 02 User Flow · 03 Kiosk · 04 Admin · 05 Prototype · 06 Archive)는 아래 **3페이지로 통합**합니다.

| Page | SCR | 통합 내용 |
| --- | --- | --- |
| **02. User Flow** | — | 표지·팀 정보, DS 토큰 요약, 고객·관리자 흐름 다이어그램, 프로토타입 링크, Archive 참고 |
| **03. Kiosk Screens** | SCR-001~014, 020~021 | 키오스크 화면 프레임 |
| **04. Admin Screens** | SCR-015~019 | 관리자 화면 프레임 |

플러그인 `docs/design/figma-rename-scr-plugin/` — **3페이지만 생성**, SCR 프레임은 Kiosk/Admin으로 이동. 유료 플랜 전환 시 00·01·05·06 분리 가능.

</aside>

<aside>
✅

**Figma frame 링크 동기화 (2026-07-06)** — `FIGMA_TOKEN` + `sync_figma_links.py --all`로 `figma-links.template.json` · Notion SCR DB `Figma 링크` · DevCopilot 반영. Page 구조는 **무료 플랜 3페이지**(02 User Flow · 03 Kiosk · 04 Admin).

팀 파일: [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) · frame 이름: `SCR-XXX 화면명` · 플러그인: `docs/design/figma-rename-scr-plugin/`

</aside>

<aside>
📌

**이 페이지의 역할** — SCR×Figma **매트릭스·체크리스트·팀 규칙**. 파일 셋업 레시피는 [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md) · wireframe은 [SCR 화면별 가이드](SCR%20%ED%99%94%EB%A9%B4%EB%B3%84%20%EA%B0%80%EC%9D%B4%EB%93%9C%20(%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C).md) · 화면 목록 정본은 [04. 화면 설계 SCR DB](../../04%20%ED%99%94%EB%A9%B4%20%EC%84%A4%EA%B3%84.md)

</aside>

<aside>
🔗

**Git 로컬 도구** (정본 아님)

- GitHub: [https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md](https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md)
- [figma-links.template.json](https://github.com/hagenie128/ASAK/blob/main/docs/design/figma-links.template.json)
</aside>

---

> 팀 Figma **kiosk_design** · 태블릿 세로(portrait) · SCR-001~021 frame 템플릿
>

---

## 팀 정본 Figma

| 항목 | 값 |
| --- | --- |
| **파일명** | `kiosk_design` |
| **file key** | `iqaoVwFjFE6Zq1WpOVgjeG` |
| **URL** | [kiosk_design (팀 Figma)](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) |
| **형태** | 태블릿 **세로형** portrait |
| **Frame** | **834 × 1194** (primary) · 768 × 1024 (fallback) |

셋업 레시피: [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md)

SCR wireframe: [SCR 화면별 가이드](SCR%20%ED%99%94%EB%A9%B4%EB%B3%84%20%EA%B0%80%EC%9D%B4%EB%93%9C%20(%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C).md)

### 회의 컨셉

[2026.07.03 회의록](../../10%20%ED%9A%8C%EC%9D%98%EB%A1%9D/%ED%9A%8C%EC%9D%98%EB%A1%9D%20%EB%AA%A9%EB%A1%9D/2026%2007%2003.md) · 상세 팔레트·Trend → [브랜드 · Trend 컬러](%EB%B8%8C%EB%9E%9C%EB%93%9C%20%C2%B7%20Trend%20%EC%BB%AC%EB%9F%AC.md)

### Figma × SCR × 회의 매트릭스

| SCR | 회의 MVP | 팀 kiosk_design | Community / KIT | 프랜차이즈 패턴 |
| --- | --- | --- | --- | --- |
| 001 홈 (매장·포장) | ✅ | 03. Kiosk Screens | [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype), [Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) | 맥도날드 CTA + 매장/포장 |
| 002 유형 | **병합됨→001** | Archive | Kiosk Prototype | 맥도날드·써브웨이 분기 (홈 통합) |
| 003 메뉴 | ✅ photo-first | 03. Kiosk Screens | Kiosk Prototype, [Courses 14-410](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) card | 버거킹·샐러디 grid |
| 004 옵션 | ✅ 3단 트리 | 03. Kiosk Screens | Kiosk Prototype | 공차·써브웨이·샐러디 |
| 005 장바구니·주문확인 | ✅ 컨펌 팝업 | 03. Kiosk Screens | Kiosk Prototype | 맥도날드·스타벅스 |
| 006 확인 | **병합됨→005** | Archive | Kiosk Prototype | 스타벅스 confirm (팝업) |
| 007 결제 | ✅ 가상결제 | 03. Kiosk Screens | Kiosk Prototype | 맥도날드 pay |
| 008 완료 | ✅ 주문번호 | 03. Kiosk Screens | Case Study | 스타벅스 pickup |
| 009~011 Admin | ✅ Week 6 | 03. Kiosk Screens | Courses 14-410 | 표·상태 (회의) |
| 012 결제실패 | 최소 | 03. Kiosk Screens | Kiosk Prototype | — |
| 013~014 | 후반 | 03. Kiosk Screens | Case Study, [Moja UI](https://www.figma.com/community/file/1108679668074690379/moja-ui-ultimate-ui-kit-design-system-variables-darkmode) | — |
| 015~019 Admin | 보류 | 04. Admin Screens | Courses 14-410 | — |
| 020 영수증 | 후반 | 03. Kiosk Screens | Case Study | 맥도날드 영수증 선택 |
| 021 멤버십 | 후반 | 03. Kiosk Screens | Kiosk Prototype | 스타벅스 스탬프 |
| DS 전체 | Variables | 02. User Flow | [Moja UI](https://www.figma.com/community/file/1108679668074690379/moja-ui-ultimate-ui-kit-design-system-variables-darkmode), [DS Checklist](https://www.figma.com/community/file/1152167555200057574/design-systems-checklist) | — |

### Page 구조 (무료 플랜 3페이지)

| Page | SCR | 내용 |
| --- | --- | --- |
| **02. User Flow** | — | Cover·DS·흐름·Prototype·Archive 통합 |
| **03. Kiosk Screens** | 001~014, 020~021 | 키오스크 화면 |
| **04. Admin Screens** | 015~019 | 관리자 화면 |

> 상세 셋업·**페이지별 안에서 만들 것** 체크리스트 → [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md) · 유료 시 00~06 분리 가능
>

---

## 링크 템플릿

Frame 선택 → **Copy link**:

```
https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id={nodeId}
```

| 변수 | 값 |
| --- | --- |
| `{nodeId}` | Copy link의 `node-id` (예: `12-345`) |

→ `figma-links.template.json`의 `screens[].figma_url` / `node_id`에 저장

---

## 화면별 체크리스트

상태: `WIREFRAME` | `DESIGNING` | `CODING`

| SCR ID | 화면명 | Page | Figma frame | 상태 |
| --- | --- | --- | --- | --- |
| SCR-001 | 홈 (매장·포장) | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-002 | 【병합됨→SCR-001】먹고가기 / 포장 선택 | 03. Kiosk Screens (Archive) | *(레거시·Archive)* | **병합됨** |
| SCR-003 | 메뉴 선택 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-004 | 메뉴 상세 / 옵션 선택 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-005 | 장바구니·주문확인 (컨펌 팝업) | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-006 | 【병합됨→SCR-005】주문 확인 | 03. Kiosk Screens (Archive) | *(레거시·Archive)* | **병합됨** |
| SCR-007 | 결제 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-008 | 주문 완료 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-009 | 관리자 주문 관리 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-010 | 관리자 주문 상세 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-011 | 관리자 판매 항목 품절 관리 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-012 | 결제 실패 / 재시도 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-013 | 타임아웃 안내 / 자동 초기화 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-014 | 접근성 설정 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-015 | 관리자 로그인 | 04. Admin Screens | *(팀 입력)* | WIREFRAME |
| SCR-016 | 관리자 메뉴 관리 | 04. Admin Screens | *(팀 입력)* | WIREFRAME |
| SCR-017 | 관리자 메뉴 등록/수정 | 04. Admin Screens | *(팀 입력)* | WIREFRAME |
| SCR-018 | 관리자 결제수단 설정 | 04. Admin Screens | *(팀 입력)* | WIREFRAME |
| SCR-019 | 관리자 매출 요약 | 04. Admin Screens | *(팀 입력)* | WIREFRAME |
| SCR-020 | 영수증 출력 여부 선택 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |
| SCR-021 | 포인트·쿠폰 적립 | 03. Kiosk Screens | *(팀 입력)* | WIREFRAME |

상세: [https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md](https://github.com/hagenie128/ASAK/blob/main/docs/design/SCR_FIGMA_CHECKLIST.md) (Git 로컬 작업표)

---

## 참고 자료 (Community · kiosk_design 내 참고)

| # | 링크 | 용도 |
| --- | --- | --- |
| 1 | [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) | flow — Duplicate to this file (선택) |
| 2 | [Kiosk UI/UX Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) | 세로 UX 패턴 |
| 3 | [Moja UI + Variables + Dark Mode](https://www.figma.com/community/file/1108679668074690379/moja-ui-ultimate-ui-kit-design-system-variables-darkmode) | DS Variables |
| 4 | [Design Systems Checklist](https://www.figma.com/community/file/1152167555200057574/design-systems-checklist) | DS QA |
| 5 | [Courses Dashboard UI KIT](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) | Admin UI · node 14-410 |

브랜드 컬러·UI 패턴: [브랜드 · Trend 컬러](%EB%B8%8C%EB%9E%9C%EB%93%9C%20%C2%B7%20Trend%20%EC%BB%AC%EB%9F%AC.md) · 스와치 [color-swatches.html](https://github.com/hagenie128/ASAK/blob/main/docs/design/color-swatches.html)

ASAK Trend-1~5 오리지널 팔레트 (프로티너 등 타 브랜드 색상 복제 금지, mood 참고만)

> Community frame은 참고용. SCR frame은 **834×1194 portrait**로 새로 생성.
>

---

## DevCopilot Screens

| 방식 | 설명 |
| --- | --- |
| **localStorage** | `ws_2_screens` — 공용 PC마다 import |
| **Wiki (권장)** | 서버 공유 — [Wiki id=5](https://devcopilot.ai.kr/workspace/2/wiki/5) |

→ [DevCopilot/Wiki 업로드](%ED%99%94%EB%A9%B4%EC%84%A4%EA%B3%84%20DevCopilot%20Wiki%20%EC%97%85%EB%A1%9C%EB%93%9C.md)

---

## 팀 규칙

1. **디자인** → `kiosk_design` 파일 내 세로 Page·Frame (별도 파일 X)
2. **SCR·REQ** → Notion [04. 화면 설계](../../04%20%ED%99%94%EB%A9%B4%20%EC%84%A4%EA%B3%84.md)
3. **DevCopilot** → Wiki id=5 + Screens `figmaUrl`
4. frame 링크 → `figma-links.template.json` → Notion DB Figma URL
5. Week 5 MVP: **SCR-001~011** (+ SCR-012 최소)

---

## 관련 페이지

| 항목 | 링크 |
| --- | --- |
| Figma 셋업 | [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md) |
| SCR wireframe | [SCR 화면별 가이드](SCR%20%ED%99%94%EB%A9%B4%EB%B3%84%20%EA%B0%80%EC%9D%B4%EB%93%9C%20(%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C).md) |
| 브랜드·Trend | [브랜드 · Trend 컬러](%EB%B8%8C%EB%9E%9C%EB%93%9C%20%C2%B7%20Trend%20%EC%BB%AC%EB%9F%AC.md) |
| DevCopilot 업로드 | [Wiki 업로드 가이드](%ED%99%94%EB%A9%B4%EC%84%A4%EA%B3%84%20DevCopilot%20Wiki%20%EC%97%85%EB%A1%9C%EB%93%9C.md) |