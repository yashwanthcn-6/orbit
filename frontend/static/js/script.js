/**
 * StudySaarthi Frontend JavaScript
 * Handles UI interactions and API communication with the backend agent
 */

// ============================================
// Global Configuration
// ============================================

const API_BASE = 'http://localhost:5000/api';
let currentUserId = localStorage.getItem('studysaarthi_user_id') || generateUserId();
let currentSessionData = null;

// Generate unique user ID
function generateUserId() {
    const userId = 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    localStorage.setItem('studysaarthi_user_id', userId);
    return userId;
}

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    updateSessionDisplay();
    setupEventListeners();
    checkAPIHealth();
});

// ============================================
// Event Setup
// ============================================

function setupEventListeners() {
    // Topic input Enter key
    const topicInput = document.getElementById('topic-input');
    topicInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitTopic();
        }
    });

    // Learn button click
    document.getElementById('learn-btn').addEventListener('click', submitTopic);
}

// ============================================
// Session Management
// ============================================

function updateSessionDisplay() {
    const sessionBadge = document.getElementById('session-id');
    const shortId = currentUserId.substring(0, 12) + '...';
    sessionBadge.textContent = `Session: ${shortId}`;
}

// ============================================
// API Communication
// ============================================

/**
 * Check if backend API is healthy
 */
function checkAPIHealth() {
    fetch(`${API_BASE}/health`)
        .then(response => {
            if (!response.ok) throw new Error('Health check failed');
            return response.json();
        })
        .then(data => {
            console.log('✓ API Health Check:', data);
        })
        .catch(error => {
            console.error('✗ API Health Check Failed:', error);
            showError('Backend API is not responding. Please ensure Flask server is running on http://localhost:5000');
        });
}

/**
 * Submit topic to autonomous agent
 */
function submitTopic() {
    const topicInput = document.getElementById('topic-input');
    const topic = topicInput.value.trim();

    // Validate input
    if (!topic) {
        showError('Please enter a topic to learn about');
        return;
    }

    if (topic.length < 2) {
        showError('Topic must be at least 2 characters long');
        return;
    }

    if (topic.length > 100) {
        showError('Topic must be less than 100 characters');
        return;
    }

    // Clear previous errors
    clearError();

    // Show loading state
    setLoadingState(true);

    // Prepare request payload
    const payload = {
        topic: topic,
        user_id: currentUserId
    };

    // Send to backend agent
    fetch(`${API_BASE}/learn`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        setLoadingState(false);

        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'API error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            currentSessionData = data;
            displayResults(data);
            hideFeatures();
            topicInput.value = '';
        } else {
            showError(data.error || 'An error occurred while processing your request');
        }
    })
    .catch(error => {
        setLoadingState(false);
        console.error('Error:', error);

        if (error.message.includes('Failed to fetch')) {
            showError('Cannot connect to backend. Is the Flask server running on http://localhost:5000?');
        } else {
            showError(error.message || 'An error occurred. Please try again.');
        }
    });
}

// ============================================
// Display Results
// ============================================

/**
 * Display agent results on the UI
 */
function displayResults(data) {
    updateModeBanner(data.mode);

    // Update classification card
    document.getElementById('result-topic').textContent = capitalizeWords(data.topic);
    
    const categoryBadge = document.getElementById('category-badge');
    const categoryText = data.category.replace(/_/g, ' ');
    document.getElementById('result-category').textContent = capitalizeWords(categoryText);
    
    // Apply category-specific styling
    categoryBadge.className = 'category-badge category-' + data.category;

    // Update explanation
    document.getElementById('result-explanation').textContent = data.explanation || 'No explanation available';

    // Update notes
    document.getElementById('result-notes').textContent = data.notes || 'No notes available';

    // Update quiz
    document.getElementById('result-quiz').textContent = data.quiz || 'No quiz available';

    // Update next topics
    document.getElementById('result-next-topics').textContent = data.next_topics || 'No suggestions available';

    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Add animation class
    resultsSection.classList.add('fade-in');
}

/**
 * Hide features section when results are shown
 */
