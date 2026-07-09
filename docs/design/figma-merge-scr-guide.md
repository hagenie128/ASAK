# Figma SCR 병합 가이드 — 002→001 · 006→005

> **근거**: [screen-design-changes-2026-07-06.md](./meetings/screen-design-changes-2026-07-06.md)  
> **파일**: [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design)  
> **DS**: **DS-02 Modern Minimal** (`docs/design/figma-create-ds02-components-plugin/`)  
> **사전 작업**: `figma-rename-scr-plugin` 실행 → 프레임 이름 `SCR-XXX` 형식 정리

## 고객 UI 6단계 (병합 후)

| 순서 | SCR | 화면명 | 비고 |
|:--:|-----|--------|------|
| 1 | SCR-001 | 홈 (매장·포장) | SCR-002 흡수 |
| 2 | SCR-003 | 메뉴 선택 | |
| 3 | SCR-004 | 메뉴 상세 / 옵션 선택 | |
| 4 | SCR-005 | 장바구니·주문확인 | SCR-006 흡수 · 컨펌 팝업 |
| 5 | SCR-007 | 결제 | 로딩 필수 |
| 6 | SCR-008 | 주문 완료 | |

SCR-002·006 ID는 **병합됨** 표기로 Archive에만 유지 (참조·링크 호환).

---

## 준비

1. Figma Desktop에서 `kiosk_design` 열기
2. **Plugins → Development → Import** → `docs/design/figma-create-ds02-components-plugin/manifest.json`
3. **02. User Flow** 페이지에 **Create DS-02 User Flow Components** 실행 → `DS-02 · Component Library` 생성
4. **Plugins → Import** → `docs/design/figma-rename-scr-plugin/manifest.json` → 실행 (병합됨 프레임은 자동 스킵)

---

## A. SCR-002 → SCR-001 (홈에 매장·포장 통합)

### 목표

`SCR-001 홈 (매장·포장)` 한 프레임에 브랜드·주문 시작 CTA·**먹고가기/포장** 선택(`OrderTypeTile`)을 배치.

### 단계

1. **03. Kiosk Screens**에서 `SCR-001 홈 (매장·포장)` 프레임 선택 (834×1194)
2. `SCR-002` / `먹고가기/포장 선택` 프레임 내용 참고:
   - `DS-02 / OrderTypeTile` 인스턴스 2개 (DineIn Default · TakeOut Default)를 SCR-001 하단에 배치
   - `DS-02 / TopBar` variant **Home** 상단 고정
   - `DS-02 / Button` Primary — 「주문 시작」또는 타일 선택 후 메뉴로 진행
3. SCR-001에 **orderType** 상태 주석 레이어 추가 (DevCopilot 연동용):
   - `orderType: EAT_IN | TAKE_OUT`
4. 프로토타입 연결: OrderTypeTile 선택 → `SCR-003 메뉴 선택`
5. `SCR-002` 프레임:
   - 이름을 `SCR-002 먹고가기 / 포장 선택 [병합됨→001]`로 변경 (플러그인 자동 가능)
   - **02. User Flow** 하단 Archive 섹션으로 이동 (또는 숨김)
6. SCR-001만 `figma-links.template.json` · Notion SCR DB **Figma 링크** 정본으로 유지

### DS-02 컴포넌트

| 컴포넌트 | 용도 |
|----------|------|
| `DS-02 / TopBar` Home | 상단 브랜드·홈 |
| `DS-02 / OrderTypeTile` | 매장/포장 2타일 |
| `DS-02 / Button` Primary | CTA |
| `DS-02 / Typography` Display·H1 | 브랜드 카피 |

---

## B. SCR-006 → SCR-005 (장바구니·컨펌 팝업 통합)

### 목표

`SCR-005 장바구니·주문확인` 본문 + **주문 확인 컨펌 팝업**(`ModalConfirm`)을 한 화면 흐름으로 설계.

### 단계

1. **03. Kiosk Screens**에서 `SCR-005 장바구니·주문확인` 프레임 선택
2. 본문 구성:
   - `DS-02 / TopBar` Cart
   - `DS-02 / CartLine` × N
   - `DS-02 / BottomBar` Confirm — 「주문하기」
3. 컨펌 팝업 (SCR-006 기능 흡수):
   - `DS-02 / ModalConfirm` Default 오버레이 추가 (초기 hidden 또는 별도 variant 프레임)
   - 팝업 문구: 최종 금액·orderType·제외 재료 요약
   - Primary: 「결제하기」→ API-005 주문 생성 후 `SCR-007`
   - Ghost: 「돌아가기」→ 팝업 닫기
4. `SCR-006` 프레임:
   - 이름 `SCR-006 주문 확인 [병합됨→005]`
   - Archive로 이동
5. 프로토타입: BottomBar Confirm 탭 → ModalConfirm 표시 → Confirm → SCR-007

### DS-02 컴포넌트

| 컴포넌트 | 용도 |
|----------|------|
| `DS-02 / CartLine` | 담은 메뉴 행 |
| `DS-02 / BottomBar` Confirm | 하단 CTA |
| `DS-02 / ModalConfirm` | 주문 최종 확인 팝업 |
| `DS-02 / Stepper` | 수량 조절 |
| `DS-02 / ProgressStep` | 6단계 중 4단계 표시 (선택) |

---

## C. Archive · 정리

1. **02. User Flow**에 「Archive · 병합됨」라벨 프레임 생성
2. `SCR-002 [병합됨→001]`, `SCR-006 [병합됨→005]`를 그 안에 배치 (프로토타입 연결 제거)
3. `figma-rename-scr-plugin` 재실행 — 병합됨/Archive 프레임은 이동·이름변경 스킵
4. 링크 동기화 (로컬):

```bash
set FIGMA_TOKEN=figd_...
python asak-data/scripts/sync_figma_links.py --all
```

5. Notion [Figma SCR×매트릭스](https://app.notion.com/p/39451ef04f0b81849dc7d81f8106b5ad) · [SCR DB](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8) 확인

---

## 검증 체크리스트

- [ ] 고객 프로토타입이 **6 UI 단계**만 거침 (002·006 별도 화면 없음)
- [ ] SCR-001에 OrderTypeTile 동작
- [ ] SCR-005에서 ModalConfirm으로 주문 확정
- [ ] SCR-002·006은 Archive·**병합됨** 표기
- [ ] 활성 프레임에 DS-02 컴포넌트 인스턴스 적용
- [ ] `sync_figma_links.py` 후 Git·Notion 링크 일치

---

## 관련 문서

- [SCR_FIGMA_CHECKLIST.md](./SCR_FIGMA_CHECKLIST.md)
- [figma-rename-scr-plugin](./figma-rename-scr-plugin/)
- [figma-create-ds02-components-plugin](./figma-create-ds02-components-plugin/)
- [notion-merge-sync-audit-2026-07-06.md](../team/notion-merge-sync-audit-2026-07-06.md)
