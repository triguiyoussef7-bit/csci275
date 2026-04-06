"""
SQLAlchemy Models for Event Planner
Defines the Event model and related database logic
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

# Initialize SQLAlchemy here to avoid circular imports
db = SQLAlchemy()


class Event(db.Model):
    """Event model representing an event in the planner"""
    
    __tablename__ = 'events'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default='')
    date = db.Column(db.Date, nullable=False)  # Format: YYYY-MM-DD
    time = db.Column(db.Time, nullable=False)  # Format: HH:MM
    category = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, default=0.0)  # Budget in dollars
    estimated_cost = db.Column(db.Float, default=0.0)  # Estimated cost based on category
    event_type = db.Column(db.String(100), default='custom')  # Event type (birthday, wedding, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.id}: {self.title} on {self.date} at {self.time}>'
    
    def to_dict(self):
        """Convert event object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time.isoformat() if self.time else None,
            'category': self.category,
            'budget': self.budget,
            'estimated_cost': self.estimated_cost,
            'event_type': self.event_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def check_conflict(date, time, exclude_id=None):
        """
        Check if an event already exists for the given date and time.
        
        Args:
            date: Event date (YYYY-MM-DD)
            time: Event time (HH:MM)
            exclude_id: ID of event to exclude from conflict check (for updates)
        
        Returns:
            Conflicting Event object if found, None otherwise
        """
        query = Event.query.filter_by(date=date, time=time)
        
        if exclude_id:
            query = query.filter(Event.id != exclude_id)
        
        return query.first()
    
    @staticmethod
    def get_by_date(date):
        """Get all events for a specific date"""
        return Event.query.filter_by(date=date).order_by(Event.time).all()
    
    @staticmethod
    def get_by_category(category):
        """Get all events for a specific category"""
        return Event.query.filter_by(category=category).order_by(Event.date, Event.time).all()
    
    @staticmethod
    def get_upcoming(limit=None):
        """Get upcoming events (sorted by date and time)"""
        events = Event.query.order_by(Event.date, Event.time).all()
        if limit:
            events = events[:limit]
        return events
