from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

carrito = Blueprint('carrito', __name__)


@carrito.route('/agregar', methods=['POST'])
def agregar_al_carrito():
  try:
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    producto_id = data.get('id')
    cantidad = int (data.get('cantidad'))

    if (cantidad <= 0):
      return jsonify({'error': 'cantidad incorrecta'})

      producto = Carrito.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()

      if producto:
        producto.cantidad += cantidad
      else:
        producto = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(producto)

      db.session.commit()
      return jsonify({'message': f'Producto añadido al carrito correctamente. Cantidad: {cantidad}'}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 500

