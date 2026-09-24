@echo off
title Push CardioGuard AI to GitHub
echo ========================================================
echo Pushing CardioGuard AI Project to GitHub (yp498205/MLproject)
echo ========================================================
echo.

cd /d "%~dp0"
"C:\Users\ADMIN\.local\git\cmd\git.exe" push -u origin main --force

echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Your project has been pushed successfully to GitHub!
    echo Check your repository at: https://github.com/yp498205/MLproject
) else (
    echo [NOTICE] If GitHub asked for authentication, please sign in with your GitHub account.
)

echo.
pause
