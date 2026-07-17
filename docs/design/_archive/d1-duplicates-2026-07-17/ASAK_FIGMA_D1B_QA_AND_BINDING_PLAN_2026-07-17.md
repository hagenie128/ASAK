# D1 Visual Pilot 검수 계획 + D1-B Master 바인딩 실행계획

> 작성일: 2026-07-17
> 성격: **계획·체크리스트 문서. 실행 프롬프트 아님. Figma에 대한 어떤 실행도 포함하지 않음.**
> 작성 방식: 이 대화에서 이미 라이브로 확인한 사실만 사용. 프로젝트 재탐색 없음.
> 현재 소유 세션: `508:44937` (D1 Visual Pilot 진행 중). 이 문서를 작성한 세션은 읽기 전용 Design Director/QA — Figma MCP 호출 없음.

---

## ⚠️ 먼저 확인이 필요한 충돌 2건

문서를 채우기 전에, 지금까지 확정된 사실과 이번에 주신 체크리스트 항목이 서로 안 맞는 부분이 있어 먼저 표시합니다. 제가 임의로 하나를 골라 문서에 반영하지 않았습니다.

**충돌 1 — "기존 3열 Grid 유지" vs D1 v2 문서의 "세로 목록/Stack"**
`ASAK_FIGMA_D1_MENU_DETAIL_RECOVERY_PROMPT_2026-07-17.md` v2는 "한 Group 안에서는 OptionSelectionRow를 읽기 쉬운 세로 목록으로 배치"하도록 지시했고, `Kiosk/OptionGroup` 마스터의 `children` 슬롯 자체도 세로 flex(`flex flex-col`) 구조입니다. 반면 이번 체크리스트 1번은 "기존 3열 Grid 유지"를 요구합니다. 이 둘은 같은 화면에 동시에 적용할 수 없는 상반된 지시입니다 — 아래 §1/§2에서는 **"세로 목록"**을 기준으로 체크리스트를 작성했고, 3열 Grid를 유지해야 한다면 D1 v2 문서 자체를 다시 고쳐야 합니다.

**충돌 2 — "중량·kcal·가격 겹침 없음" vs `OptionSelectionRow` 마스터에 중량/kcal 필드 없음**
`Kiosk/OptionSelectionRow`(`160:1831`)의 Property는 `label`, `additionalPrice`, `showPrice`, `soldOutLabel`뿐이며, 중량(g)·kcal을 표시할 자리가 마스터에 없습니다(기존 깨진 화면의 "0g/0kcal"은 애초에 `OrderDetailRow`용 필드였음). "중량·kcal·가격 겹침 없음"을 PASS 조건으로 유지하려면 (a) 중량/kcal 표시를 포기하거나, (b) `OptionSelectionRow` 마스터에 새 필드를 추가해야 하는데 후자는 "새 Component Set 생성 금지" 원칙과 충돌합니다.

두 항목 모두 아래 문서에서는 "확정된 사실 기준"으로 작성하고, 실제 답을 알 수 없는 부분은 표에 명시적으로 표시했습니다.

---

## 1. D1 Visual Pilot 최종 PASS/FAIL 체크리스트

