from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db, Pedido, Carrito, Producto, Producto_pedido

pedidos = Blueprint('pedidos', __name__)

"""
Función auxiliar para obtener un pedido por su ID.
"""
def get_pedido_details(pedido):
    productos_pedido = db.session.query(Producto.nombre, Producto_pedido.cantidad, Producto_pedido.precio, Producto.fotoUrl).join(
        Producto_pedido, Producto.id == Producto_pedido.producto_id
    ).filter(Producto_pedido.pedido_id == pedido.id).all()
    pedido_info = {
        'id': pedido.id,
        'fecha_creacion': pedido.fecha_creacion,
        'precio_total': pedido.precio_total,
        'productos': [
            {
                'nombre': nombre,
                'cantidad': cantidad,
                'precio': precio,
                'fotoUrl': fotoUrl
            }
            for nombre, cantidad, precio, fotoUrl in productos_pedido
        ]
    }
    return pedido_info

"""
Función auxiliar que devuelve todos los pedidos
"""
def get_pedidos_by_user(user_id):
    pedidos = Pedido.query.filter_by(usuario_id=user_id).all()
    resultado = []
    for pedido in pedidos:
        pedido_info = get_pedido_details(pedido)
        resultado.append(pedido_info)
    return resultado

"""
Ruta que devuelve los productos que tiene el carrito actualmente.
"""
@pedidos.route('/', methods=['GET'])
@jwt_required()
def get_pedidos():
    try:
        user_id = get_jwt_identity()
        pedidos = get_pedidos_by_user(user_id)
        return jsonify(pedidos), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los pedidos realizados por el usuario"}), 500

"""
Ruta que devuelve los detalles de un pedido en concreto
"""
@pedidos.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_pedido_por_id(id):
    try:
        pedido = Pedido.query.filter_by(id=id).first()
        if not pedido:
            return jsonify({"error": "Pedido no encontrado"}), 404
        pedido_info = get_pedido_details(pedido)
        return jsonify(pedido_info), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los detalles del pedido"}), 500
