# 02_Order_Cart_Payment

> Status: **CANONICAL**
> Updated: `2026-08-14`
> Pack 경계는 유지하고, 반복 문서는 도메인별 통합 문서로 줄였습니다.

## 현재 문서

- [CART_BIBLE.md](CART_BIBLE.md)
- [ORDER_BIBLE.md](ORDER_BIBLE.md)
- [PAYMENT_BIBLE.md](PAYMENT_BIBLE.md)

## 이전 Pack 안내

### Pack 02 — Order / Cart / Payment

> **허브:** [product-bible-hub.md](../product-bible-hub.md) §3 키오스크 흐름

#### 흐름

Home → Menu → Detail → **Cart** → Order Create → **Payment** → Complete

- Cart ≠ Order · Payment는 Order와 **별도 상태** · **서버가 가격 최종 권한**

#### 문서 목록

##### Cart
| 문서 | 내용 |
|---|---|
| [Cart Architecture](CART_BIBLE.md) | 구조 |
| [Cart State & Events](CART_BIBLE.md) | 상태·이벤트 |
| [Cart API Contract](CART_BIBLE.md) | API·필드 |
| [Cart Edge Cases & QA](CART_BIBLE.md) | 예외·QA |

##### Order
| 문서 | 내용 |
|---|---|
| [Order Architecture](ORDER_BIBLE.md) | 구조 |
| [Order Flow & State](ORDER_BIBLE.md) | 상태 머신 |
| [Order API Contract](ORDER_BIBLE.md) | API |
| [Order Edge Cases & QA](ORDER_BIBLE.md) | 예외·QA |

##### Payment
| 문서 | 내용 |
|---|---|
| [Payment Architecture](PAYMENT_BIBLE.md) | 구조 |
| [Payment Flow & State](PAYMENT_BIBLE.md) | 흐름 |
| [Payment API Contract](PAYMENT_BIBLE.md) | API |
| [Payment Why](PAYMENT_BIBLE.md) | 설계 이유 |
| [Payment Edge Cases & QA](PAYMENT_BIBLE.md) | 예외·QA |

#### 연결 화면 (Pack 7)

[SCR-005 Cart](../07_Screen_Bible/SCR-005-KIOSK-CART.md) · [SCR-007 Payment](../07_Screen_Bible/SCR-007-KIOSK-PAYMENT.md) · [SCR-008 Complete](../07_Screen_Bible/SCR-008-KIOSK-COMPLETE.md)
