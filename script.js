/**
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