| # | 항목 | PASS 기준 | 근거 |
|---|---|---|---|
| 1 | Production 무변경 | `134:7810`의 x/y/width/height, `Kiosk/OrderDetailRow` 인스턴스 수(46), 카테고리 프레임 7개가 작업 시작 전과 완전히 동일 | 이번 세션에서 마지막 재확인: 46개/7개 원본 유지 확인됨 |
| 2 | Pilot 격리 | 모든 변경이 `503:2`(또는 `508:44937`) 복제본 내부에서만 발생, 새 Component Set 미생성, Instance Detach 없음 | D1 v2 §1 |
| 3 | Header 고정 | y=0~140, 내용·크기 무변경 | D1 v2 §6 |
| 4 | BottomCTA 고정 | x=0, y=1740, w=1080, h=180 유지 | D1 v2 §6, 이번 세션에서 Pilot 내 `503:99` 실측 일치 확인 |
| 5 | Body 스크롤 컨테이너 | Header 하단(140)~BottomCTA 상단(1740) 사이가 하나의 스크롤 가능 영역으로 구성 | 이번 세션에서 `scroll-body`(clipsContent+overflowDirection=VERTICAL) 생성 확인 |
| 6 | 7개 OptionGroup 세로 배치 | ⚠️ 충돌 1 참고 — "세로 목록" 기준이면 그리드 압축 없이 위→아래 배치 | D1 v2 §6 |
| 7 | 46개 옵션 누락 없음 | 베이스8 · 드레싱8 · 토핑8 · 세트음료6 · 세트스프4 · 세트사이드6 · 제외재료6 = 46 | D1 v2 §3 표 |
| 8 | 옵션명 최대 2줄 | 실제 텍스트가 2줄을 넘거나 잘리지 않음 | D1 v2 §6 |
| 9 | 가격 별도 고정 영역 | `additionalPrice`가 옵션명과 겹치지 않는 우측 고정 위치에 표시 | D1 v2 §6, `OptionSelectionRow` 구조상 기본 충족(라벨 flex-1 + 가격 shrink-0) |
| 10 | 실제 텍스트 렌더링 | 모든 옵션에 실제 이름·가격이 표시되고 "옵션 이름"/"+1,000원" 같은 마스터 기본값이 하나도 안 보임 | **D1-B(마스터 바인딩) 완료가 선행 조건** — 이번 세션에서 100% 미바인딩 확인됨 |
| 11 | 선택/품절 상태 구분 | `selected`=라임 배경+채워진 인디케이터, `soldOut`=배지+회색 텍스트(투명도만 사용 아님) | `OptionSelectionRow` 컴포넌트 설명("opacity만 사용하지 않음") |
| 12 | 터치 영역 | Row 최소 48px(확정 기준), 현재 실측 80px로 이미 충족 | 이번 세션 실측(`508:2` 하위 row height=80) |
| 13 | 카테고리 문구 정리 | `category-drink`=세트 스프, `category-soup`=세트 사이드로 표시 문구만 정리, 레이어 이름·데이터 Key 무변경 | D1 v2 §3 |
| 14 | 알레르기 Accordion 위치 | Body 스크롤 영역 맨 아래에 정상 위치, 내용 무변경 | D1 v2 §5 |
| 15 | 다른 State/Prototype/Master/07-C 무변경 | 이번 D1 Pilot 작업으로 인한 부수 변경 없음 | D1 v2 §5, §7 |
| 16 | Before/After 스크린샷 세트 | Production(Before)과 Pilot(After) 스크린샷이 함께 제공됨 | D1 v2 §8 |

---

## 2. Screenshot으로 확인할 항목 (8개 지정 항목 + 확인 방법)

| 항목 | 확인 방법 | 비고 |
|---|---|---|
| 기존 3열 Grid 유지 | 카테고리별 옵션이 3열로 배열돼 있는지 육안 확인 | ⚠️ 충돌 1 — D1 v2와 상반, 결정 필요 |
| AI SaaS 형태 아님 | ASAK 브랜드 톤(라임 `#A3E635`/`#B5E30F` 계열 선택 강조, Cream 배경, 둥근 카드) 유지 여부, 일반 대시보드처럼 각지고 무채색인 테이블형 UI로 안 보이는지 | 주관적 판단 필요, 스크린샷만으로 100% 판별 어려움 — Figma 파일의 Design System(00. 디자인 시스템 페이지) 토큰과 대조 권장 |
| 옵션명 최대 2줄 | 가장 긴 한국어 옵션명 행에서 줄바꿈이 2줄 이내인지, 3줄째가 잘리는지 확인 | 짧은 예시만으로 검증 끝내지 않기(D1 v2 §6) |
| 중량·kcal·가격 겹침 없음 | 가격 텍스트와 다른 텍스트가 겹치지 않는지만 확인 가능 | ⚠️ 충돌 2 — 중량/kcal 필드 자체가 마스터에 없음, "겹침 없음"은 자동 충족되지만 "중량·kcal 표시"는 별도 결정 필요 |
| 선택/품절 상태 구분 | `selected` 행이 라임 배경으로 눈에 띄는지, `soldOut` 행이 배지+텍스트로 표시되는지(단순히 흐릿하기만 한 게 아닌지) | §1-11 참고 |
| 46개 옵션 누락 없음 | 카테고리별 개수를 세어 8/8/8/6/4/6/6과 일치하는지 | §1-7 참고 |
| 알레르기 Accordion 적절성 | 접힌 상태의 헤더("알레르기 정보", "2개 보기" 등)가 다른 옵션 그룹과 겹치지 않고 스크롤 영역 맨 아래에 자연스럽게 이어지는지 | 내용 자체는 D1 범위 밖, 위치만 확인 |
| Header/BottomCTA 고정 | 정적 스크린샷 1장으로는 "고정되어 스크롤 안 됨"을 직접 증명할 수 없음 — Header/BottomCTA의 크기·위치가 스크롤 전/후 스크린샷 2장에서 동일한지 비교하거나, Figma Prototype 모드에서 실제 스크롤 테스트 필요 | 정적 캡처의 한계로 별도 언급 |

