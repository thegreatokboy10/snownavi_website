from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_url_path='/')
CORS(app)  # 允许跨域请求

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
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../'), 'course_admin.html')

if __name__ == '__main__':
    app.run(port=8899, debug=True)
