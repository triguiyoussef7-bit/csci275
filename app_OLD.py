"""
Event Planner Flask Application
Main entry point for the web application
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, date, time
import os

# Import db and Event from models to avoid circular imports
from models import db, Event

# Initialize Flask app
app = Flask(__name__)

# Create necessary directories
basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'templates'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'static'), exist_ok=True)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize database with app
db.init_app(app)

# Event templates with budget ranges and images
EVENT_TEMPLATES = {
    'birthday': {
        'name': '🎂 Birthday Party',
        'description': 'Celebrate with family and friends',
        'min_budget': 100,
        'max_budget': 2000,
        'image': 'https://images.unsplash.com/photo-1558636508-e0db3814a69e?w=400&h=300&fit=crop',
        'icon': '🎂'
    },
    'wedding': {
        'name': '💒 Wedding',
        'description': 'Celebrate your special day',
        'min_budget': 1000,
        'max_budget': 10000,
        'image': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop',
        'icon': '💒'
    },
    'graduation': {
        'name': '🎓 Graduation',
        'description': 'Celebrate academic achievement',
        'min_budget': 200,
        'max_budget': 2500,
        'image': 'https://images.unsplash.com/photo-1554734898-e0a39ffb4a30?w=400&h=300&fit=crop',
        'icon': '🎓'
    },
    'business': {
        'name': '💼 Business Meeting',
        'description': 'Professional conference or seminar',
        'min_budget': 500,
        'max_budget': 5000,
        'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop',
        'icon': '💼'
    },
    'party': {
        'name': '🎉 Party/Celebration',
        'description': 'Fun gathering with friends',
        'min_budget': 150,
        'max_budget': 3000,
        'image': 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=400&h=300&fit=crop',
        'icon': '🎉'
    },
    'meeting': {
        'name': '📅 Team Meeting',
        'description': 'Work meeting or brainstorming session',
        'min_budget': 50,
        'max_budget': 1000,
        'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop',
        'icon': '📅'
    },
    'dinner': {
        'name': '🍽️ Dinner Event',
        'description': 'Formal or casual dinner gathering',
        'min_budget': 200,
        'max_budget': 5000,
        'image': 'https://images.unsplash.com/photo-1547573854-74e2b9508482?w=400&h=300&fit=crop',
        'icon': '🍽️'
    },
    'workshop': {
        'name': '🎓 Workshop/Training',
        'description': 'Educational event or training session',
        'min_budget': 300,
        'max_budget': 4000,
        'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop',
        'icon': '🎓'
    }
}


@app.route('/')
def home():
    """Home page - display all events"""
    return render_template('index.html')


@app.route('/budget')
def budget_page():
    """Budget input page - user enters budget"""
    return render_template('budget.html')


@app.route('/suggestions')
def suggestions_page():
    """Event suggestions based on budget"""
    budget = request.args.get('budget', type=float)
    if not budget:
        return render_template('index.html'), 400
    
    # Filter event templates based on budget
    suggestions = []
    for key, template in EVENT_TEMPLATES.items():
        if template['min_budget'] <= budget <= template['max_budget']:
            suggestions.append({'type': key, **template})
    
    # Sort by min_budget
    suggestions.sort(key=lambda x: x['min_budget'])
    
    return render_template('suggestions.html', budget=budget, suggestions=suggestions)


@app.route('/create')
def create_event_page():
    """Event creation page"""
    event_type = request.args.get('type', 'custom')
    template = EVENT_TEMPLATES.get(event_type, {})
    return render_template('create.html', template=template, event_type=event_type)


@app.route('/edit/<int:event_id>')
def edit_event_page(event_id):
    """Event editing page"""
    event = Event.query.get(event_id)
    if not event:
        return render_template('index.html'), 404
    return render_template('edit.html', event=event)


# ==================== API ENDPOINTS ====================

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events with optional filtering"""
    try:
        # Get filter parameters
        date_filter = request.args.get('date')
        category_filter = request.args.get('category')
        
        # Build query
        query = Event.query
        
        if date_filter:
            query = query.filter_by(date=date_filter)
        
        if category_filter:
            query = query.filter_by(category=category_filter)
        
        # Order by date and time
        events = query.order_by(Event.date, Event.time).all()
        
        return jsonify([event.to_dict() for event in events]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'date', 'time', 'category']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Convert string dates/times to Python objects
        event_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        event_time = datetime.strptime(data.get('time'), '%H:%M').time()
        
        # Check for conflicts
        conflict = Event.check_conflict(event_date, event_time)
        if conflict:
            return jsonify({
                'error': 'Time conflict with existing event',
                'conflicting_event': conflict.to_dict()
            }), 409
        
        # Determine estimated cost based on event type
        event_type = data.get('event_type', 'custom')
        estimated_cost = EVENT_TEMPLATES.get(event_type, {}).get('max_budget', 0) / 2 if event_type != 'custom' else 0
        
        # Create new event
        event = Event(
            title=data.get('title'),
            description=data.get('description', ''),
            date=event_date,
            time=event_time,
            category=data.get('category'),
            budget=data.get('budget', 0),
            estimated_cost=estimated_cost,
            event_type=event_type
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify(event.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a single event by ID"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        return jsonify(event.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        data = request.get_json()
        
        # Check for conflicts if date or time is being changed
        if ('date' in data or 'time' in data):
            new_date = data.get('date')
            new_time = data.get('time')
            
            # Convert strings to Python objects if provided
            if new_date:
                new_date = datetime.strptime(new_date, '%Y-%m-%d').date()
            else:
                new_date = event.date
            
            if new_time:
                new_time = datetime.strptime(new_time, '%H:%M').time()
            else:
                new_time = event.time
            
            conflict = Event.check_conflict(new_date, new_time, exclude_id=event_id)
            if conflict:
                return jsonify({
                    'error': 'Time conflict with existing event',
                    'conflicting_event': conflict.to_dict()
                }), 409
        
        # Update fields
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            event.time = datetime.strptime(data['time'], '%H:%M').time()
        if 'category' in data:
            event.category = data['category']
        if 'budget' in data:
            event.budget = data['budget']
        if 'event_type' in data:
            event.event_type = data['event_type']
        
        db.session.commit()
        return jsonify(event.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'message': 'Event deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        categories = db.session.query(Event.category).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        return jsonify(categories), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-templates', methods=['GET'])
def get_event_templates():
    """Get all event templates"""
    return jsonify(EVENT_TEMPLATES), 200


@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get event suggestions based on budget"""
    try:
        data = request.get_json()
        budget = data.get('budget')
        
        if not budget or budget <= 0:
            return jsonify({'error': 'Invalid budget amount'}), 400
        
        # Filter templates based on budget
        suggestions = []
        for key, template in EVENT_TEMPLATES.items():
            if template['min_budget'] <= budget <= template['max_budget']:
                suggestions.append({'type': key, **template})
        
        suggestions.sort(key=lambda x: x['min_budget'])
        return jsonify(suggestions), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
