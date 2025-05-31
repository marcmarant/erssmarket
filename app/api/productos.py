from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

productos = Blueprint('productos', __name__)

"""
Función auxiliar que devuelve todos los productos, esten o no disponibles.
"""
def get_products_query():
    available_products = Producto.query.all()
    return [product.to_dict() for product in available_products]

"""
Función auxiliar que devuelve todos los productos disponibles.
"""
def get_available_products_query():
    available_products = Producto.query.filter(Producto.stock > 0).all()
    return [product.to_dict() for product in available_products]

"""
Ruta que devuelve todos los productos disponibles.
"""
@productos.route('/', methods=['GET'])
def get_products():
    try:
        products = get_available_products_query()
        return jsonify(products), 200
    except Exception:
        return jsonify({"error": "Error al obtener los productos"}), 500

"""
Ruta que devuelve un producto específico por su id.
"""
@productos.route('/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Producto.query.filter(Producto.id == id).first()
        if not product:
            return jsonify({"error": "No existe ningún producto con el id dado"}), 404
        return jsonify(product.to_dict()), 200
    except Exception:
        return jsonify({"error": "Error al obtener el producto"}), 500

"""
Ruta que actualiza completamente un producto.
"""
@productos.route('/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()
        product = Producto.query.filter(Producto.id == id).first()
        if not product:
            print("LLEGO AQUI")
            return jsonify({"error": "No existe ningún producto con el id dado"}), 404
        if 'nombre' not in data or 'descripcion' not in data or 'precio' not in data or 'stock' not in data:
            return jsonify({"error": "Peticion Invalida se necesita nombre, descripción, precio y stock"}), 400
        if not isinstance(data['precio'], (int)) or data['precio'] <= 0:
            return jsonify({"error": "El precio debe ser un entero positivo en centimos"}), 400
        if not isinstance(data['stock'], (int)) or data['stock'] < 0:
            return jsonify({"error": "El stock debe ser un entero"}), 400
        product.nombre = data['nombre']
        product.descripcion = data['descripcion']
        product.precio = data['precio']
        product.stock = data['stock']
        db.session.commit()
        return jsonify({"message": "Producto actualizado correctamente"}), 200
    except Exception:
        return jsonify({"error": "Error al actualizar el producto"}), 500

"""
Ruta que actualiza parcialmente un producto.
"""
@productos.route('/<int:id>', methods=['PATCH'])
def update_product_field(id):
    try:
        data = request.get_json()
        product = Producto.query.filter(Producto.id == id).first()
        if not product:
            return jsonify({"error": "No existe ningún producto con el id dado"}), 404
        if 'nombre' not in data and 'descripcion' not in data and 'precio' not in data and 'stock' not in data:
            return jsonify({"error": "Peticion Invalida, se necesita al menos nombre, descripcion, precio o stock"}), 400
        if 'nombre' in data:
            product.nombre = data['nombre']
        if 'descripcion' in data:
            product.descripcion = data['descripcion']
        if 'precio' in data:
            if not isinstance(data['precio'], (int)):
                return jsonify({"error": "El precio debe ser un entero en centimos"}), 400
            product.precio = data['precio']
        if 'stock' in data:
            if not isinstance(data['stock'], (int)):
                return jsonify({"error": "El stock debe ser un entero"}), 400
            product.stock = data['stock']
        db.session.commit()
        return jsonify({"message": "Producto actualizado correctamente"}), 200
    except Exception:
        return jsonify({"error": "Error al actualizar el producto"}), 500
