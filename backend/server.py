from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
import mimetypes
import uuid
import datetime
import hashlib
import re
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
NAVIGATION_FILE = os.path.join(DATA_DIR, 'navigation.json')

# Password generation and hashing functions
def generate_default_password(member_id):
    """Generate a default password based on member ID using a fixed algorithm"""
    # Use a combination of member_id and a fixed salt for generating the password
    salt = "SnowNavi2025Salt"  # Fixed salt for all passwords
    raw_password = f"{member_id}{salt}"
    # Create a SHA-256 hash of the raw password
    hashed = hashlib.sha256(raw_password.encode()).hexdigest()
    # Return the first 8 characters as the password
    return hashed[:8]

def hash_password(password):
    """Hash a password for storing"""
    # Use SHA-256 for password hashing
    return hashlib.sha256(password.encode()).hexdigest()

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

# Set maximum content length for file uploads (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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

@app.route('/admin.html')
def serve_admin_page():
    return send_from_directory(ROOT_DIR, 'admin.html')

@app.route('/course_admin.html')
def serve_course_admin_page():
    return send_from_directory(ROOT_DIR, 'course_admin.html')

@app.route('/member_admin.html')
def serve_member_admin_page():
    return send_from_directory(ROOT_DIR, 'member_admin.html')

@app.route('/navigation_admin.html')
def serve_navigation_admin_page():
    return send_from_directory(ROOT_DIR, 'navigation_admin.html')

@app.route('/login.html')
def serve_login_page():
    return send_from_directory(ROOT_DIR, 'login.html')

@app.route('/auth_callback.html')
def serve_auth_callback_page():
    return send_from_directory(ROOT_DIR, 'auth_callback.html')

@app.route('/member.html')
def serve_member_page():
    return send_from_directory(ROOT_DIR, 'member.html')

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

@app.route('/data/members.json', methods=['GET'])
def get_members():
    return send_from_directory(DATA_DIR, 'members.json')

