from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

productos = Blueprint('productos', __name__)

@productos.route('/productos', methods=['GET'])
def get_products():
  try:
    #users = Producto.query.all()
    # Simulando la consulta a la base de datos
    products = [
      Producto(1, "Producto 1", 350, None),
      Producto(2, "Producto 2", 1100, None)
    ]

    products_list = []
    for product in products:
      products_list.append({
        "id": product.id,
        "nombre": product.nombre,
        "precio": product.precio,
        "fotoUrl": product.fotoUrl
      })
    return jsonify(users_list), 200
  except Exception as e:
    print(f"Error al obtener los productos: {e}")
    return jsonify({"error": "Error al obtener los productos"}), 500

#  /api/productos/{id}