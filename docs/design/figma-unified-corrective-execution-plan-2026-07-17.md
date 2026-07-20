# ASAK Figma 종합 수정 실행 계획

> 기준 문서: `FIGMA_QA_UNIFIED_COMPLETE_2026-07-17.md`  
> 기준 파일: `JSrjOy668zhfkiLplCkreh`  
> 대상: Foundations, Shared, Kiosk Components/Screens, Admin Components/Screens  
> 원칙: **AI가 전체를 대신 고치지 않는다. 사람은 디자인 결정과 Figma 편집을 맡고, AI는 수치 추출·변경 목록·교차 검증·회귀 탐지를 맡는다.**

## 1. 결론

이번 작업의 목표는 “더 많은 QA”가 아니라 **고친 항목이 Master와 화면에 동시에 반영되고, 같은 문제를 다시 만들지 않는 구조**를 만드는 것이다.

따라서 66개 키오스크와 72개 관리자 화면을 한 번에 다시 디자인하지 않는다. 아래 5개 배치를 순서대로 닫는다.

1. **수정 전 잠금** — 실제 기준값·Variant 오류·중복 자산을 확정한다.
2. **키오스크 P0 Master** — BottomCTA, CategoryTab, Cart, Detail/Option을 고친다.
3. **관리자 P0 Master** — SaveBar, SoldOut, 조작 영역, Navbar/표를 고친다.
4. **Shared 상태 컴포넌트** — Confirm/Toast/Empty/Error를 기기별로 분기한다.
5. **화면 전파와 회귀 확인** — 해당 Screen ID만 반영·검증하고 다음 배치로 넘어간다.

한 배치는 “수정 → 해당 화면 반영 → 수치 재검증 → 완료 체크”까지 끝난 뒤에만 다음 배치로 간다. 중간에 새 이슈가 보여도 현재 배치의 범위를 바꾸지 않고 `다음 배치 후보`에 기록한다.

---

## 2. 역할 분리

### 사람이 직접 처리하는 편이 빠르고 정확한 작업

| 작업 | 사람이 해야 하는 이유 | AI가 제공할 보조물 |
|---|---|---|
| 우선순위 충돌 결정 | 예: CategoryTab 52px 유지 vs 64px, BottomCTA r12/16 vs r20은 브랜드 감각·현장 기기 크기 판단이 필요하다. | 선택지 비교표, 적용 화면 목록, 장단점. |
| Figma의 실제 배치·여백·시각 위계 수정 | 1~2px, 이미지 crop, 문장 길이, 한글 줄바꿈, 장식량은 캔버스를 직접 보고 판단해야 한다. | 수정 전/후 체크 기준, 수치 목록, screenshot QA. |
| 컴포넌트 삭제·병합·rename 확정 | instance 연결이 끊길 수 있다. `CategoryTap`, Deprecated, SaveBar 3벌은 팀이 실제 사용처를 확인해야 한다. | 사용처 후보 목록, rename mapping, 삭제 전 체크리스트. |
| 문구·업무 정책 확정 | Empty CTA, 결제 거절/네트워크 오류 CTA, Unauthorized 문구, 품절·환불 정책은 제품 결정이다. | Screen Bible 대조, 상태표, 문구 초안. |
| 실제 데이터 오류 수정 | `SCR-009` 총액 0원, `SCR-018` 좌우 불일치는 화면만 바꿔서는 해결되지 않을 수 있다. | DTO/계산 흐름 추적, 재현 조건, 테스트 항목. |
| 기기에서 최종 확인 | 키오스크 터치 반응과 관리자 태블릿 밀도는 실제 기기 또는 프로토타입에서 확인해야 한다. | 터치·대비·상태 QA 표. |

### AI가 맡으면 더 정확하고 반복 실수가 줄어드는 작업

