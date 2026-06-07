document.addEventListener('DOMContentLoaded', function() {
    // Initialize socket.io connection
    var socket = io();
    
    // Listen for fridge updates
    socket.on('fridge_updated', function(data) {
        // Reload the page when fridges are updated
        location.reload();
    });
    
    // Initialize checkboxes for shopping list
    initShoppingListCheckboxes();
});

/**
 * Shows a toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of notification: 'success', 'warning', or 'error'
 */
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    
    if (!toast) return;
    
    // Set the message
    toast.textContent = message;
    
    // Add the appropriate class
    toast.className = 'toast';
    if (type === 'success') {
        toast.classList.add('toast-success');
    } else if (type === 'warning') {
        toast.classList.add('toast-warning');
    } else if (type === 'error') {
        toast.classList.add('toast-error');
    }
    
    // Show the toast
    toast.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

/**
 * Toggle recipe details visibility
 */
function toggleDetails() {
    const details = document.getElementById('details');
    if (details) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
    }
}

/**
 * Go back to plan another meal
 */
function planAnotherMeal() {
    const resultsSection = document.getElementById('results-section');
    const mainForm = document.getElementById('main-form');
    
    if (resultsSection && mainForm) {
        resultsSection.style.display = 'none';
        mainForm.style.display = 'block';
    }
}

/**
 * Initialize shopping list checkbox functionality
 */
function initShoppingListCheckboxes() {
    const checkboxes = document.querySelectorAll('#shopping-list input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.checked) {
                label.style.textDecoration = 'line-through';
                label.style.color = '#999';
            } else {
                label.style.textDecoration = 'none';
                label.style.color = '';
            }
        });
    });
} 