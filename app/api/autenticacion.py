from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from ..db import db
from ..db import Usuario

autenticacion = Blueprint('autenticacion', __name__)
# TODO : Borrar a futuro usuarios de prueba a falta de DB
users = [
  Usuario(1, 'Juan Pérez', 'juan.perez@example.com', 'pass123', '2025-04-30T12:34:56',True),
  Usuario(2, 'Ana López', 'ana.lopez@example.com', 'asv134', '2025-04-30T13:45:12')
]

def get_user_by_id(id):
  #user = Usuario.query.get(user_id)
  user = next((u for u in users if u.id == int(id)), None)  # Simulando la consulta a la base de datos
  return user

def get_users_query():

  users = [
    Usuario(1, 'Juan Pérez', 'juan.perez@example.com', 'pass123', '2025-04-30T12:34:56', True),
    Usuario(2, 'Ana López', 'ana.lopez@example.com', 'asv134', '2025-04-30T13:45:12')
  ]
  users_list = []
  for user in users:
      users_list.append({
          "id": user.id,
          "nombre": user.nombre,
          "email": user.email,
          "fecha_creacion": user.fecha_creacion
      })
  return users_list


"""
TODO Ruta para el registro del usuario
"""
@autenticacion.route('/register', methods=['POST'])
def register():
  print("Registrando usuario")
  return 200


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

  #user = Usuario.query.filter_by(email=email).first()
  user = next((u for u in users if u.email == email), None) # Simulando la consulta a la base de datos

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



# PRUEBA
@autenticacion.route('/users', methods=['GET'])
def get_users():
  try:
    #users = Usuario.query.all()
    # Simulando la consulta a la base de datos
    get_users_query()
    return jsonify(users_list), 200
  except Exception as e:
    print(f"Error al obtener los usuarios: {e}")
    return jsonify({"error": "Error al obtener los usuarios"}), 500