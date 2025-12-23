# ======================================
# Health App REST API
# Flask-based API for Health Log Analysis
# ======================================

from flask import Flask, jsonify, request, render_template, send_from_directory
import pandas as pd
import re
from datetime import datetime
import os
import logging
from functools import lru_cache
from auth import auth_bp, token_required

# ======================================
# Logging Configuration
# ======================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

# ======================================
# Configuration
# ======================================
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Register authentication blueprint
app.register_blueprint(auth_bp)

# ======================================
# 1. Load & Parse Log File
# ======================================

def read_logs(file_name):
    """Read and parse logs from file"""
    logs = []
    try:
        with open(file_name, "r") as file:
            for line in file:
                match = re.match(r"(.*?),(.*?),(.*?),(.*)", line.strip())
                if match:
                    date, user, action, value = match.groups()
                    logs.append({
                        "date": date,
                        "user": user,
                        "action": action,
                        "value": value
                    })
        logger.info(f"Successfully loaded {len(logs)} logs from {file_name}")
    except FileNotFoundError:
        logger.error(f"Log file not found: {file_name}")
        return []
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return []
    return logs


@lru_cache(maxsize=128)
def get_dataframe():
    """Get pandas dataframe from logs (cached)"""
    try:
        df = pd.read_csv(
            "health_logs.txt",
            header=None,
            names=["date", "user", "action", "value"]
        )
        df["date"] = pd.to_datetime(df["date"])
        logger.info("DataFrame created successfully")
        return df
    except Exception as e:
        logger.error(f"Error creating dataframe: {str(e)}")
        return None


# ======================================
# 2. API Routes (Protected)
# ======================================

@app.route('/', methods=['GET'])
def home():
    """Redirect to login"""
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve dashboard"""
    return render_template('dashboard.html')


@app.route('/stats', methods=['GET'])
def stats_page():
    """Serve advanced statistics page"""
    return render_template('stats.html')


@app.route('/validate-page', methods=['GET'])
def validate_page():
    """Serve health data validation page"""
    return render_template('validate.html')


@app.route('/users-page', methods=['GET'])
def users_page():
    """Serve users list page"""
    return render_template('users.html')


@app.route('/api/', methods=['GET'])
def api_home():
    """API documentation"""
    return jsonify({
        "status": "success",
        "message": "Health App API is running",
        "version": "2.0",
        "authentication": "JWT Bearer Token"
    })


@app.route('/api/summary', methods=['GET'])
@token_required
def get_summary():
    """Get overall summary of health data"""
    try:
        logs = read_logs("health_logs.txt")
        
        # Total users
        users = set(log["user"] for log in logs)
        total_users = len(users)
        
        # Successful logins
        success_logins = sum(
            1 for log in logs 
            if log["action"] == "LOGIN" and log["value"] == "success"
        )
        
        # Average heart rate
        heart_rates = [
            int(log["value"]) for log in logs 
            if log["action"] == "HEART_RATE"
        ]
        avg_hr = sum(heart_rates) / len(heart_rates) if heart_rates else 0
        
        return jsonify({
            "status": "success",
            "data": {
                "total_users": total_users,
                "successful_logins": success_logins,
                "average_heart_rate": round(avg_hr, 2),
                "total_logs": len(logs)
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/users', methods=['GET'])
@token_required
def get_users():
    """Get list of all users"""
    try:
        logs = read_logs("health_logs.txt")
        users = sorted(list(set(log["user"] for log in logs)))
        
        return jsonify({
            "status": "success",
            "data": {
                "total_users": len(users),
                "users": users
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/logins', methods=['GET'])
@token_required
def get_logins():
    """Get login statistics"""
    try:
        logs = read_logs("health_logs.txt")
        
        login_logs = [log for log in logs if log["action"] == "LOGIN"]
        successful = sum(1 for log in login_logs if log["value"] == "success")
        failed = sum(1 for log in login_logs if log["value"] == "failed")
        
        return jsonify({
            "status": "success",
            "data": {
                "total_logins": len(login_logs),
                "successful_logins": successful,
                "failed_logins": failed,
                "success_rate": round((successful / len(login_logs) * 100), 2) if login_logs else 0
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/heart-rate', methods=['GET'])
@token_required
def get_heart_rate_stats():
    """Get overall heart rate statistics"""
    try:
        logs = read_logs("health_logs.txt")
        
        heart_rates = [
            int(log["value"]) for log in logs 
            if log["action"] == "HEART_RATE"
        ]
        
        if not heart_rates:
            return jsonify({
                "status": "success",
                "data": {
                    "total_readings": 0,
                    "average": 0,
                    "min": 0,
                    "max": 0
                }
            })
        
        return jsonify({
            "status": "success",
            "data": {
                "total_readings": len(heart_rates),
                "average": round(sum(heart_rates) / len(heart_rates), 2),
                "min": min(heart_rates),
                "max": max(heart_rates)
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/user/<username>', methods=['GET'])
@token_required
def get_user_info(username):
    """Get information for a specific user"""
    try:
        logs = read_logs("health_logs.txt")
        user_logs = [log for log in logs if log["user"] == username]
        
        if not user_logs:
            return jsonify({
                "status": "error",
                "message": f"User '{username}' not found"
            }), 404
        
        logins = [log for log in user_logs if log["action"] == "LOGIN"]
        successful_logins = sum(1 for log in logins if log["value"] == "success")
        
        return jsonify({
            "status": "success",
            "data": {
                "username": username,
                "total_logs": len(user_logs),
                "login_attempts": len(logins),
                "successful_logins": successful_logins
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/user/<username>/heart-rate', methods=['GET'])
@token_required
def get_user_heart_rate(username):
    """Get heart rate data for a specific user"""
    try:
        logs = read_logs("health_logs.txt")
        user_hr_logs = [
            log for log in logs 
            if log["user"] == username and log["action"] == "HEART_RATE"
        ]
        
        if not user_hr_logs:
            return jsonify({
                "status": "error",
                "message": f"No heart rate data found for user '{username}'"
            }), 404
        
        heart_rates = [int(log["value"]) for log in user_hr_logs]
        
        return jsonify({
            "status": "success",
            "data": {
                "username": username,
                "readings": len(heart_rates),
                "average": round(sum(heart_rates) / len(heart_rates), 2),
                "min": min(heart_rates),
                "max": max(heart_rates),
                "heart_rate_history": [
                    {
                        "date": log["date"],
                        "heart_rate": int(log["value"])
                    } for log in user_hr_logs
                ]
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/user-wise-heart-rate', methods=['GET'])
@token_required
def get_user_wise_heart_rate():
    """Get user-wise average heart rate"""
    try:
        logs = read_logs("health_logs.txt")
        
        user_heart_rate = {}
        for log in logs:
            if log["action"] == "HEART_RATE":
                user = log["user"]
                rate = int(log["value"])
                
                if user not in user_heart_rate:
                    user_heart_rate[user] = []
                
                user_heart_rate[user].append(rate)
        
        result = {}
        for user in user_heart_rate:
            avg = sum(user_heart_rate[user]) / len(user_heart_rate[user])
            result[user] = round(avg, 2)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ======================================
# 4. Data Validation Endpoints
# ======================================

@app.route('/api/health/validate', methods=['POST'])
@token_required
def validate_health_data():
    """Validate incoming health data before saving"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        errors = []
        
        # Validate heart rate
        if 'heart_rate' in data:
            try:
                hr = int(data['heart_rate'])
                if not (20 <= hr <= 220):
                    errors.append("Heart rate must be between 20 and 220 BPM")
            except (ValueError, TypeError):
                errors.append("Heart rate must be a valid number")
        
        # Validate blood pressure
        if 'blood_pressure' in data:
            bp = data['blood_pressure']
            if isinstance(bp, str) and '/' in bp:
                try:
                    sys, dia = bp.split('/')
                    sys, dia = int(sys), int(dia)
                    if not (70 <= sys <= 200 and 40 <= dia <= 130):
                        errors.append("Blood pressure values out of normal range")
                except:
                    errors.append("Blood pressure format should be 'sys/dia'")
        
        # Validate temperature
        if 'temperature' in data:
            try:
                temp = float(data['temperature'])
                if not (35 <= temp <= 42):
                    errors.append("Temperature must be between 35°C and 42°C")
            except (ValueError, TypeError):
                errors.append("Temperature must be a valid number")
        
        if errors:
            logger.warning(f"Validation errors: {errors}")
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            }), 400
        
        logger.info(f"Health data validated successfully: {data}")
        return jsonify({
            "status": "success",
            "message": "Data is valid",
            "data": data
        }), 200
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ======================================
# 5. Advanced Stats Endpoint
# ======================================

