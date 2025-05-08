from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

carrito = Blueprint('carrito', __name__)


@carrito.route('/agregar', methods=['POST'])
def get_products():
  try:
    get_products_query()
    return jsonify(products_list), 200
  except Exception as e:
    print(f"Error al obtener los productos: {e}")
    return jsonify({"error": "Error al obtener los productos"}), 500

#  /api/productos/{id}