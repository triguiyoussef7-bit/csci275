"""
Seed script to populate EventLogic with realistic sample data
"""
import sys
from datetime import datetime, timedelta
import random

sys.path.insert(0, '/Mac/Home/Downloads/csci275')

from app_eventlogic import app, db
from models_eventlogic import Customer, Vendor, Admin, Service, Booking, Payment, Event, Budget

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("[OK] Database tables created")
        
        # Create Admin
        admin = Admin(name='Admin', email='admin@eventlogic.com')
        admin.set_password('admin123')
        db.session.add(admin)
        print("[OK] Admin created")
        
        # Create Vendors
        vendors = [
            ('Premium Venues Co.', 'venue@eventlogic.com', 'Professional event venues for all occasions'),
            ('Delicious Catering', 'catering@eventlogic.com', 'Gourmet catering services'),
            ('Smile Photography', 'photo@eventlogic.com', 'Professional photography and videography'),
            ('Party Decorations Ltd', 'decor@eventlogic.com', 'Creative event decoration services'),
            ('DJ Elite', 'dj@eventlogic.com', 'Professional DJ and music entertainment'),
        ]
        
        vendor_objs = []
        for vendor_name, email, description in vendors:
            vendor = Vendor(vendor_name=vendor_name, email=email, description=description)
            vendor.set_password('vendor123')
            vendor.verified = True
            vendor.verification_date = datetime.utcnow()
            vendor.phone = '555-' + str(random.randint(1000, 9999))
            vendor.city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
            db.session.add(vendor)
            vendor_objs.append(vendor)
        db.session.commit()
        print(f"[OK] Created {len(vendor_objs)} vendors")
        
        # Create Services for each vendor with EMOJI placeholders (Unicode)
        service_data = {
            0: [  # Venue vendor
                ('Banquet Hall', 'venue', 2500.0, 'Spacious hall for up to 500 guests', '🏛️'),
                ('Garden Venue', 'venue', 3000.0, 'Beautiful outdoor garden setting', '🌳'),
                ('Rooftop Terrace', 'venue', 3500.0, 'Modern rooftop with city views', '🏙️'),
            ],
            1: [  # Catering vendor
                ('Buffet Service', 'catering', 1500.0, 'Delicious buffet with variety of cuisines', '🍽️'),
                ('Sit-down Dinner', 'catering', 2500.0, 'Formal sit-down dinner service', '🥂'),
                ('Cocktail Party', 'catering', 1200.0, 'Cocktail and appetizer service', '🍸'),
            ],
            2: [  # Photography vendor
                ('Photography Package', 'photography', 2000.0, '8 hours of professional photography', '📷'),
                ('Videography Package', 'photography', 3000.0, 'Professional videography with editing', '🎥'),
                ('Photo Booth Rental', 'photography', 800.0, 'Interactive photo booth for guests', '📸'),
            ],
            3: [  # Decoration vendor
                ('Floral Arrangements', 'decoration', 1000.0, 'Beautiful floral centerpieces', '🌹'),
                ('Lighting Setup', 'decoration', 1500.0, 'Professional event lighting', '💡'),
                ('Balloon Decorations', 'decoration', 600.0, 'Custom balloon arrangements', '🎈'),
            ],
            4: [  # DJ vendor
                ('DJ Service 4 Hours', 'music', 800.0, 'Professional DJ for 4 hours', '🎧'),
                ('DJ Service 8 Hours', 'music', 1500.0, 'Professional DJ for 8 hours', '🎵'),
                ('Live Band', 'music', 3000.0, 'Live music band performance', '🎸'),
            ],
        }
        
        service_objs = []
        for vendor_idx, services in service_data.items():
            for service_name, category, price, description, photo_url in services:
                service = Service(
                    vendor_id=vendor_objs[vendor_idx].id,
                    service_name=service_name,
                    category=category,
                    price=price,
                    description=description,
                    photo_url=photo_url,
                    availability=True
                )
                db.session.add(service)
                service_objs.append(service)
        db.session.commit()
        print(f"[OK] Created {len(service_objs)} services with photos")
        
        # Create Customers
        customers = [
            ('John Smith', 'john@example.com'),
            ('Sarah Johnson', 'sarah@example.com'),
            ('Mike Wilson', 'mike@example.com'),
            ('Emma Davis', 'emma@example.com'),
        ]
        
        customer_objs = []
        for name, email in customers:
            customer = Customer(name=name, email=email)
            customer.set_password('customer123')
            customer.verified = True
            customer.phone = '555-' + str(random.randint(1000, 9999))
            customer.city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
            db.session.add(customer)
            customer_objs.append(customer)
        db.session.commit()
        print(f"[OK] Created {len(customer_objs)} customers")
        
        # Create Events
        event_types = ['Wedding', 'Birthday', 'Corporate Event', 'Graduation', 'Anniversary']
        event_objs = []
        for customer in customer_objs:
            for _ in range(2):
                event = Event(
                    customer_id=customer.id,
                    event_type=random.choice(event_types),
                    event_date=datetime.now() + timedelta(days=random.randint(30, 180)),
                    guest_count=random.randint(50, 300),
                    location_preference=customer.city,
                    description='Upcoming event'
                )
                db.session.add(event)
                event_objs.append(event)
        db.session.commit()
        print(f"[OK] Created {len(event_objs)} events")
        
        # Create Budgets
        for event in event_objs:
            budget = Budget(
                customer_id=event.customer_id,
                event_id=event.id,
                total_budget=random.choice([3000, 5000, 7000, 10000, 15000])
            )
            db.session.add(budget)
        db.session.commit()
        print(f"[OK] Created {len(event_objs)} budgets")
        
        # Create Bookings and Payments
        booking_count = 0
        for customer in customer_objs[:3]:  # Only first 3 customers
            for _ in range(3):
                service = random.choice(service_objs)
                booking = Booking(
                    customer_id=customer.id,
                    vendor_id=service.vendor_id,
                    service_id=service.id,
                    status=random.choice(['pending', 'confirmed', 'completed']),
                    requested_date=datetime.utcnow().date()
                )
                db.session.add(booking)
                db.session.flush()
                
                payment = Payment(
                    booking_id=booking.id,
                    amount=service.price,
                    payment_status=random.choice(['pending', 'completed']) if booking.status in ['pending', 'confirmed'] else 'completed',
                    payment_date=datetime.utcnow() if booking.status == 'completed' else None
                )
                db.session.add(payment)
                booking_count += 1
        
        db.session.commit()
        print(f"[OK] Created {booking_count} bookings with payments")
        
        print()
        print("="*50)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        print()
        print("Demo Accounts:")
        print("-" * 50)
        print("ADMIN:")
        print("  Email: admin@eventlogic.com")
        print("  Password: admin123")
        print()
        print("CUSTOMERS:")
        for name, email in customers:
            print(f"  Email: {email}")
            print(f"  Password: customer123")
        print()
        print("VENDORS:")
        for vendor_name, email, _ in vendors:
            print(f"  Email: {email}")
            print(f"  Password: vendor123")
        print()

if __name__ == '__main__':
    seed_database()
