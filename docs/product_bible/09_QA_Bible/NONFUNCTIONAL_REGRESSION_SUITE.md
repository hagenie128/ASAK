# Nonfunctional Regression Suite

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ACCESSIBILITY_QA.md`
- `FIGMA_REGRESSION_CHECKLIST.md`
- `REGRESSION_SUITE.md`

---

## 원문: `ACCESSIBILITY_QA.md`

### Accessibility QA

#### Kiosk

- 터치 80×80px
- 글자 확대
- 고대비
- color-independent state
- Modal clipping
- focus outline

#### Admin

- keyboard navigation
- label
- aria
- table semantics
- modal focus trap
- ESC
- error focus

#### Copy

- 사용자를 탓하지 않음
- 해결 방법 포함
- 기술 원문 미노출

---

## 원문: `FIGMA_REGRESSION_CHECKLIST.md`

### Figma Regression Checklist

- 05-B / 06-B 원본 보호
- Premium 시안은 C 페이지
- Footer y/height 유지
- 16,800원 유지
- `__spec` 노출 없음
- Save 문구 오타 없음
- 반복 날짜 없음
- Component instance 해제 없음
- Variant property 유지
- PrototypeMap v2 최신

---

## 원문: `REGRESSION_SUITE.md`

### Regression Suite

기존 팀원이 만든 고객용 Frontend를 보호하기 위한 핵심 회귀 테스트다.

#### 변경 후 반드시 확인

- Home → Menu
- Menu → Detail
- Detail → Cart
- Cart quantity
- Cart total
- Payment route
- Complete route
- orderSessionStore
- 기존 API mock
- 기존 component import
- build
- lint

#### 중복 방지

- 기존 MenuCard가 유지되는가
- BottomCTA가 재사용되는가
- 기존 Store action이 유지되는가
- 기존 route가 깨지지 않았는가
- 새로운 component가 기존 역할을 대체하지 않았는가
