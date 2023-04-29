import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import WebSocket
from src.models.room import Room
from src.managers.rooms_manager import RoomsManager


@pytest.fixture
def sample_room():
    return Room(name='Test Room', description='This is a test room')


@pytest.fixture
def rooms_manager():
    return RoomsManager()


@pytest.fixture
def websocket():
    return AsyncMock(spec=WebSocket)


@pytest.mark.asyncio
async def test_add_rooms_listener(rooms_manager, websocket):
    await rooms_manager.add_rooms_listner(websocket)
    assert websocket in rooms_manager.rooms_listeners


@pytest.mark.asyncio
async def test_remove_rooms_listener(rooms_manager, websocket):
    rooms_manager.rooms_listeners.add(websocket)
    await rooms_manager.remove_rooms_listner(websocket)
    assert websocket not in rooms_manager.rooms_listeners


@pytest.mark.asyncio
async def test_send_room_to(rooms_manager, websocket, sample_room):
    expected_dict = sample_room.to_dict()
    await rooms_manager.add_rooms_listner(websocket)
    await rooms_manager.send_room_to(websocket, sample_room)
    websocket.send_json.assert_called_once_with(expected_dict)


@pytest.mark.asyncio
async def test_broadcast_room(rooms_manager, sample_room):
    ws1, ws2, ws3 = AsyncMock(spec=WebSocket), AsyncMock(spec=WebSocket), AsyncMock(spec=WebSocket)
    rooms_manager.rooms_listeners = {ws1, ws2, ws3}

    # mock send_json
    ws1.send_json = AsyncMock()
    ws2.send_json = MagicMock(side_effect=Exception)
    ws3.send_json = AsyncMock()

    # expected results
    expected_json = {'__id:': 'Test Room', 'name': 'Test Room', 'description': 'This is a test room'}

    # broadcast room
    await rooms_manager.broadcast_room(sample_room)

    # assert that send_json is called for ws1 and ws3 only
    ws1.send_json.assert_called_once_with(expected_json)
    ws2.send_json.assert_called_once_with(expected_json)
    ws3.send_json.assert_called_once_with(expected_json)

    # assert that ws2 was removed from the listeners due to exception
    assert ws2 not in rooms_manager.rooms_listeners
