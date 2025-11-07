from fastapi import FastAPI, Request
from app.db.session import SessionLocal
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.api import users, password_reset, auth
from app.api import admin  # type: ignore
from app.api import admin_users

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/plantillas")

app.include_router(admin_users.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(password_reset.router)
app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    role = request.cookies.get("user_role")
    if role != "admin":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@ app.get("/vendedor", response_class=HTMLResponse)
def vendedor_page(request: Request):
    role = request.cookies.get("user_role")
    if role != "vendedor":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("vendedor/vendedor.html", {"request": request})

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("user_role")
    return response

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "errores/404.html",
        {"request": request},
        status_code=404
        )