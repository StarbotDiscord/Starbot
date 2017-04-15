@echo off

REM StarBot run script for Windows.

REM Get latest version and star bot.
echo Updating...
git pull
echo Starting bot...
python main.py

REM Loop back again.
goto start
