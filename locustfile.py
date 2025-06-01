from locust import HttpUser, task, between
import random
import string
import json
import time

# Función auxiliar para generar correos únicos en cada prueba
def generar_email():
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"usuario_{sufijo}@test.com"

# Función auxiliar para generar correos únicos en cada prueba
def generar_password():
    return "test1234"

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
        })

        # Hacer login para obtener el token JWT
        response = self.client.post("/api/login", json={
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 200:
            token = response.json().get("access_token")
            self.headers = {
                "Authorization": f"Bearer {token}"
            }
        else:
            # En caso de error, no se podrá continuar
            self.headers = {}

    """
    Consulta general al menú principal
    """
    @task(1)
    def ver_menu_principal(self):
        self.client.get("/api/menu/")

    """
    Consulta para obtener todos los productos disponibles
    """
    @task(3)
    def listar_productos(self):
        response = self.client.get("/api/productos/", headers=self.headers)
        if response.status_code == 200:
            productos = response.json()
            if productos:
                producto = random.choice(productos)
                self.ultimo_producto = producto.get("id")

    """
    Consulta para ver el detalle de un producto individual
    """
    @task(2)
    def ver_producto_detallado(self):
        if hasattr(self, 'ultimo_producto'):
            self.client.get(f"/api/productos/{self.ultimo_producto}", headers=self.headers)

    """
    Agrega un producto aleatorio al carrito
    """
    #@task(2)
    @task(3)
    def agregar_al_carrito(self):
        if hasattr(self, 'ultimo_producto'):
            self.client.post("/api/carrito/agregar", headers=self.headers, json={
                "producto_id": self.ultimo_producto,
                "cantidad": random.randint(1, 3)
            })

    """
    Consulta el contenido actual del carrito
    """
    @task(1)
    def ver_carrito(self):
        self.client.get("/api/carrito/", headers=self.headers)

    """
    Simula la compra de los productos en el carrito.
    El backend introduce un retardo para simular interacción con la pasarela de pago.
    """
    @task(1)
    def realizar_checkout(self):
        with self.client.post("/api/checkout", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                time.sleep(random.uniform(2.5, 4.5))  # Simula espera de pasarela de pago
                response.success()
            else:
                response.failure(f"Fallo en checkout: {response.status_code}")

    """
    Consulta los pedidos anteriores del usuario
    """
    @task(1)
    def ver_pedidos(self):
        self.client.get("/api/pedidos/", headers=self.headers)

    """
    Consulta los pedidos anteriores del usuario
    """
    @task(1)
    def vaciar_carrito(self):
        self.client.delete("/api/carrito/vaciar", headers=self.headers)

"""
Clase que representa a un usuario administrador de la tienda
"""
class UsuarioAdmin(HttpUser):
    host = "http://localhost:5000" # Host con la ruta a nuestra web
    wait_time = between(1, 3) # Tiempo de espera entre tareas simulando el comportamiento de usuarios reales
    producto_ids = [] # Array con los ids de los productos, para que el usuario los pueda editar

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
        })

        response = self.client.post("/api/login", json={
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 200:
            token = response.json().get("access_token")
            self.headers = {
                "Authorization": f"Bearer {token}"
            }
        else: # En caso de error, no se podrá continuar
            self.headers = {}

        with self.client.get("/productos/", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                productos = response.json()
                self.producto_ids = [p['id'] for p in productos]
            else:
                self.producto_ids = []

    """
    Simula la edición de un campo en un producto.
    """
    @task(1)
    def cambiar_stock(self):
        if not self.producto_ids:
            return
        producto_id = random.choice(self.producto_ids)
        nuevo_stock = random.randint(0, 200)
        with self.client.patch("/productos/"+str(producto_id), headers=self.headers, catch_response=True, json={
            "stock": nuevo_stock
        })
