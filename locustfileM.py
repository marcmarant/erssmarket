from locust import HttpUser, task, between, events
import random
import string
import json
import time
import mysql.connector
from datetime import datetime

# Datos de conexión
db_config = {
    "host": "localhost",
    "user": "locust_user",
    "password": "martinezmejiadujo",
    "database": "locust_metrics"
}

# Conexión global a la BD (mejor usar conexión por hilo en producción)
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Función auxiliar para generar correos únicos en cada prueba
def generar_email():
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"usuario_{sufijo}@test.com"

# Función auxiliar para generar correos únicos en cada prueba
def generar_password():
    return "test1234"

# Función auxiliar para hacer login y obtener el token JWT
def login(user):
    response = user.client.post("/api/login", json={
        "email": user.email,
        "password": user.password
    })

    if response.status_code == 200:
        token = response.json().get("access_token")
        user.headers = {
            "Authorization": f"Bearer {token}"
        }
        user.autenticado = True
    else:
        user.headers = {} # En caso de error, no se inserta el token
        user.autenticado = False 

"""
Clase que representa a los usuarios clientes de la tienda 
"""
class UsuarioWeb(HttpUser):
    host = "http://localhost:5000" # Host con la ruta a nuestra web
    wait_time = between(1, 3) # Tiempo de espera entre tareas simulando el comportamiento de usuarios reales

    """
    Esta función se ejecuta automáticamente al inicio de cada usuario simulado.
    Registra un nuevo usuario y realiza login para obtener el token JWT necesario
    para todas las demás peticiones.
    """
    def on_start(self):
        self.email = generar_email()
        self.password = generar_password()
        self.nombre = "Usuario Locust"

        # Registrar nuevo usuario
        self.client.post("/api/register", json={
            "email": self.email,
            "password": self.password,
            "name": self.nombre
        }, name="registro_usuario")
        login(self)

    """
    Cierra la sesión
    """
    @task(1)
    def cerrar_sesion(self):
        if self.autenticado:
            with self.client.post("/api/logout", headers=self.headers, catch_response=True, name="cerrar_sesion") as response:
                if response.status_code == 200:
                    self.headers = {}
                    self.autenticado = False
                    response.success()
                else:
                    response.failure("Fallo en logout")

    """
    Inicia la de sesión
    """
    @task(1)
    def iniciar_sesion(self):
        if not self.autenticado:
            login(self)

    """
    Consulta general al menú principal
    """
    @task(3)
    def ver_menu_principal(self):
        self.client.get("/api/menu/", name="ver_menu_principal")

    """
    Consulta para obtener todos los productos disponibles
    """
    @task(6)
    def listar_productos(self):
        response = self.client.get("/api/productos/", headers=self.headers, name="listar_productos")
        if response.status_code == 200:
            productos = response.json()
            if productos:
                producto = random.choice(productos)
                self.random_producto = producto.get("id")

    """
    Consulta para ver el detalle de un producto individual
    """
    @task(5)
    def ver_producto_detallado(self):
        if hasattr(self, 'random_producto'):
            self.client.get(f"/api/productos/{self.random_producto}", headers=self.headers, name="ver_producto_detallado")

    """
    Agrega un producto aleatorio al carrito
    """
    @task(4)
    def agregar_al_carrito(self):
        if self.autenticado and hasattr(self, 'random_producto'):
            self.client.post("/api/carrito/agregar", headers=self.headers, name="agregar_al_carrito", json={
                "producto_id": self.random_producto,
                "cantidad": random.randint(1, 3)
            })
            # Guardar el último producto agregado al carrito
            self.random_producto_en_carrito = self.random_producto

    """
    Consulta el contenido actual del carrito
    """
    @task(2)
    def ver_carrito(self):
        if self.autenticado:
            self.client.get("/api/carrito/", headers=self.headers, name="ver_carrito")

    """
    Retira un producto aleatorio del carrito
    """
    @task(2)
    def retirar_del_carrito(self):
        if self.autenticado and hasattr(self, 'random_producto_en_carrito'):
            with self.client.delete(f"/api/carrito/{self.random_producto_en_carrito}", headers=self.headers, catch_response=True, name="retirar_del_carrito") as response:
                if response.status_code != 200:
                    response_data = response.json()
                    response.failure(f"{response.status_code} - Fallo al retirar del carrito: {response_data.get('error')}")

    """
    Vacia el carrito
    """
    @task(1)
    def vaciar_carrito(self):
        if self.autenticado:
            self.client.delete("/api/carrito/vaciar", headers=self.headers, name="vaciar_carrito")

    """
    Simula la compra de los productos en el carrito.
    El backend introduce un retardo para simular interacción con la pasarela de pago.
    """
    @task(2)
    def realizar_checkout(self):
        if self.autenticado:
            with self.client.post("/api/checkout", headers=self.headers, catch_response=True, name="realizar_checkout") as response:
                if response.status_code == 200:
                    time.sleep(random.uniform(2.5, 4.5))  # Simula espera de pasarela de pago
                    response.success()
                else:
                    response_data = response.json()
                    response.failure(f"{response.status_code} - Fallo al realizar la compra: {response_data.get('error')}")

    """
    Consulta los pedidos anteriores del usuario
    """
    @task(2)
    def ver_pedidos(self):
        if self.autenticado:
            with self.client.get("/api/pedidos/", headers=self.headers, name="ver_pedidos") as response:
                if response.status_code == 200:
                    pedidos = response.json()
                    if pedidos:
                        pedido = random.choice(pedidos)
                        self.random_pedido = pedido.get("id")

    """
    Consulta para ver el detalle de un pedido individual
    """
    @task(2)
    def ver_pedido_detallado(self):
        if self.autenticado and hasattr(self, 'random_pedido'):
            self.client.get(f"/api/pedidos/{self.random_pedido}", headers=self.headers, name="ver_pedido_detallado")

