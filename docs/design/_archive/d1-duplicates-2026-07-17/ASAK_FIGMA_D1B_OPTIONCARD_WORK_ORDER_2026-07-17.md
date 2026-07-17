# D1-B — Kiosk/OptionCard Component化 실행 Work Order

> 작성일: 2026-07-17
> 성격: **실행 프롬프트. 아직 실행하지 않음.** 이 문서에 적힌 실행 지시는 사용자의 별도 "지금 시작" 승인이 있을 때만 시작한다.
> 선행 문서: [ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md)(무엇을 만들지), [ASAK_FIGMA_D1_MENU_DETAIL_RECOVERY_PROMPT_2026-07-17.md](ASAK_FIGMA_D1_MENU_DETAIL_RECOVERY_PROMPT_2026-07-17.md)(D1-A 승인 상태)

## 0. 목표

`508:44937`(D1-A Visual Pilot, 최종 승인됨)의 일반 Frame `OptionCard` 디자인을 그대로 참고해, **정식 Component Set `Kiosk/OptionCard`**로 재현한다. `508:44937`·Production·기존 Master는 전혀 건드리지 않는 **독립 Sandbox**에서 진행한다.

## 1. Sandbox 원칙 (절대 준수)

- 새로 만드는 모든 것은 **독립 검증 Frame** 안에서만 생성한다(캔버스 빈 공간, 기존 콘텐츠와 겹치지 않는 위치).
- `508:44937` — 어떤 노드도 변경 금지(참고용 스크린샷/실측만 허용).
- Production `134:7810` — 변경 금지.
- 기존 `Kiosk/OptionSelectionRow`(`160:1831`), `Kiosk/OptionGroup`(`160:1764`) — 변경 금지.
- Component 생성 후 **작은 Instance Matrix**로 Property 작동을 검증하기 전까지는 어디에도 배포하지 않는다.
- **승인 전 46개 카드 교체 금지.** 이 Work Order의 §5(마이그레이션)는 §4(바인딩 검증)가 전부 PASS한 뒤, 그리고 사람의 승인이 있은 뒤에만 진행한다.
- 새 Component Set은 이번에 만드는 `Kiosk/OptionCard` 하나로 한정 — 그 외 추가 Component Set을 임의로 만들지 않는다.

## 2. Component 생성 절차

1. Sandbox Frame 안에 `Kiosk/OptionCard` Component Set을 만든다. Variant: `state=default`, `state=selected`, `state=disabled`, `state=soldOut` — [스펙 문서 §2](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md#2-variant) 기준.
2. 각 Variant 내부에 [스펙 문서 §4](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md#4-레이아웃) 레이아웃 규칙대로 Auto Layout 구조를 만든다 — 고정 좌표 텍스트 배치 금지, 품절 배지만 절대 위치 오버레이.
3. Component Property 6개를 정의한다: `optionName`(TEXT), `secondaryText`(TEXT), `additionalPrice`(TEXT), `showSecondaryText`(BOOLEAN), `showPrice`(BOOLEAN), `soldOutLabel`(TEXT) — [스펙 문서 §3](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md#3-component-property).
4. [스펙 문서 §5](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md#5-시각-상태-state별-규칙) 기준으로 State별 시각 스타일 적용. Dark Fill·Blue Selected 금지 재확인.

## 3. 바인딩 검증 (필수 — 생략 불가)

이 Figma 파일에서 지금까지 **3차례** 같은 결함이 발견됐다: Property는 정의했지만 실제 텍스트/가시성 노드에 `componentPropertyReferences`를 연결하지 않아, 인스턴스에 값을 넣어도 화면에 반영되지 않는 문제 (`showEditButton`, `optionSummaryText`, `OptionGroup`+`OptionSelectionRow` 전체 17개 Variant). `Kiosk/OptionCard`는 처음부터 이 문제를 피해서 만든다.

- [ ] `optionName`/`secondaryText`/`additionalPrice`/`soldOutLabel` — 각 TEXT Property가 대상 텍스트 노드의 `componentPropertyReferences.characters`에 정확히 연결됐는지, **4개 Variant 전부 개별로** 확인한다(하나를 고쳤다고 나머지에 자동 전파되지 않는다 — 각 Variant가 자기만의 텍스트 레이어 사본을 가짐).
- [ ] `showSecondaryText`/`showPrice` — 대상 노드의 `componentPropertyReferences.visible`에 연결됐는지 4개 Variant 전부 확인.
- [ ] 값을 아무것도 지정하지 않은 새 인스턴스가 Property 기본값을 그대로 표시하는지 확인(하위 호환성).
- [ ] 최소 1개 Variant에서 임의 테스트 문자열(예: `TEST_NAME_0001`)로 바인딩 여부를 먼저 확인한 뒤, 나머지 3개 Variant도 각각 재검증.

## 4. Small Instance Matrix 테스트

[스펙 문서 §6](ASAK_FIGMA_OPTIONCARD_COMPONENT_SPEC_2026-07-17.md#6-검증-데이터-propertystate-조합-테스트용)의 6개 검증 데이터로 Sandbox 안에 작은 테스트 매트릭스를 만든다.

| 검증 항목 | 데이터/조합 |
|---|---|
| 짧은 이름 | 양배추라이스, 곤약라이스 |
| 중간 길이 이름 | 허니머스타드, 트러플오일, 통밀또띠아 (2줄 줄바꿈 확인) |
| 품절 | 베이컨칩, `state=soldOut` |
| 가격 있음/없음 | 동일 옵션에 `showPrice=true`/`false` 각각 |
| Secondary 있음/없음 | 동일 옵션에 `showSecondaryText=true`/`false` 각각 |

전부 스크린샷으로 확인하고, §3 체크리스트가 전부 PASS해야 다음 단계로 진행한다.

## 5. 마이그레이션 절차 (§3·§4 PASS 후, 별도 승인 후에만)

1. Component §3·§4 PASS 확인.
2. `508:44937`을 **다시 복제**(508:44937 자체는 건드리지 않음)해 새 Sandbox Pilot(가칭 `D1B_SANDBOX / Menu Detail Default`)을 만든다.
3. 그 복제본 안에서 일반 Frame 카드 **3개만** 시범적으로 정식 `Kiosk/OptionCard` Instance로 교체한다.
4. 교체한 3개와 `508:44937`(레퍼런스)을 나란히 스크린샷으로 비교해 시각 동일성을 확인한다(카드 크기, 색상, 텍스트 위치, 줄바꿈 동일해야 함).
5. 시각 동일성 PASS 후에만 나머지 43개(총 46개)도 정식 Component Instance로 전체 교체한다.
6. 구조 QA: `OptionGroup`의 `children` Slot 안에 일반 Frame이 하나도 안 남았는지, 46개 카운트 유지, Instance Detach 없음, 새 Component Set 추가 생성 없음(`Kiosk/OptionCard` 하나로 한정) 확인.
7. 이후에만 Production `134:7810` 적용을 **검토** — 실제 반영은 이 Work Order 범위 밖, 별도 승인 필요.

## 6. 완료 후 보고 형식

- Component 생성 스크린샷(4개 State 나란히)
- §3 바인딩 검증 체크리스트 결과(4개 Variant × 6개 Property)
- §4 Instance Matrix 스크린샷
- §5 마이그레이션 진행 시: 3개 시범 교체 Before/After, 시각 동일성 판정, 46개 전체 교체 후 구조 QA 결과
- 생성/변경 Node ID 전체 목록
- Production 미반영 확인
- 다음 지시 대기
