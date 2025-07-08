@echo off
echo ========================================
echo        Task Management Scripts
echo ========================================
echo.

cd /d "C:\Users\jdkal\projects"

echo Running Task Tracker...
python task_tracker.py

echo.
echo Running Task Logger...
python task_logger.py

echo.
echo ========================================
echo Both scripts completed!
echo Press any key to exit...
pause >nul
