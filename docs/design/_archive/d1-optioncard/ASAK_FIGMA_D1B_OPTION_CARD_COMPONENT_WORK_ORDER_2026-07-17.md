# D1-B — Kiosk/OptionCard Component 생성 실행 Work Order

> 작성일: 2026-07-17
> 성격: **실행 프롬프트. 문서 작성 시점 기준 아직 실행 여부 미확인.** 이 문서는 D1-B를 실행하는 별도 Figma 세션이 참고하는 작업 지시서다. 이 문서를 작성한 세션(QA 세션)은 Figma MCP를 호출하지 않았다.
> 선행 문서: [ASAK_FIGMA_D1_MENU_DETAIL_RECOVERY_PROMPT_2026-07-17.md](ASAK_FIGMA_D1_MENU_DETAIL_RECOVERY_PROMPT_2026-07-17.md)(D1-A 승인 + 최종 확정 사양), [ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md)(이전 버전 명세, 이 문서가 최신 통합본)

---

## 1. D1-B 목적

D1-A Visual Pilot(`508:44937`, 최종 PASS 승인됨)의 일반 Frame `OptionCard` 디자인을 그대로 참고해 **정식 Component Set `Kiosk/OptionCard`**를 만든다. `508:44937`은 승인된 Visual Reference로 동결된 상태이며, D1-B는 그 시각 기준을 정식 컴포넌트로 옮기는 작업이다. 완료 후에도 Production `134:7810` 반영은 별도 승인 사항이다.

## 2. Kiosk/OptionCard Component 명세 (v3, 타이포·간격 기준표 반영)

> **v3 갱신 이력**: 최초 명세(카드 104px, 절대위치 배지)로 만든 뒤 실측 결과 두 가지 구조적 문제가 발견되어 보정함 — (1) 배지가 절대위치라 긴 이름과 겹칠 위험, (2) 카드 정렬이 기본(위쪽 정렬)이라 같은 Row에서도 가격 줄 Y좌표가 카드마다 어긋남. 1차 보정으로 116px+SPACE_BETWEEN+배지 flow 편입까지 갔고, 이후 사용자가 제공한 "키오스크 OptionCard 타이포·간격 기준표"를 최종 기준으로 다시 한 번 보정해 **128px**로 확정. 아래는 그 최종 기준표를 반영한 최신 버전이다. Master Node ID: `579:1782`(2026-07-17, D1-B 실행 세션이 보고한 값 — 이 QA 세션은 아직 직접 확인 못 함, §11 참고).

### 2-1. 4개 State (Variant)

`state = default | selected | disabled | soldOut`

| State | Surface | Border | Text |
|---|---|---|---|
| `default` | White | Neutral 1px | 기본 |
| `selected` | 연한 Lime | Lime 2px | 선명하게 유지 |
| `disabled` | 연한 Neutral | Neutral | 읽히지만 조작 불가 |
| `soldOut` | 연한 Neutral/Red Tint | Neutral | Dim + Red Badge |

금지: Blue Selected, 검은(Dark Fill) 카드, 과도한 Shadow. Selected는 Lime 배경+Border만으로 표현.

`pressed`, `selectionType`(single/multiple/exclude)은 이번 범위 밖 — `selectionType`은 카드 레벨에서 시각 차이가 없어 Variant로 만들지 않고, 선택 개수 제한 로직은 `OptionGroup`의 `selectionRule` Property가 담당.

### 2-2. 6개 Component Property

| Property Key | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `optionName` | TEXT | "옵션 이름" | 옵션명 |
| `secondaryText` | TEXT | "" | "172g · 240kcal" 형식. 중량·kcal 중 하나만 있으면 그것만, 둘 다 없으면 Row 전체 숨김 |
| `additionalPrice` | TEXT | "" | "+1,500원" 형식만 허용 |
| `showSecondaryText` | BOOLEAN | `true` | 값이 실질적으로 없으면 숨김 |
| `showPrice` | BOOLEAN | `true` | 추가금 0원/기본 포함이면 반드시 `false` |
| `soldOutLabel` | TEXT | "품절" | `state=soldOut`일 때만 표시 |

