# Git 전략

<aside>
➡️

**이 페이지는 보관되었습니다.** 정본 → Git [`01-team-setup.md` §10](https://github.com/hagenie128/ASAK/blob/main/docs/guides/01-team-setup.md#10-팀-공통-git-순서) · [📚 팀 운영 레퍼런스](../%ED%82%A4%EC%98%A4%EC%8A%A4%ED%81%AC%20%ED%92%80%EC%8A%A4%ED%83%9D%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/01%20%ED%8C%80%20%EC%97%AD%ED%95%A0%20%EC%9D%BC%EC%A0%95/%ED%8C%80%20%EC%9A%B4%EC%98%81%20%EB%A0%88%ED%8D%BC%EB%9F%B0%EC%8A%A4.md) · [WBS-006](../%ED%82%A4%EC%98%A4%EC%8A%A4%ED%81%AC%20%ED%92%80%EC%8A%A4%ED%83%9D%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/07%20WBS%20%EA%B0%9C%EB%B0%9C%20%EC%A7%84%ED%96%89%20%ED%98%84%ED%99%A9/WBS%20%EA%B0%9C%EB%B0%9C%20%EC%A7%84%ED%96%89%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/Git%20%EC%A0%84%EB%9E%B5%20%C2%B7%20%EB%B0%B1%EB%A1%9C%EA%B7%B8%20%ED%8B%B0%EC%BC%93%ED%99%94.md)

</aside>

[https://github.com/hagenie128/Greens.git](https://github.com/hagenie128/Greens.git)

### 브랜치 구조

```
main        → 발표/데모용 최종 안정 버전
develop     → 다음 배포 대상, 기능 브랜치들이 여기로 병합
feature/*   → 기능 단위 작업 브랜치 (develop에서 분기)
fix/*       → 버그 수정 브랜치
```

**브랜치 네이밍 예시**

- `feature/menu-selection-ui`
- `feature/order-api`
- `fix/cart-quantity-bug`

### 워크플로우

1. develop에서 feature/기능명 브랜치 생성
2. 작업 완료 후 develop으로 Pull Request
3. 최소 1명 리뷰 후 병합 (본인 PR 본인 머지 금지)
4. 스프린트 종료 시 develop → main 병합

**커밋 메시지 컨벤션**

```
feat: 메뉴 옵션 선택 UI 구현
fix: 장바구니 수량 계산 오류 수정
docs: API 명세서 업데이트
refactor: 주문 서비스 로직 분리
```

**체크리스트**

- [ ]  1주차 안에 GitHub 레포 생성 + 브랜치 규칙 전원 공유
- [ ]  PR 템플릿 만들기 (변경사항 / 테스트 여부 / 스크린샷)
- [ ]  .gitignore 설정