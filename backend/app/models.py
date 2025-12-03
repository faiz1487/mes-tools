from sqlalchemy import Column, Integer, String, DateTime, JSON
from .db import Base
from datetime import datetime

class WorkOrder(Base):
    __tablename__ = 'workorders'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TraceRecord(Base):
    __tablename__ = 'trace_records'
    id = Column(Integer, primary_key=True, index=True)
    serial = Column(String, index=True, nullable=False)
    station = Column(String, nullable=False)
    status = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'station': self.station,
            'status': self.status,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }
