# ASAK 0718 화면 조합 맵

**목표:** 0718에 “잘 조합해서” 남기기. 전부 고치지 않고 **정본 소스 + Keep 세트**만 유지.

## 소스 역할

| 소스 | fileKey | 쓰는 것 |
|---|---|---|
| **0714** | `VXKyzoNdsgM4oN57mrECxb` | 키오스크 **레이아웃·간격 정본** (17화면) |
| **0715 Archive** | `JSrjOy668zhfkiLplCkreh` → `525:19725` | 관리자 **화면 정본** (68) |
| **0718** | `yHhvn5RKjBd91U8BJUQz7F` | 쓰기 타깃. 토큰·Master는 여기. 화면은 정리·정렬 |

## 키오스크 Keep (코드용 Core)

0714 17장과 1:1 + 코드에 꼭 필요한 상태만.

| SCR | Keep (0718 id 또는 이름) | 레이아웃 정본 | 비고 |
|---|---|---|---|
| 001 | Default, High Contrast | 0714 `2:4696` | CTA y≈890 |
| 003 | Default, Empty, Loading, Sold-out, Error | 0714 `2:4704` | row-1/2/3 |
| 004 | Default, Loading, Error, Option Selected, Menu Sold-out | 0714 `2:4775` | Edit*는 QA 섹션 |
| 005 | Default, Empty, Delete Confirm, Sold-out* | 0714 `2:4791` | |
| 007 | Collapsed, Expanded, Processing, Loading, Method Selected, All Disabled, Network Error | 0714 계열 | |
| 008 | Default **1개만** | 0714 `2:4877` | 중복 제거 |
| 012 | Declined, Network, Retry Loading | 0714 | |
| 013 | Expired, Warning, Continue | 0714 | |
| 014 | Default, High Contrast, Reverted | 0714 | |

나머지는 `ARCHIVED_` 접두 또는 **QA States** 섹션으로 이동.

## 관리자 Keep

0718 `06-C`에 섹션 분리 완료: `✅ KEEP — Admin Code Core` (35) / `📦 QA States` (37).

| SCR | 0715 Archive Default (복사 소스) | layoutMode | 0718 유지 |
|---|---|---|---|
| SCR-009 Live Order | `525:19726` | NONE | Dirty/Save·토큰 |
| SCR-010 Order Detail | `525:19749` | NONE | Dirty/Save·토큰 |
| SCR-011 Sold-out | `525:20767` | NONE | StickyActionBar |
| SCR-015 Login | `525:20937` | NONE | 토큰 |
| SCR-016 Menu Mgmt | `525:21041` | HORIZONTAL | StickyActionBar |
| SCR-018 Payment | `525:20397` | HORIZONTAL | 토큰 |
| SCR-019 Sales Summary | `525:19780` | HORIZONTAL | 토큰 |
| SCR-020 Monthly | `525:19970` | HORIZONTAL | 토큰 |
| SCR-021 Daily | `525:20163` | HORIZONTAL | 토큰 |
| SCR-022 Dashboard | `525:21941` | NONE | 토큰 |

수동 복붙: 0715 Archive → 0718 Admin KEEP → **0718 로컬 Semantic만** 재바인딩 (AI bulk 금지).

## 조합 원칙

1. **레이아웃/줄맞춤** = 0714(키오스크) · 0715 Archive(관리자)
2. **색/토큰** = 0718 로컬 Semantic (이미 복구분)
3. **Master 인스턴스** = 0718 `02-C~04-C`
4. AL은 화면 루트를 억지로 바꾸지 말고 **Header / Content / Bottom** 구역만
