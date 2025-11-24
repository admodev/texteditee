#!/bin/bash
# macOS build script for TextEditee

echo "Building TextEditee for macOS..."

# Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build executable
cd installers
pyinstaller --clean --onefile build.pyinstaller

echo "Build complete! Executable is in dist/texteditee"

# Make executable
chmod +x dist/texteditee

# Optionally create DMG
if command -v hdiutil &> /dev/null; then
    echo "Creating DMG package..."
    bash macos/build_dmg.sh
else
    echo "hdiutil not found. Skipping DMG creation."
fi
