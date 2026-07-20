# Create DS-02 User Flow Components

`kiosk_design` Figma 파일 **`02. User Flow`** 페이지에 **DS-02 Modern Minimal** 키오스크 컴포넌트 라이브러리를 자동 생성하는 플러그인입니다.

| 항목 | 값 |
|------|-----|
| 플러그인 이름 | **Create DS-02 User Flow Components** |
| 경로 | `docs/design/figma-create-ds02-components-plugin/` |
| 대상 페이지 | **02. User Flow** |
| 출력 프레임 | **DS-02 · Component Library** · **ASAK Salady · DS-02 UI Kit** |
| 팔레트 | `#1A1C20` charcoal · `#C8F135` electric lime |
| 그리드 | Moja **8px** · radius **10/12/16px** · stroke **2px** |

> **모든 라이브러리 출력은 `figma.createComponent()` 단일 컴포넌트 또는 `combineAsVariants()` variant set입니다.** 일반 레이어/프레임은 라이브러리에 배치되지 않습니다.

---

## 설치 · 실행

1. Figma Desktop → **Plugins → Development → Import plugin from manifest…**
2. `docs/design/figma-create-ds02-components-plugin/manifest.json` 선택
3. `kiosk_design` 파일에서 플러그인 실행
   - **DS-02 컴포넌트 생성** — `DS-02 · Component Library` 프레임
   - **DS-02 UI Kit 생성** — `ASAK Salady · DS-02 UI Kit` 마스터 프레임 (Y2K 24섹션 → DS-02)
4. 기존 동일 이름 프레임이 있으면 삭제 후 재생성

### DS-02 UI Kit (Y2K → DS-02 전체 키트)

Y2K UI Kit Android XML 24섹션을 DS-02 charcoal + lime 스타일로 재구성합니다.

| 항목 | 값 |
|------|-----|
| 명령 | `fullkit` (relaunch: **DS-02 UI Kit 생성**) |
| 마스터 프레임 | **ASAK Salady · DS-02 UI Kit** |
| 섹션 수 | 25 (Buttons … Chip … Section Titles) |
| 컴포넌트 | 150+ (`figma.createComponent` / variant sets) |
| 매핑 문서 | [Archive migration mapping](../../archive/design-migrations/y2k-to-ds02-migration.md) |

```bash
# full_kit.js 변경 후 code.js에 번들
node docs/design/figma-create-ds02-components-plugin/bundle_plugin.js
node docs/design/figma-create-ds02-components-plugin/_test_mock.js
```

### Mock 테스트 (로컬)

```bash
python docs/design/figma-create-ds02-components-plugin/embed_kiosk_icons.py
node docs/design/figma-create-ds02-components-plugin/_test_mock.js
```

### 키오스크 아이콘 PNG 재생성

1. 새 4×4 아이콘 시트 PNG를 `assets/asak-kiosk-icons-4x4.png`에 덮어쓰기 (행·열 순서는 [Archive icon prompt](../../archive/design-prompts/kiosk-icon-pack-prompt.md) 및 위 `IconSheet` 표와 동일해야 함)
2. base64 주입:

```bash
python docs/design/figma-create-ds02-components-plugin/embed_kiosk_icons.py
```

3. Figma Desktop에서 플러그인 manifest **재 import** 후 `02. User Flow`에서 실행

> **이미지 embed 형식:** PNG → base64 ASCII `KIOSK_ICONS_B64` → `bytesFromBase64()` → `figma.createImage(Uint8Array)`. 4×4 시트 셀 크롭은 **`scaleMode: "CROP"`** + `imageTransform` `[[0.25,0,col×0.25],[0,0.25,row×0.25]]` (Figma API: `imageTransform`은 CROP/TILE에서만 적용 — `FILL`이면 전체 시트가 들어감).

---

## 컴포넌트 인벤토리

### Variant sets (26세트 · 117 variants)

