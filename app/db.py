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

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

    # Todo: Borrar a futuro
    def __init__(self, id, nombre, email, contrasenya, fecha_creacion):
        self.id = id
        self.nombre = nombre
        self.contrasenya = contrasenya
        self.email = email
        self.fecha_creacion = fecha_creacion
