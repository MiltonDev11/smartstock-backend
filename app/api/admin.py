"""Módulo `app.api.admin`.

Define las rutas del panel de administración para mostrar plantillas
HTML y endpoints de gestión de materiales y usuarios.
"""
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.material import Material
from app.esquemas.material import MaterialCreate, MaterialOut
from fastapi.responses import JSONResponse

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

@router.post("/registrar-material", response_model=MaterialOut)
def registrar_material(material: MaterialCreate, db: Session = Depends(get_db)):
    nuevo = Material(
        material=material.material,
        medida=material.medida,
        unidad=material.unidad,
        precio_unitario=material.precio_unitario,
        marca=material.marca,
        cantidad=material.cantidad
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return MaterialOut(
        id=nuevo.id,
        material=nuevo.material,
        medida=nuevo.medida,
        unidad=nuevo.unidad,
        precio_unitario=nuevo.precio_unitario,
        marca=nuevo.marca,
        cantidad=nuevo.cantidad,
        ingreso=nuevo.calcular_ingreso()
    )

@router.get("/api/materiales", response_model=list[MaterialOut])
def obtener_materiales(db: Session = Depends(get_db)):
    materiales = db.query(Material).all()
    return [
        MaterialOut(
            id=m.id,
            material=m.material,
            medida=m.medida,
            unidad=m.unidad,
            precio_unitario=m.precio_unitario,
            marca=m.marca,
            cantidad=m.cantidad,
            ingreso=m.calcular_ingreso()
        )
        for m in materiales
    ]

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
        .order_by(User.id.asc())
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
