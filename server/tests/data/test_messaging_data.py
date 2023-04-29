import uuid
import pytest
from unittest import mock
from src.data.messaging_data import MessageData
from src.models.chat_message import ChatMessage


@pytest.fixture
def message_data(request):
    # create a test database
    test_db_name = f"test_{uuid.uuid4()}"
    test_db_uri = f"mongodb://localhost:27017/{test_db_name}"
    message_data = MessageData(mongo_url=test_db_uri, db_name=test_db_name)

    # setup cleanup function to drop test database
    def cleanup():
        message_data.client.drop_database(test_db_name)
    request.addfinalizer(cleanup)

    yield message_data


def test_add_message_success(message_data):
    # create a mock ChatMessage object
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    with mock.patch.object(message_data.messages_collection, 'insert_one') as mock_insert:
        message_data.add_message(message)
        mock_insert.assert_called_once()


def test_add_message_failure(message_data):
    # create a mock ChatMessage object
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    with mock.patch.object(message_data.messages_collection, 'insert_one', side_effect=Exception) as mock_insert:
        message_data.add_message(message)
        mock_insert.assert_called_once()


def test_get_messages_of_success(message_data):
    # create a mock ChatMessage object
    message = ChatMessage(
        message_id=str(uuid.uuid4()),
        user_id="test_user",
        message="Test message",
        room_id="test_room"
    )

    # add the message to the database
    message_data.messages_collection.insert_one(message.to_dict())

    messages = message_data.get_messages_of("test_room")
    assert len(messages) == 1
    assert messages[-1].user_id == "test_user"
    assert messages[-1].message == "Test message"
    assert messages[-1].room_id == "test_room"


def test_get_messages_of_failure(message_data):
    with mock.patch.object(message_data.messages_collection, 'find', side_effect=Exception):
        messages = message_data.get_messages_of("test_room")
        assert len(messages) == 0
