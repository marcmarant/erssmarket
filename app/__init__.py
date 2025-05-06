from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .routes import init_routes
from .db import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuracion de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    jwt = JWTManager(app)

    init_db(app)
    init_routes(app)


    return app