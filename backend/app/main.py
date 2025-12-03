from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .api.routes_production import router as production_router
from .api.routes_trace import router as trace_router
from .ws import manager

app = FastAPI(title='MES Starter Full')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
async def startup():
    # Create tables for dev
    Base.metadata.create_all(bind=engine)

app.include_router(production_router, prefix='/api/workorders', tags=['workorders'])
app.include_router(trace_router, prefix='/api/trace', tags=['trace'])

@app.get('/')
def root():
    return {'status': 'ok', 'service': 'mes-starter-full'}

@app.websocket('/ws/line/{line_id}')
async def websocket_endpoint(websocket: WebSocket, line_id: str):
    await manager.connect(line_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # broadcast to other clients on same line
            await manager.broadcast(line_id, data)
    except WebSocketDisconnect:
        manager.disconnect(line_id, websocket)
