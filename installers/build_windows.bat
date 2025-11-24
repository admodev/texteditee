@echo off
REM Windows build script for TextEditee

echo Building TextEditee for Windows...

REM Install dependencies
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Build executable
echo Running PyInstaller...
python -m PyInstaller --clean --onefile --name texteditee src\texteditee\main.py

REM Check if build succeeded
if not exist "dist\texteditee.exe" (
    echo ERROR: PyInstaller failed to create executable!
    pause
    exit /b 1
)

echo Executable created successfully: dist\texteditee.exe

REM Create installer with NSIS (if available)
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    echo Creating Windows installer...
    "C:\Program Files (x86)\NSIS\makensis.exe" installers\windows\installer.nsi
) else (
    echo NSIS not found. Skipping installer creation.
    echo Install NSIS from https://nsis.sourceforge.io/ to create installers.
)

echo.
echo Build complete!
echo Executable: dist\texteditee.exe
if exist "dist\TextEditee-Setup.exe" (
    echo Installer: dist\TextEditee-Setup.exe
)
pause
