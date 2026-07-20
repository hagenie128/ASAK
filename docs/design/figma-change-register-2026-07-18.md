# ASAK Figma 변경 레지스터

> 이 파일만 작업판으로 사용한다. A~E 출처 문서는 **근거 보관용**으로 유지하고 새 통합 문서는 만들지 않는다.

## 0. 최초 1회 병합과 고정 파트너

`figma-qa-unified-complete-2026-07-17.md`를 A~E 원본 의견의 **동결된 근거 묶음**으로 쓴다. 즉, 원본 문서를 다시 서로 이어 붙이지 않는다. 아래 M0 순서로 근거를 이 변경 레지스터의 Change ID에 한 번만 배치한 뒤, 그 다음부터는 Change ID만 수정한다.

| 순서 | 사용자와 함께할 파트너 | 담당 범위 | 산출물 | 참여 금지 범위 |
|---|---|---|---|---|
| **M0-1** | **B (Cursor Component Audit)** | Foundations, Shared, Kiosk/Admin **Master**의 이름·Variant·token·크기 | 각 문제를 Change ID에 연결하는 Master 근거 | Screen 전파 판단, 상태 정책, 새 전체 계획 작성 |
| **M0-2** | **A (Cursor Screen Measurements)** | Master 문제가 실제 `SCR-*` 화면에 남은 위치·override·Frame 수치 | Screen ID, node ID, 실제 수치 | Master 구조 재설계, 권장 디자인 결정 |
| **M0-3** | **D (Codex 정량 QA, 병합 담당)** | M0-1/2 중복 제거, 수치 기준·완료 기준 확정 | 이 레지스터의 Change ID 1개당 근거 1묶음 | Figma 수정 지시 변경, 제품 취향 결정 |
| **M0-4** | **C (Claude 상태·흐름 검토)** | 저장/품절/결제처럼 상태·데이터가 바뀌는 Change ID만 보강 | 재현 조건, 필요한 상태, 정책 충돌 | 색·여백·타이포 재평가 |
| **M0-5** | **E (Figma DS QA)** | 사람이 고친 뒤 터치·대비·가독성 최종 확인 | 유지/수정 필요, 권장값 | Master 또는 Screen의 새 문제 목록 작성 |
| **M0-6** | **사용자** | 충돌 선택과 실제 Figma 수정 | Decision ID 결정, 상태 변경 | AI에게 수정 권한 넘기기 |

### 파트너 고정 규칙

- **당신이 동시에 만날 파트너는 한 명뿐이다.** `B → A → C → E` 순서이며, D는 병합·PASS/FAIL만 하는 중간 관리자다.
- **B가 구조 담당, A가 화면 담당**이다. 같은 Change ID라도 B가 Master를 먼저 확정하고 A는 그 변경이 적용된 Screen만 확인한다.
- **C는 `B2-01`(SaveBar 상태)처럼 상태가 있는 행에만**, **E는 사람 수정 완료 뒤에만** 호출한다. 둘은 앞 단계의 작업을 다시 열 수 없다.
- D는 어떤 파트너의 "새 계획을 같이 하자" 요청도 받지 않고, 이 문서의 `Change ID`에 없는 의견은 `보류 근거`로만 기록한다.
- 최종 선택권은 사용자에게 있다. 의견이 충돌하면 `DEC-*`만 만들고, 결정 전에는 어느 출처도 자신 안을 확정안으로 바꾸지 못한다.

### 실제 진행 순서

1. **지금:** B와 `M0-1`만 한다. B0~B3 및 B1/B2/B3의 Master 문제를 기존 Change ID에 연결한다.
2. **그 다음:** A와 `M0-2`를 한다. B가 연결한 Change ID마다 영향받는 `SCR-*`, node ID, override를 붙인다.
3. **그 다음:** D가 `M0-3`으로 중복을 합쳐 한 행당 "수정 1회 + 검증 1회"가 되게 정리한다.
4. **그 뒤에야:** `B0-01`부터 사람이 Figma를 수정한다. 수정 중 C/E를 부르지 않는다.
5. 상태가 있는 행만 C, 사람 수정이 끝난 행만 E, 모든 행의 최종 수치 확인은 D가 맡는다.

### 각 파트너에게 처음 보내는 고정 요청문