---

## 3. D1-B — Master Text Property 바인딩 실행계획

### 3-1. 대상 컴포넌트와 Variant

**`Kiosk/OptionGroup` (`160:1764`, COMPONENT_SET) — 2개 Variant 전부 미바인딩**

| Variant | Variant ID | title | requiredLabel | description |
|---|---|---|---|---|
| state=default | `160:1750` | `160:1752` | `160:1753` | `160:1754` |
| state=disabled | `160:1757` | `160:1759` | `160:1760` | `160:1761` |

**`Kiosk/OptionSelectionRow` (`160:1831`, COMPONENT_SET) — 15개 Variant 전부 미바인딩**

| selectionType | state | Variant ID | label | additionalPrice | soldOutLabel |
|---|---|---|---|---|---|
| single | default | `160:1765` | `160:1767` | `160:1768` | — |
| single | selected | `160:1769` | `160:1771` | `160:1772` | — |
| single | disabled | `160:1773` | `160:1775` | `160:1776` | — |
| single | soldOut | `160:1777` | `160:1779` | `160:1782` | `160:1781` |
| single | pressed | `160:1783` | `160:1785` | `160:1786` | — |
| multiple | default | `160:1787` | `160:1789` | `160:1790` | — |
| multiple | selected | `160:1791` | `160:1793` | `160:1794` | — |
| multiple | disabled | `160:1795` | `160:1797` | `160:1798` | — |
| multiple | soldOut | `160:1799` | `160:1801` | `160:1804` | `160:1803` |
| multiple | pressed | `160:1805` | `160:1807` | `160:1808` | — |
| exclude | default | `160:1809` | `160:1811` | `160:1812` | — |
| exclude | selected | `160:1813` | `160:1815` | `160:1816` | — |
| exclude | disabled | `160:1817` | `160:1819` | `160:1820` | — |
| exclude | soldOut | `160:1821` | `160:1823` | `160:1826` | `160:1825` |
| exclude | pressed | `160:1827` | `160:1829` | `160:1830` | — |

### 3-2. Property Reference 연결 규칙

CartItemCard에서 이미 두 번 검증된 패턴을 그대로 따른다 (`showEditButton`→`visible`, `optionSummaryText`→`characters`).

