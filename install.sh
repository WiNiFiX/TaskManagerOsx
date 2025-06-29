#!/bin/bash

# TaskManager Installation Script for macOS
# This script installs the TaskManager application to /Applications

echo "TaskManager Installation Script"
echo "================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This installer is for macOS only."
    exit 1
fi

# Check if taskmanager executable exists
if [ ! -f "./dist/taskmanager/taskmanager" ]; then
    echo "Error: TaskManager executable not found."
    echo "Please run 'pyinstaller --clean taskmanager.spec' first."
    exit 1
fi

echo "Installing TaskManager to /Applications..."

# Create Applications directory if it doesn't exist
sudo mkdir -p /Applications

# Copy the taskmanager directory to Applications
sudo cp -R ./dist/taskmanager /Applications/

# Set proper permissions
sudo chmod +x /Applications/taskmanager/taskmanager
sudo chown -R root:wheel /Applications/taskmanager

echo "Installation complete!"
echo ""
echo "You can now run TaskManager by:"
echo "1. Opening Finder"
echo "2. Going to Applications"
echo "3. Double-clicking on 'taskmanager'"
echo ""
echo "Or from Terminal:"
echo "open /Applications/taskmanager/taskmanager"
echo ""
echo "Note: You may need to allow the application in System Preferences > Security & Privacy"
echo "if you get a security warning on first run." 