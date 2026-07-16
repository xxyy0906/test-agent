@echo off
REM Windows 一键启动 NTCIP SNMP Agent
REM 用法:
REM   start_windows.bat
REM   start_windows.bat --port 161
REM   start_windows.bat --full
REM   start_windows.bat --dev-cap 16
REM   start_windows.bat -- --verbose
REM
REM 默认: --port 1161 --dev-cap 8
REM 端口 161 需「以管理员身份运行」本脚本。

setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PORT=1161"
set "DEV_CAP=8"
set "FULL=0"
set "EXTRA="

:parse
if "%~1"=="" goto after_parse
if /I "%~1"=="-h" goto show_help
if /I "%~1"=="--help" goto show_help
if /I "%~1"=="--port" (
  if "%~2"=="" (
    echo ERROR: --port requires a value
    exit /b 1
  )
  set "PORT=%~2"
  shift
  shift
  goto parse
)
if /I "%~1"=="--dev-cap" (
  if "%~2"=="" (
    echo ERROR: --dev-cap requires a value
    exit /b 1
  )
  set "DEV_CAP=%~2"
  shift
  shift
  goto parse
)
if /I "%~1"=="--full" (
  set "FULL=1"
  shift
  goto parse
)
if "%~1"=="--" (
  shift
  goto collect_rest
)
set "EXTRA=!EXTRA! %~1"
shift
goto parse

:collect_rest
if "%~1"=="" goto after_parse
set "EXTRA=!EXTRA! %~1"
shift
goto collect_rest

:after_parse

set "PYTHON="
if exist "%~dp0.venv\Scripts\python.exe" set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not defined PYTHON (
  where py >nul 2>&1 && set "PYTHON=py"
)
if not defined PYTHON (
  where python >nul 2>&1 && set "PYTHON=python"
)
if not defined PYTHON (
  echo ERROR: No Python found. Create .venv or install Python launcher "py".
  echo   py -m venv .venv
  echo   .venv\Scripts\activate
  echo   python -m pip install -r requirements.txt
  exit /b 1
)

set "ARGS=agent.py --port %PORT%"
if "%FULL%"=="0" set "ARGS=%ARGS% --dev-cap %DEV_CAP%"
if defined EXTRA set "ARGS=%ARGS%%EXTRA%"

echo Working directory: %CD%
echo Python: %PYTHON%
echo Command: %PYTHON% %ARGS%

if %PORT% LSS 1024 (
  echo Port %PORT% is privileged. If bind fails, re-run this script as Administrator.
)

"%PYTHON%" %ARGS%
exit /b %ERRORLEVEL%

:show_help
echo Usage: start_windows.bat [options] [-- agent.py args...]
echo.
echo Options:
echo   --port N       UDP port (default: 1161^)
echo   --dev-cap N    Table dimension cap (default: 8^). Ignored with --full.
echo   --full         Full OID fill (no --dev-cap^)
echo   -h, --help     Show this help.
echo.
echo Examples:
echo   start_windows.bat
echo   start_windows.bat --port 161
echo   start_windows.bat --full
echo   start_windows.bat -- --verbose
exit /b 0
