from flask import Blueprint, request, jsonify, current_app
from getmac import get_mac_address
import hashlib
from .models import create_user, find_user, verify_password, update_user_password, delete_user

api_bp = Blueprint('api', __name__)

# Helper function to hash the MAC address
def hash_mac_address(mac_address):
    return hashlib.sha256(mac_address.encode()).hexdigest()

# Register Route
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # MongoDB client (accessing the 'mongo' instance)
    mongo = current_app.extensions['pymongo'][mongo]
    
    # Check if username already exists
    if find_user(mongo, username):
        return jsonify({'message': 'Username already exists.'}), 400

    # Get system MAC address and hash it
    mac_address = get_mac_address()
    if not mac_address:
        return jsonify({'message': 'Unable to retrieve MAC address.'}), 400
    hashed_mac = hash_mac_address(mac_address)

    # Create new user with hashed password
    create_user(mongo, username, password, hashed_mac)

    return jsonify({'message': 'Registration successful! Please log in.'}), 201

# Login Route
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # MongoDB client (accessing the 'mongo' instance)
    mongo = current_app.extensions['pymongo'][mongo]

    # Fetch user document
    user = find_user(mongo, username)
    if user:
        # Verify password and hashed MAC address
        mac_address = get_mac_address()
        if verify_password(user['password'], password):
            if user['mac_address'] == hash_mac_address(mac_address):
                return jsonify({'message': 'Login successful!'}), 200
            return jsonify({'message': 'MAC address does not match.'}), 403
        return jsonify({'message': 'Incorrect password.'}), 401

    return jsonify({'message': 'Username not found.'}), 404
