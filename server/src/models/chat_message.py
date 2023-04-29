"""
    Model class for chat messages
"""
import uuid
from pydantic import BaseModel, validator


class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    message_id: str = str(uuid.uuid4())
    user_id: str
    message: str
    room_id: str

    
    @validator('user_id', 'message', 'room_id')
    def check_not_empty(cls, v):
        if not v:
            raise ValueError('value cannot be empty')
        return v

    def to_dict(self) -> dict:
        '''
            Converts the dataclass to a dictionary
        '''
        return {
            'message_id': self.message_id,
            'message': self.message,
            'user_id': self.user_id,
            'room_id': self.room_id
        }
