from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
import mimetypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Root directory of the project
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
JSON_FILE = os.path.join(DATA_DIR, 'courses.json')

# Initialize Flask app
app = Flask(__name__, static_folder=None)  # Disable default static folder
CORS(app)  # Enable CORS

# Ensure proper MIME types are registered
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')

# Main routes
@app.route('/')
def index():
    return send_from_directory(ROOT_DIR, 'index.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory(ROOT_DIR, 'index.html')

@app.route('/course.html')
def serve_course():
    return send_from_directory(ROOT_DIR, 'course.html')

@app.route('/course_admin.html')
def serve_admin_page():
    return send_from_directory(ROOT_DIR, 'course_admin.html')

@app.route('/login.html')
def serve_login_page():
    return send_from_directory(ROOT_DIR, 'login.html')

@app.route('/auth_callback.html')
def serve_auth_callback_page():
    return send_from_directory(ROOT_DIR, 'auth_callback.html')

# API routes
@app.route('/api/config')
def get_config():
    # Return the necessary configuration from environment variables
    return jsonify({
        'googleClientId': os.environ.get('GOOGLE_CLIENT_ID', ''),
        'authorizedEmail': os.environ.get('ALLOWED_EMAILS', '')
    })

# Data routes
@app.route('/data/courses.json', methods=['GET'])
def get_courses():
    return send_from_directory(DATA_DIR, 'courses.json')

@app.route('/data/courses.json', methods=['POST'])
def update_courses():
    data = request.get_json()
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success'}), 200

# Static files routes
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/<path:filename>')
def serve_static_files(filename):
    # Check if the file exists in the root directory
    if os.path.isfile(os.path.join(ROOT_DIR, filename)):
        return send_from_directory(ROOT_DIR, filename)
    else:
        return 'File not found', 404

# Add some basic logging
@app.before_request
def log_request_info():
    app.logger.debug('Request Headers: %s', request.headers)
    app.logger.debug('Request Path: %s', request.path)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    app.logger.error('Server Error: %s', e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Get host and port from environment variables or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8899))

    print(f"Starting server at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
