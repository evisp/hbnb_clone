const API_URL = 'http://127.0.0.1:5000/api/v1';

// Cookie helper functions
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// Helper function to check if user is authenticated
function isAuthenticated() {
    return getCookie('token') !== null;
}

// Helper function to get token
function getToken() {
    return getCookie('token');
}

// Login functionality
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('error-message');
            
            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // Store token in cookie
                    setCookie('token', data.access_token);
                    
                    errorMessage.textContent = '';
                    errorMessage.style.color = 'green';
                    errorMessage.textContent = 'Login successful! Redirecting...';
                    
                    // Redirect to index.html
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    const data = await response.json();
                    errorMessage.style.color = 'red';
                    errorMessage.textContent = data.error || 'Login failed. Please check your credentials.';
                }
            } catch (error) {
                errorMessage.style.color = 'red';
                errorMessage.textContent = 'Network error. Please try again.';
                console.error('Login error:', error);
            }
        });
    }
    
    // Check authentication status on page load
    checkAuthStatus();
});

// Function to update login button based on authentication
function checkAuthStatus() {
    const loginButton = document.querySelector('.login-button-nav');
    
    if (loginButton) {
        if (isAuthenticated()) {
            loginButton.textContent = 'Logout';
            loginButton.onclick = (e) => {
                e.preventDefault();
                deleteCookie('token');
                window.location.href = '/login';
            };
        } else {
            loginButton.textContent = 'Login';
            loginButton.href = '/login';
        }
    }
}