| # | Component Set | Variants | SCR |
|---|---------------|----------|-----|
| 1 | `DS-02 / Typography` | 7 (Display, H1, H2, Body, BodyStrong, Caption, Button) | 전체 |
| 2 | `DS-02 / Button` | **30** (10 Style × 3 Size) — 아래 매트릭스 | 001, 005, 007, 012 |
| 3 | `DS-02 / IconButton` | 6 (Default/Accent/Ghost × M/S) | 003, 004, 005 |
| 4 | `DS-02 / Chip` | 3 (Default, Selected, Disabled) · 10px radius · 2px stroke | 003, 004 |
| 5 | `DS-02 / Badge` | 4 (HOT, NEW, SoldOut, Allergy) | 003, 004 |
| 6 | `DS-02 / TopBar` | 5 (Home, Menu, Detail, Cart, Payment) | 전체 |
| 7 | `DS-02 / BottomBar` | 3 (Cart, Confirm, Payment) | 005, 007 |
| 8 | `DS-02 / MenuCard` | 3 (Default, Selected, SoldOut) | 003 |
| 9 | `DS-02 / CartLine` | 2 (Default, Editing) | 005 |
| 10 | `DS-02 / OrderTypeTile` | 4 (DineIn/TakeOut × Default/Selected) | 001 |
| 11 | `DS-02 / OptionRadio` | 3 (Unselected, Selected, Disabled) | 004 |
| 12 | `DS-02 / OptionCheckbox` | 3 (Unselected, Selected, Disabled) | 004 |
| 13 | `DS-02 / Stepper` | 3 (1, 2, 5) | 004, 005 |
| 14 | `DS-02 / ModalConfirm` | 2 (Default, Destructive) | 005 |
| 15 | `DS-02 / Toast` | 4 (Success, Error, Info, Warning) | 012 |
| 16 | `DS-02 / LoadingOverlay` | 2 (Spinner, Progress) | 007 |
| 17 | `DS-02 / PaymentMethod` | 6 (Card/EasyPay/Cash × Default/Selected) | 007 |
| 18 | `DS-02 / SearchBar` | 3 (Empty, Filled, Focused) | 003 |
| 19 | `DS-02 / EmptyState` | 3 (NoMenu, NoCart, NoResult) | 003, 005 |
| 20 | `DS-02 / SectionHeader` | 2 (None, Link) | 004, 005 |
| 21 | `DS-02 / Divider` | 2 (Horizontal, Vertical) | 전체 |
| 22 | `DS-02 / ProgressStep` | 5 (Step 1–5) | 005, 007 |
| 23 | `DS-02 / SegmentedControl` | 3 (A/B/C selected) | 003, 014 |
| 24 | `DS-02 / Skeleton` | 3 (Text, Card, Row) | 003, 007 |
| 25 | `DS-02 / CategoryTab` | 3 (Active, Inactive, Disabled) | 003 |
| 26 | `DS-02 / QuantityBadge` | 3 (1, 9, 99+) | 005 |

#### `DS-02 / Button` 매트릭스 (Moja → DS-02)

| Moja | Style (variant) | Fill | Text | Stroke 2px | Size (h) | 샘플 라벨 |
|------|-----------------|------|------|------------|----------|-----------|
| `button_prim` | Primary | `#C8F135` | `#1A1C20` | — | L 56 / M 48 / S 40 | 확인 |
| — | Primary Disabled | `#C8F135` @40% | `#1A1C20` | — | 동일 | 확인 |
| `button_dark` | Dark | `#1A1C20` | white | — | 동일 | 결제하기 |
| `button_seco` | Secondary | `#F0F1ED` | `#1A1C20` | `#E5E7EB` | 동일 | 메뉴 담기 |
| `button_outl` | Outline | transparent | `#1A1C20` | `#1A1C20` | 동일 | 확인 |
| `button_outl` (dark) | Outline Dark | `#1A1C20` | white | `#C8F135` | 동일 | 결제하기 |
| `button_dang` | Danger | `#DC2626` | white | `#DC2626` | 동일 | 취소 |
| — | Danger Outline | transparent | `#DC2626` | `#DC2626` | 동일 | 취소 |
| `button_bord` | *(별도 variant 없음 — white + `#C8F135` stroke는 Outline 커스텀)* | white | `#1A1C20` | `#C8F135` | | 확인 |
| `button_whit` | Ghost | white | `#1A1C20` | `#E5E7EB` | 동일 | 장바구니 |
| — | Ghost Disabled | white @60% | muted | `#E5E7EB` | 동일 | 장바구니 |

