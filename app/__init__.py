from flask import Flask, g, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request
from dotenv import load_dotenv
from datetime import timedelta
from .routes import init_routes
from .db import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración de JWT para guardar el token en una cookie
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_super_secret_key') 
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365)  # Un año
    app.config['JWT_IDENTITY_CLAIM'] = 'identity'  # Esto define el nombre del campo en el token JWT

    jwt = JWTManager(app)
    
    init_db(app)
    init_routes(app)

    return app
