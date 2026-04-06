"""
Detailed Setup Instructions - Event Planner Application

This file provides step-by-step instructions to complete the Event Planner setup.
"""

# ============================================================================
# STEP 1: CREATE DIRECTORIES (if not auto-created)
# ============================================================================

# If the setup.py doesn't work on your system, manually create these folders:
# - templates/
# - static/

# From command line:
# Windows:
#   mkdir templates
#   mkdir static
#
# Linux/Mac:
#   mkdir -p templates
#   mkdir -p static

# ============================================================================
# STEP 2: CREATE TEMPLATE FILES
# ============================================================================

# File: templates/layout.html
# This is the base template inherited by all other pages

LAYOUT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Event Planner - Manage your events efficiently">
    
    <title>{% block title %}Event Planner{% endblock %}</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    
    <!-- Additional styles for specific pages -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="navbar-content">
                <div class="navbar-brand">
                    <a href="/">📅 Event Planner</a>
                </div>
                <ul class="nav-links">
                    <li><a href="/">Events</a></li>
                    <li><a href="/create" class="btn-primary">+ Create Event</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Event Planner. All rights reserved.</p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="{{ url_for('static', filename='script.js') }}"></script>
    
    <!-- Additional scripts for specific pages -->
    {% block extra_js %}{% endblock %}
</body>
</html>"""

# File: templates/index.html
# Events listing page with filtering

INDEX_HTML = """{% extends "layout.html" %}

{% block title %}Events - Event Planner{% endblock %}

{% block content %}
<section class="events-container">
    <!-- Header -->
    <div class="events-header">
        <h1>My Events</h1>
        <p class="subtitle">Manage and organize your events</p>
    </div>

    <!-- Filters -->
    <div class="filters-section">
        <div class="filter-group">
            <label for="filter-date">Filter by Date:</label>
            <input type="date" id="filter-date" />
        </div>
        <div class="filter-group">
            <label for="filter-category">Filter by Category:</label>
            <select id="filter-category">
                <option value="">All Categories</option>
            </select>
        </div>
        <button id="btn-clear-filters" class="btn-secondary">Clear Filters</button>
    </div>

    <!-- Events List -->
    <div id="events-list" class="events-list">
        <div class="loading">Loading events...</div>
    </div>

    <!-- Empty State -->
    <div id="empty-state" class="empty-state" style="display: none;">
        <p>No events found. <a href="/create">Create your first event</a></p>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', () => {
        loadEvents();
        loadCategories();
        setupEventListeners();
    });

    function setupEventListeners() {
        document.getElementById('filter-date').addEventListener('change', loadEvents);
        document.getElementById('filter-category').addEventListener('change', loadEvents);
        document.getElementById('btn-clear-filters').addEventListener('click', clearFilters);
    }

    function clearFilters() {
        document.getElementById('filter-date').value = '';
        document.getElementById('filter-category').value = '';
        loadEvents();
    }

    async function loadEvents() {
        try {
            const date = document.getElementById('filter-date').value;
            const category = document.getElementById('filter-category').value;

            let url = '/api/events';
            const params = new URLSearchParams();
            if (date) params.append('date', date);
            if (category) params.append('category', category);
            if (params.toString()) url += '?' + params.toString();

            const response = await fetch(url);
            const events = await response.json();

            displayEvents(events);
        } catch (error) {
            console.error('Error loading events:', error);
            showError('Failed to load events');
        }
    }

    function displayEvents(events) {
        const eventsList = document.getElementById('events-list');
        const emptyState = document.getElementById('empty-state');

        if (events.length === 0) {
            eventsList.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        eventsList.style.display = 'grid';
        emptyState.style.display = 'none';

        eventsList.innerHTML = events.map(event => `
            <div class="event-card">
                <div class="event-header">
                    <h3>${escapeHtml(event.title)}</h3>
                    <span class="event-category">${escapeHtml(event.category)}</span>
                </div>
                <p class="event-description">${escapeHtml(event.description)}</p>
                <div class="event-meta">
                    <span class="event-date">📅 ${event.date}</span>
                    <span class="event-time">⏰ ${event.time}</span>
                </div>
                <div class="event-actions">
                    <a href="/edit/${event.id}" class="btn-secondary">Edit</a>
                    <button class="btn-danger" onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    async function loadCategories() {
        try {
            const response = await fetch('/api/categories');
            const categories = await response.json();

            const select = document.getElementById('filter-category');
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    async function deleteEvent(eventId) {
        if (!confirm('Are you sure you want to delete this event?')) return;

        try {
            const response = await fetch(`/api/events/${eventId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                showSuccess('Event deleted successfully');
                loadEvents();
            } else {
                showError('Failed to delete event');
            }
        } catch (error) {
            console.error('Error deleting event:', error);
            showError('Failed to delete event');
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showError(message) {
        console.error(message);
        alert(message);
    }

    function showSuccess(message) {
        console.log(message);
        alert(message);
    }
</script>
{% endblock %}"""

# ============================================================================
# INSTRUCTIONS
# ============================================================================

print(__doc__)
print("\n" + "="*80)
print("QUICK START GUIDE")
print("="*80)

print("""
1. Create the necessary directories:
   - templates/
   - static/

2. Install Python dependencies:
   $ pip install -r requirements.txt

3. Run the setup script:
   $ python setup.py

4. Start the Flask application:
   $ python app.py

5. Open your browser and navigate to:
   http://localhost:5000

""")

print("\n" + "="*80)
print("FILE CONTENTS TO CREATE MANUALLY")
print("="*80)

print("\nCreate: templates/layout.html")
print("-" * 80)
print(LAYOUT_HTML[:500] + "...")

print("\n\nCreate: templates/index.html")
print("-" * 80)
print(INDEX_HTML[:500] + "...")

print("\n\nFor complete file contents, see README.md")
