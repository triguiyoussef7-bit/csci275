#!/usr/bin/env python
"""
Bootstrap script - Creates templates and static files for Event Planner
Run this before running app.py
"""

import os
import sys

def create_templates():
    """Create all HTML template files"""
    template_dir = 'templates'
    os.makedirs(template_dir, exist_ok=True)
    
    files = {
        'layout.html': '''<!DOCTYPE html>
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
</html>''',

        'index.html': '''{% extends "layout.html" %}

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
{% endblock %}''',

        'create.html': '''{% extends "layout.html" %}

{% block title %}Create Event - Event Planner{% endblock %}

{% block content %}
<section class="form-container">
    <h1>Create New Event</h1>

    <form id="event-form" class="event-form">
        <div class="form-group">
            <label for="title">Event Title *</label>
            <input type="text" id="title" name="title" required placeholder="Enter event title" />
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" placeholder="Enter event description"></textarea>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="date">Date *</label>
                <input type="date" id="date" name="date" required />
            </div>

            <div class="form-group">
                <label for="time">Time *</label>
                <input type="time" id="time" name="time" required />
            </div>
        </div>

        <div class="form-group">
            <label for="category">Category *</label>
            <input type="text" id="category" name="category" required placeholder="e.g., Meeting, Birthday, Conference" />
        </div>

        <div class="form-actions">
            <button type="submit" class="btn-primary">Create Event</button>
            <a href="/" class="btn-secondary">Cancel</a>
        </div>
    </form>

    <div id="error-message" class="error-message" style="display: none;"></div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    document.getElementById('event-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const category = document.getElementById('category').value.trim();

        if (!title || !date || !time || !category) {
            showError('Please fill in all required fields');
            return;
        }

        try {
            const response = await fetch('/api/events', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title,
                    description,
                    date,
                    time,
                    category
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert('Event created successfully!');
                window.location.href = '/';
            } else if (response.status === 409) {
                showError(`Time conflict: An event already exists at ${date} ${time}`);
            } else {
                showError(result.error || 'Failed to create event');
            }
        } catch (error) {
            console.error('Error creating event:', error);
            showError('Failed to create event');
        }
    });

    function showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
</script>
{% endblock %}''',

        'edit.html': '''{% extends "layout.html" %}

{% block title %}Edit Event - Event Planner{% endblock %}

{% block content %}
<section class="form-container">
    <h1>Edit Event</h1>

    <form id="event-form" class="event-form">
        <div class="form-group">
            <label for="title">Event Title *</label>
            <input type="text" id="title" name="title" required placeholder="Enter event title" value="{{ event.title }}" />
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" placeholder="Enter event description">{{ event.description }}</textarea>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="date">Date *</label>
                <input type="date" id="date" name="date" required value="{{ event.date.isoformat() }}" />
            </div>

            <div class="form-group">
                <label for="time">Time *</label>
                <input type="time" id="time" name="time" required value="{{ event.time.isoformat() }}" />
            </div>
        </div>

        <div class="form-group">
            <label for="category">Category *</label>
            <input type="text" id="category" name="category" required placeholder="e.g., Meeting, Birthday, Conference" value="{{ event.category }}" />
        </div>

        <div class="form-actions">
            <button type="submit" class="btn-primary">Update Event</button>
            <a href="/" class="btn-secondary">Cancel</a>
        </div>
    </form>

    <div id="error-message" class="error-message" style="display: none;"></div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    const eventId = {{ event.id }};

    document.getElementById('event-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const category = document.getElementById('category').value.trim();

        if (!title || !date || !time || !category) {
            showError('Please fill in all required fields');
            return;
        }

        try {
            const response = await fetch(`/api/events/${eventId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title,
                    description,
                    date,
                    time,
                    category
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert('Event updated successfully!');
                window.location.href = '/';
            } else if (response.status === 409) {
                showError(`Time conflict: An event already exists at ${date} ${time}`);
            } else {
                showError(result.error || 'Failed to update event');
            }
        } catch (error) {
            console.error('Error updating event:', error);
            showError('Failed to update event');
        }
    });

    function showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
</script>
{% endblock %}'''
    }
    
    for filename, content in files.items():
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created {filepath}")


