import pytest
from src.models.room import Room

def test_new_room():
    room = Room(name="general", description="This is a test room").to_dict()
    assert room['__id:'] == "general"
    assert room['name'] == "general"
    assert room['description'] == "This is a test room"

def test_room_invalid_name():
    with pytest.raises(ValueError):
        Room(name="", description="This is an invalid room name")

def test_room_invalid_description():
    with pytest.raises(ValueError):
        Room(name="test_room", description="")
