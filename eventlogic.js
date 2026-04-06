/**
 * EventLogic System - JavaScript Utilities
 * Common functions for all pages
 */

// ============================================================================
// ALERTS
// ============================================================================

function closeAlert(button) {
    const alert = button.closest('.alert');
    if (alert) {
        alert.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => alert.remove(), 300);
    }
}

// Auto-close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeBtn = alert.querySelector('.alert-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });
});

// ============================================================================
// FORM VALIDATION
// ============================================================================

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const email = form.querySelector('input[type="email"]');
    const password = form.querySelector('input[type="password"]');

    if (email && !validateEmail(email.value)) {
        alert('Please enter a valid email address');
        email.focus();
        return false;
    }

    if (password && !validatePassword(password.value)) {
        alert('Password must be at least 6 characters');
        password.focus();
        return false;
    }

    return true;
}

// ============================================================================
// BUDGET INPUT - INTERACTIVE SLIDER
// ============================================================================

class BudgetPlanner {
    constructor() {
        this.minBudget = 100;
        this.maxBudget = 100000;
        this.slider = document.getElementById('budget-slider');
        this.input = document.getElementById('budget-input');
        this.display = document.getElementById('budget-display');

        if (this.slider && this.input) {
            this.slider.addEventListener('input', (e) => this.updateBudget(e.target.value));
            this.input.addEventListener('input', (e) => this.updateSlider(e.target.value));
        }
    }

    updateBudget(value) {
        value = Math.max(this.minBudget, Math.min(this.maxBudget, value));
        this.input.value = value;
        this.updateDisplay(value);
    }

    updateSlider(value) {
        value = Math.max(this.minBudget, Math.min(this.maxBudget, value));
        this.slider.value = value;
        this.updateDisplay(value);
    }

    updateDisplay(value) {
        if (this.display) {
            this.display.textContent = '$' + parseInt(value).toLocaleString();
        }
        this.updateBreakdown(value);
    }

    updateBreakdown(total) {
        const breakdown = {
            venue: Math.round(total * 0.35),
            catering: Math.round(total * 0.25),
            photography: Math.round(total * 0.15),
            decoration: Math.round(total * 0.15),
            music: Math.round(total * 0.10)
        };

        for (const [category, amount] of Object.entries(breakdown)) {
            const element = document.getElementById(`${category}-budget`);
            if (element) {
                element.textContent = '$' + amount.toLocaleString();
            }
        }
    }

    setPreset(amount) {
        this.updateBudget(amount);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new BudgetPlanner();
});

// ============================================================================
// API HELPERS
// ============================================================================

async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

async function searchServices(category, maxPrice) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (maxPrice) params.append('max_price', maxPrice);

    return fetchData(`/api/services/search?${params.toString()}`);
}

// ============================================================================
// RECOMMENDATION ENGINE - CLIENT SIDE
// ============================================================================

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    if (!container) return;

    const html = Object.entries(recommendations).map(([tier, config]) => `
        <div class="package-card ${tier === 'standard' ? 'featured' : ''}">
            <div class="package-header">
                <h3 class="package-name">${config.name}</h3>
                <p class="package-price">$${Math.round(config.price).toLocaleString()}</p>
            </div>
            <div class="package-body">
                <p class="package-description">${config.description}</p>
                <ul class="package-services">
                    ${config.services.map(s => `
                        <li>${s.category}: ${s.name} - $${s.price}</li>
                    `).join('')}
                </ul>
            </div>
            <div class="package-footer">
                <button class="btn btn-primary btn-block" onclick="selectPackage('${tier}', ${config.price})">
                    Select ${config.name}
                </button>
            </div>
        </div>
    `).join('');

    container.innerHTML = html;
}

function selectPackage(tier, price) {
    const form = document.getElementById('package-form');
    if (form) {
        const input = form.querySelector('input[name="package_tier"]');
        if (input) input.value = tier;
        form.submit();
    }
}

// ============================================================================
// TABLE FILTERING & SORTING
// ============================================================================

class DataTable {
    constructor(tableId) {
        this.table = document.getElementById(tableId);
        if (!this.table) return;

        this.rows = Array.from(this.table.querySelectorAll('tbody tr'));
        this.setupSearch();
        this.setupSort();
    }

