from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from core.security import decode_token
from services.ws_manager import ws_manager

router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/telemetry/{device_id}")
async def ws_telemetry(websocket: WebSocket, device_id: str):
    # Validate JWT passed as query param 'token'
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4401)
        return
    try:
        payload = decode_token(token)
        user_id = str(payload.get("sub"))
        if not user_id:
            await websocket.close(code=4401)
            return
    except Exception:
        await websocket.close(code=4401)
        return

    await ws_manager.connect(user_id, device_id, websocket)
    try:
        while True:
            # Keep alive; ignore client messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(user_id, device_id, websocket)
