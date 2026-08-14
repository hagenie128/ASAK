# ASAK README·Cloudinary 문서 동기화 근거

## 1. 대상과 기준

| 저장소 | 기준 커밋 | 확인 범위 |
|---|---|---|
| Workspace | `76c18e7` | 루트 README와 다섯 독립 저장소 안내 |
| ASAK | `9c4ab9c` | 문서·데이터·이미지 README |
| ASAK-Admin | `7a5d451` | 화면 구조·실API/mock·이미지 표시 |
| ASAK-Kiosk | `d4203bd` | 주문 흐름·API·PWA·이미지 표시 |
| ASAK-back | `536334e` | Controller·Service·Mapper·DTO·Cloudinary 전환 |

작업일: 2026-08-14

## 2. 확인한 코드·문서

- Backend `build.gradle`, Controller 11개, Service·Mapper·Mapper XML 실제 구조
- `CreateMenuRequest.mediaAssetId`, `AdminMenuService.resolveMediaAssetId`
- `AdminMenuMapper.xml`, `UserMenuMapper.xml`의 `media_asset` JOIN
- `ASAK-back/docs/MENU_IMAGE_ASSET_FLOW.md`
- Admin `AdminApp.jsx`, API·Hook·mock repository, 메뉴 패널의 `imageUrl`
- Kiosk `KioskApp.jsx`, 메뉴·장바구니·주문 API, 이미지 사용 컴포넌트
- 각 앱 `package.json`, `.env.example`, Vite/PWA 설정
- 워크스페이스와 ASAK 하위 README 목록 및 기존 변경

## 3. 갱신한 README

### 주요 진입 문서

- `README.md`
- `ASAK/README.md`
- `ASAK-Admin/README.md`
- `ASAK-Kiosk/README.md`
- `ASAK-back/README.md`

주요 앱 README는 제목·배지·빠른 링크를 통일하고, 초보자가 파일 역할을 따라갈 수 있도록 실제 구조도와 기능 상태를 자세히 적었다.

### 앱 보조 문서

- `ASAK-Admin/src/README.md`
- `ASAK-Admin/src/mocks/README.md`
- `ASAK-Admin/public/mocks/README.md`
- `ASAK-Kiosk/src/README.md`
- `ASAK-Kiosk/src/mocks/README.md`
- `ASAK-Kiosk/public/mocks/README.md`
- `ASAK-back/api/README.md`
- `ASAK-back/docs/guides/README.md`

### 데이터·이미지 경계

- `ASAK/asak-data/README.md`
- `ASAK/asak-data/images/README.md`
- `ASAK/asak-data/images/ingredient-assets/README.md`
- `ASAK/data-pipeline/README.md`

이외 ASAK 저장소의 다수 README에는 이 작업 전부터 진행 중이던 문서 구조 정리 변경이 있다. 해당 변경을 되돌리지 않고 현재 내용을 보존했다.

## 4. API 번호 표기 (Kiosk + Admin)

`ASAK-back/IMPLEMENTATION_PLAN.md` §4의 API 번호를 아래 README에 맞춰 표기했다.

| 파일 | 반영 내용 |
|---|---|
| `ASAK-back/README.md` | 키오스크·관리자 API 번호 + 미구현 Controller |
| `ASAK-Admin/README.md` | 화면·경로·프론트 함수 ↔ API 번호 |
| `ASAK-Kiosk/README.md` | 주문 단계·연결 표에 API-001~006, 014 |
| `ASAK-Admin/src/README.md` · `src/mocks/README.md` · `public/mocks/README.md` · `docs/README.md` | 실연동/mock API 번호 |
| `ASAK-Kiosk/src/README.md` · `public/mocks/README.md` | 키오스크 API 번호 |
| `ASAK-back/api/README.md` | Bruno Admin 메뉴 seq ↔ API 번호 |

| API | 상태 |
|---|---|
| API-007, 008, 011, 012, 013, 021, 022, 024 | Controller·프론트 호출 모두 구현됨 |
| API-009 / 010 (품절) | Controller 비어 있음 · Admin은 mock |
| API-015 / 016 (결제수단) | Controller 비어 있음 · 경로 표기 불일치 |
| API-017 / 018 / 019 (매출) | Controller 비어 있음 · Admin은 mock |
| API-020 (대시보드) | Controller 비어 있음 · Admin은 mock |
| 메뉴 삭제·카테고리·재료·옵션 그룹 조회 | 번호 없는 보조 endpoint로 표기 |

