-- Script para crear las tablas v2 y la relacion N-M de puntuaciones
-- Ejecutar este script en la base de datos danielmm

CREATE TABLE IF NOT EXISTS usuarios_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS videojuegos_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios_videojuegos (
    usuario_id INT NOT NULL,
    videojuego_id INT NOT NULL,
    puntuacion INT NOT NULL,
    PRIMARY KEY (usuario_id, videojuego_id),
    CONSTRAINT fk_uv_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios_v2(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_uv_videojuego FOREIGN KEY (videojuego_id)
        REFERENCES videojuegos_v2(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Copiar datos desde tablas legacy si existen
INSERT IGNORE INTO usuarios_v2 (id, username, password_hash, is_admin, created_at)
SELECT id, username, password_hash, is_admin, created_at FROM usuarios;

INSERT IGNORE INTO videojuegos_v2 (id, nombre)
SELECT id, nombre FROM videojuegos;
