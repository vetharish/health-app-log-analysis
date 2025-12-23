# Health App API Documentation

## Overview
REST API built with Flask for analyzing health logs including user logins and heart rate data.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API
```bash
python api.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### 1. **Home** - Health Check
- **URL**: `/`
- **Method**: GET
- **Response**: API status and available endpoints

**Example**:
```bash
curl http://localhost:5000/
```

---

### 2. **Summary** - Overall Health Data
- **URL**: `/api/summary`
- **Method**: GET
- **Response**: Total users, successful logins, and average heart rate

**Example**:
```bash
curl http://localhost:5000/api/summary
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_users": 5,
    "successful_logins": 15,
    "average_heart_rate": 75.5,
    "total_logs": 50
  }
}
```

---

### 3. **Users** - Get All Users
- **URL**: `/api/users`
- **Method**: GET
- **Response**: List of all users in the system

**Example**:
```bash
curl http://localhost:5000/api/users
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_users": 5,
    "users": ["alice", "bob", "charlie", "diana", "eve"]
  }
}
```

---

### 4. **Login Statistics** - Login Data
- **URL**: `/api/logins`
- **Method**: GET
- **Response**: Total logins, successful/failed counts, and success rate

**Example**:
```bash
curl http://localhost:5000/api/logins
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_logins": 20,
    "successful_logins": 18,
    "failed_logins": 2,
    "success_rate": 90.0
  }
}
```

---

### 5. **Heart Rate Stats** - Overall Heart Rate Data
- **URL**: `/api/heart-rate`
- **Method**: GET
- **Response**: Heart rate readings count, average, min, and max

**Example**:
```bash
curl http://localhost:5000/api/heart-rate
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_readings": 25,
    "average": 75.5,
    "min": 60,
    "max": 95
  }
}
```

---

### 6. **User Info** - Get Specific User Data
- **URL**: `/api/user/<username>`
- **Method**: GET
- **Parameters**: 
  - `username` (path parameter): The username to query

**Example**:
```bash
curl http://localhost:5000/api/user/alice
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "username": "alice",
    "total_logs": 10,
    "login_attempts": 4,
    "successful_logins": 4
  }
}
```

---

### 7. **User Heart Rate** - Get User's Heart Rate Data
- **URL**: `/api/user/<username>/heart-rate`
- **Method**: GET
- **Parameters**: 
  - `username` (path parameter): The username to query

**Example**:
```bash
curl http://localhost:5000/api/user/alice/heart-rate
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "username": "alice",
    "readings": 5,
    "average": 74.2,
    "min": 65,
    "max": 85,
    "heart_rate_history": [
      {
        "date": "2024-01-01",
        "heart_rate": 72
      },
      {
        "date": "2024-01-02",
        "heart_rate": 75
      }
    ]
  }
}
```

---

### 8. **User-wise Heart Rate** - All Users' Average Heart Rates
- **URL**: `/api/user-wise-heart-rate`
- **Method**: GET
- **Response**: Average heart rate for each user

**Example**:
```bash
curl http://localhost:5000/api/user-wise-heart-rate
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "alice": 74.2,
    "bob": 72.5,
    "charlie": 76.8,
    "diana": 73.1,
    "eve": 75.9
  }
}
```

---

## Error Handling

All errors return a JSON response with a status and error message.

**Example Error Response** (404):
```json
{
  "status": "error",
  "message": "User 'unknown' not found"
}
```

**Example Error Response** (500):
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## Testing with cURL

### Quick Test Script
```bash
# Test home endpoint
curl http://localhost:5000/

# Test summary
curl http://localhost:5000/api/summary

# Test users
curl http://localhost:5000/api/users

# Test logins
curl http://localhost:5000/api/logins

# Test heart rate
curl http://localhost:5000/api/heart-rate

# Test user-wise heart rate
curl http://localhost:5000/api/user-wise-heart-rate
```

### Windows PowerShell Example
```powershell
$Uri = "http://localhost:5000/api/summary"
$Response = Invoke-WebRequest -Uri $Uri -Method Get
$Response.Content | ConvertFrom-Json | ConvertTo-Json
```

---

## File Structure
```
health/
├── api.py                 # Main API file
├── health_app.py          # Pure Python analysis
├── health_app_pandas.py   # Pandas-based analysis
├── health_app_menu.py     # Menu-driven interface
├── health_logs.txt        # Log data file
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## Notes

- Ensure `health_logs.txt` is in the same directory as `api.py`
- The API runs in debug mode by default
- Change `debug=False` in `api.py` for production use
- Default port is 5000 (changeable in the run configuration)

---

## Future Enhancements

- Add database integration (SQLite, PostgreSQL)
- Add authentication (JWT tokens)
- Add data validation and error handling
- Add API rate limiting
- Add Swagger/OpenAPI documentation
- Add user registration endpoint
- Add data filtering and search capabilities
