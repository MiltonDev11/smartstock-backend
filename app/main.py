# Importa las clases y funciones necesarias de FastAPI y otros módulos
from fastapi import FastAPI, Request
from app.db.session import SessionLocal # Importa la función para crear una nueva sesión de base de datos local
from fastapi.staticfiles import StaticFiles # Para servir archivos estáticos (CSS, JS, imágenes)
from fastapi.templating import Jinja2Templates # Para usar plantillas Jinja2 para el renderizado de HTML
from fastapi.responses import RedirectResponse, HTMLResponse # Tipos de respuestas: redirección y HTML
# Importa los routers (grupos de rutas) de las diferentes partes de la API
from app.api import users, password_reset, auth
from app.api import admin  # type: ignore # Router para funcionalidades administrativas
from app.api import admin_users # Router para la gestión de usuarios por el administrador
from app.api.vendedor import router as vendedor_router # Router específico para el rol de vendedor
from app.api.solicitudes import router as vendedor_solicitudes, admin_router as admin_solicitudes_router# Routers para la gestión de solicitudes
from fastapi.middleware.cors import CORSMiddleware # Middleware para manejar Cross-Origin Resource Sharing (CORS)

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Configuración del Middleware CORS
# Esto permite que navegadores web de diferentes orígenes accedan a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs (puedes restringir luego)
    allow_credentials=True, # Permite cookies, encabezados de autenticación, etc.
    allow_methods=["*"],  # Permite POST, OPTIONS, GET...
    allow_headers=["*"],  # Permite Content-Type, Authorization...
)

# Monta la carpeta 'static' para servir archivos estáticos
# Los archivos en 'static/' serán accesibles a través de la URL '/static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura Jinja2Templates para el renderizado de plantillas HTML
# Las plantillas se buscarán en el directorio 'app/plantillas'
templates = Jinja2Templates(directory="app/plantillas")

# Incluye los routers de las diferentes secciones de la aplicación
# Esto asocia las rutas definidas en cada módulo con la aplicación principal
app.include_router(admin_users.router) # Rutas para administración de usuarios
app.include_router(admin.router) # Rutas generales de administración
app.include_router(users.router) # Rutas para usuarios (registro, perfil, etc.)
app.include_router(password_reset.router)# Rutas para el restablecimiento de contraseñas
app.include_router(auth.router) # Rutas de autenticación (login)
app.include_router(vendedor_router) # Rutas para el rol de vendedor
app.include_router(vendedor_solicitudes) # Rutas de solicitudes específicas del vendedor
app.include_router(admin_solicitudes_router) # Rutas de solicitudes específicas del administrador

# Función generadora para obtener una sesión de base de datos
# Se utiliza como una dependencia en las rutas que necesitan acceder a la DB
def get_db():
    """
    Proporciona una sesión de base de datos (SessionLocal) a las rutas.
    La sesión se cierra automáticamente después de que se completa la solicitud
    (gracias a 'finally').
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de inicio (raíz)
@app.get("/")
def root():
    """
    Redirige la solicitud desde la raíz ('/') a la página de login ('/login').
    """
    return RedirectResponse(url="/login")

# Ruta para la página principal del administrador
@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    """
    Muestra el dashboard de administraci    
    Requiere que el rol del usuario, almacenado en la cookie 'user_role', sea 'admin'.
    Si el rol no es 'admin', redirige al login.
    """
    role = request.cookies.get("user_role") # Obtiene el rol del usuario de las cookies
    if role != "admin":
        # Si no es administrador, redirige al login
        return RedirectResponse(url="/login")
    # Renderiza la plantilla del dashboard de administración
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

# Ruta para cerrar sesión
@app.get("/logout")
def logout():
    """
    Cierra la sesión del usuario eliminando la cookie 'user_role' y redirigiendo al login.
    """
    response = RedirectResponse(url="/login")
    # Elimina la cookie que almacena el rol del usuario (o el token de sesión)
    response.delete_cookie("user_role")
    return response

# Manejador de excepciones para el error 404 (No Encontrado)
@app.exception_handler(404)
async def not_found(request: Request, exc):
    """
    Maneja todas las respuestas 4   
    Renderiza la plantilla de error 404 personalizada ('errores/404.html').
    """
    return templates.TemplateResponse(
        "errores/404.html",
        {"request": request},
        status_code=404 # Asegura que el código de estado HTTP sea 404
        )