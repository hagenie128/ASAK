# 키오스크 디자인 시스템 — 후보 D: Trend Forward

> **(Figma: DS-03 Trend Forward)**

> **컨셉**: 딥 포레스트 + 일렉트릭 민트 · 글래스·그라데이션 · bold 키오스크  
> **캔버스**: 834×1194 (태블릿 세로) · 터치 최소 **44×44px**  
> **정본 참조**: [Notion — 브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [인덱스](./kiosk-design-system-index.md)

---

## 1. 컨셉 요약

**신선한 food photography** 위에 **대담한 UI 레이어**를 얹는 2025–2026 QSR·헬시푸드 키오스크 트렌드입니다. Sweetgreen·Toss·현대 QSR 키오스크에서 보이는 **oversized CTA**, **subtle glassmorphism**, **vibrant accent**, **dark mode**를 ASAK에 맞게 재해석했습니다.

후보 A(안전한 크림+그린)와 C(웜 베이지)가 섞여 보인다는 피드백을 반영해, **따뜻한 중성색 배경을 쓰지 않고** 쿨 화이트·딥 포레스트 대비로 방향을 분리합니다. 후보 B가 이미 트렌디하지만 **미니멀·플랫**에 가깝다면, D는 **그라데이션 CTA·글래스 카드·코랄 포인트·다크 모드**로 한 단계 더 앞선 무드를 목표로 합니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | bold, vibrant, fresh-tech, photo-forward |
| UI 패턴 | `glass-photo-card` · gradient CTA · oversized type · dark mode toggle |
| 추천 SCR | 001 홈 · 003 메뉴 · 008 완료 · 012 결제 실패 |
| Figma Variables mode | `ds-candidate-d-trend-forward` |
| 벤치마크 무드 | Sweetgreen · Toss · modern QSR kiosk · Notion Trend-3/4 |

---

## 2. 색상 (Color)

### Light mode (기본)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | `#0F2E1F` | 헤더·강조 텍스트·다크 CTA (딥 포레스트) |
| `color-primary-dark` | `#081A12` | pressed·다크 모드 배경 |
| `color-accent-mint` | `#3DFFA8` | 일렉트릭 민트 · 선택·완료·그라데이션 시작 |
| `color-accent-coral` | `#FF6B4A` | 코랄 포인트 · 뱃지·프로모·마이크로 강조 |
| `color-accent-teal` | `#14B8A6` | 그라데이션 CTA 끝색 |
| `color-background` | `#F4F7F5` | 페이지 (쿨 화이트 — cream/beige 아님) |
| `color-surface` | `#FFFFFF` | 솔리드 카드 |
| `color-surface-glass` | `rgba(255,255,255,0.72)` | 글래스 패널·sticky bar |
| `color-text` | `#0A0F0D` | 본문 |
| `color-text-muted` | `#5C6B63` | 캡션 |
| `color-border` | `rgba(15,46,31,0.12)` | 구분선 |
| `color-success` | `#3DFFA8` | 완료 (mint) |
| `color-error` | `#FF4D4D` | 결제 실패 |
| `color-overlay` | `rgba(8,26,18,0.55)` | 모달 dim |

### Dark mode

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-background-dark` | `#121816` | 다크 페이지 배경 |
| `color-surface-dark` | `#1A2420` | 다크 카드 |
| `color-surface-glass-dark` | `rgba(26,36,32,0.75)` | 다크 글래스 |
| `color-text-dark` | `#F0FDF4` | 다크 본문 |
| `color-text-muted-dark` | `#94A89C` | 다크 캡션 |

### Gradient CTA

```css
linear-gradient(135deg, #3DFFA8 0%, #2EE59D 45%, #14B8A6 100%)
```

- 텍스트: `#081A12` (민트 위 고대비)
- Hover: brightness 1.05 · scale 0.98 press (micro-interaction)

---

## 3. 타이포그래피 (Typography)

**폰트**: Pretendard (한글·본문) + **Sora** (Display·CTA·숫자)

| 토큰 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|
| `type-display` | 44px | 800 | 1.08 | 홈·주문번호·히어로 |
| `type-h1` | 36px | 800 | 1.12 | 화면 제목 |
| `type-h2` | 26px | 700 | 1.2 | 섹션 |
| `type-body` | 17px | 500 | 1.5 | 본문 |
| `type-body-strong` | 17px | 700 | 1.5 | 가격·합계 |
| `type-caption` | 13px | 600 | 1.4 | 칼로리·뱃지 |
| `type-button` | 20px | 700 | 1 | CTA (oversized) |

- Letter-spacing: Display -0.02em · Button 0.01em
- 숫자·주문번호: Sora tabular nums

---

## 4. 간격·레이아웃 (Spacing & Layout)

| 토큰 | 값 | 용도 |
|------|-----|------|
| `space-1` | 4px | micro |
| `space-2` | 8px | chip |
| `space-3` | 16px | card padding |
| `space-4` | 24px | section |
| `space-5` | 32px | block |
| `space-6` | 48px | hero |
| `radius-sm` | 10px | chip |
| `radius-md` | 16px | button·glass card |
| `radius-lg` | 24px | photo-card |
| `radius-pill` | 999px | pill CTA variant |
| `blur-glass` | 16px | backdrop-filter |
| `shadow-glass` | `0 8px 32px rgba(15,46,31,0.08)` | elevation |
| `grid-columns` | 12 | margin 16 · gutter 16 |

---

## 5. 컴포넌트 (Components)

### Primary Button (Gradient)
- 높이 **60px** (oversized CTA) · full-width · radius `radius-md`
- 배경: `gradient-cta` · 텍스트 `#081A12`
- Pressed: scale 0.98 · shadow 축소 (micro-interaction 느낌)

### Secondary Button
- 높이 48px · `color-surface-glass` + blur · stroke `color-border` 1.5px

### Glass Photo Card (SCR-003)
- photo 68% · 하단 글래스 strip (`surface-glass` + blur)
- 품절: desaturate + `품절` coral outline 뱃지
- 선택: 2px `color-accent-mint` glow

### Option Row (SCR-004)
- row ≥52px · 선택 시 mint left bar 4px + glass bg
- 체크 28px · stroke `color-primary`

### Sticky Footer CTA
- `surface-glass` + blur · 상단 hairline border
- Primary gradient 버튼 60px

### Dark Mode Toggle (SCR-014 연계)
- pill switch · track `#1A2420` / thumb `color-accent-mint`
- 전역 토큰 `data-theme="dark"` 스왑

### Admin Table
- header `color-primary` · chart accent `color-accent-coral`

---

## 6. 샘플 화면 무드 (SCR-001 홈)

```
┌────────────────────────────┐  ← #F4F7F5 (light) / #121816 (dark)
│  [optional food hero blur] │
│                            │
│         ASAK               │  Sora 44px 800
│    Fresh. Bold. Now.       │  caption muted
│                            │
│   ┌──────────────────┐     │
│   │▓▓ 주문 시작하기 ▓▓│     │  mint→teal gradient 60px
│   └──────────────────┘     │
│  [🌙 다크] [접근성]         │  glass chips 44px
└────────────────────────────┘
```

- 히어로: food photo 30% height + gradient overlay (UI가 photo를 가리지 않음)
- 단일 oversized CTA · glass 보조 칩

---

## 7. A / B / C와의 차별

| 축 | A | B | C | **D** |
|----|---|---|---|-------|
| 배경 | cream `#FFFDF3` | cool gray | warm cream | **쿨 화이트** — beige 혼합 없음 |
| Primary | corporate green | charcoal | brown | **딥 포레스트** — 안전한 초록 아님 |
| Accent | lime+yellow | electric lime | terracotta | **민트+코랄+그라데이션** |
| CTA | flat green 56px | flat lime 52px | brown 56px | **gradient 60px** |
| Surface | solid white | flat white | warm shadow | **glass + blur** |
| Dark mode | ❌ | ❌ | ❌ | **✅** |
| Food photo | 강함 | 약함(미니멀) | 강함(웜) | **강함 + bold UI 오버레이** |
| 트렌드 | 안전·MVP | 미니멀 트렌디 | 따뜻·친근 | **2025–26 QSR forward** |

---

## 8. 장단점

| 장점 | 단점 |
|------|------|
| A/C “섞인·안전한” 톤 피드백에 **명확히 다른 방향** | 회의 Primary `#16A34A`와 색상 거리 |
| food photo + bold UI — **신선함과 트렌드 동시** | glass·gradient 구현·성능 테스트 필요 |
| dark mode · oversized CTA — **키오스크·Gen-Z 정합** | coral+mint 동시 사용 시 과하면 산만 |
| Sweetgreen·Toss·QSR 벤치마크 무드 | Admin Courses kit 톤 맞춤 작업 필요 |

---

## 9. Notion hub 정합 노트

| hub 항목 | 후보 D 반영 |
|----------|-------------|
| 지양: 촌스러운 초록 | ✅ corporate green 미사용 — 딥 포레스트+네온 민트 |
| 지양: 과한 자연풍 | ✅ photo는 UI 아래, 일러스트·나뭇잎 장식 없음 |
| Trend-3 Electric Lime | ✅ mint accent · B보다 채도·그라데이션 강화 |
| Trend-4 photo-first | ✅ glass photo-card |
| UX: 단순 고객 화면 | ✅ single CTA · 큰 타이포 |
| 회의 Cream `#FFFDF3` | ❌ cool white — 팀 합의 필요 |
| Moja UI | dark mode Variables·toggle 구조 참고 |

---

## 관련 파일

- CSS 토큰: [kiosk-tokens-candidate-D.css](./kiosk-tokens-candidate-D.css)
- 비교표: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md)
- Figma 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md)
