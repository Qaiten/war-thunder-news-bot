@echo off
cd %~dp0
echo Activating virtual environment...
call venv\Scripts\activate
echo Running bot...
python WTNewsCheck.py
echo.
pause
