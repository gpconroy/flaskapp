// Optional: Add client-side form validation and enhancements
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.search-form');
    const input = document.querySelector('.input-field');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Trim whitespace
            input.value = input.value.trim();
            
            // Validate that city name only contains letters, spaces, and hyphens
            const cityRegex = /^[a-zA-Z\s\-']+$/;
            if (input.value && !cityRegex.test(input.value)) {
                e.preventDefault();
                alert('Please enter a valid city name (letters, spaces, and hyphens only)');
                return false;
            }
        });
        
        // Add visual feedback when user starts typing
        input.addEventListener('focus', function() {
            this.style.borderColor = '#667eea';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '#e0e0e0';
        });
    }
});
