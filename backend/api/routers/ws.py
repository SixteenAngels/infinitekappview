from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from core.security import get_current_user_id
from services.ws_manager import ws_manager

router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/telemetry/{device_id}")
async def ws_telemetry(websocket: WebSocket, device_id: str):
  # Accept without auth header due to FastAPI WS limitations, use query token if provided
  await websocket.accept()
  user_id = websocket.query_params.get("token_user") or "public"
  try:
      await ws_manager.connect(user_id, device_id, websocket)
      while True:
          # Keep the connection alive; no incoming messages needed
          await websocket.receive_text()
  except WebSocketDisconnect:
      await ws_manager.disconnect(user_id, device_id, websocket)
