from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB CRUD operations
def create_user(mongo, username, password, mac_address):
    """Add a new user document to MongoDB."""
    if find_user(mongo, username):
        raise ValueError("User already exists")
    mongo.db.users.insert_one({
        'username': username,
        'password': generate_password_hash(password),  # Hash password for security
        'mac_address': mac_address
    })

def find_user(mongo, username):
    """Find a user in MongoDB by username."""
    return mongo.db.users.find_one({'username': username})

def verify_password(stored_password, provided_password):
    """Verify the provided password against the stored password hash."""
    return check_password_hash(stored_password, provided_password)

def update_user_password(mongo, username, new_password):
    """Update a user's password in MongoDB."""
    hashed_password = generate_password_hash(new_password)
    mongo.db.users.update_one({'username': username}, {'$set': {'password': hashed_password}})

def delete_user(mongo, username):
    """Delete a user from MongoDB."""
    mongo.db.users.delete_one({'username': username})
