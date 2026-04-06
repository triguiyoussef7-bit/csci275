#!/usr/bin/env python3
"""
EventLogic - Direct Runner (bypasses network path issues)
Run this directly: python RUN_NOW.py
"""

import os
import sys
import subprocess
import time
import shutil

# Get actual path
project_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Project directory: {project_dir}")

# Change to project directory
os.chdir(project_dir)

print("\n" + "="*80)
print("EventLogic - SYSTEM STARTUP")
print("="*80 + "\n")

# Step 1
print("[1/4] Stopping any running servers...")
os.system('taskkill /F /IM python.exe 2>nul')
time.sleep(1)

# Step 2
print("[2/4] Cleaning database...")
if os.path.exists('eventlogic.db'):
    os.remove('eventlogic.db')
    print("  ✓ Old database removed")

# Step 3
print("[3/4] Creating fresh database...")
try:
    result = subprocess.run([sys.executable, 'seed_data.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ Database created successfully")
        print(result.stdout)
    else:
        print("  ✗ ERROR creating database:")
        print(result.stderr)
except Exception as e:
    print(f"  ✗ ERROR: {e}")

# Step 4
print("\n" + "="*80)
print("✅ STARTING SERVER")
print("="*80)
print("\nServer will run at: http://localhost:5000")
print("\nLOGIN WITH:")
print("  Email:    admin@eventlogic.com")
print("  Password: admin123")
print("  Role:     Admin")
print("\n" + "="*80 + "\n")

# Start server
try:
    from app_eventlogic import app
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=False)
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
