from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..db import SessionLocal
from ..models import WorkOrder

router = APIRouter()

class WorkOrderIn(BaseModel):
    order_id: str
    product: str
    quantity: int

@router.post('/create')
async def create_workorder(payload: WorkOrderIn):
    db = SessionLocal()
    existing = db.query(WorkOrder).filter(WorkOrder.order_id == payload.order_id).first()
    if existing:
        raise HTTPException(status_code=400, detail='workorder exists')
    wo = WorkOrder(order_id=payload.order_id, product=payload.product, quantity=payload.quantity)
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return {'status': 'ok', 'workorder': {'id': wo.id, 'order_id': wo.order_id}}

@router.get('/list')
async def list_workorders():
    db = SessionLocal()
    wos = db.query(WorkOrder).all()
    return [{'id': w.id, 'order_id': w.order_id, 'product': w.product, 'quantity': w.quantity} for w in wos]