@app.route('/api/stats/advanced', methods=['GET'])
@token_required
def get_advanced_stats():
    """Get advanced aggregated health statistics"""
    try:
        df = get_dataframe()
        
        if df is None or df.empty:
            return jsonify({
                "status": "error",
                "message": "No data available"
            }), 404
        
        # Heart rate statistics
        hr_data = df[df['action'] == 'HEART_RATE']['value'].astype(int)
        login_data = df[df['action'] == 'LOGIN']
        
        stats = {
            "total_users": int(df['user'].nunique()),
            "total_logs": len(df),
            "date_range": {
                "start": str(df['date'].min()),
                "end": str(df['date'].max())
            },
            "heart_rate": {
                "count": int(len(hr_data)),
                "average": float(round(hr_data.mean(), 2)) if len(hr_data) > 0 else 0,
                "min": int(hr_data.min()) if len(hr_data) > 0 else 0,
                "max": int(hr_data.max()) if len(hr_data) > 0 else 0,
                "std_dev": float(round(hr_data.std(), 2)) if len(hr_data) > 0 else 0
            },
            "login_stats": {
                "total": len(login_data),
                "successful": len(login_data[login_data['value'] == 'success']),
                "failed": len(login_data[login_data['value'] == 'failed']),
                "success_rate": float(round(len(login_data[login_data['value'] == 'success']) / len(login_data) * 100, 2)) if len(login_data) > 0 else 0
            }
        }
        
        logger.info("Advanced stats retrieved successfully")
        return jsonify({
            "status": "success",
            "data": stats
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting advanced stats: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ======================================
# 6. Error Handlers
# ======================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {error}")
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    logger.warning(f"401 error: Unauthorized access attempt")
    return jsonify({
        "status": "error",
        "message": "Unauthorized - Invalid or missing token"
    }), 401


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


# ======================================
# 7. Run API
# ======================================

if __name__ == '__main__':
    logger.info("Starting Health App API on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
