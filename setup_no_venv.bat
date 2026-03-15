@echo off
echo ====================================================================
echo POLYMARKET SNIPER BOT - SETUP WITHOUT VIRTUAL ENVIRONMENT
echo ====================================================================
echo.
echo WARNING: This will install packages to your system Python
echo Only use this if virtual environment creation fails
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" exit /b 0

echo.
echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

echo.
echo [2/4] Upgrading pip (corporate network mode)...
python -m pip install --upgrade pip ^
    --trusted-host pypi.org ^
    --trusted-host pypi.python.org ^
    --trusted-host files.pythonhosted.org ^
    --disable-pip-version-check

echo.
echo [3/4] Installing dependencies (corporate network mode)...
pip install ^
    --trusted-host pypi.org ^
    --trusted-host pypi.python.org ^
    --trusted-host files.pythonhosted.org ^
    --user ^
    -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)

echo.
echo [4/4] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env file
)

if not exist data mkdir data
if not exist logs mkdir logs

echo.
echo ====================================================================
echo SETUP COMPLETE (System Python Installation)
echo ====================================================================
echo.
echo NEXT STEPS:
echo 1. Edit .env file and add your PRIVATE_KEY
echo 2. Run: python test_setup.py
echo 3. Run: python run.py
echo.
echo ====================================================================
pause
