@echo off
REM EventLogic - AUTOMATIC COMPLETE SETUP
REM Bypass UNC path issues by using absolute paths

REM Use PUSHD to temporarily map the UNC path to a drive letter
pushd "\\mac\Home\Downloads\csci275" >nul 2>&1

if %errorlevel% equ 0 (
    python AUTOMATIC_COMPLETE.py
    popd
) else (
    REM If PUSHD fails, try running Python directly with absolute path
    python "\\mac\Home\Downloads\csci275\AUTOMATIC_COMPLETE.py"
)

pause

