#!/usr/bin/env python3
"""
EventLogic - DIAGNOSTIC VERSION (Shows all errors)
"""

import os
import sys
import subprocess
import time

print("\n" + "="*80)
print("EventLogic - DIAGNOSTIC MODE")
print("="*80 + "\n")

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print()

# Find project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Project directory: {project_dir}")
print()

# Change directory
try:
    os.chdir(project_dir)
    print(f"✓ Changed to: {os.getcwd()}")
except Exception as e:
    print(f"✗ Cannot change directory: {e}")
    sys.exit(1)

print()

# STEP 1: Kill Python
print("[1/5] Killing Python processes...")
try:
    subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                  capture_output=True, timeout=5)
    print("✓ Done")
except Exception as e:
    print(f"⚠ {e}")
time.sleep(2)

print()

# STEP 2: Delete database
print("[2/5] Removing old database...")
try:
    if os.path.exists('eventlogic.db'):
        os.remove('eventlogic.db')
        print("✓ Deleted")
    else:
        print("✓ No database found")
except Exception as e:
    print(f"✗ {e}")

print()

# STEP 3: Install dependencies
print("[3/5] Installing dependencies...")
try:
    result = subprocess.run([sys.executable, '-m', 'pip', 'install',
                           'flask', 'flask-login', 'flask-sqlalchemy', '-q'],
                          capture_output=True, timeout=60)
    if result.returncode == 0:
        print("✓ Installed")
    else:
        print(f"⚠ Some warnings (continuing anyway)")
except Exception as e:
    print(f"⚠ {e}")

print()

# STEP 4: Seed database
print("[4/5] Creating database...")
try:
    result = subprocess.run([sys.executable, 'seed_data.py'],
                          capture_output=True, text=True, timeout=30)
    print(result.stdout)
    if result.returncode != 0:
        print(f"✗ ERROR: {result.stderr}")
        input("Press Enter to exit...")
        sys.exit(1)
except Exception as e:
    print(f"✗ ERROR: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

print()
print("="*80)
print("✅ STARTING SERVER AT http://localhost:5000")
print("="*80)
print()
print("Login with:")
print("  Email:    admin@eventlogic.com")
print("  Password: admin123")
print()

# STEP 5: Start server
print("[5/5] Starting Flask server...")
print()

try:
    # Import and run app
    from app_eventlogic import app
    print("✓ App imported successfully")
    print()
    print("Server running on: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
except ImportError as e:
    print(f"✗ IMPORT ERROR: {e}")
    print()
    print("This usually means:")
    print("  1. Flask is not installed")
    print("  2. models_eventlogic.py is missing")
    print("  3. app_eventlogic.py has syntax errors")
    print()
    input("Press Enter to exit...")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print()
    input("Press Enter to exit...")
    sys.exit(1)

