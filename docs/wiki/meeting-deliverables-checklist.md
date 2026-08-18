# ASAK 회의록 및 최종 배포 검증

> **⚠️ HISTORICAL / 참고용 — 일일 실행에 쓰지 마세요.**
> → 대신 [**START_HERE**](https://github.com/hagenie128/ASAK/blob/main/docs/START_HERE.md) · [**wbs.md**](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/wbs.md) · [구현 맵](https://github.com/hagenie128/ASAK/blob/main/docs/planning/current-implementation-map-2026-07-16.md) · [wbs-status-notes](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/wbs-status-notes.md) · [baseline](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/current-status-baseline.md) · [주차별 회의록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md)
> 산출물 존재 ≠ 구현 근거. (체크리스트의 `ASAK-front` 등은 구 명칭.)

> Notion 10. 회의록 + 11. 최종 제출 체크리스트 (2026-07-06)

## 회의록 인덱스

| 회의                                      | Hub / Notion                                                                                    | 로컬                                                                                                                                                                                                                                                                                           |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **주차별 공식 회의록 (2026-07-01~08-18)** | [Hub wiki/78](https://devcopilot.ai.kr/workspace/2/wiki/78) | [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · W27~W34                                                                                                                                                                                       |
| **워크로그 인덱스 (daily·entries·weekly)** | [Hub wiki/83](https://devcopilot.ai.kr/workspace/2/wiki/83) | [로컬](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/worklog-index.md) · [worklog/](https://github.com/hagenie128/ASAK/tree/main/worklog) · W28~W34                                                                                                                                 |
| 2026-07-03 키오스크 컨셉                  | (Notion 10)                                                                                     | 아래 §                                                                                                                                                                                                                                                                                         |
| 화면 설계 초기 회의 · 사전 의견           | [Notion 인덱스](https://app.notion.com/p/39551ef04f0b8190b76ae4b48b8497ac)                      | [Archive 회의 기록](https://github.com/hagenie128/ASAK/blob/main/docs/_archive/project-history/design-meetings/README.md)                                                                                                                                                                      |
| **2026-07-06 화면 설계 초기 회의**        | [Notion 취합본](https://app.notion.com/p/39551ef04f0b815f8dc6e788176186d7)                      | [회의록](https://github.com/hagenie128/ASAK/blob/main/docs/_archive/project-history/design-meetings/screen-design-meeting-minutes-2026-07-06.md) · [변경 이력](https://github.com/hagenie128/ASAK/blob/main/docs/_archive/project-history/design-meetings/screen-design-changes-2026-07-06.md) |

### 주차별 공식 회의록 (김나연·이하진)

| 주차 | 기간        | 주제                             | 파일                                                                                                    |
| ---- | ----------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| W27  | 06-29~07-05 | 킥오프·기획 정비                 | [2026-W27.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W27.md) |
| W28  | 07-06~07-12 | 디자인 방향·관리자 UI 골격       | [2026-W28.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W28.md) |
| W29  | 07-13~07-19 | 저장소 분리·Figma→코드·구현 경계 | [2026-W29.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W29.md) |
| W30  | 07-20~07-26 | mock 완성·백엔드 골격·제출       | [2026-W30.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W30.md) |
| W31  | 07-27~08-02 | Admin API·계약 통일·연동 시작    | [2026-W31.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W31.md) |
| W32  | 08-03~08-07 | 실연동·관리자 CRUD·문서화        | [2026-W32.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W32.md) |
| W33  | 08-10~08-16 | 키오스크 실API·관리자 메뉴 연동  | [2026-W33.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W33.md) |
| W34  | 08-17~08-21 | 장치 이벤트/RTOS 연동            | [2026-W34.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W34.md) |

Hub 전체본: [meeting-minutes-weekly.md](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/meeting-minutes-weekly.md) · 로컬 정본 폴더: [`docs/operations/meeting-minutes/`](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md)

### 2026-08-07 스냅샷 (선생님 우선순위)

| 순서 | 작업                                                          | 상태                                                                                                                                                                                                                            |
| ---- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Kiosk 장바구니 검증 → 주문 생성 → 결제수단·승인 (실 DB)       | 진행                                                                                                                                                                                                                            |
| 2    | Admin 주문 Live·목록·상태·취소 통합 테스트                    | 구현·미검증                                                                                                                                                                                                                     |
| 3    | Admin 메뉴 CRUD → 품절 → 결제수단 → 매출·대시보드 (mock 제거) | 대기/스텁                                                                                                                                                                                                                       |
| —    | 회의록·위키 최신화                                            | Hub wiki/78·15 반영                                                                                                                                                                                                             |
| —    | WBS 상태·일정                                                 | TODO→작업중(008·027·045·056·057·059) · 일정 rebase 8/7 (P0~발표) · [Notion](https://www.notion.so/3b551ef04f0b814f913afedb7b353ad3) · Hub [wiki/81](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/wbs-status-notes.md) |
| —    | Figma                                                         | 추가 디자인 중지 · 구독 종료 전 백업본 팀 공유                                                                                                                                                                                  |

계약 필드 정본: `totalAmount` / `approvedAmount` / `approvedAt` / `APPROVED` / `CANCELED` / `EAT_IN`·`TAKE_OUT`
Hub API 명세서: [wiki/12](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/rest-api-spec.md) · 흐름도: [project-flow.md](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/project-flow.md)
참고 문서 표: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07) · DONE/PASS: [asak-done-pass-audit](https://github.com/hagenie128/ASAK/blob/main/docs/ai-reports/2026-08-07/asak-done-pass-audit.md)

## 회의록

### 2026-07-03 키오스크 컨셉 회의

| 항목   | 내용                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------ |
| 참석   | 하진, 유진, 나연                                                                                             |
| 결정   | 서비스명 **ASAK/아삭**, Week 5 MVP = 고객 주문 (SCR-001~008, 8/1) + Week 6 관리자 확인, KVS/매출/멤버십 보류 |
| 디자인 | Primary #16A34A, Crunch Yellow #FACC15, Cream #FFFDF3                                                        |
| 다음   | Figma 팔레트, 화면 흐름도, MVP DB/API, 와이어프레임                                                          |

**MVP 고객**: 홈~결제완료 8화면 · **관리자**: 주문목록/상세/상태/품절

### 2026-07-06 화면 설계 초기 회의

| 항목 | 내용                                                                                                                   |
| ---- | ---------------------------------------------------------------------------------------------------------------------- |
| 참석 | 이하진, 김나연, 박유진, 강민준                                                                                         |
| 결정 | **DS-02 Modern Minimal**, SCR-001+002 병합, SCR-005+006 병합(컨펌 팝업), 고객 UI **6단계**, 결제 로딩·에러 팝업/토스트 |
| 보류 | DS-08 참고안, 추천 우선 모드, 멤버십·영수증, 고객/관리자 DS 분리                                                       |
| 다음 | Figma DS-02·통합 와이어, Notion SCR DB 반영                                                                            |

**MVP 고객 UI**: 홈·매장/포장 → 메뉴 → 옵션 → 장바구니·주문확인(팝업) → 결제 → 완료 (**6 UI 단계**, SCR-001~008 ID 유지)

상세: [회의록](https://github.com/hagenie128/ASAK/blob/main/docs/_archive/project-history/design-meetings/screen-design-meeting-minutes-2026-07-06.md) · [변경 이력](https://github.com/hagenie128/ASAK/blob/main/docs/_archive/project-history/design-meetings/screen-design-changes-2026-07-06.md)

---

## 11. 최종 제출 체크리스트

### 필수 산출물

| 산출물          | 위치                   | 상태                                     |
| --------------- | ---------------------- | ---------------------------------------- |
| 요구사항 정의서 | Notion 02 / Wiki       | 완료                                     |
| 사용자 시나리오 | Notion 03 SC-001~018   | 완료                                     |
| 화면 설계서     | Notion 04 SCR-001~021  | 진행중 (로컬·Hub 반영 완료, Notion 수동) |
| ERD·테이블 정의 | Notion 05 · 22테이블   | 완료                                     |
| API 명세        | Notion 06 API-001~020  | 완료                                     |
| React/Spring    | GitHub ASAK-front/back | 예정                                     |
| MySQL seed      | asak-data/seed         | 진행중                                   |
| 테스트 결과     | Notion 09 TC-001~014   | 진행중                                   |
| README          | ASAK/README.md         | 완료                                     |

### 시연 체크리스트

- [ ] 관리자 데이터 등록
- [ ] 키오스크 목록 조회
- [ ] 손님 주문 (SC-001)
- [ ] 결제 (SC-004)
- [ ] 완료 화면·주문번호
- [ ] 관리자 주문 확인·상태 변경
- [ ] 품절 비활성화 (SC-003)
- [ ] 재방문 5단계 이내 주문 (SC-002)

### DevCopilot Wiki 검증

1. https://devcopilot.ai.kr/workspace/2/wiki 접속
2. 산출물 8개 Wiki 문서 제목·내용 확인
3. Requirements / APIs / WBS 탭과 ID 추적성 대조

### 화면 설계 회의 반영 (2026-07-06)

- [x] `screens.json`·Wiki·SCR_REQ_MAP 병합 반영 (001+002, 005+006)
- [x] DS-02 Modern Minimal 프로덕션 DS 문서화
- [ ] Notion 04 SCR DB 수동 반영
- [ ] Figma DS-02·통합 와이어 적용

### Notion 문서 완성 (2026-07-05)

- [x] API-001~020 정합
- [x] SC-001~018 Mermaid
- [x] DB ERD 22테이블
- [x] WBS·테스트 Relation 컬럼
- [ ] Figma 프로토타입 (Notion 밖) — **DS-02 Modern Minimal** 방향 확정, 적용 진행
- [ ] React/Spring 구현 (Notion 밖)
