from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from ..api.productos import get_products, get_products_query
from ..api.autenticacion import get_users, get_user_by_id
from ..db import db
from ..db import Usuario

main = Blueprint('main', __name__)

"""
Función para inyectar el objeto con el usuario actual, de forma.
que este sera accesible en todas las vistas de la aplicación.
"""
@main.app_context_processor
@jwt_required(optional=True)
def inject_user_info():
    user_id = get_jwt_identity()
    if user_id:
        user = get_user_by_id(user_id)
    else:
        user = None
    return {'current_user': user}

"""
Ruta principal de la aplicación, muestra la vista de inicio.
"""
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
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('login.html')

"""
Ruta con la vista para registrar un nuevo usuario.
Si el usuario ya está loggeado se le redirige a home.
"""
@main.route('/register')
@jwt_required(optional=True)
def register():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('register.html')

@main.route('/selector')
def selector():
    productos = get_products_query() # Cargamos los porductos que se encuentran en la tienda, estos los debe de coger de la bd
    return render_template('selector.html', productos=productos)

"""
Ruta con la vista para editar los productos del catalogo
Esta vista solo es accesible a los usuarios que sean administradores.
"""
@main.route('/editor')
@jwt_required(optional=True)
def editor():
    user_id = get_jwt_identity()
    if user_id:
        user = get_user_by_id(user_id)
        if user.is_admin:
            productos = get_products_query()
            return render_template('editor.html', productos=productos)
    return redirect(url_for('main.login'))
    

"""
Ruta con la vista en la que se muestra el listado de pedidos
realizados por el usuario y sus detalles.
"""
@main.route('/pedidos')
@jwt_required(optional=True)
def pedidos():
    user_id = get_jwt_identity()
    if not user_id:
        return redirect(url_for('main.login'))
    # Llamar a la API de los pedidos
    # Borrar lo anterior y pillarlo con una funcion
    return render_template('pedidos.html', pedidos=pedidos)