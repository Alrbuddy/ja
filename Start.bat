@echo off

set "scriptpath=%~dp0"
set "publicpath=%scriptpath%Public"

:DELETE_CONFIRMATION_PUBLIC
if exist "%publicpath%\confirmation.txt" (
    del "%publicpath%\confirmation.txt"
    goto START_SCRIPT
)

cd /d "%publicpath%"
node versioncheck.js

:START_SCRIPT
title Adolfs Spoofer

start /B python "%publicpath%\main.py"

timeout /t 5 > nul

:WAIT_CONFIRMATION
if not exist "%publicpath%\confirmation.txt" (
    timeout /t 5 > nul
    goto WAIT_CONFIRMATION
)

start /B node "%publicpath%\Default.mjs"
