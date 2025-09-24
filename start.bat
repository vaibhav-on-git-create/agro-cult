@echo off

REM Change directory to your project folder (edit as needed)
cd /d ../agro-cult

REM Create a virtual environment named "venv" if it doesn't exist
if not exist venv (
    python -m venv venv
)

REM Activate the virtual environment
call ../agro-cult/.venv/Scripts/activate.bat

REM Run the Python script (edit script name as needed)
python ../agro-cult/UI/MAINPAGE.py

REM Optional: Deactivate the virtual environment after run
deactivate

pause
