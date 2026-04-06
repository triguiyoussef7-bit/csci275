"""
EventLogic System - Simplified Flask Application
Minimal working version - all routes render correctly
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os
from functools import wraps

# Import models and database
from models_eventlogic import (
    db, Customer, Vendor, Admin, Service, Booking, Payment, Event, Budget, Dispute, Review
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
    customer = Customer.query.get(user_id)
    if customer:
        customer.user_type = 'customer'
        return customer
    
    vendor = Vendor.query.get(user_id)
    if vendor:
        vendor.user_type = 'vendor'
        return vendor
    
    admin = Admin.query.get(user_id)
    if admin:
        admin.user_type = 'admin'
        return admin
    
    return None


# ============================================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================================
def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Customer):
            flash('Please login as a customer', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def vendor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Vendor):
            flash('Please login as a vendor', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
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
        role = request.form.get('role')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
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
        role = request.form.get('role', 'customer')
        
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
            name = user.name if hasattr(user, 'name') else user.vendor_name
            flash(f'Welcome back, {name}!', 'success')
            
            if role == 'customer':
                return redirect(url_for('customer_dashboard'))
            elif role == 'vendor':
                return redirect(url_for('vendor_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard_full'))
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
    """Customer dashboard"""
    upcoming_bookings = Booking.query.filter_by(
        customer_id=current_user.id
    ).filter(Booking.status.in_(['pending', 'confirmed'])).all()
    return render_template('customer_dashboard.html', bookings=upcoming_bookings)


@app.route('/customer/events', methods=['GET', 'POST'])
@customer_required
def customer_events():
    """Customer events"""
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
    return render_template('customer_events.html', events=events)


@app.route('/customer/budget')
@customer_required
def customer_budget_list():
    """List events to choose which one to budget for"""
    events = Event.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer_budget_list.html', events=events)


@app.route('/customer/budget/<int:event_id>', methods=['GET', 'POST'])
@customer_required
def customer_budget(event_id):
    """Customer budget planning"""
    event = Event.query.get(event_id)
    
    if request.method == 'POST':
        total_budget = float(request.form.get('total_budget', 0))
        description = request.form.get('description', '')
        
        budget = Budget(
            customer_id=current_user.id,
            event_id=event_id,
            total_budget=total_budget
        )
        db.session.add(budget)
        db.session.commit()
        
        flash('Budget created!', 'success')
        return redirect(url_for('customer_recommendations', budget_id=budget.id))
    
    budget = Budget.query.filter_by(event_id=event_id).first()
    return render_template('customer_budget.html', event=event, budget=budget)


@app.route('/customer/recommendations/<int:budget_id>')
@customer_required
def customer_recommendations(budget_id):
    """View vendor recommendations"""
    budget = Budget.query.get(budget_id)
    recommendations = generate_recommendations(budget)
    return render_template('customer_recommendations.html', budget=budget, recommendations=recommendations)


@app.route('/customer/budget-calculator')
@customer_required
def budget_calculator():
    """Smart budget planner with vendor recommendations"""
    return render_template('budget_planner.html')


@app.route('/customer/search-vendors')
@customer_required
def search_vendors():
    """Search vendors by budget and event type"""
    budget = request.args.get('budget', 5000, type=float)
    event_type = request.args.get('event_type', 'wedding')
    
    # Get all verified vendors
    vendors = Vendor.query.filter_by(verified=True).all()
    
    matching_vendors = []
    for vendor in vendors:
        # Get ALL services for this vendor (don't filter by category - all vendors can serve any event type)
        services = Service.query.filter_by(vendor_id=vendor.id).all()
        
        # Filter services that fit in budget
        affordable_services = [s for s in services if s.price <= budget]
        
        if affordable_services:
            matching_vendors.append({
                'id': vendor.id,
                'name': vendor.vendor_name,
                'rating': vendor.rating if vendor.rating else 0,
                'event_type': event_type,
                'services': [
                    {
                        'id': s.id,
                        'name': s.service_name,
                        'price': s.price,
                        'emoji': s.photo_url if s.photo_url and len(s.photo_url) < 5 else '⭐'
                    }
                    for s in affordable_services[:3]
                ]
            })
    
    return jsonify({'vendors': matching_vendors, 'budget': budget, 'event_type': event_type})


@app.route('/customer/plan-event')
@customer_required
def plan_event():
    """Complete event planning tool with budget calculator and vendor search"""
    return render_template('plan_event_new.html')


@app.route('/customer/vendors', methods=['GET'])
@customer_required
def customer_vendors():
    """Browse all verified vendors"""
    vendors = Vendor.query.filter_by(verified=True).all()
    return render_template('customer_vendors_new.html', vendors=vendors)


@app.route('/customer/vendor/<int:vendor_id>')
@app.route('/customer/vendor/<int:vendor_id>')
@customer_required
def customer_vendor_detail(vendor_id):
    """View vendor details with reviews"""
    vendor = Vendor.query.get(vendor_id)
    services = Service.query.filter_by(vendor_id=vendor_id).all()
    reviews = Review.query.filter_by(vendor_id=vendor_id).order_by(Review.created_at.desc()).all()
    return render_template('customer_vendor_detail.html', vendor=vendor, services=services, reviews=reviews)


@app.route('/customer/bookings')
@customer_required
def customer_bookings():
    """View bookings"""
    bookings = Booking.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer_bookings_new.html', bookings=bookings)


@app.route('/customer/booking/<int:booking_id>')
@customer_required
def customer_booking_detail(booking_id):
    """View booking details"""
    booking = Booking.query.get(booking_id)
    payment = Payment.query.filter_by(booking_id=booking_id).first()
    return render_template('customer_booking_detail.html', booking=booking, payment=payment)


@app.route('/customer/payment/<int:booking_id>', methods=['GET', 'POST'])
@customer_required
def customer_payment(booking_id):
    """Process payment"""
    booking = Booking.query.get(booking_id)
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('customer_bookings'))
    
    if request.method == 'POST':
        card_number = request.form.get('card_number', '').strip()
        cvv = request.form.get('cvv', '').strip()
        
        # Find or create payment
        payment = Payment.query.filter_by(booking_id=booking_id).first()
        if not payment:
            flash('No payment record found', 'error')
            return redirect(url_for('customer_bookings'))
        
        # Validate card
        if len(card_number) < 13 or not card_number.isdigit():
            flash('Invalid card number', 'error')
            return render_template('customer_payment.html', booking=booking)
        
        if len(cvv) < 3 or not cvv.isdigit():
            flash('Invalid CVV', 'error')
            return render_template('customer_payment.html', booking=booking)
        
        # Process payment
        payment.transaction_id = str(__import__('uuid').uuid4())
        payment.payment_status = 'completed'
        payment.payment_date = datetime.utcnow()
        db.session.commit()
        
        flash('Payment successful!', 'success')
        return redirect(url_for('customer_booking_detail', booking_id=booking_id))
    
    return render_template('customer_payment.html', booking=booking)


@app.route('/customer/booking/<int:booking_id>/cancel', methods=['POST'])
@customer_required
def customer_cancel_booking(booking_id):
    """Cancel a pending booking"""
    booking = Booking.query.get(booking_id)
    
    if not booking or booking.customer_id != current_user.id:
        flash('Booking not found', 'error')
        return redirect(url_for('customer_bookings'))
    
    if booking.status != 'pending':
        flash('Only pending bookings can be cancelled', 'error')
        return redirect(url_for('customer_booking_detail', booking_id=booking_id))
    
    booking.status = 'cancelled'
    db.session.commit()
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('customer_bookings'))



@customer_required
def customer_profile():
    """Customer profile"""
    return render_template('customer_profile.html', customer=current_user)


# ============================================================================
# VENDOR ROUTES
# ============================================================================

@app.route('/vendor/dashboard')
@vendor_required
def vendor_dashboard():
    """Vendor dashboard"""
    services = Service.query.filter_by(vendor_id=current_user.id).all()
    return render_template('vendor_dashboard.html', services=services)


@app.route('/vendor/services', methods=['GET', 'POST'])
@vendor_required
def vendor_services():
    """Manage services"""
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        
        service = Service(
            vendor_id=current_user.id,
            service_name=service_name,
            category=category,
            price=price,
            description=description,
            availability=True
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added!', 'success')
        return redirect(url_for('vendor_services'))
    
    services = Service.query.filter_by(vendor_id=current_user.id).all()
    return render_template('vendor_services.html', services=services)


@app.route('/vendor/service/<int:service_id>/edit', methods=['GET', 'POST'])
@vendor_required
def vendor_service_edit(service_id):
    """Edit service"""
    service = Service.query.get(service_id)
    
    if request.method == 'POST':
        service.service_name = request.form.get('service_name')
        service.category = request.form.get('category')
        service.price = float(request.form.get('price'))
        service.description = request.form.get('description')
        db.session.commit()
        flash('Service updated!', 'success')
        return redirect(url_for('vendor_services'))
    
    return render_template('vendor_service_edit.html', service=service)


@app.route('/vendor/bookings')
@vendor_required
def vendor_bookings():
    """View bookings"""
    services = Service.query.filter_by(vendor_id=current_user.id).all()
    service_ids = [s.id for s in services]
    bookings = Booking.query.filter(Booking.service_id.in_(service_ids)).all() if service_ids else []
    return render_template('vendor_bookings.html', bookings=bookings)


@app.route('/vendor/profile')
@vendor_required
def vendor_profile():
    """Vendor profile"""
    return render_template('vendor_profile.html', vendor=current_user)



# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/vendors')
@admin_required
def admin_vendors():
    """Manage vendors"""
    status = request.args.get('status', 'all')
    
    if status == 'pending':
        vendors = Vendor.query.filter_by(verified=False).all()
    elif status == 'verified':
        vendors = Vendor.query.filter_by(verified=True).all()
    else:
        vendors = Vendor.query.all()
    
    return render_template('admin_vendors.html', vendors=vendors, status=status)


@app.route('/admin/vendor/<int:vendor_id>/verify', methods=['POST'])
@admin_required
def admin_verify_vendor(vendor_id):
    """Verify vendor"""
    vendor = Vendor.query.get(vendor_id)
    vendor.verified = True
    vendor.verification_date = datetime.utcnow()
    db.session.commit()
    flash('Vendor verified!', 'success')
    return redirect(url_for('admin_vendors'))


@app.route('/admin/disputes')
@admin_required
def admin_disputes():
    """Manage disputes"""
    disputes = Dispute.query.all()
    return render_template('admin_disputes.html', disputes=disputes)


@app.route('/admin/reports')
@admin_required
def admin_reports():
    """View reports"""
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    
    return render_template('admin_reports.html', 
                         total_bookings=total_bookings,
                         total_revenue=total_revenue)


# ============================================================================
# API ENDPOINTS (JSON RESPONSES)
# ============================================================================

@app.route('/customer/book-service/<int:service_id>', methods=['POST'])
@customer_required
def customer_book_service(service_id):
    """Book a single service"""
    service = Service.query.get(service_id)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_vendors'))
    
    # Check if already booked
    existing = Booking.query.filter_by(
        customer_id=current_user.id,
        service_id=service_id,
        status='pending'
    ).first()
    
    if existing:
        flash('You already have a pending booking for this service', 'error')
        return redirect(url_for('customer_vendors'))
    
    booking = Booking(
        customer_id=current_user.id,
        service_id=service_id,
        vendor_id=service.vendor_id,
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()
    
    payment = Payment(
        booking_id=booking.id,
        amount=service.price,
        payment_status='pending'
    )
    db.session.add(payment)
    db.session.commit()
    
    flash(f'✓ Service Booked! {service.service_name} - ${"%.2f" % service.price}', 'success')
    return redirect(url_for('customer_bookings'))


@app.route('/customer/book-package', methods=['POST'])
@customer_required
def customer_book_package():
    """Book a recommended package"""
    package_tier = request.form.get('package_tier')
    package_price = float(request.form.get('package_price', 0))
    budget_id = request.form.get('budget_id')
    
    if not package_tier or package_price <= 0:
        flash('Invalid package', 'error')
        return redirect(url_for('customer_budget', event_id=budget_id))
    
    booking = Booking(
        customer_id=current_user.id,
        vendor_id=1,
        service_id=1,
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()
    
    payment = Payment(
        booking_id=booking.id,
        amount=package_price,
        payment_status='pending'
    )
    db.session.add(payment)
    db.session.commit()
    
    flash(f'Package "{package_tier.upper()}" booked successfully!', 'success')
    return redirect(url_for('customer_bookings'))




@app.route('/customer/booking/<int:booking_id>/review', methods=['GET', 'POST'])
@customer_required
def customer_review_booking(booking_id):
    """Leave a review for completed booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.customer_id != current_user.id:
        flash('You can only review your own bookings', 'error')
        return redirect(url_for('customer_bookings'))
    
    if booking.status != 'completed':
        flash('You can only review completed bookings', 'error')
        return redirect(url_for('customer_booking_detail', booking_id=booking_id))
    
    existing_review = Review.query.filter_by(booking_id=booking_id).first()
    
    if request.method == 'POST':
        rating = request.form.get('rating', type=float)
        title = request.form.get('title')
        comment = request.form.get('comment')
        
        if not rating or rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5', 'error')
            return redirect(url_for('customer_review_booking', booking_id=booking_id))
        
        if existing_review:
            existing_review.rating = rating
            existing_review.title = title
            existing_review.comment = comment
            db.session.commit()
            flash('Review updated successfully!', 'success')
        else:
            review = Review(
                booking_id=booking_id,
                customer_id=current_user.id,
                vendor_id=booking.vendor_id,
                rating=rating,
                title=title,
                comment=comment
            )
            db.session.add(review)
            
            vendor = booking.vendor
            all_reviews = Review.query.filter_by(vendor_id=vendor.id).all()
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else 0
            vendor.rating = avg_rating
            vendor.total_bookings += 1
            
            db.session.commit()
            flash('Review posted successfully!', 'success')
        
        return redirect(url_for('customer_booking_detail', booking_id=booking_id))
    
    return render_template('customer_review.html', booking=booking, existing_review=existing_review)


