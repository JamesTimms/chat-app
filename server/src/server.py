from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.connection_manager import ConnectionManager
import traceback
import json

app = FastAPI()

connection_manager = ConnectionManager()

@app.websocket("/messaging")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the connection from the client
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_text()
            print("Received: ", data)
            # Send the message to all the clients
            await connection_manager.broadcast(data)

    except WebSocketDisconnect:
        print('WebSocketDisconnect Exception...')
        traceback.print_exc()

    finally:
        # Remove the connection from the list of active connections
        id = connection_manager.disconnect(websocket)
        # Broadcast the disconnection of client with id to all the clients
        print(f'Client disconnected {id}')
        await connection_manager.broadcast(json.dumps({"type": "disconnected", "id": id}))
