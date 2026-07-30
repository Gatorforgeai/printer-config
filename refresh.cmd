@echo off
REM Capture current Cura printer config -> repo, vault table, Drive backup, GitHub.
REM Close Cura before running: it rewrites its config on exit.
python "%~dp0refresh.py" %*
echo.
pause
