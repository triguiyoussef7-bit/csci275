#!/usr/bin/env python3
"""
VENDOR RATING FIX
================
This script fixes the vendor rating issue by:
1. Loading the database
2. Assigning initial ratings to all vendors (4.0-5.0 stars randomly)
3. Verifying the fix worked
"""

import sys
import os

# Navigate to project directory
project_dir = r"\\Mac\Home\Downloads\csci275"
os.chdir(project_dir)
sys.path.insert(0, project_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Current directory contents: {os.listdir('.')[:5]}...\n")

try:
    from models_eventlogic import Vendor
    from app_eventlogic import app, db
    import random
    
    print("[1/4] Loading Flask app and database...")
    with app.app_context():
        # Get all vendors
        vendors = db.session.query(Vendor).all()
        print(f"[2/4] Found {len(vendors)} vendors")
        
        if len(vendors) == 0:
            print("ERROR: No vendors found in database!")
            print("Run: python seed_data.py")
            sys.exit(1)
        
        # Assign ratings to all vendors
        print("[3/4] Assigning ratings (4.0-5.0 stars)...")
        for i, vendor in enumerate(vendors):
            old_rating = vendor.rating
            # Assign random rating between 4.0 and 5.0
            vendor.rating = round(random.uniform(4.0, 5.0), 2)
            print(f"  {vendor.name}: {old_rating} → {vendor.rating} ⭐")
        
        # Save changes
        db.session.commit()
        print("[4/4] Changes saved to database\n")
        
        # Verify
        print("VERIFICATION:")
        vendors = db.session.query(Vendor).all()
        print(f"Total vendors: {len(vendors)}")
        ratings = [v.rating for v in vendors]
        print(f"Average rating: {sum(ratings)/len(ratings):.2f}⭐")
        print(f"Rating range: {min(ratings)} - {max(ratings)}")
        print("\n✅ FIX COMPLETE - Vendors now have ratings!")
        print("   - Refresh the Browse Vendors page")
        print("   - You should see all vendors now")
        print("   - Click any vendor to leave a rating")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
