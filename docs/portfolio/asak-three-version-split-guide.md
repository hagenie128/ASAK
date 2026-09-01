# ASAK 포트폴리오 3버전 분리 가이드

> Status: **CURRENT**
> 기준일: **2026-09-01**
> 목적: 팀 원본·하진 개인 확장·나연 개인 확장을 **Git history를 유지한 채** 분리하고, 배포·README·환경변수를 맞춘다.

---

## 0. 한눈에 보기

| 버전 | 라벨 | GitHub | 배포 허브 |
| --- | --- | --- | --- |
| **1. 공동 ASAK** | Team Project Original | 기존 repo 그대로 (PR/Issue 유지) | https://asak.stackroom.cloud |
| **2. 하진 ASAK** | Personal Extension | `hajin-asak-*` 신규 repo (mirror) | https://hajin-asak.stackroom.cloud |
| **3. 나연 ASAK** | Personal Extension | `nayeon-asak-*` 신규 repo (mirror) | https://nayeon-asak.stackroom.cloud |

**절대 금지**

- 새 저장소에 파일만 복사
- `git filter-repo` / squash로 팀 커밋 작성자·날짜 변경
- 팀 원본 repo에 개인 확장 커밋 추가

**팀 기간 구분**

```text
Team Development:     2026-07 ~ 2026-09  (종강 시연 2026-09-02)
Personal Extension:   2026-09-03 ~       (팀 종료 태그 이후)
```

---

## 1. 원본(Team Project Original)으로 유지할 repo

현재 GitHub 저장소를 **그대로** 원본으로 둔다. PR·Issue·작성자 이력은 이 repo에만 남긴다.

