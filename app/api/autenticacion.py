from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from ..db import db
from ..db import Usuario

autenticacion = Blueprint('autenticacion', __name__)

"""
Función auxiliar para obtener un usuario por su ID.
"""
def get_user_by_id(id):
    user = Usuario.query.filter_by(id=id).first()
    return user.to_dict() if user else None

"""
Ruta para registrar un usuario, una vez registrado se devuelve el token JWT.
"""
@autenticacion.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nombre = data.get('nombre')
    if not email or not password or not nombre:
        return jsonify({'error': 'Los campos email, contraseña y nombre son necesarios'}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400

    nuevo_usuario = Usuario(email=email, contrasenya=password, nombre=nombre) # Los usuarios que se registran no se añaden como administradores
    db.session.add(nuevo_usuario)
    db.session.flush()  # Para obtener el id del usuario que se acaba de crear
    db.session.commit()
    
    response = jsonify({"message": "Usuario creado con éxito"})
    access_token = create_access_token(
        identity=str(nuevo_usuario.id), 
        expires_delta=False,  
    )
    set_access_cookies(response, access_token)
    return response, 200

"""
Ruta para el login del usuario, recibe email y contraseña
y devuelve un token JWT si las credenciales son correctas.
"""
@autenticacion.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Los campos email y contraseña son necesarios'}), 400

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Usuario o Contraseña incorrecta"}), 400
    if user.contrasenya != password:
        return jsonify({"error": "Usuario o Contraseña incorrecta"}), 400

    response = jsonify({"message": "Inicio de sesión realizado con éxito"})
    access_token = create_access_token(
        identity=str(user.id), 
        expires_delta=False,  
    )
    set_access_cookies(response, access_token)
    return response, 200

"""
Ruta para el logout del usuario, borrando la cookie con el token JWT
"""
@autenticacion.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout realizado con éxito"})
    unset_jwt_cookies(response)  # Esto elimina el JWT de las cookies
    return response, 200
