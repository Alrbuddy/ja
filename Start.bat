@echo off

set "scriptpath=%~dp0"
set "supplementarypath=%scriptpath%\supplementary_commands"

:DELETE_CONFIRMATION
if exist "%scriptpath%\confirmation.txt" (
    del "%scriptpath%\confirmation.txt"
    goto START_SCRIPT
)

:START_SCRIPT
if exist "%supplementarypath%\STATUS.txt" (
    findstr /C:"RUN_NPM_UPDATE" "%supplementarypath%\STATUS.txt" >nul
    if not errorlevel 1 (
        echo "Adolf's Spoofer - Updating required NPM packages"
        cd /d "%supplementarypath%" && call npm i
    )
)

title Adolfs Spoofer

start /B python "%scriptpath%\main.py"

timeout /t 5 > nul

:WAIT_CONFIRMATION
if not exist "%scriptpath%\confirmation.txt" (
    timeout /t 5 > nul
    goto WAIT_CONFIRMATION
)

start /B node "%scriptpath%\Default.mjs"
