# Backend 트러블슈팅 (Gradle / bootRun)

> Status: **CURRENT**

`ASAK-back`에서 `gradlew clean`, `gradlew bootRun`, `compileJava` 실행 시 `build` 폴더를 지우지 못해 실패하는 경우의 해결법입니다.

---

## 증상

Gradle 로그에 아래와 비슷한 메시지가 나옵니다.

```text
Execution failed for task ':clean'
> java.io.IOException: Unable to delete directory 'C:\ASAK-workspace\ASAK-back\build'
    Failed to delete some children. This might happen because
    a process has files open or has its working directory set in the target directory.
```

`compileJava` 단계에서도 같은 오류가 날 수 있습니다.

```text
Execution failed for task ':compileJava'
> java.io.IOException: Unable to delete directory '...\build\classes\java\main'
```

---

## 원인

Windows에서 `build` 안의 `.class` 파일이 **다른 프로세스에 잠겨** 있을 때 발생합니다.

| 원인 | 설명 |
|------|------|
| 이전 `bootRun` | 백엔드가 아직 실행 중이거나, 종료 직후 JVM이 파일을 잠깐 유지 |
| Gradle Daemon | 이전 빌드의 daemon이 `build` 디렉터리를 참조 |
| Cursor Java 확장 | Red Hat Java Language Server가 `build\classes`를 인덱싱 |
| 명령 오타 | `gradelw` ❌ → `gradlew` ✅ (`'.\gradelw' is not recognized`) |

---

## 빠른 해결 (권장 순서)

### 방법 A — 실행 스크립트 (가장 쉬움)

```powershell
cd C:\ASAK-workspace\ASAK-back
.\scripts\boot-run.ps1
```

`build` 잠금이 있으면 daemon 중지 → `build` 삭제 재시도 → `bootRun`까지 자동 처리합니다.

### 방법 B — 수동

PowerShell에서 `ASAK-back` 폴더로 이동한 뒤:

```powershell
cd C:\ASAK-workspace\ASAK-back

# 1) 실행 중인 bootRun이 있으면 해당 터미널에서 Ctrl+C

# 2) Gradle daemon 중지
.\gradlew --stop

# 3) build 폴더 수동 삭제
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue

# 4) 다시 실행 (clean 없이도 대부분 충분)
.\gradlew bootRun
```

> **팁:** 매번 `clean`은 필요 없습니다. 코드만 바꿨다면 `.\gradlew bootRun`만 실행하세요.  
> `clean`은 캐시·산출물을 완전히 비울 때만 사용합니다.

---

## 그래도 안 될 때

### 1) Cursor Java Language Server 잠금 해제

1. **Ctrl+Shift+P** → `Developer: Reload Window`
2. 위 [빠른 해결](#빠른-해결-권장-순서) 2~4단계 반복

### 2) Java 프로세스 확인

```powershell
Get-Process -Name java -ErrorAction SilentlyContinue |
  ForEach-Object {
    $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine
    [PSCustomObject]@{ Id = $_.Id; CommandLine = $cmd }
  }
```

- `AsakBackendApplication`, `bootRun`, `ASAK-back`이 보이면 → 해당 터미널에서 **Ctrl+C** 또는 `Stop-Process -Id <PID>`
- `jdt.ls` / `redhat.java`만 보이면 → [Reload Window](#1-cursor-java-language-server-잠금-해제) 후 `build` 삭제 재시도

### 3) 포트 점유 (8080)

`bootRun`은 떴는데 접속이 안 되거나, 재기동이 꼬일 때:

```powershell
netstat -ano | findstr :8080
# LISTENING 행의 PID 확인 후
Stop-Process -Id <PID> -Force
```

---

## 자주 하는 실수

| 증상 | 원인 | 해결 |
|------|------|------|
| `'.\gradelw' is not recognized` | 철자 오타 | `.\gradlew` 사용 |
| `clean bootRun`만 실패 | `build` 잠금 | `.\gradlew --stop` 후 `build` 삭제, `bootRun`만 실행 |
| `compileJava`만 실패 | 동일 (잠금) | 위와 동일 |
| daemon 관련 메시지 반복 | 이전 daemon 잔존 | `.\gradlew --stop` |
| `Language Support for Java ... couldn't create connection` | `java.project.resourceFilters` 형식 오류 등 | 아래 [Java LS 연결 실패](#java-ls-연결-실패) 참고 |

---

## Java LS 연결 실패

Cursor 알림: `Language Support for Java client: couldn't create connection to server`

로그에 `ClassCastException` + `setResourceFilters`가 보이면, `.vscode/settings.json`의 필터 형식이 잘못된 것입니다.

```json
// 올바름 — 문자열 배열
"java.project.resourceFilters": ["build", "\\.gradle"]

// 잘못됨 — 이중 배열 (Java LS 크래시)
"java.project.resourceFilters": [["build", "build"]]
```

복구:

1. **Ctrl+Shift+P** → `Java: Clean Java Language Server Workspace` → Reload
2. 그래도 안 되면 Cursor **완전 재시작**

PowerShell `couldn't create connection` 알림은 Java LS 크래시 때 연쇄로 뜨는 경우가 많습니다. Java LS 복구 후 사라지면 무시해도 됩니다.

### PowerShell Extension Terminal 알림

**PowerShell Extension Terminal**을 닫으면 `would you like to restart it?` 알림이 뜹니다.

| 구분 | 용도 |
|------|------|
| **일반 터미널** (JavaSE-25 LTS) | `gradlew`, `boot-run.ps1` 실행용 — **이걸 쓰면 됨** |
| **PowerShell Extension Terminal** | `.ps1` 편집 시 IntelliSense용 — 닫아도 빌드와 무관 |

- 알림이 뜨면 **No** 눌러도 됩니다.
- `.ps1` 스크립트를 거의 안 쓰면: 확장 탭에서 **PowerShell → Disable (Workspace)** 해도 됩니다.

---

## 예방

- `bootRun` 터미널을 닫기 전에 **Ctrl+C**로 정상 종료
- 습관적으로 `clean bootRun` 대신 **`.\scripts\boot-run.ps1`** 또는 **`bootRun`만** 사용
- 빌드가 꼬이면 daemon 먼저 중지: `.\gradlew --stop`
- 여러 터미널에서 동시에 `bootRun` / `clean` 하지 않기
- Cursor **Reload Window** 후 재시도 (Java Language Server가 `build`를 잠근 경우)

워크스페이스 `.vscode/settings.json`에 `java.project.resourceFilters`로 `build` 폴더를 Java LS 인덱싱에서 제외해 두었습니다. 설정 반영 후 **Reload Window**가 필요할 수 있습니다.

---

## 관련 문서

| 문서 | 내용 |
|------|------|
| [getting-started.md](getting-started.md) | 백엔드 실행 기본 |
| [install-windows.md](install-windows.md) | Windows 설치·환경 변수 |
| [install-windows.md § 자주 나는 오류](install-windows.md#자주-나는-오류--해결) | Git·Java·Python 공통 오류 |

---

## 한 줄 요약

```powershell
.\gradlew --stop; Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue; .\gradlew bootRun
```
