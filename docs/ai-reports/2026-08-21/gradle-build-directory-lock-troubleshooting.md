# Windows에서 Gradle "Unable to delete directory" 잠금 해결 절차

- 날짜: 2026-08-21
- 계기: `ASAK-back`에서 gradle build 중 아래 에러 발생.

```text
java.io.IOException: Unable to delete directory 'C:\ASAK-workspace\ASAK-back\build\classes\java\main'
Failed to delete some children. This might happen because a process has files open
or has its working directory set in the target directory.
- C:\ASAK-workspace\ASAK-back\build\classes\java\main\com\asak\admin\dto\response\sales
- C:\ASAK-workspace\ASAK-back\build\classes\java\main\com\asak\admin\dto\response
- ...and more
BUILD FAILED in 5s
```

## 원인 확인 과정

1. **8080 포트 확인** — Spring Boot 앱(`bootRun`)이 실제로 떠 있어서 잠근 건지부터 배제.
   ```powershell
   Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Select-Object State,OwningProcess
   ```
   → `TimeWait`, `OwningProcess 0`만 나옴. 즉 8080은 비어 있고, 그 날 아침에 띄웠던
   `bootRun` 프로세스는 이미 종료된 상태였음. **서버 프로세스가 원인이 아니었다.**

2. **떠 있는 java.exe 전부 커맨드라인으로 확인**
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='java.exe'" | Select-Object ProcessId, CommandLine | Format-List
   ```
   → 실제로 뜬 것: Eclipse JDT Language Server(`redhat.java`, Cursor 확장), VS Code Gradle
   확장 서버, Spring Boot Language Server, Gradle Daemon. **서버가 아니라 IDE의 Java 툴링이
   `build/classes` 아래 파일을 인덱싱하려고 열어두고 있었을 가능성이 가장 큼.**
   Windows에서 흔한 케이스이며 코드 문제가 아니라 환경 문제.

## 일반 해결 절차 (재시도부터 최후 수단까지 순서대로)

### 1. 일단 재시도
파일 잠금이 순간적인 경우가 많아서, 같은 명령을 1~2번 다시 실행해보는 게 제일 빠르다.

### 2. `clean`이 꼭 필요한지부터 의심
에러는 디렉토리를 통째로 지우는 작업(`clean`류)에서만 난다. `clean` 없이
`./gradlew.bat compileJava` 또는 `./gradlew.bat build`만 돌려도 되는 상황이면 그게 제일
간단한 회피다. Gradle은 증분 컴파일이라 대부분의 경우 `clean`이 꼭 필요하지 않다.

### 3. 누가 잠갔는지 특정 (재시도로 안 풀릴 때)
Windows엔 `lsof` 가 기본으로 없어서:

- **작업 관리자 → 리소스 모니터(resmon.exe) → CPU 탭 → 연결된 핸들(Associated Handles)**
  에서 폴더 이름(`build`)으로 검색 → 어떤 프로세스가 그 파일을 열고 있는지 정확히 나온다.
  가장 확실한 방법.
- 또는 위 1~2단계처럼 `Get-CimInstance Win32_Process`로 떠 있는 java.exe 커맨드라인을 보고
  추론하는 방법(덜 정확하지만 빠름).

### 4. 범위를 좁혀서 정리
- Gradle daemon만 의심되면: `./gradlew.bat --stop` — 이 프로젝트 daemon만 안전하게 종료.
- IDE 확장(Java Language Server 등)이 의심되면: 강제 종료 대신 **Cursor "Reload Window"** —
  에디터는 안 끄고 언어 서버만 재시작돼서 안전하다.
- 그래도 안 풀리면, 리소스 모니터에서 찾은 정확한 PID를 `taskkill /PID <pid> /F`로 종료.
  이때부터는 그 프로세스가 정확히 뭔지 확인하고 지울 것 — 에디터 프로세스를 잘못 죽이면
  편집 중이던 내용이 날아갈 수 있다.

### 5. 최후 수단
재부팅. 핸들이 정말 안 풀리는 드문 경우에도 확실하게 풀린다. 시간이 걸리므로 마지막 선택지.

## 예방 팁

Java 확장(`redhat.java` 등)이 `build/` 폴더를 계속 감시·인덱싱해서 이런 잠금이 반복된다면,
확장 설정의 `files.watcherExclude`에 `**/build/**`를 추가해두면 애초에 이런 상황이 잘 생기지
않는다.

---

## 실제로 이 문제를 풀었을 때 기록 (2026-08-21, 위 절차만으론 안 풀렸던 사례)

위 1~5단계를 순서대로 다 시도했는데도 `./gradlew.bat compileJava`가 계속 같은 에러로 실패한
사례. 범인이 하나가 아니라 **여러 프로세스가 동시에 `build/classes`에 손대고 있었다.**

### 실제로 확인한 것

`Get-CimInstance Win32_Process -Filter "Name='java.exe'"`로 뜬 java 프로세스 커맨드라인을
하나씩 대조한 결과, 이 프로젝트와 관련된 것만 4개가 동시에 떠 있었다:

| PID(그때 기준) | 정체 | 처리 |
|---|---|---|
| Gradle daemon 2개(9.5.1) | 이 프로젝트의 gradle wrapper daemon | `./gradlew.bat --stop`으로 정지 |
| Gradle daemon(8.14.2, 별도) | VS Code Gradle 확장이 띄운, wrapper와 다른 버전의 daemon | `Stop-Process -Id <pid> -Force` |
| JDT Language Server (`org.eclipse.jdt.ls.core.id1`) | Cursor Java 확장의 인텔리센스 서버 | `Stop-Process -Id <pid> -Force` |
| Gradle 확장 빌드 서버 (`vscode-gradle`의 `gradle-server.jar`) | VS Code Gradle 확장의 백그라운드 빌드 연결 | `Stop-Process -Id <pid> -Force` |

이 4개를 하나씩 죽여가며 재시도했는데, 어느 시점엔 에러 메시지가 바뀌었다:

```text
New files were found. This might happen because a process is still writing to the target directory.
- C:\...\build\classes\java\main\com\asak
```

"파일이 잠겨서 못 지움"이 아니라 "**지우는 도중에 새 파일이 계속 생김**" — 즉 어떤 프로세스가
Gradle의 삭제 작업과 동시에 그 폴더에 계속 write하고 있었다는 뜻이다. 이게 위 4개 프로세스
중 VS Code Gradle 확장의 백그라운드 빌드 서버였던 것으로 보인다(죽이고 나니 이 메시지는
다시 안 나왔음).

### 실제로 통했던 방법

4개를 다 정리한 뒤에도 순수한 "Failed to delete some children"이 한 번 더 났다 — 즉 뭔가
아주 짧게(파일 인덱서 등이 새로 생긴 파일을 스캔하는 순간처럼) 핸들을 잡았다 놓는 게 계속
있었던 것으로 추정. 이럴 땐 Gradle이 재시도 없이 바로 실패해버리므로, **Gradle한테 지우게
시키지 말고 직접 지운 다음 바로 컴파일**하는 게 실질적으로 통했다.

```powershell
Remove-Item -Recurse -Force "C:\ASAK-workspace\ASAK-back\build" -ErrorAction SilentlyContinue
Test-Path "C:\ASAK-workspace\ASAK-back\build"   # False면 성공
```

```bash
./gradlew.bat compileJava --no-daemon
# BUILD SUCCESSFUL
```

### 이번 사례에서 얻은 교훈

- 위 "일반 해결 절차"의 1~4단계(재시도, clean 회피, 프로세스 하나씩 정리)만으론 부족할 수
  있다 — **동시에 여러 도구가 같은 폴더를 건드리고 있으면** 하나씩 죽여도 다른 하나가 여전히
  쓰고 있어서 실패가 반복된다. `Get-CimInstance Win32_Process`로 관련된 java 프로세스를
  **전부** 나열해서 하나씩 대조하는 게 낫다.
- "Failed to delete" 뒤에 붙는 부가 메시지("New files were found...")를 잘 보면 "잠김"과
  "동시 쓰기"를 구분할 수 있다 — 원인이 다르므로 대응도 다르다.
- Gradle의 자체 삭제 로직에 재시도 여유가 별로 없어 보이므로(핸들이 아주 짧게만 잡혀도
  실패), `Remove-Item -Recurse -Force`로 먼저 지우고 나서 Gradle을 돌리는 게 Gradle의
  내장 clean보다 실전에서 더 잘 통했다.
