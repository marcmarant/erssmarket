from flask import Flask
from dotenv import load_dotenv
from .routes import init_routes
from .db import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuracion del secreto de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    init_db(app)
    init_routes(app)


    return app