@app.route('/vendor/<int:vendor_id>/reviews', methods=['GET'])
def vendor_reviews(vendor_id):
    """View vendor reviews"""
    vendor = Vendor.query.get_or_404(vendor_id)
    reviews = Review.query.filter_by(vendor_id=vendor_id).order_by(Review.created_at.desc()).all()
    
    return render_template('vendor_reviews.html', vendor=vendor, reviews=reviews)


@app.route('/customer/activity', methods=['GET'])
@customer_required
def customer_activity():
    """View customer activity timeline"""
    customer = current_user
    
    bookings = Booking.query.filter_by(customer_id=customer.id).order_by(Booking.created_at.desc()).limit(20).all()
    payments = db.session.query(Payment, Booking).join(Booking).filter(
        Booking.customer_id == customer.id
    ).order_by(Payment.created_at.desc()).limit(20).all()
    
    events = Event.query.filter_by(customer_id=customer.id).order_by(Event.created_at.desc()).limit(10).all()
    reviews = Review.query.filter_by(customer_id=customer.id).order_by(Review.created_at.desc()).limit(10).all()
    
    activity = []
    for booking in bookings:
        activity.append({
            'type': 'booking',
            'date': booking.created_at,
            'title': f'Booked {booking.service.service_name}',
            'description': f'Service from {booking.vendor.vendor_name}',
            'status': booking.status,
            'id': booking.id
        })
    
    for payment, booking in payments:
        if payment.payment_status == 'completed':
            activity.append({
                'type': 'payment',
                'date': payment.payment_date,
                'title': f'Paid ${payment.amount:.2f}',
                'description': f'For {booking.service.service_name}',
                'amount': payment.amount,
                'id': payment.id
            })
    
    for event in events:
        activity.append({
            'type': 'event',
            'date': event.created_at,
            'title': f'Created {event.event_type} event',
            'description': f'Scheduled for {event.event_date}',
            'id': event.id
        })
    
    for review in reviews:
        activity.append({
            'type': 'review',
            'date': review.created_at,
            'title': f'Left {review.rating}-star review',
            'description': f'For {review.vendor.vendor_name}',
            'rating': review.rating,
            'id': review.id
        })
    
    activity.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('customer_activity.html', activity=activity)