- **cornerRadius:** `12px` (`radiusBtn`) — Moja middle radius (5↔24 사이)
- **strokeWeight:** `2px` (stroke 있는 스타일)
- Moja blue `#0354A6` **미사용**
- Doc 쇼케이스: `DS-02 · Doc / Buttons` (header 96h · footer 130h `#F0F1ED` · `doc_button` 패널 28px radius + shadow)

### 단일 컴포넌트 — 벡터 아이콘 (13개 · `Icon` 행)

시트 embed 후 Home·Cart·Back 벡터는 시트 컴포넌트와 중복되므로 생략됩니다.

| Component | 용도 | SCR |
|-----------|------|-----|
| `DS-02 / Icon / Search` | 검색 | 003 |
| `DS-02 / Icon / Plus` | 수량 증가 | 004, 005 |
| `DS-02 / Icon / Minus` | 수량 감소 | 004, 005 |
| `DS-02 / Icon / Check` | 선택 확인 | 004 |
| `DS-02 / Icon / Close` | 닫기 | 012 |
| `DS-02 / Icon / Menu` | 메뉴 | 003 |
| `DS-02 / Icon / DineIn` | 매장 식사 | 001 |
| `DS-02 / Icon / TakeOut` | 포장 | 001 |
| `DS-02 / Icon / Payment` | 결제 | 007 |
| `DS-02 / Icon / Success` | 성공 | 008 |
| `DS-02 / Icon / Error` | 오류 | 012 |
| `DS-02 / Icon / Info` | 정보 | 012 |
| `DS-02 / Icon / Warning` | 경고 | 012 |

### 단일 컴포넌트 — 카드·히어로 (5개)

| Component | 용도 | SCR |
|-----------|------|-----|
| `DS-02 / ModalAlert` | 일반 알림 모달 | 012 |
| `DS-02 / UpsellCard` | 장바구니 추가 제안 | 005 |
| `DS-02 / OrderCompleteCard` | 주문 완료 카드 | 008 |
| `DS-02 / PaymentFailCard` | 결제 실패 + 재시도 | 012 |
| `DS-02 / BrandHero` | 홈 브랜드 + CTA | 001 |

### 키오스크 아이콘 시트 (16개 · raster · `IconSheet` 행)

4×4 PNG 시트에서 잘라낸 **64×64** 투명 배경 컴포넌트. 벡터 `Icon` 행의 Home·Cart·Back과 이름이 겹치므로 시트 로드 시 벡터 3개는 생략됩니다.

| # | Component | 그리드 (col,row) | 용도 |
|---|-----------|------------------|------|
| 1 | `DS-02 / Icon / Home` | (0,0) | 홈·매장 시작 |
| 2 | `DS-02 / Icon / Takeout` | (1,0) | 먹고가기/포장 |
| 3 | `DS-02 / Icon / MenuGrid` | (2,0) | 메뉴 카테고리 |
| 4 | `DS-02 / Icon / Customize` | (3,0) | 옵션·커스터마이즈 |
| 5 | `DS-02 / Icon / SoldOut` | (0,1) | 품절 |
| 6 | `DS-02 / Icon / Cart` | (1,1) | 장바구니 |
| 7 | `DS-02 / Icon / OrderConfirm` | (2,1) | 주문 확인 |
| 8 | `DS-02 / Icon / CardPay` | (3,1) | 카드 결제 |
| 9 | `DS-02 / Icon / QRPay` | (0,2) | 모바일·QR 결제 |
| 10 | `DS-02 / Icon / Points` | (1,2) | 포인트·스탬프 |
| 11 | `DS-02 / Icon / Coupon` | (2,2) | 쿠폰 |
| 12 | `DS-02 / Icon / Complete` | (3,2) | 주문 완료 |
| 13 | `DS-02 / Icon / Receipt` | (0,3) | 영수증 출력 |
| 14 | `DS-02 / Icon / Accessibility` | (1,3) | 접근성 |
| 15 | `DS-02 / Icon / Language` | (2,3) | 언어 전환 |
| 16 | `DS-02 / Icon / Back` | (3,3) | 뒤로가기 |

