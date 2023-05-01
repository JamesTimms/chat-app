import uuid
import pytest
from src.models.room import Room
from mongomock import MongoClient
from src.data.rooms_data import RoomsData


@pytest.fixture
def rooms_data(request):
    # create a mock database
    chat_db = f"test_chat_db_{uuid.uuid4()}"
    mongo_client = MongoClient()
    mongo_url = f"mongodb://{mongo_client.HOST}:{mongo_client.PORT}/"
    rooms_data = RoomsData(mongo_url, chat_db)

    # setup cleanup function to drop test database
    def cleanup():
        rooms_data.client.drop_database(chat_db)
    request.addfinalizer(cleanup)

    yield rooms_data


def test_add_room_success(rooms_data):
    room = Room(name="test_room", description="Test room")
    result = rooms_data.add_room(room)
    
    assert result == room


def test_get_all_rooms_success(rooms_data):
    result = rooms_data.get_all_rooms()
    
    assert len(result) > 0
