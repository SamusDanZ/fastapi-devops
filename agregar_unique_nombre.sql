-- Script para añadir restriccion UNIQUE al nombre de videojuegos
-- Esto evita duplicados a nivel de base de datos
-- IMPORTANTE: Ejecutar solo si no hay duplicados en la tabla

-- Para videojuegos_v2 (la tabla activa)
ALTER TABLE videojuegos_v2 ADD UNIQUE (nombre);

-- Opcional: para la tabla legacy si la usas
-- ALTER TABLE videojuegos ADD UNIQUE (nombre);