### Magnific-style UI 아이콘 (20개 · 벡터 SVG · `IconUI` 행)

[Magnific uicon](https://www.magnific.com/search?format=search&iconType=uicon) 스타일에 맞춘 **두 번째 아이콘 행**입니다. Magnific 사이트는 로그인·구독·API 키(`x-magnific-api-key`) 없이는 벌크 SVG 다운로드가 불가하므로, 플러그인은 **Lucide Icons (MIT)** 경로를 `figma.createNodeFromSvg()`로 임포트합니다.

| Component | 용도 | 색상 |
|-----------|------|------|
| `DS-02 / Icon / UI / Home` | 홈 | accent `#C8F135` |
| `DS-02 / Icon / UI / Menu` | 메뉴 | charcoal `#1A1C20` |
| `DS-02 / Icon / UI / Cart` | 장바구니 | accent |
| `DS-02 / Icon / UI / Payment` | 결제 | accent |
| `DS-02 / Icon / UI / Settings` | 설정 | charcoal |
| `DS-02 / Icon / UI / User` | 사용자 | charcoal |
| `DS-02 / Icon / UI / Search` | 검색 | charcoal |
| `DS-02 / Icon / UI / Check` | 확인 | charcoal |
| `DS-02 / Icon / UI / Close` | 닫기 | charcoal |
| `DS-02 / Icon / UI / ArrowLeft` | 뒤로 | charcoal |
| `DS-02 / Icon / UI / Receipt` | 영수증 | charcoal |
| `DS-02 / Icon / UI / QR` | QR 결제 | charcoal |
| `DS-02 / Icon / UI / Coupon` | 쿠폰 | charcoal |
| `DS-02 / Icon / UI / Clock` | 대기·시간 | charcoal |
| `DS-02 / Icon / UI / Warning` | 경고 | charcoal |
| `DS-02 / Icon / UI / Plus` | 증가 | charcoal |
| `DS-02 / Icon / UI / Minus` | 감소 | charcoal |
| `DS-02 / Icon / UI / Trash` | 삭제 | charcoal |
| `DS-02 / Icon / UI / Edit` | 편집 | charcoal |
| `DS-02 / Icon / UI / Filter` | 필터 | charcoal |

각 컴포넌트는 **48×48** 프레임(흰 배경·12px radius) 안에 **24×24** SVG 벡터가 중앙 정렬됩니다.

> **법적 고지:** Magnific CDN 핫링크·무단 스크래핑은 하지 않습니다. 현재 아이콘은 Magnific-style **오픈소스 대체품**이며, Magnific 라이선스를 보유한 경우 아래 절차로 교체하세요.

#### Magnific 수동 교체 워크플로

1. [Magnific uicon 검색](https://www.magnific.com/search?format=search&iconType=uicon)에서 아이콘 선택 → **SVG 다운로드** (구독·라이선스 PDF 보관)
2. 또는 [Magnific Icons API](https://docs.magnific.com/api-reference/icons/icons-api) `GET /v1/icons/{id}/download?format=svg` + API 키
3. Figma에서 해당 `DS-02 / Icon / UI / …` 컴포넌트를 열고 SVG 레이어를 **Paste as SVG** 또는 드래그로 교체
4. (선택) `code.js`의 `MAGNIFIC_UI_ICON_SPECS[].inner`에 SVG `<path>` 내용을 붙여넣고 플러그인 재실행

### 합계

| 지표 | 수량 |
|------|------|
| Variant sets | **26** |
| Variant instances | **117** |
| 단일 components | **54** (벡터 13 + 시트 16 + UI SVG 20 + 카드 5) |
| **총 component nodes** | **171** |

---

## SCR 커버리지

| SCR | 화면 | 사용 컴포넌트 |
|-----|------|---------------|
| **001** | 홈 (매장·포장) | BrandHero, OrderTypeTile, Button/Primary, Typography/Display |
| **003** | 메뉴 선택 | TopBar/Menu, MenuCard, CategoryTab, Chip, SearchBar, Badge, Skeleton |
| **004** | 메뉴 상세·옵션 | TopBar/Detail, OptionRadio, OptionCheckbox, Stepper, SectionHeader, Badge |
| **005** | 장바구니·주문확인 | TopBar/Cart, CartLine, BottomBar, ModalConfirm, UpsellCard, ProgressStep |
| **007** | 결제 | TopBar/Payment, PaymentMethod, LoadingOverlay, BottomBar/Payment |
| **008** | 주문 완료 | OrderCompleteCard, Typography/Display, Icon/Success |
| **012** | 결제 실패 | PaymentFailCard, Toast/Error, ModalAlert, Button/Danger |

---

## 디자인 토큰

| 토큰 | 값 |
|------|-----|
| `color-primary` | `#1A1C20` |
| `color-accent` | `#C8F135` |
| `color-accent-muted` | `#E8F5A0` |
| `color-background` | `#F0F1ED` |
| `color-surface` | `#FFFFFF` |
| `color-text-muted` | `#6B7280` |
| `color-error` | `#DC2626` |
| `radius-btn` | **12px** (키오스크 버튼) |
| `radius-doc` | **28px** (doc 패널) |
| `radius-sm/md/lg` | 10 / 12 / 16px (chip·input / button·card / modal) |
| `stroke` | 2px · `#E5E7EB` default · `#1A1C20` or `#C8F135` accent |
| Touch min | 44×44px |
| Grid | 8px |

정본: [kiosk-design-system.md](../kiosk-design-system.md)

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `get_width: The node with id … does not exist` (`layoutComponentLibrary`) | `combineAsVariants` 후 임시 프레임 `parent.remove()`가 variant set까지 함께 삭제되어 `items`에 stale 노드 참조가 남음 | **v2026-07-06** 이후 `code.js` 사용 — set을 `currentPage`로 이동한 뒤 temp frame 제거. 플러그인 **재 import** 후 다시 실행 |
| 라이브러리 프레임이 비어 있거나 일부 카테고리만 표시 | 위 오류로 layout 중단, 또는 개별 노드 접근 실패 | Figma Desktop에서 플러그인 manifest 재 import → `02. User Flow` 페이지에서 실행. 기존 `DS-02 · Component Library` 프레임은 자동 삭제됨 |
| Mock 테스트 실패 | 로컬 Node 버전 또는 `code.js` 미반영 | `node docs/design/figma-create-ds02-components-plugin/_test_mock.js` 재실행 |
| IconSheet 64×64에 4×4 시트 전체가 보임 | `scaleMode: "FILL"` — `imageTransform` 무시됨 | **v2026-07-06** 이후 `code.js` (`CROP` + 양수 tx/ty). manifest **재 import** 후 재실행 |

---

## 관련 플러그인

- [figma-rename-scr-plugin](../figma-rename-scr-plugin/) — SCR 프레임 이름 정리
- [figma-apply-ds02-theme-plugin](../figma-apply-ds02-theme-plugin/) — 기존 프레임 DS-02 테마 적용
- [Figma 플러그인 안내](../FIGMA_PLUGINS.md)
