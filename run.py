#!/usr/bin/env python3
"""
Simple runner script for the Python GUI Application
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main
    print("Starting Python GUI Application...")
    main()
except ImportError as e:
    print(f"Error importing main module: {e}")
    print("Make sure main.py exists in the current directory.")
    sys.exit(1)
except Exception as e:
    print(f"Error running application: {e}")
    sys.exit(1) 