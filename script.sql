-- SCRIPT PARA CREAR LA BASE DE DATOS

DROP TABLE IF EXISTS producto_pedido;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS carrito;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS usuario;

-- Tabla con la informacion de los usuarios
CREATE TABLE usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  contrasenya VARCHAR(255) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_admin BOOLEAN DEFAULT FALSE
);

-- Tabla con la informacion de los productos
CREATE TABLE producto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,  
  precio INT NOT NULL,
  fotoUrl VARCHAR(255),
  stock INT NOT NULL
);

-- Tabla con la información de un producto añadido al carrito de un usuario
CREATE TABLE carrito (
  usuario_id INT NOT NULL,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL,
  PRIMARY KEY (usuario_id, producto_id),
  FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE CASCADE 
);

-- Tabla con la información de un pedido realizado por un usuario
CREATE TABLE pedido (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  precio_total INT NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);

-- Tabla con la información de un producto incluido dentro de un pedido
CREATE TABLE producto_pedido (
  pedido_id INT NOT NULL,
  producto_id INT NOT NULL,
  precio INT NOT NULL, -- precio unitario en el momento del pedido
  cantidad INT NOT NULL,
  PRIMARY KEY (pedido_id, producto_id),
  FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE CASCADE 
);

-- Inserts usuarios

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Juan Pérez', 'juan.perez@example.com', 'password123');

INSERT INTO usuario (nombre, email, contrasenya) 
VALUES ('Ana López', 'ana.lopez@example.com', 'securepassword');

INSERT INTO producto (nombre, precio) 
VALUES ('Producto 1', 450,1);

INSERT INTO producto (nombre, descripcion, precio, fotoUrl, stock) 
VALUES 
('Balón de fútbol', 'Balón de fútbol clásico, perfecto para entrenamientos y partidos. Fabricado con materiales resistentes y cosido a máquina para mayor durabilidad. Su superficie de cuero sintético garantiza un toque suave y un control óptimo. Ideal para jugadores de todas las edades y niveles.', 25, '../static/images/balon.jpg', 1),
('Guantes de fútbol', 'Guantes de fútbol diseñados para ofrecer un agarre seguro y cómodo en todas las condiciones. Fabricados con materiales transpirables y resistentes, garantizan máxima protección y durabilidad. Su palma de látex antideslizante asegura un excelente control del balón. Ideales para entrenamientos y partidos.', 15, '../static/images/guantes.jpg', 1),
('Camiseta Deportiva', 'Camiseta deportiva ligera y cómoda, ideal para entrenamientos y actividades físicas. Fabricada con tejido transpirable que mantiene la piel fresca y seca. Su diseño clásico y ajuste regular garantizan libertad de movimiento. Perfecta para el día a día o el gimnasio.', 25, '../static/images/camiseta.jpg', 1),
('Pantalón Deportivo', 'Pantalones deportivos cómodos y ligeros, perfectos para entrenar o relajarse. Fabricados con tejido transpirable que absorbe la humedad, mantienen la frescura en cada movimiento. Su corte ajustado pero flexible garantiza libertad y confort. Ideales para el gimnasio o el uso diario.', 30, '../static/images/pantalon.jpg', 1),
('Zapatillas Deportivas', 'Zapatillas deportivas versátiles y cómodas, diseñadas para entrenamientos y uso diario. Cuentan con una suela antideslizante que ofrece tracción y estabilidad. Su plantilla acolchada garantiza amortiguación en cada paso. Perfectas para mantener el ritmo en cualquier actividad.', 50, '../static/images/zapatilla.jpg', 1);

INSERT INTO pedido (usuario_id, precio_total) 
VALUES 
(1, 45), -- Pedido 1 de Juan Pérez
(2, 95); -- Pedido 2 de Juan Pérez

INSERT INTO producto_pedido (pedido_id, producto_id, precio, cantidad) 
VALUES 
(1, 1, 25, 1),
(1, 2, 20, 1),
(2, 2, 15, 3),
(2, 3, 30, 2),
(2, 4, 50, 1);
