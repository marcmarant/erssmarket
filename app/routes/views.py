from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from ..api.productos import get_products_query, get_available_products_query
from ..api.carrito import get_carrito_products_query
from ..api.pedidos import get_pedidos_by_user
from ..api.autenticacion import get_user_by_id
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
Función para inyectar el número de productos en el carrito del usuario actual,
de forma que este sera accesible en todas las vistas de la aplicación.
"""
@main.app_context_processor
@jwt_required(optional=True)
def inject_carrito_length_info():
    user_id = get_jwt_identity()
    carrito_length = 0
    if user_id:
        carrito_length = len(get_carrito_products_query(user_id)[0])
    return {'carrito_length': carrito_length}

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

"""
Ruta con los diferentes productos para que el usuario
los pueda agregar al carrito.
"""
@main.route('/productos')
def selector():
    carritoLength = 0
    productos = get_available_products_query()
    return render_template('productos.html', productos=productos)

"""
Ruta con los productos agregados al carrito, de forma que el usuario
pueda vaciarlo o efectuar la compra.
"""
@main.route('/carrito')
@jwt_required(optional=True)
def carrito():
    user_id = get_jwt_identity()
    if user_id:
        carrito, precio_total = get_carrito_products_query(user_id)
        return render_template('carrito.html', carrito=carrito, precio_total=precio_total)
    return redirect(url_for('main.login'))

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
        if user and user['is_admin']:
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
    pedidos = get_pedidos_by_user(user_id)
    return render_template('pedidos.html', pedidos=pedidos)
    