from __future__ import annotations

import asyncio
import json
from typing import Dict, Set, Tuple

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        # key: (owner_id, device_id) -> set of websockets
        self._connections: Dict[Tuple[str, str], Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, owner_id: str, device_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        key = (owner_id, device_id)
        async with self._lock:
            self._connections.setdefault(key, set()).add(websocket)

    async def disconnect(self, owner_id: str, device_id: str, websocket: WebSocket) -> None:
        key = (owner_id, device_id)
        async with self._lock:
            conns = self._connections.get(key)
            if conns and websocket in conns:
                conns.remove(websocket)
                if not conns:
                    self._connections.pop(key, None)

    async def broadcast(self, owner_id: str, device_id: str, message: dict) -> None:
        key = (owner_id, device_id)
        async with self._lock:
            conns = list(self._connections.get(key, set()))
        text = json.dumps(message)
        for ws in conns:
            try:
                await ws.send_text(text)
            except Exception:
                try:
                    await ws.close()
                except Exception:
                    pass
                await self.disconnect(owner_id, device_id, ws)


ws_manager = WebSocketManager()
