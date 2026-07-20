# ASAK Greens Kiosk — Design System (MASTER)

> **파일**: `kiosk_design` · **Frame**: 834×1194 (태블릿 세로)  
> **색상 후보**: [kiosk-design-system-index.md](./kiosk-design-system-index.md) (A~E · Trend-1~5 **병합 없음**)  
> **CSS**: [`kiosk-tokens.css`](./kiosk-tokens.css) (viewer 기본) · 후보별 [`kiosk-tokens-candidate-*.css`](./kiosk-design-system-index.md#5-git-파일-목록)

샐러드 키오스크(ASAK/Greens) UI의 **공통 구조** 토큰·컴포넌트 정의입니다.  
**색상 팔레트는 팀이 A~E 중 1안을 확정할 때까지 후보별로 분리** 유지합니다. 아래 Color는 현재 `frontend/viewer` 구현 기본값이며, Trend·후보와 **병합하지 않습니다**.

---

## 1. Color Palette

### Semantic (기본 모드)

| Token | Hex | 용도 | 대비 (on white) |
|-------|-----|------|-----------------|
| **Primary** | `#2D8A4E` | CTA, 브랜드 마크, 활성 칩 | 4.6:1 ✓ |
| **Primary Dark** | `#16361F` | 헤더·사이드바·강조 배경 | 12.1:1 ✓ |
| **Secondary** | `#7CB69A` | 보조 버튼, 태그, 아이콘 | 3.1:1 (대형 텍스트) |
| **Accent** | `#7CB69A` | 보조 강조, 태그 | 3.1:1 (대형 텍스트) |
| **Success** | `#16A34A` | 주문 완료, 품절 해제 | 4.5:1 ✓ |
| **Error** | `#DC2626` | 결제 실패, 품절, 경고 | 4.6:1 ✓ |
| **Warn** | `#B45309` | 타임아웃, 주의 | 4.5:1 ✓ |

### Neutral

| Token | Hex | 용도 |
|-------|-----|------|
| **Background** | `#F4F7F2` | 화면 배경 |
| **Surface** | `#FFFFFF` | 카드·패널 |
| **Text** | `#1A2E1A` | 본문·제목 |
| **Text Muted** | `#5C6B5C` | 부가 정보, 메타 |
| **Border** | `#DDE6D8` | 구분선, 카드 테두리 |
| **Border Strong** | `#B9DCC4` | 활성 칩 테두리 |

### Soft fills

| Token | Hex | 용도 |
|-------|-----|------|
| Primary Soft | `#E8F5EC` | 선택 행, 활성 칩 배경 |
| Secondary Soft | `#E8F5EC` | 보조 배경, 칩 |
| Success Soft | `#DCFCE7` | 성공 배너 |
| Error Soft | `#FEE2E2` | 오류 배너 |
| Warn Soft | `#FFF7ED` | 경고 배너 |

> **DS 구조 (2026-07-06)**: 회의 채택안 **Candidate B / DS-02 Modern Minimal**의 현재 정본은 이 문서와 [kiosk-tokens.css](./kiosk-tokens.css)입니다. 선택 기록은 [Archive](../archive/design-migrations/kiosk-design-system-candidate-B.md)에 보존합니다. Trend 색상 참고: [color-swatches.html](./color-swatches.html).

---

## 2. Typography

| Token | Family | Size | Weight | Line height | 용도 |
|-------|--------|------|--------|-------------|------|
| **Display** | Pretendard | 48px | 700 | 1.2 | 홈 히어로 (SCR-001) |
| **Title** | Pretendard | 40px | 700 | 1.2 | 화면 제목 |
| **Subtitle** | Pretendard | 32px | 600 | 1.3 | 섹션 제목 |
| **Body** | Pretendard | 24px | 400 | 1.45 | 메뉴 설명, 본문 |
| **Body SM** | Pretendard | 20px | 400 | 1.45 | 옵션 라벨 |
| **Caption** | Pretendard | 18px | 400 | 1.45 | 품절·태그 |
| **CTA** | Pretendard | 28px | 700 | 1.2 | 버튼 라벨 |
| **Price** | Pretendard | 36px | 700 | 1.2 | 금액 표시 |

**Fallback stack**: `"Pretendard", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif`

Figma에 Pretendard가 없으면 **Inter**로 대체 후, 한글 스타일은 Pretendard 설치 시 교체.

---

## 3. Spacing (8pt grid)

| Token | Value | 용도 |
|-------|-------|------|
| space-1 | 8px | 아이콘·텍스트 간격 |
| space-2 | 16px | 카드 내부 패딩, gutter |
| space-3 | 24px | 섹션 간격, safe area 상하 |
| space-4 | 32px | 화면 좌우 여백 (콘텐츠) |
| space-5 | 40px | 리스트 항목 간격 |
| space-6 | 48px | 터치 타깃 최소 높이 |
| space-7 | 56px | CTA 바 높이 |
| space-8 | 64px | 히어로 여백 |

**Grid**: 12 column · margin 16 · gutter 16 (834px frame 기준)

---

## 4. Touch Targets

| 규칙 | 값 |
|------|-----|
| 최소 터치 영역 | **48×48px** (WCAG 2.5.5 권장) |
| 절대 최소 | 44×44px (iOS HIG) |
| CTA 버튼 높이 | 56px (풀폭) |
| Option Chip | min 48px 높이, padding 12×20 |
| 아이콘 버튼 | 48×48 hit area (아이콘 24px) |

---

## 5. Border Radius & Shadows

| Token | Value | 용도 |
|-------|-------|------|
| radius-sm | 8px | 칩, 작은 카드 |
| radius-md | 14px | 메뉴 카드, 패널 |
| radius-lg | 20px | 모달, 히어로 이미지 |
| radius-pill | 999px | 검색, 필터 칩 |
| shadow-sm | `0 2px 8px rgba(26,46,26,0.06)` | 칩 hover |
| shadow-md | `0 8px 24px rgba(26,46,26,0.08)` | 카드 |
| shadow-lg | `0 16px 40px rgba(26,46,26,0.12)` | 플로팅 CTA |

---

## 6. Components

### Primary Button

- 배경: Primary `#2D8A4E` · 텍스트: `#FFFFFF` · CTA 28px Bold
- 높이 56px · radius-pill 또는 radius-md(14px) · 풀폭(좌우 safe 16)
- Hover/Pressed: Primary Dark `#16361F`
- Disabled: 배경 `#DDE6D8` · 텍스트 `#5C6B5C`

### Secondary Button

- 배경: Surface · 테두리 2px Border Strong · 텍스트 Primary
- 높이 48px · 동일 radius
- 용도: 취소, 이전, 보조 액션

### Menu Card (SCR-003)

- 크기: 2열 그리드 (gutter 16) · 카드 min-height 200px
- 이미지: 상단 16:9 crop · radius-md 상단
- 제목: Body 24px Semibold · 가격: Price 36px · 품절: Caption + Error 색

### Option Chip (SCR-004)

- 기본: Surface + Border 1px · Body SM 20px · padding 12×20 · radius-pill
- 선택: Primary Soft 배경 + Border Strong + Primary 텍스트 Bold
- 다중 선택 / 단일 선택 동일 스타일 · min-height 48px

### Cart Item Row (SCR-005)

- 높이 min 72px · 썸네일 56×56 radius-sm
- 제목 Body · 옵션 Caption Muted · 수량 스테퍼 48×48
- 구분선 Border 1px · 선택 시 Primary Soft 배경

### Header

- 높이 64px · 좌: 뒤로(48×48) · 중: Title 32px · 우: 접근성(48×48) → **SCR-014**
- 배경 Surface · 하단 Border 1px

### Footer CTA Bar

- 고정 하단 · padding 16 · 배경 Surface · 상단 shadow-md
- Primary Button 풀폭 + 합계 Price 36px 우측 정렬
- Safe area bottom 24px 포함

---

## 7. Accessibility

| 항목 | 기준 | 구현 |
|------|------|------|
| 본문 대비 | WCAG AA 4.5:1 | Text `#1A2E1A` on Surface ✓ |
| 대형 텍스트 | 3:1 | Title·Price ✓ |
| 터치 | 48px | §4 참고 |
| 큰 글자 모드 | +33% scale | `data-a11y-large-text` → [kiosk-tokens.css](./kiosk-tokens.css) |
| 고대비 모드 | 7:1 목표 | `data-a11y-high-contrast` → 검정/흰/진녹 |
| 설정 화면 | — | **[SCR-014 접근성 설정](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design)** |

---

## 8. Figma 적용

| 항목 | 위치 |
|------|------|
| DS 요약 frame | `02. User Flow` → **Design System** frame (플러그인 생성) |
| Variables | Collection `ASAK / Color` · modes: `asak-trend-*` |
| SCR 적용 | `03. Kiosk Screens` 각 frame에 토큰 적용 |

**플러그인**: [`figma-create-ds02-components-plugin`](./figma-create-ds02-components-plugin/README.md) — DS-02 컴포넌트·UI Kit 생성

---

## 관련 문서

- [kiosk-design-system-index.md](./kiosk-design-system-index.md) — A~E · Trend 매핑 (병합 없음)
- [Archive 비교표](../archive/design-migrations/kiosk-design-system-comparison.md) — 팀 비교표 · 왜 다른가
- [Figma 태블릿 세로 Setup](https://app.notion.com/p/39451ef04f0b81c1b71accd381097699)
- [color-swatches.html](./color-swatches.html)
- [figma-links.template.json](./figma-links.template.json)
- [SCR_FIGMA_CHECKLIST.md](./SCR_FIGMA_CHECKLIST.md)