    setupSearch() {
        const searchInput = this.table.parentElement.querySelector('.table-search');
        if (!searchInput) return;

        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            this.rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(term) ? '' : 'none';
            });
        });
    }

    setupSort() {
        const headers = this.table.querySelectorAll('th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => this.sortByColumn(index));
        });
    }

    sortByColumn(columnIndex) {
        this.rows.sort((a, b) => {
            const aValue = a.children[columnIndex].textContent;
            const bValue = b.children[columnIndex].textContent;

            if (!isNaN(aValue) && !isNaN(bValue)) {
                return aValue - bValue;
            }

            return aValue.localeCompare(bValue);
        });

        const tbody = this.table.querySelector('tbody');
        this.rows.forEach(row => tbody.appendChild(row));
    }
}

// Initialize tables on page load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('table').forEach(table => {
        new DataTable(table.id);
    });
});

// ============================================================================
// MODAL DIALOGS
// ============================================================================

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking outside content
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// ============================================================================
// PAYMENT FORM
// ============================================================================

function validatePaymentForm() {
    const form = document.getElementById('payment-form');
    if (!form) return true;

    const cardNumber = form.querySelector('input[name="card_number"]')?.value || '';
    const cvv = form.querySelector('input[name="cvv"]')?.value || '';
    const expiry = form.querySelector('input[name="expiry"]')?.value || '';

    // Basic validation
    if (cardNumber.replace(/\s/g, '').length < 13) {
        alert('Please enter a valid card number');
        return false;
    }

    if (cvv.length < 3) {
        alert('Please enter a valid CVV');
        return false;
    }

    if (!expiry || expiry.length < 5) {
        alert('Please enter expiry date in MM/YY format');
        return false;
    }

    return true;
}

function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '');
    let formattedValue = '';
    for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 4 === 0) formattedValue += ' ';
        formattedValue += value[i];
    }
    input.value = formattedValue;
}

// ============================================================================
// CONFIRMATION DIALOGS
// ============================================================================

function confirmDelete(message = 'Are you sure you want to delete this?') {
    return confirm(message);
}

function confirmSubmit(message = 'Are you sure?') {
    return confirm(message);
}

// ============================================================================
// LOADING STATE
// ============================================================================

function setLoading(elementId, isLoading) {
    const element = document.getElementById(elementId);
    if (!element) return;

    if (isLoading) {
        element.classList.add('loading');
        element.disabled = true;
    } else {
        element.classList.remove('loading');
        element.disabled = false;
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatCurrency(amount) {
    return '$' + parseFloat(amount).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getStatusBadgeClass(status) {
    const classes = {
        'pending': 'status-pending',
        'confirmed': 'status-confirmed',
        'completed': 'status-completed',
        'cancelled': 'status-cancelled',
        'disputed': 'status-disputed'
    };
    return classes[status] || 'status-pending';
}

// ============================================================================
// EVENT DELEGATION
// ============================================================================

document.addEventListener('click', function(e) {
    // Alert close buttons
    if (e.target.classList.contains('alert-close')) {
        closeAlert(e.target);
    }

    // Confirm delete buttons
    if (e.target.classList.contains('btn-delete')) {
        if (!confirmDelete('Are you sure you want to delete this?')) {
            e.preventDefault();
        }
    }

    // Confirm action buttons
    if (e.target.classList.contains('btn-confirm')) {
        if (!confirmSubmit('Please confirm this action')) {
            e.preventDefault();
        }
    }
});

// ============================================================================
// KEYBOARD SHORTCUTS
// ============================================================================

document.addEventListener('keydown', function(e) {
    // ESC to close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    // CTRL+S to save form
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const form = document.querySelector('form[data-auto-save]');
        if (form) form.submit();
    }
});

// ============================================================================
// ANIMATION KEYFRAMES
// ============================================================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
`;
document.head.appendChild(style);

// ============================================================================
// CONSOLE MESSAGE
// ============================================================================

console.log('%cEventLogic System', 'font-size: 20px; font-weight: bold; color: #6366f1;');
console.log('%cVersion 1.0.0', 'color: #64748b;');
console.log('%c© 2024 EventLogic - Complete Event Planning Platform', 'color: #64748b; font-size: 12px;');
