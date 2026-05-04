// js/api.js - सबै pages ले यो use गर्छ
const API = 'http://127.0.0.1:8000';

function getToken() {
    const token = localStorage.getItem('access');
    if (!token) window.location.href = 'login.html';
    return token;
}

function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
}

async function apiFetch(endpoint, options = {}) {
    const res = await fetch(`${API}${endpoint}`, {
        headers: authHeaders(),
        ...options
    });
    if (res.status === 401) {
        localStorage.clear();
        window.location.href = 'login.html';
    }
    return res;
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}