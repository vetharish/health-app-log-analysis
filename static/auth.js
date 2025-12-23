// auth.js - Shared authentication utilities for frontend pages

const AUTH = {
  getToken: () => localStorage.getItem('auth_token'),
  setToken: (token) => localStorage.setItem('auth_token', token),
  clearToken: () => localStorage.removeItem('auth_token'),
  
  isAuthenticated: () => !!AUTH.getToken(),
  
  // Check auth and redirect to login if needed
  requireAuth: () => {
    if (!AUTH.isAuthenticated()) {
      document.body.innerHTML = `
        <div class="alert alert-warning m-4">
          <h4>Authentication Required</h4>
          <p>Please <a href="/">login</a> first to access this page.</p>
        </div>
      `;
      return false;
    }
    return true;
  },
  
  // Fetch with auth header
  fetchWithAuth: async (url, options = {}) => {
    const token = AUTH.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return fetch(url, { ...options, headers });
  }
};
