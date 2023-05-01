import uuid
import pytest
from src.data.rooms_data import RoomsData
from src.models.room import Room


@pytest.fixture
def rooms_data(request):
    # create a test database
    chat_db = f"test_chat_db_{uuid.uuid4()}"
    mongo_url = f"mongodb://localhost:27017/{chat_db}"
    rooms_data = RoomsData(mongo_url, chat_db)

    # setup cleanup function to drop test database
    def cleanup():
        rooms_data.client.drop_database(chat_db)
    request.addfinalizer(cleanup)

    yield rooms_data


def test_add_room_success(rooms_data):
    # create a mock Room object
    room = Room(name="test_room", description="Test room")
    
    # add the room to the database
    result = rooms_data.add_room(room)
    
    # check that the room was added successfully
    assert result == room


def test_get_all_rooms_success(rooms_data):
    # get all rooms from the database
    result = rooms_data.get_all_rooms()
    
    # check that at least one room was returned
    assert len(result) > 0


def test_get_all_rooms_failure(rooms_data):
    # create a RoomsData object with an invalid Mongo URI
    rooms_data = RoomsData(mongo_url="invalid_uri")
    
    # get all rooms from the database
    result = rooms_data.get_all_rooms()
    
    # check that None is returned
    assert result is None
