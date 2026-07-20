> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: Dated Figma merge analysis.
> Canonical Replacement: `docs/design/README.md`
> Original Path: `docs/design/ASAK_FIGMA_1_2_MERGE_ANALYSIS_2026-07-14.md`

# ASAK 1 · ASAK 2 분석 및 병합 제안

> 작성일: 2026-07-14  
> 대상 파일
>
> - **ASAK 1**: `k67gDKvnB29ILSzIpFYSaT` — [Figma](https://www.figma.com/design/k67gDKvnB29ILSzIpFYSaT/ASAK-1?node-id=2004-9)
> - **ASAK 2**: `UkpdbylxruMqzf6bSzZ4Rb` — [Figma](https://www.figma.com/design/UkpdbylxruMqzf6bSzZ4Rb/ASAK-2?node-id=2002-6)
> - 원본 Legacy: `o9mxSeovLQPdWNwM4mNySk` — 수정 금지

## 결론

두 파일을 동등한 운영 파일로 계속 유지하는 것보다, **ASAK 2를 실제 디자인의 기준 파일로 삼고 ASAK 1의 Handoff/Code Connect 명세를 ASAK 2로 흡수하는 병합**이 가장 효율적이다.

병합의 목적은 화면을 다시 그리는 것이 아니라, 중복된 파일·문서·컴포넌트 기준점을 하나로 줄이고 개발자가 단일 Figma 파일에서 화면, 컴포넌트, 토큰, 코드 매핑을 모두 확인할 수 있게 하는 것이다.

## 파일별 역할과 현재 강점

| 구분 | ASAK 1 | ASAK 2 |
| --- | --- | --- |
| 현재 강점 | 화면 ID·Route·React 페이지·상태·Code Connect 대상을 명시한 Handoff 문서 | 실제 키오스크/관리자 화면, 상태 화면, 마이그레이션된 자산과 감사 기록 |
| 확인한 핵심 페이지 | `08. Handoff / Specs` | `05. Screens / Kiosk` |
| 화면 인벤토리 | 대표 화면 20종의 Route/상태/코드 매핑이 명확 | 실제 SCR 프레임 35개(기본·상태·접근성 포함) 기준의 운영 구조 |
| 컴포넌트 관점 | Code Connect 대상으로 삼을 Component Set과 코드 경로가 잘 정리됨 | 정식 페이지 자산이 많고 실제 화면의 인스턴스 연결을 목표로 마이그레이션 진행됨 |
| Foundation/상태 | 명세 중심 | Color/Layout/Type/Effect 및 loading·empty·error 상태를 포함한 실물 중심 |
| 프로토타입 | 시작점과 연결 의도가 문서화됨 | 연결표는 존재하지만 실제 Figma interaction은 미설정 |

## 확인된 차이와 주의점

### 1. ASAK 2는 화면 실물이 더 많지만, 일부 화면은 아직 인라인 구조다

ASAK 2의 `SCR-003 / Kiosk / Menu List / State=Default`에서 다음 항목이 확인됐다.

- `Legacy/CategoryTab (hardcoded)` 인스턴스가 남아 있음
- 반복 메뉴 카드 내부에 `Rectangle 8424`, `Frame 2113` 같은 자동 생성 이름이 있음
- 반복 메뉴 카드가 정식 `Kiosk/MenuCard` 인스턴스보다 인라인 프레임 구조에 가까움

따라서 ASAK 2의 감사 문서에 적힌 “Legacy 참조 0”은 화면 전체가 완전히 정식 Component Set만 참조한다는 의미로 바로 해석하면 안 된다. 병합 전에 실제 화면 인스턴스와 감사 문서의 수치를 한 번 더 맞춰야 한다.

### 2. ASAK 1은 명세가 강하지만 실제 캔버스의 최신 상태를 보장하지 않는다

ASAK 1의 Handoff에는 화면별 route, 상태, React 코드 파일, Component Set 속성이 잘 정리되어 있다. 다만 그 문서가 ASAK 2의 최신 상태 화면·신규 자산·최종 컴포넌트 이동 결과까지 모두 반영했는지는 별도로 검증해야 한다.

### 3. 두 파일을 모두 개발 기준으로 쓰면 기준점이 갈린다

개발자가 ASAK 1의 Code Connect 표와 ASAK 2의 실제 화면을 번갈아 참조하면 다음 문제가 생긴다.

- 어느 파일의 컴포넌트가 최종인지 불명확함
- 동일 컴포넌트의 property/variant 명세가 다를 수 있음
- 상태 화면 수와 Screen Inventory 수가 다르게 보일 수 있음
- 수정 사항이 두 파일에 분산돼 재동기화 비용이 생김

## 병합하면 좋은 점

1. **개발 기준점 단일화**
   - 화면, Component Set, variables, Handoff, Code Connect 후보가 한 파일에 모인다.
   - 내일 MCP/Code Connect 작업 시 파일 선택 오류가 줄어든다.

2. **실제 화면과 명세의 정합성 확보**
   - ASAK 2의 35개 SCR 프레임에 ASAK 1의 route/code/state 정보를 대응시킬 수 있다.
   - Screen Inventory를 “화면 종류”와 “실제 상태 프레임”으로 분리해 혼동을 없앨 수 있다.

3. **컴포넌트 중복 감소**
   - ASAK 1의 Code Connect 매핑 대상 목록을 기준으로 ASAK 2의 정식 Component Set을 확정할 수 있다.
   - `-Legacy`, hardcoded CategoryTab, 인라인 MenuCard처럼 남은 중복/미정리 항목을 한 번에 추적할 수 있다.

4. **개발 연동 준비도 향상**
   - Figma Component Set → React 파일 경로를 실제 사용 중인 컴포넌트에만 연결한다.
   - 화면 프레임이 아니라 재사용 가능한 최상위 Component Set을 Code Connect 대상으로 유지할 수 있다.

5. **향후 화면 수정 비용 감소**
   - 특히 예정된 관리자 화면 수정이 단일 토큰/컴포넌트 체계에서 이뤄진다.
   - 수정 후 ASAK 1과 ASAK 2를 다시 맞춰야 하는 작업이 사라진다.

## 권장 병합 전략

### 병합 대상과 최종 파일

- **최종 운영 파일:** ASAK 2
- **가져올 기준:** ASAK 1의 `08. Handoff / Specs` 문서 구조와 Code Connect 매핑 정보
- **보존 파일:** ASAK 1은 즉시 삭제하지 않고 `ASAK 1 — Superseded Reference`로 읽기 전용 보관
- **원본 Legacy:** 계속 수정 금지

### 안전한 순서

```text
1. ASAK 2를 기준 파일로 고정
2. ASAK 1의 Handoff 정보만 ASAK 2의 08. Handoff / Specs에 복사
3. 실제 ASAK 2 node 기준으로 Screen/Component Inventory 재검증
4. ASAK 1과 ASAK 2의 이름·property·코드 경로 충돌을 해소
5. ASAK 2의 미정리 인라인 요소를 정식 Component Set으로 치환
6. Code Connect 대상 확정
7. ASAK 1을 reference/archive로 전환
```

### 가져와야 할 내용

| ASAK 1에서 가져올 것 | ASAK 2에서 기준으로 삼을 것 |
| --- | --- |
| Screen ID, Route, 코드 페이지/컴포넌트 매핑 | 실제 SCR frame과 상태 frame |
| Component Set별 properties와 React 파일 경로 | 실제 Component Set, instance, variant/property 이름 |
| Prototype Start 명세 | User Flow/수동 연결표 |
| Code Connect 대상 원칙 | Color/Layout/Type/Effect/Gradient 및 실제 화면 디자인 |

### 가져오지 말아야 할 것

- ASAK 1의 화면 프레임을 ASAK 2에 통째로 중복 복사하는 작업
- 동일 기능의 Component Set을 이름만 바꿔 추가하는 작업
- ASAK 2에 이미 존재하는 styles/variables의 복제본
- 원본 Legacy의 삭제 또는 이동

## 병합 전 필수 검증

- [ ] ASAK 2의 Screen Inventory가 실제 SCR 프레임 수와 일치한다.
- [ ] 기본 화면 수와 상태 화면 수를 별도 열로 기록한다.
- [ ] ASAK 1의 Code Connect 경로가 실제 `frontend/src` 파일과 일치한다.
- [ ] `Shared/Button`, `Shared/Modal`, `Shared/Badge`, `Kiosk/MenuCard`, `Kiosk/CategoryTab`, `Kiosk/CartItem`, `Kiosk/PaymentMethodCard`의 최종 Component Set이 하나씩만 지정된다.
- [ ] ASAK 2의 `SCR-003`은 hardcoded CategoryTab과 인라인 MenuCard를 정식 인스턴스로 교체하거나, 보류 사유를 문서화한다.
- [ ] `-Legacy`는 화면·다른 Component Set·Archive 중 어느 곳에서 참조되는지 구분해 기록한다.
- [ ] Legacy variables/styles는 실제 화면이 신규 토큰으로 전환된 뒤에만 삭제 후보로 분류한다.
- [ ] 프로토타입은 병합 범위와 분리한다. 연결표만 유지하고, 실제 reaction 연결은 별도 수동 작업으로 둔다.

## 병합 후의 이상적인 파일 구조

```text
ASAK — Design System & Product UI
├─ 00. START HERE
├─ 01. Foundations
├─ 02. Components / Shared
├─ 03. Components / Kiosk
├─ 04. Components / Admin
├─ 05. Screens / Kiosk
├─ 06. Screens / Admin
├─ 07. User Flows & Prototype
├─ 08. Handoff / Specs
│  ├─ Screen Inventory (actual frames + states)
│  ├─ Component Inventory (final Component Sets)
│  ├─ Code Connect Mapping
│  └─ Asset Migration Inventory
└─ 99. Archive / Imported Legacy
```

## 최종 권고

병합은 가치가 높지만, “두 파일을 합쳐 복사”하는 방식으로 진행하면 중복 컴포넌트와 token 충돌이 커질 수 있다. **ASAK 2의 실제 화면과 자산을 유지한 채, ASAK 1의 Handoff/Code Connect 명세만 선별적으로 이식**하는 방식으로 진행한다.

병합 완료 뒤에는 ASAK 2만 개발·디자인의 운영 기준으로 사용하고, ASAK 1은 원본 보존을 위한 참고 파일로만 유지한다.
