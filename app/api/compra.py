from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db, Carrito, Pedido, Producto_pedido, Producto
import time

compra = Blueprint('compra', __name__)

"""
Ruta para realizar una compra de los productos que el usuario tenga en el carrito.
"""
@compra.route('/', methods=['POST'])
@jwt_required()
def do_compra():
    try:
        user_id = get_jwt_identity()
        carrito = Carrito.query.filter_by(usuario_id=user_id).all()
        if not carrito:
            return jsonify({"error": "El carrito está vacío"}), 400

        precios = []
        productos_actualizados = []
        for item in carrito:
            producto = Producto.query.filter_by(id=item.producto_id).first()
            if not producto:
                return jsonify({"error": f"Producto con ID {item.producto_id} no encontrado"}), 404
            if producto.stock < item.cantidad:
                return jsonify({"error": f"Stock insuficiente para el producto '{producto.nombre}' (Stock disponible: {producto.stock})"}), 400
            precios.append((producto.id, producto.precio, item.cantidad)) # Guardamos el precio y la cantidad del producto
            producto.stock -= item.cantidad  # Reducimos stock
            productos_actualizados.append(producto) # Guardamos el producto con el stock actualizado

        # Simulación del proceso de pago (espera de 3 segundos)
        time.sleep(3)

        # Se crea el pedido
        nuevo_pedido = Pedido(
            usuario_id=user_id,
            precio_total=sum(precio * cantidad for _, precio, cantidad in precios)
        )
        db.session.add(nuevo_pedido)
        db.session.flush() # de esta forma se obtiene el id del pedido recien creado

        # Se agregan los productos del carrito al pedido
        for item in carrito:
            precio = next((precio for producto_id, precio, cantidad in precios if producto_id == item.producto_id), None)
            producto_pedido = Producto_pedido(
                pedido_id=nuevo_pedido.id,
                producto_id=item.producto_id,
                precio=precio,
                cantidad=item.cantidad
            )
            db.session.add(producto_pedido)

        # Una vez que se ha realizado el pedido se actualiza el stock de los productos
        for producto in productos_actualizados:
            db.session.add(producto)

        Carrito.query.filter_by(usuario_id=user_id).delete() # Se vacia el carrito
        db.session.commit()
        return jsonify({"message": "Compra realizada con exito"}), 200
    except Exception:
        return jsonify({"error": "Error al realizar la compra"}), 500
