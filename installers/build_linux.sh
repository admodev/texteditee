#!/bin/bash
# Linux build script for TextEditee

echo "Building TextEditee for Linux..."

# Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build executable
cd installers
pyinstaller --clean --onefile build.pyinstaller

echo "Build complete! Executable is in dist/texteditee"

# Make executable
chmod +x dist/texteditee

# Optionally create DEB package
if command -v dpkg-deb &> /dev/null; then
    echo "Creating DEB package..."
    bash linux/build_deb.sh
else
    echo "dpkg-deb not found. Skipping DEB package creation."
fi

# Optionally create RPM package
if command -v rpmbuild &> /dev/null; then
    echo "Creating RPM package..."
    bash linux/build_rpm.sh
else
    echo "rpmbuild not found. Skipping RPM package creation."
fi
