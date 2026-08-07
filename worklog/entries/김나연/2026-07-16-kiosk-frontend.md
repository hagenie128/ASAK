# 2026-07-16 키오스크 메뉴·옵션·상세·키오스크 장바구니·합계

> **일일 기록:** [2026-07-16 daily](../../daily/김나연/2026-07-16.md)
> **근거:** Git 커밋·`git show --stat`·변경 파일. **코드 커밋 ≠ 통합 검증 완료.**

---

## 1. 기본 정보

- 작업 날짜: 2026-07-16
- 담당자: 김나연
- 저장소: `ASAK-Kiosk`
- 브랜치: remotes/origin/ny/api-connection~58, remotes/origin/ny/api-connection~59, remotes/origin/ny/api-connection~60^2
- 관련 이슈/PR/화면: SCR-003
- 작업 유형: `feature` / `fix`
- 구현 근거: `6f5340d`, `f4282f5`, `723d417`, `d75c8a1`, `656e47c`, `45fc755`
- Figma 기준: 당일 커밋에 Figma 노드 추가/변경 evidence가 명시되지 않으면 `Figma 미확인`으로 둔다. UI 커밋이 있어도 상태별(Frame/Loading/Empty/Error) 재대조는 별도 검증이다.
- 완료 판정: 커밋 반영은 확인. **Gradle/npm/Bruno/브라우저/실DB 통합 결과는 이 기록에서 재실행하지 않음.**

## 2. 작업 목적

- ASAK-Kiosk에서 확인된 당일 작업을 **키오스크 메뉴·옵션·상세 · 키오스크 장바구니·합계** 단위로 정리한다.
- 키오스크 주문 세션(유형→메뉴→옵션→장바구니→결제)에서 끊기지 않는 UI/상태 흐름을 맞추는 것이 목표다.
- mock/화면/API/문서 중 실제로 손댄 경계를 커밋·파일로 구분해, 다음 실연동·검증 범위를 남긴다.
- 완료 판정은 코드 반영과 분리한다. 통합 테스트·브라우저·실DB 증거가 없으면 미검증으로 둔다.

## 3. 직접 구현 영역

Git 커밋 이력으로 다음 직접 작업을 확인했다.

- **키오스크 메뉴·옵션·상세:**
  - `6f5340d` refactor: update CategoryTabs and OptionItem components for improved state management and styling
  - `f4282f5` fix: OptionItem 옵션 그룹에 따른 클래스 매핑 추가
  - `45fc755` feature: menuListPage 주문목록 컴포넌트 추가 + 디테일 페이지에서 저장 후 -> 메뉴리스트로 페이지 이동 -> 주문 목록List에 orderItem 추가
  - 주요 파일: `src/components/kiosk/CategoryTabs.jsx`, `src/components/kiosk/OptionGroup.jsx`, `src/components/kiosk/OptionItem.jsx`, `src/components/kiosk/OrderList.jsx`, `src/components/kiosk/OrderListItem.jsx`, `src/pages/kiosk/MenuListPage.jsx` (`6f5340d`, `f4282f5`, `45fc755`)
- **키오스크 장바구니·합계:**
  - `723d417` kiosk-menu-options-scr003 디테일 페이지 컴포넌트 추가 및 로직 구성
  - `d75c8a1` fix: MenuDetailPage_footer하단 디자인 수정 및 totalPrice 반영
  - `656e47c` fix: MenuDetailPage -> 저장 방식 수정 & MenuListPage-> 추가될 주문 목록 컴포넌트를 위한 코드 개선 & priceCalculation-> 가격이 0일때 오류 개선 & quantityLimits -> 주문 목록 컴포넌트 수량 기능을 위한 코드 추가
  - 주요 파일: `src/components/kiosk/MenuDetailFooter.jsx`, `src/components/kiosk/MenuDetailSummary.jsx`, `src/components/kiosk/QuantityStepper.jsx`, `src/pages/kiosk/MenuDetailPage.jsx`, `src/utils/currency.js`, `src/utils/priceCalculation.js`, `src/utils/quantityLimits.js`, `src/components/kiosk/MenuCard.jsx` 외 3개 (`723d417`, `d75c8a1`, `656e47c`)

## 4. 구현 로직 / 적용한 방식

