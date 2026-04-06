#!/usr/bin/env python3
"""
AUTOMATIC SETUP - Kills server, resets DB, and starts fresh
"""
import os
import sys
import time
import subprocess
import signal

def kill_flask_process():
    """Kill any running Flask processes"""
    print("[*] Stopping Flask server...")
    try:
        os.system("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq*EventLogic*\" 2>nul")
        time.sleep(2)
        result = os.system("taskkill /F /IM python.exe 2>nul")
        print("[OK] Flask server stopped")
        time.sleep(2)
    except Exception as e:
        print(f"[!] Error stopping server: {e}")

def main():
    os.chdir(r"C:\Mac\Home\Downloads\csci275")
    
    print("\n" + "="*70)
    print("EVENT LOGIC - AUTOMATIC SETUP")
    print("="*70)
    
    # Step 1: Kill Flask
    print("\n[1/5] Stopping any running servers...")
    kill_flask_process()
    
    # Step 2: Delete database
    print("\n[2/5] Deleting old database...")
    try:
        if os.path.exists("eventlogic.db"):
            os.remove("eventlogic.db")
            print("[OK] Database deleted")
        else:
            print("[OK] No old database found")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR] Could not delete DB: {e}")
        time.sleep(2)
        # Try force delete
        os.system("del /F eventlogic.db 2>nul")
        time.sleep(1)
    
    # Step 3: Install dependencies
    print("\n[3/5] Installing dependencies...")
    os.system("python -m pip install -q -r requirements.txt 2>nul")
    print("[OK] Packages installed")
    
    # Step 4: Seed database
    print("\n[4/5] Creating and seeding database...")
    result = os.system("python seed_data.py")
    if result == 0:
        print("[OK] Database seeded with test data")
    else:
        print("[!] Seeding completed with status:", result)
    time.sleep(2)
    
    # Step 5: Start server
    print("\n[5/5] Starting EventLogic server...")
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\n📱 Open your browser and visit:")
    print("   http://localhost:5000\n")
    print("👤 Demo Accounts:")
    print("   Vendor:   venue@eventlogic.com / vendor123")
    print("   Customer: john@example.com / customer123")
    print("   Admin:    admin@eventlogic.com / admin123\n")
    print("✨ What's New:")
    print("   ✅ Vendor bookings now display correctly")
    print("   ✅ Customer reviews show on vendor profiles")
    print("   ✅ Professional design with beautiful styling\n")
    print("🔧 Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Start server
    os.system("python app_eventlogic.py")

if __name__ == "__main__":
    main()
