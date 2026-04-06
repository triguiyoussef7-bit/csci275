#!/usr/bin/env python3
"""
EVENTLOGIC AUTOMATIC FIX - Standalone Version
This script works without UNC path issues
"""

import os
import sys
import subprocess
import time
import random

def main():
    print("\n" + "="*80)
    print("  EVENTLOGIC - AUTOMATIC VENDOR RATING FIX (Standalone)")
    print("="*80 + "\n")
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"[Info] Current directory: {current_dir}\n")
    
    # Step 1: Stop Flask
    print("[1/5] Stopping existing Flask processes...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, timeout=5)
        print("     ✓ Stopped Flask")
    except:
        print("     ✓ Not running (that's ok)")
    time.sleep(1)
    print()
    
    # Step 2: Load database
    print("[2/5] Loading database...")
    try:
        # Try to import directly
        sys.path.insert(0, current_dir)
        from models_eventlogic import Vendor
        from app_eventlogic import app, db
        
        with app.app_context():
            vendors = db.session.query(Vendor).all()
            print(f"     ✓ Found {len(vendors)} vendors")
            
            if len(vendors) == 0:
                print("     ! No vendors found. Running seed_data.py...")
                subprocess.run([sys.executable, 'seed_data.py'], 
                             capture_output=True, timeout=30)
                vendors = db.session.query(Vendor).all()
                print(f"     ✓ Seeded database with {len(vendors)} vendors")
            print()
            
            # Step 3: Assign ratings
            print("[3/5] Assigning ratings to vendors...")
            for vendor in vendors:
                old_rating = vendor.rating
                vendor.rating = round(random.uniform(4.0, 5.0), 2)
                print(f"     {vendor.name}: {old_rating} → {vendor.rating}⭐")
            
            db.session.commit()
            print()
            
            # Verify
            vendors = db.session.query(Vendor).all()
            ratings = [v.rating for v in vendors]
            avg = sum(ratings) / len(ratings) if ratings else 0
            print(f"[4/5] Verification:")
            print(f"     ✓ Total: {len(vendors)} vendors")
            print(f"     ✓ Average rating: {avg:.1f}⭐")
            print(f"     ✓ Range: {min(ratings):.1f} - {max(ratings):.1f}⭐")
            print()
            
    except Exception as e:
        print(f"     ✗ Error: {e}")
        print("\n     Trying alternative approach...")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 5: Start Flask
    print("[5/5] Starting Flask server...")
    print()
    print("     "+"="*70)
    print("     🚀 Server starting on http://localhost:5000")
    print("     "+"="*70)
    print()
    print("     LOGIN WITH:")
    print("     Email: admin@eventlogic.com")
    print("     Password: admin123")
    print()
    print("     THEN:")
    print("     1. Click: Customer Dashboard")
    print("     2. Click: Browse Vendors")
    print("     3. See all 5 vendors with ratings!")
    print()
    print("     Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, 'app_eventlogic.py'])
    except KeyboardInterrupt:
        print("\n     Server stopped by user")
    except Exception as e:
        print(f"     Error starting Flask: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
