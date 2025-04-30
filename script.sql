-- SCRIPT PARA CREAR LA BASE DE DATOS

DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  contrasenya VARCHAR(255) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserts usuarios

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Juan Pérez', 'juan.perez@example.com', 'password123');

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Ana López', 'ana.lopez@example.com', 'securepassword');
