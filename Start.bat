@echo off

set "scriptpath=%~dp0"
set "publicpath=%scriptpath%Public"

:DELETE_CONFIRMATION
if exist "%scriptpath%confirmation.txt" (
    del "%scriptpath%confirmation.txt"
    goto START_SCRIPT
)

cd /d "%publicpath%"
node versioncheck.js

:START_SCRIPT
title Adolfs Spoofer

start /B python "%publicpath%\main.py"

timeout /t 5 > nul

:WAIT_CONFIRMATION
if not exist "%scriptpath%confirmation.txt" (
    timeout /t 5 > nul
    goto WAIT_CONFIRMATION
)

start /B node "%publicpath%\Default.mjs"
