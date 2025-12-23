# JWT Authentication Guide

## Overview
The Health App API now includes JWT (JSON Web Token) authentication. All endpoints require a valid token except for the authentication endpoints.

## Default Credentials

Use these credentials to test the API:

```
username: admin
password: admin123

username: user01
password: password1

username: user02
password: password2

username: user03
password: password3
```

## Authentication Endpoints

### 1. Register New User
**Endpoint**: `POST /api/auth/register`

**Request**:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "newpassword123"
  }'
```

**Response**:
```json
{
  "status": "success",
  "message": "User 'newuser' registered successfully"
}
```

---

### 2. Login
**Endpoint**: `POST /api/auth/login`

This endpoint generates a JWT token valid for 24 hours.

**Request**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response**:
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "username": "admin",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzAzNDEwMDAwLCJpYXQiOjE3MDMzMjMwMDB9.xxxxx",
    "expires_in_hours": 24
  }
}
```

**Copy the token** from the response to use with protected endpoints.

---

### 3. Logout
**Endpoint**: `POST /api/auth/logout`

Requires authentication.

**Request**:
```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Response**:
```json
{
  "status": "success",
  "message": "Logout successful. Please discard the token.",
  "data": {
    "username": "admin"
  }
}
```

---

## Using Protected Endpoints

All data endpoints now require a valid JWT token in the `Authorization` header.

### Header Format
```
Authorization: Bearer <TOKEN>
```

### Example: Get Summary with Authentication

**Step 1: Login and get token**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Step 2: Use the token to access protected endpoints**
```bash
curl http://localhost:5000/api/summary \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzAzNDEwMDAwLCJpYXQiOjE3MDMzMjMwMDB9.xxxxx"
```

---

## Protected Endpoints

All of these endpoints now require authentication:

1. **GET /api/summary** - Overall health statistics
2. **GET /api/users** - List all users
3. **GET /api/logins** - Login statistics
4. **GET /api/heart-rate** - Heart rate statistics
5. **GET /api/user/<username>** - User-specific data
6. **GET /api/user/<username>/heart-rate** - User's heart rate history
7. **GET /api/user-wise-heart-rate** - All users' average heart rates

---

## Testing with PowerShell

### Login and Get Token
```powershell
$loginResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
  -Method Post `
  -Headers @{"Content-Type" = "application/json"} `
  -Body '{"username":"admin","password":"admin123"}' | ConvertFrom-Json

$token = $loginResponse.data.token
Write-Host "Token: $token"
```

### Use Token for Protected Endpoint
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/summary" `
  -Method Get `
  -Headers @{"Authorization" = "Bearer $token"} | ConvertFrom-Json

$response | ConvertTo-Json
```

---

## Error Responses

### Missing Token
**Status**: 401
```json
{
  "status": "error",
  "message": "Authentication token is missing"
}
```

### Invalid Token
**Status**: 401
```json
{
  "status": "error",
  "message": "Invalid or expired token"
}
```

### Invalid Credentials
**Status**: 401
```json
{
  "status": "error",
  "message": "Invalid username or password"
}
```

### User Already Exists
**Status**: 409
```json
{
  "status": "error",
  "message": "User already exists"
}
```

---

## Token Details

- **Algorithm**: HS256
- **Expiration**: 24 hours from login
- **Secret Key**: Configurable via `SECRET_KEY` environment variable
- **Claims**: `username`, `exp`, `iat`

---

## Production Recommendations

1. **Change Secret Key**: Set `SECRET_KEY` environment variable
   ```bash
   set SECRET_KEY=your-super-secret-key
   ```

2. **Use HTTPS**: Always use HTTPS in production

3. **Database for Users**: Replace `USERS_DB` dict with a real database

4. **Password Hashing**: Use `bcrypt` or `werkzeug.security` to hash passwords

5. **Token Blacklist**: Implement token blacklist for logout functionality

6. **Refresh Tokens**: Add refresh token endpoint for longer sessions

---

## Quick Test Script (PowerShell)

```powershell
# Login
$login = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
  -Method Post `
  -Headers @{"Content-Type" = "application/json"} `
  -Body '{"username":"admin","password":"admin123"}' | ConvertFrom-Json

$token = $login.data.token

# Get Summary
Invoke-WebRequest -Uri "http://localhost:5000/api/summary" `
  -Method Get `
  -Headers @{"Authorization" = "Bearer $token"} | ConvertFrom-Json

# Get Users
Invoke-WebRequest -Uri "http://localhost:5000/api/users" `
  -Method Get `
  -Headers @{"Authorization" = "Bearer $token"} | ConvertFrom-Json

# Get Heart Rate
Invoke-WebRequest -Uri "http://localhost:5000/api/heart-rate" `
  -Method Get `
  -Headers @{"Authorization" = "Bearer $token"} | ConvertFrom-Json
```
