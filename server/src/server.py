from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


@app.websocket("/messaging")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  try:
    while True:
        data = await websocket.receive_text()
        print(f"Received data {data}")
        await websocket.send_text(data)
  except WebSocketDisconnect:
      print(f"client disconnected")