| 작업 | AI 산출물 | 사람이 최종 확인할 것 |
|---|---|---|
| 수치 인벤토리 | node ID, frame 크기, text size/lh, Variant/Property, style 연결률, spacing 분포 | 추출 대상이 맞는지 1회 확인 |
| 변경 영향 목록 | Master 하나를 고쳤을 때 영향을 받는 Screen ID/상태/instance 목록 | 실제 의도된 재사용인지 |
| token·대비 검증 | hex 조합별 contrast, 라임 위 흰 텍스트, raw color/Primitive 사용 후보 | 사진·gradient·투명 overlay 예외 |
| 이름/Variant 정합성 검사 | `Variant4`, `sourse`, `status3`, `MenuDetailSummary`, `day` 오류와 중복 property 목록 | 최종 명명 규칙 승인 |
| 상태 회귀 QA | Default/Loading/Empty/Error/Disabled/SoldOut/Saving/Success의 누락·CTA 모순 목록 | 제품 정책상 예외 |
| 문서·체크리스트 갱신 | 배치별 완료표, 사람 확인 항목, 개발 전달용 px/token 표 | 실제 완료 여부 체크 |

### AI가 하지 않을 일

- 사용자 확인 없이 Figma 컴포넌트를 일괄 rename/delete/merge하지 않는다.
- “style 미연결 97%”만 보고 모든 텍스트에 일괄 Text Style을 적용하지 않는다. 같은 14px이라도 역할이 본문인지, 보조정보인지, 숫자인지 다르기 때문이다.
- 코드·API·가격 계산을 디자인 문제처럼 임의 수정하지 않는다.
- 하나의 QA 결과를 근거로 모든 화면을 다시 만들거나, 새 색/새 컴포넌트를 추가하지 않는다.

---

## 3. 작업 방식: 한 배치를 닫는 4단계

```text
1. AI가 수정 카드 작성
   - 대상 Master / Screen ID / 현재 node ID / As-Is / 선택지 / 완료 기준

2. 사람이 Figma에서 수정
   - 승인한 선택지만 수정
   - 화면 직접 배치와 한글 줄바꿈 확인

3. AI가 읽기 전용 재검증
   - 수치, Variant, Style binding, 상태 coverage, 영향 화면 비교

4. 사람이 완료 판정
   - "완료" / "보류" / "다음 배치" 중 하나를 기록
```

배치가 닫히는 조건은 “예쁘다”가 아니라 아래 모두를 만족하는 것이다.

- 해당 Master가 1개로 정해졌다.
- 지정된 Screen ID에서 override가 제거되거나 이유가 기록됐다.
- 해당 상태 프레임에 같은 CTA·텍스트·touch rule이 적용됐다.
- 수치 검증 결과가 완료 기준을 통과했다.
- 다음 배치로 넘길 이슈가 분리 기록됐다.

---

## 4. 수정 전 잠금 배치 — `B0`

### 목적

다른 화면을 고치기 전에 “어느 Master를 써야 하는지”와 “어떤 수치가 기준인지”를 정한다. 이 단계가 없으면 새 화면에서 Deprecated·Tap·예전 SaveBar가 다시 선택된다.

### 사람이 수정할 항목

| ID | 대상 | 사람 작업 | 완료 기준 |
|---|---|---|---|
| B0-01 | Foundations 표지 | 표지의 Primitive/Semantic 수치를 실제 `83 / 51`과 맞추거나 집계 기준을 명시 | 표지와 변수 컬렉션 수가 일치 |
| B0-02 | `day` `389:44743` | Figma Variant property 오류를 UI에서 직접 해소 | Variant property 조회 오류 0건 |
| B0-03 | naming | `Variant4`, `sourse`, `status3`, `MenuDetailSummary`의 최종 이름을 결정 | mapping 표에 old/new가 확정 |
| B0-04 | source of truth | CategoryTab/Tap, SaveBar 3벌, Payment row 2벌, Deprecated 세트의 “새 화면 사용 금지” 목록 승인 | 새 Master가 1개씩 지정 |

### AI가 처리할 항목

- rename mapping 문서화: old name → new name → 영향 Component/Screen ID → 사람이 확인할 instance.
- `day` 오류 해결 후 Variant property·옵션 수를 읽기 전용으로 재검증.
- Deprecated가 새 화면 instance에 남아 있는지 후보 목록 작성. 삭제는 사람이 승인한 뒤에만 한다.
- Foundations 변수 수, 14개 Text Style, 3개 Effect Style의 재검증 표 작성.

### B0에서 정하지 말 것

