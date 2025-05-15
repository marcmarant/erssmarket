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

    def __repr__(self):
        return f'<Producto {self.nombre}>'

    # Todo: Borrar a futuro
    def __init__(self, id, nombre, descripcion, precio, fotoUrl):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion  
        self.precio = precio
        self.fotoUrl = fotoUrl

# Tabla carrito en la base de datos
class Carrito(db.Model):
    __tablename__ = 'carrito'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Carrito Usuario: {self.usuario_id} Producto: {self.producto_id} Cantidad: {self.cantidad}>'

    # Todo: Borrar a futuro
    def __init__(self, id, usuario_id, producto_id, cantidad):
        self.id = id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad = cantidad




