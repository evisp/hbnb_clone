const API_URL = 'http://127.0.0.1:5000/api/v1';

// Global variable to store all places for filtering
let allPlaces = [];

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

// Fetch places from API
async function fetchPlaces() {
    try {
        const token = getToken();
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const places = await response.json();
            allPlaces = places; // Store for filtering
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            document.getElementById('places-list').innerHTML = '<p>Failed to load places. Please try again later.</p>';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        document.getElementById('places-list').innerHTML = '<p>Network error. Please try again later.</p>';
    }
}

// Display places as cards
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Clear current content
    
    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price; // Store price for filtering
        
        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p class="place-price">$${place.price} / night</p>
            <p class="place-description">${place.description || 'No description available'}</p>
            <button class="details-button" onclick="window.location.href='/place/${place.id}'">View Details</button>
        `;
        
        placesList.appendChild(placeCard);
    });
}

// Filter places by price
function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
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
    
    // Setup price filter event listener
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }
    
    // Check authentication status and fetch places on page load
    checkAuthStatus();
});

// Function to update login button based on authentication and fetch places
function checkAuthStatus() {
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (isAuthenticated()) {
            loginLink.textContent = 'Logout';
            loginLink.onclick = (e) => {
                e.preventDefault();
                deleteCookie('token');
                window.location.href = '/login';
            };
        } else {
            loginLink.textContent = 'Login';
            loginLink.href = '/login';
        }
    }
    
    // Fetch places regardless of authentication status
    // (API will return public places or all places based on token)
    fetchPlaces();
}
