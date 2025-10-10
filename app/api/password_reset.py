from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from fastapi_mail import FastMail, MessageSchema
from app.core.email_config import conf
from fastapi_mail import MessageType

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

    # Crear el mensaje
    mensaje = MessageSchema(
        subject="Restablecer contraseña - SmartStock",
        recipients=[correo],
        body=f"""
        <h2>Hola {user.nombre},</h2>
        <p>Recibimos una solicitud para restablecer tu contraseña.</p>
        <p>Haz clic en el siguiente enlace para continuar:</p>
        <a href="http://127.0.0.1:8000/reset-password/{user.id}" 
            style="display:inline-block; background-color:#007bff; color:white; padding:10px 20px; border-radius:5px; text-decoration:none;">
            Restablecer contraseña
        </a>
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