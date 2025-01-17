from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

# Initialize PyMongo
mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # MongoDB connection URI
    app.config['MONGO_URI'] = "mongodb+srv://nikhilsaravanan944:nikhi09@mac-auth.foem3.mongodb.net/?retryWrites=true&w=majority&appName=mac-auth"
    app.config['SECRET_KEY'] = 'my$up3r$3cur3K3y'  # Your secret key

    # Initialize PyMongo
    mongo.init_app(app)

    # Enable CORS
    CORS(app)

    # Import and register routes
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
