

const API_BASE_URL = 'http://127.0.0.1:5000/api';


function saveTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
}


function getAccessToken() {
    return localStorage.getItem('access_token');
}


function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}


function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
}


function isAuthenticated() {
    return !!getAccessToken();
}


function saveUserData(userData) {
    localStorage.setItem('user_data', JSON.stringify(userData));
}


function getUserData() {
    const data = localStorage.getItem('user_data');
    return data ? JSON.parse(data) : null;
}


async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;


    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };


    const token = getAccessToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        const data = await response.json();

        if (!response.ok) {
            throw {
                status: response.status,
                message: data.error || data.msg || 'An error occurred',
                data: data
            };
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}


async function login(email, password) {
    const data = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
    });

    saveTokens(data.access_token, data.refresh_token);
    saveUserData(data.user);

    return data;
}

async function register(userData) {
    const data = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
    });

    return data;
}

async function getCurrentUser() {
    const data = await apiCall('/auth/me', {
        method: 'GET'
    });

    saveUserData(data.user);

    return data.user;
}


async function logout() {
    try {
        await apiCall('/auth/logout', {
            method: 'POST'
        });
    } catch (error) {
        console.error('Logout API error:', error);
    } finally {
        clearTokens();
    }
}


async function refreshAccessToken() {
    const refreshToken = getRefreshToken();

    if (!refreshToken) {
        throw new Error('No refresh token available');
    }

    const data = await apiCall('/auth/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${refreshToken}`
        }
    });

    localStorage.setItem('access_token', data.access_token);

    return data.access_token;
}


function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.add('show');


        setTimeout(() => {
            element.classList.remove('show');
        }, 5000);
    }
}


function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.add('show');


        setTimeout(() => {
            element.classList.remove('show');
        }, 5000);
    }
}


function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('show');
    }
}


function redirectTo(page) {
    window.location.href = page;
}


function formatRole(role) {
    const roleMap = {
        'admin': 'Quản trị viên',
        'teacher': 'Giáo viên',
        'parent': 'Phụ huynh'
    };
    return roleMap[role] || role;
}


function formatDate(dateString) {
    if (!dateString) return 'N/A';

    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}


function requireAuth() {
    if (!isAuthenticated()) {
        redirectTo('/api/auth/login-page');
        return false;
    }
    return true;
}


function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        redirectTo('/api/auth/dashboard-page');
        return true;
    }
    return false;
}


console.log('🔐 Auth module loaded');
console.log('📍 API Base URL:', API_BASE_URL);
console.log('✅ Authenticated:', isAuthenticated());