- MenuCard radius와 가격색처럼 시각 선택이 필요한 항목.
- 97% Style 미연결을 한 번에 해결하려는 작업.
- 화면 문구와 CTA 정책 변경.

---

## 5. 키오스크 P0 Master 배치 — `B1`

### 대상

`Kiosk/BottomCTA`, `Kiosk/CategoryTab`, `Kiosk/MenuCard`, `Kiosk/MenuDetailSummary`, `Kiosk/OptionGroup`, `Kiosk/OptionSelectionRow`, `Kiosk/CartItemCard`.

### 왜 먼저 하는가

SCR-003/004/005/007/008/012/013이 이 Master들을 공유한다. 특히 `SCR-008`의 `940×200` CTA override, CategoryTap 25×11, Cart의 Blue/13px/Admin MenuButton 혼입은 화면에 바로 드러나며 잘못된 재사용을 계속 만든다.

### 사람이 직접 수정할 카드

| ID | Master / Screen | 현재 문제 | 사람의 결정·수정 | 완료 기준 |
|---|---|---|---|---|
| B1-01 | CategoryTab / CategoryTap | Tap이 25×11이고 두 컴포넌트가 공존 | `Kiosk/CategoryTab`만 유지. Tap을 Deprecated로 분리한 뒤 Screen의 instance를 Tab으로 교체 | Tap instance 0, active/disabled가 Tab에서 표현 |
| B1-02 | BottomCTA + SCR-008 `134:7926` | Master 1080×180, SCR-008은 940×200 override | Master 1080×180 사용. radius는 `12/16` 또는 `20` 중 하나를 사람이 확정 | SCR-008이 Master 크기/Variant를 사용, loading label 16px 이상 |
| B1-03 | CartItemCard | Blue, 13px 액션, Admin/MenuButton 혼입 | Blue를 Foundations semantic 색으로 교체. 수정/삭제 action을 48px pill 또는 64px 터치 영역으로 재배치 | Blue `#3B82F6/#0088FF` 0, action text 16px 이상, Admin MenuButton instance 0 또는 wrapper 64px |
| B1-04 | MenuDetailSummary | 11~13px, Blue, legacy state | legacy state 제거/분리. 배지·이름·가격의 위계를 캔버스에서 결정 | badge 14px 이상, 이름 28px 이상, 가격 24px 이상, Blue 0 |
| B1-05 | OptionGroup/Row | 필수·설명 12~15px, 20px indicator가 실제 클릭처럼 보임 | row 전체를 터치 영역으로. selected border/check를 직접 확인 | 본문 16px 이상, label 18px, price 16px, row 64px 이상(권장 72px), selected 3px 이하 border + check |
| B1-06 | MenuCard | r0, AUTO, kcal 28px, sold-out 톤 약함 | radius·kcal 값을 팀이 확정하고 Auto Layout/line-height 적용 | r16 또는 승인값, kcal 16~24, line-height 명시, sold-out 텍스트 다운톤 |

### AI가 처리할 카드

- B1-01~06마다 기존 instance가 있는 Screen ID/상태 목록을 만든다.
- `#3B82F6`, `#0088FF`, 13px 이하 action text, 64px 미만 click candidate의 남은 수를 재검증한다.
- SCR-003/004/005/007/008/012/013의 Default·Loading·Error·SoldOut·Limit 상태에서 CTA 규칙이 모순되지 않는지 표로 비교한다.
- `SCR-008` CTA가 Figma Master의 크기·Variant·Text Style에 연결됐는지 검사한다.

### B1 전파 순서

1. Master 수정
2. SCR-008
3. SCR-003 Menu List
4. SCR-004 Menu Detail
5. SCR-005 Cart
6. SCR-007 Payment, SCR-012/013 overlay

이 순서를 지키면 같은 BottomCTA/Option/Toast 문제가 화면마다 따로 되살아나는 것을 막을 수 있다.

---

## 6. 관리자 P0 Master 배치 — `B2`

### 대상

`Admin/SaveBar`, `StickyActionBar`, `Admin/PaymentSaveBar`, `Admin/SoldOutCard`, `Admin/MenuButton`, `Admin/Checkbox`, `Admin/SearchInput`, `Admin/Navbar`, `Admin/DataTableRow`, `Admin/OrderActionButtons`.

