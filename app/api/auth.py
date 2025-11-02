from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Auth"])

templates = Jinja2Templates(directory="app/plantillas")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_post(
    usuario: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user =db.query(User).filter(User.cedula == usuario).first()
    if not user:
        return HTMLResponse(
            "<div style='color:red; text-align:center;'> Usuario no encontrado</div>"
        )
    
    if not verify_password(password, user.password_hash):
        return HTMLResponse(
            "<div style='color:red; text.align: center;'> Contraseña incorrecta</div>",
            status_code=401
        )
    
    if user.role == "admin":
        return RedirectResponse(url="/admin", status_code=303)
    elif user.role == "vendedor":
        return RedirectResponse(url="/vendedor", status_code=303)
    else:
        return HTMLResponse(
            "<div style='color:red; text-align: center;'> Rol no autorizado</div>", 
            status_code=403
        )