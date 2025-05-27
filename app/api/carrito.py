from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..db import db
from ..db import Producto
from api import carrito


carrito_bp = Blueprint('carrito', __name__)


@carrito_bp.route('/carrito/agregar', methods=['POST'])
@jwt_required()
def agregar_al_carrito():

  print("Entro a agregar producto en el carrito")
  try:
    data = request.get_json()
    usuario_id = get_jwt_identity()
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

@carrito_bp.route('/carrito', methods=['GET'])
def obtener_carrito():
    contenido = []
    for prod_id, cantidad in carrito.items():
        producto = next((p for p in productos if p["id"] == prod_id), None)
        if producto:
            contenido.append({
                "id": prod_id,
                "nombre": producto["nombre"],
                "precio_unitario": producto["precio"],
                "cantidad": cantidad,
                "total": producto["precio"] * cantidad
            })
    return jsonify(contenido)

  
@carrito_bp.route('carrito/vaciar', methods=['DELETE'])
@jwt_required()
def vaciar_carrito():
    carrito.clear()
    return jsonify({"mensaje": "Carrito vaciado correctamente"})