### 사람이 직접 수정할 카드

| ID | Master / Screen | 현재 문제 | 사람의 결정·수정 | 완료 기준 |
|---|---|---|---|---|
| B2-01 | SaveBar 3벌 + SCR-011/016/018 | dirty tone이 `#292D30`, `#262626`, white로 갈리고 SCR-011은 이중 노출 | dirty/saving/error의 semantic 톤을 하나로 결정. Sticky/Payment를 같은 base로 병합할지 결정 | 새 화면 Master 1개, SCR-011 이중 bar 0, error semantic 일치 |
| B2-02 | SoldOutCard | 130×134, 9px 텍스트 | 카드 최소 150×160, 이름·보조문구 크기 수정 | 이름 13px 이상, 9px 0, selected/soldOut 의미 분리 |
| B2-03 | MenuButton / Checkbox / DateSelector | 16×16, 20×20, 35px | 아이콘은 유지하되 상위 click wrapper를 웹 40px, 태블릿 44px로 수정 | touch/click 영역 기준 통과 |
| B2-04 | SearchInput | Master 150×39 | 실제 admin 사용 폭을 240~320 중 선택하고 모든 관련 화면에 전파 | Master 폭과 화면 instance가 일치 |
| B2-05 | Navbar | shadow 4~8겹, breakpoint와 error가 같은 property | shadow 1개, viewport/mode/state를 분리 | Desktop/Tablet/Mobile과 Error가 서로 다른 property |
| B2-06 | DataTableRow / OrderAction | AUTO, hover 약함, refund가 일반 action처럼 보임 | row typography/hover 조정, 환불은 outline + confirm/danger로 구분 | row 48px 이상(조작 row 56px), hover 존재, refund confirm 연결 |
| B2-07 | SCR-009 / SCR-018 | 총액 0원, 중복 알림 / payment 좌우 불일치 | 제품·개발 담당자가 실제 데이터 및 상태 정책을 결정 | `priceCalculation`과 화면 값 비교, 알림 1개, 좌우 상태 동기 |

### AI가 처리할 카드

- SaveBar 세트의 색/높이/상태/사용 Screen ID 비교표를 제공한다.
- Admin 화면의 9px/10px 텍스트, `auto` line-height, 40/44 미만 컨트롤 후보를 재추출한다.
- SCR-009의 총액 재현 조건과 priceCalculation 입력/출력 검증 항목을 작성한다. 실제 코드 수정은 팀원이 한다.
- SCR-018의 toggle 이름·선택 상태·저장 bar 상태가 좌우 panel에서 같은지 비교한다.
- SCR-010/011/016/018/019~022의 Default/Loading/Empty/Error/Save 상태를 확인한다.

---

## 7. Shared 상태 컴포넌트 배치 — `B3`

### 사람이 직접 수정할 카드

| ID | 대상 | 사람 작업 | 완료 기준 |
|---|---|---|---|
| B3-01 | ConfirmDialog | Admin 440×248은 유지하고 키오스크 560~680 Variant를 추가할지 결정. warning 텍스트를 dark로 수정 | 라임 위 white 0, title 18/24 이상, 키오스크 CTA 56px 이상 |
| B3-02 | Toast | Admin 299×76은 유지, Kiosk size를 별도 정의 | kiosk toast 폭 400px 이상, 본문 16px 이상, 높이 80px 이상 |
| B3-03 | Empty/Error | CTA를 type별로 결정: Cart=메뉴 담으러 가기, Menu=새 메뉴 추가 등 | radius 12, raw `#ccc` 0, CTA 문구/목적이 상태와 일치 |
| B3-04 | Allergen | warning text semantic과 Tag radius 결정 | warning contrast 4.5:1 이상, desc 16px 이상, tag r8 |
| B3-05 | Loading | Skeleton gray를 semantic token 하나로 통일 | card/table/page/button에서 동일 semantic 사용 |

### AI가 처리할 카드

- confirm type×tone×state와 error type×layout의 “실제로 허용되는 조합표”를 작성한다.
- Kiosk와 Admin이 같은 Toast/Modal을 쓸 때 size Variant가 정확히 선택됐는지 검증한다.
- contrast matrix와 raw color/Primitive 사용 후보를 다시 뽑는다.