**가격 표시 금지 문구**: `+0원`, `0원 추가`, `0000원 추가`, `기본 포함 0원` — 어떤 상황에서도 이런 임의 0원 표기를 넣지 않는다. 추가금이 없으면 `showPrice=false`로 가격 영역 자체를 숨긴다.

### 2-3. 3열 Grid 기준

| 항목 | 기준 |
|---|---|
| OptionGroup 콘텐츠 폭 | 912px |
| 카드 폭 | 292px |
| 열 개수 | 3열 |
| 열 간격 | 18px |
| 행 간격 | 16px |
| 그룹 제목 → 카드 간격 | 16px |
| 옵션 그룹 간 간격 | 36px |
| **카드 높이** | **128px 고정** |
| 카드 내부 Padding | 좌우 18px / 상하 16px |
| Radius | 12px |
| 기본 Border | 1px |
| Selected Border | 2px |

`292×3 + 18×2 = 912px` — OptionGroup Slot 폭과 정확히 일치.

### 2-4. 타이포그래피 (Pretendard Variable)

| 요소 | 크기/행간 | 굵기 | 정렬 |
|---|---|---|---|
| 옵션 그룹 제목 | 26/34px | 700 | 좌측 |
| 선택 규칙 설명 | 16/24px | 400~500 | 제목 우측 또는 하단 |
| 필수 표시 | 14/20px | 600 | Base에만 |
| **옵션명** | **24/30px** | **600~700** | 좌측 상단 |
| 중량·kcal | 16/22px | 400 | 옵션명 아래 |
| 추가 금액 | 18/24px | 600 | 우측 하단 |
| 품절 Badge | 14/20px | 600 | 우측 상단 |

옵션명 규칙: 최대 2줄, Auto Height, Text Width는 FILL, **긴 이름을 맞추려고 폰트 크기를 줄이지 않는다.** 2줄을 넘으면 말줄임보다 데이터 명칭 축약 여부를 먼저 검토.

### 2-5. Auto Layout 구조

```text
OptionCard — Vertical, 128px, padding 18px(좌우)/16px(상하), primaryAxisAlignItems: SPACE_BETWEEN
├─ TopRow — Horizontal
│  ├─ Selection Indicator — 24×24
│  ├─ InfoStack — FILL
│  │  ├─ OptionName — 최대 2줄
│  │  └─ SecondaryText — 조건부(showSecondaryText)
│  └─ SoldOutBadge — 조건부(state=soldOut), Flow 안, InfoStack이 FILL이라 겹치지 않음
└─ BottomRow — Horizontal
   ├─ Spacer — FILL
   └─ AdditionalPrice — 조건부(showPrice)
```

**중요(v2→v3 변경)**: 이전 버전은 `soldOutBadge`를 절대위치 오버레이로 두라고 했으나, 실측 결과 `InfoStack=FILL` 구조에서는 배지를 **TopRow 안 Flow 위치**(옵션명과 같은 줄, 전용 슬롯)에 둬도 겹치지 않는 것으로 확인됐다(D1-B 실행 세션 보고, §11 참고). **고정 좌표 배치는 여전히 금지**지만, 배지의 절대위치 예외 규정은 이번 버전에서 철회한다 — Flow 안에 두되 `InfoStack=FILL`로 공간을 확보하는 방식을 기본으로 한다.

세부 간격: 선택 표시↔텍스트 12px / 옵션명↔Secondary 4px / 상단 정보↔가격 행 최소 8px / Badge 내부 Padding 좌우 8px·상하 2px / Badge 높이 24px(44~48px 폭의 작은 Radius 6px Badge, 이전의 "긴 빨간 띠" 형태는 폐기).

카드 전체가 하나의 Touch Target — 내부에 별도 분리된 작은 버튼을 두지 않는다. 같은 Grid Row의 카드 3개는 `card-row`(Horizontal Auto Layout) + 각 인스턴스 `layoutSizingVertical=FILL`로 높이를 강제 일치시킨다.

### 2-6. 긴 한국어 이름 규칙

