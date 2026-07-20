# ASAK Figma 플러그인 안내

현재 운영 플러그인은 아래 3개입니다. 모두 Figma Desktop에서 **Plugins → Development → Import plugin from manifest…**로 각 `manifest.json`을 등록합니다.

| 순서 | 플러그인 | 용도 |
|---:|---|---|
| 1 | [SCR Frame Rename](./figma-rename-scr-plugin/README.md) | 화면명을 `SCR-XXX 화면명`으로 정리하고 Kiosk/Admin 페이지로 이동 |
| 2 | [Create DS-02 Components](./figma-create-ds02-components-plugin/README.md) | DS-02 컴포넌트 라이브러리와 UI Kit 생성 |
| 3 | [Apply DS-02 Theme](./figma-apply-ds02-theme-plugin/README.md) | 기존 프레임 또는 선택 영역에 DS-02 색상 적용 |

디자인 정본은 [kiosk-design-system.md](./kiosk-design-system.md)입니다. Candidate B 선택 기록은 [Archive](../archive/design-migrations/kiosk-design-system-candidate-B.md)에 보존합니다. 후보 프레임 생성 플러그인은 DS-02 컴포넌트 플러그인으로 통합해 제거했습니다.
