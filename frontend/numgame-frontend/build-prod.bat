@echo off
setlocal enabledelayedexpansion

REM ========================================
REM build-prod.bat - Build NumGame Frontend
REM ========================================
REM This script:
REM   1. Installs dependencies
REM   2. Builds the frontend locally
REM   3. Builds the production Docker image
REM
REM Usage:
REM   build-prod.bat
REM
REM Prerequisites:
REM   - Node.js 18+
REM   - Docker Desktop (running)
REM ========================================

echo ==========================================
echo   NumGame Frontend - Production Build
echo ==========================================
echo.

REM ---- Step 1: Install dependencies ----
echo [1/3] Installing dependencies...
call npm install
echo [OK] Dependencies installed
echo.

REM ---- Step 2: Build dist locally ----
echo [2/3] Building frontend (npm run build)...
call npm run build
echo [OK] Frontend built -^> dist/
echo.

REM ---- Step 3: Build Docker image ----
echo [3/3] Building Docker image...

REM Temporarily rename .dockerignore so dist/ is not excluded
if exist .dockerignore (
    ren .dockerignore .dockerignore.bak
)

docker build -f Dockerfile.prod -t numgame-frontend:prod .

REM Restore .dockerignore
if exist .dockerignore.bak (
    ren .dockerignore.bak .dockerignore
)
echo [OK] Docker image built: numgame-frontend:prod
echo.

echo ==========================================
echo   Build complete!
echo ==========================================
echo.
echo Next step:
echo   cd d:\PyLearn\NumGame
echo   docker compose up -d
echo.

endlocal