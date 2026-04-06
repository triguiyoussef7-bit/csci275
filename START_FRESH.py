#!/usr/bin/env python3
"""
AUTO SETUP AND RUN - EventLogic
Resets database, seeds data, and starts server
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    print(f"\n{'='*60}")
    print(f"[*] {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    result = os.system(cmd)
    if result != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Success: {description}")
    return True

def main():
    print("\n" + "="*60)
    print("EventLogic - Auto Setup & Run")
    print("="*60)
    
    os.chdir(r"C:\Mac\Home\Downloads\csci275")
    
    # Step 1: Delete old database
    print("\n[1/4] Deleting old database...")
    if os.path.exists("eventlogic.db"):
        os.remove("eventlogic.db")
        print("✅ Database deleted")
    else:
        print("ℹ️  No old database found")
    
    # Step 2: Install dependencies
    print("\n[2/4] Installing dependencies...")
    run_command("python -m pip install -q -r requirements.txt", "Installing packages")
    
    # Step 3: Seed database
    print("\n[3/4] Seeding database with test data...")
    run_command("python seed_data.py", "Seeding database")
    
    # Step 4: Start server
    print("\n[4/4] Starting server...")
    print("\n" + "="*60)
    print("✅ Setup complete! Starting EventLogic server...")
    print("="*60)
    print("\n📱 Open your browser and visit:")
    print("   http://localhost:5000")
    print("\n👤 Demo Accounts:")
    print("   Vendor:   venue@eventlogic.com / vendor123")
    print("   Customer: john@example.com / customer123")
    print("   Admin:    admin@eventlogic.com / admin123")
    print("\n🔧 Press Ctrl+C to stop the server")
    print("\n" + "="*60 + "\n")
    
    os.system("python app_eventlogic.py")

if __name__ == "__main__":
    main()
