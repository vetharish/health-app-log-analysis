# Health App - Project Documentation

## Overview

The Health App is a lightweight Flask-based application for parsing simple health/activity logs, exposing REST APIs, and serving a basic dashboard. It includes JWT authentication, log parsing, summary and statistics endpoints, and a small frontend dashboard.

## Key Features

- JWT authentication (`/api/auth/*`) with register/login/logout
- Read and parse `health_logs.txt` for actions: `LOGIN`, `HEART_RATE`, etc.
- Summary endpoints: `/api/summary`, `/api/users`, `/api/logins`, `/api/heart-rate`
- Advanced statistics endpoint: `/api/stats/advanced`
- Data validation endpoint: `POST /api/health/validate`
- Simple dashboard UI at `/dashboard` and additional pages: `/stats`, `/users-page`, `/validate-page`
- Minimal caching for DataFrame using `functools.lru_cache`

## File Layout (important files)

- `api.py` - Main Flask app, routes, logging, caching
- `auth.py` - JWT authentication blueprint and helper functions
- `health_app.py` - Original CLI-style log analysis script
- `health_logs.txt` - Sample log data used by the app
- `templates/` - HTML templates (`dashboard.html`, `login.html`, `stats.html`, `users.html`, `validate.html`)
- `static/` - Static assets (`dashboard.js`, `style.css`)
- `requirements.txt` - Python dependencies

## Setup (local, development)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or
.\.venv\Scripts\activate.bat    # cmd
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Set a secure secret key for JWT (recommended in production):

```powershell
$env:SECRET_KEY = "your-very-secret-key"
```

4. Run the app:

```bash
python api.py
```

The server will run at `http://127.0.0.1:5000`.

## Quick API Usage

- Get API info (no auth):

```bash
curl http://127.0.0.1:5000/api/
```

- Login to receive JWT:

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

- Use returned token to call protected endpoints:

```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/api/summary
```

- Validate health data (requires token):

```bash
curl -X POST http://127.0.0.1:5000/api/health/validate \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"heart_rate":78, "temperature":37.0}'
```

## Frontend pages

- `/` - Login page
- `/dashboard` - Main dashboard with charts and summary
- `/stats` - Advanced stats (calls `/api/stats/advanced`)
- `/users-page` - Users list (calls `/api/users`)
- `/validate-page` - Frontend form to POST to `/api/health/validate`

Note: Some pages call protected API endpoints and will display a message if not authenticated. You can implement a small frontend login to store the JWT in `localStorage` and attach it to requests.

## Notes & Next Steps

- For production deploy, run behind a WSGI server (Gunicorn / uWSGI) and set a secure `SECRET_KEY`.
- Consider persisting logs and users in a real database (SQLite/SQLAlchemy or other), and enable migration tooling.
- Add frontend login and token management for better UX (store token securely, refresh if implemented).
- Add unit tests and CI (was generated during enhancement but may have been removed per workspace changes).

## Troubleshooting

- "Connection refused" when testing endpoints: ensure `python api.py` is running and listening on port 5000.
- JWT issues: ensure `SECRET_KEY` is consistent between processes.
- Missing dependencies: run `pip install -r requirements.txt`.

---

If you want, I can:
- add a `README.md` replacement with this content, or
- add a `docs/` folder and split this into separate pages (Setup, API, Frontend, Deployment), or
- implement a simple frontend login and token storage so the pages automatically call protected endpoints.

Which option do you prefer?