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
            
            // Save to history
            if (input.value) {
                addToSearchHistory(input.value);
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
    
    // Load and display search history
    displaySearchHistory();
});

// Search History Management
const HISTORY_KEY = 'weatherAppSearchHistory';
const MAX_HISTORY_ITEMS = 5;

function addToSearchHistory(city) {
    let history = getSearchHistory();
    
    // Remove if already exists (to move to top)
    history = history.filter(c => c.toLowerCase() !== city.toLowerCase());
    
    // Add to the beginning
    history.unshift(city);
    
    // Keep only the last 5 items
    history = history.slice(0, MAX_HISTORY_ITEMS);
    
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function getSearchHistory() {
    const stored = localStorage.getItem(HISTORY_KEY);
    return stored ? JSON.parse(stored) : [];
}

function clearSearchHistory() {
    localStorage.removeItem(HISTORY_KEY);
    displaySearchHistory();
}

function displaySearchHistory() {
    const historyContainer = document.querySelector('.search-history');
    if (!historyContainer) return;
    
    const history = getSearchHistory();
    
    // Clear existing history
    historyContainer.innerHTML = '';
    
    if (history.length === 0) {
        historyContainer.style.display = 'none';
        return;
    }
    
    historyContainer.style.display = 'block';
    
    const historyTitle = document.createElement('p');
    historyTitle.className = 'history-title';
    historyTitle.textContent = 'Recent Searches:';
    historyContainer.appendChild(historyTitle);
    
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'history-buttons';
    
    history.forEach(city => {
        const btn = document.createElement('button');
        btn.className = 'history-btn';
        btn.textContent = city;
        btn.type = 'button';
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = document.querySelector('.search-form');
            const input = document.querySelector('.input-field');
            if (input) {
                input.value = city;
            }
            if (form) {
                form.submit();
            }
        });
        buttonsContainer.appendChild(btn);
    });
    
    historyContainer.appendChild(buttonsContainer);
    
    // Add clear history button
    const clearBtn = document.createElement('button');
    clearBtn.className = 'clear-history-btn';
    clearBtn.textContent = 'Clear History';
    clearBtn.type = 'button';
    clearBtn.addEventListener('click', function(e) {
        e.preventDefault();
        clearSearchHistory();
    });
    historyContainer.appendChild(clearBtn);
}