```text
현재 단계: M0-1
당신 역할: B (Master 구조 근거만 담당)
대상: FIGMA_CHANGE_REGISTER의 기존 Change ID
해야 할 일: 각 Change ID에 Master / Variant / Property / 현재 수치만 연결
하지 말 일: 새 전체 계획, Screen 재디자인, 다른 출처 의견 재정리
출력 형식: Change ID | Master node | as-is 수치 | 수정 필요 속성 | instance 영향
```

## 0718 복구 배치 (2026-07-18) — 완료 요약

**쓰기 타깃:** `yHhvn5RKjBd91U8BJUQz7F` (0718)  
**참고:** ASAK-1 · 0714(화면 시각) · 0715 **구분선 아래** 컴포넌트/화면 보관본  
**정본 표:** [figma-0718-color-canon-2026-07-18.md](./figma-0718-color-canon-2026-07-18.md)

| Phase | 내용 | 결과 |
|---|---|---|
| 0 | 색·파일 정본 표 | 완료 |
| 1 | Master TEXT→BG/Surface 오바인딩 | Shared 41 · Admin 2 · Kiosk 0 → **잔여 0** |
| 2 | BottomCTA disabled opacity 제거 · loading→Brand/Subtle · Blue/Orange 표 재바인딩 | 완료 · `Semantic/Category/Side`·`WarningText` 추가 |
| 3 | 갭 | CategoryTap→Deprecated · StickyActionBar Master 04-C 재부착 · 0715 아래는 반입 창고로 유지 |
| 4 | 05-C/06-C 화면 Blue/Orange override | Kiosk Blue 3 · Admin Blue 206 + Orange 192 |
| — | 표 밖 unbound hex | 바꾸지 않음 · 캐논 문서에 목록만 |
| 5 | 화면 조합 (잘 데려가기) | 맵 문서 · 키오스크/Admin Core·QA 섹션 · SCR-008/001/003 정리 · Archive Default ID 확정 |

**조합 맵:** [figma-0718-screen-combine-map-2026-07-18.md](./figma-0718-screen-combine-map-2026-07-18.md)

### 지금 할 일

1. 0718에서 Modal / BottomCTA / SaveBar / MenuButton side·drink 눈 QA
2. 깨진 Default만 수동 복붙  
   - 키오스크 → **0714**  
   - Admin → **0715 Archive** (`525:19726` 등, 맵 표 참고)  
   - 붙여넣은 뒤 **0718 로컬 Semantic만** 재바인딩 (**Figma AI bulk 금지**)
3. 기존 Change ID(B0/B1…)는 수치·구조 이슈용으로 유지 — 색·조합과 섞지 않음

**한 번에 한 행만 진행한다.** 새 의견은 아래 Change ID에 덧붙이고, 같은 대상의 새 문서를 만들지 않는다.

## 상태값

`대기` → `사람 수정 중` → `AI 검증 요청` → `PASS` 또는 `보류`

`보류`는 의견 충돌 또는 제품 정책 결정이 필요한 경우만 쓴다. 해결 전까지 다른 Change ID로 넘어가도 된다.

## 변경 작업판

