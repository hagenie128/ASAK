# Apply DS-02 Theme (Y2K → Salady)

커뮤니티 [Y2K UI Kit (Retro Bubblegum)](https://www.figma.com/design/ndHUuQpfTvanwdspoIKM4Q/Y2K-UI-Kit)을 **사용자 사본**에서 DS-02 Modern Minimal로 일괄 리컬러하는 Figma 플러그인입니다.

| 항목 | 값 |
|------|-----|
| 플러그인 이름 | **Apply DS-02 Theme (Y2K → Salady)** |
| 경로 | `docs/design/figma-apply-ds02-theme-plugin/` |
| 대상 페이지 | `02. User Flow` (권장) |
| 토큰 | charcoal `#1A1C20` · lime `#C8F135` · surface `#F5F5F0` |

## 설치

1. Figma Desktop → **Plugins → Development → Import plugin from manifest…**
2. `manifest.json` 선택
3. `kiosk_design` 파일에서 실행

## 명령

| 명령 | 동작 |
|------|------|
| **현재 페이지에 DS-02 적용** | 페이지 전체 노드 순회 |
| **선택 영역에 DS-02 적용** | 선택 프레임/섹션만 |

## 매핑 규칙

- 핑크·마젠타·퍼플 fill/stroke (`#FF69B4`, `#E91E8C`, `#FF4D8D` 등) → lime `#C8F135` 또는 charcoal `#1A1C20`
- 연한 핑크 배경 → `#F5F5F0` / `#FFFFFF`
- `Retro Bubblegum` 등 브랜딩 텍스트 → `ASAK Salady · DS-02`
- `Foundations` / `Colour Palette` 섹션 제목 → Inter Extra Bold · charcoal
- 이름에 palette/colour 포함 프레임 내 스와치 그리드 → DS-02 시맨틱 8행 램프

## Mock 테스트

```bash
node docs/design/figma-apply-ds02-theme-plugin/_test_mock.js
```

## 관련 문서

- [Archive migration mapping](../../archive/design-migrations/y2k-to-ds02-migration.md)
- [figma-create-ds02-components-plugin](../figma-create-ds02-components-plugin/README.md)
- [Figma 플러그인 안내](../FIGMA_PLUGINS.md)
