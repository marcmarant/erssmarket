from flask import Flask
from .views import main
from .api import api

def init_routes(app):
    """
    Inicializa las rutas de la aplicación Flask.
    Tanto de la interfaz de usuario como de la API.
    """
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
