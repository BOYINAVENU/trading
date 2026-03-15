@echo off
REM Quick install script for corporate networks
REM Use this if setup.bat failed due to SSL errors

echo Installing Python packages with corporate network SSL workaround...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install with trusted host flags
pip install ^
    --trusted-host pypi.org ^
    --trusted-host pypi.python.org ^
    --trusted-host files.pythonhosted.org ^
    --disable-pip-version-check ^
    -r requirements.txt

if errorlevel 1 (
    echo.
    echo Installation failed. See CORPORATE_NETWORK_FIX.md for more solutions.
    pause
    exit /b 1
) else (
    echo.
    echo Installation successful!
    echo.
    echo Run: python test_setup.py
    pause
)
