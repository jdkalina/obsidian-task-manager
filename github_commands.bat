@echo off
echo ========================================
echo    GitHub Backup Instructions
echo ========================================
echo.
echo This file contains the Git commands you need to run.
echo Copy and paste these commands into Command Prompt or Git Bash.
echo.
echo 1. Navigate to your project directory:
echo    cd "C:\Users\jdkal\projects"
echo.
echo 2. Initialize Git repository:
echo    git init
echo.
echo 3. Configure Git (replace with your info):
echo    git config user.name "Your Name"
echo    git config user.email "your.email@example.com"
echo.
echo 4. Add all files:
echo    git add .
echo.
echo 5. Create first commit:
echo    git commit -m "Initial commit: Obsidian Task Manager"
echo.
echo 6. Connect to GitHub (replace 'yourusername' and 'repository-name'):
echo    git remote add origin https://github.com/yourusername/repository-name.git
echo.
echo 7. Push to GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
echo Press any key to exit...
pause >nul
