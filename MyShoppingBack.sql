-- Eliminar las tablas si existen
DROP TABLE IF EXISTS orden_producto;
DROP TABLE IF EXISTS factura;
DROP TABLE IF EXISTS orden_compra;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

-- Crear la tabla de productos con precio
CREATE TABLE productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla de clientes
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cedula VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL
);

-- Crear la tabla de orden de compra sin la fecha
CREATE TABLE orden_compra (
    orden_id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

-- Crear la tabla de conexión para productos en una orden de compra
CREATE TABLE orden_producto (
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    PRIMARY KEY (orden_id, producto_id),
    FOREIGN KEY (orden_id) REFERENCES orden_compra(orden_id),
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id)
);

-- Crear la tabla factura con precio total
CREATE TABLE factura (
    factura_id SERIAL PRIMARY KEY,
    orden_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    precio_total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (orden_id) REFERENCES orden_compra(orden_id)
);

-- Insertar algunos datos de ejemplo con datos de Pokémon
INSERT INTO productos (nombre, descripcion, cantidad, precio)
VALUES 
('Bulbasaur', 'Bulbasaur es un Pokémon tipo Planta/Veneno.', 100, 10.00),
('Charmander', 'Charmander es un Pokémon tipo Fuego.', 100, 12.00),
('Squirtle', 'Squirtle es un Pokémon tipo Agua.', 100, 8.00),
('Pikachu', 'Pikachu es un Pokémon tipo Eléctrico.', 100, 15.00),
('Jigglypuff', 'Jigglypuff es un Pokémon tipo Normal/Hada.', 100, 9.00);