---

## 8. Text Style 연결 배치 — `B4`

### 이 작업을 마지막에 하는 이유

Kiosk 97.4%, Admin 97.8%의 Text Style 미연결은 반드시 해결해야 한다. 하지만 숫자만 줄이려고 한 번에 Style을 덮어쓰면 Summary/Option/Table/Toast의 위계가 무너진다. B1~B3에서 Master의 역할을 먼저 확정한 뒤 연결한다.

### 적용 순서

1. Foundations의 14개 Style 이름/size/line-height를 lock한다.
2. Shared Master에 적용한다.
3. Kiosk Master에 적용한다.
4. Admin Master에 적용한다.
5. 화면은 Master로 해결되지 않는 override만 사람이 직접 처리한다.

### 화면별 최소 규칙

| 영역 | 허용 Text Style | 금지 |
|---|---|---|
| Kiosk 본문/선택 row | Body M 16/24 이상 | 12~15px 조작 텍스트, AUTO lh |
| Kiosk CTA | Label L 20/24 이상, BottomCTA는 24/30 이상 | 15px loading label |
| Kiosk 결과/가격 | Number M 26/32 이상 | 가격 18px 이하 |
| Admin 표 본문 | Body S 14/20 또는 Label S 12/16 | 9~10px, AUTO lh |
| Admin KPI | Number M/L/XL | 일반 Body로 금액 표시 |
| 오류/보조문구 | Label S 12/16 이상 | 12px 미만, 색만으로 오류 전달 |

### AI가 완료로 판정하는 수치

- 새로 수정한 Master의 Text Style ID 미연결: 0개
- 새로 수정한 화면의 신규 텍스트 `AUTO` line-height: 0개
- Kiosk 조작 텍스트 16px 미만: 0개
- Admin 9~10px 텍스트: 0개

기존 화면의 미연결 수가 남아 있어도 배치를 닫을 수 있다. 단, 남은 노드는 Screen ID와 이유를 backlog에 적고 다음 범위를 명확히 한다.

---

## 9. 화면 전파·회귀 배치 — `B5`

### Screen 우선순위

| 우선 | Screen ID | 확인해야 할 핵심 |
|---:|---|---|
| 1 | SCR-008 | BottomCTA `940×200` override 제거, loading/disabled/complete CTA |
| 2 | SCR-005 | Cart Blue, 13px, MenuButton, dialog 680/440, checkout block |
| 3 | SCR-004 | option font/touch/selected, legacy Summary, limit/sold-out/error |
| 4 | SCR-003 | CategoryTab, Empty/Error CTA, toast, loading CTA 정책 |
| 5 | SCR-011 | SoldOut 9px, SaveBar/Sticky 이중 노출 |
| 6 | SCR-018 | PaymentSaveBar, toggle 이름/상태, 좌우 동기 |
| 7 | SCR-009 | total 0원, 주문 알림 중복, row/취소 동작 |
| 8 | SCR-016 | menu name, empty CTA, validation/save states |
| 9 | SCR-010/015/019~022 | table hover, login error, sales partial/empty/error |

### 상태별 종료 조건

| 상태 | 반드시 확인할 것 |
|---|---|
| Default | Master instance, typography, semantic color, hit target |
| Loading | CTA 재탭 방지, skeleton/label 위치, layout shift 없음 |
| Empty | 상태에 맞는 CTA와 문구, raw color 없음 |
| Error | 복구 CTA가 원인에 맞음, contrast 4.5:1 이상 |
| Disabled | opacity만 사용하지 않음, 클릭 불가와 이유가 보임 |
| SoldOut | 메뉴/옵션/장바구니/결제 차단이 같은 정책 |
| Saving/Success | save bar와 toast가 중복되지 않음 |

---

## 10. 사람이 작업할 때 쓰는 15분 단위 카드

한 번에 한 카드만 연다. 아래 양식을 복사해 작업 로그에 남긴다.

