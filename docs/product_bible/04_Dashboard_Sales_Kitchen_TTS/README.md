# 04_Dashboard_Sales_Kitchen_TTS

> Status: `Canonical Pack`
> Updated: `2026-08-14`
> Pack 경계는 유지하고, 반복 문서는 도메인별 통합 문서로 줄였습니다.

## 현재 문서

- [DASHBOARD_BIBLE.md](DASHBOARD_BIBLE.md)
- [KITCHEN_BIBLE.md](KITCHEN_BIBLE.md)
- [SALES_BIBLE.md](SALES_BIBLE.md)
- [TTS_BIBLE.md](TTS_BIBLE.md)

## 이전 Pack 안내

### Pack 04 — Dashboard / Sales / Kitchen / TTS

> **허브:** [product-bible-hub.md](../product-bible-hub.md) · 관리자 SCR-009~022

#### 운영 흐름

```text
Dashboard → Kitchen/Live Order → 주문 완료 → TTS → Sales 집계
```

#### 문서 목록

##### Dashboard
| 문서 | 내용 |
|---|---|
| [Dashboard Architecture](DASHBOARD_BIBLE.md) | 구조 |
| [Dashboard Decisions & QA](DASHBOARD_BIBLE.md) | 결정·QA |

##### Kitchen / Live Order
| 문서 | 내용 |
|---|---|
| [Kitchen Architecture](KITCHEN_BIBLE.md) | 구조 |
| [Kitchen Flow & Edge Case](KITCHEN_BIBLE.md) | 흐름·예외 |

##### Sales
| 문서 | 내용 |
|---|---|
| [Sales Architecture](SALES_BIBLE.md) | 구조 |
| [Sales API Contract](SALES_BIBLE.md) | API |
| [Sales Data Integrity & QA](SALES_BIBLE.md) | 정합성·QA |

##### TTS (MVP 이후 가능)
| 문서 | 내용 |
|---|---|
| [TTS Architecture](TTS_BIBLE.md) | 구조 |
| [TTS Implementation Guide](TTS_BIBLE.md) | 구현 가이드 |
| [TTS Edge Cases & QA](TTS_BIBLE.md) | 예외·QA |

#### 연결 화면

[SCR-009 Live Order](../07_Screen_Bible/SCR-009-ADMIN-LIVE-ORDER-BOARD.md) · [SCR-019~021 Sales](../07_Screen_Bible/SCR-019-ADMIN-SALES-SUMMARY.md) · [SCR-022 Dashboard](../07_Screen_Bible/SCR-022-ADMIN-DASHBOARD.md)
