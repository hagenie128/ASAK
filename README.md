# ASAK

> **👉 문서·구현 입구:** [**START_HERE**](docs/START_HERE.md) · [**PROJECT_HUB**](PROJECT_HUB.md)  
> **Current structure notice (2026-07-16/20):** 실행 코드는 `ASAK-Kiosk`, `ASAK-Admin`, `ASAK-back`. 이 저장소는 문서·데이터·Product Bible. 아래 `frontend/`·`ASAK-front` 안내는 **Legacy Reference** — 신규 작업에 쓰지 마세요. 현실: [baseline](docs/wiki/current-status-baseline.md).

> **설치/온보딩:** [**GETTING_STARTED**](docs/operations/setup/GETTING_STARTED.md) · [**INSTALL_WINDOWS**](docs/operations/setup/INSTALL_WINDOWS.md) · Notion [팀 온보딩](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b)

`ASAK`는 `A Salad A Kiosk`의 **문서·데이터·Product Bible** 정본 저장소입니다.  
앱 실행 코드는 워크스페이스의 `ASAK-Kiosk` · `ASAK-Admin` · `ASAK-back`에 있습니다.  
로컬에서는 보통 `ASAK-workspace` + `ASAK.code-workspace`로 네 저장소를 함께 엽니다. ([워크스페이스 README](../README.md))

