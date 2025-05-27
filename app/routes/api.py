from flask import Blueprint, render_template
from ..api.autenticacion import autenticacion
from ..api.productos import productos
from ..api.carrito import carrito
from ..api.pedidos import pedidos

api = Blueprint('api', __name__)

api.register_blueprint(autenticacion)
api.register_blueprint(productos, url_prefix='/productos')
api.register_blueprint(carrito, url_prefix='/carrito') 
api.register_blueprint(pedidos, url_prefix='/pedidos') 