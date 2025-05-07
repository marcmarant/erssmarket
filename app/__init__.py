from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .routes import init_routes
from .db import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuracion de JWT para guardar el token en una cookie
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False # Ya que no usamos https
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/' # Cookie disponible en todas las rutas
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False # Para que no haya problemas con el CSRF
    
    jwt = JWTManager(app)

    init_db(app)
    init_routes(app)


    return app