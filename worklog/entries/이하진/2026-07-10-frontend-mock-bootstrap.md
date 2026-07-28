# 2026-07-10 프론트엔드 mock 데이터 기반 구축

> 일일: [2026-07-10](../../daily/이하진/2026-07-10.md)

## 1. 기본 정보

- 작업 날짜: 2026-07-10 (React/Vite 초기화 기반은 7/9 커밋에서 시작)
- 담당자: 이하진
- 저장소: ASAK / 이후 ASAK-Kiosk로 분리된 프론트 작업 기준
- 브랜치: `main`
- 관련 이력: PR #1·#2 병합, `d217f16`(React/Vite 초기화), `7dd02f1`(메뉴·옵션·주문·결제 mock), `77256b9`(mock setup·초기 데이터), `172d3cd`(mock data flow 문서 정리)
- 작업 유형: `feature` / `data` / `docs`

## 2. 작업 목적

- 백엔드 업무 API가 완성되기 전에도 키오스크/관리자 화면의 메뉴 선택, 옵션, 주문, 결제 흐름을 정해진 데이터로 검증할 수 있게 한다.
- mock을 임시 하드코딩으로 끝내지 않고, 이후 API adapter로 교체할 때 어떤 필드와 흐름을 맞춰야 하는지 문서화한다.

## 3. 직접 구현 영역

- React·Vite 프론트 기본 진입점과 설정을 추가했다. 이 초기화는 7/9 `d217f16`에서 시작됐고, 7/10에는 화면 작업과 mock data 기반을 병합·보강했다.
- `frontend/public/mocks/asak-admin-data.json`에 메뉴, 옵션, 주문, 결제 관리용 mock 데이터를 추가했다.
- `MOCK_SETUP.md`에 mock 파일 위치, 데이터 흐름, 화면 연결 시 주의할 점을 정리했다.
- MySQL seed와 option 정책, 판매 view 동기화용 스크립트도 추가해 mock 계약이 실제 데이터·분석 계약으로 이어질 수 있는 기반을 보강했다.
- 팀원의 홈/메뉴 페이지 작업이 mock 데이터를 연결한 변경과 PR #1·#2 병합 이력을 확인했다. 이 워크로그는 팀원 UI 구현 전체를 본인이 구현했다는 의미가 아니다.

## 4. 구현 로직 / 적용한 방식

### mock 데이터 흐름

1. 화면은 `public/mocks`의 고정 JSON에서 메뉴·옵션·주문·결제 예시를 읽는다.
2. 화면은 mock의 메뉴 정보, 옵션 항목, 주문 상태, 결제 상태를 이용해 UI 흐름을 먼저 만든다.
3. 실제 API가 준비되면 화면 컴포넌트 전체를 바꾸는 대신, API client/adapter에서 응답을 같은 화면 모델로 변환하는 것을 목표로 한다.
4. mock 필드와 서버 계약이 다르면 adapter에서만 legacy 필드를 흡수하고, 화면 내부의 금액·상태 용어는 정본 계약으로 수렴시킨다.

이 날짜의 mock은 화면 작업을 막지 않는 중간 정본이다. API가 구현·검증됐다는 뜻도 아니고, mock만으로 브라우저의 모든 오류 상태를 검증했다는 뜻도 아니다.

## 5. AI 도움 영역

- 사용한 AI: 사후 워크로그 작성 시 커밋·mock setup 문서·데이터 파일의 역할을 대조하는 보조.
- 사람이 수행한 부분: mock의 도메인 범위, 화면 연결 순서, PR 병합과 데이터 문서 반영.
- AI를 사용해도 실제 브라우저·API 결과가 없는 항목은 검증 완료로 기록하지 않는 원칙을 유지했다.

## 6. 발생 이슈

### 이슈 1 — 실제 API 부재로 화면 흐름 검증 불가

- 증상: 주문/결제 백엔드가 준비되기 전에는 화면을 누르며 상태 전환을 확인할 데이터 원본이 없었다.
- 대응: 메뉴·옵션·주문·결제 mock을 먼저 두고, 화면이 소비할 모델을 고정했다.

### 이슈 2 — mock이 서버 계약을 대체하는 문제

- 위험: mock 필드명이 API DTO와 다르면 나중에 컴포넌트 곳곳에서 변환·예외 처리가 중복될 수 있다.
- 대응: `MOCK_SETUP.md`에 데이터 흐름과 교체 방향을 남기고, 이후 API adapter에서 변환하도록 하는 기준을 세웠다.

### 이슈 3 — 화면 구현 책임과 기반 작업의 혼동

- 위험: 같은 날짜의 PR 병합·팀원 화면 작업까지 모두 개인 구현으로 보일 수 있다.
- 대응: 이 기록의 직접 기여는 React/Vite·mock data·setup 기반이며, 병합된 화면 작업은 협업 맥락으로 분리해 기록한다.

## 7. 디버깅 기록

- 확인한 근거: `d217f16`의 Vite 진입/설정, `7dd02f1`의 `asak-admin-data.json`과 seed/policy 스크립트, `77256b9`의 `MOCK_SETUP.md`, `172d3cd`의 데이터 흐름 문서 변경을 대조했다.
- 확인하지 못한 범위: 이 날짜의 `npm run build`, 브라우저 화면, mock fallback, 실제 백엔드 API와의 필드 일치 결과는 저장된 실행 증거가 없다.
- 이후 확인할 위치: `frontend/package.json`, `frontend/src/`, `frontend/public/mocks/asak-admin-data.json`, `MOCK_SETUP.md`, API adapter 경로.

## 8. 이번 작업에서 배운 점

- mock은 단순 더미 데이터가 아니라 UI가 필요로 하는 도메인 필드와 상태를 미리 검증하는 계약 초안이다.
- 화면별 mock을 직접 import하기 시작하면 실제 API 전환 비용이 커지므로, 초기부터 data source와 화면 모델의 경계를 기록해야 한다.

## 9. 개선사항 / TODO

- [ ] 메뉴/옵션/주문/결제 mock의 필드를 API DTO와 대조하고 canonical 이름을 확정한다.
- [ ] 화면별 default/loading/empty/error와 sold-out, 결제 실패, 수량 변경 시나리오를 mock으로 확인한다.
- [ ] API adapter를 도입해 mock과 실응답의 전환 지점을 한 곳으로 모은다.
- [ ] `npm` build/lint와 브라우저 동작을 실제로 기록한다.

## 10. 검증 내용

- Git 로그와 커밋 변경 파일에서 React/Vite 초기화, mock JSON 추가, mock setup 문서, seed/policy·sales-view 동기화 스크립트가 추가된 사실을 확인했다.
- PR #1·#2 병합 이력은 확인했지만, PR의 모든 화면 구현을 본인 직접 구현 또는 기능 완료로 판정하지 않았다.
- 이 날짜에는 build·브라우저·API 통합 결과가 보관되지 않았으므로 정적 변경 근거까지만 기록한다.

## 11. 포트폴리오용 요약

- 실제 API 이전에도 키오스크/관리자 화면 흐름을 개발할 수 있도록 React/Vite 기반과 메뉴·옵션·주문·결제 mock 계약을 만들고, 이후 API adapter로 교체할 데이터 흐름을 문서화했다.

## 12. 참고 자료

- `frontend/public/mocks/asak-admin-data.json`, `MOCK_SETUP.md`
- `frontend/package.json`, `frontend/src/`, `asak-data/scripts/load_seed_mysql.py`, `asak-data/scripts/apply_option_policy_mysql.py`, `asak-data/scripts/create_sales_views_mysql.py`