| Property Key | 타입 | 바인딩 대상 필드 | 규칙 |
|---|---|---|---|
| `title#160:89` | TEXT | `characters` | 해당 Variant의 title 텍스트 노드에 바인딩 |
| `description#160:92` | TEXT | `characters` | 해당 Variant의 description 텍스트 노드에 바인딩 |
| `requiredLabel#160:95` | TEXT | `characters` | 해당 Variant의 requiredLabel 텍스트 노드에 바인딩 |
| `showRequiredLabel#160:98` | BOOLEAN | `visible` | requiredLabel 텍스트 노드 자체의 표시 여부에 바인딩 (별도 배지 프레임 없음 — 텍스트 노드가 곧 "필수" 표시) |
| `selectionRule#160:101` | TEXT | (바인딩 대상 없음) | 화면에 렌더링되는 텍스트가 아니라 로직/데이터용 Property로 추정 — 바인딩 불필요, 이 문서 §3-4에서 재확인 필요 항목으로 별도 표시 |
| `label#160:107` | TEXT | `characters` | 해당 Variant의 label 텍스트 노드에 바인딩 |
| `additionalPrice#160:123` | TEXT | `characters` | 해당 Variant의 additionalPrice 텍스트 노드에 바인딩 |
| `showPrice#160:139` | BOOLEAN | `visible` | additionalPrice 텍스트 노드 자체의 표시 여부에 바인딩 |
| `soldOutLabel#160:155` | TEXT | `characters` | soldOut 계열 3개 Variant(`160:1781`/`160:1803`/`160:1825`)에만 해당 |

**주의**: 이번 세션 실측(`instance.componentProperties`는 값이 정확한데 텍스트 노드의 `componentPropertyReferences`만 전부 `{}`)에 근거해 boolean 바인딩(`showRequiredLabel`, `showPrice`)도 마찬가지로 안 되어 있을 것으로 **추정**했다. text-characters 바인딩만 직접 스크린샷으로 확인했고, boolean-visible 바인딩은 라이브로 별도 확인하지 않았으므로 실행 전 재확인 필요.

### 3-3. 작은 검증 Instance를 통한 테스트 절차

1. Production·Pilot과 무관한 캔버스 빈 공간에 `OptionGroup`(default 1개)과 `OptionSelectionRow`(single/default 1개) 테스트 인스턴스를 각각 하나씩 생성.
2. 마스터 수정 전, 이 테스트 인스턴스에 구분되는 임의 문자열(예: `"TEST_TITLE_0001"`)을 Property로 설정 → 현재는 반영 안 되는 것(재현)을 스크린샷으로 재확인.
3. 마스터의 해당 Variant 텍스트 노드에 §3-2 규칙대로 `componentPropertyReferences` 바인딩 적용.
4. 같은 테스트 인스턴스(또는 새 인스턴스)에 동일한 임의 문자열을 다시 설정 → 이번엔 반영되는지 스크린샷으로 확인.
5. 최소 1개 Variant에서 성공을 확인한 뒤, **17개 Variant 전부 개별로 같은 방식 재검증** — Default variant를 고친다고 다른 Variant의 텍스트 노드가 같이 고쳐지지 않는다(각 Variant가 자기만의 텍스트 레이어 사본을 가짐, 이번 세션 스캔에서 확인된 사실).
6. 검증 끝난 뒤 테스트용 임시 인스턴스는 삭제해 캔버스에 잔재를 남기지 않는다.

### 3-4. Production 전파 금지 조건 (아래 전부 충족 전까지 자동 전파 금지)

- 17개 Variant 전부 개별 바인딩 검증 완료(§3-3 5번 항목).
- 값을 아무것도 안 준 새 인스턴스가 여전히 Master의 원래 기본값(예: "드레싱 선택")을 정상 표시 — 즉 기존에 이미 배치된 다른 화면의 인스턴스들에 회귀가 없는지 하위 호환성 확인.
- `selectionRule#160:101`의 실제 용도(로직용인지 표시용인지) 재확인 후 처리 방향 결정.
- 현재 D1 Pilot 소유 세션(`508:44937`)이 마스터 수정 후 Pilot 렌더링이 정상인지 재확인·승인.
- 사용자로부터 **Master 수정 자체에 대한 별도 승인** — D1 Pilot 승인과는 별개 승인 필요(D1 v2 문서가 Master 수정을 별도 승인 대상으로 명시).
- 같은 Master를 다른 세션이 동시에 편집 중이지 않은지 조율 확인.

---

## 4. D1 Pilot PASS 후 Production 적용 절차

