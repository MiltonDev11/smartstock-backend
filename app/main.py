from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from app.api import users

app = FastAPI()

app.include_router(users.router)

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