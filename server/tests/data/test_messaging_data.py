import uuid
import pytest
from unittest import mock
from mongomock import MongoClient
from src.data.messaging_data import MessageData
from src.models.chat_message import ChatMessage


@pytest.fixture
def message_data(request):
    # create a mock database
    chat_db = f"test_chat_db_{uuid.uuid4()}"
    mongo_client = MongoClient()
    mongo_url = f"mongodb://{mongo_client.HOST}:{mongo_client.PORT}/"
    message_data = MessageData(mongo_url, chat_db)

    # setup cleanup function to drop test database
    def cleanup():
        mongo_client.drop_database(chat_db)
    request.addfinalizer(cleanup)

    yield message_data


def test_add_message_success(message_data):
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    message_data.add_message(message)
    assert len(message_data.get_messages_of("test_room")) == 1


def test_add_message_failure(message_data):
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    with pytest.raises(Exception):
        # Raise an exception when inserting the message
        with message_data.messages_collection.watch([{'$match': {'operationType': 'insert'}}]):
            message_data.add_message(message)


def test_get_messages_of_success(message_data):
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    message_data.add_message(message)

    messages = message_data.get_messages_of("test_room")
    assert len(messages) == 1
    assert messages[-1].user_id == "test_user"
    assert messages[-1].message == "Test message"
    assert messages[-1].room_id == "test_room"


def test_get_messages_of_failure(message_data):
    with mock.patch.object(message_data.messages_collection, 'find', side_effect=Exception):
        messages = message_data.get_messages_of("test_room")
        assert len(messages) == 0
