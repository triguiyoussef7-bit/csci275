"""
DIAGNOSTIC SCRIPT - Check what's wrong with admin & photos
Run this to see what's happening
"""

import sys
import os
sys.path.insert(0, '/Mac/Home/Downloads/csci275')

try:
    from app_eventlogic import app, db
    from models_eventlogic import Admin, Customer, Vendor, Service
    
    print("=" * 70)
    print("EVENTLOGIC DIAGNOSTIC CHECK")
    print("=" * 70)
    
    with app.app_context():
        # Check 1: Database file exists
        db_path = '/Mac/Home/Downloads/csci275/eventlogic.db'
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"\n✓ DATABASE EXISTS: {db_path}")
            print(f"  Size: {size} bytes")
        else:
            print(f"\n✗ DATABASE MISSING: {db_path}")
            print("  RUN: DELETE_AND_SETUP.bat first!")
        
        # Check 2: Admin account exists
        print("\n" + "=" * 70)
        print("CHECKING ADMIN ACCOUNT")
        print("=" * 70)
        
        admins = Admin.query.all()
        print(f"\nAdmin accounts in database: {len(admins)}")
        
        if admins:
            for admin in admins:
                print(f"\n✓ Found admin:")
                print(f"  Email: {admin.email}")
                print(f"  ID: {admin.id}")
                
                # Test password
                is_valid = admin.check_password('admin123')
                if is_valid:
                    print(f"  Password 'admin123': ✓ CORRECT")
                else:
                    print(f"  Password 'admin123': ✗ WRONG")
        else:
            print(f"\n✗ NO ADMINS FOUND IN DATABASE!")
            print("  This is why login doesn't work!")
            print("  FIX: Run DELETE_AND_SETUP.bat")
        
        # Check 3: Other users
        print("\n" + "=" * 70)
        print("CHECKING OTHER ACCOUNTS")
        print("=" * 70)
        
        customers = Customer.query.all()
        vendors = Vendor.query.all()
        services = Service.query.all()
        
        print(f"\nCustomers: {len(customers)}")
        print(f"Vendors: {len(vendors)}")
        print(f"Services: {len(services)}")
        
        if len(customers) == 0 and len(vendors) == 0:
            print("\n⚠️  DATABASE IS EMPTY!")
            print("  FIX: Run DELETE_AND_SETUP.bat to populate")
        
        # Check 4: Service photos
        print("\n" + "=" * 70)
        print("CHECKING SERVICE PHOTOS")
        print("=" * 70)
        
        if services:
            print(f"\nFound {len(services)} services")
            working = 0
            missing = 0
            
            for service in services[:3]:
                if service.photo_url:
                    print(f"\n✓ {service.service_name}")
                    print(f"  Photo URL: {service.photo_url[:60]}...")
                    working += 1
                else:
                    print(f"\n✗ {service.service_name}")
                    print(f"  No photo URL!")
                    missing += 1
            
            print(f"\nPhoto Summary: {working} have URLs, {missing} missing")
        else:
            print("\n⚠️  NO SERVICES FOUND - Database is empty!")
        
        # Final diagnosis
        print("\n" + "=" * 70)
        print("DIAGNOSIS & FIX")
        print("=" * 70)
        
        if len(admins) == 0:
            print("\n❌ PROBLEM #1: No admin account!")
            print("   FIX: Run DELETE_AND_SETUP.bat")
            print("   This will create fresh database with admin account")
        else:
            print("\n✓ Admin account exists")
        
        if len(services) == 0:
            print("\n❌ PROBLEM #2: No services (photos won't show)")
            print("   FIX: Run DELETE_AND_SETUP.bat")
            print("   This will create 15 services with photos")
        else:
            print("\n✓ Services exist")
        
        if len(admins) > 0 and len(services) > 0:
            print("\n✓ DATABASE LOOKS GOOD!")
            print("   Problem might be browser cache or server issue")
            print("   Try:")
            print("   1. Refresh page (F5)")
            print("   2. Hard refresh (Ctrl+Shift+R)")
            print("   3. Clear browser cache")
            print("   4. Try different browser")
        
        print("\n" + "=" * 70)

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Make sure Flask is installed: pip install flask")
    print("2. Make sure you're in right directory")
    print("3. Try running: python -c 'import flask'")

print("\nPress any key to close...")
input()
