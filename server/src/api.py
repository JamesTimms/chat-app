"""Main app server"""
import uuid
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Response, Request

from src.models.room import Room
from src.models.chat_message import ChatMessage


chat_router = APIRouter()

@chat_router.post("/add-room/", status_code=status.HTTP_201_CREATED)
async def handle_add_room(room: Room, response: Response, request: Request):
    '''
        Function to handle new room created by a client
    '''
    room = request.app.state.rooms_data.add_room(room)
    request.app.state.rooms_data.add_room(room)
    if room:
        await request.app.state.rooms_manager.broadcast_room(room)
        return {"message": "Room added"}
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "Room not added"}


@chat_router.websocket("/rooms")
async def handle_new_connection_rooms(websocket: WebSocket):
    '''
        Function to handle new conenctions to the rooms
        The function accepts the connection from the client
        and sends all the available rooms to the client
    '''
    try:
        await websocket.app.state.rooms_manager.add_rooms_listner(websocket)
        rooms = websocket.app.state.rooms_data.get_all_rooms()
        websocket.app.state.api_logger.info(f"Sending rooms: {len(rooms)}")
        for room in rooms:
            await websocket.app.state.rooms_manager.send_room_to(websocket, room)
        while True:
            # we keep the connection alive
            # when a new room is created by a client
            # we broadcast the new room to all the clients
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await websocket.app.state.rooms_manager.remove_rooms_listner(websocket)


@chat_router.websocket("/connect-rooms/{room_id}")
async def handle_connect_to_room(websocket: WebSocket, room_id: str):
    '''
        The function accepts the connection from the client
        and sends the messages to the clients of a specific room
    '''
    # Accept the connection from the client
    await websocket.app.state.chat_manager.connect(websocket, room_id)

    # Sending the messages to the new client
    messages = websocket.app.state.messages_data.get_messages_of(room_id)
    for message in messages:
        websocket.app.state.api_logger.info("Sending message to new client")
        await websocket.app.state.chat_manager.send_message_to(websocket, message)

    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            websocket.app.state.api_logger.info(f"Received {data}")

            if "type" in data and data["type"] == "close":
                websocket.app.state.chat_manager.disconnect(websocket, room_id)
            else:
                message = ChatMessage(
                    message_id=str(uuid.uuid4()),
                    user_id=data["user_id"],
                    message=data["message"],
                    room_id=data["room_id"]
                )
                websocket.app.state.messages_data.add_message(message)
                # Send the message to all the clients
                await websocket.app.state.chat_manager.broadcast(message, room_id)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        websocket.app.state.api_logger.info("Client disconnected")
        websocket.app.state.chat_manager.disconnect(websocket, room_id)
