from unittest.mock import AsyncMock
from src.models.chat_message import ChatMessage
from src.managers.messaging_manager import MessagingManager


pytest_plugins = ('pytest_asyncio',)


async def test_connect():
    messaging_manager = MessagingManager()
    websocket = AsyncMock()
    room_id = "test_room"

    assert len(messaging_manager.active_connections) == 0

    # test new connection
    await messaging_manager.connect(websocket, room_id)
    assert len(messaging_manager.active_connections) == 1
    assert room_id in messaging_manager.active_connections
    assert websocket in messaging_manager.active_connections[room_id]

    # test existing connection
    await messaging_manager.connect(websocket, room_id)
    assert len(messaging_manager.active_connections) == 1
    assert room_id in messaging_manager.active_connections
    assert websocket in messaging_manager.active_connections[room_id]


async def test_disconnect():
    messaging_manager = MessagingManager()
    websocket1 = AsyncMock()
    websocket2 = AsyncMock()
    room_id = "test_room"
    messaging_manager.active_connections[room_id] = set()

    await messaging_manager.connect(websocket1, room_id)
    await messaging_manager.connect(websocket2, room_id)

    assert len(messaging_manager.active_connections[room_id]) == 2

    # test disconnect
    messaging_manager.disconnect(websocket1, room_id)
    assert len(messaging_manager.active_connections[room_id]) == 1

    messaging_manager.disconnect(websocket2, room_id)
    assert len(messaging_manager.active_connections[room_id]) == 0


async def test_send_message_to():
    messaging_manager = MessagingManager()
    websocket = AsyncMock()
    room_id = "test_room"
    message = ChatMessage(
        message_id=1,
        user_id=1,
        room_id=room_id,
        message="test_message"
    )

    # test send_message_to
    await messaging_manager.send_message_to(websocket, message)
    websocket.send_json.assert_called_once_with(message.to_dict())


async def test_broadcast():
    messaging_manager = MessagingManager()
    websocket1 = AsyncMock()
    websocket2 = AsyncMock()
    room_id = "test_room"
    message = ChatMessage(
        message_id=1,
        user_id=1,
        room_id=room_id,
        message="test_message"
    )

    await messaging_manager.connect(websocket1, room_id)
    await messaging_manager.connect(websocket2, room_id)

    # test broadcast
    await messaging_manager.broadcast(message, room_id)
    assert websocket1.send_json.call_count == 1
    assert websocket2.send_json.call_count == 1
