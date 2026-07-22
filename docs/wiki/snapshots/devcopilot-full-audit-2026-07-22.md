# DevCopilot 전체 감사 (2026-07-22)

> MCP workspace `2` · 스냅샷: `docs/wiki/snapshots/devcopilot-*-live-2026-07-22.json`  
> 목적: WBS뿐 아니라 요구사항·시나리오·화면·API·DB·QA까지 **원격 vs 코드 실측** 차이를 본다.  
> 정본 우선순위: **코드 → 로컬 문서 → DevCopilot**

## 1. 한줄 결론

**이전에 한 일은 WBS Status 재확인뿐이었다.**  
이번 감사에서 나머지를 모두 조회했다.  
**Status를 당장 바꿀 항목은 거의 없다** (Admin mock 1차 연결도 DONE이 아니므로 LMIS는 계속 `IN_PROGRESS`가 맞다).  
다만 **화면(SCR)은 전부 `WIREFRAME`이라 mock 연결/정적 구분이 원격에 안 보인다.**

## 2. 엔티티별 수량

| 엔티티 | 건수 | Status 요약 | 코드 실측과 |
|---|---:|---|---|
| Requirements | 57 | TODO 25 · IN_PROGRESS 19 · EXCLUDED 13 | Admin LMIS는 IN_PROGRESS 유지가 맞음 (DONE 아님) |
| Scenarios | 24 | DRAFT 21 · ARCHIVED 3 | 시나리오 실행 evidence 없음 → DRAFT OK |
| Screens | 24 | WIREFRAME 20 · ARCHIVED 4 | **표현 한계**: mock 1차 연결과 정적 UI가 같은 WIREFRAME |
| WBS | 170 | EXCLUDED 98 · TODO 28 · IN_PROGRESS 26 · DONE 11 · BLOCKED 7 | P4 active Status = 로컬과 일치 |
| API specs | 46 | (status 필드 없음) | `/api/*` + `/api/v1/*` + `[TARGET]` 혼재 |
| DB schema | 30 tables급 | (구현 없음) | Backend entity 없음 → 명세만 |
| Test cases | 16 | TODO 16 | 실행 evidence 없음 → TODO OK |
| Bugs | 0 | — | 테스트 미실행과 일치 |

## 3. Admin 관련 요구사항 (코드 대조)

| ID | DevCopilot | 코드 실측 (2026-07-22) | 판정 |
|---|---|---|---|
| LMIS-ORDER-001 주문 목록 | IN_PROGRESS | mock 1차 연결 · 필터 TODO | **유지** |
| LMIS-ORDER-002 주문 상세 | IN_PROGRESS | 상세 패널·환불/영수증 stub | **유지** |
| LMIS-ORDER-003 주문 상태 변경 | IN_PROGRESS | Live 완료/취소만 · 목록 PATCH 미완 | **유지** (과대평가 아님) |
| LMIS-MENU-001 품절 처리 | IN_PROGRESS | draft·저장 stub · 실패 fixture TODO | **유지** |
| LMIS-MENU-002 품절→키오스크 반영 | IN_PROGRESS | Admin↔Kiosk 연동 evidence 없음 | **주의**: UI shell 수준으로만 해석 |
| LMIS-MENU-004 메뉴 등록/수정 | IN_PROGRESS | Admin 메뉴 화면 **정적** | **유지** (UI shell) |
| LMIS-ORDER-005 일별 매출 | IN_PROGRESS | 매출 3화면 **정적** | **유지** (UI shell) |
| LMIS-PAY-001 결제수단 설정 | IN_PROGRESS | 토글·저장 mock 1차 | **유지** |

Kiosk FWD-* / 결제·타임아웃 TODO·IN_PROGRESS 분포는 7/20 기준과 크게 다르지 않다.

## 4. 화면 (SCR)

| SCR | 이름 | DevCopilot | 코드 |
|---|---|---|---|
| 009 Live | 주문 현황 | WIREFRAME | MOCK_WIRED |
| 010 Orders | 주문 관리 | WIREFRAME | MOCK_WIRED |
| 011 Sold-out | 품절 | WIREFRAME | MOCK_WIRED |
| 018 Payments | 결제수단 | WIREFRAME | MOCK_WIRED |
| 022 Dashboard | 대시보드 | WIREFRAME | MOCK_WIRED |
| 016/017 Menus | 메뉴 | WIREFRAME | UI_ONLY / PLACEHOLDER |
| 019~021 Sales | 매출 3화면 | WIREFRAME | UI_ONLY |
| 023/024 | 영수증·멤버십 | ARCHIVED | Future — OK |

`update_screen`으로 mock 연결 여부를 넣을 **전용 status 값이 문서화되어 있지 않아**, 이번엔 화면 status를 바꾸지 않았다.  
구분은 로컬 `current-implementation-map` / Admin README 바인딩 표를 정본으로 둔다.

## 5. API / DB / QA

- API: business API는 Backend에 **미구현**. DevCopilot 명세·TARGET 경로만 존재 → 수정 불필요.
- DB: 모델 문서만, JPA/migration 없음 → 수정 불필요.
- QA: TC-001~016 전부 TODO. Admin #1 TC-A01~A06 회귀도 미실행 → TODO 유지가 맞음.
- Bugs: 0건 — 실행 없으므로 정상.

## 6. MCP로 못 하는 것

| 하고 싶은 일 | MCP |
|---|---|
| WBS Evidence / Notes 상세 | ❌ (`update_wbs_task`에 필드 없음) |
| Requirement description에 실측 메모 | △ `update_requirement`에 description 가능 여부는 스키마 확인 필요 |
| Screen을 MOCK_WIRED로 표기 | ❌ 허용 enum 불명 · 현행 전부 WIREFRAME |
| API status 갱신 | ❌ update_api 도구 없음 (create만) |

## 7. 다음에 손대면 좋은 것 (선택)

1. 로컬 맵을 정본으로 두고 DevCopilot은 Status만 유지 (현재 전략 — **권장**)  
2. LMIS-MENU-002처럼 “연동 evidence 없는 IN_PROGRESS”를 description에 한 줄 주의 문구 추가  
3. QA 실행 후 TC status만 PASS/FAIL로 올리기  

이번 세션에서는 **조회·감사·로컬 기록**까지 하고, 원격 Status 대량 변경은 하지 않았다.
