@echo off
echo ====================================================================
echo Installing Dependencies Only (venv already exists)
echo ====================================================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing packages with corporate network SSL workaround...
pip install ^
    --trusted-host pypi.org ^
    --trusted-host pypi.python.org ^
    --trusted-host files.pythonhosted.org ^
    --disable-pip-version-check ^
    -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed
    echo Check the error message above
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo SUCCESS! All dependencies installed
echo ====================================================================
echo.
echo Next steps:
echo 1. Edit .env file (copy from .env.example if needed)
echo 2. Add your PRIVATE_KEY
echo 3. Run: python test_setup.py
echo.
pause
