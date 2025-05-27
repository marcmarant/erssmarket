from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db, Pedido, Carrito, Producto

pedidos = Blueprint('pedidos', __name__)

"""
Ruta que devuelve los productos que tiene el carrito actualmente.
"""
@pedidos.route('/', methods=['GET'])
@jwt_required()
def get_pedidos():
    try:
        user_id = get_jwt_identity()
        pedidos = Pedido.query.filter_by(usuario_id=user_id).all()
        resultado = []
        for pedido in pedidos:
            productos_pedido = db.session.query(Producto.nombre, Producto_pedido.cantidad, Producto_pedido.precio).join(
                Producto_pedido, Producto.id == Producto_pedido.producto_id
            ).filter(Producto_pedido.pedido_id == pedido_id).all()
            pedido_info = {
                'id': pedido.id,
                'fecha_creacion': pedido.fecha_creacion,
                'precio_total': pedido.precio_total,
                'productos': [
                    {
                        'nombre': producto.nombre,
                        'cantidad': producto_pedido.cantidad,
                        'precio': producto_pedido.precio
                    }
                    for producto, producto_pedido in productos_pedido
                ]
            }
            resultado.append(pedido_info)
        return jsonify(resultado), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los pedidos realizados por el usuario"}), 500

"""
Ruta que devuelve los detalles de un pedido en concreto
"""
@pedidos.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_pedido_por_id(id):
    try:
        user_id = get_jwt_identity()
        pedido = Pedido.query.filter_by(usuario_id=user_id).all()

        if not pedido:
            return jsonify({"error": "Pedido no encontrado"}), 404

        productos_pedido = db.session.query(Producto.nombre, Producto_pedido.cantidad, Producto_pedido.precio).join(
            Producto_pedido, Producto.id == Producto_pedido.producto_id
        ).filter(Producto_pedido.pedido_id == pedido_id).all()
        pedido_info = {
            'id': pedido.id,
            'fecha_creacion': pedido.fecha_creacion,
            'precio_total': pedido.precio_total,
            'productos': [
                {
                    'nombre': producto.nombre,
                    'cantidad': producto_pedido.cantidad,
                    'precio': producto_pedido.precio
                }
                for producto, producto_pedido in productos_pedido
            ]
        }
        return jsonify(pedido_info), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los detalles del pedido"}), 500
