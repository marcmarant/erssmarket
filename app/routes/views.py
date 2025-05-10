from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from ..api.productos import get_products
from ..api.autenticacion import get_users
from ..db import db
from ..db import Usuario

main = Blueprint('main', __name__)

@main.route('/')
def home():
    try:
        # Verificar si el JWT está presente en las cookies de la solicitud
        print("Verificando JWT en la solicitud...")
        verify_jwt_in_request(optional=True)  # La verificación no es obligatoria
        
        user_identity = get_jwt_identity()  # Obtiene la identidad del usuario desde el token
        
        if user_identity:
            # Si hay un JWT válido, el usuario está autenticado
            print(f"Usuario autenticado con ID: {user_identity}")
        else:
            # Si no hay JWT válido, el usuario no está autenticado
            print("Usuario no autenticado, mostrando página como visitante")

    except Exception as e:
        # En caso de error al verificar el JWT
        print(f"Error al verificar JWT: {str(e)}")
    
    # Renderizar siempre la página principal
    print("Renderizando página principal")

    #usuarios = get_users()
    #print(usuarios)
    # Buscar el usuario actual por ID
    usuario_actual = None
    
    users_list = [
    Usuario(1, 'Juan Pérez', 'juan.perez@example.com', 'pass123', '2025-04-30T12:34:56'),
    Usuario(2, 'Ana López', 'ana.lopez@example.com', 'asv134', '2025-04-30T13:45:12')
    ]

    if user_identity:
        try:
            user_id = int(user_identity)
            for usuario in users_list:
                if usuario.id == user_id:
                    usuario_actual = usuario
            print(f"Usuario encontrado: {usuario_actual}")
        except ValueError:
            print("Error: El ID de usuario no es un número válido.")
    
    # Renderizar la página principal con el usuario actual si existe
    print("Renderizando página principal")
    return render_template('home.html', usuario=usuario_actual)

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