```md
## [B1-02] BottomCTA + SCR-008

- 목표: SCR-008 CTA를 Master 1080×180에 연결하고 loading 16px 이상으로 만든다.
- 수정 범위: Kiosk/BottomCTA, SCR-008 / Order Complete / Default
- 하지 않는 것: 다른 Complete 화면 문구 변경, 새 색상 추가
- 사람 결정: radius = [12/16 | 20]
- 수정 후 확인:
  - [ ] instance가 BottomCTA Master
  - [ ] 1080×180
  - [ ] loading label 16px 이상
  - [ ] disabled가 opacity-only가 아님
- AI 재검증 요청: node 크기 / variant / style / screen override 비교
- 결과: 완료 | 보류 | 다음 배치
```

이 양식이 중요한 이유는 AI에게 “전체 피그마 다시 점검해줘”라고 요청하지 않고, **닫을 수 있는 한 개의 목표**만 주기 위해서다.

---

## 11. 이번 주 완료 정의

### 반드시 끝낼 것

- [ ] B0: 표지 83/51, `day` Variant, naming/source-of-truth 확정
- [ ] B1-01: CategoryTap 제거 또는 Deprecated 분리 + 화면 instance 교체
- [ ] B1-02: SCR-008 BottomCTA override 제거
- [ ] B1-03: Cart Blue/13px/Admin MenuButton 문제 제거
- [ ] B2-01: SaveBar 3벌의 새 Master 지정 + SCR-011 이중 노출 제거
- [ ] B2-02: SoldOutCard 9px 제거
- [ ] B3-01/B3-02: Kiosk Confirm/Toast size Variant 확정

### 다음 주로 넘겨도 되는 것

- 66/72개 프레임 전체의 Text Style 100% 연결
- Admin Navbar 장식/shadow의 미세 polish
- 모든 화면의 radius·spacing 미세 통일
- Sales/TopHeader/StatusBadge의 Master 정리(실사용 여부 확인 후)
- extension screens SCR-023/024의 신규 QA

---

## 12. 검증 기록표

| 배치 | 사람 수정 완료 | AI 읽기 전용 재검증 | 결과 | 다음 조치 |
|---|---|---|---|---|
| B0 기준 잠금 | ⬜ | ⬜ | 대기 | — |
| B1 키오스크 P0 Master | ⬜ | ⬜ | 대기 | — |
| B2 관리자 P0 Master | ⬜ | ⬜ | 대기 | — |
| B3 Shared 상태 | ⬜ | ⬜ | 대기 | — |
| B4 Text Style | ⬜ | ⬜ | 대기 | — |
| B5 화면 전파 | ⬜ | ⬜ | 대기 | — |

## 13. 남은 위험

- Figma 수정은 instance 연결, property 값, component binding을 끊을 수 있다. 사람 수정 후 AI 검증을 반드시 한 번 둔다.
- 같은 14px 텍스트라도 역할이 다르다. Style 연결은 수치 일괄치환이 아니라 역할 단위로 한다.
- `SCR-009` 총액 0원, `SCR-018` 상태 불일치는 Figma만 고쳐도 해결되지 않을 수 있다. 화면·mock·backend contract를 함께 확인한다.
- 권장값이 서로 다른 항목(예: Tab 52 vs 64, CTA radius 12/16 vs 20)은 팀이 한 값을 결정하기 전까지 AI가 임의로 고정하지 않는다.

## 14. 공부 포인트

- Master를 먼저 고치고 Screen override를 지우는 것은 “디자인 통일”이 아니라 재발 방지 장치다.
- AI는 많은 노드의 차이·누락을 빠뜨리지 않고 찾는 데 강하고, 사람은 그 차이가 실제 제품 경험에 맞는지 판단하는 데 강하다.
- 가장 좋은 협업 단위는 전체 파일이 아니라 `Master 1개 + 영향 Screen 3~7개 + 완료 수치`다.

---

## 15. 출처 운영 원칙 — 누구와 진행하고, 누구에게 검증받을지

### 결론

**한 출처를 전체 정답으로 쓰지 않는다.**

- 계속 수정 진행의 기준은 **B + A**다.
  - **B(Cursor 컴포넌트)**: Master의 현재 구조·Variant·속성·재사용 문제를 가장 직접적으로 다룬다.
  - **A(Cursor 스크린 실측)**: 수정한 Master가 실제 05-C/06-C 프레임에서 어떻게 override됐는지 수치로 확인한다.
