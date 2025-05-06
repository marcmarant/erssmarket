from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from ..db import db
from ..db import Usuario

autenticacion = Blueprint('autenticacion', __name__)
# TODO : Borrar a futuro usuarios de prueba a falta de DB
users = [
  Usuario(1, "Juan Pérez", "juan.perez@example.com", "pass123", "2025-04-30T12:34:56"),
  Usuario(2, "Ana López", "ana.lopez@example.com", "asv134", "2025-04-30T13:45:12")
]

"""
Ruta para el login del usuario, recibe email y contraseña
y devuelve un token JWT si las credenciales son correctas.
"""
@autenticacion.route('/login', methods=['POST'])
@jwt_required()
def login():
  data = request.json
  email = data.get('email')
  contrasenya = data.get('contrasenya')

  if not email or not contrasenya:
    return jsonify({"error": "Email y contraseña son requeridos"}), 400

  #user = Usuario.query.filter_by(email=email).first()
  user = next((u for u in users if u.email == email), None) # Simulando la consulta a la base de datos

  if not user:
    return jsonify({"error": "Usuario o Contraseña incorrecta"}), 400

  # check password
  if user.contrasenya != contrasenya:
    return jsonify({"error": "Usuario o Contraseña incorrecta"}), 400

  access_token = create_access_token(identity={"id": user.id, "nombre": user.nombre, "email": user.email})
  return jsonify({"token": access_token}), 200


"""
TODO Ruta para el registro del usuario
"""
@autenticacion.route('/register', methods=['POST'])
def register():
  print("Registrando usuario")
  return 200

# PRUEBA
@autenticacion.route('/users', methods=['GET'])
def get_users():
  try:
    #users = Usuario.query.all()
    # Simulando la consulta a la base de datos

    users_list = []
    for user in users:
      users_list.append({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "fecha_creacion": user.fecha_creacion
      })
    return jsonify(users_list), 200
  except Exception as e:
    print(f"Error al obtener los usuarios: {e}")
    return jsonify({"error": "Error al obtener los usuarios"}), 500