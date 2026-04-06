#!/usr/bin/env python
"""
Setup script - Creates necessary directories and initializes the Event Planner app
"""

import os
import sys

def setup():
    """Create necessary directories"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    dirs_to_create = [
        os.path.join(base_dir, 'templates'),
        os.path.join(base_dir, 'static'),
    ]
    
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    print("\nSetup complete! You can now run: python app.py")

if __name__ == '__main__':
    setup()
