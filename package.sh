#!/bin/bash

# TaskManager Distribution Package Script
# This script creates a distributable package for macOS

echo "TaskManager Distribution Package Script"
echo "======================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is for macOS only."
    exit 1
fi

# Check if taskmanager executable exists
if [ ! -f "./dist/taskmanager/taskmanager" ]; then
    echo "Error: TaskManager executable not found."
    echo "Please run 'pyinstaller --clean taskmanager.spec' first."
    exit 1
fi

# Create distribution directory
DIST_DIR="TaskManager-Distribution"
echo "Creating distribution package..."

# Clean up any existing distribution
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Copy the executable
cp -R ./dist/taskmanager "$DIST_DIR/"

# Copy installation script
cp install.sh "$DIST_DIR/"

# Copy README
cp README.md "$DIST_DIR/"

# Create a simple launcher script
cat > "$DIST_DIR/launch-taskmanager.sh" << 'EOF'
#!/bin/bash
# Simple launcher for TaskManager
cd "$(dirname "$0")"
./taskmanager/taskmanager
EOF

chmod +x "$DIST_DIR/launch-taskmanager.sh"

# Create a DMG creation script (optional)
cat > "$DIST_DIR/create-dmg.sh" << 'EOF'
#!/bin/bash
# Script to create a DMG file (requires hdiutil)

echo "Creating DMG file..."
hdiutil create -volname "TaskManager" -srcfolder . -ov -format UDZO TaskManager.dmg
echo "DMG file created: TaskManager.dmg"
EOF

chmod +x "$DIST_DIR/create-dmg.sh"

# Create a simple README for distribution
cat > "$DIST_DIR/DISTRIBUTION-README.txt" << 'EOF'
TaskManager for macOS
====================

This package contains a standalone TaskManager application that can run on any macOS system without requiring Python installation.

Contents:
- taskmanager/          - The main application folder
- install.sh           - Installation script (run with sudo)
- launch-taskmanager.sh - Simple launcher script
- create-dmg.sh        - Script to create a DMG file
- README.md            - Full documentation

Quick Start:
1. Run the installation script: sudo ./install.sh
2. Or simply run: ./launch-taskmanager.sh

The application will display all running processes in a grid format with real-time monitoring capabilities.

System Requirements:
- macOS 10.13 or later
- No Python installation required
- No additional dependencies needed

Note: On first run, you may need to allow the application in System Preferences > Security & Privacy.
EOF

echo "Distribution package created in: $DIST_DIR"
echo ""
echo "To distribute:"
echo "1. Copy the entire '$DIST_DIR' folder to other MacBooks"
echo "2. Run 'sudo ./install.sh' on the target machine"
echo "3. Or run './launch-taskmanager.sh' directly"
echo ""
echo "Optional: Create a DMG file by running './create-dmg.sh' in the distribution folder" 