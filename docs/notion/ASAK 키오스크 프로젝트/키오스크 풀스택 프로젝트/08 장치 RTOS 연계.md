# 08. 장치/RTOS 연계

# 목적

<aside>
🖨️

**Week 5 MVP 제외** — 영수증·QR·프린터·결제 단말·RTOS Simulator·장치 이벤트 로그는 **이후 확장** 범위입니다.

</aside>

이 페이지는 ASAK 키오스크 프로젝트에서 장치/RTOS 연계 기능을 이후 확장 범위로 관리하기 위한 참고 문서입니다.

Week 5 MVP에서는 아래를 **우선 구현**합니다.

- 고객 주문 흐름
- 옵션 선택
- 장바구니
- 가상 결제
- 관리자 주문 확인

## Week 5 MVP 기준

- 실제 프린터/QR/바코드/결제 단말 연동은 구현하지 않습니다.
- 결제는 `payment` 테이블에 가상 승인 결과만 기록합니다.
- `device_event` 테이블과 장치 로그 API는 MVP DB/API 범위에 포함하지 않습니다.
- 주문 완료 화면에는 주문번호와 결제 완료 메시지만 표시합니다.

## 이후 확장 시 전체 구조

```
키오스크 UI
→ Spring Boot API
→ MySQL DB
→ 장치/RTOS Simulator
→ 처리 결과 반환
→ 장치 이벤트 로그 기록
```

## 이후 확장 API 후보

| 확장 기능 | API 후보 | 설명 |
| --- | --- | --- |
| 영수증 출력 | POST /api/orders/{orderId}/receipt-print | 주문/결제/상품 내역 조회 후 프린터 요청 |
| QR/바코드 스캔 | POST /api/device/scan | 쿠폰, 멤버십, 바코드 입력값 검증 |
| 장치 상태 조회 | GET /api/device/status | 프린터/스캐너/결제장치 상태 확인 |
| 장치 이벤트 로그 조회 | GET /api/admin/device-events | 관리자 장치 로그 확인 |

## 이후 확장 DB 후보

| 테이블 후보 | 역할 | 비고 |
| --- | --- | --- |
| device_event | 장치 이벤트 로그 저장 | 프린터 출력, 스캔, 장치 오류 등을 기록 |

> payment_method_config는 05번 DB 설계에서 이미 22개 정식 테이블 중 17번으로 확정되어 있어 이 후보 목록에서 제외합니다 (2026-07-04 수정). Week 5 MVP 기준 구조만 두고 선택 구현하는 대상이며, 실제 결제수단 활성/비활성 반영은 API-013/014·WBS-030에서 다룹니다.
>

## 요구사항 ID 기준

| 확장 ID | 내용 | 현재 처리 |
| --- | --- | --- |
| RTOS-DEVICE-001 | 영수증 출력 여부 선택 및 출력 처리 | Week 5 MVP 제외, 주문 완료 화면의 주문번호로 대체 |
| RTOS-DEVICE-002 | QR/바코드 스캔을 통한 쿠폰·멤버십 인식 | Week 5 MVP 제외, 멤버십 확장 시 함께 검토 |
| RTOS-DEVICE-003 | 장치 이벤트 로그 저장 및 조회 | Week 5 MVP 제외, device_event 확장 시 적용 |
| LMIS-PAY-001 | 결제수단 설정 및 실제 PG 연동 | Week 5 MVP에서는 CARD 가상 결제만 사용 |
| RTOS-SYS-001 | CMS/원격 모니터링 | 후반 확장 아이디어로 보관 |

## 장치 연계 원칙

1. 장치 또는 RTOS Simulator는 DB에 직접 접근하지 않습니다.
2. DB 접근은 Spring Boot API만 담당합니다.
3. 장치 요청/응답은 API를 통해 처리합니다.
4. 장치 이벤트 로그가 필요해지는 시점에 `device_event`를 별도 추가합니다.
5. MVP 문서, API, DB에는 장치 기능을 필수 범위처럼 섞지 않습니다.
