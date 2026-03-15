@echo off
echo ====================================================================
echo POLYMARKET SNIPER BOT - WINDOWS QUICK SETUP
echo ====================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Python detected
python --version

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...

REM Remove existing venv if it exists (prevents permission errors)
if exist venv (
    echo Removing existing venv folder...
    rmdir /s /q venv >nul 2>&1
)

python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo.
    echo TROUBLESHOOTING:
    echo 1. Run fix_permissions.bat to clean up
    echo 2. Try running as Administrator
    echo 3. Corporate network? Use setup_corporate.bat
    echo 4. Alternative: setup_no_venv.bat
    echo.
    echo See TROUBLESHOOTING.md for more solutions
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo.
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Copy .env.example to .env if it doesn't exist
echo.
echo [4/5] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo [IMPORTANT] Edit .env file and add your PRIVATE_KEY before running!
) else (
    echo .env file already exists
)

REM Create data and logs directories
if not exist data mkdir data
if not exist logs mkdir logs

REM Run setup test
echo.
echo [5/5] Running setup verification...
python test_setup.py

echo.
echo ====================================================================
echo SETUP COMPLETE!
echo ====================================================================
echo.
echo NEXT STEPS:
echo 1. Edit .env file and add your Ethereum private key
echo 2. Fund your wallet with USDC on Polygon network
echo 3. Run: python test_setup.py (to verify everything works)
echo 4. Run: python run.py (to start the bot)
echo.
echo ====================================================================
pause
