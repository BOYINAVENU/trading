@echo off
echo ====================================================================
echo POLYGON RPC FIX - Update to Working Endpoint
echo ====================================================================
echo.
echo Current RPC in .env: https://polygon-rpc.com
echo This endpoint may be down or blocked by your network
echo.
echo Available options:
echo 1. Ankr (Public, Fast, Reliable)
echo 2. Alchemy Demo (Very Fast)
echo 3. Chainstack (Public, Reliable)
echo 4. Keep current
echo.
set /p choice="Choose option (1-4): "

if "%choice%"=="1" (
    set NEW_RPC=https://rpc.ankr.com/polygon
    echo Selected: Ankr
)
if "%choice%"=="2" (
    set NEW_RPC=https://polygon-mainnet.g.alchemy.com/v2/demo
    echo Selected: Alchemy Demo
)
if "%choice%"=="3" (
    set NEW_RPC=https://polygon-mainnet.public.blastapi.io
    echo Selected: Chainstack
)
if "%choice%"=="4" (
    echo Keeping current RPC
    pause
    exit /b 0
)

echo.
echo Updating .env file...

REM Backup .env
copy .env .env.backup >nul 2>&1

REM Update RPC URL using PowerShell
powershell -Command "(Get-Content .env) -replace 'POLYGON_RPC_URL=.*', 'POLYGON_RPC_URL=%NEW_RPC%' | Set-Content .env"

if errorlevel 1 (
    echo [ERROR] Failed to update .env
    echo Please manually edit .env and change POLYGON_RPC_URL
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Updated POLYGON_RPC_URL to: %NEW_RPC%
echo.
echo Testing connection...
echo.

REM Activate venv and test
call venv\Scripts\activate.bat
python test_setup.py

echo.
pause