| Change ID | 지금 문제 | 사람의 Figma 작업 | 주 진행 출처 | AI 검증 | 완료 기준 | 상태 |
|---|---|---|---|---|---|---|
| **B0-01** | Foundations 표지 `80 / 47` ≠ 실제 `83 / 51` | 표지 수치를 `83 / 51`로 바꾸거나 집계 기준을 적기 | B | D | 표지와 실제 Variable Collection 수 일치 | **지금 시작** |
| **B0-02** | `day` `389:44743` Variant 조회 오류 | Figma에서 깨진 Variant property/값을 정리 | B | D | Variant 오류 0건 | 대기 |
| **B0-03** | `Variant4`, `sourse`, `status3`, `MenuDetailSummary` | 팀이 새 이름 확정 후 사람이 rename | B | D | old name 0, 새 property 이름 확인 | 대기 |
| **B0-04** | CategoryTap, SaveBar 3벌, Deprecated가 공존 | 새 화면에 쓸 Master 1개씩 지정, 나머지 Deprecated 표기 | B | D | source of truth 표 완성 | 대기 |
| **B1-01** | CategoryTap `25×11`, CategoryTab과 중복 | Tap instance를 CategoryTab으로 교체, Tap Deprecated | B | A + D | Tap instance 0, Tab active/disabled 존재 | 대기 |
| **B1-02** | SCR-008 CTA `940×200` override | BottomCTA Master `1080×180`로 연결 | B | A + D | override 0, loading 16px 이상 | 대기 |
| **B1-03** | Cart Blue, 13px action, Admin MenuButton 혼입 | CartItemCard Master 수정 후 SCR-005 전파 | B | A + D | `#3B82F6/#0088FF` 0, action 16px+, hit 64px+ | 대기 |
| **B1-04** | MenuDetailSummary 11~13px, Blue, legacy | legacy 분리, badge/name/price 위계 수정 | B | D + E | 14/28/24px 이상, Blue 0 | 대기 |
| **B1-05** | Option 12~15px, indicator 20px | row 전체를 touch target으로 수정 | B | D + E | body16, label18, price16, row64px+ | 대기 |
| **B2-01** | SaveBar 3벌 + SCR-011 이중 노출 | 새 SaveBar Master 1개 확정·전파 | B | A + C + D | 이중 bar 0, dirty/saving/error 일치 | 대기 |
| **B2-02** | SoldOutCard 9px, 130×134 | 카드/텍스트 크기 수정 | B | A + D + E | 150×160 이상, 이름13px+, 9px 0 | 대기 |
| **B2-03** | Admin 16/20/35px 조작 영역 | MenuButton/Checkbox/DateSelector wrapper 확장 | B | D + E | 웹40px+, 태블릿44px+ | 대기 |
| **B3-01** | Confirm warning 라임+흰 글자 | dark text + kiosk size Variant 확정 | B | D + E | contrast 4.5:1+, kiosk CTA56px+ | 대기 |
| **B3-02** | Kiosk Toast가 299×76 | kiosk Toast size 추가·화면 전파 | B | A + D + E | width400px+, body16px+, height80px+ | 대기 |

## 출처에 요청하는 방식

### B에게: 수정 진행안만 요청

```text
Change ID: B1-03
역할: Master 구조만 확인
출력: 수정할 Master / Variant / Property / 기존 instance 영향만 표로 작성
금지: 화면 전체 재디자인, 새 문서 생성, 코드 수정
```

### A에게: 실제 Screen 전파만 요청

```text
Change ID: B1-03
역할: SCR-005 Default / Item Sold-out / Checkout Blocked만 확인
출력: 남은 override와 node ID, frame 수치만 작성
```

### D에게: PASS/FAIL만 요청

```text
Change ID: B1-03
역할: 읽기 전용 정량 검증
출력: PASS/FAIL, 기준별 실제 수치, 남은 node ID만 작성
```

### C에게: 상태/데이터 문제가 있을 때만 요청

```text
Change ID: B2-01 또는 B2-07
역할: Loading/Saving/Success/Error와 실제 데이터 흐름만 검증
출력: 재현 조건, 정책 충돌, 필요한 Screen ID만 작성
```

### E에게: 사람이 수정한 뒤 최종 품질만 요청

```text
Change ID: B1-04
역할: 터치·가독성·위계·위험 행동의 시각 QA
출력: 유지 / 수정 필요 / 이유와 권장값만 작성
```

## 충돌 결정판

| Decision ID | 대상 | 선택지 | 팀 결정 | 결정 전에는 할 일 |
|---|---|---|---|---|
| DEC-01 | CategoryTab 높이 | 52px 또는 64px | 미정 | 실제 키오스크에서 둘 다 눌러 보고 결정 |
| DEC-02 | BottomCTA radius | 12/16 또는 20 | 미정 | SCR-008 포함 3개 화면에서 비교 |
| DEC-03 | MenuCard kcal | 16 또는 20~24 | 미정 | 메뉴명/가격보다 약하게 보이는지 확인 |
| DEC-04 | MenuCard 가격색 | `#6C9700` 또는 `#4A7A00` | 미정 | D 대비 검증 + 사람 시안 선택 |
| DEC-05 | Error CTA | 라임 또는 dark | 미정 | 오류 복구가 primary인지 제품 정책 확정 |

## 규칙

- 같은 대상·속성·상태의 의견은 새 문서가 아니라 기존 Change ID의 근거로 붙인다.
- 수치 실측(A/B/D)과 권고(C/E)는 한 칸에 섞지 않는다.
- 의견 충돌은 Decision ID를 만들고 사람이 결정한다.
- D가 PASS하지 않은 행은 완료가 아니다.
- 한 Change ID가 PASS되기 전에는 같은 도메인의 다음 P0를 열지 않는다.
