# Sistema de Gestión de Videojuegos con Autenticación

Sistema web con registro de usuarios, login/logout y panel de administración.

## Características

### Usuarios Registrados
- ✅ Ver lista de videojuegos
- ✅ Acceso solo después de registrarse e iniciar sesión
- ✅ Puntuar videojuegos (1-10)

### Administradores
- ✅ Todas las funciones de usuarios registrados
- ✅ Añadir nuevos videojuegos
- ✅ Actualizar videojuegos existentes
- ✅ Borrar videojuegos
- ✅ Gestionar usuarios

### Seguridad
- ✅ Contraseñas encriptadas con bcrypt
- ✅ Sesiones con cookies HTTP-only
- ✅ Rutas protegidas según permisos

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Inicializar la base de datos

```bash
python inicializar_db.py
```

Este script creará:
- Tabla `usuarios` (legacy)
- Tabla `videojuegos` (legacy)
- Tabla `usuarios_v2`
- Tabla `videojuegos_v2`
- Tabla `usuarios_videojuegos` (relacion N-M con puntuaciones)
- Usuario administrador por defecto:
  - **Usuario:** admin
  - **Contraseña:** admin123
  - ⚠️ **Importante:** Cambiar esta contraseña después del primer login

### 3. Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en: http://127.0.0.1:8000

## Uso

### Para Usuarios Nuevos

1. Ir a http://127.0.0.1:8000
2. Click en "Registrarse"
3. Crear cuenta con usuario y contraseña
4. Iniciar sesión
5. Ver videojuegos disponibles

### Para Administradores

1. Iniciar sesión con credenciales de admin
2. Acceder al "Panel de Administración"
3. Gestionar usuarios y videojuegos

## Estructura del Proyecto

```
webregistro/
├── main.py                      # Aplicación principal FastAPI
├── requirements.txt             # Dependencias
├── inicializar_db.py           # Script de inicialización
├── crear_tabla_usuarios.sql    # SQL alternativo
├── data/
│   ├── database.py             # Conexión a MySQL
│   ├── videojuego_repository.py # Repositorio videojuegos
│   └── user_repository.py      # Repositorio usuarios
├── domain/
│   ├── user.py                 # Modelo User con bcrypt
│   └── model/
│       └── Alumno.py           # Modelo Videojuegos
├── templates/
│   ├── index.html              # Página principal
│   ├── registro.html           # Formulario registro
│   ├── login.html              # Formulario login
│   ├── admin.html              # Panel administración
│   ├── videojuegos.html        # Lista videojuegos
│   ├── insert_videojuegos.html
│   ├── editar_videojuego.html
│   └── borrar_videojuegos.html
└── static/
    └── style.css               # Estilos CSS
```

## Rutas de la Aplicación

### Públicas
- `GET /` - Página principal
- `GET /registro` - Formulario de registro
- `POST /do_registro` - Procesar registro
- `GET /login` - Formulario de login
- `POST /do_login` - Procesar login

### Usuarios Registrados
- `GET /videojuegos` - Ver videojuegos
- `POST /puntuar_videojuego` - Puntuar videojuego
- `GET /logout` - Cerrar sesión

### Solo Administradores
- `GET /admin` - Panel de administración
- `GET /insert_videojuegos` - Añadir videojuego
- `POST /do_insertar_videojuego` - Procesar nuevo videojuego
- `GET /editar_videojuego?id=X` - Editar videojuego
- `POST /do_actualizar_videojuego` - Actualizar videojuego
- `GET /borrar_videojuegos` - Lista para borrar
- `POST /do_borrar_videojuego` - Borrar videojuego

## Seguridad

### Encriptación de Contraseñas
Las contraseñas se encriptan usando **bcrypt** con salt automático antes de guardarse en la base de datos.

### Gestión de Sesiones
- Las sesiones se manejan con cookies HTTP-only
- No se almacenan contraseñas en cookies
- Solo se guarda el username del usuario autenticado

### Control de Acceso
- Las rutas verifican automáticamente si el usuario está autenticado
- Las funciones de administrador requieren `is_admin = TRUE`
- Redirección automática si no hay permisos

## Base de Datos

### Tabla: usuarios_v2

```sql
CREATE TABLE usuarios_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: videojuegos_v2

```sql
CREATE TABLE videojuegos_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

### Tabla: usuarios_videojuegos

```sql
CREATE TABLE usuarios_videojuegos (
    usuario_id INT NOT NULL,
    videojuego_id INT NOT NULL,
    puntuacion INT NOT NULL,
    PRIMARY KEY (usuario_id, videojuego_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios_v2(id),
    FOREIGN KEY (videojuego_id) REFERENCES videojuegos_v2(id)
);
```
```

## Notas Importantes

1. **Cambiar contraseña del admin:** El usuario admin creado por defecto tiene contraseña `admin123`. Cámbiala inmediatamente.

2. **Variables de entorno:** Para producción, considera mover las credenciales de base de datos a variables de entorno.

3. **HTTPS:** En producción, usa HTTPS para proteger las cookies de sesión.

4. **Backup:** Realiza backups regulares de la base de datos.

## Solución de Problemas

### Error de conexión a la base de datos
- Verifica que los datos de conexión en `data/database.py` sean correctos
- Asegúrate de que el servidor MySQL esté accesible

### No se pueden instalar las dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error con bcrypt
```bash
pip install --upgrade bcrypt
```

## Autor
Desarrollado como proyecto de Implantación de Aplicaciones Web
