from app.db import engine, Base, SessionLocal
from app.models import WorkOrder, TraceRecord

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(WorkOrder).first():
    wo = WorkOrder(order_id='WO-1001', product='Model-X', quantity=500)
    db.add(wo)

if not db.query(TraceRecord).first():
    for i in range(1,6):
        tr = TraceRecord(serial=f'SN100{i}', station='assembly', status='PASS', metadata={'operator':'op1'})
        db.add(tr)

db.commit()
print('Seed complete')
