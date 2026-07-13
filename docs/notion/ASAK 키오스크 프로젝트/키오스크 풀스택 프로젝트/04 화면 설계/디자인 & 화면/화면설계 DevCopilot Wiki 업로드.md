# 화면설계 DevCopilot/Wiki 업로드

<aside>
📌

**이 페이지의 역할** — Notion SCR → **DevCopilot/Wiki 업로드 절차만**. Figma·wireframe 가이드는 [디자인 & 화면 hub](../%EB%94%94%EC%9E%90%EC%9D%B8%20&%20%ED%99%94%EB%A9%B4.md) 참고.

</aside>

<aside>
🔗

**Git 로컬 도구** (정본 아님)

- `docs/screens/` — export JSON·MD
- `asak-data/scripts/export_screens.py` · `upload_screens_wiki.py`
</aside>

---

Notion [**04. 화면 설계**](../../04%20%ED%99%94%EB%A9%B4%20%EC%84%A4%EA%B3%84.md) SCR DB (SCR-001~021)를 학원 PC에서 DevCopilot에 올리는 방법입니다.

> Figma frame 링크·셋업 → [Figma 태블릿 세로 Setup](Figma%20%ED%83%9C%EB%B8%94%EB%A6%BF%20%EC%84%B8%EB%A1%9C%20Setup.md) · [Figma 가이드](Figma%20%EA%B0%80%EC%9D%B4%EB%93%9C%20+%20SCR%C3%97Figma%20%EB%A7%A4%ED%8A%B8%EB%A6%AD%EC%8A%A4.md)
> 

## 미리 준비한 파일 (집에서 USB/클라우드로 복사)

| 파일 | 용도 |
| --- | --- |
| `docs/screens/screens.md` | Screens UI 수동 입력용 표 (가장 읽기 쉬움) |
| `docs/screens/screens.json` | 구조화 체크리스트 |
| `docs/screens/screens-devcopilot-import-array.json` | localStorage import용 배열 |
| `docs/screens/screens-wiki.md` | Wiki 업로드 본문 |
| `asak-data/scripts/upload_screens_wiki.py` | Wiki API 업로드 스크립트 |

재생성: `python asak-data/scripts/export_screens.py`

---

## DevCopilot Screens localStorage 형식 (확인됨)

- **키**: `ws_2_screens` (패턴: `ws_{workspaceId}_screens`)
- **값**: JSON 배열. 항목 필드:

```json
{
  "id": "SCR-001",
  "name": "홈 화면",
  "figmaUrl": "",
  "inputs": "없음",
  "outputs": "주문 시작 버튼, 브랜드 안내",
  "status": "WIREFRAME"
}
```

- **status 값**: `WIREFRAME` | `DESIGNING` | `CODING` (UI 드롭다운)
- **Import 방법**: DevCopilot에 **공식 import UI 없음**. 학원 PC Chrome 개발자도구 → Application → Local Storage → `https://devcopilot.ai.kr` → `ws_2_screens`에 `screens-devcopilot-import-array.json` 내용 붙여넣기 후 새로고침.
- **주의**: 공용 PC라면 작업 후 localStorage 삭제 또는 팀 Wiki 방식 권장.

---

## 방법 비교

|  | Screens UI (localStorage) | Wiki API |
| --- | --- | --- |
| 저장 | 브라우저 로컬만 | 서버, 팀 공유 |
| 학원 PC | 매 PC마다 import 필요 | 한 번 업로드면 URL 공유 |
| Figma embed | UI에서 figmaUrl 입력·미리보기 | Markdown 링크만 |
| 소요 시간 | 19건 수동 ~20~40분 | 스크립트 1분 + 확인 5분 |
| **추천** | Figma 미리보기 데모 필요 시 | **시간 제한·공용 PC → 1순위** |

### 추천 (학원: 공용 PC + 시간 제한)

1. **집에서** `upload_screens_wiki.py`로 Wiki 업로드 (또는 학원에서 1회 실행)
2. 학원에서는 Wiki 페이지 열어 팀과 공유
3. 9/2 최종 발표 데모용 Figma가 필요하면 **SCR-001~011만** Screens UI에 localStorage import

---

## 방법 A — Screens UI 수동 입력

1. [https://devcopilot.ai.kr/workspace/2/screens](https://devcopilot.ai.kr/workspace/2/screens) 접속
2. `screens.md` 표를 보며 좌측 **+ 추가** 또는 기존 항목 선택
3. 필드 매핑:
    - ID → `id`
    - 화면명 → `name`
    - Figma URL → `figmaUrl`
    - 입력/출력 → `inputs` / `outputs`
    - 상태: 와이어프레임→`WIREFRAME`, 디자인중→`DESIGNING`, 개발중→`CODING`

## 방법 B — Wiki 업로드 (권장)

**업로드 완료 URL:** [https://devcopilot.ai.kr/workspace/2/wiki/16](https://devcopilot.ai.kr/workspace/2/wiki/16)

```powershell
# ASAK repo 루트에서 (로컬: C:\greens)
python asak-data/scripts/upload_screens_wiki.py

# 미리보기만
python asak-data/scripts/upload_screens_wiki.py --dry-run
```

curl 대안:

```powershell
curl -X POST "https://devproject-hub-backend.onrender.com/api/workspaces/2/wikis" `
  -H "Content-Type: application/json" `
  -H "x-user-username: hagenie128" `
  -d "{\"title\":\"ASAK 화면설계 (SCR-001~021)\",\"content\":\"...(screens-wiki.md 내용)...\"}"
```

## 방법 C — localStorage 일괄 import

1. `screens-devcopilot-import-array.json` 열기
2. Chrome F12 → Application → Local Storage → `devcopilot.ai.kr`
3. 키 `ws_2_screens` 생성/수정 → 값에 JSON 배열 전체 붙여넣기
4. `/workspace/2/screens` 새로고침 → 21건 표시 확인

---

## 학원 체크리스트

### 5분 버전 (Wiki만)

- [ ]  DevCopilot 로그인 (workspace 2)
- [ ]  Wiki에 화면설계 문서 있는지 확인 (없으면 `upload_screens_wiki.py` 실행)
- [ ]  팀원에게 Wiki URL 공유
- [ ]  Notion 04. 화면 설계 링크도 백업으로 열어두기

### 30분 버전 (9/2 최종 발표 데모 완성)

- [ ]  Wiki 업로드 확인 (5분)
- [ ]  `ws_2_screens` localStorage import (5분)
- [ ]  SCR-001~011 필드 누락 없는지 `screens.md` 대조 (15분)
- [ ]  Figma URL 있으면 figmaUrl 붙여넣기 (5분)
- [ ]  스크린샷 1장 (Screens 목록 + Wiki) 저장

---

## Week 5 MVP 우선 화면 (SCR-001~011)

고객 흐름 001~008 + 관리자 009~011 + 결제실패 012(최소 안내).  

SCR-013~021은 후반 확장 — Wiki에만 있어도 제출 가능.

---

## Notion 동기화

이 export는 **2026-07-06** Notion MCP fetch 스냅샷 기준. Notion 수정 후:

```powershell
python asak-data/scripts/export_screens.py
```

Notion DB 일괄 쿼리는 Business 플랜 필요 — 개별 페이지 fetch 또는 `screens_notion_snapshot.json` 수동 갱신.