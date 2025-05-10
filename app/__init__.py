from flask import Flask, g, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request
from dotenv import load_dotenv
from .routes import init_routes
from .db import init_db
import os
from datetime import timedelta

load_dotenv()

def get_current_user():
    """
    Función global para obtener el usuario actual.
    Retorna el diccionario con el ID y el rol del usuario autenticado o None si no está autenticado.
    """
    try:
        user_id = get_jwt_identity()
        role = g.get('jwt', {}).get('role', 'invitado')  # Obtener el rol desde los claims adicionales
        if user_id:
            return {"id": str(user_id), "role": role}
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        return None

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
