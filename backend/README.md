# SnowNavi Backend Server

This directory contains the Flask server that powers the SnowNavi website's backend, including the admin interface and API endpoints.

## Overview

The Flask server (`server.py`) handles:

1. Serving the admin interface (course_admin.html, login.html, auth_callback.html)
2. Providing API endpoints for Google OAuth configuration
3. Managing course data through the /data/courses.json endpoint
4. Serving static assets when needed

## Configuration

The server uses environment variables stored in a `.env` file for configuration:

```
FLASK_SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
ALLOWED_EMAILS=okboy2008@gmail.com
```

## Setup Instructions

### Local Development

1. Create a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the server:
   ```
   python server.py
   ```

4. Access the server at http://localhost:8899

### Production Deployment

1. Copy the nginx configuration:
   ```
   sudo cp nginx/snownavi.ski /etc/nginx/sites-available/
   sudo ln -s /etc/nginx/sites-available/snownavi.ski /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

2. Set up the Flask server as a systemd service:
   ```
   sudo ./setup_flask_server.sh
   ```

3. Check the service status:
   ```
   sudo systemctl status snownavi-flask.service
   ```

## Nginx Configuration

The nginx configuration (`nginx/snownavi.ski`) is set up to:

1. Serve static files directly from the filesystem
2. Proxy requests for admin pages and API endpoints to the Flask server
3. Handle SSL termination and HTTP to HTTPS redirection

## Troubleshooting

### Checking Logs

```
sudo journalctl -u snownavi-flask.service
```

### Restarting the Service

```
sudo systemctl restart snownavi-flask.service
```

### Checking Nginx Configuration

```
sudo nginx -t
sudo systemctl status nginx
```
