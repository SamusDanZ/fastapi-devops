from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from data.database import database
from data.videojuego_repository import VideojuegosRepository
from data.user_repository import UserRepository
from data.valoracion_repository import ValoracionesRepository
from domain.model.Alumno import Videojuegos
from domain.user import User
from starlette.middleware.sessions import SessionMiddleware

import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(title="Mi Primera Web FastAPI", description="Ejemplo básico con Jinja2")

# Configurar middleware de sesiones (IMPORTANTE: cambiar secret_key en producción)
app.add_middleware(SessionMiddleware, secret_key="tu-clave-secreta-aqui-cambiar-en-produccion")

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    """Devuelve la conexión a BD o lanza 503 si no hay conexión."""
    if database is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    return database


# Función para obtener el usuario actual desde la sesión
def get_current_user(request: Request) -> User | None:
    username = request.session.get("username")
    if not username:
        return None
    db = get_db()
    user_repo = UserRepository()
    return user_repo.get_by_username(db, username)

#RUTA RAIZ
@app.get("/")
async def inicio(request: Request, current_user: User | None = Depends(get_current_user)):
    """Página de inicio"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": current_user
    })

# RUTA INSERTAR
@app.post("/do_insertar_videojuego")
async def do_insertar_videojuego(request: Request,
                                 nombre : Annotated[str, Form()]=None,
                                 current_user: User | None = Depends(get_current_user)):
    """Página de navegación con enlaces"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    videojuego = Videojuegos(0, nombre)
    
    if not videojuegos_repo.insertar_videojuego(db, videojuego):
        return templates.TemplateResponse("insert_videojuegos.html", {
            "request": request,
            "user": current_user,
            "error": "Ya existe un videojuego con ese nombre"
        })

    return templates.TemplateResponse("do_insert_videojuegos.html", {"request": request, "user": current_user})


# RUTA INSERTAR
@app.get("/insert_videojuegos")
async def insert_videojuegos(request: Request, current_user: User | None = Depends(get_current_user)):
    """Página de navegación con enlaces"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})

    return templates.TemplateResponse("insert_videojuegos.html", {"request": request, "user": current_user})


# RUTA Borrar
@app.get("/borrar_videojuegos")
async def borrar_videojuegos(request: Request, current_user: User | None = Depends(get_current_user)):
    """Página de navegación con enlaces"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    videojuegos = videojuegos_repo.get_all(db)

    return templates.TemplateResponse("borrar_videojuegos.html", {"request": request,
                                                              "videojuegos": videojuegos,
                                                              "user": current_user})



# RUTA BORRAR
@app.post("/do_borrar_videojuego")
async def do_borrar_videojuego(request: Request,
                               id : Annotated[str, Form()],
                               current_user: User | None = Depends(get_current_user)):
    """Página de navegación con enlaces"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    videojuegos_repo.borrar_videojuego(db, int(id))

    return templates.TemplateResponse("do_borrar_videojuegos.html", {"request": request, "user": current_user})



# RUTAS GET
@app.get("/videojuegos", response_class=HTMLResponse)
async def videojuegos(request: Request, current_user: User | None = Depends(get_current_user)):
    """Página de navegación con enlaces"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    valoraciones_repo = ValoracionesRepository()
    videojuegos = videojuegos_repo.get_all(db)
    puntuaciones = valoraciones_repo.get_by_user(db, current_user.id)
    promedios = valoraciones_repo.get_promedios_por_videojuego(db)

    return templates.TemplateResponse("videojuegos.html", {
        "request": request,
        "videojuegos": videojuegos,
        "puntuaciones": puntuaciones,
        "promedios": promedios,
        "user": current_user,
    })


