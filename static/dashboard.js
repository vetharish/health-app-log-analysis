// ================================
// Dashboard JavaScript
// ================================

const API_BASE = '/api';
let token = localStorage.getItem('token');
let username = localStorage.getItem('username');
let loginChart = null;
let heartRateChart = null;

// Check authentication
if (!token) {
    window.location.href = '/';
}

// Set welcome message
document.getElementById('welcomeUser').textContent = `Welcome, ${username}!`;

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', () => {
    fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/';
    });
});

// Helper function to make API requests
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, mergedOptions);
        if (response.status === 401) {
            // Token expired
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            window.location.href = '/';
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Load Summary Data
async function loadSummary() {
    const data = await apiCall('/summary');
    
    if (data && data.status === 'success') {
        document.getElementById('totalUsers').textContent = data.data.total_users;
        document.getElementById('successLogins').textContent = data.data.successful_logins;
        document.getElementById('avgHeartRate').textContent = data.data.average_heart_rate + ' bpm';
        document.getElementById('totalLogs').textContent = data.data.total_logs;
    }
}

// Load Heart Rate Statistics
async function loadHeartRateStats() {
    const data = await apiCall('/heart-rate');
    
    if (data && data.status === 'success') {
        document.getElementById('minHeartRate').textContent = data.data.min + ' bpm';
        document.getElementById('avgHeartRateLarge').textContent = data.data.average + ' bpm';
        document.getElementById('maxHeartRate').textContent = data.data.max + ' bpm';
    }
}

// Load Login Chart
async function loadLoginChart() {
    const data = await apiCall('/logins');
    
    if (data && data.status === 'success') {
        const ctx = document.getElementById('loginChart').getContext('2d');
        
        // Destroy existing chart if any
        if (loginChart) {
            loginChart.destroy();
        }
        
        loginChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Successful', 'Failed'],
                datasets: [{
                    data: [
                        data.data.successful_logins,
                        data.data.failed_logins
                    ],
                    backgroundColor: [
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(25, 135, 84, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed;
                            }
                        }
                    }
                }
            }
        });
    }
}

// Load Heart Rate Chart
async function loadHeartRateChart() {
    const data = await apiCall('/user-wise-heart-rate');
    
    if (data && data.status === 'success') {
        const ctx = document.getElementById('heartRateChart').getContext('2d');
        
        // Destroy existing chart if any
        if (heartRateChart) {
            heartRateChart.destroy();
        }
        
        const users = Object.keys(data.data);
        const rates = Object.values(data.data);
        
        heartRateChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: users,
                datasets: [{
                    label: 'Average Heart Rate (bpm)',
                    data: rates,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'x',
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value + ' bpm';
                            }
                        }
                    }
                }
            }
        });
    }
}

// Load Users List
async function loadUsersList() {
    const data = await apiCall('/users');
    
    if (data && data.status === 'success') {
        const usersList = document.getElementById('usersList');
        usersList.innerHTML = '';
        
        for (const user of data.data.users) {
            const userDiv = document.createElement('div');
            userDiv.className = 'col-md-4';
            
            // Get user info
            const userInfo = await apiCall(`/user/${user}`);
            
            if (userInfo && userInfo.status === 'success') {
                const info = userInfo.data;
                
                userDiv.innerHTML = `
                    <div class="user-card">
                        <h6><i class="bi bi-person-circle"></i> ${info.username}</h6>
                        <p><span class="badge bg-primary">${info.total_logs} Logs</span></p>
                        <small class="text-muted">
                            Logins: ${info.login_attempts} | 
                            Successful: ${info.successful_logins}
                        </small>
                    </div>
                `;
            }
            
            usersList.appendChild(userDiv);
        }
    }
}

// Initialize Dashboard
async function initDashboard() {
    try {
        // Show loading state
        document.body.classList.add('loading');
        
        // Load all data
        await Promise.all([
            loadSummary(),
            loadHeartRateStats(),
            loadLoginChart(),
            loadHeartRateChart(),
            loadUsersList()
        ]);
        
        // Hide loading state
        document.body.classList.remove('loading');
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        alert('Error loading dashboard data');
    }
}

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', initDashboard);

// Refresh dashboard every 30 seconds
setInterval(initDashboard, 30000);
