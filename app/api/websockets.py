from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websockets.manager import manager

router = APIRouter()

@router.websocket("/ws/events/{event_id}")
async def websocket_endpoint(websocket: WebSocket,event_id: int):
    #no jwt ,no http ....everyone should be able to seeseat availabity even without login
    await manager.connect(
        event_id,
        websocket,
    )
    #we need to keep the connection on so we write it inside a while loop even if we are not excepting any msg at a moment
    #when it .recive_text() raises WebSocketDisconeent only then it ends the connection 
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(
            event_id,
            websocket,
        )
