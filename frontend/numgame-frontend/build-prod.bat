@echo off
setlocal enabledelayedexpansion

REM ========================================
REM build-prod.bat - Build NumGame Frontend
REM ========================================
REM This script installs dependencies and builds dist/.
REM
REM Usage:
REM   build-prod.bat
REM
REM Prerequisites:
REM   - Node.js 18+
REM ========================================

echo ==========================================
echo   NumGame Frontend - Production Build
echo ==========================================
echo.

REM ---- Step 1: Install dependencies ----
echo [1/2] Installing dependencies...
call npm install
echo [OK] Dependencies installed
echo.

REM ---- Step 2: Build dist/ ----
echo [2/2] Building frontend (npm run build)...
call npm run build
echo [OK] Frontend built -^> dist/
echo.

echo ==========================================
echo   Build complete!
echo ==========================================
echo.
echo Next step:
echo   cd d:\PyLearn\NumGame
echo   docker compose build numgame-frontend
echo.

endlocal