**9주 (7/2~9/2)** · Week 5 MVP · 최종 발표 9/2(수).  
할 일: [WBS 2.0](docs/wiki/wbs-v2-2026-07-16.md) · 현실: [baseline](docs/wiki/current-status-baseline.md) · Notion [프로젝트 허브](https://app.notion.com/p/39151ef04f0b808f99f8ea068efb5790)

## 저장소 역할 (2026-07-20)

| 폴더 / 원격 | 역할 |
|---|---|
| `ASAK` → `hagenie128/ASAK` | docs, Product Bible, asak-data, worklog |
| `ASAK-Kiosk` → `hagenie128/ASAK-Kiosk` (로컬 remote가 `ASAK-front`일 수 있음) | 고객 키오스크 React |
| `ASAK-Admin` → `hagenie128/ASAK_Admin` | 관리자 React **정본** |
| `ASAK-back` → `hagenie128/ASAK-back` | Spring Boot (현재 health only) |

> `frontend/` · `ASAK-front` 단독 클론 안내는 **Legacy**. 신규 작업은 위 표만 따르세요.

## 작업 방식

네 폴더는 **서로 다른 Git 저장소**입니다. 변경은 **해당 폴더에서** 커밋·푸시합니다.

```powershell
# 문서
cd C:\ASAK-workspace\ASAK

# 키오스크 / 관리자 / 백엔드
cd C:\ASAK-workspace\ASAK-Kiosk
cd C:\ASAK-workspace\ASAK-Admin
cd C:\ASAK-workspace\ASAK-back
```

구조·계획: 각 앱 `IMPLEMENTATION_PLAN.md`, `src/STRUCTURE_GUIDE.md` · 문서 입구: [START_HERE](docs/START_HERE.md)
## 데이터·이미지

키오스크 **학원 과제·포트폴리오**용입니다. 메뉴 데이터·이미지는 [샐러디(salady.com)](https://salady.com) 공개 정보를 참고했습니다. 상업적 서비스·실매장 배포에는 그대로 사용하지 마세요.

```powershell
python asak-data/scripts/download_menu_images.py
python asak-data/scripts/apply_original_images.py
```

- 원본 썸네일: `asak-data/images/original/`
- 키오스크용 경로: `asak-data/images/menu/` → `menu.json`의 `/assets/menu/{id}.png`

## 문서 — Notion vs Git

| Git (ASAK repo) 유지 | Notion (본문 정본) |
|----------------------|-------------------|
| 스크립트, JSON, HTML (`color-swatches.html`, `figma-links.template.json`) | [📐 디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) 하위 가이드 |
| `asak-data/scripts/*`, `docs/screens/*` export | [04. 화면 설계](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8) · SCR DB |
| `docs/wiki/*` DevCopilot source | DevCopilot Wiki + Notion 링크 |
| `docs/guides/*` 팀 온보딩·Issue·작업 기록 | [📖 문서 읽는 순서](https://app.notion.com/p/39451ef04f0b81088a91d914f985fb11) |
| `worklog/daily/` sync | [📅 일일 워크로그 DB](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9) · 사용법 [팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) |

Git `docs/design/*.md`는 **Notion 링크 stub**만 유지합니다. Notion 페이지 상단 **Git 도구만** 섹션에서 로컬 도구 링크를 제공합니다.

## 디자인 · Figma (가이드 본문 → Notion)

| Git stub | Notion (편집) |
|----------|---------------|
| [`SCR_TABLET_PORTRAIT_FRAMES.md`](docs/design/SCR_TABLET_PORTRAIT_FRAMES.md) | [SCR 화면별 가이드](https://app.notion.com/p/39451ef04f0b81109d07c01293d73c6d) |
| [`BRAND_DESIGN_OPTIONS.md`](docs/design/BRAND_DESIGN_OPTIONS.md) | [브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) |
| [`TABLET_PORTRAIT_FIGMA_SETUP.md`](docs/design/TABLET_PORTRAIT_FIGMA_SETUP.md) | [Figma 태블릿 세로 Setup](https://app.notion.com/p/39451ef04f0b81c1b71accd381097699) |
| [`FIGMA_GUIDE.md`](docs/design/FIGMA_GUIDE.md) | [Figma 가이드 + SCR×Figma](https://app.notion.com/p/39451ef04f0b81849dc7d81f8106b5ad) |
| [`SCREENS_UPLOAD_GUIDE.md`](docs/design/SCREENS_UPLOAD_GUIDE.md) | [DevCopilot/Wiki 업로드](https://app.notion.com/p/39451ef04f0b81bc83a1f291eeb1ce31) |
| [`NOTION_DB_COLOR_GUIDE.md`](docs/design/NOTION_DB_COLOR_GUIDE.md) | [DB 색상 수동 가이드](https://app.notion.com/p/39451ef04f0b810d81f6eea53c4d0682) |

Hub (**시작**: [📐 디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc)) · 화면 목록 정본: [04. 화면 설계 SCR DB](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8)

읽기 순서: 1 브랜드 → 2 Figma Setup → 3 SCR wireframe → 4 Figma 매트릭스 → 5 DevCopilot 업로드

Git 로컬 도구: [`color-swatches.html`](docs/design/color-swatches.html) · [`figma-links.template.json`](docs/design/figma-links.template.json) · [`SCR_FIGMA_CHECKLIST.md`](docs/design/SCR_FIGMA_CHECKLIST.md)

## 팀 세팅 가이드

**신규 합류:** Windows PC → [`docs/operations/setup/INSTALL_WINDOWS.md`](docs/operations/setup/INSTALL_WINDOWS.md) · Notion [🚀 처음 시작하기](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b) · [`docs/operations/setup/GETTING_STARTED.md`](docs/operations/setup/GETTING_STARTED.md) → [`docs/guides/README.md`](docs/guides/README.md) 순으로 읽으세요.

팀원 온보딩·Issue·작업 기록 템플릿은 [`docs/guides/`](docs/guides/README.md)에 있습니다.

| 순서 | Git | 내용 |
|------|-----|------|
| 01 | [`01-team-setup.md`](docs/guides/01-team-setup-2026-07-16.md) | 클론·세팅·Git·9주 일정 |
| 02 | [`02-github-issues-guide.md`](docs/guides/02-github-issues-guide-2026-07-16.md) | Issue·라벨·WBS |
| 03–06 | [`03`](docs/guides/03-work-log-template-2026-07-02.md) · [`04`](docs/guides/04-sample-work-log-example-2026-07-02.md) · [`05`](docs/guides/05-personal-portfolio-template-2026-07-06.md) · [`06`](docs/guides/06-team-ai-prompt-2026-07-06.md) | 작업 기록·포트폴리오·AI 프롬프트 |

- `worklog/` — 일일 워크로그 + [캘린더 뷰](worklog/calendar/index.html) · [README 확인 순서](worklog/README.md) · 개인 stub: [`guide-personal-worklog.md`](worklog/guide-personal-worklog.md) → Notion [팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95)