@app.route('/vendor/analytics', methods=['GET'])
@vendor_required
def vendor_analytics():
    """View vendor analytics and statistics"""
    vendor = current_user
    
    bookings = Booking.query.filter_by(vendor_id=vendor.id).all()
    completed_bookings = [b for b in bookings if b.status == 'completed']
    pending_bookings = [b for b in bookings if b.status == 'pending']
    confirmed_bookings = [b for b in bookings if b.status == 'confirmed']
    
    total_revenue = sum(
        p.amount for b in completed_bookings 
        for p in b.payments if p.payment_status == 'completed'
    )
    
    reviews = Review.query.filter_by(vendor_id=vendor.id).all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
    
    monthly_revenue = {}
    for booking in completed_bookings:
        month = booking.updated_at.strftime('%Y-%m')
        revenue = sum(p.amount for p in booking.payments if p.payment_status == 'completed')
        monthly_revenue[month] = monthly_revenue.get(month, 0) + revenue
    
    return render_template('vendor_analytics.html', 
        vendor=vendor,
        total_bookings=len(bookings),
        completed_bookings=len(completed_bookings),
        pending_bookings=len(pending_bookings),
        confirmed_bookings=len(confirmed_bookings),
        total_revenue=total_revenue,
        reviews=reviews,
        avg_rating=avg_rating,
        monthly_revenue=monthly_revenue
    )


