# ASAK

> **👉 문서·구현 입구:** [**문서 시작**](docs/START_HERE.md) · [**프로젝트 허브**](PROJECT_HUB.md)
> **현재 구조 안내 (2026-07-16/20):** 실행 코드는 `ASAK-Kiosk`, `ASAK-Admin`, `ASAK-back`에 있습니다. 이 저장소는 문서·데이터·제품 기준 문서의 정본입니다. `frontend/`·`ASAK-front` 안내는 **과거 참고 자료**이므로 신규 작업에 사용하지 마세요. 현재 구현 상태는 [구현 현황 요약](docs/wiki/current-status-baseline.md)을 봅니다.

> **설치/첫 시작:** [**시작 안내**](docs/operations/setup/getting-started.md) · [**윈도우 설치**](docs/operations/setup/install-windows.md) · Notion [팀 온보딩](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b)

`ASAK`는 `A Salad A Kiosk`의 **문서·데이터·제품 기준 문서** 정본 저장소입니다.
앱 실행 코드는 워크스페이스의 `ASAK-Kiosk` · `ASAK-Admin` · `ASAK-back`에 있습니다.
로컬에서는 보통 `ASAK-workspace` + `ASAK.code-workspace`로 네 저장소를 함께 엽니다. ([워크스페이스 README](../README.md))

**9주 (7/2~9/2)** · Week 5 MVP · 최종 발표 9/2(수).
할 일: [작업 분해표](docs/wiki/wbs.md) · 현재 상태: [구현 현황 요약](docs/wiki/current-status-baseline.md) · Notion [프로젝트 허브](https://app.notion.com/p/39151ef04f0b808f99f8ea068efb5790)

## 저장소 역할 (2026-07-20)

| 폴더 / 원격 | 역할 |
|---|---|
| `ASAK` → `hagenie128/ASAK` | 문서, 제품 기준 문서, 데이터, 작업 기록 |
| `ASAK-Kiosk` → `hagenie128/ASAK-Kiosk` | 고객 키오스크 React |
| `ASAK-Admin` → `hagenie128/ASAK_Admin` | 관리자 React **정본** |
| `ASAK-back` → `nayeon0828/ASAK-backend` | Spring Boot API (로컬 폴더명은 `ASAK-back`) |

> `frontend/` · `ASAK-front` 단독 복제 안내는 **과거 방식**입니다. 신규 작업은 위 표만 따르세요.

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

## 문서 — Notion과 Git의 역할

| Git 저장소에 유지 | Notion 본문 정본 |
|----------------------|-------------------|
| 스크립트, JSON, HTML (`color-swatches.html`, `figma-links.template.json`) | [📐 디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) 하위 가이드 |
| `asak-data/scripts/*`, `docs/screens/*` export | [04. 화면 설계](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8) · SCR DB |
| `docs/wiki/*` DevCopilot source | DevCopilot Wiki + Notion 링크 |
| `docs/guides/*` 팀 온보딩·Issue·작업 기록 | [📖 문서 읽는 순서](https://app.notion.com/p/39451ef04f0b81088a91d914f985fb11) |
| `worklog/daily/` sync | [📅 일일 워크로그 DB](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9) · 사용법 [팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) |

Git `docs/design/*.md`는 **Notion 링크 stub**만 유지합니다. Notion 페이지 상단 **Git 도구만** 섹션에서 로컬 도구 링크를 제공합니다.

## 디자인 · Figma

| Git 안내 파일 | Notion 편집 문서 |
|----------|---------------|
| [디자인 문서 입구](docs/design/README.md) | [디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) |
| [`figma-guide.md`](docs/design/figma-guide.md) | [Figma 가이드 + 화면 매트릭스](https://app.notion.com/p/39451ef04f0b81849dc7d81f8106b5ad) |

Hub (**시작**: [📐 디자인 & 화면](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc)) · 화면 목록 정본: [04. 화면 설계 SCR DB](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8)

읽기 순서: 1 브랜드 → 2 Figma 설정 → 3 화면 설계 초안 → 4 Figma 매트릭스 → 5 DevCopilot 업로드

예전 Git 안내 파일은 [`docs/design/_archive/`](docs/design/_archive/)에 있습니다. 신규 작업은 위 Notion 페이지와 [디자인 문서 입구](docs/design/README.md)만 사용하세요.

## 팀 세팅 가이드

**신규 합류:** Windows PC → [`docs/operations/setup/install-windows.md`](docs/operations/setup/install-windows.md) · Notion [🚀 처음 시작하기](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b) · [`docs/operations/setup/getting-started.md`](docs/operations/setup/getting-started.md) → [`docs/guides/README.md`](docs/guides/README.md) 순으로 읽으세요.

팀원 온보딩·Issue·작업 기록 템플릿은 [`docs/guides/`](docs/guides/README.md)에 있습니다.

| 순서 | Git | 내용 |
|------|-----|------|
| 01 | [`01-team-setup.md`](docs/guides/01-team-setup.md) | 클론·세팅·Git·9주 일정 |
| 02 | [`02-github-issues-guide.md`](docs/guides/02-github-issues-guide.md) | Issue·라벨·작업 분해표 |
| 03–06 | [`03`](docs/guides/03-work-log-template.md) · [`04`](docs/guides/04-sample-work-log-example.md) · [`05`](docs/guides/05-personal-portfolio-template.md) · [`06`](docs/guides/06-team-ai-prompt.md) | 작업 기록·포트폴리오·AI 요청문 |

- `worklog/` — 일일 워크로그 + [캘린더 뷰](worklog/calendar/index.html) · [README 확인 순서](worklog/README.md) · 개인 stub: [`guide-personal-worklog.md`](worklog/guide-personal-worklog.md) → Notion [팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95)
