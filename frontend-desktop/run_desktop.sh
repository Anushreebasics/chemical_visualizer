#!/bin/bash

# Chemical Equipment Visualizer - Desktop App Launcher
# Uses Homebrew Python with PyQt5

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Use Homebrew's Python which has PyQt5 available
export PYTHONPATH="/opt/homebrew/lib/python3.11/site-packages:$PYTHONPATH"

# Run the desktop app
/opt/homebrew/bin/python3 main.py "$@"
