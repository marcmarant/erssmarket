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
  descripcion TEXT,  
  precio INT NOT NULL,
  fotoUrl VARCHAR(255),
  stock INT NOT NULL
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
