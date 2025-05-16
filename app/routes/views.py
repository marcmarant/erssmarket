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
Si el usuario ya está loggeado se le redirige a home
"""
@main.route('/login')
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('login.html')


from flask import request

@main.route('/selector')
def selector():
    productos = get_products_query() # Cargamos los porductos que se encuentran en la tienda, estos los debe de coger de la bd
    return render_template('selector.html', productos=productos)

@main.route('/editor')
def editor():
    productos = get_products_query()
    return render_template('editor.html', productos=productos)