1. §1 체크리스트 16개 항목 전부 PASS(10번 항목은 D1-B 완료가 전제) 확인.
2. Pilot 추가 편집 중단, Before(Production)/After(Pilot) 스크린샷과 변경 Node ID 목록을 최종 스냅샷으로 고정.
3. Production `134:7810` 또는 그 상위 페이지를 다른 세션이 동시에 건드리고 있지 않은지 조율 확인.
4. Production에 Pilot과 동일한 구조 반영: 기존 46개 `OrderDetailRow` + 7개 category-header 프레임 제거, Header/BottomCTA 고정 + scroll-body 구조 삽입, 7개 `OptionGroup`+`OptionSelectionRow` 세트를 **실제 서비스 데이터**(placeholder였던 "+0원" 등이 아닌 실 가격·옵션명)로 삽입.
5. 삭제 대상 노드(46개 `OrderDetailRow`, 7개 category-header)를 Prototype Reaction이 참조하고 있지 않은지 사전 확인 — 참조 중이면 삭제 전 연결 재배선 필요.
6. Production 반영 후 재검증: 46개 옵션 카운트, Pilot과의 스크린샷 비교, Prototype 연결 정상 동작.
7. 문서 갱신은 사용자 확인 후에만 진행(07-C QA Matrix, D1 지시서 상태 갱신 등).
8. Pilot 복제본(`503:2`/`508:44937`)은 Production 반영이 확정되고 더 이상 비교 대상으로 필요 없다고 사용자가 명시적으로 확인한 뒤에만 삭제 — 자동 삭제 금지.

---

## 5. D2 형제 State 전파 시 위험 목록

1. **State별 콘텐츠 차이**: Default에서 확인한 46개/7카테고리 구성을 그대로 복사하면, 필수 옵션 미선택·최대 선택 도달·옵션 품절·알레르기 경고 등 다른 State의 실제 콘텐츠(문구, 강조 요소)가 빠질 위험.
2. **같은 마스터 바인딩 결함 재발**: 이번에 발견한 100% 미바인딩이 다른 화면에서도 "정본이니까 안전하다"고 믿고 그대로 재사용되며 같은 문제가 반복 전파될 위험(이미 3번째 발견된 패턴).
3. **Auto Layout 재구조화의 부작용**: `options-content`를 Auto Layout 세로 스택으로 바꾸는 방식을 다른 State에 그대로 적용하면, 그 State에만 있는 절대 위치 오버레이(예: `sold-out-badge`류)가 깨질 위험.
4. **Prototype 연결 단절**: 형제 State 간 전환 Reaction이 이번에 삭제되는 특정 Node ID(46개 OrderDetailRow 등)를 참조하고 있다면, 구조 교체로 그 연결이 끊길 위험.
5. **단계적 반영으로 인한 일시적 불일치**: Default만 먼저 Production에 반영하고 형제 State 전파를 미루면, 화면 간 구조가 달라 보이는 과도기가 생기고 07-C QA Matrix가 다시 실제 상태와 어긋날 위험.
6. **병렬 세션 충돌**: 이번 대화에서만 세 차례 확인된 것처럼 다른 세션이 동시에 같은 파일/같은 State를 건드릴 가능성 — D2 착수 전 단독 소유 세션 재확인 필요.
7. **Placeholder 데이터 확산**: 이번 Pilot의 베이스 카테고리는 "+0원" 같은 placeholder 가격으로 채워졌다 — 실제 서비스 데이터 연결 없이 형제 State에도 같은 placeholder가 그대로 복제될 위험.
8. **category-drink/category-soup 이름 불일치 재발**: Default에서만 표시 문구를 바로잡고 형제 State에서 같은 뒤바뀜이 다시 나타날 위험.

---

## 다음 결정이 필요한 사항 (요약)

- **충돌 1**: 3열 Grid 유지 vs 세로 목록(D1 v2) — 어느 쪽을 기준으로 할지.
- **충돌 2**: 중량/kcal 표시를 포기할지, `OptionSelectionRow`에 필드를 추가할지(단, 후자는 "새 Component Set 금지"와 충돌하므로 별도 승인 필요).
- D1-B(마스터 바인딩) 착수를 이 문서 §3 계획대로 진행해도 될지, 그리고 어느 세션이 실행할지.
