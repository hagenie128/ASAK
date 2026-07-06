# 키오스크 디자인 시스템 — 후보 E: Fresh Warm Trend (A+C 트렌디)

> **(Figma: DS-04 A+C Trendy)**

> **컨셉**: A 신선함 + C 따뜻함 + 트렌디 실행 · Sweetgreen × 웜 카페  
> **캔버스**: 834×1194 (태블릿 세로) · 터치 최소 **44×44px** (팀 safe area: 상하 24 / 좌우 16)  
> **정본 참조**: [Notion — 브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [디자인 & 화면 hub](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc)

---

## 1. 컨셉 요약

후보 **A(Fresh Greens)** 의 신선·건강 신뢰와 **C(Warm Bistro)** 의 따뜻·친근 무드를 **단순 혼합이 아닌 트렌디 레이어**로 재조합합니다. 회의 green `#16A34A`를 그대로 쓰지 않고 **sage·forest** 톤으로 세련화하고, C의 terracotta를 **에너지 액센트**로 끌어옵니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | fresh, warm, instagrammable, approachable, modern |
| UI 패턴 | oversized `photo-card` · gradient CTA · soft shadow · bold menu type |
| 벤치마크 무드 | Sweetgreen · CAVA · 웜 브런치 카페 키오스크 |
| 추천 SCR | 001 홈 · 003 메뉴 · 004 옵션 · 008 완료 |
| Figma Variables mode | `ds-candidate-e-fresh-warm-trend` |

### A+C DNA vs 지루한 혼합

| 출처 | 가져오는 것 | E에서의 실행 |
|------|-------------|--------------|
| **A** | 신선 green 정체성 · photo-first · 밝은 여백 | corporate `#16A34A` 대신 **sage `#3D8B5F` / forest `#2D6A4F`** |
| **C** | 웜 크림·베이지 언더톤 · terracotta 포인트 · 둥근 카드 | 배경 `#FAF7F2` · accent `#E07A5F` · **radius 24px** 카드 |
| **트렌디** | — | CTA **sage→forest 그라데이션** · **Display 40px** 메뉴명 · soft elevation · 인스타그램mable 볼 aesthetic |

> **지양**: A 크림 + C 베이지를 50:50로 섞은 **안전한 카페 톤** · flat corporate green 버튼 · 작은 radius 카드

---

## 2. 색상 (Color)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | `#3D8B5F` | CTA·활성 탭·주요 버튼 (sage green) |
| `color-primary-dark` | `#2D6A4F` | pressed·그라데이션 끝·강조 텍스트 |
| `color-primary-light` | `#D4E8DC` | 선택 row·칩 배경 |
| `color-secondary` | `#EDE6DB` | 카드 보조·섹션 (warm neutral) |
| `color-accent` | `#E07A5F` | terracotta · 뱃지·할인·포인트 |
| `color-accent-soft` | `#F4A261` | hover·warm coral 보조 |
| `color-background` | `#FAF7F2` | 페이지 (warm off-white) |
| `color-surface` | `#FFFFFF` | 카드·모달 |
| `color-surface-warm` | `#F5F0E8` | sticky bar·히어로 strip |
| `color-text` | `#2C2C2C` | 본문 (warm charcoal) |
| `color-text-muted` | `#6B6560` | 보조·캡션 |
| `color-border` | `#E5DDD3` | 구분선·카드 stroke |
| `color-success` | `#40916C` | 주문 완료 |
| `color-error` | `#D64545` | 결제 실패·품절 |
| `color-overlay` | `rgba(44,44,44,0.42)` | 타임아웃·모달 dim |
| `gradient-cta` | `#3D8B5F` → `#2D6A4F` | Primary 버튼 (135deg) |

---

## 3. 타이포그래피 (Typography)

**폰트**: Pretendard (한글·영문) + **Fraunces** 또는 **DM Sans** (Display·메뉴명·가격)

| 토큰 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|
| `type-display` | 40px | 700 | 1.15 | 홈 브랜드·완료 화면 |
| `type-menu` | 22px | 700 | 1.25 | **메뉴명 bold display** (SCR-003) |
| `type-h1` | 32px | 700 | 1.25 | 화면 제목 |
| `type-h2` | 24px | 600 | 1.3 | 섹션·옵션 그룹 |
| `type-body` | 18px | 400 | 1.5 | 본문 |
| `type-body-strong` | 18px | 600 | 1.5 | 가격·합계 |
| `type-caption` | 14px | 500 | 1.4 | 칼로리·안내 |
| `type-button` | 20px | 600 | 1 | CTA 라벨 |

---

## 4. 간격·레이아웃 (Spacing & Layout)

| 토큰 | 값 | 용도 |
|------|-----|------|
| `space-1` | 4px | 아이콘 gap |
| `space-2` | 8px | 칩 내부 |
| `space-3` | 12px | 리스트 row gap |
| `space-4` | 16px | 카드 padding·grid gutter |
| `space-5` | 24px | safe area 상하 |
| `space-6` | 32px | 섹션 간격 |
| `space-7` | 48px | thumb zone·hero 여백 |
| `radius-sm` | 12px | 칩·뱃지 |
| `radius-md` | 16px | 버튼 |
| `radius-lg` | **24px** | **oversized photo-card** |
| `radius-xl` | 32px | 홈 히어로·모달 |
| `shadow-card` | `0 8px 32px rgba(44,44,44,0.08)` | soft elevation |
| `shadow-button` | `0 4px 16px rgba(45,106,79,0.25)` | gradient CTA glow |
| `grid-columns` | 12 | margin 16 · gutter 16 |

---

## 5. 컴포넌트 (Components)

### Primary Button (Gradient CTA)
- 높이 **56px** · full-width · radius `radius-md`
- 배경 `linear-gradient(135deg, #3D8B5F 0%, #2D6A4F 100%)`
- 텍스트 `#FFFFFF` · shadow `shadow-button`
- Pressed: gradient 끝 `#1B4332` · Disabled: `#9CA3AF` 40%

### Secondary Button
- 높이 48px · 배경 `color-surface` · stroke `color-border` 1.5px · radius `radius-md`

### Photo Card (SCR-003) — Oversized
- 2열 그리드 · **radius `radius-lg` (24px)** · shadow-card
- photo 65~70% · 메뉴명 `type-menu` bold
- **NEW** 뱃지: `color-accent` terracotta pill
- 품절: warm overlay `rgba(250,247,242,0.7)` + muted label

### Option Chip (SCR-004)
- pill height 44px · bg `color-secondary` · selected: `color-primary-light` + stroke `color-primary`

### Sticky Footer CTA
- bg `color-surface-warm` · 상단 shadow `0 -8px 24px rgba(44,44,44,0.06)`
- 내부 Primary = gradient CTA

### Admin Table (SCR-009~011)
- Courses kit + header `color-primary-dark` · chart accent `color-accent`

---

## 6. 샘플 화면 무드 (SCR-001 홈)

```
┌────────────────────────────┐  ← background #FAF7F2
│         [ASAK]             │
│    아삭하게, 건강하게        │  type-display #2C2C2C
│                            │
│   ┌──────────────────┐     │  optional: soft bowl hero
│   │  (warm photo)    │     │  radius-xl · shadow-card
│   └──────────────────┘     │
│   ┌──────────────────┐     │
│   │  주문 시작하기     │     │  sage→forest gradient · 56px
│   └──────────────────┘     │
│  [접근성 ⚙]                 │  44×44 · terracotta dot optional
└────────────────────────────┘
```

- 단일 CTA · 스크롤 없음 · hero는 **웜톤 food photo** (C) + **밝은 여백** (A)
- terracotta는 CTA가 아닌 **미세 포인트** (뱃지·아이콘)로만 사용

---

## 7. 장단점

| 장점 | 단점 |
|------|------|
| A+C 요구에 **트렌디 차별화** — 지루한 green+beige 회피 | Display 폰트·그라데이션 → 구현·Figma Variables 작업량 ↑ |
| 신선(sage) + 따뜻함(terra) **동시 전달** | terracotta 과용 시 C만큼 브런치 카페 연상 |
| photo-first·인스타그램mable — Gen-Z·SNS 친화 | 회의 `#16A34A`와 hue 거리 → 팔레트 설득 필요 |
| oversized card·soft shadow — 2024~26 food app 트렌드 | Admin은 Courses kit 톤 별도 정리 |

---

## 8. Notion hub 정합 노트

| hub 항목 | 후보 E 반영 |
|----------|-------------|
| 회의 Primary `#16A34A` | ⚠️ sage/forest로 **트렌디 재해석** (hue 유지, 채도·명도 조정) |
| 지양: 촌스러운 초록 | ✅ corporate flat green 회피 |
| 지양: 과한 자연풍 | ⚠️ hero photo 톤·비율 제한 |
| Trend-1 sage + Trend-2 coral | ✅ A+C 트렌디 하이브리드 |
| UX: photo-first · 3단 옵션 | ✅ oversized photo-card + option chip |
| vs 단순 A+C 혼합 | gradient CTA · bold menu type · radius 24px로 **실행 차별** |

---

## 관련 파일

- CSS 토큰: [kiosk-tokens-candidate-E.css](./kiosk-tokens-candidate-E.css)
- 비교표: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md)
- Figma 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md) → `DS-04 A+C Trendy`
