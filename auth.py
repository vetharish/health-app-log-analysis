# ======================================
# Authentication Module
# JWT Login & Registration
# ======================================

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import jwt
from functools import wraps

# Create blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Simple user database (in production, use a real database)
USERS_DB = {
    'admin': 'admin123',
    'user01': 'password1',
    'user02': 'password2',
    'user03': 'password3'
}

# JWT Configuration
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


# ======================================
# JWT Functions
# ======================================

def generate_token(username, secret_key):
    """Generate JWT token for user"""
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, secret_key, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token, secret_key):
    """Verify JWT token and return username if valid"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    "status": "error",
                    "message": "Invalid token format. Use: Authorization: Bearer <token>"
                }), 401
        
        if not token:
            return jsonify({
                "status": "error",
                "message": "Authentication token is missing"
            }), 401
        
        username = verify_token(token, current_app.config['SECRET_KEY'])
        if not username:
            return jsonify({
                "status": "error",
                "message": "Invalid or expired token"
            }), 401
        
        request.username = username
        return f(*args, **kwargs)
    
    return decorated


# ======================================
# Authentication Routes
# ======================================

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing username or password"
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        # Validation
        if len(username) < 3:
            return jsonify({
                "status": "error",
                "message": "Username must be at least 3 characters"
            }), 400
        
        if len(password) < 6:
            return jsonify({
                "status": "error",
                "message": "Password must be at least 6 characters"
            }), 400
        
        if username in USERS_DB:
            return jsonify({
                "status": "error",
                "message": "User already exists"
            }), 409
        
        # Add user to database
        USERS_DB[username] = password
        
        return jsonify({
            "status": "success",
            "message": f"User '{username}' registered successfully",
            "data": {
                "username": username
            }
        }), 201
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing username or password"
            }), 400
        
        username = data['username']
        password = data['password']
        
        # Verify credentials
        if username not in USERS_DB or USERS_DB[username] != password:
            return jsonify({
                "status": "error",
                "message": "Invalid username or password"
            }), 401
        
        # Generate token
        token = generate_token(username, current_app.config['SECRET_KEY'])
        
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "username": username,
                "token": token,
                "expires_in_hours": JWT_EXPIRATION_HOURS
            }
        }), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Logout user (token invalidation on client side)"""
    return jsonify({
        "status": "success",
        "message": "Logout successful. Please discard the token.",
        "data": {
            "username": request.username
        }
    }), 200