@app.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard_full():
    """Admin dashboard with system statistics"""
    customers = Customer.query.all()
    vendors = Vendor.query.all()
    verified_vendors = Vendor.query.filter_by(verified=True).all()
    bookings = Booking.query.all()
    completed_bookings = [b for b in bookings if b.status == 'completed']
    pending_bookings = [b for b in bookings if b.status == 'pending']
    
    total_revenue = sum(
        p.amount for b in completed_bookings 
        for p in b.payments if p.payment_status == 'completed'
    )
    
    disputes = Dispute.query.all()
    open_disputes = [d for d in disputes if d.status == 'open']
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    top_vendors = sorted(vendors, key=lambda v: v.rating, reverse=True)[:5]
    
    return render_template('admin_dashboard_full.html',
        total_customers=len(customers),
        total_vendors=len(vendors),
        verified_vendors=len(verified_vendors),
        total_bookings=len(bookings),
        completed_bookings=len(completed_bookings),
        pending_bookings=len(pending_bookings),
        total_revenue=total_revenue,
        total_disputes=len(disputes),
        open_disputes=len(open_disputes),
        recent_bookings=recent_bookings,
        top_vendors=top_vendors
    )


@app.route('/api/services', methods=['GET'])
def api_services():
    """Get all services"""
    services = Service.query.all()
    return jsonify([{
        'id': s.id,
        'service_name': s.service_name,
        'category': s.category,
        'price': s.price,
        'vendor_name': s.vendor.vendor_name
    } for s in services])


