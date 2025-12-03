from fastapi import APIRouter, HTTPException
from ..db import SessionLocal
from ..models import TraceRecord

router = APIRouter()

@router.get('/{serial}')
async def get_trace(serial: str):
    db = SessionLocal()
    recs = db.query(TraceRecord).filter(TraceRecord.serial == serial).order_by(TraceRecord.timestamp).all()
    return [r.to_dict() for r in recs]

@router.post('/add')
async def add_trace(payload: dict):
    db = SessionLocal()
    if not payload.get('serial') or not payload.get('station'):
        raise HTTPException(status_code=400, detail='serial and station required')
    tr = TraceRecord(serial=payload.get('serial'), station=payload.get('station'), status=payload.get('status','UNKNOWN'), metadata=payload.get('metadata',{}))
    db.add(tr)
    db.commit()
    db.refresh(tr)
    return {'status': 'ok', 'id': tr.id}
