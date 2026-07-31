from collections import defaultdict

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections=defaultdict(list)#initially empty i.e. 1->[] , 2->[]


    async def connect(self,event_id: int,websocket: WebSocket):
        await websocket.accept()#rule to write else fastapi rejects connecction

        self.active_connections[event_id].append(
            websocket
        )

    def disconnect(self,event_id: int,websocket: WebSocket):
        #to prevent from memoty leak 
        self.active_connections[event_id].remove(
            websocket
        )
        if not self.active_connections[event_id]:
            del self.active_connections[event_id]

    async def broadcast_to_event(self,event_id: int,message: dict):

        connections = self.active_connections.get(event_id, [])

        for websocket in connections.copy():
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(event_id, websocket)


manager = ConnectionManager()