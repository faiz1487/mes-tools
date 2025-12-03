from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, line_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(line_id, []).append(websocket)

    def disconnect(self, line_id: str, websocket: WebSocket):
        if line_id in self.active_connections:
            try:
                self.active_connections[line_id].remove(websocket)
            except ValueError:
                pass

    async def broadcast(self, line_id: str, message: str):
        conns = self.active_connections.get(line_id, [])
        for ws in list(conns):
            try:
                await ws.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()
