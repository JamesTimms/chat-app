""" 
    Model class for chat rooms
"""
from pydantic import BaseModel, validator


class Room (BaseModel):
    '''
        Room dataclass for the chat
    '''

    name: str
    description: str

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('Room name cannot be empty')
        return value

    @validator('description')
    def description_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('Room description cannot be empty')
        return value

    def to_dict(self):
        '''
            Converts the room to a dictionary
        '''
        return {
            '__id:': self.name,
            'name': self.name,
            'description': self.description,
        }
