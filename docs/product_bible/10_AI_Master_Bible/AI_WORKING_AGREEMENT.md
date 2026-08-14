# AI Working Agreement

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `AI_GOVERNANCE.md`
- `SOURCE_OF_TRUTH.md`
- `MASTER_PROMPT.md`
- `CODEX_RULES.md`
- `CLAUDE_RULES.md`
- `GPT_RULES.md`
- `AI_HANDOFF_CHECKLIST.md`

---

## 원문: `AI_GOVERNANCE.md`

### AI Governance

AI는 다음 순서로 판단한다.

Product Bible
→ Screen Bible
→ Component Bible
→ Engineering Bible
→ 기존 코드

AI는 기존 컴포넌트를 먼저 검색한 뒤 재사용을 시도한다.

---

## 원문: `SOURCE_OF_TRUTH.md`

### Source of Truth

1. Product Bible
2. 최신 Figma
3. API Contract
4. DB Schema
5. 기존 구현

충돌 시 상위 기준을 우선 검토한다.

---

## 원문: `MASTER_PROMPT.md`

### Master Prompt

프로젝트를 구현할 때는:

- 기존 구조 유지
- JavaScript 유지
- Spring Boot 구조 유지
- 새 컴포넌트보다 기존 컴포넌트 재사용
- Mock Data와 실제 API를 혼동하지 않음
- 변경 이유를 먼저 설명

---

## 원문: `CODEX_RULES.md`

### Codex Rules

- Scaffold 삭제 금지
- MenuCard, BottomCTA 등 기존 컴포넌트 우선
- 기존 팀원 코드 리팩터링은 최소화
- 변경 시 영향 파일 목록 제시

---

## 원문: `CLAUDE_RULES.md`

### Claude Rules

- 설계 변경은 근거 포함
- 문서와 구현의 불일치 발견 시 먼저 보고
- 추측으로 API 생성 금지

---

## 원문: `GPT_RULES.md`

### GPT Rules

- 문서 생성 시 기존 네이밍 유지
- MVP와 확장 기능을 구분
- 팀 합의 없는 기능 추가 금지

---

## 원문: `AI_HANDOFF_CHECKLIST.md`

### AI Handoff Checklist

- [ ] 기존 코드 재사용 검토
- [ ] Screen Bible 확인
- [ ] Component Bible 확인
- [ ] API 계약 확인
- [ ] QA 영향 검토
- [ ] 회귀 테스트 확인
