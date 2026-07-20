# 레거시(Legacy) 및 참조(Reference) 색인

> 문서 입구: [START_HERE](../START_HERE.md) · 슬림 인벤토리: [문서 인벤토리](../document-inventory-slim-2026-07-20.md)
> 이 색인은 고유 콘텐츠를 삭제·이동·재작성하지 않고 비정본(non-canonical) 문서를 분류합니다. 정본 제품 규칙은 [Product Bible 얇은 안내](../product_bible/README.md) · [Pack Index](product-bible-index-2026-07-16.md)에 있습니다.

## 참조(Reference)

| 문서 그룹 | 정본이 아닌 이유 | 보존할 고유 정보 | 후속 조치 |
|---|---|---|---|
| `docs/guides/**` | 온보딩 및 작업 가이드이며, 제품 계약이 아님 | 팀 설정, Git 프로세스, 작업 로그 형식 | 해당되는 경우 현재 Pack으로 링크 |
| `docs/wiki/**` | 내보낸 프로젝트 요약 | 요구사항, 시나리오, DB/API/WBS 맥락 | 재사용 전 Product Bible과 비교 |
| `docs/design/**` (현재 Figma 가이드/스펙) | Figma 지원 자료 | Figma 노드, 디자인 에셋, 디자인 프로세스 | 최신 Figma/Screen Registry 확인 |
| `docs/notion/**` | 스크립트 기반 Notion 입력 스냅샷 | DevCopilot 업로드 소스 전용 | 재사용 전 Product Bible과 비교 |

## 레거시(Legacy)

| 문서 그룹 | 정본이 아닌 이유 | 보존할 고유 정보 |
|---|---|---|
| `ASAK-Kiosk/src/pages/admin/**`, `components/admin/**`, `api/admin.js`, `api/sales.js` | 관리자 구현 정본은 ASAK-Admin | 이전 프론트엔드 스캐폴드 및 필드 기대값 |
| `docs/team/**`, 디자인 회의 의견 | 날짜가 있는 협업/결정 맥락 | 작성자, 리뷰 이력, 미해결 피드백 |
| Notion 일일 작업 로그 및 이전 구현 계획 | 특정 시점 진행 기록 | 구현 이력 및 테스트 증거 |

## 아카이브(Archived)

| 문서 그룹 | 아카이브된 이유 |
|---|---|
| `docs/product_bible/_archive/**` | 현재 구현 기준에서 명시적으로 제외됨 |
| `docs/_archive/notion-export/**` | 과거 Notion 내보내기 |
| 종료된 회의, 날짜가 있는 일정, 완료된 WBS 기록 | 보존된 이력; 현재 요구사항이 아님 |

## 검토 필요(Needs Review)

- `docs/notion/**`은 현재 스크립트가 읽는 경우에만 유지합니다. 사용 전 정책 수용 여부를 Product Bible과 대조해 검토하세요.
- `docs/design/**/prompts/**`, 플러그인 문서, 이전 디자인 후보: 유용한 도구 이력이지만 현재 Figma 및 Pack 08과 대조해야 합니다.

## Product Bible 검토 후보 고유 정보

1. 디바이스 이벤트 로그 및 API 성능 목표.
2. 한/영 UI 전환, QR/바코드 스캔, 포장 봉투 옵션, 세트 할인, 고급 토핑 수량 제어.
3. Pack 09에 없는 과거 요구사항 근거 및 QA 증거.

위 항목은 검토 후보일 뿐입니다. 사람이 Product Bible에 수용하기 전까지는 MVP 약속이 아닙니다.
