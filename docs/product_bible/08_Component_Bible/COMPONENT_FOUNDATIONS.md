# Component Foundations

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `COMPONENT_CREATION_RULES.md`
- `COMPONENT_SYSTEM.md`
- `TOKEN_CONNECTION_RULES.md`

---

## 원문: `COMPONENT_CREATION_RULES.md`

### Component Creation Rules

새 컴포넌트를 만들기 전 아래를 확인한다.

1. 기존 동일 역할 컴포넌트가 있는가?
2. props 확장으로 해결 가능한가?
3. variant 추가로 해결 가능한가?
4. Figma component set에 이미 존재하는가?
5. Kiosk/Admin 중 한쪽에 동일 역할이 있는가?
6. 단일 화면에서만 사용하는 markup인가?

#### 만들지 말아야 할 중복 예

```text
BottomCTA ↔ FooterButton ↔ PaymentFooter
MenuCard ↔ FoodCard ↔ ProductCard
StatusBadge ↔ StatusChip ↔ StateBadge
ConfirmDialog ↔ DeleteModal ↔ WarningPopup
SalesMetricCard ↔ KpiCard ↔ DashboardMetricCard
```

#### 기존 코드 보호

기존 팀원이 만든 컴포넌트가 있으면:

- 이름만 다르다고 새로 만들지 않는다.
- 먼저 props와 책임을 확인한다.
- 필요한 기능만 추가한다.
- 대규모 rename은 별도 승인 후 진행한다.

---

## 원문: `COMPONENT_SYSTEM.md`

### Component System

#### Tier

##### Tier 1 — Primitive

작은 UI 단위.

- Button
- IconButton
- Input
- Checkbox
- Radio
- Switch
- Badge
- Chip
- Divider
- Spinner

##### Tier 2 — Composite

Primitive 조합.

- BottomCTA
- MenuCard
- CartItemCard
- PaymentMethodCard
- OrderCard
- SalesMetricCard
- Toast
- ConfirmDialog
- FilterDropdown

##### Tier 3 — Section

화면의 의미 단위.

- CategoryTabs
- OrderSummary
- MenuGrid
- DashboardSummary
- OrderTable
- SalesChartSection
- MenuFormSection

##### Tier 4 — Screen

Route 단위.

- SCR-001~SCR-024

#### Dependency Rule

```text
Screen
→ Section
→ Composite
→ Primitive
```

반대 의존 금지.

Primitive가 특정 Screen을 import하지 않는다.

#### Ownership

```text
Shared
Kiosk
Admin
```

같은 역할의 컴포넌트를 Kiosk/Admin에 중복 생성하지 않는다.

---

## 원문: `TOKEN_CONNECTION_RULES.md`

### Token Connection Rules

#### Typography

- Font: Pretendard Variable
- Figma Text Style와 CSS token을 연결
- 임의 px 사용보다 token 우선

#### Color

권장 semantic token:

```text
colorBrandPrimary
colorBrandPrimaryPressed
colorSurfaceDefault
colorSurfaceSubtle
colorTextPrimary
colorTextSecondary
colorBorderDefault
colorSuccess
colorWarning
colorDanger
colorDisabled
```

#### Spacing

8px base grid.

```text
space1 = 8
space2 = 16
space3 = 24
space4 = 32
space5 = 40
space6 = 48
space8 = 64
```

#### Radius

```text
radiusSm
radiusMd
radiusLg
radiusXl
radiusPill
```

#### Elevation

관리자 카드와 Modal에만 제한적으로 사용.

#### Motion

- 빠른 상태 전환: 120~160ms
- Modal/Drawer: 180~240ms
- 과도한 spring 금지
