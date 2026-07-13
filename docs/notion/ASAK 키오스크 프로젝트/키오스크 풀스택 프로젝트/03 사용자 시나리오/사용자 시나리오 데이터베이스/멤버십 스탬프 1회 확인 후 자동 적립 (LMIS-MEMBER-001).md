# 멤버십 스탬프 1회 확인 후 자동 적립 (LMIS-MEMBER-001)

시작 조건: 결제 단계 진입
종료 조건: 결제완료 화면에 적립 여부가 표시됨(결제 전/후 이중 확인 없음)
기본 흐름: 결제 진행 중 멤버십 적립 여부 1회 확인 → 결제 완료 시 자동 적립 처리 → 결제완료 화면에 적립 결과 표시
예외 흐름: 멤버십 미가입 고객은 적립 단계 생략하고 바로 결제 진행
관련 화면: SCR-007, SCR-021, SCR-008
기능계층: 추가기능
관련 요구사항: LMIS-MEMBER-001
관련 API: POST /payments, POST /membership/stamps
단계: KSD
비고: 8주 로드맵 후반 멤버십 확장 시 함께 구현. Day 10 1차 발표 범위 외.
사용자 유형: 손님
상태: 초안
시나리오 ID: SC-006
시나리오 유형: 결제
우선순위: 중
Related to 테스트 시나리오 데이터베이스 (↔ 시나리오): 스탬프 적립 확인이 결제 전후로 중복되지 않는지 검증 (../../09%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%98%A4%EB%A5%98%20%EA%B4%80%EB%A6%AC/%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EC%8A%A4%ED%83%AC%ED%94%84%20%EC%A0%81%EB%A6%BD%20%ED%99%95%EC%9D%B8%EC%9D%B4%20%EA%B2%B0%EC%A0%9C%20%EC%A0%84%ED%9B%84%EB%A1%9C%20%EC%A4%91%EB%B3%B5%EB%90%98%EC%A7%80%20%EC%95%8A%EB%8A%94%EC%A7%80%20%EA%B2%80%EC%A6%9D.md), 포인트·쿠폰 적립 및 QR 할인 적용 (../../09%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%98%A4%EB%A5%98%20%EA%B4%80%EB%A6%AC/%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7%EC%BF%A0%ED%8F%B0%20%EC%A0%81%EB%A6%BD%20%EB%B0%8F%20QR%20%ED%95%A0%EC%9D%B8%20%EC%A0%81%EC%9A%A9.md)
↔ API: 가상 결제 처리 (../../06%20API%20%EB%AA%85%EC%84%B8/API%20%EB%AA%85%EC%84%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EA%B0%80%EC%83%81%20%EA%B2%B0%EC%A0%9C%20%EC%B2%98%EB%A6%AC.md), 멤버십 스탬프 적립 (../../06%20API%20%EB%AA%85%EC%84%B8/API%20%EB%AA%85%EC%84%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EB%A9%A4%EB%B2%84%EC%8B%AD%20%EC%8A%A4%ED%83%AC%ED%94%84%20%EC%A0%81%EB%A6%BD.md)
↔ 요구사항: 멤버십 스탬프 자동 적립 (../../02%20%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%20%EC%A0%95%EC%9D%98/%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%20%EB%AA%A9%EB%A1%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EB%A9%A4%EB%B2%84%EC%8B%AD%20%EC%8A%A4%ED%83%AC%ED%94%84%20%EC%9E%90%EB%8F%99%20%EC%A0%81%EB%A6%BD.md), 스탬프 1회 확인 후 자동 적립 (../../02%20%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%20%EC%A0%95%EC%9D%98/%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%20%EB%AA%A9%EB%A1%9D%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EC%8A%A4%ED%83%AC%ED%94%84%201%ED%9A%8C%20%ED%99%95%EC%9D%B8%20%ED%9B%84%20%EC%9E%90%EB%8F%99%20%EC%A0%81%EB%A6%BD.md)

```mermaid
flowchart TD
    A[결제 SCR-007] --> B[적립 확인 SCR-021 1회 노출]
    B --> C[결제 완료 SCR-008]
    C --> D[적립 결과 자동 표시]
```