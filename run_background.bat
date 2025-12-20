@echo off
title Mira Bot - Background Runner

REM Run Python script in background (minimized)
start /min python main.py

echo Mira Bot is now running in the background!
echo The bot will continue running even if you close this window.
echo.
echo To stop the bot, open Task Manager and end the Python process.
echo.
pause
