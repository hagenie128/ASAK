# 키오스크 디자인 시스템 — 후보 B: Modern Minimal

> **(Figma: DS-02 Modern Minimal)**

> **컨셉**: 흑백 + 포인트 · 큰 타이포 · 미니멀  
> **캔버스**: 834×1194 (태블릿 세로) · 터치 최소 **44×44px**  
> **정본 참조**: [Notion — 브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [디자인 & 화면 hub](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) · [인덱스](./kiosk-design-system-index.md)

---

## 1. 컨셉 요약

차콜·화이트 기반에 **일렉트릭 라임** 한 점만 포인트로 쓰는 Gen-Z 키오스크 무드입니다. Notion **Trend-3 Electric Lime + Charcoal**을 후보 B의 기반으로 재해석했으며, green monotony(초록 단조)를 탈피합니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | bold, clean, high-contrast, fast |
| UI 패턴 | `hero-detail` · 대형 타이포 CTA · flat card |
| 추천 SCR | 001 홈 · 008 완료 · 012 결제 실패 |
| Figma Variables mode | `ds-candidate-b-modern-minimal` |

---

## 2. 색상 (Color)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | `#1A1C20` | CTA·헤더·주요 텍스트 |
| `color-primary-light` | `#4A4E57` | 보조 버튼·아이콘 |
| `color-accent` | `#C8F135` | 포인트 CTA·선택 상태·완료 아이콘 |
| `color-accent-muted` | `#E8F5A0` | 선택 row 배경 |
| `color-background` | `#F0F1ED` | 페이지 배경 |
| `color-surface` | `#FFFFFF` | 카드·패널 |
| `color-surface-elevated` | `#FAFAFA` | sticky bar |
| `color-text` | `#1A1C20` | 본문 |
| `color-text-inverse` | `#FFFFFF` | 다크 버튼 위 |
| `color-text-muted` | `#6B7280` | 캡션 |
| `color-border` | `#E5E7EB` | 1px 구분선 |
| `color-border-strong` | `#1A1C20` | 포커스 링·강조 stroke |
| `color-success` | `#C8F135` | 완료 (accent 재사용) |
| `color-error` | `#DC2626` | 에러 아이콘만 (과한 경고 지양) |
| `color-overlay` | `rgba(26,28,32,0.55)` | 모달 |

---

## 3. 타이포그래피 (Typography)

**폰트**: Pretendard (본문) + **Space Grotesk** (Display·숫자·주문번호)

| 토큰 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|
| `type-display` | 40px | 800 | 1.1 | 홈·주문번호 |
| `type-h1` | 34px | 800 | 1.15 | 화면 제목 |
| `type-h2` | 24px | 700 | 1.25 | 섹션 |
| `type-body` | 16px | 500 | 1.5 | 본문 |
| `type-body-strong` | 16px | 700 | 1.5 | 가격 |
| `type-caption` | 12px | 600 | 1.4 | 라벨·뱃지 |
| `type-button` | 18px | 700 | 1 | CTA (대문자 optional) |

---

## 4. 간격·레이아웃 (Spacing & Layout)

| 토큰 | 값 | 용도 |
|------|-----|------|
| `space-1` | 4px | micro |
| `space-2` | 8px | inline |
| `space-3` | 16px | card padding |
| `space-4` | 24px | section |
| `space-5` | 32px | block |
| `space-6` | 48px | display 여백 |
| `radius-sm` | 4px | 미니멀 칩 |
| `radius-md` | 8px | 버튼·카드 |
| `radius-lg` | 0px | 풀블리드 photo (선택) |
| `grid-columns` | 12 | margin 16 · gutter 16 |

---

## 5. 컴포넌트 (Components)

### Primary Button
- 높이 **52px** · 배경 `color-primary` · 텍스트 inverse
- Accent variant: 배경 `color-accent` · 텍스트 `color-primary` (홈 CTA)

### Ghost Button
- 높이 44px · 투명 · `color-border-strong` 2px stroke

### Photo Card (SCR-003)
- border 없음 · photo 100% width · 이름 `type-body-strong` only
- 품절: `color-text-muted` + line-through

### Option Row (SCR-004)
- flat list · 선택 시 좌측 4px `color-accent` bar
- 체크박스 28px square · stroke `color-border-strong`

### Segmented Control (SCR-014 접근성)
- Moja UI 패턴 참고 · pill 44px height

### Admin Table
- header `color-primary` · row zebra `#FAFAFA` / `#FFFFFF`

---

## 6. 샘플 화면 무드 (SCR-001 홈)

```
┌────────────────────────────┐  ← #F0F1ED
│                            │
│         ASAK               │  Space Grotesk 40px 800
│                            │
│   ┌──────────────────┐     │
│   │  주문 시작하기     │     │  #C8F135 bg · #1A1C20 text
│   └──────────────────┘     │
│                            │
└────────────────────────────┘
```

- 로고·슬로건 최소 · 여백 극대화
- 히어로 사진 생략 권장 (미니멀 유지)

---

## 7. 장단점

| 장점 | 단점 |
|------|------|
| **green monotony 탈피** — hub Trend-3 정합 | 회의 Primary green(`#16A34A`)과 거리 있음 |
| 큰 타이포·고대비 → 키오스크 **가독성·속도** 우수 | 따뜻함·친근(건강메이트) 톤은 약할 수 있음 |
| photo 메뉴에서 food가 **주인공** (UI는 배경) | 라임 accent가 과하면 유치해 보일 수 있음 |
| 완료·에러 상태 명확 (SCR-008·012) | Admin은 Courses kit 보라 톤과 이질감 |

---

## 8. Notion hub 정합 노트

| hub 항목 | 후보 B 반영 |
|----------|-------------|
| 지양: 촌스러운 초록 | ✅ primary 비-green |
| Trend-3 Electric Lime | ✅ 직접 기반 |
| UX: 단순 고객 화면 | ✅ 미니멀 레이아웃 |
| 회의 Cream `#FFFDF3` | ❌ cool gray bg — 팀 합의 필요 |
| SCR-012 결제 실패 | Trend-3 lime accent on error only (SCR 가이드) |
| Moja UI | toggle·segmented·Variables 구조 참고 |
| Community | [Kiosk UI/UX Case Study](https://www.figma.com/community/file/1497969269675579774/kiosk-ui-ux-case-study) 세로 UX |

---

## 관련 파일

- CSS 토큰: [kiosk-tokens-candidate-B.css](./kiosk-tokens-candidate-B.css)
- 비교표: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md)
- Figma 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md)
