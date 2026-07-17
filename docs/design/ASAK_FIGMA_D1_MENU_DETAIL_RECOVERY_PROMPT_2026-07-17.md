# D1 — Menu Detail Default 구조 복구 지시서 (v3, 3열 Card Grid 확정)

> 작성일: 2026-07-17 (v3 — 3열 Option Card Grid로 방향 확정, 세로 목록 지시 폐기)
> 대상 파일: [ASAK Figma](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715)
> 성격: 계획 문서. 이 갱신 자체는 Figma에 어떤 실행도 포함하지 않음.
> 실행 상태: `508:44937`은 **Visual Reference Pilot**로 유지(시각 기준 참고용). 그 안의 `OptionCard`(일반 Frame 46개)는 **Production 정본으로 인정하지 않음.** Production `134:7810`은 이 문서 갱신 이후에도 여전히 무변경 상태를 유지해야 하며, 실제 반영은 별도 승인 후에만 진행한다.

## D1-A 승인 상태

**D1-A Visual Pilot (`508:44937`) — 2026-07-17 최종 승인.** 3열 Card Grid 구조, Header/BottomCTA 고정, 46개 옵션, 필수/선택 배지(베이스만 필수, 나머지 6개 선택) 전부 QA 재검증 완료 후 승인. 승인 범위는 **시각 기준(Visual Reference)에 한정** — `508:44937` 내부의 일반 Frame `OptionCard`는 여전히 Production 정본이 아니며, 정식 Component化는 D1-B로 별도 진행한다. D1-A 승인 이후 `508:44937`은 추가 변경 없이 참고용으로 고정 보존한다.

**D1-B — `Kiosk/OptionCard` 정식 Component化.** 설계 명세와 실행 Work Order는 별도 문서 참고: [ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md), [ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md](ASAK_FIGMA_D1B_OPTIONCARD_WORK_ORDER_2026-07-17.md). (참고: 이 "D1-B" 명칭은 이전에 `OptionSelectionRow` 텍스트 바인딩 수정을 가리켰으나, 그 작업은 별도 Design System 유지보수 배치로 이관되어 이제 "D1-B"는 `Kiosk/OptionCard` Component化를 가리킨다.)

## 최종 확정 사양 (2026-07-17 재확인)

| 항목 | 확정 내용 |
|---|---|
| 옵션 UI 형태 | 세로 `OptionSelectionRow` 목록 지시 제거 — **3열 Option Card Grid**로 확정 |
| 결정 주체 | 사용자가 직접 승인한 디자인 결정 |
| 그룹/옵션 수 | 총 7개 그룹 / 46개 옵션 |
| 필수 여부 | **베이스만 필수**, 드레싱·토핑·세트 음료·세트 스프·세트 사이드·제외 재료는 전부 **선택** |
| Header | 고정 (y=0~140) |
| BottomCTA | 고정 (y=1740, h=180) |
| Body | Scroll |
| 알레르기 정보 | 주황색 Accordion — 배경 `#FFF5ED` + 테두리 `#D97326`, "알레르기 정보 / N개 보기" 구조 |
| 일반 Frame `OptionCard` | Visual Pilot(`508:44937`) 전용, Production 반영 금지 |
| Production | 정식 Component Instance만 사용 |
| `508:44937` | 승인된 Visual Reference로 **동결** — 추가 변경 금지 |
| `134:7810` | 아직 반영 금지, 무변경 유지 |

## v3 변경 요약 (사용자 결정, 2026-07-17)

