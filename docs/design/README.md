# 디자인 문서

이 폴더는 현재 반복 사용하는 Figma 실행 기준만 둡니다. 제품 정책과 SCR 정본은 각각 `docs/product_bible/`과 `docs/product_bible/07_Screen_Bible/`에서 확인합니다.

## 정본

- `FIGMA_GUIDE.md`: Figma와 SCR 매핑의 진입점
- `FIGMA-TOKEN-REPORT.md`: 0718 이식 중 관찰한 토큰·이탈 정리
- `kiosk-design-system.md`, `kiosk-design-system-index.md`, `kiosk-tokens.css`: 현재 디자인 시스템·토큰
- `SCR_TABLET_PORTRAIT_FRAMES.md`, `TABLET_PORTRAIT_FIGMA_SETUP.md`: 현재 태블릿 프레임 기준
- `SCREENS_UPLOAD_GUIDE.md`: DevCopilot 업로드 시 현재 Screen Registry를 참조하는 방법

완료 감사는 `../archive/design-audits/`, 완료 프롬프트는 `../archive/design-prompts/`, 과거 병합/후보 비교는 `../archive/design-migrations/`에 보관합니다. 플러그인 소스와 자산은 실행 자산이므로 이 cleanup에서 이동하거나 수정하지 않습니다.

```powershell
git status -- docs/design docs/archive/design-*
```
