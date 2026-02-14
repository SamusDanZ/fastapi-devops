-- Script para crear la tabla de usuarios
-- Ejecutar este script en la base de datos danielmm

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear un usuario administrador por defecto
-- Usuario: admin
-- Contraseña: admin123
-- NOTA: Cambiar esta contraseña después del primer login
INSERT INTO usuarios (username, password_hash, is_admin) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIqnVT.5D6', TRUE);

-- Para crear más usuarios manualmente, usa bcrypt para encriptar la contraseña
-- Ejemplo de usuarios normales (contraseña: user123):
-- INSERT INTO usuarios (username, password_hash, is_admin) 
-- VALUES ('usuario1', '$2b$12$hash_aqui', FALSE);
