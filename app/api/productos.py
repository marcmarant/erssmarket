from flask import Blueprint, jsonify, request
from ..db import db
from ..db import Producto

productos = Blueprint('productos', __name__)

def get_products_query():

    #users = Producto.query.all()
    # Simulando la consulta a la base de datos
    products = [
      Producto(1, "Balón de fútbol", "Balón de fútbol clásico, perfecto para entrenamientos y partidos. Fabricado con materiales resistentes y cosido a máquina para mayor durabilidad. Su superficie de cuero sintético garantiza un toque suave y un control óptimo. Ideal para jugadores de todas las edades y niveles.", 25, "../static/images/balon.jpg", 1),
      Producto(2, "Guantes de fútbol", "Guantes de fútbol diseñados para ofrecer un agarre seguro y cómodo en todas las condiciones. Fabricados con materiales transpirables y resistentes, garantizan máxima protección y durabilidad. Su palma de látex antideslizante asegura un excelente control del balón. Ideales para entrenamientos y partidos.", 15, "../static/images/guantes.jpg", 1),
      Producto(3, "Camiseta Deportiva", "Camiseta deportiva ligera y cómoda, ideal para entrenamientos y actividades físicas. Fabricada con tejido transpirable que mantiene la piel fresca y seca. Su diseño clásico y ajuste regular garantizan libertad de movimiento. Perfecta para el día a día o el gimnasio.", 25, "../static/images/camiseta.jpg",1),
      Producto(4, "Pantalón Deportivo", "Pantalones deportivos cómodos y ligeros, perfectos para entrenar o relajarse. Fabricados con tejido transpirable que absorbe la humedad, mantienen la frescura en cada movimiento. Su corte ajustado pero flexible garantiza libertad y confort. Ideales para el gimnasio o el uso diario.", 30, "../static/images/pantalon.jpg", 1),
      Producto(5, "Zapatillas Deportivas", "Zapatillas deportivas versátiles y cómodas, diseñadas para entrenamientos y uso diario. Cuentan con una suela antideslizante que ofrece tracción y estabilidad. Su plantilla acolchada garantiza amortiguación en cada paso. Perfectas para mantener el ritmo en cualquier actividad.", 50, "../static/images/zapatilla.jpg", 1)
    ]

    products_list = []
    for product in products:
      products_list.append({
        "id": product.id,
        "nombre": product.nombre,
        "descripcion": product.descripcion,
        "precio": product.precio,
        "fotoUrl": product.fotoUrl,
        "stock": product.stock
      })
    
    return products_list

@productos.route('/productos', methods=['GET'])
def get_products():
  try:
    get_products_query()
    return jsonify(products_list), 200
  except Exception as e:
    print(f"Error al obtener los productos: {e}")
    return jsonify({"error": "Error al obtener los productos"}), 500


@productos.route('/productos/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()

        products_list = get_products_query()
        producto = next((p for p in products_list if p["id"] == id), None)

        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404

        if 'nombre' in data:
            producto["nombre"] = data['nombre']
        if 'descripcion' in data:
            producto["descripcion"] = data['descripcion']
        if 'precio' in data:
            producto["precio"] = data['precio']
        if 'stock' in data:
            producto["stock"] = data['stock']

        print("Datos del producto actualizados:")
        print(f'{producto["nombre"]}, {producto["descripcion"]}, {producto["precio"]}, {producto["stock"]}')
        return jsonify({"message": "Producto actualizado correctamente"}), 200

    except Exception as e:
        print(f"Error al actualizar el producto: {e}")
        return jsonify({"error": "Error al actualizar el producto"}), 500


@productos.route('/productos/<int:id>', methods=['PATCH'])
def update_product_detail(id):
    data = request.get_json()
    producto = Producto.query.get_or_404(id)

    if 'nombre' in data:
        producto.nombre = data['nombre']
    if 'descripcion' in data:
        producto.descripcion = data['descripcion']
    if 'precio' in data:
        producto.precio = data['precio']
    if 'stock' in data:
        producto.stock = data['stock']

    db.session.commit()

    return jsonify({"message": "Producto actualizado parcialmente"}), 200
