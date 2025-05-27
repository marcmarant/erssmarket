from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Tabla usuario en la base de datos
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasenya = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

    # Todo: Borrar a futuro
    def __init__(self, id, nombre, email, contrasenya, fecha_creacion, is_admin=False):
        self.id = id
        self.nombre = nombre
        self.contrasenya = contrasenya
        self.email = email
        self.fecha_creacion = fecha_creacion
        self.is_admin = is_admin

# Tabla producto en la base de datos
class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)  
    precio = db.Column(db.Integer, nullable=False)
    fotoUrl = db.Column(db.String(255))
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, descripcion, precio, fotoUrl, stock):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.fotoUrl = fotoUrl
        self.stock = stock

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'fotoUrl': self.fotoUrl,
            'stock': self.stock
        }

# Tabla carrito en la base de datos
class Carrito(db.Model):
    __tablename__ = 'carrito'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

    def __init__(self, usuario_id, producto_id, cantidad):
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad
        }

# Tabla pedido en la base de datos
class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    precio_total = db.Column(db.Integer, nullable=False)

    def __init__(self, usuario_id, precio_total):
        self.usuario_id = usuario_id
        self.precio_total = precio_total

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion,
            'precio_total': self.precio_total
        }


# Tabla producto_pedido en la base de datos
class Producto_pedido(db.Model):
    __tablename__ = 'producto_pedido'

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), primary_key=True)
    precio = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __init__(self, pedido_id, producto_id, precio, cantidad):
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.precio = precio
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'precio': self.precio,
            'cantidad': self.cantidad
        }