- 배치 종료의 객관 검증은 **D(Codex 정량)**가 맡는다.
- 상태·데이터·화면 흐름의 검증은 **C(Claude v2)**가 맡는다.
- 최종 시각 품질·터치·가독성 검증은 **E(Figma DS QA)**가 맡는다.
- 최종 결정권은 항상 **팀원(사람)**에게 있다.

이렇게 나누면 “AI 의견 5개를 다시 합치는 작업”을 반복하지 않고, 각 출처가 잘하는 한 가지 역할만 수행한다.

### 출처별 신뢰 범위와 역할

| 출처 | 가장 잘하는 것 | 계속 진행에 쓰는 방식 | 검증 역할 | 단독 결정하면 안 되는 것 |
|---|---|---|---|---|
| **A — Cursor 스크린 실측** | 실제 Screen frame 크기, override, 화면별 문제 위치 | B1/B2 수정 후 영향을 받는 SCR 프레임을 전파할 때 기준으로 사용 | `940×200`, Dialog 680/440, gap 218, 9px처럼 **화면 실측값** 확인 | Master 구조의 최종 설계, 브랜드 감각 |
| **B — Cursor 컴포넌트** | Master Variant, Property, component 간 중복/혼입 | **B0~B3의 주 진행 출처**. Master 하나를 고칠 때 가장 먼저 참조 | Variant/Property 이름, component source of truth, Deprecated 분리 | 실제 모든 Screen에서 쓰이는지 여부 |
| **C — Claude v2** | Master 결함이 실제 화면/상태/데이터 흐름에 미치는 영향 | 수정 진행의 주 기준이 아니라, B1/B2에서 화면 동작이 걸린 항목만 요청 | Loading CTA, 총액 0원, SaveBar 이중 노출, Unauthorized/품절/결제 상태의 정책 검증 | 단일 수치·시각값의 최종 확정. 일부 Master 문제는 화면 실사용 0건으로 하향됐으므로 재현 여부가 선행돼야 함 |
| **D — Codex 정량** | 변수 수, Style binding, Text size/lh, 색 대비, hit target, Node/Variant 오류, coverage | 수정하지 않고 배치 전·후의 수치를 기록 | **모든 배치의 종료 게이트**. 완료 기준을 수치로 PASS/FAIL | 한글 줄바꿈, 이미지 crop, 장식량 같은 시각 판단 |
| **E — Figma DS QA** | 터치 UX, 가독성, 위계, Auto Layout, 위험 행동의 시각 구분 | B1/B2/B3의 사람이 고친 결과를 다듬는 마지막 단계에서 사용 | 키오스크/태블릿 크기, title/body hierarchy, hover, focus, destructive action 품질 검증 | 실제 node 사용처·실제 데이터·팀의 브랜드 선택 |

### 근거 우선순위

출처가 서로 다르게 말하면 아래 순서로 판정한다.

```text
현재 Figma 원본 + 실제 제품 정책
  > A/B/D의 현재 실측·구조 근거
  > C의 화면/상태 교차 재현 근거
  > E의 디자인 시스템 권고
  > 과거 문서의 서술값
```

예를 들어 E가 Tab 64px을 권고해도, 현재 실제 키오스크의 사용 환경과 A/B의 52px 실측을 보고 팀이 52 또는 64 중 하나를 선택한다. E의 권고는 강한 품질 기준이지만, 현재 Figma의 사실을 덮어쓰는 근거는 아니다.

### 출처 충돌 처리 규칙

