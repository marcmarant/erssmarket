from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

carrito = Blueprint('carrito', __name__)


@carrito.route('/agregar', methods=['POST'])
def agregar_al_carrito():

  printf("Entro a agregar producto en el carrito")
  try:
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    producto_id = data.get('id')
    cantidad = int (data.get('cantidad'))

    if (cantidad <= 0):
      return jsonify({'error': 'cantidad incorrecta'})

    """
    #Cuando haya bd se busca si actualemnte hay un carrito asignado a este usuario
    carrito_item = Carrito.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()

    if carrito_item:
        # Si ya existe, aumentar la cantidad
        carrito_item.cantidad += cantidad
    else:
        # Si no existe, crear una nueva entrada en el carrito
        carrito_item = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(carrito_item)

    db.session.commit()
    """
    print("Producto añadido al carrito")
    return jsonify({'message': f'Producto añadido al carrito correctamente. Cantidad: {cantidad}'}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 500

