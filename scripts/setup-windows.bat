@echo off
REM ASAK Windows setup wrapper — 더블클릭 실행용
REM 관리자 권한 불필요 (winget 설치 시 UAC 팝업은 나올 수 있음)

setlocal
cd /d "%~dp0.."

echo.
echo ========================================
echo   ASAK Windows Setup
echo ========================================
echo.

where powershell >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell을 찾을 수 없습니다.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-windows.ps1" %*
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% equ 0 (
    echo Setup finished. See checklist above.
) else (
    echo Setup finished with warnings. See output above.
)
echo.
pause
exit /b %EXITCODE%
