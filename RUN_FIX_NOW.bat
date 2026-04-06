@echo off
REM Use PUSHD to handle UNC paths
pushd "C:\Mac\Home\Downloads\csci275"
python START_FIX.py
popd
pause
