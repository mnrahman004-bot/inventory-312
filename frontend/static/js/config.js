// Configuration for Frontend Application

const PROD_API_URL = 'https://your-production-backend.onrender.com/api';
const LOCAL_API_URL = 'http://localhost:5000/api';

// Determine if we are running locally or in production
const isLocalhost = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1' || 
                    window.location.hostname === '' || 
                    window.location.protocol === 'file:';

// Set the global API base URL
const API_BASE = isLocalhost ? LOCAL_API_URL : PROD_API_URL;

// Helper to check authentication
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const path = window.location.pathname;
    
    // Don't redirect if we're on login or index page
    if (!token && !path.endsWith('login.html') && !path.endsWith('index.html') && path !== '/' && path !== '') {
        window.location.href = 'login.html';
    }
    
    const user = JSON.parse(localStorage.getItem('user'));
    const userNameElement = document.getElementById('userName');
    if (user && userNameElement) {
        userNameElement.textContent = user.username;
    }
}

// Global logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