| 충돌 항목 | 현재 의견 | 처리 방식 | 결정 주체 |
|---|---|---|---|
| Kiosk CategoryTab 높이 | B/C는 약 52px, E는 64px 권고 | 실제 기기에서 52px 탭을 눌러 보고 64px과 비교. 선택 뒤 token/Variant에 하나만 남김 | 사람 |
| BottomCTA radius | B는 12/16, E는 20 | SCR-008 포함 대표 3개 화면을 같은 캔버스에서 비교. 한 값을 결정하면 Master만 수정 | 사람 |
| MenuCard kcal | B는 20~24, E는 16 | 정보 우선순위에 따라 선택. 메뉴명/가격보다 약하게 보이면 16, 영양정보가 핵심이면 20~24 | 사람 |
| MenuCard 가격색 | B/C `#6C9700`, E `#4A7A00` | white/dark surface 각각 대비와 브랜드 시안을 확인. Semantic token 하나로 확정 | 사람 + D 대비 검증 |
| Error CTA 색 | A/B는 라임 스케일, E는 dark CTA | 오류의 복구 행동이 primary인지 secondary인지 제품 정책을 먼저 확정. 동일 상태에는 한 규칙만 사용 | 사람 + C 상태 검증 |
| StatusBadge 긴급도 | A/B는 P0, C는 화면 실사용 0으로 하향 | Master 오류는 B0에서 고치되, 화면 전파는 실제 instance 발견 시에만 B5에 넣음 | B + A + D |
| Live Order gap 218 | A/B는 재현, C는 미재현 | A의 node ID를 기준으로 현재 frame을 다시 확인. 값이 없으면 backlog, 있으면 B2-06에서 수정 | A + D |

### 배치별 출처 운영표

| 배치 | 수정 진행 기준 | 수정 후 첫 검증 | 배치 종료 검증 | 사람의 확인 |
|---|---|---|---|---|
| B0 기준 잠금 | **B** | D: Variant/Property/변수 수 | D: 오류 0, source-of-truth 1개 | rename·Deprecated·삭제 승인 |
| B1 키오스크 Master | **B** | A: SCR-003/004/005/007/008 실측 전파 | D: 색·폰트·hit target·override | E: 터치 크기/시각 위계, C: Loading·SoldOut·Limit 흐름 |
| B2 관리자 Master | **B** | A: SCR-009/011/016/018 실측 전파 | D: 9px/AUTO/wrapper/상태 수치 | E: table/hover/refund, C: total/save/toggle 동작 |
| B3 Shared 상태 | **B** | A: kiosk/admin 사용 프레임 크기 | D: contrast/size/allowed Variant | E: modal/toast/error visual, C: 오류 복구 정책 |
| B4 Text Style | **D** | B: Master 역할 확인 | D: Style binding/AUTO 수치 | 사람: 한글 줄바꿈·위계 |
| B5 화면 회귀 | **A** | C: 상태·데이터 교차 | D: frame/coverage/hit target | E: 대표 화면 100% scale 최종 QA |

### 실제 진행 요청 템플릿

출처에게 전체 문서를 다시 주고 “전부 검토”라고 요청하지 않는다. 아래처럼 배치와 역할을 고정한다.

```md
[진행 요청]
배치: B1-03 CartItemCard
대상: Kiosk/CartItemCard + SCR-005 Default / Item Sold-out / Checkout Blocked
당신 역할: B(컴포넌트 Master 기준)
할 일: Variant/Property/중복 컴포넌트만 확인하고 수정 후보를 1개 mapping 표로 제시
하지 않을 일: 화면 전체 재디자인, 새 색상 제안, 코드 수정
완료 기준: Blue 0, action 16px+, Admin/MenuButton 혼입 처리 방식 명시
```

```md
[검증 요청]
배치: B1-03 CartItemCard
당신 역할: D(정량 검증)
할 일: 수정 후 해당 Master와 SCR-005 3개 상태만 읽기 전용 비교
PASS 기준: #3B82F6/#0088FF 0, action 16px+, click wrapper 64px+, style/lh 명시
출력: PASS/FAIL + 남은 node ID만
```

이 방식이면 B가 수정 방향을 넓히지 않고, A/D/C/E가 서로 같은 이야기를 반복하지 않는다.

### 최종 추천 조합

| 목적 | 계속 함께할 출처 | 검증 출처 |
|---|---|---|
| Figma Master 정리 | **B** | D |
| Screen override/전파 | **A** | D |
| 키오스크 터치·폰트·위계 | 사람 + E | D |
| 관리자 업무 화면·상태 | 사람 + B | C + D |
| 토큰/Text Style/대비 | D | 사람 + E |
| 데이터/업무 흐름 오류 | 사람 + 개발 담당 | C + D |
