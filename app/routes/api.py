from flask import Blueprint, render_template
from ..api.autenticacion import autenticacion
from ..api.productos import productos
from ..api.carrito import carrito

api = Blueprint('api', __name__)

api.register_blueprint(autenticacion)
api.register_blueprint(productos)
api.register_blueprint(carrito, url_prefix='/carrito') 