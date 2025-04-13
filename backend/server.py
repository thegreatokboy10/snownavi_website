from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
import mimetypes
import uuid
import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Root directory of the project
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
UPLOADS_DIR = os.path.join(ROOT_DIR, 'uploads')
JSON_FILE = os.path.join(DATA_DIR, 'courses.json')

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Create subdirectories for images and PDFs
images_dir = os.path.join(UPLOADS_DIR, 'images')
pdfs_dir = os.path.join(UPLOADS_DIR, 'pdfs')

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

if not os.path.exists(pdfs_dir):
    os.makedirs(pdfs_dir)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
    'pdfs': {'pdf'}
}

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
    # Get environment variables
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
    allowed_emails = os.environ.get('ALLOWED_EMAILS', '')

    # Log the values being returned (remove in production)
    app.logger.info(f"Returning config: googleClientId={google_client_id}, authorizedEmail={allowed_emails}")

    # Return the necessary configuration from environment variables
    return jsonify({
        'googleClientId': google_client_id,
        'authorizedEmail': allowed_emails
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

# File upload helper functions
def allowed_file(filename, file_type):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, set())

def generate_unique_filename(filename):
    # Get file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    # Generate unique filename with timestamp and UUID
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}.{ext}"

# File upload endpoints
@app.route('/api/upload/<file_type>', methods=['POST'])
def upload_file(file_type):
    try:
        if file_type not in ['images', 'pdfs']:
            return jsonify({'error': 'Invalid file type'}), 400

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename, file_type):
            return jsonify({'error': f'File type not allowed. Allowed types for {file_type}: {ALLOWED_EXTENSIONS[file_type]}'}), 400

        # Process the file
        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        upload_folder = os.path.join(UPLOADS_DIR, file_type)
        file_path = os.path.join(upload_folder, unique_filename)

        # Ensure the upload folder exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the file
        file.save(file_path)

        # Return the relative path to the file
        relative_path = f"/uploads/{file_type}/{unique_filename}"
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'originalName': filename,
            'path': relative_path,
            'url': relative_path
        })
    except Exception as e:
        # Log the error
        app.logger.error(f"Error uploading file: {str(e)}")
        # Return a JSON error response
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# File listing endpoint
@app.route('/api/files/<file_type>', methods=['GET'])
def list_files(file_type):
    try:
        if file_type not in ['images', 'pdfs']:
            return jsonify({'error': 'Invalid file type'}), 400

        upload_folder = os.path.join(UPLOADS_DIR, file_type)
        files = []

        # Create the directory if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            return jsonify({'files': []})

        # List files in the directory
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path) and allowed_file(filename, file_type):
                file_url = f"/uploads/{file_type}/{filename}"
                files.append({
                    'name': filename,
                    'path': file_url,
                    'url': file_url,
                    'size': os.path.getsize(file_path),
                    'lastModified': os.path.getmtime(file_path)
                })

        # Sort files by last modified time (newest first)
        files.sort(key=lambda x: x['lastModified'], reverse=True)

        return jsonify({
            'files': files
        })
    except Exception as e:
        # Log the error
        app.logger.error(f"Error listing files: {str(e)}")
        # Return a JSON error response
        return jsonify({'error': f'Server error: {str(e)}', 'files': []}), 500

# Serve uploaded files
@app.route('/uploads/')
@app.route('/uploads/<path:subpath>')
def serve_uploads(subpath=''):
    if not subpath:
        return jsonify({'error': 'Directory listing not allowed'}), 403

    parts = subpath.split('/')
    if len(parts) != 2:
        return jsonify({'error': 'Invalid path format'}), 400

    file_type, filename = parts
    return serve_uploaded_file(file_type, filename)

@app.route('/uploads/<file_type>/<filename>')
def serve_uploaded_file(file_type, filename):
    try:
        if file_type not in ['images', 'pdfs']:
            return jsonify({'error': 'Invalid file type'}), 400

        file_path = os.path.join(UPLOADS_DIR, file_type, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_from_directory(os.path.join(UPLOADS_DIR, file_type), filename)
    except Exception as e:
        app.logger.error(f"Error serving file: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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
