# 키오스크 디자인 시스템 — 후보 A: Fresh Greens

> **(Figma: DS-01 Fresh Greens)**

> **컨셉**: 샐러드·신선함 · 그린 primary · 밝은 배경  
> **캔버스**: 834×1194 (태블릿 세로) · 터치 최소 **44×44px** (팀 safe area: 상하 24 / 좌우 16)  
> **정본 참조**: [Notion — 브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [디자인 & 화면 hub](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc)

---

## 1. 컨셉 요약

회의 확정 팔레트(`#16A34A` · Cream `#FFFDF3`)를 축으로, 샐러디·프레시 키오스크의 **신선·건강·친근** 무드를 직접 반영합니다. photo-first 메뉴 카드와 밝은 크림 배경이 ASAK 브랜드(아삭·건강메이트)와 가장 가깝습니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | fresh, crisp, healthy, approachable |
| UI 패턴 | `photo-card` · `option-list` · sticky CTA |
| 추천 SCR | 001 홈 · 003 메뉴 · 004 옵션 · 008 완료 |
| Figma Variables mode | `ds-candidate-a-fresh-greens` |

---

## 2. 색상 (Color)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | `#16A34A` | CTA·활성 탭·주요 버튼 (회의 Primary) |
| `color-primary-dark` | `#15803D` | pressed·hover·강조 텍스트 |
| `color-primary-light` | `#DCFCE7` | 선택 row·칩 배경 |
| `color-secondary` | `#E8F5E9` | 카드 보조·섹션 구분 |
| `color-accent-lime` | `#A3E635` | 완료 아이콘·뱃지 (회의 Lime) |
| `color-accent-yellow` | `#FACC15` | 선택 카드 포인트 (SCR-002) |
| `color-background` | `#FFFDF3` | 페이지 배경 (회의 Cream) |
| `color-surface` | `#FFFFFF` | 카드·모달 |
| `color-text` | `#1F2937` | 본문 (회의 Text) |
| `color-text-muted` | `#6B7280` | 보조·캡션 |
| `color-border` | `#D1E7D4` | 구분선·카드 stroke |
| `color-success` | `#22C55E` | 주문 완료·판매 중 |
| `color-error` | `#EF4444` | 결제 실패·품절 강조 |
| `color-overlay` | `rgba(31,41,55,0.45)` | 타임아웃·모달 dim |

---

## 3. 타이포그래피 (Typography)

**폰트**: Pretendard (한글·영문 단일) · fallback: Apple SD Gothic Neo, Malgun Gothic

| 토큰 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|
| `type-display` | 36px | 700 | 1.2 | 홈 브랜드·완료 화면 |
| `type-h1` | 32px | 700 | 1.25 | 화면 제목 |
| `type-h2` | 24px | 600 | 1.3 | 섹션·옵션 그룹 |
| `type-body` | 18px | 400 | 1.5 | 본문·메뉴명 |
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
| `space-7` | 48px | thumb zone 여백 |
| `radius-sm` | 8px | 칩·뱃지 |
| `radius-md` | 12px | 카드·버튼 |
| `radius-lg` | 16px | photo-card |
| `grid-columns` | 12 | margin 16 · gutter 16 |

---

## 5. 컴포넌트 (Components)

### Primary Button
- 높이 **56px** (≥44px 터치) · full-width 또는 min-width 200px
- 배경 `color-primary` · 텍스트 `#FFFFFF` · radius `radius-md`
- Pressed: `color-primary-dark` · Disabled: `#9CA3AF` 40% opacity

### Secondary Button
- 높이 48px · 배경 `color-surface` · stroke `color-border` 1.5px

### Photo Card (SCR-003)
- 2열 그리드 · 카드 min-height 160px · 상단 16:9 photo 60~70%
- 품절: grayscale overlay + `품절` 뱃지 `color-text-muted`

### Option Row (SCR-004)
- row 높이 ≥48px · 라디오/체크 24px · 그룹 헤더 `type-h2`

### Sticky Footer CTA
- 하단 고정 · padding 16px · shadow `0 -4px 16px rgba(0,0,0,0.06)`

### Admin Table (SCR-009~011)
- Courses kit surface `#FFFFFF` + header `color-primary-dark` · row ≥48px

---

## 6. 샘플 화면 무드 (SCR-001 홈)

```
┌────────────────────────────┐  ← background #FFFDF3
│         [ASAK]             │
│    아삭하게, 건강하게        │  type-h2 #1F2937
│                            │
│   ┌──────────────────┐     │
│   │  주문 시작하기     │     │  #16A34A · 56px
│   └──────────────────┘     │
│  [접근성 ⚙]                 │  44×44
└────────────────────────────┘
```

- 히어로 사진 optional · 과한 자연풍 지양 (hub SCR 가이드)
- 단일 CTA · 스크롤 없음

---

## 7. 장단점

| 장점 | 단점 |
|------|------|
| 회의 확정 팔레트와 **1:1 정합** — 팀 설득 비용 최소 | green-heavy → **촌스러운 초록** 인상 위험 (hub 지양 항목) |
| 샐러드·볼 브랜드와 즉시 연상 | 경쟁 프랜차이즈(샐러디)와 시각적 유사도 |
| photo-first 메뉴와 조화 우수 | Admin 화면은 별도 Courses kit 톤 보강 필요 |
| Trend-4 대비 브랜드 메시지(건강·신선) 직관적 | Gen-Z bold 톤(Trend-3) 대비 덜 트렌디할 수 있음 |

---

## 8. Notion hub 정합 노트

| hub 항목 | 후보 A 반영 |
|----------|-------------|
| 회의 팔레트 Primary `#16A34A` | ✅ 직접 사용 |
| 지양: 촌스러운 초록 | ⚠️ lime/yellow 포인트로 완화 필요 |
| UX: photo-first · 3단 옵션 | ✅ `photo-card` + `option-list` |
| Trend 매핑 | Option A Salady + 회의 green · Trend-1 sage 보조 가능 |
| Community | [Kiosk Prototype](https://www.figma.com/community/file/784444951689918956/kiosk-prototype) flow 참고 |
| Moja UI | Variables·dark mode 구조만 참고 (색상 복제 X) |

---

## 관련 파일

- CSS 토큰: [kiosk-tokens-candidate-A.css](./kiosk-tokens-candidate-A.css)
- 비교표: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md)
- Figma 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md)
