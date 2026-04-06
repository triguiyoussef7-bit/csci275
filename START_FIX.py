#!/usr/bin/env python3
"""
EventLogic - Diagnostic and Recovery Script
Shows actual errors instead of silently failing
"""

import os
import sys
import subprocess
import time

os.chdir(r'C:\Mac\Home\Downloads\csci275')

print("\n" + "="*80)
print("EventLogic - DIAGNOSTIC & RECOVERY")
print("="*80 + "\n")

# Step 1: Kill processes
print("[STEP 1] Killing running Python processes...")
os.system('taskkill /F /IM python.exe 2>nul')
time.sleep(2)
print("✓ Done\n")

# Step 2: Delete database
print("[STEP 2] Deleting old database...")
if os.path.exists('eventlogic.db'):
    os.remove('eventlogic.db')
    print("✓ Deleted eventlogic.db\n")
else:
    print("✓ No old database found\n")

# Step 3: Install dependencies
print("[STEP 3] Installing dependencies...")
subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask', 'flask-login', 'flask-sqlalchemy', '-q'], check=False)
print("✓ Dependencies installed\n")

# Step 4: Seed database
print("[STEP 4] Creating database with test data...")
try:
    result = subprocess.run([sys.executable, 'seed_data.py'], capture_output=True, text=True, timeout=30)
    print(result.stdout)
    if result.returncode != 0:
        print("ERROR in seed_data.py:")
        print(result.stderr)
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# Step 5: Verify admin
print("[STEP 5] Verifying admin account...")
try:
    from app_eventlogic import app, db
    from models_eventlogic import Admin
    
    with app.app_context():
        admin = Admin.query.filter_by(email='admin@eventlogic.com').first()
        if admin:
            print("✓ Admin account verified\n")
        else:
            print("✗ ERROR: Admin account not found!\n")
            sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}\n")
    sys.exit(1)

# Step 6: Start server
print("="*80)
print("✅ ALL SYSTEMS READY - STARTING SERVER")
print("="*80)
print()
print("Server will start at: http://localhost:5000")
print()
print("LOGIN CREDENTIALS:")
print("─" * 80)
print("Email:    admin@eventlogic.com")
print("Password: admin123")
print("Role:     Admin")
print()
print("If you see errors below, copy them and send them to me.")
print("="*80)
print()

# Start Flask
try:
    from app_eventlogic import app
    app.run(host='0.0.0.0', port=5000, debug=False)
except Exception as e:
    print(f"\n\n❌ ERROR STARTING SERVER:\n{e}\n")
    import traceback
    traceback.print_exc()
    input("Press Enter to close...")
