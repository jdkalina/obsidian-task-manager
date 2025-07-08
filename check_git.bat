@echo off
echo Checking if Git is installed...
git --version
if %errorlevel% equ 0 (
    echo Git is already installed!
) else (
    echo Git is not installed. Please download from: https://git-scm.com/download/
    start https://git-scm.com/download/
)
pause
