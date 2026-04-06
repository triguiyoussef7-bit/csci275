"""
EventLogic System Models - Complete Database Schema
Implements all entities from ERD: Customer, Vendor, Service, Booking, Payment, Admin
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ============================================================================
# CUSTOMER MODEL
# ============================================================================
class Customer(UserMixin, db.Model):
    """Customer account - enters event needs, selects vendors, makes payments"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True, cascade='all, delete-orphan')
    events = db.relationship('Event', backref='customer', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def register(self, email, password, name):
        """Register new customer account"""
        self.email = email
        self.name = name
        self.set_password(password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'verified': self.verified,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# VENDOR MODEL
# ============================================================================
class Vendor(UserMixin, db.Model):
    """Vendor account - offers services, responds to bookings"""
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)  # Admin verification
    verification_date = db.Column(db.DateTime)
    rating = db.Column(db.Float, default=0.0)  # Out of 5
    total_bookings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', backref='vendor', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='vendor', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='vendor', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def manage_listings(self, service_data):
        """Create or update service listings"""
        service = Service(**service_data)
        service.vendor_id = self.id
        return service
    
    def respond_to_request(self, booking_id, response_status):
        """Accept or reject booking request"""
        booking = Booking.query.get(booking_id)
        if booking and booking.vendor_id == self.id:
            booking.status = response_status
            db.session.commit()
        return booking
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_name': self.vendor_name,
            'email': self.email,
            'phone': self.phone,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'verified': self.verified,
            'rating': self.rating,
            'total_bookings': self.total_bookings,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# ADMIN MODEL
# ============================================================================
class Admin(UserMixin, db.Model):
    """Admin account - verifies vendors, monitors disputes, manages reports"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='admin')  # admin, moderator, analyst
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def verify_vendor(self, vendor_id, approved=True):
        """Approve or reject vendor verification"""
        vendor = Vendor.query.get(vendor_id)
        if vendor:
            vendor.verified = approved
            vendor.verification_date = datetime.utcnow() if approved else None
            db.session.commit()
        return vendor
    
    def monitor_disputes(self):
        """Monitor disputed bookings"""
        disputes = Booking.query.filter(Booking.status == 'disputed').all()
        return disputes
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# SERVICE MODEL
# ============================================================================
class Service(db.Model):
    """Service offerings by vendors"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Venue, Catering, Photography, etc.
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    package_tier = db.Column(db.String(50))  # Basic, Standard, Premium
    availability = db.Column(db.Boolean, default=True)
    max_guests = db.Column(db.Integer)  # For venue services
    photo_url = db.Column(db.String(500))  # Service photo URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='service', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.vendor_name if self.vendor else None,
            'service_name': self.service_name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'package_tier': self.package_tier,
            'availability': self.availability,
            'max_guests': self.max_guests
        }


# ============================================================================
# EVENT MODEL - Customer describes event needs
# ============================================================================
class Event(db.Model):
    """Event details - customer describes what they need"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)  # Birthday, Wedding, Corporate, etc.
    event_date = db.Column(db.Date, nullable=False)
    guest_count = db.Column(db.Integer)
    description = db.Column(db.Text)
    location_preference = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'event_type': self.event_type,
            'event_date': self.event_date.isoformat(),
            'guest_count': self.guest_count,
            'description': self.description,
            'location_preference': self.location_preference
        }


# ============================================================================
# BUDGET MODEL - Customer enters budget and receives recommendations
# ============================================================================
class Budget(db.Model):
    """Budget input and recommendations"""
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    total_budget = db.Column(db.Float, nullable=False)
    venue_budget = db.Column(db.Float)
    catering_budget = db.Column(db.Float)
    photography_budget = db.Column(db.Float)
    decoration_budget = db.Column(db.Float)
    music_budget = db.Column(db.Float)
    other_budget = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'total_budget': self.total_budget,
            'venue_budget': self.venue_budget,
            'catering_budget': self.catering_budget,
            'photography_budget': self.photography_budget,
            'decoration_budget': self.decoration_budget,
            'music_budget': self.music_budget,
            'other_budget': self.other_budget
        }


# ============================================================================
# BOOKING MODEL
# ============================================================================
class Booking(db.Model):
    """Booking request - customer requests service from vendor"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    event_details = db.Column(db.Text)
    requested_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled, completed, disputed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='booking', lazy=True, cascade='all, delete-orphan')
    
    def update_status(self, new_status):
        """Update booking status"""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.vendor_name,
            'service_id': self.service_id,
            'service_name': self.service.service_name if self.service else None,
            'event_details': self.event_details,
            'requested_date': self.requested_date.isoformat() if self.requested_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# ============================================================================
# PAYMENT MODEL
# ============================================================================
class Payment(db.Model):
    """Payment processing for bookings"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, debit_card, paypal, etc.
    transaction_id = db.Column(db.String(255), unique=True)
    payment_status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    payment_date = db.Column(db.DateTime)
    refund_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def process_payment(self, payment_method, transaction_id=None):
        """Process payment for booking"""
        self.payment_method = payment_method
        self.transaction_id = transaction_id
        self.payment_status = 'completed'
        self.payment_date = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'refund_date': self.refund_date.isoformat() if self.refund_date else None,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# REVIEW MODEL - Customer reviews vendors
# ============================================================================
class Review(db.Model):
    """Customer reviews for vendors after completed bookings"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)  # 1-5 stars
    title = db.Column(db.String(255))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.vendor_name if self.vendor else None,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# DISPUTE MODEL - For admin monitoring
# ============================================================================
class Dispute(db.Model):
    """Handle disputes between customers and vendors"""
    __tablename__ = 'disputes'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    raised_by = db.Column(db.String(50))  # customer or vendor
    reason = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')  # open, resolved, closed
    resolution = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'raised_by': self.raised_by,
            'reason': self.reason,
            'status': self.status,
            'resolution': self.resolution,
            'created_at': self.created_at.isoformat()
        }
