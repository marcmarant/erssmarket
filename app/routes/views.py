from flask import Blueprint, render_template, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html');

@main.route('/home2')
def home2():
    return render_template('home2.html');

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
    return render_template('login.html');

@main.route('/selector')
def selector():
    return render_template('selector.html');