최대 2줄, 초과 시 말줄임(단 §2-4 규칙대로 폰트 축소로 우회 금지). 짧은 예시만으로 검증을 끝내지 않고, 실제로 긴 이름(예: "화이트치즈 (*채소믹스 미포함) 빼기", "특제 트러플크림 로스트치킨 샐러드 드레싱")으로 Clipping 여부를 확인한다.

### 2-7. Secondary·가격 영역

`secondaryText`와 `additionalPrice`가 `optionName` 영역을 침범하지 않도록 §2-5 구조(TopRow/BottomRow 분리)로 구획한다. 가격은 BottomRow 우측 정렬로 항상 카드 맨 아래 고정. 화면 전체 가격 위계는 "상품 요약에서 기본가 한 번 → 옵션 카드는 추가금 발생 시에만 → BottomCTA에서 최종 금액 한 번" 원칙을 따르고, 여러 곳에서 동시에 다른 형태의 가격을 노출하지 않는다.

---

## 3. 보호 대상 (절대 준수)

- `508:44937` — 어떤 노드도 변경 금지. 승인된 Visual Reference, 참고용으로만 사용.
- Production `134:7810` — 변경 금지.
- 기존 `Kiosk/OptionSelectionRow`(`160:1831`), `Kiosk/OptionGroup`(`160:1764`) — 변경 금지.
- **일반 Frame 카드 금지** — 이번에 만드는 것은 반드시 `mainComponent` 연결이 있는 정식 Component/Instance여야 한다. `508:44937`처럼 `mainComponent` 없는 일반 Frame으로 만들지 않는다.
- **Instance Detach 금지.**
- 새 Component Set은 `Kiosk/OptionCard` 하나로 한정 — 그 외 추가 Component Set을 임의로 만들지 않는다.
- 모든 작업은 독립 Sandbox Frame(기존 콘텐츠와 겹치지 않는 새 위치)에서 진행한다.

## 4. Property Binding 검증 기준 (필수, 생략 불가)

이 Figma 파일에서 지금까지 **3차례** 같은 결함이 반복됐다: Property는 정의했지만 실제 텍스트/가시성 노드에 `componentPropertyReferences`를 연결하지 않아, 인스턴스에 값을 넣어도 화면에 반영되지 않는 문제(`showEditButton`, `optionSummaryText`, `OptionGroup`+`OptionSelectionRow` 전체 17개 Variant). `Kiosk/OptionCard`는 다음을 전부 통과해야 "바인딩 완료"로 인정한다.

- [ ] `optionName`/`secondaryText`/`additionalPrice`/`soldOutLabel` — 각 TEXT Property가 대상 텍스트 노드의 `componentPropertyReferences.characters`에 실제로 연결됐는지, **4개 State 전부 개별로** 확인(한 Variant를 고쳐도 나머지에 자동 전파되지 않는다).
- [ ] `showSecondaryText`/`showPrice` — 대상 노드의 `componentPropertyReferences.visible`에 연결됐는지 4개 State 전부 확인.
- [ ] 인스턴스에서 `setProperties()`로 값을 바꿨을 때 화면에 실제로 반영되는지 확인(Property 패널 값만 바뀌고 렌더링은 그대로인 상태가 아닌지).
- [ ] 텍스트가 **인스턴스 레벨 직접 Override**(Property를 거치지 않고 텍스트 레이어를 손으로 고친 것)로 맞춰진 게 아닌지 확인 — 이 방식은 화면은 맞아 보이지만 재사용 가능한 컴포넌트가 아니다.
- [ ] 값을 아무것도 지정하지 않은 새 인스턴스가 Property 기본값을 그대로 표시하는지(하위 호환성) 확인.

## 5. Instance Matrix 검증 데이터 (v2, 최종 확정)

| 이름 | 용도 |
|---|---|
| 포케볼 | 짧은 이름 |
| 양배추라이스 | 짧은 이름 |
| 그린어니언크림 | 짧은~중간 이름, 가격 있음 |
| 허니머스타드 | 중간 길이 이름 |
| 통밀또띠아 | 중간 길이 이름, 줄바꿈 확인 |
| 로스트닭다리살 | 중간 길이 이름, 품절 상태(`state=soldOut`) |
| 무가당그릭요거트 | 중간 길이 이름, 가격 없음(`showPrice=false`) |

