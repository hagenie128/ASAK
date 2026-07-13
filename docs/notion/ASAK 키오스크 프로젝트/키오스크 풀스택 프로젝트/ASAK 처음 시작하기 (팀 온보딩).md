# ASAK 처음 시작하기 (팀 온보딩)

<aside>
📌

**Notion 정본:** [ASAK 처음 시작하기 (팀 온보딩)](ASAK%20%EC%B2%98%EC%9D%8C%20%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0%20(%ED%8C%80%20%EC%98%A8%EB%B3%B4%EB%94%A9).md) · Git mirror: [`docs/GETTING_STARTED.md`](https://github.com/hagenie128/ASAK/blob/main/docs/GETTING_STARTED.md)

</aside>

---

> **한 줄 요약:** ASAK는 샐러디 키오스크를 만드는 풀스택 학습 프로젝트입니다. 화면(프론트)과 API(백엔드)를 **둘 다** 켜야 실제 주문 흐름을 볼 수 있습니다.
> 

처음이어도 괜찮아요. 이 문서만 순서대로 따라 하면 됩니다.

**목차**

- Part 1 — 프로젝트 세팅
- Part 2 — 워크로그 쓰기 (유치원 선생님 모드)

---

# Part 1 — 프로젝트 세팅

## 이 프로젝트가 뭔가요?

**ASAK** = **A Salad A Kiosk** (샐러디 키오스크 풀스택 프로젝트)

- 고객이 키오스크에서 메뉴를 고르고 주문하는 **화면(프론트엔드)**
- 메뉴·주문 데이터를 주고받는 **서버(백엔드 API)**
- 메뉴 원본 데이터를 모으는 **데이터 파이프라인(Python)**

이 세 가지가 함께 동작합니다.

---

## 꼭 알아둘 것: 저장소가 3개예요

헷갈리기 쉬운 부분이라 **먼저** 읽어 주세요.

| 로컬 폴더 (예시) | GitHub | 하는 일 |
| --- | --- | --- |
| `c:\ASAK` | [ASAK](https://github.com/hagenie128/ASAK) | 문서, 데이터 파이프라인, 팀 가이드 |
| `c:\ASAK-front` | [ASAK-front](https://github.com/hagenie128/ASAK-front) | **실제** 키오스크 화면 (React) |
| `c:\ASAK-back` | [ASAK-back](https://github.com/hagenie128/ASAK-back) | **실제** API 서버 (Spring Boot) |

`ASAK` 통합 저장소 안의 `frontend/`, `backend/` 폴더는 **구조 참고용**에 가깝습니다.

실제 키오스크 개발은 `ASAK-front`와 `ASAK-back`에서 합니다.

> 작업 후 통합 저장소(`ASAK`)에 다시 합칠 필요는 **없습니다.** 어디서 작업했으면 그 저장소에만 push 하면 됩니다.
> 

---

## 왜 프론트와 백엔드를 둘 다 켜야 하나요?

| 케이스 | 어떻게 되나요? |
| --- | --- |
| **프론트만** 켬 | 화면은 뜨지만 API 호출이 실패합니다. |
| **백엔드만** 켬 | API는 살아 있지만 화면이 없어서 주문 흐름을 확인할 수 없습니다. |
| **둘 다** 켬 | 화면·메뉴·주문 결과가 정상 표시됩니다. ✅ |

**비유:** 프론트 = 메뉴판, 백엔드 = 주방.

### 예외: 데이터만 보고 싶을 때

`frontend/run_viewer.py`는 JSON만으로 동작합니다. **진짜 키오스크 앱**은 `ASAK-front` + `ASAK-back`입니다.

---

## 준비물 · 1~4단계 세팅

Windows(PowerShell) 기준 — Git · Python 3.11 · Java 21 · Node 20 LTS.

```powershell
git clone https://github.com/hagenie128/ASAK.git c:\ASAK
git clone https://github.com/hagenie128/ASAK-front.git c:\ASAK-front
git clone https://github.com/hagenie128/ASAK-back.git c:\ASAK-back
```

```powershell
cd c:\ASAK\data-pipeline\phase1
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_phase1.py
```

```powershell
cd c:\ASAK-back
.\gradlew.bat bootRun
```

```powershell
cd c:\ASAK-front
npm install
npm run dev
```

---

## 체크리스트

- [ ]  `git --version`, `python --version` OK
- [ ]  3개 저장소 클론 완료
- [ ]  백엔드 + 프론트 기동 → 메뉴 표시 🎉

> **상세 명령·에러 해결·5단계 뷰어**는 Git 정본 [`docs/GETTING_STARTED.md`](https://github.com/hagenie128/ASAK/blob/main/docs/GETTING_STARTED.md) Part 1 참고.
> 

---

# Part 2 — 워크로그 쓰기 (유치원 선생님 모드)

워크로그는 **오늘 뭘 했는지** 팀에게 알려주는 일기입니다. 퇴근 전 **5분**이면 됩니다.

**정본(토큰·DB·상세):** [일일 워크로그 — 팀 가이드](01%20%ED%8C%80%20%EC%97%AD%ED%95%A0%20%EC%9D%BC%EC%A0%95/%EC%9D%BC%EC%9D%BC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EA%B7%B8%20%E2%80%94%20%ED%8C%80%20%EA%B0%80%EC%9D%B4%EB%93%9C.md)

## Quick Start

```powershell
$env:NOTION_TOKEN = "secret_..."
cd C:\ASAK
python asak-data/scripts/verify_notion_token.py
python worklog/scripts/init_daily.py
python worklog/scripts/sync_daily_to_notion.py --date today
```

또는 한 줄:

```powershell
python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "작업 요약"
```

> **Part 2 전체(토큰 검증·중복 정리·명령표)**는 Git [`docs/GETTING_STARTED.md` Part 2](https://github.com/hagenie128/ASAK/blob/main/docs/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드) 또는 위 팀 가이드 정본을 보세요.
> 

---

## 다음에 할 일

1. [문서 읽는 순서](01%20%ED%8C%80%20%EC%97%AD%ED%95%A0%20%EC%9D%BC%EC%A0%95/%EB%AC%B8%EC%84%9C%20%EC%9D%BD%EB%8A%94%20%EC%88%9C%EC%84%9C.md) — guides 01~02
2. `develop`에서 `feature/...` 브랜치로 작업
3. **매일 퇴근 전** 워크로그 한 줄 ✍️

화이팅! 🥗