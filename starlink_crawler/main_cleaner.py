#!/usr/bin/env python3
"""
Main entry point for the Starlink Markdown Cleaner UI.

This module provides a simple entry point to launch the interactive UI
for the markdown cleaner.
"""

import os
import sys

# Add the parent directory to the path to allow importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

# Now we can import from the package
from starlink_crawler.clean_markdown_ui import run_cleaner_ui

if __name__ == "__main__":
    run_cleaner_ui()
