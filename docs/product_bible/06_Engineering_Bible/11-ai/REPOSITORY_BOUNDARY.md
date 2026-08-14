# Repository Boundary

## ASAK

담당:

- Product Bible
- Design/API/DB 문서
- seed
- 설정
- AI rules
- 운영 기준

금지:

- Kiosk/Admin 실제 UI 구현 복제
- Spring source 복제

---

## ASAK-Kiosk

담당:

- 고객용 React
- Cart/Order session
- Kiosk API client
- 접근성/Timeout

금지:

- Admin 실제 화면 신규 구현
- Backend 비즈니스 규칙 복제

---

## ASAK_Admin

담당:

- Dashboard
- Live Order
- Order Management
- Sold-out
- Menu Management
- Payment Settings
- Sales
- TTS

금지:

- 고객 Cart 구현
- Kiosk route

---

## ASAK-back

담당:

- API
- 비즈니스 검증
- Entity/DTO
- DB
- 상태 전이
- 가격 권한

금지:

- UI 문구 결정
- 브라우저 TTS 실행
- React state 책임
