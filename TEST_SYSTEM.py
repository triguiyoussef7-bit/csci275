#!/usr/bin/env python
"""
EventLogic Diagnostic Script
Tests if all components are working
"""

import sys
import os

print("=" * 70)
print("EventLogic Diagnostic Test")
print("=" * 70)
print()

# Test 1: Check Python version
print("[TEST 1] Python Version")
print(f"  Python: {sys.version}")
print(f"  ✓ OK")
print()

# Test 2: Check required packages
print("[TEST 2] Required Packages")
required_packages = {
    'flask': 'Flask',
    'flask_login': 'Flask-Login',
    'flask_sqlalchemy': 'Flask-SQLAlchemy',
    'sqlalchemy': 'SQLAlchemy'
}

missing = []
for module, name in required_packages.items():
    try:
        __import__(module)
        print(f"  ✓ {name} installed")
    except ImportError:
        print(f"  ✗ {name} NOT installed")
        missing.append(name)

if missing:
    print()
    print("MISSING PACKAGES! Install them:")
    print("  pip install Flask Flask-Login Flask-SQLAlchemy")
    sys.exit(1)
print()

# Test 3: Check files exist
print("[TEST 3] Project Files")
files_to_check = [
    'app_eventlogic.py',
    'models_eventlogic.py',
    'seed_data.py',
    'templates/login.html',
    'templates/customer_dashboard.html',
    'templates/customer_vendor_detail.html'
]

missing_files = []
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} MISSING")
        missing_files.append(file)

if missing_files:
    print()
    print("MISSING FILES! Create or restore them.")
    sys.exit(1)
print()

# Test 4: Try to import models
print("[TEST 4] Import Models")
try:
    from models_eventlogic import db, Customer, Vendor, Admin, Service
    print("  ✓ Models imported successfully")
except Exception as e:
    print(f"  ✗ ERROR importing models:")
    print(f"    {str(e)}")
    sys.exit(1)
print()

# Test 5: Try to import app
print("[TEST 5] Import Flask App")
try:
    from app_eventlogic import app
    print("  ✓ Flask app imported successfully")
except Exception as e:
    print(f"  ✗ ERROR importing app:")
    print(f"    {str(e)}")
    sys.exit(1)
print()

# Test 6: Try to create database
print("[TEST 6] Database Operations")
try:
    with app.app_context():
        db.create_all()
        customer_count = Customer.query.count()
        vendor_count = Vendor.query.count()
        print(f"  ✓ Database created")
        print(f"  ✓ Customers: {customer_count}")
        print(f"  ✓ Vendors: {vendor_count}")
except Exception as e:
    print(f"  ✗ ERROR with database:")
    print(f"    {str(e)}")
    sys.exit(1)
print()

# Summary
print("=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print()
print("Your EventLogic application is ready!")
print()
print("To start the server, run:")
print("  python app_eventlogic.py")
print()
print("Then visit:")
print("  http://localhost:5000")
print()
