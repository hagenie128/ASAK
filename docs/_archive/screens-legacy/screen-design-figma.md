# ASAK 화면 설계 · Figma 연동 요약

> [`TABLET_PORTRAIT_FIGMA_SETUP.md`](../design/TABLET_PORTRAIT_FIGMA_SETUP.md) · Wiki: [id=5](https://devcopilot.ai.kr/workspace/2/wiki/5)

## 팀 Figma (정본)

| 항목 | 값 |
|------|-----|
| 파일 | `kiosk_design` |
| URL | [https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) |
| 형태 | 태블릿 세로 **834×1194** |
| frame 패턴 | `?node-id={nodeId}` → [`figma-links.template.json`](../design/figma-links.template.json) |

## Page 구조 (파일 내 · Notion 정본)

> **무료 플랜: 페이지 최대 3개** — 7페이지(00~06)는 02/03/04로 통합. 상세 체크리스트: [Notion Figma Setup](https://app.notion.com/p/39451ef04f0b81c1b71accd381097699)

| Page | SCR | 내용 | 방법 |
|------|-----|------|------|
| 02. User Flow | — | Cover·흐름·Prototype·DS·Archive | 수동 (SCR 프레임 없음) |
| 03. Kiosk Screens | SCR-001~014, 020~021 | 키오스크·Day10 관리자·예외 | 플러그인 834×1194 |
| 04. Admin Screens | SCR-015~019 | 후반 관리자 | 플러그인 834×1194 |

플러그인: [`figma-rename-scr-plugin/README.md`](../design/figma-rename-scr-plugin/README.md)

## 참고 (Community → kiosk_design 내 참고)

| 링크 | 용도 |
|------|------|
| [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) | flow |
| [Kiosk UI/UX Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) | 세로 UX |
| [Moja UI + Dark Mode](https://www.figma.com/community/file/1108679668074690379/moja-ui-ultimate-ui-kit-design-system-variables-darkmode) | Variables |
| [Design Systems Checklist](https://www.figma.com/community/file/1152167555200057574/design-systems-checklist) | DS QA |
| [Courses Dashboard UI KIT](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT) | Admin UI |

## 추적

- **Notion**: [04. 화면 설계](https://app.notion.com/p/1c751ef04f0b825ea3aa8145f563bbc8)
- **DevCopilot**: Wiki id=5, Screens `figmaUrl`
- **Repo**: [`SCR_TABLET_PORTRAIT_FRAMES.md`](../design/SCR_TABLET_PORTRAIT_FRAMES.md)