"""
Clase que representa a un usuario administrador de la tienda
"""
class UsuarioAdmin(HttpUser):
    host = "http://localhost:5000" # Host con la ruta a nuestra web
    wait_time = between(60, 120)  # Espera más larga para ejecutar tareas de administrador (edicion de productos)
    producto_ids = [] # Array con los ids de los productos, para que el usuario los pueda editar
    posibles_nombres = [
        'Guantes de fútbol', 'Camiseta', 'Balón de fútbol', 'Pantalon', 'Zapatillas', 
        'Espinilleras', 'Raqueta', 'Medias', 'Balón de baloncesto', 'Pelota de tenis',
        'Gorra', 'Sudadera', 'Chaqueta', 'Mochila', 'Toalla deportiva',
    ]

    """
    Esta función se ejecuta automáticamente al inicio de cada usuario simulado.
    Registra un nuevo usuario y realiza login para obtener el token JWT necesario
    para todas las demás peticiones.
    """
    def on_start(self):
        self.email = generar_email()
        self.password = generar_password()
        self.nombre = "Usuario Administrador Locust"

        self.client.post("/api/register", json={
            "email": self.email,
            "password": self.password,
            "name": self.nombre,
            "is_admin": True
        }, name="registro_admin")
        login(self)

        with self.client.get("/api/productos/", headers=self.headers, catch_response=True, name="listar_productos_admin") as response:
            if response.status_code == 200:
                productos = response.json()
                self.producto_ids = [p['id'] for p in productos]
            else:
                self.producto_ids = []

    """
    Simula el aumento de stock de un producto
    """
    @task(1)
    def cambiar_stock(self):
        if not self.producto_ids:
            return
        producto_id = random.choice(self.producto_ids)
        nuevo_stock = random.randint(0, 200)
        self.client.patch(f"/api/productos/{producto_id}", headers=self.headers, catch_response=True,name="cambiar_stock", json={
            "stock": nuevo_stock
        })

    """
    Simula el cambio en el precio de un producto (pudiendo equitativamente disminuir hasta la mitad o aumentar hasta el doble)
    """
    @task(1)
    def cambiar_precio(self):
        if not self.producto_ids:
            return
        if random.random() < 0.5:
            factor = random.uniform(0.5, 1.0)
        else:
            factor = random.uniform(1.0, 2.0)
        producto_id = random.choice(self.producto_ids)
        with self.client.get(f"/api/productos/{producto_id}", headers=self.headers, catch_response=True,name="ver_producto_precio") as response:
            if response.status_code == 200:
                producto = response.json()
                nuevo_precio = round(producto['precio'] * factor, 2)
                self.client.patch(f"/api/productos/{producto_id}", headers=self.headers, catch_response=True, name="cambiar_precio",json={
                    "precio": nuevo_precio
                })

    """
    Simula la realización de varios cambios en un producto
    """
    @task(1)
    def cambiar_producto(self):
        if not self.producto_ids:
            return
        producto_id = random.choice(self.producto_ids)
        nuevo_nombre = random.choice(self.posibles_nombres)
        nueva_descripcion = "Descripción actualizada del producto " + nuevo_nombre
        self.client.put(f"/api/productos/{producto_id}", headers=self.headers, catch_response=True, name="editar_producto", json={
            "nombre": nuevo_nombre,
            "descripcion": nueva_descripcion,
        })


@events.request.add_listener
def registrar_metricas(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    endpoint = name or url
    method = request_type  # normalmente "GET", "POST", etc.
    response_length_val = response_length or 0
    status_code = response.status_code if response else 0
    is_error = 1 if exception or (status_code >= 400) else 0
    user_count = 0
    user_type = "Desconocido"
    task_name = name or None

    # Obtener número de usuarios concurrentes y tipo de usuario si están disponibles
    if context and context.environment and context.environment.runner:
        user_count = sum(context.environment.runner.user_classes_count.values())
    else:
        user_count = 0

    try:
        db_cursor.execute("""
            INSERT INTO locust_requests 
                (timestamp, endpoint, method, response_time_ms, response_length, status_code, is_error, user_count, user_type, task_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (timestamp, endpoint, method, int(response_time), response_length_val, status_code, is_error, user_count, user_type, task_name))
        db_connection.commit()
    except Exception as e:
        print(f"[ERROR BD] No se pudo guardar métrica: {e}")

