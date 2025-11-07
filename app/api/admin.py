from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin"])

templates = Jinja2Templates(directory="app/plantillas")

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@router.get("/gestion", response_class=HTMLResponse)
def vendedor_gestion(request: Request):
    return templates.TemplateResponse("admin/gestion.html", {"request": request})

@router.get("/materiales", response_class=HTMLResponse)
def admin_materiales(request: Request):
    return templates.TemplateResponse("admin/materiales.html", {"request": request})

@router.get("/reportes", response_class=HTMLResponse)
def admin_reportes(request: Request):
    return templates.TemplateResponse("admin/reportes.html", {"request": request})

@router.get("/solicitudes", response_class=HTMLResponse)
def admin_solicitudes(request: Request):
    return templates.TemplateResponse("admin/solicitudes.html", {"request": request})

@router.get("/stock", response_class=HTMLResponse)
def admin_stock(request: Request):
    return templates.TemplateResponse("admin/stock.html", {"request": request})

@router.get("/supervisar", response_class=HTMLResponse)
def admin_supervisar(request: Request):
    return templates.TemplateResponse("admin/supervisar.html", {"request": request})

@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = (
        db.query(User)
        .filter(User.role.in_(["vendedor", "cliente"]))
        .all()
    )
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": f"IDU{u.id}",
            "nombre": u.nombre,
            "cedula": u.cedula,
            "celular": u.celular,
            "correo": u.correo,
            "role": u.role.capitalize(),
            "estado": "Vinculado" if u.is_active else "Desvinculado"
        })
    return resultado
