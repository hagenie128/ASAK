# Primitive Components

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `BADGE_AND_CHIP.md`
- `BUTTON.md`
- `FORM_CONTROLS.md`
- `SPINNER_AND_DIVIDER.md`

---

## 원문: `BADGE_AND_CHIP.md`

### Badge and Chip

#### Badge

상태를 표현한다.

예:

```text
품절
준비중
완료
실패
BEST
NEW
```

#### Chip

필터·선택을 표현한다.

예:

```text
전체
샐러드
랩
음료
```

#### 차이

- Badge = 정보 전달
- Chip = 선택 또는 필터

같은 스타일로 만들지 않는다.

#### Accessibility

색상 외 텍스트와 shape 차이 사용.

---

## 원문: `BUTTON.md`

### Button

#### Tier / Owner

- Tier: Primitive
- Owner: Shared

#### Purpose

사용자의 명시적 행동을 실행한다.

#### Variants

```text
primary
secondary
danger
ghost
```

#### States

```text
default
hover
pressed
focus
disabled
loading
```

#### Props

```js
{
  type,
  variant,
  size,
  disabled,
  loading,
  icon,
  children,
  onClick,
  ariaLabel
}
```

#### Rules

- loading 중 중복 클릭 금지
- disabled 이유가 필요한 경우 주변 문구 제공
- icon-only는 aria-label 필수
- Kiosk 최소 터치 영역 80×80px

#### Do Not

- `<div onClick>`로 구현하지 않는다.
- 화면마다 새로운 button style을 만들지 않는다.

---

## 원문: `FORM_CONTROLS.md`

### Form Controls

#### Includes

- Input
- SearchInput
- Checkbox
- Radio
- Switch
- Select

#### Rules

- label 필수
- error message 연결
- placeholder는 label 대체 불가
- Switch는 즉시 반영 여부 명확히
- Checkbox는 다중 선택
- Radio는 단일 선택

#### Admin Use

- IngredientSelectModal
- Login
- MenuForm
- FilterBar
- Payment settings

---

## 원문: `SPINNER_AND_DIVIDER.md`

### Spinner and Divider

#### Spinner

- loading 상태 표현
- 버튼 내부 또는 page state
- 300ms 미만 요청에는 깜빡임 방지를 검토

#### Divider

- 정보 그룹 구분
- 장식용 과다 사용 금지
- BottomCTA 상단 구분선에 사용 가능
