from fastapi import WebSocket

async def stream_updates(websocket: WebSocket):
    await websocket.accept()
