from flask import Blueprint
from .autenticacion import autenticacion
from .productos import productos
from .carrito import carrito

# Función para inicializar la API
def init_api(app):
    app.register_blueprint(autenticacion)
    app.register_blueprint(productos)
    app.register_blueprint(carrito, url_prefix='/carrito') 