-- Borrar la tabla existente
DROP TABLE IF EXISTS productos;

-- Crear la tabla de productos con precio
CREATE TABLE productos (
    producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    imagen_url TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Insertar algunos datos de ejemplo con datos de Pokémon y precios
INSERT INTO productos (nombre, descripcion, imagen_url, precio)
VALUES 
('Bulbasaur', 'Bulbasaur es un Pokémon tipo Planta/Veneno.', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png', 9.99),
('Charmander', 'Charmander es un Pokémon tipo Fuego.', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png', 12.99),
('Squirtle', 'Squirtle es un Pokémon tipo Agua.', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png', 11.99),
('Pikachu', 'Pikachu es un Pokémon tipo Eléctrico.', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png', 15.99),
('Jigglypuff', 'Jigglypuff es un Pokémon tipo Normal/Hada.', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png', 10.99);