| 로컬 폴더 | 원본 GitHub | 소유자 |
| --- | --- | --- |
| `ASAK` | [hagenie128/ASAK](https://github.com/hagenie128/ASAK) | 하진 |
| `ASAK-back` | [nayeon0828/ASAK-backend](https://github.com/nayeon0828/ASAK-backend) | 나연 |
| `ASAK-Admin` | [hagenie128/ASAK-Admin](https://github.com/hagenie128/ASAK-Admin) | 하진 |
| `ASAK-Kiosk` | [hagenie128/ASAK-Kiosk](https://github.com/hagenie128/ASAK-Kiosk) | 하진 |
| `ASAK-workspace` | [hagenie128/ASAK-workspace](https://github.com/hagenie128/ASAK-workspace) | 하진 |

> `ASAK-skill`은 에이전트 도구용으로 3버전 분리 대상에서 **제외**한다.

### 1-1. 팀 종료 시점 고정 (태그)

종강 시연·최종 merge 완료 후, 각 저장소 `main` HEAD에 태그를 박는다.

```powershell
cd C:\ASAK-workspace\ASAK-back   # 각 저장소 반복
git fetch origin --prune
git switch main
git pull --ff-only origin main

git tag -a team-original-2026-09-02 -m "ASAK Team Project Original — graduation demo freeze"
git push origin team-original-2026-09-02

git switch -c team-original team-original-2026-09-02
git push origin team-original
```

| 저장소 | main HEAD (2026-09-01 기준) |
| --- | --- |
| ASAK | `ac0557b` |
| ASAK-back | `a219483` |
| ASAK-Admin | `c6099f4` |
| ASAK-Kiosk | `349fd7f` |

이후 **팀 원본 repo에는 개인 작업을 push하지 않는다.** (branch protection 권장)

### 1-2. (선택) GitHub Organization

`asak-team` org를 만들고 5개 repo를 Transfer하면 “팀 프로젝트 원본”이 더 명확해진다. 이력·PR·Issue는 유지된다.

---

## 2. 개인 repo 생성 (Git history 유지)

### 2-1. 방식: `git clone --mirror` → `git push --mirror`

파일 복사가 아니라 **전체 Git 객체**를 옮긴다.

```powershell
# 예: 하진 개인 백엔드 (팀 원본 = 나연 repo)
git clone --mirror https://github.com/nayeon0828/ASAK-backend.git hajin-asak-backend.git
cd hajin-asak-backend.git
git push --mirror https://github.com/hagenie128/hajin-asak-backend.git
```

GitHub에서 **빈 repo를 먼저 생성**한 뒤 mirror push한다.

### 2-2. 개인 repo 네이밍

| 구분 | 하진 (`hagenie128`) | 나연 (`nayeon0828`) |
| --- | --- | --- |
| 문서 | `hajin-asak` | `nayeon-asak` |
| 백엔드 | `hajin-asak-backend` | `nayeon-asak-backend` |
| Admin | `hajin-asak-admin` | `nayeon-asak-admin` |
| Kiosk | `hajin-asak-kiosk` | `nayeon-asak-kiosk` |
| 워크스페이스 | `hajin-asak-workspace` | `nayeon-asak-workspace` |

### 2-3. mirror 대상 (팀 원본 → 개인)

| 개인 | mirror 출처 (팀 원본) |
| --- | --- |
| 하진 4+1 repo | `hagenie128/ASAK`, `ASAK-Admin`, `ASAK-Kiosk`, `ASAK-workspace` + `nayeon0828/ASAK-backend` |
| 나연 4+1 repo | 위 5개 팀 원본 전부 |

### 2-4. 로컬 remote 설정

```powershell
git clone https://github.com/hagenie128/hajin-asak-backend.git
cd hajin-asak-backend
git remote add upstream https://github.com/nayeon0828/ASAK-backend.git
# origin    → 개인 repo (push)
# upstream  → 팀 원본 (참조만)
```

### 2-5. 개인 확장 첫 커밋

mirror 직후 README에 Personal Extension 섹션을 추가한다.

```powershell
git commit -m "docs: Personal Extension 시작 — team-original-2026-09-02 기준"
git push origin main
```

### 2-6. 이력 검증

```powershell
git shortlog -sn --all
git log --oneline --author="kimnayeon" | Select-Object -First 5
git log --oneline --author="hagenie128" | Select-Object -First 5
git log team-original-2026-09-02 -1
```

---

## 3. Frontend / Backend repo 구조

**현재 구조를 그대로 유지**한다. 모노레포로 합치지 않는다.

```text
ASAK/           문서·WBS·워크로그
ASAK-back/      Spring Boot (user + admin 패키지)
ASAK-Admin/     관리자 Vite React PWA
ASAK-Kiosk/     키오스크 Vite React PWA
ASAK-workspace/ 서브모듈 포인터 (선택)
```

각 버전(팀·하진·나연)마다 위 4~5개 repo 세트가 **같은 태그 SHA**에서 출발해야 배포가 맞는다.

### 팀 역할 (포트폴리오 README용)

| 담당 | 프론트 | 백엔드 |
| --- | --- | --- |
| **김나연** | ASAK-Kiosk — 주문 세션, 옵션, 토스페이먼츠, 타임아웃 | `user` — API-003/005/006, `UserOrderMapper` |
| **이하진** | ASAK-Admin — 주문·메뉴 CRUD, 품절·결제수단 | `admin` — `AdminOrderMapper`, 품절·매출, CORS·스키마 |

근거: [`docs/operations/meeting-minutes/README.md`](../operations/meeting-minutes/README.md)

---

## 4. 배포 구조

### 4-1. 도메인

```text
stackroom.cloud                         포트폴리오 메인

asak.stackroom.cloud                    Team Original 허브
  kiosk.asak.stackroom.cloud            Vercel — ASAK-Kiosk
  admin.asak.stackroom.cloud            Vercel — ASAK-Admin
  api.asak.stackroom.cloud              OCI VM — ASAK-back

hajin-asak.stackroom.cloud              하진 Personal Extension 허브
  kiosk.hajin-asak.stackroom.cloud
  admin.hajin-asak.stackroom.cloud
  api.hajin-asak.stackroom.cloud

nayeon-asak.stackroom.cloud             나연 Personal Extension 허브
  kiosk.nayeon-asak.stackroom.cloud
  admin.nayeon-asak.stackroom.cloud
  api.nayeon-asak.stackroom.cloud
```

허브 페이지는 Kiosk/Admin 링크 + **Team Project Original** / **Personal Extension** 배지를 표시한다.

### 4-2. Vercel (프론트)

| Vercel 프로젝트 | Git | Production | 도메인 |
| --- | --- | --- | --- |
| `asak-kiosk-team` | `hagenie128/ASAK-Kiosk` | `team-original` 브랜치 | `kiosk.asak.stackroom.cloud` |
| `asak-admin-team` | `hagenie128/ASAK-Admin` | `team-original` | `admin.asak.stackroom.cloud` |
| `hajin-asak-kiosk` | `hagenie128/hajin-asak-kiosk` | `main` | `kiosk.hajin-asak.stackroom.cloud` |
| `hajin-asak-admin` | `hagenie128/hajin-asak-admin` | `main` | `admin.hajin-asak.stackroom.cloud` |
| `nayeon-asak-kiosk` | `nayeon0828/nayeon-asak-kiosk` | `main` | `kiosk.nayeon-asak.stackroom.cloud` |
| `nayeon-asak-admin` | `nayeon0828/nayeon-asak-admin` | `main` | `admin.nayeon-asak.stackroom.cloud` |

### 4-3. Oracle Cloud VM (백엔드)

VM 1대 + 포트 분리 또는 버전별 VM.

```text
api.asak.stackroom.cloud          → :8080  (DB: asak_db_team)
api.hajin-asak.stackroom.cloud    → :8081  (DB: asak_db_hajin)
api.nayeon-asak.stackroom.cloud   → :8082  (DB: asak_db_nayeon)
```

Nginx 리버스 프록시 + Let's Encrypt. **DB는 버전별로 분리**한다.

---

## 5. Git 명령어 체크리스트

```text
Phase 1 — 팀 원본 동결
  □ 5개 repo에 team-original-2026-09-02 태그 + team-original 브랜치 push
  □ 팀 원본 README에 Team Project Original 배지
  □ (선택) main branch protection

Phase 2 — 개인 repo 생성
  □ GitHub에 hajin-asak-* / nayeon-asak-* 빈 repo 생성
  □ git clone --mirror → git push --mirror (저장소별)
  □ upstream remote 추가

Phase 3 — 개인 작업 시작
  □ README Personal Extension 섹션 + 첫 docs 커밋
  □ 이후 모든 개인 작업은 개인 repo에만 push

Phase 4 — 배포
  □ Vercel 6프로젝트 + 커스텀 도메인
  □ OCI VM + Nginx + DB 분리
  □ CORS 화이트리스트 적용

Phase 5 — 검증
  □ git shortlog로 팀 작성자 이력 존재 확인
  □ 브라우저에서 Kiosk → API → Admin E2E
```

전체 mirror 스크립트 예시:

```powershell
$teamRepos = @(
  @{ Src = "https://github.com/hagenie128/ASAK.git";           Dst = "https://github.com/hagenie128/hajin-asak.git" },
  @{ Src = "https://github.com/nayeon0828/ASAK-backend.git";   Dst = "https://github.com/hagenie128/hajin-asak-backend.git" },
  @{ Src = "https://github.com/hagenie128/ASAK-Admin.git";     Dst = "https://github.com/hagenie128/hajin-asak-admin.git" },
  @{ Src = "https://github.com/hagenie128/ASAK-Kiosk.git";     Dst = "https://github.com/hagenie128/hajin-asak-kiosk.git" }
)

foreach ($r in $teamRepos) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($r.Src -replace '/$','')
  git clone --mirror $r.Src "$name.git"
  Set-Location "$name.git"
  git push --mirror $r.Dst
  Set-Location ..
}
```

---

## 6. README 수정안

### 6-1. 팀 원본 repo (모든 repo 상단)

```markdown
> **Team Project Original** — 팀 프로젝트 종료 시점 스냅샷
> Team Development: 2026.07 ~ 2026.09
> Freeze tag: `team-original-2026-09-02`
> 이 저장소에는 팀 종료 이후 개인 확장 작업을 추가하지 않습니다.

| 버전 | 배포 |
| --- | --- |
| Team Original (이 repo) | https://asak.stackroom.cloud |
| 하진 Personal Extension | https://hajin-asak.stackroom.cloud |
| 나연 Personal Extension | https://nayeon-asak.stackroom.cloud |
```

### 6-2. 하진 개인 repo

```markdown
# ASAK — Personal Extension (Hajin)

## Project Origin

**Original ASAK Team Project**
Team Development: 2026.07 ~ 2026.09

## My Role

| 영역 | 담당 |
| --- | --- |
| 프론트 | ASAK-Admin — 주문·메뉴 CRUD, 품절·결제수단 |
| 백엔드 | admin 도메인 — AdminOrderMapper, 품절·매출 API |
| 공통 | Figma·디자인 시스템, MySQL DDL, CORS, 문서 |

## Personal Extension

팀 종료(`team-original-2026-09-02`) 이후 개인적으로 추가·개선한 기능을 여기에 기록한다.

## Original Repository

- https://github.com/hagenie128/ASAK
- https://github.com/nayeon0828/ASAK-backend
- https://github.com/hagenie128/ASAK-Admin
- https://github.com/hagenie128/ASAK-Kiosk

## Contribution

- https://github.com/hagenie128/ASAK/commits?author=hagenie128
- https://github.com/nayeon0828/ASAK-backend/commits?author=hagenie128
- https://github.com/hagenie128/ASAK-Admin/commits?author=hagenie128
- https://github.com/hagenie128/ASAK-Kiosk/commits?author=hagenie128
```

### 6-3. 나연 개인 repo

```markdown
# ASAK — Personal Extension (Nayeon)

## Project Origin

**Original ASAK Team Project**
Team Development: 2026.07 ~ 2026.09

## My Role

| 영역 | 담당 |
| --- | --- |
| 프론트 | ASAK-Kiosk — 주문 세션, 토스페이먼츠, 타임아웃 |
| 백엔드 | user 도메인 — API-003/005/006, UserOrderMapper |
| 공통 | Spring Boot·MyBatis 골격, API 명세 |

## Personal Extension

팀 종료(`team-original-2026-09-02`) 이후 개인적으로 추가·개선한 기능을 여기에 기록한다.

## Original Repository

- https://github.com/hagenie128/ASAK
- https://github.com/nayeon0828/ASAK-backend
- https://github.com/hagenie128/ASAK-Admin
- https://github.com/hagenie128/ASAK-Kiosk

## Contribution

- https://github.com/hagenie128/ASAK/commits?author=kimnayeon
- https://github.com/nayeon0828/ASAK-backend/commits?author=kimnayeon
- https://github.com/hagenie128/ASAK-Kiosk/commits?author=kimnayeon
```

---

## 7. `.env`, API URL, CORS

### 7-1. 프론트 (Vercel Environment Variables)

**Team — Kiosk**

```env
VITE_API_BASE_URL=https://api.asak.stackroom.cloud
VITE_TOSS_CLIENT_KEY=test_ck_발급키
VITE_PAYMENT_PUBLIC_ORIGIN=https://kiosk.asak.stackroom.cloud
```

**Team — Admin**

```env
VITE_API_BASE_URL=https://api.asak.stackroom.cloud
```

하진·나연 버전은 `api.hajin-asak.stackroom.cloud`, `kiosk.hajin-asak.stackroom.cloud` 등으로 동일 패턴.

로컬 개발은 기존 `vite.config.js` proxy(`/api` → `localhost:8080`) 유지.

### 7-2. Vercel API 프록시 (선택)

`VITE_API_BASE_URL=/api` 사용 시 `vercel.json`:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.asak.stackroom.cloud/api/:path*"
    }
  ]
}
```

### 7-3. 백엔드 `.env` (OCI VM)

```env
DB_URL=jdbc:mysql://localhost:3306/asak_db_team?useSSL=false&serverTimezone=Asia/Seoul&allowPublicKeyRetrieval=true&characterEncoding=UTF-8
DB_USERNAME=asak_team
DB_PASSWORD=***
TOSS_SECRET_KEY=test_sk_***
CORS_ALLOWED_ORIGINS=https://kiosk.asak.stackroom.cloud,https://admin.asak.stackroom.cloud,https://asak.stackroom.cloud
```

버전별로 DB 이름·`CORS_ALLOWED_ORIGINS`를 분리한다.

### 7-4. CORS 운영화 (`SecurityConfig`)

현재 개발용 `allowedOriginPatterns("*")`를 환경변수 기반으로 전환한다.

`application.properties`:

```properties
app.cors.allowed-origins=${CORS_ALLOWED_ORIGINS}
```

`SecurityConfig.java`:

```java
@Value("${app.cors.allowed-origins}")
private String corsAllowedOrigins;

config.setAllowedOriginPatterns(
    Arrays.stream(corsAllowedOrigins.split(","))
        .map(String::trim)
        .toList());
```

로컬 `application-local.properties`에는 `http://localhost:5173,http://localhost:5174` 추가.

| 버전 | CORS_ALLOWED_ORIGINS |
| --- | --- |
| Team | `https://kiosk.asak.stackroom.cloud,https://admin.asak.stackroom.cloud,https://asak.stackroom.cloud` |
| Hajin | `https://kiosk.hajin-asak.stackroom.cloud,https://admin.hajin-asak.stackroom.cloud,https://hajin-asak.stackroom.cloud` |
| Nayeon | `https://kiosk.nayeon-asak.stackroom.cloud,https://admin.nayeon-asak.stackroom.cloud,https://nayeon-asak.stackroom.cloud` |

---

## 8. 주의사항

1. **하진이 소유한 repo = 팀 원본이기도 함** — 개인 작업은 `hajin-asak-*`에서만 진행한다.
2. **백엔드 원본은 나연 계정** — 하진 개인 백엔드는 mirror로 새 repo를 만든다.
3. **2026-09-01 커밋**은 졸업 MVP 준비(팀 작업)로 본다. 태그는 시연 직후에 거는 것이 안전하다.
4. 팀 원본의 PR/Issue는 **원본 repo에만** 유지한다. 개인 repo README에서 링크로 참조한다.

---

## 관련 문서

- [Git 저장소 현황](../operations/setup/git-repositories.md)
- [종강 시연 MVP](../wiki/graduation-demo-mvp-2026-09-02.md)
- [팀 역할·회의록](../operations/meeting-minutes/README.md)