| # | 결정 |
|---|---|
| 1 | Menu Detail 옵션 UI는 **세로 목록이 아니라 3열 Card Grid**로 확정. v2의 "세로 목록/Stack" 지시는 폐기. |
| 2 | 이 결정은 사용자가 직접 내린 디자인 결정. |
| 3 | `508:44937`은 **Visual Reference Pilot**로 유지 — 시각 기준 참고용으로만 사용. |
| 4 | 현재 `508:44937` 안의 일반 Frame `OptionCard` 46개는 **Production 정본으로 인정하지 않음.** |
| 5 | 기존 `Kiosk/OptionSelectionRow`(`160:1831`)는 3열 카드 요구사항과 구조가 달라 **억지로 재사용하지 않음.** |
| 6 | 별도 배치에서 `Kiosk/OptionCard` 정식 Component 생성 여부를 검토 — 설계 명세는 이 문서와 별도로 작성(→ [ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md)). |
| 7 | `OptionSelectionRow`의 Text Property 미바인딩 수정(D1-B)은 **별도 Design System 유지보수 배치**로 이관 — D1 범위에서 제외. |

---

## 0. 배경

`SCR-004 / Menu Detail / Default` (`134:7810`)의 옵션 그리드가 `Kiosk/OrderDetailRow` (`150:247`) 인스턴스 46개로 잘못 채워져 있던 문제는 여전히 유효한 출발점이다. 다만 올바른 대체 방식을 v2(`OptionGroup`+`OptionSelectionRow` 세로 목록)로 시도한 결과, 실제로는 **3열 카드 그리드**가 최종 방향으로 확정됐다. `OptionSelectionRow`는 432×80px 세로 행(Row) 구조로 설계되어 있어 3열 카드 요구사항과 근본적으로 맞지 않으므로, 새 컴포넌트(`Kiosk/OptionCard`)를 별도로 설계·검토한다.

## 1. Pilot 위상 재정의 (v3)

- `503:2` — 이 세션에서 만든 세로 목록 버전. **폐기**(v2 접근 방식의 증거로만 남김, Production 반영 대상 아님).
- `508:44937` — 3열 Card Grid를 실제로 구현한 **Visual Reference Pilot**. 시각적 기준(카드 크기, 간격, 색상, 상태 표현)의 참고 자료로 유지하되, 그 안의 `OptionCard` 프레임 46개는 정식 컴포넌트가 아니므로 **그대로 Production에 옮기지 않는다.**
- Production `134:7810`은 계속 무변경 유지. 어떤 Pilot도 아직 Production에 반영되지 않았다.

## 2. 3열 Option Card Grid 사양

`508:44937`에서 검증된 수치를 기준으로 한다.

- Slot 유효 폭 912px(`OptionGroup` 좌우 패딩 24px×2 제외) 안에 카드 3개, 열 사이 간격(gap) 18px: `292×3 + 18×2 = 912`.
- 카드 크기: 292×104px(고정), 셀 사이 세로 간격 18px(2행 이상일 때).
- 카테고리별 옵션 개수는 서로 다르므로(8/8/8/6/4/6/6) 3열 기준으로 자동 줄바꿈되는 Grid/Wrap 레이아웃이어야 한다 — 특정 개수에 맞춘 고정 행 수를 가정하지 않는다.

## 3. 필수/선택 구분 (v3에서 재확인)

**베이스만 필수, 나머지 6개 그룹은 전부 선택.**

| 카테고리 | 필수 여부 | 원본 문구 |
|---|---|---|
| 베이스 | **필수** | "필수 · 최소 1개 선택" |
| 드레싱 | 선택 | "옵션 · 최대 1개 선택" |
| 토핑 | 선택 | "옵션 · 최대 5개 선택" |
| 세트 음료 | 선택 | "옵션 · 최대 1개 선택" |
| 세트 스프 | 선택 | "옵션 · 최대 1개 선택" |
| 세트 사이드 | 선택 | "옵션 · 최대 1개 선택" |
| 제외 재료 | 선택 | "옵션" |

> **주의(이번 QA에서 발견된 회귀)**: `508:44937`에서는 `requiredLabel`의 `hidden` 처리가 토핑·제외재료 2개 그룹에만 적용돼 있어, 드레싱·세트 음료·세트 스프·세트 사이드 4개 그룹까지 "필수" 배지가 잘못 노출되는 상태였다. 정식 `Kiosk/OptionCard`/`OptionGroup` 구조를 만들 때는 **베이스를 제외한 6개 그룹 전부 필수 배지를 숨겨야 한다.**

