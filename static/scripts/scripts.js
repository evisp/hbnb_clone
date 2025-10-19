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

// Get place ID from URL
function getPlaceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

// Fetch place details
async function fetchPlaceDetails(placeId) {
    try {
        const token = getToken();
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            fetchPlaceReviews(placeId);
        } else {
            document.getElementById('place-details').innerHTML = '<p>Failed to load place details.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        document.getElementById('place-details').innerHTML = '<p>Network error. Please try again.</p>';
    }
}

// Display place details
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    
    // Get amenities HTML
    let amenitiesHTML = '';
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHTML = '<div class="amenities"><h3>Amenities</h3><ul>';
        place.amenities.forEach(amenity => {
            amenitiesHTML += `<li>${amenity.name}</li>`;
        });
        amenitiesHTML += '</ul></div>';
    }
    
    placeDetails.innerHTML = `
        <div class="place-info">
            <h1>${place.title}</h1>
            <p class="place-price">$${place.price} / night</p>
            <p class="place-host">Host: ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
            <p class="place-description">${place.description || 'No description available'}</p>
            <p class="place-location">Location: ${place.latitude}, ${place.longitude}</p>
            ${amenitiesHTML}
        </div>
    `;
}

// Fetch place reviews
async function fetchPlaceReviews(placeId) {
    try {
        const response = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            document.getElementById('reviews-list').innerHTML = '<p>No reviews yet.</p>';
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        document.getElementById('reviews-list').innerHTML = '<p>Failed to load reviews.</p>';
    }
}

// Display reviews - CORRECTED FIELD NAME
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }
    
    reviewsList.innerHTML = '';
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        const userName = review.user ? `${review.user.first_name} ${review.user.last_name}` : 'Anonymous';
        const rating = '⭐'.repeat(review.rating);
        
        reviewCard.innerHTML = `
            <div class="review-header">
                <span class="review-author">${userName}</span>
                <span class="review-rating">${rating} (${review.rating}/5)</span>
            </div>
            <p class="review-comment">${review.text}</p>
        `;
        
        reviewsList.appendChild(reviewCard);
    });
}

// Submit review - CORRECTED FIELD NAME
async function submitReview(placeId, rating, comment) {
    const token = getToken();
    if (!token) {
        alert('You must be logged in to submit a review');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                rating: parseInt(rating),
                text: comment  // Changed from "comment" to "text"
            })
        });
        
        const reviewError = document.getElementById('review-error');
        
        if (response.ok) {
            reviewError.style.color = 'green';
            reviewError.textContent = 'Review submitted successfully!';
            document.getElementById('review-form').reset();
            // Refresh reviews
            fetchPlaceReviews(placeId);
        } else {
            const data = await response.json();
            reviewError.style.color = 'red';
            reviewError.textContent = data.error || 'Failed to submit review';
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        document.getElementById('review-error').textContent = 'Network error. Please try again.';
    }
}


// Fetch places from API
async function fetchPlaces() {
    try {
        const token = getToken();
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
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
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price;
        
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
                    setCookie('token', data.access_token);
                    
                    errorMessage.textContent = '';
                    errorMessage.style.color = 'green';
                    errorMessage.textContent = 'Login successful! Redirecting...';
                    
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
    
    // Setup price filter event listener (for index page)
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }
    
    // Setup review form (for place details page)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const placeId = getPlaceIdFromURL();
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;
            
            await submitReview(placeId, rating, comment);
        });
    }
    
    // Check if we're on place details page
    if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        fetchPlaceDetails(placeId);
        
        // Show add review form if authenticated
        const addReviewSection = document.getElementById('add-review');
        if (isAuthenticated() && addReviewSection) {
            addReviewSection.style.display = 'block';
        }
    }
    
    // Check authentication status and fetch places on index page
    checkAuthStatus();
});

// Function to update login button based on authentication
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
    
    // Fetch places if on index page
    if (document.getElementById('places-list')) {
        fetchPlaces();
    }
}

// Add review page functionality (for add_review.html standalone page)
if (document.getElementById('add-review-form')) {
    document.addEventListener('DOMContentLoaded', () => {
        // Check authentication
        const token = getToken();
        if (!token) {
            // Redirect to index if not authenticated
            window.location.href = '/';
            return;
        }
        
        // Get place ID from URL
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            alert('Invalid place ID');
            window.location.href = '/';
            return;
        }
        
        // Setup form submission
        const addReviewForm = document.getElementById('add-review-form');
        addReviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const rating = document.getElementById('review-rating').value;
            const text = document.getElementById('review-text').value;
            const reviewMessage = document.getElementById('review-message');
            
            try {
                const response = await fetch(`${API_URL}/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        rating: parseInt(rating),
                        text: text
                    })
                });
                
                if (response.ok) {
                    reviewMessage.style.color = 'green';
                    reviewMessage.textContent = 'Review submitted successfully! Redirecting...';
                    addReviewForm.reset();
                    
                    // Redirect back to place details after 2 seconds
                    setTimeout(() => {
                        window.location.href = `/place/${placeId}`;
                    }, 2000);
                } else {
                    const data = await response.json();
                    reviewMessage.style.color = 'red';
                    reviewMessage.textContent = data.error || 'Failed to submit review';
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                reviewMessage.style.color = 'red';
                reviewMessage.textContent = 'Network error. Please try again.';
            }
        });
        
        checkAuthStatus();
    });
}
