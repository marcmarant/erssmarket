from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.db import db, Carrito, Producto

carrito = Blueprint('carrito', __name__)

def get_carrito_products_query(user_id):
    productos_cantidad = db.session.query(Producto, Carrito.cantidad).join(
        Carrito, Producto.id == Carrito.producto_id
    ).filter(Carrito.usuario_id == user_id).all()
    productos_carrito = [
        {
            **producto.to_dict(),
            'cantidad': cantidad
        }
        for producto, cantidad in productos_cantidad
    ]
    precio_total = sum(producto['precio'] * producto['cantidad'] for producto in productos_carrito)
    return productos_carrito, precio_total

"""
Ruta que devuelve los productos que tiene el carrito actualmente.
"""
@carrito.route('/', methods=['GET'])
@jwt_required()
def get_carrito():
    try:
        user_id = get_jwt_identity()
        productos_carrito, precio_total = get_carrito_products_query(user_id)
        return jsonify({
            "productos": productos_carrito,
            "precio_total": precio_total
        }), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener los datos del carrrito"}), 500

"""
Ruta que agrega un producto al carrito del usuario.
"""
@carrito.route('/agregar', methods=['POST'])
@jwt_required()
def agregar_al_carrito():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1) # si no se pasa cantidad, se asume 1
        if not producto_id or cantidad <= 0:
            return jsonify({"error": "Peticion invalida"}), 400

        producto_en_carrito = Carrito.query.filter_by(usuario_id=user_id, producto_id=producto_id).first()

        if producto_en_carrito:
            producto_en_carrito.cantidad += cantidad
        else:
            nuevo_producto = Carrito(usuario_id=user_id, producto_id=producto_id, cantidad=cantidad)
            db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"message": "Producto agregado al carrito"}), 200
    except Exception:
        return jsonify({"error": "Error insertando el producto en el carrito"}), 500

"""
Ruta que vacia el carrito de un usuario.
"""
@carrito.route('/vaciar', methods=['DELETE'])
@jwt_required()
def vaciar_carrito():
    try:
        user_id = get_jwt_identity()
        Carrito.query.filter_by(usuario_id=user_id).delete()
        db.session.commit()
        return jsonify({"mensaje": "Carrito vaciado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error al intentar vaciar el carrito"}), 500

"""
Ruta que quita una unidad de un producto del carrito.
"""
@carrito.route('/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def substract_from_carrito(producto_id):
    try:
        user_id = get_jwt_identity()
        item_carrito = Carrito.query.filter_by(usuario_id=user_id, producto_id=producto_id).first()

        if not item_carrito:
            return jsonify({"error": "Producto no encontrado en el carrito"}), 404
        
        if item_carrito.cantidad > 0:
            item_carrito.cantidad -= 1
        else:
            db.session.delete(item_carrito)
        db.session.commit()
        return jsonify({"mensaje": "Producto retirado del carrito"}), 200
    except Exception as e:
        return jsonify({"error": "Error al intentar vaciar el carrito"}), 500
