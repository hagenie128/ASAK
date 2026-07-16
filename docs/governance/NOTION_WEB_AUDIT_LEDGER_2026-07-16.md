# Notion Web Audit Ledger — 2026-07-16

> **PARTIAL AUDIT — RESUME REQUIRED**
>
> 기준 Repository commit: `1e4fa2e4b15fc958a0be6d2a39ca849798e4d415` (PR #5 merge commit)
>
> 원칙: 이 Ledger는 Notion Web의 실제 페이지·Database record를 개별 열람한 결과만 기록한다. 검색 제목만으로 판정하지 않으며, 수정은 재열람으로 확인한다.

## 현재 범위와 수치의 의미

| 구분 | 수치 | 의미 |
|---|---:|---|
| 발견 | P0 120 / P1·P2 48 | 키워드 검색의 순위 결과 수. 중복 결과를 포함하며, 열람·검증 완료를 뜻하지 않는다. |
| 실제 개별 열람 | 33 | 상위 문서/DB 10건, WBS·요구사항 record 12건, 화면·API 대표 record 11건 |
| 수정 후 재열람 검증 | 10 | 상위 문서 5건과 DB record 5건의 변경 반영 확인 |
| 실제 수정 | 10 | 상위 문서 5건, DB record 5건 |

P0는 **초기 감사만 수행**했다. P1/P2는 후보 검색만 수행했으며 개별 열람·검증·수정은 아직 시작하지 않았다. 열지 않은 record를 `VERIFIED`로 표기하지 않는다.

## 다음 시작 지점

1. P0 잔여 WBS·요구사항·화면·API record를 10~20건씩 개별 열람하여 전수 정합성을 확인한다.
2. DB 설계의 과거 22-table 서술과 현재 DevCopilot 26 tables/4 views 차이를 근거 문서별로 검증한다.
3. P0가 끝난 뒤에만 Ledger의 P1/P2 후보를 시작한다.

## 기준 문서

- `docs/wiki/current-status-baseline.md`
- `docs/wiki/devcopilot-sync-report.md`
- `docs/wiki/wbs-v2.md`
- `docs/wiki/legacy-wbs2-mapping-audit-2026-07-16.md`
- `docs/wiki/rest-api-spec.md`, `docs/wiki/db-audit-plan.md`, `docs/wiki/qa-test-cases.md`
- `docs/product_bible/07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md`

## 배치 체크포인트

| Batch | 우선순위 | 범위 | 개별 열람 | 수정 | 결과 |
|---|---|---|---:|---:|---|
| 0 | Setup | main 기준 문서 및 Notion 연결 확인 | 0 | 0 | 완료 — 연결 워크스페이스와 ASAK 허브 확인 |
| 1 | P0 | WBS·요구사항·화면·API·DB 상위 문서와 5개 인라인 DB 구조 확인 | 10 | 5 | 완료 — 상위 문서에 현재 기준 병기, 각 수정 직후 재열람 완료 |
| 2 | P0 | WBS/요구사항 record 후보 개별 열람 | 12 | 2 | 완료 — 근거가 명확한 2건만 상태·비고 정정, 나머지는 보존 |
| 3 | P0 | 화면/API DB 후보 조회 및 대표 record 개별 열람 | 11 | 3 | 완료 — 화면은 구현 완료 오표기 없음, API 경로 불일치 3건을 검토중으로 전환 |
| 4 | P1/P2 | 디자인·QA·Git·회의록·워크로그·아카이브 키워드 후보 검색 | 0 | 0 | 완료 — 후보만 수집, 개별 열람·수정은 다음 배치 |
| 5 | P0 | DB 설계·테이블 정의 재검색 | 0 | 0 | 완료 — DB 설계는 단일 문서 중심이며 별도 테이블 모델 DB는 검색 결과에서 확인되지 않음 |

## 변경 및 판정 기록

| 대상 URL/ID | 유형 | 우선순위 | 판정 | 변경 전 → 후 | 검증 근거 | 비고 |
|---|---|---|---|---|---|---|
| `cd951ef0-4f0b-82b0-81de-019cc9a4c580` | 프로젝트 허브 | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | WBS·요구사항 등 하위 프로젝트 허브 연결 확인 |
| `dfd51ef0-4f0b-820e-9b5a-01f2c1343d16` | WBS DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | `작업 ID`, `상태`, `진척률`, 요구사항 Relation 존재 |
| `22551ef0-4f0b-8217-94d4-012f787551bc` | 요구사항 DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | WBS·시나리오 Relation 존재 |
| `f9251ef0-4f0b-83a6-85ef-8190b77d5748` | 화면 DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | 화면 설계 상위 문서 하위 DB |
| `56a51ef0-4f0b-83fb-bfb0-81c63640f66d` | API DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | API 명세 상위 문서 하위 DB |
| `1d951ef0-4f0b-8301-9b42-81f04c7b12cc` | DB 설계 문서 | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | P0 대상 문서로 식별 |
| `1ab51ef0-4f0b-8330-afca-012a4e8d14fa` | WBS 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 기존 WBS 본문 보존 |
| `81b51ef0-4f0b-8259-a933-01381182f754` | 요구사항 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 구현율 0.0%, 일괄 DONE 없음 |
| `1c751ef0-4f0b-825e-a3aa-8145f563bbc8` | 화면 설계 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | DESIGN_DONE과 구현 완료 분리 |
| `34651ef0-4f0b-838c-a3a4-81e55eebfb2b` | API 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 명세와 백엔드 구현 분리 |
| `1d951ef0-4f0b-8301-9b42-81f04c7b12cc` | DB 설계 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 모델과 애플리케이션 구현 분리 |
| `39151ef0-4f0b-81ee-8778-c89fce69ea1d` | WBS-001 record | P0 | 정정 | 예정/미기재 → 완료/100% | 수정 후 Notion Web 재열람 | 설계·데이터 정의 완료만 의미, React/API/QA 완료 아님 |
| `39151ef0-4f0b-8193-ab52-ec6221dfd7b3` | FWD-CART-002 포장봉투 추가 | P0 | 정정 | 예정 → 제외 | 수정 후 Notion Web 재열람 | 기존 설명이 이미 Future Scope였음 |
| `3a551ef0-4f0b-8376-bd80-87f10660acc4` | 화면 설계 DB | P0 | 후보 조회 | 변경 없음 | 20 record 조회, 대표 5 record 개별 열람 | 모두 `개발 완료=아니오`; Figma/구현 근거 불충분으로 상태 보존 |
| `98151ef0-4f0b-82c8-91e2-87cc01b9eb15` | API 명세 DB | P0 | 후보 조회 | 변경 없음 | 20 record 조회, API-002/003/004/005/006/009 개별 열람 | 구현 완료 표기 없음 |
| `04851ef0-4f0b-831a-bbe6-01a5cd258ac9` | API-002 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | `/api/menus`와 최신 목표 경로 간 계약 결정 필요 |
| `39251ef0-4f0b-81b6-a23b-d0da22f3632e` | API-003 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | legacy `/api/menus/**` 계약 검토 필요 |
| `39151ef0-4f0b-8165-83b6-f7d373600582` | API-004 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | legacy `/api/menus/**` 계약 검토 필요 |

## 다음 배치 후보

| 우선순위 | 실제 Notion 후보 | 다음 확인 목적 |
|---|---|---|
| P1 | `2026-07-09~14 이하진 Figma 디자인 작업`, `Figma 가이드 + SCR×Figma 매트릭스` | 디자인 완료와 구현 완료의 경계, Figma 링크 정합성 |
| P1 | `09. 테스트/오류 관리`, `11. 최종 제출 체크리스트` | 실행 근거 없는 PASS/완료 표기 확인 |
| P1 | `문서 읽는 순서`, `Git 전략` | Git 정본 링크와 현재 원칙 점검 |
| P2 | `10. 회의록`, `회의록 목록`, `📅 일일 워크로그` | 중복·이관 후보와 기록 위치 점검 |
| P2 | `Zip Import - ASAK 키오스크 프로젝트.zip - Jul 13, 2026`, `Zip Import - notion.zip - Jul 13, 2026` | import 보관물의 정본 혼동 여부 확인 |

DB 설계의 "22개 테이블"·seed 관련 과거 서술과 현재 DevCopilot 26 tables/4 views의 차이는 확인됐다. 그러나 별도 DB 모델 database record는 검색 결과에서 확인되지 않아, DB 설계 문서의 현재 기준 안내만 병기하고 데이터 모델을 추정 생성·수정하지 않았다.

## 미지원·보류

| 항목 | 사유 | 후속 |
|---|---|---|