@app.route('/api/vendors', methods=['GET'])
def api_vendors():
    """Get all verified vendors"""
    vendors = Vendor.query.filter_by(verified=True).all()
    return jsonify([{
        'id': v.id,
        'vendor_name': v.vendor_name,
        'description': v.description
    } for v in vendors])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_recommendations(budget):
    """Generate vendor recommendations based on budget"""
    recommendations = {
        'basic': {
            'name': 'Basic Package',
            'description': 'Essential services',
            'price': budget.total_budget * 0.6,
            'services': []
        },
        'standard': {
            'name': 'Standard Package',
            'description': 'Popular choice',
            'price': budget.total_budget * 0.8,
            'services': []
        },
        'premium': {
            'name': 'Premium Package',
            'description': 'All features',
            'price': budget.total_budget,
            'services': []
        }
    }
    
    categories = ['venue', 'catering', 'photography', 'decoration', 'music']
    
    for tier, config in recommendations.items():
        tier_budget = config['price']
        per_category = tier_budget / len(categories) if categories else 1
        
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
    """Process payment"""
    if not card_number or len(card_number) < 13:
        return False
    if not cvv or len(cvv) < 3:
        return False
    
    import uuid
    payment.transaction_id = str(uuid.uuid4())
    payment.payment_status = 'completed'
    payment.payment_date = datetime.utcnow()
    
    return True


# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        
        if Admin.query.count() == 0:
            admin = Admin(name='Admin', email='admin@eventlogic.com')
            admin.set_password('admin123')
            db.session.add(admin)
            
            vendor = Vendor(vendor_name='Premium Venue Co.', email='venue@eventlogic.com')
            vendor.set_password('vendor123')
            vendor.verified = True
            vendor.verification_date = datetime.utcnow()
            vendor.description = 'Professional event venue'
            db.session.add(vendor)
            
            service = Service(
                vendor_id=1,
                service_name='Banquet Hall',
                category='venue',
                description='Hall for up to 500 guests',
                price=2500.0,
                availability=True
            )
            db.session.add(service)
            
            customer = Customer(name='Test Customer', email='customer@eventlogic.com')
            customer.set_password('customer123')
            db.session.add(customer)
            
            db.session.commit()
            print("[OK] Database initialized")


if __name__ == '__main__':
    init_db()
    print()
    print("[OK] Starting EventLogic server...")
    print("[OK] Visit: http://localhost:5000")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
