from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Usuario

autenticacion = Blueprint('autenticacion', __name__)

@autenticacion.route('/login', methods=['POST'])
def login():
  print("Loggeando usuario")
  return jsonify({"message": "usuario loggeado correctamente"}), 200

@autenticacion.route('/register', methods=['POST'])
def register():
  print("Registrando usuario")
  return 200

@autenticacion.route('/users', methods=['GET'])
def get_users():
  try:
    #users = Usuario.query.all()
    # Simulando la consulta a la base de datos
    users = [
      Usuario(1, "Juan Pérez", "juan.perez@example.com", "paswfwewv", "2025-04-30T12:34:56"),
      Usuario(2, "Ana López", "ana.lopez@example.com", "asv134", "2025-04-30T13:45:12")
    ]

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