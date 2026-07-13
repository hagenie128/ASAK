# 데이터는 Spring Boot를 통해서만 접근

검수 기준: DB 접속 설정은 Spring Boot 프로젝트에만 존재한다.
구분: 비기능
단계: KSD
비고: 아키텍처 핵심 원칙
상세 설명: React와 모의 장치/RTOS Simulator는 DB에 직접 접근하지 않고 Spring Boot API를 통해서만 데이터를 처리해야 한다.
상태: 예정
요구사항 ID: REQ-011
우선순위: 상