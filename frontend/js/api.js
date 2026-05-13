const API = 'http://127.0.0.1:8000';

// ── Token Helpers ──
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

// ── Token Refresh ──
async function refreshToken() {
    const refresh = localStorage.getItem('refresh');

    // Refresh token नै छैन भने login मा पठाउ
    if (!refresh) {
        localStorage.clear();
        window.location.href = 'login.html';
        return false;
    }

    const res = await fetch(`${API}/api/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });

    if (res.ok) {
        const data = await res.json();
        // नयाँ access token save गर
        localStorage.setItem('access', data.access);
        return true;
    } else {
        // Refresh token पनि expire भयो - re-login
        localStorage.clear();
        window.location.href = 'login.html';
        return false;
    }
}

// ── Smart API Fetch ──
// Token expire भयो भने automatically refresh गरेर retry गर्छ
async function apiFetch(endpoint, options = {}) {
    let res = await fetch(`${API}${endpoint}`, {
        headers: authHeaders(),
        ...options
    });

    // 401 = Token expired
    if (res.status === 401) {
        const refreshed = await refreshToken();

        if (refreshed) {
            // नयाँ token लिएर same request retry गर
            res = await fetch(`${API}${endpoint}`, {
                headers: authHeaders(), // ← नयाँ token सहित
                ...options
            });
        }
    }

    return res;
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}