## 4. `OptionCard`가 지원해야 하는 정보

1. 이름(옵션명) — 최대 2줄, 초과 시 말줄임
2. 중량(g)
3. kcal
4. 추가 가격(예: `+1,500원`, `+0원`)
5. 상태(State)
6. 선택 표시(선택됐음을 나타내는 명시적 인디케이터 — 배경색만이 아니라 별도 표시 요소 권장, 상세는 별도 컴포넌트 명세 참고)

## 5. State

`Default` / `Selected` / `Disabled` / `Sold-out` — 최소 이 4개 State를 지원해야 한다. (상세 시각 규칙은 별도 컴포넌트 명세 문서 참고.)

## 6. 긴 한국어 이름 처리

옵션명은 최대 2줄까지 허용, 그 이상은 말줄임 처리. 짧은 예시만으로 검증을 끝내지 않고 실제로 긴 이름(예: "화이트치즈 (*채소믹스 미포함) 빼기")으로 Clipping을 확인한다.

## 7. Production 반영 조건 (v3에서 명확화)

- `OptionGroup`의 `children` Slot 안에는 **최종적으로 정식 Component Instance만 배치한다.** 일반 Frame(`mainComponent` 연결 없는 카드)은 Pilot 전용이며 **Production 반영 절대 금지.**
- 정식 `Kiosk/OptionCard` Component(및 필요 시 Variant Set)를 별도 배치에서 먼저 만들고, 그 Instance로 Pilot을 다시 구성해 검증을 통과한 뒤에만 Production에 반영한다.
- Production 적용 전 **Component Master 구조와 Instance 구조에 대한 QA가 필수**다 — 특히 이 파일에서 이미 3차례(`showEditButton`, `optionSummaryText`, `OptionGroup`/`OptionSelectionRow` 전체) 반복된 "Property는 정의됐는데 대상 노드에 바인딩이 안 된" 결함이 새 컴포넌트에서 재발하지 않는지 반드시 확인한다.

## 8. 유지해야 하는 것 (v2에서 이어짐, 변경 없음)

- `Kiosk/QuantityStepper` (`150:166`), `Kiosk/BottomCTA` (`150:385`, Production 인스턴스 `134:7813`은 이미 `x=0,y=1740,w=1080,h=180`로 기준과 일치, 변경 금지).
- 캔버스 크기 `1080×1920` 유지.
- `MenuDetailSummary` (`134:7814`), `allergy-accordion` (`136:4015`)은 이번 작업 범위 밖. 단, 색상 사양은 508 계열 Pilot에서 이미 확인됨 — **주황 배경(`#FFF5ED`) + 주황 테두리(`#D97326`)**, "알레르기 정보 / N개 보기" 구조. 이 사양은 Production `136:4015` 자체를 지금 바꾸라는 뜻이 아니라, 이후 정식 반영 시 유지해야 할 참고 기준이다.
- `category-drink`/`category-soup` 레이어 이름 뒤바뀜은 화면 표시 문구만 정리, 데이터 Key·Property 이름은 그대로.
- Production `134:7810` 원본, 다른 State, Prototype 연결, `07-C QA Matrix` 문서는 승인 전까지 모두 수정 금지.
- **`Kiosk/OptionSelectionRow`(`160:1831`) 마스터의 Text Property 바인딩 수정은 D1 범위에서 제외 — 별도 Design System 유지보수 배치로 이관.** (단, `Kiosk/OptionCard`를 새로 만들 때는 같은 결함을 처음부터 만들지 않도록 §7의 QA 절차를 따른다.)

## 9. 다음 단계 (아직 실행 아님)

1. `Kiosk/OptionCard` Component 설계 명세 검토([ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md)) 및 생성 여부 승인.
2. 승인되면 별도 배치에서 `Kiosk/OptionCard` Component + Variant 생성, 텍스트 바인딩까지 포함해 QA.
3. 새 Component로 Pilot을 다시 구성해 `508:44937`(Visual Reference)과 시각적으로 대조.
4. PASS 확인 후에만 Production `134:7810` 반영.
