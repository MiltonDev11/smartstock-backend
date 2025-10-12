from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from fastapi_mail import FastMail, MessageSchema
from app.core.email_config import conf
from fastapi_mail import MessageType
from fastapi import HTTPException
from app.core.security import hash_password

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

@router.get("/reset-password/{user_id}", response_class=HTMLResponse)
def reset_password_form(user_id: int):
    return f"""
    <html>
        <head>
            <title>Restablecer contraseña</title>
        </head>
        <body style="font-family: Arial; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 300px;">
                <h2 style="text-align: center;">Nueva Contraseña</h2>
                <form method="post" action="/reset-password/{user_id}">
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

@router.post("/reset-password/{user_id}")
def reset_password(user_id: int, new_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    print("NUEVA CONTRASEÑA:", new_password)
    user.password_hash = hash_password(new_password) # type: ignore
    db.commit()

    return HTMLResponse(
        """
        <div style='background-color: #d1e7dd; color: #0f5132; padding: 10px; border-radius: 6px; text-align: center;'>
            Contraseña actualizada correctamente. Ya puedes cerrar esta ventana y volver a iniciar sesión.
        </div>
        """,
        status_code=200
    )