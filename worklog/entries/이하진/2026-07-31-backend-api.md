# 2026-07-31 고객 API·주문·메뉴·문서·계약·스킬·설정

> **일일 기록:** [2026-07-31 daily](../../daily/이하진/2026-07-31.md)
> **근거:** Git 커밋·`git show --stat`·변경 파일. **코드 커밋 ≠ 통합 검증 완료.**

---

## 1. 기본 정보

- 작업 날짜: 2026-07-31
- 담당자: 이하진
- 저장소: `ASAK` / `ASAK-back`
- 브랜치: chore/menu-seed-dedupe~5, fix/admin-menu-pagination~6
- 관련 이슈/PR/화면: 커밋·경로 기준 (정식 ID 미기재 시 추정 표기)
- 작업 유형: `feature` / `fix` / `docs`
- 구현 근거: `202a05a`, `d903e17`
- Figma 기준: 당일 커밋에 Figma 노드 추가/변경 evidence가 명시되지 않으면 `Figma 미확인`으로 둔다. UI 커밋이 있어도 상태별(Frame/Loading/Empty/Error) 재대조는 별도 검증이다.
- 완료 판정: 커밋 반영은 확인. **Gradle/npm/Bruno/브라우저/실DB 통합 결과는 이 기록에서 재실행하지 않음.**

## 2. 작업 목적

- ASAK / ASAK-back에서 확인된 당일 작업을 **고객 API·주문·메뉴 · 문서·계약·스킬·설정** 단위로 정리한다.
- mock/화면/API/문서 중 실제로 손댄 경계를 커밋·파일로 구분해, 다음 실연동·검증 범위를 남긴다.
- 완료 판정은 코드 반영과 분리한다. 통합 테스트·브라우저·실DB 증거가 없으면 미검증으로 둔다.

## 3. 직접 구현 영역

Git 커밋 이력으로 다음 직접 작업을 확인했다.

- **고객 API·주문·메뉴:**
  - `202a05a` fix:orderNo 형식 및 db업데이트
  - 주요 파일: `src/main/java/com/asak/user/dto/order/response/CreateOrderResponse.java`, `src/main/java/com/asak/user/service/UserMenuService.java`, `src/main/java/com/asak/user/service/UserOrderService.java` (`202a05a`)
- **문서·계약·스킬·설정:**
  - `d903e17` docs: ASAK 스킬 문서 갱신 및 정본 원칙 추가
  - 주요 파일: `docs/guides/agent-skill-templates/asak-devcopilot-sync/SKILL.md`, `docs/guides/agent-skill-templates/asak-doc-sync/SKILL.md`, `docs/guides/agent-skill-templates/asak-git-publish/SKILL.md`, `docs/guides/agent-skill-templates/asak-signoff/SKILL.md`, `docs/guides/agent-skill-templates/asak-study/SKILL.md` (`d903e17`)

## 4. 구현 로직 / 적용한 방식

- **근거 순서:** Git 커밋·변경 파일 → 현재 코드 경로 → (있으면) Screen/API 문서. Product Bible과 코드가 다르면 코드/실측을 우선하고 문서는 별도 TODO로 남긴다.
- **저장소 경계:** ASAK / ASAK-back. 프론트·백엔드·문서 커밋이 섞이면 영역별로 나눠 기록한다.
- **고객 API·주문·메뉴:** Controller→Service→Mapper(XML)→DTO 흐름으로 고객 메뉴/주문 API를 보강했다. 대표 파일: `CreateOrderResponse.java`, `UserMenuService.java`, `UserOrderService.java`.
- **문서·계약·스킬·설정:** 스킬/가이드/팀 설정/명세처럼 구현 완료와 분리된 문서 정본을 갱신했다. 대표 파일: `SKILL.md`, `SKILL.md`, `SKILL.md`, `SKILL.md`.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: `2026-07-31` 작업을 2026-07-23 API 계약 entry 수준의 12섹션 상세 기록으로 재작성하도록 요청했다.
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
| 당일 커밋 | 2건 (`202a05a` … `d903e17`) | 각 저장소 `git log --since/--until` |
| 고객 API·주문·메뉴 | 커밋 1건 · 파일 3+ | `src/main/java/com/asak/user/dto/order/response/CreateOrderResponse.java` |
| 문서·계약·스킬·설정 | 커밋 1건 · 파일 5+ | `docs/guides/agent-skill-templates/asak-devcopilot-sync/SKILL.md` |
| 실행 검증 | 이 entry 보강 시점에 Gradle/npm/Bruno/브라우저 재실행 없음 | 저장소별 test/build · Network 탭 |

## 8. 이번 작업에서 배운 점

1. 화면이 보이는 것과 API/DB까지 연결된 것은 다른 완료 기준이다. 커밋 수만으로 DONE을 올리지 않는다.
2. 같은 날의 백업 커밋과 기능 커밋을 구분해야 포트폴리오 설명이 정확해진다.
3. 변경 파일 목록이 있어야 메뉴/장바구니/결제/Admin 같은 단위로 작업을 설명할 수 있다.
4. 백엔드는 Controller/Service/Mapper/DTO를 한 줄로 묶어 수직 슬라이스 단위로 검증하는 편이 안전하다.

## 9. 개선사항 / TODO

- [ ] 관련 화면을 브라우저에서 Loading/Empty/Error까지 수동 확인
- [ ] 실연동 구간이면 Bruno 또는 Network 탭으로 요청/응답 envelope 확인
- [ ] 필드명(`totalAmount`, `CANCELED`, `EAT_IN`/`TAKE_OUT` 등) 정본과 불일치 여부 재대조
- [ ] `ASAK-back`에서 `./gradlew test` 또는 최소 bootRun 스모크
- [ ] 메뉴 조회→장바구니→주문 생성 경로를 실DB fixture로 한 사이클 확인

## 10. 검증 내용

- 실행한 명령어:
  - `git log --since/--until` (ASAK / ASAK-back)
  - `git show --stat --name-only <commit>`
- 테스트한 시나리오:
  - Git evidence로 영역별 변경 범위 확인
  - 기능 시나리오(주문 완료, Admin 상태 변경, 실DB 저장 등)는 **미실행**
- 확인 결과:
  - 2026-07-31 작성자 커밋 **2건**과 영역별 파일 목록을 확인했다.
  - 이 entry 작성/보강 시점에는 자동 테스트·실서버 호출·E2E 성공 결과를 새로 확보하지 않았다.

## 11. 포트폴리오용 요약

2026-07-31 이하진 작업은 ASAK / ASAK-back에서 고객 API·주문·메뉴 · 문서·계약·스킬·설정 범위를 커밋 2건으로 진행한 기록이다. 변경 파일과 영역 경계를 기준으로 설명하고, 통합 테스트·실DB·브라우저 검증은 완료로 과장하지 않았다.

## 12. 첨부하면 좋은 자료

- 일일 기록: [2026-07-31 daily](../../daily/이하진/2026-07-31.md)
- 관련 커밋: `202a05a`, `d903e17`
- 변경이 큰 경로: `src/main/java/com/asak/user/dto/order/response/CreateOrderResponse.java`, `src/main/java/com/asak/user/service/UserMenuService.java`, `src/main/java/com/asak/user/service/UserOrderService.java`
