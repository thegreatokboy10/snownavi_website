from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__, static_url_path='/')
CORS(app)  # Enable CORS

# Root directory of the project
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
JSON_FILE = os.path.join(DATA_DIR, 'courses.json')

@app.route('/data/courses.json', methods=['GET'])
def get_courses():
    return send_from_directory(DATA_DIR, 'courses.json')

@app.route('/data/courses.json', methods=['POST'])
def update_courses():
    data = request.get_json()
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'success'}), 200

@app.route('/course_admin.html')
def serve_admin_page():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'course_admin.html')

@app.route('/login.html')
def serve_login_page():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'login.html')

@app.route('/auth_callback.html')
def serve_auth_callback_page():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'auth_callback.html')

@app.route('/api/config')
def get_config():
    # Return the necessary configuration from environment variables
    return jsonify({
        'googleClientId': os.environ.get('GOOGLE_CLIENT_ID', ''),
        'authorizedEmail': os.environ.get('ALLOWED_EMAILS', '')
    })
                            
if __name__ == '__main__':
    app.run(port=8899, debug=True)
