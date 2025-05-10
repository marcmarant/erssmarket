from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
from ..api.productos import get_products, get_products_query
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
            print(f"Usuario autenticado con ID: {user_identity}")
        else:
            print("Usuario no autenticado, mostrando página como visitante")

    except Exception as e:
        print(f"Error al verificar JWT: {str(e)}")
     
    #Cuando esté la bd hacer consulta a los usuarios registrados para conocer quien de ellos es el que ha accedido a la pagina 
    #usuarios = get_users() 

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
            print("Error: El ID de usuario no es un número válido.")    # Esto es algo que no debería ocurrir

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


from flask import request

@main.route('/selector')
def selector():
    # Obtener el ID del usuario desde los parámetros de la URL
    user_id = request.args.get('user_id') # Este para cuando funcione la bd, debería ser el objeto usuario directamente y no user_id

    usuario_actual = None
    users_list = [
        Usuario(1, 'Juan Pérez', 'juan.perez@example.com', 'pass123', '2025-04-30T12:34:56'),
        Usuario(2, 'Ana López', 'ana.lopez@example.com', 'asv134', '2025-04-30T13:45:12')
    ]

    # Buscar el usuario en la lista usando el ID
    if user_id:
        try:
            user_id = int(user_id)
            for usuario in users_list:
                if usuario.id == user_id:
                    usuario_actual = usuario
                    break
            print(f"Usuario encontrado en selector: {usuario_actual}")
        except ValueError:
            print("Error: El ID de usuario no es un número válido.")

    productos = get_products_query() # Cargamos los porductos que se encuentran en la tienda, estos los debe de coger de la bd
    return render_template('selector.html', productos=productos, usuario=usuario_actual)