@app.get("/mis_puntuaciones", response_class=HTMLResponse)
async def mis_puntuaciones(request: Request, current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    db = get_db()
    valoraciones_repo = ValoracionesRepository()
    mis_valoraciones = valoraciones_repo.get_by_user_with_details(db, current_user.id)

    return templates.TemplateResponse("mis_puntuaciones.html", {
        "request": request,
        "valoraciones": mis_valoraciones,
        "user": current_user,
    })


@app.get("/puntuaciones", response_class=HTMLResponse)
async def ver_puntuaciones(request: Request, current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    db = get_db()
    valoraciones_repo = ValoracionesRepository()
    valoraciones = valoraciones_repo.get_all_with_details(db)

    return templates.TemplateResponse("puntuaciones.html", {
        "request": request,
        "valoraciones": valoraciones,
        "user": current_user,
    })


@app.get("/videojuego/{videojuego_id}", response_class=HTMLResponse)
async def ver_videojuego(request: Request, videojuego_id: int, current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    videojuego = videojuegos_repo.get_by_id(db, videojuego_id)

    if not videojuego:
        return RedirectResponse(url="/videojuegos", status_code=303)

    valoraciones_repo = ValoracionesRepository()
    valoraciones = valoraciones_repo.get_by_videojuego(db, videojuego_id)
    promedio = valoraciones_repo.get_promedio_videojuego(db, videojuego_id)
    mi_puntuacion_dict = valoraciones_repo.get_by_user(db, current_user.id)
    mi_valoracion = mi_puntuacion_dict.get(videojuego_id)

    return templates.TemplateResponse("videojuego_detalle.html", {
        "request": request,
        "videojuego": videojuego,
        "valoraciones": valoraciones,
        "promedio": promedio,
        "mi_valoracion": mi_valoracion,
        "user": current_user,
    })


@app.post("/puntuar_videojuego")
async def puntuar_videojuego(
    request: Request,
    videojuego_id: Annotated[int, Form()],
    puntuacion: Annotated[int, Form()],
    comentario: Annotated[str, Form()] = "",
    current_user: User | None = Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    if puntuacion < 1 or puntuacion > 10:
        return RedirectResponse(url="/videojuegos?error=puntuacion", status_code=303)

    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    if not videojuegos_repo.get_by_id(db, int(videojuego_id)):
        return RedirectResponse(url="/videojuegos", status_code=303)

    valoraciones_repo = ValoracionesRepository()
    valoraciones_repo.upsert_puntuacion(db, current_user.id, int(videojuego_id), int(puntuacion), comentario)

    return RedirectResponse(url="/videojuegos", status_code=303)


# RUTA EDITAR (muestra formulario)
@app.get("/editar_videojuego", response_class=HTMLResponse)
async def editar_videojuego(request: Request, id: Optional[int] = None, current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    if id is None:
        # Si falta id, redirigir a la lista
        return RedirectResponse(url="/videojuegos", status_code=303)

    videojuego = videojuegos_repo.get_by_id(db, int(id))
    if not videojuego:
        return RedirectResponse(url="/videojuegos", status_code=303)

    return templates.TemplateResponse("editar_videojuego.html", {"request": request, "videojuego": videojuego, "user": current_user})


# RUTA ACTUALIZAR (procesa POST)
@app.post("/do_actualizar_videojuego")
async def do_actualizar_videojuego(request: Request,
                                   id: Annotated[int, Form()],
                                   nombre: Annotated[str, Form()]=None,
                                   current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    if not current_user.is_admin:
        return templates.TemplateResponse("error_admin.html", {"request": request, "user": current_user})
    
    db = get_db()
    videojuegos_repo = VideojuegosRepository()
    videojuego = Videojuegos(int(id), nombre)
    videojuegos_repo.actualizar_videojuego(db, videojuego)

    return templates.TemplateResponse("do_actualizar_videojuegos.html", {"request": request, "user": current_user})


# RUTA REGISTRO (Mostrar formulario)
@app.get("/registro")
async def registro(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("registro.html", {"request": request})

# RUTA REGISTRO (Procesar formulario)
@app.post("/do_registro")
async def do_registro(request: Request, 
                     username: Annotated[str, Form()],
                     password: Annotated[str, Form()]):
    """Procesar registro"""
    user_repo = UserRepository()
    
    # Verificar si el usuario ya existe
    db = get_db()
    existing_user = user_repo.get_by_username(db, username)
    if existing_user:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "El usuario ya existe"
        })
    
    # Crear nuevo usuario
    new_user = User(0, username, None, False)
    new_user.set_password(password)
    user_repo.insertar_usuario(db, new_user)
    
    return RedirectResponse(url="/login", status_code=303)

# RUTA LOGIN (Mostrar formulario)
@app.get("/login")
async def login(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

# RUTA LOGIN (Procesar formulario)
@app.post("/do_login")
async def do_login(request: Request,
                  username: Annotated[str, Form()],
                  password: Annotated[str, Form()]):
    """Procesar login"""
    db = get_db()
    user_repo = UserRepository()
    user = user_repo.get_by_username(db, username)
    
    if not user or not user.check_password(password):
        return RedirectResponse(url="/login?error=1", status_code=303)
    
    # Guardar username en la sesión
    request.session["username"] = username
    
    return RedirectResponse(url="/", status_code=303)

# RUTA LOGOUT
@app.get("/logout")
async def logout(request: Request):
    """Cerrar sesión"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# RUTA ADMIN (Gestión de usuarios)
@app.get("/admin")
async def admin(request: Request, current_user: User | None = Depends(get_current_user)):
    """Panel de administración"""
    if not current_user or not current_user.is_admin:
        return RedirectResponse(url="/", status_code=303)
    
    db = get_db()
    user_repo = UserRepository()
    usuarios = user_repo.get_all(db)
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": current_user,
        "usuarios": usuarios
    })

# RUTA ADMIN - Cambiar rol de usuario (hacer admin/quitar admin)
@app.post("/admin/toggle_admin")
async def toggle_admin(request: Request,
                      user_id: Annotated[int, Form()],
                      current_user: User | None = Depends(get_current_user)):
    """Cambiar rol de administrador de un usuario"""
    if not current_user or not current_user.is_admin:
        return RedirectResponse(url="/", status_code=303)

    # Funcionalidad deshabilitada: no se permite cambiar roles desde la web
    return RedirectResponse(url="/admin?error=toggle_desactivado", status_code=303)

# RUTA ADMIN - Borrar usuario
@app.post("/admin/borrar_usuario")
async def admin_borrar_usuario(request: Request,
                               id: Annotated[int, Form()],
                               current_user: User | None = Depends(get_current_user)):
    """Borrar un usuario"""
    if not current_user or not current_user.is_admin:
        return RedirectResponse(url="/", status_code=303)
    
    db = get_db()
    user_repo = UserRepository()
    usuario = user_repo.get_by_id(db, int(id))

    # No permitir borrar administradores ni tu propia cuenta
    if not usuario:
        return RedirectResponse(url="/admin", status_code=303)
    if usuario.is_admin:
        return RedirectResponse(url="/admin?error=borrar_admin_no_permitido", status_code=303)
    if usuario.id == current_user.id:
        return RedirectResponse(url="/admin?error=self_delete", status_code=303)

    user_repo.borrar_usuario(db, int(id))
    
    return RedirectResponse(url="/admin", status_code=303)


if __name__ == "__main__":
    # Usar el import string evita el warning de reload/workers
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
