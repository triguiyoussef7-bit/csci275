"""
EventLogic v2.0 - System Verification Script
Checks all new features are properly installed
"""
import sys
import os

sys.path.insert(0, 'C:\\Mac\\Home\\Downloads\\csci275')

def check_models():
    """Check if Review model exists"""
    try:
        from models_eventlogic import Review
        print("[OK] Review model found in models_eventlogic.py")
        return True
    except ImportError:
        print("[ERROR] Review model NOT found")
        return False

def check_routes():
    """Check if new routes exist in app"""
    try:
        with open('C:\\Mac\\Home\\Downloads\\csci275\\app_eventlogic.py', 'r') as f:
            content = f.read()
            
            routes_to_check = [
                '@app.route(\'/customer/activity\'',
                '@app.route(\'/customer/booking/<int:booking_id>/review\'',
                '@app.route(\'/vendor/<int:vendor_id>/reviews\'',
                '@app.route(\'/vendor/analytics\'',
                '@app.route(\'/admin/dashboard\''
            ]
            
            missing = []
            for route in routes_to_check:
                if route not in content:
                    missing.append(route)
            
            if missing:
                print(f"[ERROR] Missing routes:")
                for route in missing:
                    print(f"  - {route}")
                return False
            else:
                print("[OK] All 5 new routes found in app_eventlogic.py")
                return True
    except Exception as e:
        print(f"[ERROR] Could not check routes: {e}")
        return False

def check_templates():
    """Check if new templates exist"""
    templates = [
        'customer_review.html',
        'customer_activity.html',
        'vendor_reviews.html',
        'vendor_analytics.html',
        'admin_dashboard_full.html'
    ]
    
    template_dir = 'C:\\Mac\\Home\\Downloads\\csci275\\templates'
    missing = []
    
    for template in templates:
        path = os.path.join(template_dir, template)
        if not os.path.exists(path):
            missing.append(template)
    
    if missing:
        print(f"[ERROR] Missing templates:")
        for template in missing:
            print(f"  - {template}")
        return False
    else:
        print(f"[OK] All 5 new templates found in templates/")
        return True

def check_seed_script():
    """Check if seed script exists"""
    seed_file = 'C:\\Mac\\Home\\Downloads\\csci275\\seed_data.py'
    seed_bat = 'C:\\Mac\\Home\\Downloads\\csci275\\SEED_DATA.bat'
    
    if not os.path.exists(seed_file):
        print("[ERROR] seed_data.py not found")
        return False
    
    if not os.path.exists(seed_bat):
        print("[ERROR] SEED_DATA.bat not found")
        return False
    
    print("[OK] seed_data.py and SEED_DATA.bat found")
    return True

def check_documentation():
    """Check if documentation exists"""
    docs = [
        'FEATURES_NEW.md',
        'QUICKSTART_V2.md',
        'COMPLETE_FEATURES.md'
    ]
    
    doc_dir = 'C:\\Mac\\Home\\Downloads\\csci275'
    missing = []
    
    for doc in docs:
        path = os.path.join(doc_dir, doc)
        if not os.path.exists(path):
            missing.append(doc)
    
    if missing:
        print(f"[ERROR] Missing documentation:")
        for doc in missing:
            print(f"  - {doc}")
        return False
    else:
        print(f"[OK] All 3 new documentation files found")
        return True

def main():
    """Run all checks"""
    print()
    print("=" * 60)
    print("EventLogic v2.0 - System Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Models", check_models),
        ("Routes", check_routes),
        ("Templates", check_templates),
        ("Seed Data", check_seed_script),
        ("Documentation", check_documentation),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"[ERROR] {name} check failed: {e}")
            results.append(False)
    
    print()
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if all(results):
        print()
        print("[SUCCESS] All checks passed!")
        print()
        print("EventLogic v2.0 is ready to use!")
        print()
        print("Next steps:")
        print("1. Double-click SEED_DATA.bat to populate sample data")
        print("2. Double-click START_EVENTLOGIC_SERVER.bat to start server")
        print("3. Visit http://localhost:5000")
        print()
        print("Demo Accounts:")
        print("  Customer: john@example.com / customer123")
        print("  Vendor: venue@eventlogic.com / vendor123")
        print("  Admin: admin@eventlogic.com / admin123")
        print()
    else:
        print()
        print("[ERROR] Some checks failed. Please review above.")
        print()
    
    print("=" * 60)

if __name__ == '__main__':
    main()
