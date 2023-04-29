import pytest
from src.models.chat_message import ChatMessage


@pytest.fixture
def sample_chat_message():
    return ChatMessage(
        message_id='1',
        user_id='1',
        message='test message',
        room_id='test room'
    )


def test_chat_message(sample_chat_message):
    assert sample_chat_message.message_id == '1'
    assert sample_chat_message.user_id == '1'
    assert sample_chat_message.message == 'test message'
    assert sample_chat_message.room_id == 'test room'


def test_chat_message_validation():        
    with pytest.raises(ValueError):
        ChatMessage(
            message_id='1',
            user_id='',
            message='test message',
            room_id='test room'
        )
        
    with pytest.raises(ValueError):
        ChatMessage(
            message_id='1',
            user_id='1',
            message='',
            room_id='test room'
        )
        
    with pytest.raises(ValueError):
        ChatMessage(
            message_id='1',
            user_id='1',
            message='test message',
            room_id=''
        )
