from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime, timezone
import json

router = APIRouter()

@router.websocket("/stream")
async def coordinate_stream(websocket: WebSocket):
    """
    Establishes a real-time connection to stream Geodetic coordinates
    to the frontend visualization engine (e.g., CesiumJS or Three.js).
    """
    await websocket.accept()
    print("[WS] Client connected to live telemetry stream.")
    
    try:
        while True:
            # For the MVP, this acts as a heartbeat. 
            # In production, you will pull the cached active satellites,
            # run them through sgp4_engine.propagate_satellite_state, 
            # and yield their updated Lat/Lon/Alt here every second.
            
            now = datetime.now(timezone.utc).isoformat()
            payload = {
                "type": "telemetry_update",
                "timestamp": now,
                "data": [] # List of updated Geodetic dictionaries will go here
            }
            
            await websocket.send_text(json.dumps(payload))
            
            # Throttle the stream to 1 frame per second to save bandwidth
            await asyncio.sleep(1.0)
            
    except WebSocketDisconnect:
        print("[WS] Client disconnected from telemetry stream.")
    except Exception as e:
        print(f"[WS] Error in stream: {e}")