추가 필수 조합:
- 1줄 / 2줄 이름
- 가격 있음 / 없음
- Secondary 있음 / 없음
- Selected / Disabled / Sold-out
- **Sold-out + 2줄 이름 동시**(최악의 케이스 — 배지+2줄 이름+Secondary+가격이 전부 있는 조합)
- 같은 행 카드 3개 높이 동일 여부
- **0원, 0g, 0kcal 노출 0건** 확인

## 6. Production 전파 전 승인 조건

아래 전부 충족 전까지 어떤 화면에도 배포하지 않는다.

- §4 바인딩 검증 체크리스트 전항목 PASS (4개 State 개별 확인 포함).
- §5 Instance Matrix 전체 스크린샷으로 시각 확인 완료.
- 일반 Frame이 하나도 섞이지 않았음을 구조적으로 확인(전부 `mainComponent` 연결된 Instance).
- Instance Detach 이력 없음.
- 사람(사용자)의 명시적 "Production 반영 승인".

## 7. 3개 Instance 시범 교체 절차

1. `508:44937`을 **다시 복제**(원본은 건드리지 않음)해 새 Sandbox(`D1B_SANDBOX / Menu Detail Default` 등)를 만든다.
2. 그 복제본 안에서 일반 Frame 카드 **3개만** 정식 `Kiosk/OptionCard` Instance로 교체한다(짧은 이름 1개, 중간 길이 이름 1개, 품절 1개 권장).
3. 교체한 3개와 `508:44937`(레퍼런스)을 나란히 스크린샷으로 비교 — 카드 크기·색상·텍스트 위치·줄바꿈이 동일한지 확인.
4. 시각 동일성 PASS 전까지 다음 단계(46개 전체 교체)로 진행하지 않는다.

## 8. 46개 전체 교체 절차

1. §7 시각 동일성 PASS 확인 후 진행.
2. 나머지 43개(총 46개)까지 전부 정식 `Kiosk/OptionCard` Instance로 교체.
3. 구조 QA: `OptionGroup`의 `children` Slot 안에 일반 Frame이 하나도 안 남았는지, 46개 카운트 유지(8+8+8+6+4+6+6), Instance Detach 없음, `Kiosk/OptionCard` 외 추가 Component Set 없음.
4. Long text Clipping, Secondary/Price 겹침, State별 시각 구분(§2-1 기준)을 카드 단위로 전수 확인.
5. `508:44937`, Production `134:7810`, 기존 Master(`160:1764`/`160:1831`) 무변경 재확인.
6. 여기까지 완료해도 **Production 반영은 별도 승인 후에만** — §6 조건 충족 여부를 사용자에게 보고하고 대기.

## 9. Rollback 기준

아래 중 하나라도 해당하면 즉시 작업을 멈추고 되돌린 뒤 보고한다.

- §4 바인딩 검증이 2회 시도 후에도 통과하지 못하는 State/Property가 있는 경우 → 해당 Component 배포를 보류하고, 인스턴스 직접 Override로 임시 봉합하지 않는다. 사용자에게 보고 후 재설계 여부 결정.
- §7 시범 교체 3개 중 하나라도 `508:44937` 레퍼런스와 시각적으로 다르게 렌더링되는데 같은 세션에서 원인을 못 찾는 경우 → 그 3개 교체를 원래 일반 Frame으로 되돌리고, 46개 전체 교체로 진행하지 않는다.
- §8 46개 전체 교체 중 새로운 겹침·잘림·State 오표시가 발견되는 경우 → §7 시범 교체 상태(또는 원본 46개 일반 Frame 상태)까지 되돌리고, Production 반영 검토를 중단한다.
- 작업 도중 실수로 `508:44937`, Production `134:7810`, 기존 Master(`160:1764`/`160:1831`) 중 하나라도 변경된 경우 → 그 변경을 즉시 원복하고, 원복 완료를 확인한 뒤 나머지 작업을 이어간다. 원복이 불확실하면 즉시 작업을 멈추고 사용자에게 보고한다.
- 새 Component Set이 `Kiosk/OptionCard` 외에 의도치 않게 추가로 생긴 경우 → 정리(병합 또는 삭제)한 뒤가 아니면 다음 단계로 진행하지 않는다.

