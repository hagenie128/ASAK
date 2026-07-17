# Document Structure Plan

## 권장 구조

현재 Product Bible의 Pack 구조를 보존하고, 새 문서는 이동이 아니라 인덱스와 계획 문서로 연결한다.

```text
ASAK/docs
├─ README.md                       # 문서 진입점 (추후 승인 후)
├─ product_bible/                  # Pack 1~12 정본
├─ planning/                       # requirements, scope, WBS, decisions
├─ design/                         # Figma, screen-flow, assets
├─ architecture/                   # frontend, backend, api, database
├─ qa/                             # test-cases, reports, demo
├─ operations/                     # setup, deployment, ai-rules
├─ reference/                      # Notion export 등 참고 자료
└─ _archive/                       # legacy-docs
```

## 배치 원칙

- 중앙 정본: Product Bible, 공통 API/DB 결정, 프로젝트 수준 QA/운영 문서.
- 저장소별 문서: 각 저장소 README, 실행 방법, 국소 구조, 구현 메모. 중앙 문서를 복사하지 않고 링크한다.
- Notion export·회의록: reference 또는 archive 성격으로 보관하고 Product Bible을 대체하지 않는다.
- 기존 경로는 승인 전 이동하지 않는다. 이 구조는 이후 문서 작업의 목적지 제안이다.

## README 연결 구조

루트 `docs/README.md`는 Product Bible Index → 현재 구현 지도 → Gap Report → Priority → 도메인 문서 순으로 연결한다. Kiosk/Admin/Backend README는 각각 해당 Pack 12/11 및 중앙 API/QA 문서를 링크한다.
