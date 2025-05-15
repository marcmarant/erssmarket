-- SCRIPT PARA CREAR LA BASE DE DATOS

DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS producto;

CREATE TABLE usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  contrasenya VARCHAR(255) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE producto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255),  
  precio INT NOT NULL,
  fotoUrl VARCHAR(255)
);


-- Inserts usuarios

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Juan Pérez', 'juan.perez@example.com', 'password123');

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Ana López', 'ana.lopez@example.com', 'securepassword');

INSERT INTO producto (nombre, precio) 
VALUES ('Producto 1', 450);

INSERT INTO producto (nombre, precio) 
VALUES ('Producto 2', 1200);
