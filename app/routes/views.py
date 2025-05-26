from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from ..api.productos import get_products, get_products_query
from ..api.autenticacion import get_users
from ..db import db
from ..db import Usuario

main = Blueprint('main', __name__)

@main.route('/')
def home():  
    return render_template('home.html')

"""
Ruta con la vista para iniciar sesión en la aplicación
Si el usuario ya está loggeado se le redirige a home.
"""
@main.route('/login')
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/selector')
def selector():
    productos = get_products_query() # Cargamos los porductos que se encuentran en la tienda, estos los debe de coger de la bd
    return render_template('selector.html', productos=productos)

@main.route('/editor')
def editor():
    productos = get_products_query()
    return render_template('editor.html', productos=productos)

"""
Ruta con la vista en la que se muestra el listado de pedidos
realizados por el usuario y sus detalles.
"""
@main.route('/pedidos')
def pedidos():
    # Llamar a la API de los pedidos
    pedidos = [
        {
            "id": 1,
            "usuario_id": 1,
            "fecha": "2025-5-10",
            "productos": [
                {"nombre": "balon", "cantidad": 3, "precio": 4.99, "fotoUrl": "/static/images/balon.jpg"},
                {"nombre": "camiseta", "cantidad": 1, "precio": 10.5, "fotoUrl": "/static/images/camiseta.jpg"}
            ],
            "precio_total": 25.47
        },
        {
            "id": 2,
            "usuario_id": 2,
            "fecha": "2025-4-13",
            "productos": [
                {"nombre": "balon", "cantidad": 3, "precio": 4.99, "fotoUrl": "/static/images/balon.jpg"},
                {"nombre": "camiseta", "cantidad": 1, "precio": 10.5, "fotoUrl": "/static/images/camiseta.jpg"}
            ],
            "precio_total": 25.47
        }
    ]
    # Borrar lo anterior y pillarlo con una funcion
    return render_template('pedidos.html', pedidos=pedidos)