def create_static():
    """Create all static files (CSS and JS)"""
    static_dir = 'static'
    os.makedirs(static_dir, exist_ok=True)
    
    # CSS file content is very long, so create it separately
    css_file = os.path.join(static_dir, 'style.css')
    js_file = os.path.join(static_dir, 'script.js')
    
    if not os.path.exists(css_file):
        # CSS will be created by calling the function below
        create_css_file(css_file)
        print(f"✓ Created {css_file}")
    
    if not os.path.exists(js_file):
        create_js_file(js_file)
        print(f"✓ Created {js_file}")


def create_css_file(filepath):
    """Create the CSS file"""
    css_content = '''/* ==================== GLOBAL STYLES ==================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --danger-color: #ef4444;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --dark-color: #1f2937;
    --light-color: #f9fafb;
    --border-color: #e5e7eb;
    --text-color: #374151;
    --text-light: #6b7280;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
    --radius: 8px;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    color: var(--text-color);
    background-color: var(--light-color);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* ==================== TYPOGRAPHY ==================== */

h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 10px;
    color: var(--dark-color);
}

h1 {
    font-size: 2.5rem;
}

h2 {
    font-size: 2rem;
}

h3 {
    font-size: 1.5rem;
}

a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.3s;
}

a:hover {
    color: var(--secondary-color);
}

/* ==================== BUTTONS ==================== */

.btn-primary, .btn-secondary, .btn-danger {
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    display: inline-block;
    text-align: center;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-secondary {
    background-color: #d1d5db;
    color: var(--dark-color);
}

.btn-secondary:hover {
    background-color: #9ca3af;
}

.btn-danger {
    background-color: var(--danger-color);
    color: white;
}

.btn-danger:hover {
    background-color: #dc2626;
}

/* ==================== NAVIGATION ==================== */

.navbar {
    background-color: white;
    border-bottom: 1px solid var(--border-color);
    box-shadow: var(--shadow);
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
}

.navbar-brand a {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 30px;
    align-items: center;
}

.nav-links a {
    color: var(--text-color);
    font-weight: 500;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary-color);
}

.nav-links .btn-primary {
    padding: 10px 20px;
    font-size: 0.95rem;
}

/* ==================== FORMS ==================== */

.form-container {
    background-color: white;
    border-radius: var(--radius);
    padding: 40px;
    margin: 40px 0;
    box-shadow: var(--shadow);
}

.event-form {
    max-width: 600px;
    margin: 30px 0;
}

.form-group {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

label {
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--dark-color);
}

input[type="text"], input[type="date"], input[type="time"], select, textarea {
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s;
}

input[type="text"]:focus, input[type="date"]:focus, input[type="time"]:focus, select:focus, textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

textarea {
    resize: vertical;
    min-height: 120px;
}

.form-actions {
    display: flex;
    gap: 15px;
    margin-top: 30px;
}

.form-actions .btn-primary, .form-actions .btn-secondary {
    flex: 1;
    padding: 14px 24px;
}

/* ==================== MESSAGES ==================== */

.error-message {
    background-color: #fee;
    color: var(--danger-color);
    padding: 15px;
    border-radius: var(--radius);
    margin-bottom: 20px;
    border-left: 4px solid var(--danger-color);
}

.success-message {
    background-color: #efe;
    color: var(--success-color);
    padding: 15px;
    border-radius: var(--radius);
    margin-bottom: 20px;
    border-left: 4px solid var(--success-color);
}

/* ==================== EVENTS SECTION ==================== */

.events-container {
    margin: 40px 0;
}

.events-header {
    margin-bottom: 40px;
}

.events-header h1 {
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.1rem;
    color: var(--text-light);
}

/* ==================== FILTERS ==================== */

.filters-section {
    background-color: white;
    padding: 20px;
    border-radius: var(--radius);
    margin-bottom: 30px;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    align-items: flex-end;
    box-shadow: var(--shadow);
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.filter-group label {
    font-size: 0.95rem;
    font-weight: 600;
}

.filter-group input, .filter-group select {
    min-width: 200px;
}

#btn-clear-filters {
    padding: 10px 20px;
}

/* ==================== EVENTS LIST ==================== */

.events-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
}

.event-card {
    background-color: white;
    border-radius: var(--radius);
    padding: 20px;
    box-shadow: var(--shadow);
    transition: all 0.3s;
    display: flex;
    flex-direction: column;
}

.event-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.event-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
}

.event-header h3 {
    margin: 0;
    flex: 1;
}

.event-category {
    background-color: var(--primary-color);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}

.event-description {
    color: var(--text-light);
    margin-bottom: 15px;
    line-height: 1.5;
}

.event-meta {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 15px;
    padding: 15px 0;
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    color: var(--text-light);
    font-size: 0.95rem;
}

.event-actions {
    display: flex;
    gap: 10px;
    margin-top: auto;
}

.event-actions a, .event-actions button {
    flex: 1;
    padding: 10px;
    font-size: 0.9rem;
}

/* ==================== EMPTY STATE ==================== */

.empty-state {
    background-color: white;
    border-radius: var(--radius);
    padding: 60px 20px;
    text-align: center;
    box-shadow: var(--shadow);
    color: var(--text-light);
}

.empty-state p {
    font-size: 1.1rem;
    margin-bottom: 20px;
}

.empty-state a {
    color: var(--primary-color);
    font-weight: 600;
}

/* ==================== LOADING STATE ==================== */

.loading {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-light);
    font-size: 1.1rem;
}

/* ==================== FOOTER ==================== */

.footer {
    background-color: var(--dark-color);
    color: white;
    text-align: center;
    padding: 30px 0;
    margin-top: 60px;
}

.footer p {
    margin: 0;
    font-size: 0.95rem;
}

/* ==================== RESPONSIVE DESIGN ==================== */

@media (max-width: 768px) {
    h1 {
        font-size: 2rem;
    }

    .navbar-content {
        flex-direction: column;
        gap: 20px;
    }

    .nav-links {
        flex-direction: column;
        gap: 15px;
        width: 100%;
    }

    .nav-links a {
        display: block;
        text-align: center;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .filters-section {
        flex-direction: column;
    }

    .filter-group input, .filter-group select {
        width: 100%;
    }

    .events-list {
        grid-template-columns: 1fr;
    }

    .form-actions {
        flex-direction: column;
    }

    .form-container {
        padding: 20px;
    }
}

@media (max-width: 480px) {
    h1 {
        font-size: 1.5rem;
    }

    .container {
        padding: 0 15px;
    }

    .event-header {
        flex-direction: column;
    }

    .event-category {
        align-self: flex-start;
    }
}
'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(css_content)


def create_js_file(filepath):
    """Create the JavaScript file"""
    js_content = '''/**
 * Event Planner - Main JavaScript File
 * Handles client-side interactions and API calls
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Event Planner app loaded');
});

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

function escapeHtml(unsafe) {
    const div = document.createElement('div');
    div.textContent = unsafe;
    return div.innerHTML;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

async function fetchEvents(filters = {}) {
    try {
        const params = new URLSearchParams();
        if (filters.date) params.append('date', filters.date);
        if (filters.category) params.append('category', filters.category);

        const url = `/api/events${params.toString() ? '?' + params.toString() : ''}`;
        const response = await fetch(url);

        if (!response.ok) throw new Error('Failed to fetch events');
        return await response.json();
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
}

async function fetchEvent(eventId) {
    try {
        const response = await fetch(`/api/events/${eventId}`);

        if (!response.ok) throw new Error('Failed to fetch event');
        return await response.json();
    } catch (error) {
        console.error('Error fetching event:', error);
        throw error;
    }
}

async function createEvent(eventData) {
    try {
        const response = await fetch('/api/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to create event');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating event:', error);
        throw error;
    }
}

async function updateEvent(eventId, eventData) {
    try {
        const response = await fetch(`/api/events/${eventId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to update event');
        }

        return await response.json();
    } catch (error) {
        console.error('Error updating event:', error);
        throw error;
    }
}

async function deleteEvent(eventId) {
    try {
        const response = await fetch(`/api/events/${eventId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to delete event');
        }

        return await response.json();
    } catch (error) {
        console.error('Error deleting event:', error);
        throw error;
    }
}

async function fetchCategories() {
    try {
        const response = await fetch('/api/categories');

        if (!response.ok) throw new Error('Failed to fetch categories');
        return await response.json();
    } catch (error) {
        console.error('Error fetching categories:', error);
        throw error;
    }
}
'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)


if __name__ == '__main__':
    print("Creating Event Planner project structure...")
    print()
    
    try:
        create_templates()
        print()
        create_static()
        print()
        print("=" * 80)
        print("✓ Project structure created successfully!")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        print()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
