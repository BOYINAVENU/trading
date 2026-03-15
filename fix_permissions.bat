@echo off
echo ====================================================================
echo PERMISSION FIX - Removing locked virtual environment
echo ====================================================================
echo.

REM Check if venv exists
if exist venv (
    echo Found existing venv folder - attempting to remove...
    
    REM Try to remove read-only attributes
    attrib -r -s -h venv\*.* /s /d
    
    REM Force remove the directory
    rmdir /s /q venv
    
    if exist venv (
        echo [WARNING] Could not remove venv folder automatically
        echo.
        echo Please manually delete the venv folder:
        echo 1. Close all Python processes and terminals
        echo 2. Delete C:\Users\AL55582\CascadeProjects\polymarket-sniper\venv
        echo 3. Run this script again
        pause
        exit /b 1
    ) else (
        echo [SUCCESS] Removed existing venv folder
    )
) else (
    echo No existing venv folder found
)

echo.
echo Creating fresh virtual environment...
python -m venv venv

if errorlevel 1 (
    echo.
    echo [ERROR] Still cannot create virtual environment
    echo.
    echo TROUBLESHOOTING OPTIONS:
    echo.
    echo 1. Run Command Prompt as Administrator
    echo    Right-click Command Prompt -^> Run as administrator
    echo    Then run: setup_corporate.bat
    echo.
    echo 2. Disable antivirus temporarily
    echo    Some antivirus software blocks venv creation
    echo.
    echo 3. Use alternative installation (see TROUBLESHOOTING.md)
    echo.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Virtual environment created!
echo.
echo Next step: Run setup_corporate.bat to install dependencies
pause