function hideFeatures() {
    const featuresSection = document.getElementById('features-section');
    if (featuresSection) {
        featuresSection.style.display = 'none';
    }
}

function updateModeBanner(mode) {
    const banner = document.getElementById('mode-banner');
    if (!banner) {
        return;
    }

    if (mode === 'local') {
        banner.textContent = 'Running in local study mode because OpenAI is currently unavailable.';
        banner.className = 'mode-banner mode-local';
    } else {
        banner.textContent = 'Connected to OpenAI for live AI-generated study content.';
        banner.className = 'mode-banner mode-openai';
    }

    banner.style.display = 'block';
}

// ============================================
// Error Handling
// ============================================

/**
 * Display error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = '❌ ' + message;
    errorDiv.style.display = 'block';
}

/**
 * Clear error message
 */
function clearError() {
    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';
}

// ============================================
// UI State Management
// ============================================

/**
 * Set loading state for submit button
 */
function setLoadingState(isLoading) {
    const learnBtn = document.getElementById('learn-btn');
    const btnText = learnBtn.querySelector('.btn-text');
    const btnLoader = learnBtn.querySelector('.btn-loader');

    if (isLoading) {
        learnBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        learnBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Reset the form to initial state
 */
function resetForm() {
    document.getElementById('topic-input').value = '';
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('features-section').style.display = 'block';
    clearError();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// Utility Functions
// ============================================

/**
 * Capitalize words in a string
 */
function capitalizeWords(str) {
    return str
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('✓ Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('✓ Copied to clipboard!');
    }
}

/**
 * Show temporary notification
 */
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
    `;
    notification.textContent = message;

    // Add animation keyframes if not already present
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ============================================
// Progress and Statistics
// ============================================

/**
 * Display user's learning progress
 */
function viewProgress() {
    fetch(`${API_BASE}/stats/${currentUserId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayStats(data.stats);
            }
        })
        .catch(error => {
            console.error('Error fetching stats:', error);
            showError('Failed to load progress');
        });
}

/**
 * Display statistics and learning progress
 */
function displayStats(stats) {
    // Update stat cards
    document.getElementById('total-sessions').textContent = stats.total_sessions;
    document.getElementById('total-topics').textContent = stats.total_topics;
    document.getElementById('science-topics').textContent = stats.category_breakdown.science_math;
    document.getElementById('history-topics').textContent = stats.category_breakdown.history_gk;

    // Display topics list
    const topicsList = document.getElementById('learned-topics');
    if (stats.topics_learned && stats.topics_learned.length > 0) {
        topicsList.innerHTML = stats.topics_learned
            .map(topic => `<li>📚 ${capitalizeWords(topic)}</li>`)
            .join('');
    } else {
        topicsList.innerHTML = '<li>No topics learned yet</li>';
    }

    // Show progress section and hide results
    document.getElementById('progress-section').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('features-section').style.display = 'none';

    // Scroll to progress
    document.getElementById('progress-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Close progress section
 */
function closeProgress() {
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'block';
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

// ============================================
// Suggested Topic Handling
// ============================================

/**
 * Learn a suggested topic from next topics
 */
function learnFromSuggestion(elementId) {
    const suggestionsText = document.getElementById(elementId).textContent;
    
    // Extract first topic from suggestions (simple parsing)
    const lines = suggestionsText.split('\n');
    let firstTopic = '';
    
    for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('-') && trimmed.length > 2) {
            // Extract topic name (before parenthesis if exists)
            firstTopic = trimmed.split('(')[0].trim();
            break;
        }
    }

    if (firstTopic) {
        document.getElementById('topic-input').value = firstTopic;
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => {
            submitTopic();
        }, 500);
    } else {
        showError('Could not extract topic from suggestions');
    }
}

// ============================================
// Keyboard Shortcuts
// ============================================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const topicInput = document.getElementById('topic-input');
        if (topicInput === document.activeElement) {
            submitTopic();
        }
    }

    // ESC to reset
    if (e.key === 'Escape') {
        if (document.getElementById('results-section').style.display !== 'none') {
            resetForm();
        }
    }
});

console.log('✓ StudySaarthi Frontend Loaded');
console.log('User ID:', currentUserId);
