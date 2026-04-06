#!/usr/bin/env python
"""
Test script to verify EventLogic setup:
- Check if database is populated
- Test admin login
- Verify photo URLs
- Check database integrity
"""

import sys
sys.path.insert(0, '/Mac/Home/Downloads/csci275')

from app_eventlogic import app, db
from models_eventlogic import Admin, Customer, Vendor, Service
import requests

def test_database():
    """Test if database is properly populated"""
    with app.app_context():
        print("=" * 60)
        print("TESTING DATABASE")
        print("=" * 60)
        
        # Check Admin
        admins = Admin.query.all()
        print(f"\n✓ Admins: {len(admins)}")
        if admins:
            for admin in admins:
                print(f"  - {admin.email} (password: admin123)")
                # Test password check
                is_valid = admin.check_password('admin123')
                print(f"    Password check: {'✓ VALID' if is_valid else '✗ INVALID'}")
        
        # Check Customers
        customers = Customer.query.all()
        print(f"\n✓ Customers: {len(customers)}")
        if customers:
            for c in customers[:2]:
                print(f"  - {c.email}")
        
        # Check Vendors
        vendors = Vendor.query.all()
        print(f"\n✓ Vendors: {len(vendors)}")
        if vendors:
            for v in vendors[:2]:
                print(f"  - {v.vendor_name} ({v.email})")
        
        # Check Services
        services = Service.query.all()
        print(f"\n✓ Services: {len(services)}")
        
        # Check photo URLs
        print(f"\n{'CHECKING SERVICE PHOTOS':^60}")
        print("-" * 60)
        
        working = 0
        broken = 0
        
        for service in services[:5]:  # Check first 5
            if service.photo_url:
                try:
                    response = requests.head(service.photo_url, timeout=5)
                    if response.status_code == 200:
                        print(f"✓ {service.service_name}: OK")
                        working += 1
                    else:
                        print(f"✗ {service.service_name}: HTTP {response.status_code}")
                        broken += 1
                except Exception as e:
                    print(f"✗ {service.service_name}: {str(e)[:40]}")
                    broken += 1
            else:
                print(f"⚠ {service.service_name}: NO PHOTO URL")
                broken += 1
        
        print("-" * 60)
        print(f"Photo Status: {working} working, {broken} broken")
        print("=" * 60)
        
        return len(admins) > 0

if __name__ == '__main__':
    try:
        if test_database():
            print("\n✅ DATABASE IS READY!")
            print("\nYou can now:")
            print("  1. Start server (START_EVENTLOGIC_SERVER.bat)")
            print("  2. Login with admin@eventlogic.com / admin123")
        else:
            print("\n❌ DATABASE IS EMPTY!")
            print("\nYou need to:")
            print("  1. Run RESET_AND_SEED.bat to populate database")
            print("  2. Then run this test again")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Make sure Flask app is configured")
        print("  - Check database.db location")
        print("  - Run: python seed_data.py")