@app.route('/data/members.json', methods=['POST'])
def update_members():
    data = request.get_json()
    members_file = os.path.join(DATA_DIR, 'members.json')
    with open(members_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success'}), 200

@app.route('/data/navigation.json', methods=['GET'])
def get_navigation():
    # Check if navigation.json exists, if not create a default one
    if not os.path.exists(NAVIGATION_FILE):
        default_navigation = {
            "items": [
                {
                    "id": "courses",
                    "url": "index.html#courses",
                    "translations": {
                        "en": "Courses",
                        "zh": "课程",
                        "nl": "Cursussen"
                    },
                    "visible": True,
                    "order": 1
                },
                {
                    "id": "map",
                    "url": "index.html#map",
                    "translations": {
                        "en": "Interactive Ski Map",
                        "zh": "在线滑雪地图",
                        "nl": "Interactieve Skikaart"
                    },
                    "visible": True,
                    "order": 2
                },
                {
                    "id": "story",
                    "url": "index.html#story",
                    "translations": {
                        "en": "Our Story",
                        "zh": "我们的故事",
                        "nl": "Ons Verhaal"
                    },
                    "visible": True,
                    "order": 3
                },
                {
                    "id": "contact",
                    "url": "index.html#contact",
                    "translations": {
                        "en": "Contact",
                        "zh": "联系我们",
                        "nl": "Contact"
                    },
                    "visible": True,
                    "order": 4
                }
            ]
        }
        with open(NAVIGATION_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_navigation, f, ensure_ascii=False, indent=2)

    return send_from_directory(DATA_DIR, 'navigation.json')

@app.route('/data/navigation.json', methods=['POST'])
def update_navigation():
    data = request.get_json()
    with open(NAVIGATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success'}), 200

@app.route('/api/member/<member_id>', methods=['GET'])
def get_member(member_id):
    try:
        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            return jsonify({'error': 'Members data not found'}), 404

        with open(members_file, 'r', encoding='utf-8') as f:
            members = json.load(f)

        if member_id in members:
            return jsonify(members[member_id])
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving member data: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/member/<member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        # Validate member_id format to prevent injection attacks
        if not re.match(r'^SN\d{4}\d{4}$', member_id):
            return jsonify({'error': 'Invalid member ID format'}), 400

        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            return jsonify({'error': 'Members data not found'}), 404

        with open(members_file, 'r', encoding='utf-8') as f:
            members = json.load(f)

        # Check if the member exists
        if member_id not in members:
            return jsonify({'error': 'Member not found'}), 404

        # Get the updated member data from the request
        updated_member = request.get_json()

        # Validate the updated member data
        if not updated_member or not isinstance(updated_member, dict):
            return jsonify({'error': 'Invalid member data'}), 400

        # Ensure the member ID in the data matches the URL parameter
        if 'id' not in updated_member or updated_member['id'] != member_id:
            return jsonify({'error': 'Member ID mismatch'}), 400

        # Validate required fields
        required_fields = ['name', 'isActive', 'validityPeriod']
        for field in required_fields:
            if field not in updated_member:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate validityPeriod is an object
        if not isinstance(updated_member['validityPeriod'], dict):
            return jsonify({'error': 'validityPeriod must be an object'}), 400

        # Update the member in the members dictionary
        members[member_id] = updated_member

        # Write the updated members dictionary back to the file
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"Error updating member data: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/member/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            return jsonify({'error': 'Members data not found'}), 404

        with open(members_file, 'r', encoding='utf-8') as f:
            members = json.load(f)

        # Check if the member exists
        if member_id not in members:
            return jsonify({'error': 'Member not found'}), 404

        # Delete the member from the members dictionary
        del members[member_id]

        # Write the updated members dictionary back to the file
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"Error deleting member data: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/member', methods=['POST'])
def create_member():
    try:
        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            # Create a new members file if it doesn't exist
            members = {}
        else:
            # Load existing members
            with open(members_file, 'r', encoding='utf-8') as f:
                members = json.load(f)

        # Get the new member data from the request
        new_member = request.get_json()

        # Ensure the member has an ID
        if 'id' not in new_member:
            return jsonify({'error': 'Member ID is required'}), 400

        member_id = new_member['id']

        # Check if a member with this ID already exists
        if member_id in members:
            return jsonify({'error': 'A member with this ID already exists'}), 409

        # Generate default password for the new member
        default_password = generate_default_password(member_id)
        # Store the hashed password
        new_member['password'] = default_password
        # Store the plain text password temporarily for the response
        plain_password = default_password

        # Add the new member to the members dictionary
        members[member_id] = new_member

        # Write the updated members dictionary back to the file
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)

        return jsonify({
            'status': 'success',
            'id': member_id,
            'password': plain_password  # Return the plain text password in the response
        }), 201
    except Exception as e:
        app.logger.error(f"Error creating member data: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/member/<member_id>/check-expiration', methods=['POST'])
def check_member_expiration(member_id):
    """Check if a member's validity period has expired and update status if needed"""
    try:
        # Validate member_id format to prevent injection attacks
        if not re.match(r'^SN\d{4}\d{4}$', member_id):
            return jsonify({'error': 'Invalid member ID format'}), 400

        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            return jsonify({'error': 'Members data not found'}), 404

        with open(members_file, 'r', encoding='utf-8') as f:
            members = json.load(f)

        # Check if the member exists
        if member_id not in members:
            return jsonify({'error': 'Member not found'}), 404

        member = members[member_id]

        # Only proceed if the member is currently active
        if not member.get('isActive', False):
            return jsonify({
                'status': 'success',
                'message': 'Member is already marked as expired',
                'updated': False
            }), 200

        # Check if validity period exists
        if not member.get('validityPeriod'):
            return jsonify({'error': 'Missing validity period data'}), 400

        # Get the validity period (could be string or object with language keys)
        validity_period = None
        if isinstance(member['validityPeriod'], str):
            # New format: single string
            validity_period = member['validityPeriod']
        elif isinstance(member['validityPeriod'], dict):
            # Old format: object with language keys
            for lang in ['en', 'zh', 'nl']:
                if lang in member['validityPeriod'] and member['validityPeriod'][lang]:
                    validity_period = member['validityPeriod'][lang]
                    break
        else:
            return jsonify({'error': 'Invalid validity period format'}), 400

        if not validity_period:
            return jsonify({
                'status': 'success',
                'message': 'No validity period found to check',
                'updated': False
            }), 200

        # Check if the validity period is in the dd/mm/yyyy - dd/mm/yyyy format
        is_expired = False
        match = re.match(r'^(\d{2}/\d{2}/\d{4}) - (\d{2}/\d{2}/\d{4})$', validity_period)
        if match:
            end_date_str = match.group(2)
            try:
                # Parse the end date
                day, month, year = map(int, end_date_str.split('/'))
                end_date = datetime.datetime(year, month, day, 23, 59, 59)

                # Compare with current date
                now = datetime.datetime.now()
                is_expired = now > end_date
            except ValueError:
                app.logger.error(f"Error parsing date: {end_date_str}")
                return jsonify({'error': 'Invalid date format'}), 400
        else:
            # If not in standard format, try to extract year from the end date
            parts = validity_period.split(' - ')
            if len(parts) == 2:
                year_match = re.search(r'\d{4}', parts[1])
                if year_match:
                    year = int(year_match.group(0))
                    is_expired = datetime.datetime.now().year > year

        # If expired, update the member status
        if is_expired:
            member['isActive'] = False

            # Write the updated members dictionary back to the file
            with open(members_file, 'w', encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=2)

            return jsonify({
                'status': 'success',
                'message': 'Member status updated to expired',
                'updated': True
            }), 200
        else:
            return jsonify({
                'status': 'success',
                'message': 'Member validity period has not expired',
                'updated': False
            }), 200

    except Exception as e:
        app.logger.error(f"Error checking member expiration: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/members/generate-passwords', methods=['POST'])
def generate_all_passwords():
    """Generate or update passwords for all members"""
    try:
        members_file = os.path.join(DATA_DIR, 'members.json')
        if not os.path.exists(members_file):
            return jsonify({'error': 'Members data not found'}), 404

        # Load existing members
        with open(members_file, 'r', encoding='utf-8') as f:
            members = json.load(f)

        # Track members that had passwords generated
        updated_members = []

        # Generate passwords for all members
        for member_id, member in members.items():
            # Generate a default password based on member ID
            default_password = generate_default_password(member_id)
            # Store the hashed password
            member['password'] = default_password
            # Add to the list of updated members with plain text password
            updated_members.append({
                'id': member_id,
                'name': member.get('name', ''),
                'password': default_password  # Plain text password for display
            })

        # Write the updated members dictionary back to the file
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)

        return jsonify({
            'status': 'success',
            'message': f'Generated passwords for {len(updated_members)} members',
            'members': updated_members
        }), 200
    except Exception as e:
        app.logger.error(f"Error generating passwords: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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

@app.errorhandler(413)
def request_entity_too_large(e):
    max_size_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
    return jsonify(error=f"File too large. Maximum allowed size is {max_size_mb:.1f}MB"), 413

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
