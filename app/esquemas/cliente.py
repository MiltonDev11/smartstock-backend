from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    cedula: str
    celular: str | None = None
    correo: EmailStr
