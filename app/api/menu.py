from flask import Blueprint, jsonify

menu = Blueprint('menu', __name__)

"""
Ruta para devolver informacion general de la tienda y categorias de productos.
"""
@menu.route('/', methods=['GET'])
def get_menu():
    try:
        return jsonify({
        "titulo": "SportMarket",
        "secciones": [
            "Página principal",
            "Selector de productos",
            "Carrito",
            "Pedidos",
            "Editor",
        ],
        "categorias": [
            "Deporte",
            "Ropa",
            "Fútbol"
        ]
        }), 200
    except Exception:
        return jsonify({"error": "Error al intentar obtener la informacion"}), 500
