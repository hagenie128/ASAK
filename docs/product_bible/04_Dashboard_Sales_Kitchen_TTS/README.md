# Pack 04 — Dashboard / Sales / Kitchen / TTS

> **허브:** [product-bible-hub.md](../product-bible-hub.md) · 관리자 SCR-009~022

## 운영 흐름

```text
Dashboard → Kitchen/Live Order → 주문 완료 → TTS → Sales 집계
```

## 문서 목록

### Dashboard
| 문서 | 내용 |
|---|---|
| [Dashboard Architecture](docs/09-features/dashboard/DASHBOARD_ARCHITECTURE.md) | 구조 |
| [Dashboard Decisions & QA](docs/09-features/dashboard/DASHBOARD_DECISIONS_AND_QA.md) | 결정·QA |

### Kitchen / Live Order
| 문서 | 내용 |
|---|---|
| [Kitchen Architecture](docs/09-features/kitchen/KITCHEN_ARCHITECTURE.md) | 구조 |
| [Kitchen Flow & Edge Case](docs/09-features/kitchen/KITCHEN_FLOW_AND_EDGE_CASE.md) | 흐름·예외 |

### Sales
| 문서 | 내용 |
|---|---|
| [Sales Architecture](docs/09-features/sales/SALES_ARCHITECTURE.md) | 구조 |
| [Sales API Contract](docs/09-features/sales/SALES_API_CONTRACT.md) | API |
| [Sales Data Integrity & QA](docs/09-features/sales/SALES_DATA_INTEGRITY_AND_QA.md) | 정합성·QA |

### TTS (MVP 이후 가능)
| 문서 | 내용 |
|---|---|
| [TTS Architecture](docs/09-features/tts/TTS_ARCHITECTURE.md) | 구조 |
| [TTS Implementation Guide](docs/09-features/tts/TTS_IMPLEMENTATION_GUIDE.md) | 구현 가이드 |
| [TTS Edge Cases & QA](docs/09-features/tts/TTS_EDGE_CASE_AND_QA.md) | 예외·QA |

## 연결 화면

[SCR-009 Live Order](../07_Screen_Bible/docs/07-screens/SCR-009-ADMIN-LIVE-ORDER-BOARD.md) · [SCR-019~021 Sales](../07_Screen_Bible/docs/07-screens/SCR-019-ADMIN-SALES-SUMMARY.md) · [SCR-022 Dashboard](../07_Screen_Bible/docs/07-screens/SCR-022-ADMIN-DASHBOARD.md)