## 10. 완료 후 보고 형식

- Component 4개 State 나란히 스크린샷
- §4 바인딩 검증 체크리스트 결과(4 State × 6 Property)
- §5 Instance Matrix 스크린샷
- §7/§8 진행 시: Before/After, 시각 동일성 판정, 구조 QA 결과
- 생성·변경 Node ID 전체 목록
- `508:44937`/Production/기존 Master 무변경 확인
- §9 Rollback 발동 여부(있었다면 사유와 처리 결과)
- 다음 지시 대기

## 11. 실행 세션 자체보고 로그 (미검증 — QA 세션이 Figma로 직접 확인 못 함)

2026-07-17, D1-B 실행 세션이 두 라운드에 걸쳐 아래를 보고함. **이 QA 세션은 이번 라운드에 Figma MCP 호출 권한이 없어 아래 내용을 라이브로 재검증하지 못했다.** 문서에는 참고용으로만 기록하고, PASS 판정은 내리지 않는다.

**1라운드 (레이아웃 구조 보정, 카드 104→116px)**
- 원인 진단: soldOutBadge 절대위치가 긴 이름과 겹칠 수 있었음 / 카드 기본 정렬(위쪽 정렬)이라 카드마다 hug 높이가 달라 가격 Y좌표가 어긋남 / Matrix가 카드를 독립 hug시켜 같은 줄에서도 높이가 제각각이었음.
- 수정: soldOutBadge를 optionName과 같은 `name-row`(가로 Auto Layout)로 이동, `primaryAxisAlignItems: SPACE_BETWEEN` 적용, minHeight 104→116px, Instance Matrix를 Row 단위(`card-row` + `layoutSizingVertical=FILL`) 구조로 재구성.
- 보고된 실측: 6개 카드(그린어니언크림/양배추라이스/허니머스타드/통밀또띠아/로스트닭다리살/무가당그릭요거트) 전부 116px 동일, 2줄 이름+SoldOut 배지+Secondary+가격 동시 조합도 겹침 0.
- 가격 표시 단순화(OptionCard 범위만): 추가금 있는 옵션만 표시, 무료/기본 포함은 `showPrice=false`로 숨김, "+0원" 등 플레이스홀더 문구 전면 배제.
- 보호 대상(508:44937/503:2/134:7810/OptionGroup 2 variant/OptionSelectionRow 15 variant) 자식 개수 무변경 보고.

**2라운드 (타이포·간격 기준표 전면 적용, 카드 116→128px)**
- 사용자가 제공한 최종 기준표(§2 반영됨)대로 재보정: 옵션명 폰트 24/30 SemiBold로 확대, 카드 높이 128px, SPACE_BETWEEN 유지.
- 보고된 이슈 해결 확인: 가격 텍스트가 하단 경계에 붙어 보이는 것은 실측 결과 패딩 16px 정상 유지(잘림 아님), 스크린샷 도구의 "height 104" 표기는 캐시 지연 표시였고 실제 카드 높이는 128px라고 보고.
- 24px 확대 폰트 + 2줄 줄바꿈 + SoldOut 배지 + Secondary + 가격 동시 조합도 128px 안에서 겹침 없다고 보고.
- Master Node ID: `Kiosk/OptionCard`, `579:1782` (4 Variant).
- **지시하신 완료 보고 형식(카드 확대 Screenshot, 3열 Row Screenshot, 위계 설명, 조정 내용, PASS/FAIL 표)이 이번에 전달받은 내용에는 명시적으로 포함되지 않음** — 서술형 요약만 있고 정형 보고 포맷은 비어 있다. 다음 라운드에서 정형 포맷으로 다시 요청 필요.

**QA 세션 코멘트**: 서술 내용 자체는 이 문서의 §2(타이포·간격 기준표)와 정합적이라 신뢰도는 높으나, "확인함"/"보고함"을 "검증됨"으로 승격하지 않는다. 읽기 전용 권한이 다시 주어지면 §4 바인딩 체크리스트와 §5 Instance Matrix를 라이브로 재확인할 것.
