from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db, Carrito, Pedido, Producto_pedido
import time

compra = Blueprint('compra', __name__)

"""
Ruta para realizar una compra de los productos que el usuario tenga en el carrito.
"""
@compra.route('/', methods=['POST'])
@jwt_required()
def compra():
    try:
        user_id = get_jwt_identity()
        carrito = Carrito.query.filter_by(usuario_id=user_id).all()
        if not carrito:
            return jsonify({"error": "El carrito está vacío"}), 400

        precio_total = sum(producto.precio * producto.cantidad for producto in carrito)

        # Simulación del proceso de pago (espera de 3 segundos)
        time.sleep(3)

        # Se crea el pedido
        nuevo_pedido = Pedido(
            usuario_id=user_id,
            precio_total=precio_total
        )
        db.session.add(nuevo_pedido)
        db.session.flush() # de esta forma se obtiene el id del pedido recien creado

        # Se agregan los productos del carrito al pedido
        for item in carrito:
            producto_pedido = Producto_pedido(
                pedido_id=nuevo_pedido.id,
                producto_id=item.producto_id,
                precio=item.producto.precio,
                cantidad=item.cantidad
            )
            db.session.add(producto_pedido)

        Carrito.query.filter_by(usuario_id=user_id).delete() # Se vacia el carrito
        db.session.commit()
        return jsonify({"message": "Compra realizada con exito"}), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los pedidos realizados por el usuario"}), 500
