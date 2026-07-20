> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Historical component migration mapping.
> Canonical Replacement: `docs/design/kiosk-design-system.md`
> Original Path: `docs/design/y2k-to-ds02-migration.md`

# Y2K UI Kit → ASAK Salady DS-02 매핑

Figma **Y2K UI Kit** Android XML 섹션을 **ASAK Salady DS-02** (`#1A1C20` charcoal + `#C8F135` electric lime) 컴포넌트로 재구성할 때의 대응표입니다.

| # | Y2K 섹션 (XML) | DS-02 UI Kit 섹션 프레임 | DS-02 컴포넌트 / Variant Set | 비고 |
|---|----------------|--------------------------|-------------------------------|------|
| 1 | `buttons` | Buttons | `DS-02 / Kit / ButtonRow` · `DS-02 / Button` | 한국어: 확인, 취소, 메뉴, 장바구니 |
| 2 | `segmented_c` | Segmented Control | `DS-02 / SegmentedControl` · `DS-02 / CategoryTab` | 전체 / 샐러드 / 음료 |
| 3 | `starring` | Rating / Stars | `DS-02 / Kit / Rating` | 3·4·5성 variant |
| 4 | `notificatio` | Notifications | `DS-02 / Kit / Notification` | Info / Success / Alert |
| 5 | `badge` | Badge | `DS-02 / Badge` · `DS-02 / QuantityBadge` | HOT, NEW, 품절, 알레르기 |
| 6 | `toggle` | Toggle | `DS-02 / Kit / Toggle` | ON / OFF · 44px 터치 |
| 7 | `text_field` | Text Field | `DS-02 / Kit / TextField` | Empty / Filled / Error |
| 8 | `combobox` | Combobox | `DS-02 / Kit / Combobox` | 매장 선택 드롭다운 |
| 9 | `menu` | Menu | `DS-02 / Kit / MenuDropdown` · `DS-02 / Chip` | 접힘 / 펼침 |
| 10 | `modal` | Modal | `DS-02 / ModalConfirm` · `DS-02 / ModalAlert` | 확인·취소 / 알림 |
| 11 | `card` | Card | `DS-02 / MenuCard` · `DS-02 / UpsellCard` · `DS-02 / OrderCompleteCard` | 메뉴·업셀·완료 |
| 12 | `search` | Search | `DS-02 / SearchBar` · `DS-02 / EmptyState` | Empty / Filled / Focused |
| 13 | `icons` | Icons | `DS-02 / Kit / Icon / *` (5종) | Home, Menu, Cart, Search, Check |
| 14 | `typography` | Typography | `DS-02 / Kit / TypographyRow` · `DS-02 / Typography` | Display~Caption |
| 15 | `shadows` | Shadows | `DS-02 / Kit / Shadow` | Elevation 1–4 |
| 16 | `colour_pale` | Colour Palette | `DS-02 / Kit / ColorSwatch` | **DS-02 semantic only** (핑크·레인보우 제외) |
| 17 | `icon_button` | Icon Button | `DS-02 / IconButton` | Default / Accent / Ghost × M/S |
| 18 | `tooltip` | Tooltip | `DS-02 / Kit / Tooltip` | Top / Bottom / Left / Right |
| 19 | `progress_ba` | Progress Bar | `DS-02 / Kit / OrderFlowProgress` · `DS-02 / ProgressStep` · `DS-02 / LoadingOverlay` | **5단계 주문 플로우** 포함 |
| 20 | `volume_bar` | Volume Bar | `DS-02 / Kit / Slider` | 25% / 50% / 75% |
| 21 | `toaster` | Toaster | `DS-02 / Toast` | Success / Error / Info / Warning |
| 22 | `radio_check` | Radio + Checkboxes | `DS-02 / OptionRadio` · `DS-02 / OptionCheckbox` | 옵션 선택 |
| 23 | `nav_bar` | Nav Bar | `DS-02 / TopBar` · `DS-02 / BottomBar` | 홈~결제 / CTA 바 |
| 24 | `section_tit` | Section Titles | `DS-02 / SectionHeader` · `DS-02 / Divider` | 링크형 헤더 |

## 디자인 토큰 (Y2K → DS-02 치환)

| Y2K 스타일 | DS-02 대체 |
|------------|------------|
| 핑크·퍼플·레인보우 그라데이션 | `#1A1C20` + `#C8F135` 단색·muted `#E8F5A0` |
| 초소형 radius | `radius-sm` 12px · `radius-md` 16px · pill 999 |
| 장식용 별·하트 아이콘 | 키오스크 기능 아이콘 (메뉴·장바구니·결제) |
| 32px 이하 터치 | **최소 44×44px** (`MIN_TOUCH`) |
| 영문 placeholder | 한국어: 확인, 취소, 메뉴, 장바구니 등 |

## Figma 출력

| 항목 | 값 |
|------|-----|
| 페이지 | `02. User Flow` |
| 마스터 프레임 | **ASAK Salady · DS-02 UI Kit** |
| 플러그인 | `docs/design/figma-create-ds02-components-plugin/` |
| 진입점 | `buildY2KStyleFullKit()` · 명령 `fullkit` |

## 관련 문서

- [figma-create-ds02-components-plugin README](../tools-plugins/figma-create-ds02-components-plugin/README.md)
- [kiosk-design-system-candidate-B.md](./kiosk-design-system-candidate-B.md)
