from flask import Blueprint
from .autenticacion import autenticacion

# Función para inicializar la API
def init_api(app):
    app.register_blueprint(autenticacion) 