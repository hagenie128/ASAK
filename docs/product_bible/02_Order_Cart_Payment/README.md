# Pack 02 — Order / Cart / Payment

> **허브:** [product-bible-hub.md](../product-bible-hub.md) §3 키오스크 흐름

## 흐름

Home → Menu → Detail → **Cart** → Order Create → **Payment** → Complete

- Cart ≠ Order · Payment는 Order와 **별도 상태** · **서버가 가격 최종 권한**

## 문서 목록

### Cart
| 문서 | 내용 |
|---|---|
| [Cart Architecture](cart/CART_ARCHITECTURE.md) | 구조 |
| [Cart State & Events](cart/CART_STATE_AND_EVENT_FLOW.md) | 상태·이벤트 |
| [Cart API Contract](cart/CART_API_AND_DATA_CONTRACT.md) | API·필드 |
| [Cart Edge Cases & QA](cart/CART_EDGE_CASE_AND_QA.md) | 예외·QA |

### Order
| 문서 | 내용 |
|---|---|
| [Order Architecture](order/ORDER_ARCHITECTURE.md) | 구조 |
| [Order Flow & State](order/ORDER_FLOW_AND_STATE.md) | 상태 머신 |
| [Order API Contract](order/ORDER_API_CONTRACT.md) | API |
| [Order Edge Cases & QA](order/ORDER_EDGE_CASE_AND_QA.md) | 예외·QA |

### Payment
| 문서 | 내용 |
|---|---|
| [Payment Architecture](payment/PAYMENT_ARCHITECTURE.md) | 구조 |
| [Payment Flow & State](payment/PAYMENT_FLOW_AND_STATE.md) | 흐름 |
| [Payment API Contract](payment/PAYMENT_API_CONTRACT.md) | API |
| [Payment Why](payment/PAYMENT_WHY.md) | 설계 이유 |
| [Payment Edge Cases & QA](payment/PAYMENT_EDGE_CASE_AND_QA.md) | 예외·QA |

## 연결 화면 (Pack 7)

[SCR-005 Cart](../07_Screen_Bible/SCR-005-KIOSK-CART.md) · [SCR-007 Payment](../07_Screen_Bible/SCR-007-KIOSK-PAYMENT.md) · [SCR-008 Complete](../07_Screen_Bible/SCR-008-KIOSK-COMPLETE.md)
