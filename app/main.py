from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import users, password_reset, auth


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/plantillas")

app.include_router(users.router)
app.include_router(password_reset.router)
app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Conexión exitosa con PostgreSQL"}
    except Exception as e:
        return {"status": "error", "message": str(e)}