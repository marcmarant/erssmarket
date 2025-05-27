from flask import Blueprint, render_template
from ..api.autenticacion import autenticacion
from ..api.productos import productos
from ..api.carrito import carrito
from ..api.pedidos import pedidos
from ..api.compra import compra
from ..api.menu import menu

api = Blueprint('api', __name__)

api.register_blueprint(autenticacion)
api.register_blueprint(productos, url_prefix='/productos')
api.register_blueprint(carrito, url_prefix='/carrito') 
api.register_blueprint(pedidos, url_prefix='/pedidos')
api.register_blueprint(compra, url_prefix='/checkout')
api.register_blueprint(menu, url_prefix='/menu') 
