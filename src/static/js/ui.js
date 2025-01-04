// Debug logging
console.log('UI.js loaded successfully');

// Direct tab functionality
function switchTab(tabName) {
    console.log('Switching to tab:', tabName);
    
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-section');
    const selectedButton = document.querySelector(`[data-tab="${tabName}"]`);
    
    if (selectedTab && selectedButton) {
        selectedTab.style.display = 'block';
        selectedTab.classList.add('active');
        selectedButton.classList.add('active');
    }
}

// Initialize tabs when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing tabs');
    
    // Add click handlers to all tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
    
    // Show default tab
    switchTab('templates');
});
