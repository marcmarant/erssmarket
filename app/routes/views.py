from flask import Blueprint, render_template, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..api.productos import get_products

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

@main.route('/selector')
def selector():
    productos = get_products()
    return render_template('selector.html', productos = productos)