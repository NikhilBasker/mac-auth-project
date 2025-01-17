from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB CRUD operations
def create_user(mongo, username, password, mac_address):
    """Add a new user document to MongoDB."""
    mongo.db.users.insert_one({
        'username': username,
        'password': generate_password_hash(password),  # Hash password for security
        'mac_address': mac_address
    })

def find_user(mongo, username):
    """Find a user in MongoDB by username."""
    return mongo.db.users.find_one({'username': username})