- **근거 순서:** Git 커밋·변경 파일 → 현재 코드 경로 → (있으면) Screen/API 문서. Product Bible과 코드가 다르면 코드/실측을 우선하고 문서는 별도 TODO로 남긴다.
- **저장소 경계:** ASAK-Kiosk. 프론트·백엔드·문서 커밋이 섞이면 영역별로 나눠 기록한다.
- **키오스크 메뉴·옵션·상세:** 메뉴 목록/상세/옵션 선택 UI와 가격 반영 경로를 페이지·컴포넌트 단위로 쌓았다. 대표 파일: `CategoryTabs.jsx`, `OptionGroup.jsx`, `OptionItem.jsx`, `OrderList.jsx`.
- **키오스크 장바구니·합계:** 장바구니 목록·수량·합계 표시와 페이지 이동이 같은 세션 상태를 보도록 맞췄다. 대표 파일: `MenuDetailFooter.jsx`, `MenuDetailSummary.jsx`, `QuantityStepper.jsx`, `MenuDetailPage.jsx`.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: `2026-07-16` 작업을 2026-07-23 API 계약 entry 수준의 12섹션 상세 기록으로 재작성하도록 요청했다.
- AI가 도움 준 내용: 커밋·파일 목록 수집, 영역 분류, 이슈/TODO/검증 문장 구조화.
- 그대로 사용한 부분: 커밋 해시, 메시지, 변경 파일 경로, stat 요약.
- 수정해서 사용한 부분: 서술 문장·영역 묶음. 원 구현 시점의 AI 사용 여부와 런타임 로그는 커밋만으로 복원하지 않았다.

## 6. 발생 이슈

### 이슈 — 스펙/코드 불일치를 fix 커밋으로 맞춤

- 증상: 필드명·경로·SQL·UI 상태 중 일부가 명세 또는 화면과 달랐다.
- 원인: mock·문서·API가 병렬로 진화했다.
- 해결: fix 커밋의 변경 파일 기준으로 정합을 맞췄다. 회귀 테스트는 별도 실행이 필요하다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| 당일 커밋 | 6건 (`6f5340d` … `45fc755`) | 각 저장소 `git log --since/--until` |
| 키오스크 메뉴·옵션·상세 | 커밋 3건 · 파일 6+ | `src/components/kiosk/CategoryTabs.jsx` |
| 키오스크 장바구니·합계 | 커밋 3건 · 파일 11+ | `src/components/kiosk/MenuDetailFooter.jsx` |
| 실행 검증 | 이 entry 보강 시점에 Gradle/npm/Bruno/브라우저 재실행 없음 | 저장소별 test/build · Network 탭 |

## 8. 이번 작업에서 배운 점

1. 화면이 보이는 것과 API/DB까지 연결된 것은 다른 완료 기준이다. 커밋 수만으로 DONE을 올리지 않는다.
2. 같은 날의 백업 커밋과 기능 커밋을 구분해야 포트폴리오 설명이 정확해진다.
3. 변경 파일 목록이 있어야 메뉴/장바구니/결제/Admin 같은 단위로 작업을 설명할 수 있다.
4. 키오스크는 공통 Footer/Header/Stepper와 페이지 상태가 어긋나면 결제 직전 UX가 바로 깨진다.

## 9. 개선사항 / TODO

- [ ] 관련 화면을 브라우저에서 Loading/Empty/Error까지 수동 확인
- [ ] 실연동 구간이면 Bruno 또는 Network 탭으로 요청/응답 envelope 확인
- [ ] 필드명(`totalAmount`, `CANCELED`, `EAT_IN`/`TAKE_OUT` 등) 정본과 불일치 여부 재대조
- [ ] 해당 FE 저장소 `npm run build` 회귀

## 10. 검증 내용

- 실행한 명령어:
  - `git log --since/--until` (ASAK-Kiosk)
  - `git show --stat --name-only <commit>`
- 테스트한 시나리오:
  - Git evidence로 영역별 변경 범위 확인
  - 기능 시나리오(주문 완료, Admin 상태 변경, 실DB 저장 등)는 **미실행**
- 확인 결과:
  - 2026-07-16 작성자 커밋 **6건**과 영역별 파일 목록을 확인했다.
  - 이 entry 작성/보강 시점에는 자동 테스트·실서버 호출·E2E 성공 결과를 새로 확보하지 않았다.

## 11. 포트폴리오용 요약

2026-07-16 김나연 작업은 ASAK-Kiosk에서 키오스크 메뉴·옵션·상세 · 키오스크 장바구니·합계 범위를 커밋 6건으로 진행한 기록이다. 변경 파일과 영역 경계를 기준으로 설명하고, 통합 테스트·실DB·브라우저 검증은 완료로 과장하지 않았다.

## 12. 첨부하면 좋은 자료

- 일일 기록: [2026-07-16 daily](../../daily/김나연/2026-07-16.md)
- 관련 커밋: `6f5340d`, `f4282f5`, `723d417`, `d75c8a1`, `656e47c`, `45fc755`
- 변경이 큰 경로: `src/components/kiosk/CategoryTabs.jsx`, `src/components/kiosk/OptionGroup.jsx`, `src/components/kiosk/OptionItem.jsx`, `src/components/kiosk/OrderList.jsx`, `src/components/kiosk/OrderListItem.jsx`
