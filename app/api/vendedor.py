from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.db.session import get_db
from app.models.user import User
from app.esquemas.cliente import ClienteCreate
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/vendedor", tags=["Vendedor"])

templates = Jinja2Templates(directory="app/plantillas")

@router.get("/", response_class=HTMLResponse)
def vendedor_dashboard(request: Request):
    return templates.TemplateResponse("vendedor/vendedor.html", {"request": request})


@router.post("/registrar-cliente")
def registrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):

    nuevo_cliente = User(
        nombre=cliente.nombre,
        cedula=cliente.cedula,
        celular=cliente.celular,
        correo=cliente.correo,
        role="cliente",
        is_active=True
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return {
        "msg": "Cliente registrado correctamente",
        "id": nuevo_cliente.id,
        "nombre": nuevo_cliente.nombre,
        "cedula": nuevo_cliente.cedula,
        "correo": nuevo_cliente.correo
    }
