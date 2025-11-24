@echo off
REM Windows build script for TextEditee

echo Building TextEditee for Windows...

REM Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
cd installers
pyinstaller --clean --onefile build.pyinstaller

REM Create installer with NSIS (if available)
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    echo Creating Windows installer...
    "C:\Program Files (x86)\NSIS\makensis.exe" windows\installer.nsi
) else (
    echo NSIS not found. Skipping installer creation.
    echo Install NSIS from https://nsis.sourceforge.io/ to create installers.
)

echo Build complete! Executable is in dist\texteditee.exe
pause
