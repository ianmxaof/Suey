@echo off
setlocal
set "SUEY_ROOT=%~dp0"
if not exist "C:\Python314\pythonw.exe" (
  echo Python 3.14 is missing from C:\Python314.
  pause
  exit /b 1
)
start "Suey" "C:\Python314\pythonw.exe" "%SUEY_ROOT%desktop_suey.pyw"
