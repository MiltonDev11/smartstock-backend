from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from fastapi_mail import FastMail, MessageSchema
from app.core.email_config import conf
from fastapi_mail import MessageType
from fastapi import HTTPException
from app.core.security import hash_password
from app.core.token_manager import generate_token, verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/password-reset", response_class=HTMLResponse)
async def password_reset_request(cedula: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.cedula == cedula).first()

    if not user:
        return HTMLResponse(
            """
            <div style='background-color: #f8d7da; color: #842029; padding: 10px; border-radius: 6px; text-align: center;'>
                Lo siento, no existe un usuario con esa cédula.
            </div>
            """,
            status_code=404
        )

    correo = str(user.correo)
    partes = correo.split("@")
    censurado = partes[0][:3] + "***@" + "***" + partes[1][-4:]

    user_id_raw = getattr(user, "id")
    try:
        user_id = int(user_id_raw)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno: id del usuario inválido")
    token = generate_token(user_id)
    user.last_reset_token = token
    db.commit()
    reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"

    # Crear el mensaje
    mensaje = MessageSchema(
        subject="Restablecer contraseña - SmartStock",
        recipients=[correo],
        body=f"""
        <h2>Hola {user.nombre},</h2>
        <p>Hemos recibimos una solicitud para restablecer tu contraseña.</p>
        <p>Haz clic en el siguiente enlace para crear tu nueva contraseña:</p>
        <a href="{reset_link}" > {reset_link}"></a>
        <p> Este enlace expirará en 15 minutos. </p>
        <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
        """,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(mensaje)

    return HTMLResponse(
        f"""
        <div style='background-color: #d1e7dd; color: #0f5132; padding: 10px; border-radius: 6px; text-align: center;'>
            Mensaje enviado. La validación fue enviada con éxito.<br>
            Revisa el correo: {censurado}
        </div>
        """,
        status_code=200
    )

@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_form(request: Request, token: str, db: Session = Depends(get_db)):
    # Verificar firma y expiración
    try:
        user_id = verify_token(token)
    except ValueError as e:
        return HTMLResponse(f"<h3 style='color:red; text-align:center;'>{str(e)}</h3>", status_code=400)

    # Buscar usuario y comprobar que token coincide con el guardado
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("<h3 style='color:red; text-align:center;'>Usuario no encontrado.</h3>", status_code=404)

    if not user.last_reset_token or user.last_reset_token != token:
        return HTMLResponse("<h3 style='color:red; text-align:center;'>Lo siento, este enlace ha expirado.</h3>", status_code=400)

    return f"""
    <html>
        <head>
            <title>Restablecer contraseña</title>
        </head>
        <body style="font-family: Arial; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 300px;">
                <h2 style="text-align: center;">Nueva Contraseña</h2>
                <form method="post" action="/reset-password?token={token}">
                    <input type="password" id="new_password" name="new_password" placeholder="Nueva contraseña" required
                        style="width: 100%; padding: 10px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc;">
                    <button type="submit" 
                        style="width: 100%; background-color: #4CAF50; color: white; padding: 10px; margin-top: 10px; border: none; border-radius: 5px;">
                        Actualizar
                    </button>
                </form>
            </div>
        </body>
    </html>
    """

@router.post("/reset-password", response_class=HTMLResponse)
def reset_password(token: str, new_password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user_id = verify_token(token)
    except ValueError as e:
        return HTMLResponse(f"<h3 style='color:red;'>{str(e)}</h3>", status_code=400)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que token coincida con el almacenado (único uso)
    if not user.last_reset_token or user.last_reset_token != token:
        return HTMLResponse("<h3 style='color:red;'>Lo siento, este token ya se usó o es inválido.</h3>", status_code=400)

    # Actualizar contraseña
    user.password_hash = hash_password(new_password)  # type: ignore
    # Invalidar token (marcar usado)
    user.last_reset_token = None
    db.commit()

    return HTMLResponse(
        "<div style='background-color:#d1e7dd; color:#0f5132; padding:10px; border-radius:6px; text-align:center;'>Contraseña actualizada correctamente.</div>",
        status_code=200
    )
