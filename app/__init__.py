from flask import Flask
from dotenv import load_dotenv
from .routes import init_routes
from .db import init_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    #app.config.from_pyfile('../config.py')

    init_db(app)
    init_routes(app)


    return app