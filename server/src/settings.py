from pydantic import BaseSettings, MongoDsn
from typing import Optional


# These variables set from environment variables
class Settings(BaseSettings):
    MONGO_URI: MongoDsn = None
    CHAT_DB: Optional[str] = "chat"
    
    API_PORT: Optional[int] = 8000
    API_HOST: Optional[str] = "0.0.0.0"
  