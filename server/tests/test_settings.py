from pydantic import ValidationError
import pytest

from src.settings import Settings


def test_settings():
    settings = Settings(MONGO_URL="mongodb://localhost:27017", CHAT_DB="my-chat")
    assert settings.API_PORT == 8000
    assert settings.API_HOST == "0.0.0.0"
    assert settings.MONGO_URL == "mongodb://localhost:27017"
    assert settings.CHAT_DB == "my-chat"


def test_settings_without_optional_params():
    settings = Settings(MONGO_URL="mongodb://localhost:27017")
    assert settings.API_PORT == 8000
    assert settings.API_HOST == "0.0.0.0"
    assert settings.MONGO_URL == "mongodb://localhost:27017"
    assert settings.CHAT_DB == "chat"


def test_settings_with_invalid_mongo_url():
    with pytest.raises(ValidationError):
        Settings(MONGO_URL="invalid_mongo_url")
