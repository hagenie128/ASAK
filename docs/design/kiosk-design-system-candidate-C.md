# 키오스크 디자인 시스템 — 후보 C: Warm Bistro

> **팀 결정으로 후보 목록에서 제외 (Trend-2/C warm bistro 참고용 보관)**

> **컨셉**: 따뜻한 톤 · 베이지/브라운 · 친근한 키오스크  
> **캔버스**: 834×1194 (태블릿 세로) · 터치 최소 **44×44px**  
> **정본 참조**: [Notion — 브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [인덱스](./kiosk-design-system-index.md)

---

## 1. 컨셉 요약

테라코타·크림·웜 브라운으로 **식욕·친근·편안함**을 전달하는 키오스크 무드입니다. Notion **Trend-2 Warm Coral + Cream** 및 프레퍼스·알라보 벤치마크를 ASAK 오리지널 hex로 재해석했습니다. green primary 없이도 건강·프레시 이미지는 **food photography**로 보완합니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | warm, cozy, appetite, friendly |
| UI 패턴 | `photo-card` hero · rounded card · soft shadow |
| 추천 SCR | 001 홈(hero optional) · 003 메뉴 · 005 장바구니 |
| Figma Variables mode | `ds-candidate-c-warm-bistro` |

---

## 2. 색상 (Color)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | `#8B5A3C` | CTA·헤더·강조 (warm brown) |
| `color-primary-dark` | `#6B4428` | pressed·footer |
| `color-primary-light` | `#C49A6C` | 보조 링크 |
| `color-secondary` | `#F5E6D3` | 카드·선택 배경 (beige) |
| `color-accent` | `#C45C3E` | terracotta 포인트·뱃지 |
| `color-accent-soft` | `#E8A87C` | hover·칩 |
| `color-background` | `#FFFBF5` | 페이지 (warm cream) |
| `color-surface` | `#FFFFFF` | 카드 |
| `color-surface-warm` | `#FFF5E8` | sticky bar·섹션 |
| `color-text` | `#3D2C29` | 본문 |
| `color-text-muted` | `#7A655C` | 캡션 |
| `color-border` | `#E8D5C4` | 구분선 |
| `color-success` | `#5A8F5A` | 완료 (muted sage) |
| `color-error` | `#C45C3E` | 에러 (accent 재사용, 톤 유지) |
| `color-overlay` | `rgba(61,44,41,0.4)` | 모달 |

---

## 3. 타이포그래피 (Typography)

**폰트**: Pretendard (한글) + **DM Sans** (영문·숫자·가격)

| 토큰 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|
| `type-display` | 34px | 700 | 1.2 | 홈 슬로건 |
| `type-h1` | 30px | 700 | 1.25 | 화면 제목 |
| `type-h2` | 22px | 600 | 1.3 | 섹션 |
| `type-body` | 17px | 400 | 1.55 | 본문 |
| `type-body-strong` | 17px | 600 | 1.55 | 메뉴명·가격 |
| `type-caption` | 13px | 400 | 1.4 | 칼로리 |
| `type-button` | 18px | 600 | 1 | CTA |

---

## 4. 간격·레이아웃 (Spacing & Layout)

| 토큰 | 값 | 용도 |
|------|-----|------|
| `space-1` | 4px | micro |
| `space-2` | 8px | chip |
| `space-3` | 12px | list |
| `space-4` | 16px | card padding |
| `space-5` | 24px | safe area |
| `space-6` | 32px | section |
| `space-7` | 40px | hero margin |
| `radius-sm` | 10px | chip |
| `radius-md` | 14px | button |
| `radius-lg` | 20px | photo-card |
| `shadow-card` | `0 4px 20px rgba(61,44,41,0.08)` | 카드 elevation |
| `grid-columns` | 12 | margin 16 · gutter 16 |

---

## 5. 컴포넌트 (Components)

### Primary Button
- 높이 **56px** · 배경 `color-primary` · radius `radius-md`
- shadow `0 2px 8px rgba(107,68,40,0.2)` · pressed: `color-primary-dark`

### Selection Card (SCR-002)
- 높이 ≥64px · 배경 `color-surface-warm` · 선택 시 stroke `color-accent` 2px
- 아이콘 + 라벨 중앙 정렬

### Photo Card (SCR-003)
- radius `radius-lg` · shadow-card · photo 65% · 하단 beige strip
- 버거킹형 풀블리드 + **따뜻한 프레임** (hub `photo-card`)

### Option Chip (SCR-004)
- pill height 40px · bg `color-secondary` · selected `color-accent-soft`

### Sticky Cart Bar
- bg `color-surface-warm` · 상단 border `color-border`

### Admin
- Courses kit layout + warm header `color-primary-dark` · chart accent `color-accent`

---

## 6. 샘플 화면 무드 (SCR-003 메뉴)

```
┌────────────────────────────┐  ← #FFFBF5
│ ←  샐러드 · 볼 · 랩          │
├────────────────────────────┤
│ ┌──────────┐ ┌──────────┐  │
│ │  [photo] │ │  [photo] │  │  radius 20px
│ │ 그린볼    │ │ 치킨랩    │  │
│ │ ₩9,500   │ │ ₩8,900   │  │
│ └──────────┘ └──────────┘  │
├────────────────────────────┤
│ 🛒 장바구니 (2)              │  #FFF5E8 bar
└────────────────────────────┘
```

---

## 7. 장단점

| 장점 | 단점 |
|------|------|
| **친근·건강메이트** 톤에 최적 — hub 브랜드 가치 정합 | 회의 Primary green과 색상 거리 |
| food photo와 **식욕 자극** 시너지 (Trend-2) | 과하면 **자연풍·고급 웅장** 느낌 (hub 지양) |
| 포장·먹고가기 선택 카드 UX에 적합 | 신선(salad)보다 **브런치·베이커리** 연상 가능 |
| green-heavy 피하면서도 따뜻함 유지 | Admin 대시보드와 톤 통일 작업 필요 |

---

## 8. Notion hub 정합 노트

| hub 항목 | 후보 C 반영 |
|----------|-------------|
| 지양: 과한 자연풍 | ⚠️ hero photo 비율·톤 제한 필요 |
| Trend-2 Warm Coral | ✅ hex 기반 재해석 |
| 벤치마크: 프레퍼스·알라보 | mood only · hex 독자 설계 |
| UX: photo-first | ✅ `photo-card` 60~70% |
| 회의: 친근·편의성 | ✅ copy tone과 궁합 |
| SCR-002 | warm selection card (yellow 대신 terracotta) |

---

## 관련 파일

- CSS 토큰: [kiosk-tokens-candidate-C.css](./kiosk-tokens-candidate-C.css)
- 비교표: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md)
- Figma 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md)
