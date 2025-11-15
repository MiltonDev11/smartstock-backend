"""Módulo `app.api.solicitudes`.

Define endpoints para crear y administrar solicitudes desde la perspectiva
del vendedor y del administrador. Incluye rutas para crear solicitudes,
listar, obtener y cambiar estado.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.solicitud import Solicitud, SolicitudItem, SolicitudStatus
from app.models.user import User
from app.esquemas.solicitud import SolicitudCreate, SolicitudOut
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/vendedor", tags=["Vendedor"])

@router.post("/crear-solicitud", response_model=SolicitudOut)
def crear_solicitud(payload: SolicitudCreate, db: Session = Depends(get_db)):
    # 1) validar cliente existe
    cliente = db.query(User).filter(User.cedula == payload.cliente_cedula).first()
    if not cliente:
        raise HTTPException(status_code=400, detail="Cédula no registrada")

    # 2) crear solicitud
    nueva = Solicitud(
        cliente_cedula = payload.cliente_cedula,
        status = SolicitudStatus.pendiente
    )
    db.add(nueva)
    db.flush()  # asigna id sin commit

    # 3) crear items
    for it in payload.items:
        item = SolicitudItem(
            solicitud_id = nueva.id,
            descripcion = it.descripcion,
            cantidad = it.cantidad,
            precio_unitario = it.precio_unitario
        )
        db.add(item)

    db.commit()
    db.refresh(nueva)
    return nueva

# ---------------------------------------------------
# Admin endpoints para listar / filtrar / obtener
# ---------------------------------------------------
from fastapi import Query

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/api/solicitudes", response_model=list[SolicitudOut])
def listar_solicitudes(status: str = Query(None), search: str = Query(None), db: Session = Depends(get_db)):
    q = db.query(Solicitud)
    if status:
        q = q.filter(Solicitud.status == status)
    if search:
        # buscar por id de solicitud (S0001 sin prefijo) o por id_producto (solicitud_items.id)
        if search.startswith("S"):
            try:
                sid = int(search.lstrip("S"))
                q = q.filter(Solicitud.id == sid)
            except:
                pass
        else:
            # buscar por item id
            q = q.join(Solicitud.items).filter(SolicitudItem.id == int(search))
    q = q.order_by(Solicitud.created_at.desc())
    results = q.all()
    return results

@admin_router.get("/api/solicitudes/{solicitud_id}", response_model=SolicitudOut)
def obtener_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    s = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return s

@admin_router.post("/api/solicitudes/{solicitud_id}/estado")
def cambiar_estado(solicitud_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    s = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if nuevo_estado not in [e.value for e in SolicitudStatus]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    s.status = SolicitudStatus(nuevo_estado)
    if s.status == SolicitudStatus.completado:
        from datetime import datetime, timezone
        s.delivery_date = datetime.now(timezone.utc)
    db.commit()
    db.refresh(s)
    return {"msg":"Estado actualizado"}
