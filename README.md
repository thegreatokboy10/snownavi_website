# SnowNavi Website

This is the website for SnowNavi Snow Club, featuring course information, an interactive ski map, and an admin panel for managing course content.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd snownavi_website
   ```

2. Install Python dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

3. Configure the `.env` file in the backend directory:
   ```
   # Navigate to the backend directory
   cd backend

   # Edit the .env file with your configuration
   # Make sure to set these values:
   FLASK_SECRET_KEY=your-secret-key
   GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ALLOWED_EMAILS=okboy2008@gmail.com
   ```

### Running the Application

1. Start the Flask server:
   ```
   cd backend
   python server.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8899
   ```

## Google OAuth Setup

### Creating a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "OAuth consent screen"
4. Select "External" user type and click "Create"
5. Fill in the required information:
   - App name: "SnowNavi Admin"
   - User support email: Your email
   - Developer contact information: Your email
6. Click "Save and Continue"
7. Skip adding scopes and click "Save and Continue"
8. Add your test user email (okboy2008@gmail.com) and click "Save and Continue"
9. Review your settings and click "Back to Dashboard"

### Creating OAuth Credentials

1. Navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Web application" as the application type
4. Name: "SnowNavi Admin Web Client"
5. Add Authorized JavaScript origins:
   - Add your website's domain (e.g., https://snownavi.ski)
   - For local testing, add http://localhost:3000
6. Add Authorized redirect URIs:
   - Add your callback URL (e.g., https://snownavi.ski/auth_callback.html)
   - For local testing, add http://localhost:3000/auth_callback.html
7. Click "Create"
8. Copy the Client ID and add it to your `.env` file

## Security Features

- Authentication is handled via Google OAuth
- Only the authorized email (okboy2008@gmail.com) can access the admin panel
- Client ID and authorized email are stored in a .env file, not hardcoded
- Authentication tokens expire after 1 hour
- Server-side validation of configuration

## File Structure

- `index.html` - Main website homepage
- `course.html` - Course details page
- `course_admin.html` - Admin panel for managing courses (requires authentication)
- `login.html` - Login page for admin panel
- `auth_callback.html` - Callback page for Google OAuth
- `backend/server.py` - Python Flask server for serving the website and handling API requests
- `backend/.env` - Environment variables for configuration
- `data/courses.json` - JSON file containing course data

## Development

For development with automatic server restarts, you can use Flask's debug mode (already enabled in server.py) or install and use `flask-debug`:

```
pip install flask-debug
FLASK_APP=backend/server.py flask run --debug
```

## Deployment

1. Set up your production environment with Python
2. Clone the repository
3. Install dependencies with `pip install -r backend/requirements.txt`
4. Configure the `.env` file with your production settings
5. For production, you might want to use a WSGI server like Gunicorn:
   ```
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8899 backend.server:app
   ```

6. For a more robust setup, consider using Nginx as a reverse proxy and Supervisor to manage the process.