### 후속 README 정합성 보정

- `ASAK-Admin/public/mocks/README.md`: 토스페이, `totalAmount`, 실제 주문 컴포넌트·API 경로, 환불·영수증 미구현 상태 반영
- `ASAK-Kiosk/public/mocks/README.md`: 결제 오류 모달 흐름과 API-006 경로 계약 불일치 기록
- `docs/planning/README.md`, `docs/operations/README.md`: 누락된 문서 인덱스 추가
- `docs/product_bible/06_Engineering_Bible/README.md`: Spring Boot 실제 버전 `4.0.7` 반영
- `asak-data/images/**/README.md`: 재료·메뉴 이미지 스크립트 상대경로 수정
- `worklog/README.md`: `team_config.json` 기준 현재 2인 팀 반영
- `docs/design/figma-rename-scr-plugin/README.md`: 구 플러그인의 SCR-020/021 충돌을 `LEGACY / 사용 중지`로 명시

### PWA 반영

- `ASAK-Kiosk/README.md` · `ASAK-Admin/README.md`: PWA 전용 섹션 추가 (manifest, orientation, fullscreen 코드 경로)
- `docs/operations/setup/android-pwa-fullscreen.md`: Kiosk + Admin 공통 설치 절차로 갱신, `entries/kiosk.jsx` 경로 수정
- 워크스페이스·`ASAK/README`·`docs/README`·`START_HERE`·Admin docs 목차에 PWA 링크 추가

## 5. Cloudinary 변경 근거

현재 확인된 런타임 흐름:

```text
Cloudinary → media_asset.url → menu.image_asset_id
→ Mapper JOIN → API imageUrl → Kiosk/Admin <img>
```

- 프론트 응답 필드 `imageUrl`은 유지한다.
- Kiosk는 Cloudinary SDK를 직접 호출하지 않고 공개 URL을 표시한다.
- Admin 목록·상세도 공개 `imageUrl`을 표시한다.
- Admin 메뉴 등록·수정은 아직 `mediaAssetId` 선택 UI가 없고 레거시 `imageUrl` 호환 경계를 사용한다.
- Backend에는 Cloudinary 업로드 API가 아직 없다.
- `asak-data/images/**`는 원본·가공·복구·재업로드 소스이며 앱 런타임 URL 정본이 아니다.

## 6. 검증 결과

- 각 저장소에서 `git diff --check` 실행
- 발견된 README trailing whitespace와 Kiosk README EOF 공백 수정
- 새로 추가한 상대 링크의 대상 경로 확인
- 문서 작업이므로 앱 빌드·테스트는 실행하지 않음

## 7. 남은 불일치·결정 필요

1. Admin 메뉴 편집에 `mediaAssetId`를 직접 선택·전송하는 UI가 없다.
2. Cloudinary 업로드·서명·`media_asset` INSERT 책임이 서버 API인지 별도 관리 도구인지 결정이 필요하다.
3. `image_asset_id`가 없는 기존 메뉴의 수동 연결과 실제 DB 반영은 미검증이다.
4. Kiosk의 Cloudinary SDK 의존성은 현재 직접 사용되지 않아 유지·제거 판단이 필요하다.
5. Admin 결제수단 Cloudinary SVG는 attachment 응답 가능성이 있어 로컬 glyph fallback을 유지한다.
6. API-015/016 결제수단 경로가 코드 camelCase와 Product Bible kebab-case로 갈려 있어 정본 확정이 필요하다.
7. Kiosk `API_ENDPOINTS.payments`가 `/payments`이고 백엔드 API-006은 `/api/kiosk/payments`여서 화면 연결 전 수정·계약 검증이 필요하다.
8. 레거시 Figma rename 플러그인 코드는 SCR-020/021을 구 확장 화면으로 생성하므로 현재 0718 정본에 사용하지 않는다.

## 8. 수정하지 않은 범위

- 소스코드와 DB
- Cloudinary 원격 자산·설정
- Figma·DevCopilot·Notion 원격 데이터
- Git commit·push·branch
