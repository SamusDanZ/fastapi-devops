"""
Script para crear la tabla de usuarios y el admin inicial
Ejecuta este script una vez para inicializar la base de datos
"""
from data.database import get_database_connection
import bcrypt
import sys

# Conectar a la base de datos
database = get_database_connection()

if database is None:
    print("\n❌ No se pudo establecer conexión con la base de datos")
    print("Por favor verifica la configuración en data/database.py")
    sys.exit(1)

cursor = database.cursor()

# Crear tabla de usuarios (legacy)
print("Creando tabla de usuarios (legacy)...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✓ Tabla usuarios creada")

# Crear tabla de videojuegos (legacy)
print("Creando tabla de videojuegos (legacy)...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS videojuegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
)
""")
print("✓ Tabla videojuegos creada")

# Crear tablas v2
print("Creando tabla de usuarios_v2...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✓ Tabla usuarios_v2 creada")

print("Creando tabla de videojuegos_v2...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS videojuegos_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
)
""")
print("✓ Tabla videojuegos_v2 creada")

print("Creando tabla usuarios_videojuegos...")
cursor.execute("""
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
)
""")
print("✓ Tabla usuarios_videojuegos creada")

# Copiar datos legacy a v2
print("\nCopiando datos legacy a v2 (si existen)...")
try:
    cursor.execute(
        """
        INSERT IGNORE INTO usuarios_v2 (id, username, password_hash, is_admin, created_at)
        SELECT id, username, password_hash, is_admin, created_at FROM usuarios
        """
    )
    database.commit()
    print("✓ Usuarios copiados a usuarios_v2")
except Exception as e:
    print(f"⚠️  No se pudieron copiar usuarios legacy: {e}")
    database.rollback()

try:
    cursor.execute(
        """
        INSERT IGNORE INTO videojuegos_v2 (id, nombre)
        SELECT id, nombre FROM videojuegos
        """
    )
    database.commit()
    print("✓ Videojuegos copiados a videojuegos_v2")
except Exception as e:
    print(f"⚠️  No se pudieron copiar videojuegos legacy: {e}")
    database.rollback()

# Crear usuario admin en v2
print("\nCreando usuario administrador en usuarios_v2...")
admin_password = "admin123"
password_bytes = admin_password.encode('utf-8')
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

try:
    cursor.execute("""
    INSERT INTO usuarios_v2 (username, password_hash, is_admin) 
    VALUES (%s, %s, %s)
    """, ('admin', password_hash, True))
    database.commit()
    print("✓ Usuario admin creado")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("  ⚠️  IMPORTANTE: Cambia esta contraseña después del primer login")
except Exception as e:
    if "Duplicate entry" in str(e):
        print("⚠️  El usuario admin ya existe")
    else:
        print(f"❌ Error al crear usuario: {e}")
        database.rollback()

# Cerrar conexión
cursor.close()
database.close()
print("\n✓ Base de datos inicializada correctamente")
