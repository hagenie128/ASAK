# Kiosk/OptionCard — Component 설계 명세 (v2, 확정)

> 작성일: 2026-07-17 (v2 — 사용자 확정 사양 반영, D1-B 소관)
> 성격: **설계 명세서. 아직 Figma에 생성하지 않음.**
> 근거: `508:44937`(D1-A Visual Pilot, 최종 승인됨) 실측 + 사용자 확정 사양.
> 실행: 이 명세를 실제로 만드는 절차는 [ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md](ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md) 참고 — 그 문서도 아직 실행 전 단계.

---

## 1. Component 이름

`Kiosk/OptionCard`

기존 `Kiosk/OrderDetailRow`(장바구니/주문요약용, 용도 다름)와 `Kiosk/OptionSelectionRow`(세로 Row 구조, 이번 3열 카드 요구사항과 구조 불일치로 재사용하지 않기로 확정)는 그대로 둔다. 셋 다 서로 다른 용도의 별개 컴포넌트다.

## 2. Variant

| Variant 축 | 값 |
|---|---|
| `state` | `default` \| `selected` \| `disabled` \| `soldOut` |

- `pressed`는 이번 범위에 포함하지 않음 — 필요 시 별도 검토.
- `selectionType`(single/multiple/exclude 같은 축)은 **시각적 차이가 실제로 있을 때만** Variant로 추가한다. 현재 `508:44937`의 카드 46개를 확인한 결과, selectionType별 시각 차이가 카드 레벨에서는 나타나지 않았다(선택 여부는 `state=selected`만으로 표현됨) — 그러므로 기본안은 **`selectionType`을 Variant로 만들지 않는다.** 선택 개수 제한(단일/다중/제외) 로직은 `OptionGroup` 레벨의 `selectionRule` Property가 담당하고, 카드는 `state`만 반응한다.

## 3. Component Property

| Property Key(제안) | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `optionName` | TEXT | "옵션 이름" | 옵션명, 최대 2줄 |
| `secondaryText` | TEXT | "0g · 0kcal" | 중량·kcal 등 보조 정보. 하나의 텍스트로 통합(`508:44937`에서 검증된 "172g · 271kcal" 형태를 그대로 채택) |
| `additionalPrice` | TEXT | "+0원" | 추가 가격 |
| `showSecondaryText` | BOOLEAN | `true` | 보조 정보 표시 여부(제외 재료처럼 중량/kcal이 의미 없는 카테고리에서 숨김 가능 — `508:44937`의 제외 재료 카드도 `cardSecondary` 필드 자체가 없었음) |
| `showPrice` | BOOLEAN | `true` | 가격 표시 여부 |
| `soldOutLabel` | TEXT | "품절" | `state=soldOut`일 때만 노출되는 배지 문구 |

`selected` 여부와 활성/비활성/품절 여부는 전부 `state` Variant로 처리하고 별도 Boolean으로 중복 만들지 않는다.

## 4. 레이아웃

- 3열 Grid 기준 카드 폭 292px, 최소 높이 104px.
- 옵션명(`optionName`) 최대 2줄, 초과 시 말줄임.
- `secondaryText`와 `additionalPrice`가 `optionName` 영역을 침범하지 않도록 세로로 명확히 구획한다(이름 → 보조정보 → 가격 순서, `508:44937`의 `cardName`/`cardSecondary`/`priceRow` 배치를 그대로 따름).
- 가격 영역은 우측 정렬.
- **카드 전체가 Touch Target**(카드 어디를 눌러도 선택 동작) — 카드 내부에 별도로 분리된 작은 버튼을 두지 않는다.
- **Auto Layout 사용, 고정 좌표 기반 텍스트 배치 금지.** `508:44937`의 `OptionCard`는 자식 텍스트들이 `x`/`y` 고정 좌표로 배치돼 있었다(예: `cardName` x=16,y=16 / `cardSecondary` x=16,y=41.5 / `priceRow` x=16,y=67). 정식 Component에서는 이를 Auto Layout(세로 stack + 내부 패딩/gap)으로 바꿔서, 텍스트 길이가 달라져도 겹치거나 잘리지 않게 한다. 이것이 v1 지시서에서 발견했던 "고정 좌표라 실제 콘텐츠 길이를 못 견딘다"는 문제를 근본적으로 막는 조치다.
- 품절 배지(`soldOutBadge`)는 **절대 위치 오버레이**로 배치 — Auto Layout 흐름 안에 넣지 않는다. (`508:44937`에서 배지가 flow 안에 들어가 카드 높이를 초과해 이름 텍스트가 찌그러지는 버그가 실제로 발생했고, 절대 위치로 바꿔서 해결한 전례를 그대로 반영.)

## 5. 시각 상태 (State별 규칙)

| State | 배경/테두리 | 텍스트 | 배지 |
|---|---|---|---|
| `default` | White + Neutral Border | 기본 색상 | 없음 |
| `selected` | 연한 Lime Surface(`#F5FBE0` 톤) + Lime Border | 기본 색상 유지 | 없음 |
| `disabled` | 읽기 가능한 수준의 Neutral(흐림 처리하되 텍스트는 읽을 수 있어야 함) | 흐림 처리 | 없음 |
| `soldOut` | Dim 처리 | 흐림 처리 | 우측 상단 Red "품절" 배지(절대 위치) |

**금지**: Dark Fill, Blue Selected. (이 프로젝트에서 "Selected에 Blue 금지"는 CartItemCard 등에서 이미 여러 번 확인된 공통 잠금 규칙 — `Kiosk/OptionCard`에도 동일하게 적용.)

## 6. 검증 데이터 (Property/State 조합 테스트용)

| 이름 | 용도 |
|---|---|
| 양배추라이스 | 짧은 이름, 기본 |
| 곤약라이스 | 짧은 이름, 기본 |
| 허니머스타드 | 중간 길이 이름 |
| 트러플오일 | 중간 길이 이름 |
| 통밀또띠아 | 중간 길이 이름, 받침 포함 줄바꿈 확인 |
| 베이컨칩 | 품절 상태 테스트용 |

추가로 검증할 조합:
- 가격 있음 / 없음(`showPrice=false`)
- Secondary 있음 / 없음(`showSecondaryText=false`)
- 품절 상태(`state=soldOut`)

## 7. 다음 단계

실제 생성 절차, Sandbox 원칙, 바인딩 검증 절차, 마이그레이션 절차는 [ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md](ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md)에 정리했다. 이 명세 문서는 "무엇을 만들지"만 정의하며, "어떻게 안전하게 만들지"는 Work Order 문서의 소관이다.
