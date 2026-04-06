"""
EventLogic System - Complete Flask Application
Implements multi-role platform: Customer, Vendor, Admin
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os
from functools import wraps

# Import models and database
from models_eventlogic import (
    db, Customer, Vendor, Admin, Service, Booking, Payment, Event, Budget, Dispute
)

# Initialize Flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "eventlogic.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'eventlogic-secret-key-change-in-production'

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create directories
os.makedirs(os.path.join(basedir, 'templates'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'static'), exist_ok=True)


# ============================================================================
# USER LOADER FOR FLASK-LOGIN
# ============================================================================
@login_manager.user_loader
def load_user(user_id):
    """Load user from session"""
    # Try customer first
    customer = Customer.query.get(user_id)
    if customer:
        customer.user_type = 'customer'
        return customer
    
    # Try vendor
    vendor = Vendor.query.get(user_id)
    if vendor:
        vendor.user_type = 'vendor'
        return vendor
    
    # Try admin
    admin = Admin.query.get(user_id)
    if admin:
        admin.user_type = 'admin'
        return admin
    
    return None


# ============================================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================================
def customer_required(f):
    """Decorator to require customer login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Customer):
            flash('Please login as a customer', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def vendor_required(f):
    """Decorator to require vendor login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Vendor):
            flash('Please login as a vendor', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash('Please login as an admin', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        if isinstance(current_user, Customer):
            return redirect(url_for('customer_dashboard'))
        elif isinstance(current_user, Vendor):
            return redirect(url_for('vendor_dashboard'))
        elif isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new account"""
    if request.method == 'POST':
        role = request.form.get('role')  # customer, vendor
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        # Check if user exists
        if role == 'customer':
            if Customer.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            customer = Customer(name=name, email=email)
            customer.set_password(password)
            db.session.add(customer)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        
        elif role == 'vendor':
            if Vendor.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            vendor = Vendor(vendor_name=name, email=email)
            vendor.set_password(password)
            db.session.add(vendor)
            db.session.commit()
            flash('Registration successful. Waiting for admin verification.', 'info')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to account"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # customer, vendor, admin
        
        user = None
        
        if role == 'customer':
            user = Customer.query.filter_by(email=email).first()
        elif role == 'vendor':
            user = Vendor.query.filter_by(email=email).first()
        elif role == 'admin':
            user = Admin.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            session['user_role'] = role
            flash(f'Welcome back, {user.name if hasattr(user, "name") else user.vendor_name}!', 'success')
            
            if role == 'customer':
                return redirect(url_for('customer_dashboard'))
            elif role == 'vendor':
                return redirect(url_for('vendor_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


# ============================================================================
# CUSTOMER ROUTES
# ============================================================================

@app.route('/customer/dashboard')
@customer_required
def customer_dashboard():
    """Customer dashboard - main navigation"""
    upcoming_bookings = Booking.query.filter_by(
        customer_id=current_user.id,
        status='confirmed'
    ).all()
    
    return render_template('customer_dashboard.html', bookings=upcoming_bookings)


@app.route('/customer/events', methods=['GET', 'POST'])
@customer_required
def customer_events():
    """Customer - describe event needs"""
    if request.method == 'POST':
        event_type = request.form.get('event_type')
        event_date = datetime.strptime(request.form.get('event_date'), '%Y-%m-%d').date()
        guest_count = int(request.form.get('guest_count', 0))
        description = request.form.get('description')
        location = request.form.get('location_preference')
        
        event = Event(
            customer_id=current_user.id,
            event_type=event_type,
            event_date=event_date,
            guest_count=guest_count,
            description=description,
            location_preference=location
        )
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('customer_budget', event_id=event.id))
    
    events = Event.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer/events.html', events=events)


@app.route('/customer/budget', methods=['GET', 'POST'])
@customer_required
def customer_budget():
    """Customer - enter budget"""
    event_id = request.args.get('event_id', type=int)
    
    if request.method == 'POST':
        total_budget = float(request.form.get('total_budget'))
        
        budget = Budget(
            customer_id=current_user.id,
            event_id=event_id,
            total_budget=total_budget,
            venue_budget=float(request.form.get('venue_budget', 0)),
            catering_budget=float(request.form.get('catering_budget', 0)),
            photography_budget=float(request.form.get('photography_budget', 0)),
            decoration_budget=float(request.form.get('decoration_budget', 0)),
            music_budget=float(request.form.get('music_budget', 0)),
            other_budget=float(request.form.get('other_budget', 0))
        )
        db.session.add(budget)
        db.session.commit()
        
        flash('Budget set! View recommendations below.', 'success')
        return redirect(url_for('customer_recommendations', budget_id=budget.id))
    
    event = Event.query.get(event_id) if event_id else None
    return render_template('customer/budget.html', event=event)


@app.route('/customer/recommendations/<int:budget_id>')
@customer_required
def customer_recommendations(budget_id):
    """Customer - view budget-based recommendations"""
    budget = Budget.query.get(budget_id)
    if not budget or budget.customer_id != current_user.id:
        flash('Budget not found', 'error')
        return redirect(url_for('customer_dashboard'))
    
    # RECOMMENDATION ENGINE: Generate packages based on budget
    recommendations = generate_recommendations(budget)
    
    return render_template('customer/recommendations.html', 
                         budget=budget, 
                         recommendations=recommendations)


@app.route('/customer/vendors')
@customer_required
def customer_vendors():
    """Customer - view verified vendors"""
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    
    query = Vendor.query.filter_by(verified=True)
    
    if category:
        # Filter by category - join with services
        query = query.join(Service).filter(Service.category == category)
    
    vendors = query.paginate(page=page, per_page=10)
    
    return render_template('customer/vendors.html', vendors=vendors)


@app.route('/customer/vendor/<int:vendor_id>')
@customer_required
def customer_vendor_detail(vendor_id):
    """Customer - view vendor details and services"""
    vendor = Vendor.query.get(vendor_id)
    if not vendor or not vendor.verified:
        flash('Vendor not found', 'error')
        return redirect(url_for('customer_vendors'))
    
    services = Service.query.filter_by(vendor_id=vendor_id, availability=True).all()
    
    return render_template('customer/vendor_detail.html', vendor=vendor, services=services)


@app.route('/customer/booking', methods=['POST'])
@customer_required
def customer_booking():
    """Customer - send booking request"""
    service_id = request.form.get('service_id', type=int)
    event_details = request.form.get('event_details')
    requested_date = request.form.get('requested_date')
    
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    booking = Booking(
        customer_id=current_user.id,
        vendor_id=service.vendor_id,
        service_id=service_id,
        event_details=event_details,
        requested_date=datetime.strptime(requested_date, '%Y-%m-%d').date(),
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()
    
    flash('Booking request sent to vendor!', 'success')
    return redirect(url_for('customer_bookings'))


@app.route('/customer/bookings')
@customer_required
def customer_bookings():
    """Customer - view all bookings"""
    status = request.args.get('status')
    
    query = Booking.query.filter_by(customer_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    return render_template('customer/bookings.html', bookings=bookings)


@app.route('/customer/booking/<int:booking_id>')
@customer_required
def customer_booking_detail(booking_id):
    """Customer - view booking details"""
    booking = Booking.query.get(booking_id)
    if not booking or booking.customer_id != current_user.id:
        flash('Booking not found', 'error')
        return redirect(url_for('customer_bookings'))
    
    payment = Payment.query.filter_by(booking_id=booking_id).first()
    
    return render_template('customer/booking_detail.html', booking=booking, payment=payment)


@app.route('/customer/payment/<int:booking_id>', methods=['GET', 'POST'])
@customer_required
def customer_payment(booking_id):
    """Customer - make payment for booking"""
    booking = Booking.query.get(booking_id)
    if not booking or booking.customer_id != current_user.id:
        flash('Booking not found', 'error')
        return redirect(url_for('customer_bookings'))
    
    if request.method == 'POST':
        # Create payment record
        payment = Payment(
            booking_id=booking_id,
            amount=booking.service.price,
            payment_method=request.form.get('payment_method')
        )
        
        # PAYMENT PROCESSING
        success = process_payment(payment, request.form.get('card_number'), 
                                request.form.get('cvv'))
        
        if success:
            db.session.add(payment)
            booking.status = 'confirmed'
            db.session.commit()
            flash('Payment successful! Booking confirmed.', 'success')
            return redirect(url_for('customer_booking_detail', booking_id=booking_id))
        else:
            flash('Payment failed. Please try again.', 'error')
    
    return render_template('customer/payment.html', booking=booking)


@app.route('/customer/profile')
@customer_required
def customer_profile():
    """Customer - view and edit profile"""
    return render_template('customer/profile.html', customer=current_user)


@app.route('/customer/profile/update', methods=['POST'])
@customer_required
def customer_profile_update():
    """Customer - update profile"""
    current_user.name = request.form.get('name')
    current_user.phone = request.form.get('phone')
    current_user.address = request.form.get('address')
    current_user.city = request.form.get('city')
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('customer_profile'))


# ============================================================================
# VENDOR ROUTES
# ============================================================================

@app.route('/vendor/dashboard')
@vendor_required
def vendor_dashboard():
    """Vendor dashboard"""
    if not current_user.verified:
        flash('Your account is pending admin verification', 'warning')
    
    pending_bookings = Booking.query.filter_by(
        vendor_id=current_user.id,
        status='pending'
    ).all()
    
    confirmed_bookings = Booking.query.filter_by(
        vendor_id=current_user.id,
        status='confirmed'
    ).all()
    
    return render_template('vendor_dashboard.html',
                         pending_bookings=pending_bookings,
                         confirmed_bookings=confirmed_bookings)


@app.route('/vendor/services', methods=['GET', 'POST'])
@vendor_required
def vendor_services():
    """Vendor - manage service listings"""
    if request.method == 'POST':
        service = Service(
            vendor_id=current_user.id,
            service_name=request.form.get('service_name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            package_tier=request.form.get('package_tier'),
            max_guests=int(request.form.get('max_guests', 0)) or None
        )
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully!', 'success')
        return redirect(url_for('vendor_services'))
    
    services = Service.query.filter_by(vendor_id=current_user.id).all()
    
    return render_template('vendor/services.html', services=services)


@app.route('/vendor/service/<int:service_id>/edit', methods=['GET', 'POST'])
@vendor_required
def vendor_service_edit(service_id):
    """Vendor - edit service"""
    service = Service.query.get(service_id)
    if not service or service.vendor_id != current_user.id:
        flash('Service not found', 'error')
        return redirect(url_for('vendor_services'))
    
    if request.method == 'POST':
        service.service_name = request.form.get('service_name')
        service.description = request.form.get('description')
        service.price = float(request.form.get('price'))
        service.availability = request.form.get('availability') == 'on'
        db.session.commit()
        
        flash('Service updated!', 'success')
        return redirect(url_for('vendor_services'))
    
    return render_template('vendor/service_edit.html', service=service)


@app.route('/vendor/bookings')
@vendor_required
def vendor_bookings():
    """Vendor - view booking requests"""
    status = request.args.get('status')
    
    query = Booking.query.filter_by(vendor_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    return render_template('vendor/bookings.html', bookings=bookings)


@app.route('/vendor/booking/<int:booking_id>/respond', methods=['POST'])
@vendor_required
def vendor_booking_respond(booking_id):
    """Vendor - respond to booking request"""
    booking = Booking.query.get(booking_id)
    if not booking or booking.vendor_id != current_user.id:
        flash('Booking not found', 'error')
        return redirect(url_for('vendor_bookings'))
    
    response = request.form.get('response')  # accepted, rejected
    notes = request.form.get('notes')
    
    booking.status = 'confirmed' if response == 'accepted' else 'cancelled'
    booking.notes = notes
    db.session.commit()
    
    flash(f'Booking {response}!', 'success')
    return redirect(url_for('vendor_bookings'))


@app.route('/vendor/profile')
@vendor_required
def vendor_profile():
    """Vendor - view profile"""
    return render_template('vendor/profile.html', vendor=current_user)


@app.route('/vendor/profile/update', methods=['POST'])
@vendor_required
def vendor_profile_update():
    """Vendor - update profile"""
    current_user.vendor_name = request.form.get('vendor_name')
    current_user.description = request.form.get('description')
    current_user.phone = request.form.get('phone')
    current_user.address = request.form.get('address')
    current_user.city = request.form.get('city')
    db.session.commit()
    
    flash('Profile updated!', 'success')
    return redirect(url_for('vendor_profile'))


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = Customer.query.count() + Vendor.query.count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter(
        Payment.payment_status == 'completed'
    ).scalar() or 0
    
    pending_vendors = Vendor.query.filter_by(verified=False).count()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         pending_vendors=pending_vendors)


@app.route('/admin/vendors')
@admin_required
def admin_vendors():
    """Admin - verify vendors"""
    status = request.args.get('status', 'pending')  # pending, verified, rejected
    
    if status == 'pending':
        vendors = Vendor.query.filter_by(verified=False).all()
    elif status == 'verified':
        vendors = Vendor.query.filter_by(verified=True).all()
    
    return render_template('admin/vendors.html', vendors=vendors, status=status)


@app.route('/admin/vendor/<int:vendor_id>/verify', methods=['POST'])
@admin_required
def admin_vendor_verify(vendor_id):
    """Admin - approve vendor"""
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({'error': 'Vendor not found'}), 404
    
    action = request.form.get('action')  # approve, reject
    
    if action == 'approve':
        vendor.verified = True
        vendor.verification_date = datetime.utcnow()
        db.session.commit()
        flash(f'Vendor {vendor.vendor_name} approved!', 'success')
    else:
        db.session.delete(vendor)
        db.session.commit()
        flash('Vendor rejected', 'success')
    
    return redirect(url_for('admin_vendors'))


@app.route('/admin/disputes')
@admin_required
def admin_disputes():
    """Admin - monitor disputes"""
    disputes = Dispute.query.filter(Dispute.status != 'closed').all()
    
    return render_template('admin/disputes.html', disputes=disputes)


@app.route('/admin/dispute/<int:dispute_id>/resolve', methods=['POST'])
@admin_required
def admin_dispute_resolve(dispute_id):
    """Admin - resolve dispute"""
    dispute = Dispute.query.get(dispute_id)
    if not dispute:
        return jsonify({'error': 'Dispute not found'}), 404
    
    dispute.status = 'resolved'
    dispute.resolution = request.form.get('resolution')
    db.session.commit()
    
    flash('Dispute resolved', 'success')
    return redirect(url_for('admin_disputes'))


@app.route('/admin/reports')
@admin_required
def admin_reports():
    """Admin - view analytics and reports"""
    # Revenue by month
    bookings_by_status = db.session.query(
        Booking.status,
        db.func.count(Booking.id)
    ).group_by(Booking.status).all()
    
    top_vendors = db.session.query(
        Vendor.vendor_name,
        db.func.count(Booking.id).label('booking_count')
    ).join(Booking).group_by(Vendor.id).order_by(db.desc('booking_count')).limit(10).all()
    
    return render_template('admin/reports.html',
                         bookings_by_status=bookings_by_status,
                         top_vendors=top_vendors)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/services/search', methods=['GET'])
@login_required
def api_search_services():
    """Search services by category and budget"""
    category = request.args.get('category')
    max_price = request.args.get('max_price', type=float)
    
    query = Service.query.filter_by(availability=True).join(Vendor).filter(Vendor.verified == True)
    
    if category:
        query = query.filter(Service.category == category)
    
    if max_price:
        query = query.filter(Service.price <= max_price)
    
    services = query.limit(20).all()
    
    return jsonify([service.to_dict() for service in services])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_recommendations(budget):
    """
    RECOMMENDATION ENGINE
    Generate 3-tier package recommendations based on budget
    """
    recommendations = {
        'basic': {
            'name': 'Basic Package',
            'description': 'Essential services for your event',
            'price': budget.total_budget * 0.6,
            'services': []
        },
        'standard': {
            'name': 'Standard Package',
            'description': 'Popular choice with good variety',
            'price': budget.total_budget * 0.8,
            'services': []
        },
        'premium': {
            'name': 'Premium Package',
            'description': 'All features and premium services',
            'price': budget.total_budget,
            'services': []
        }
    }
    
    # Query services within budget ranges
    categories = ['venue', 'catering', 'photography', 'decoration', 'music']
    
    for tier, config in recommendations.items():
        tier_budget = config['price']
        per_category = tier_budget / len(categories)
        
        for category in categories:
            services = Service.query.filter(
                Service.category == category,
                Service.price <= per_category,
                Service.availability == True
            ).join(Vendor).filter(Vendor.verified == True).limit(2).all()
            
            config['services'].extend([{
                'category': category,
                'name': s.service_name,
                'vendor': s.vendor.vendor_name,
                'price': s.price,
                'id': s.id
            } for s in services])
    
    return recommendations


def process_payment(payment, card_number, cvv):
    """
    PAYMENT PROCESSING
    Simulate payment gateway (in production, use real gateway like Stripe)
    """
    # Validate card details (basic validation)
    if not card_number or len(card_number) < 13:
        return False
    
    if not cvv or len(cvv) < 3:
        return False
    
    # Generate transaction ID
    import uuid
    payment.transaction_id = str(uuid.uuid4())
    
    # Process payment
    payment.payment_status = 'completed'
    payment.payment_date = datetime.utcnow()
    
    return True


# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create sample data if empty
        if Admin.query.count() == 0:
            admin = Admin(name='Admin', email='admin@eventlogic.com')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Add sample vendors
            vendor = Vendor(vendor_name='Premium Venue Co.', email='venue@eventlogic.com')
            vendor.set_password('vendor123')
            vendor.verified = True
            vendor.verification_date = datetime.utcnow()
            vendor.description = 'Professional event venue provider'
            db.session.add(vendor)
            
            # Add sample services
            service = Service(
                vendor_id=1,
                service_name='Banquet Hall Package',
                category='venue',
                description='Spacious hall for up to 500 guests',
                price=2500.0,
                package_tier='Standard',
                max_guests=500
            )
            db.session.add(service)
            
            db.session.commit()
            print("[OK] Database initialized with sample data")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
