"""
EventLogic System - Database Migration & Setup Script
Run this to initialize the database with all tables and sample data
"""

from app_eventlogic import app, db, init_db
from models_eventlogic import Customer, Vendor, Admin, Service, Booking, Payment, Event, Budget
from datetime import datetime, timedelta

def setup_database():
    """Initialize database and create all tables"""
    print("=" * 80)
    print("EventLogic System - Database Setup")
    print("=" * 80)
    
    with app.app_context():
        print("\n[1/5] Creating all tables...")
        db.create_all()
        print("[OK] All tables created successfully")
        
        print("\n[2/5] Creating sample admin account...")
        admin = Admin.query.filter_by(email='admin@eventlogic.com').first()
        if not admin:
            admin = Admin(
                name='Admin',
                email='admin@eventlogic.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin created: admin@eventlogic.com / admin123")
        else:
            print("[OK] Admin already exists")
        
        print("\n[3/5] Creating sample vendors...")
        vendors = [
            {
                'name': 'Premium Venues Co.',
                'email': 'venue1@eventlogic.com',
                'description': 'Professional event venues for all occasions',
                'city': 'New York'
            },
            {
                'name': 'Delicious Catering',
                'email': 'catering1@eventlogic.com',
                'description': 'Gourmet catering services',
                'city': 'New York'
            },
            {
                'name': 'Pro Photography Studio',
                'email': 'photo1@eventlogic.com',
                'description': 'Professional photography and videography',
                'city': 'New York'
            }
        ]
        
        for vendor_data in vendors:
            vendor = Vendor.query.filter_by(email=vendor_data['email']).first()
            if not vendor:
                vendor = Vendor(
                    vendor_name=vendor_data['name'],
                    email=vendor_data['email'],
                    description=vendor_data['description'],
                    city=vendor_data['city'],
                    verified=True,
                    verification_date=datetime.utcnow(),
                    rating=4.5
                )
                vendor.set_password('vendor123')
                db.session.add(vendor)
                db.session.commit()
                print(f"[OK] Created vendor: {vendor_data['name']}")
            else:
                print(f"[OK] Vendor {vendor_data['name']} already exists")
        
        print("\n[4/5] Creating sample services...")
        services_data = [
            {
                'vendor_id': 1,
                'name': 'Banquet Hall',
                'category': 'venue',
                'description': 'Spacious hall for 200-500 guests',
                'price': 2500.0,
                'tier': 'Standard',
                'max_guests': 500
            },
            {
                'vendor_id': 1,
                'name': 'Garden Venue',
                'category': 'venue',
                'description': 'Beautiful outdoor garden setting',
                'price': 3000.0,
                'tier': 'Premium',
                'max_guests': 300
            },
            {
                'vendor_id': 2,
                'name': 'Buffet Service',
                'category': 'catering',
                'description': 'Delicious buffet with variety of cuisines',
                'price': 1500.0,
                'tier': 'Standard',
                'max_guests': 500
            },
            {
                'vendor_id': 2,
                'name': 'Sit-down Dinner',
                'category': 'catering',
                'description': 'Formal sit-down dinner service',
                'price': 2500.0,
                'tier': 'Premium',
                'max_guests': 200
            },
            {
                'vendor_id': 3,
                'name': 'Photography Package',
                'category': 'photography',
                'description': '8 hours photography with editing',
                'price': 1200.0,
                'tier': 'Standard',
                'max_guests': None
            },
            {
                'vendor_id': 3,
                'name': 'Photography + Videography',
                'category': 'photography',
                'description': 'Full day coverage with professional video',
                'price': 2000.0,
                'tier': 'Premium',
                'max_guests': None
            }
        ]
        
        for service_data in services_data:
            service = Service.query.filter_by(
                vendor_id=service_data['vendor_id'],
                service_name=service_data['name']
            ).first()
            if not service:
                service = Service(
                    vendor_id=service_data['vendor_id'],
                    service_name=service_data['name'],
                    category=service_data['category'],
                    description=service_data['description'],
                    price=service_data['price'],
                    package_tier=service_data['tier'],
                    max_guests=service_data.get('max_guests'),
                    availability=True
                )
                db.session.add(service)
                db.session.commit()
                print(f"[OK] Created service: {service_data['name']}")
            else:
                print(f"[OK] Service {service_data['name']} already exists")
        
        print("\n[5/5] Creating sample customer account...")
        customer = Customer.query.filter_by(email='customer@eventlogic.com').first()
        if not customer:
            customer = Customer(
                name='John Doe',
                email='customer@eventlogic.com',
                phone='555-1234',
                city='New York',
                verified=True
            )
            customer.set_password('customer123')
            db.session.add(customer)
            db.session.commit()
            print("[OK] Sample customer created: customer@eventlogic.com / customer123")
        else:
            print("[OK] Customer already exists")
        
        print("\n" + "=" * 80)
        print("SUCCESS: DATABASE SETUP COMPLETE!")
        print("=" * 80)
        print("\nDEMO CREDENTIALS:")
        print("  Admin:    admin@eventlogic.com / admin123")
        print("  Vendor:   vendor123@eventlogic.com / vendor123")
        print("  Customer: customer@eventlogic.com / customer123")
        print("\nSTART THE APP:")
        print("  python app_eventlogic.py")
        print("\nVISIT:")
        print("  http://localhost:5000")
        print("=" * 80)


def reset_database():
    """Drop all tables and recreate from scratch"""
    print("[WARNING] This will delete all data!")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() == 'yes':
        with app.app_context():
            print("Dropping all tables...")
            db.drop_all()
            print("[OK] All tables dropped")
            setup_database()
    else:
        print("Operation cancelled")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        setup_database()
