import logging
import pytest
from unittest.mock import patch, MagicMock
from src.logger.logger import Logger


@pytest.fixture
def sample_logger():
    return Logger("TestLogger", log_level="DEBUG")


def test_logger_creation(sample_logger):
    assert isinstance(sample_logger.logger, logging.Logger)


def test_info_logging(sample_logger, caplog):
    sample_logger.info("Test info message")
    assert "Test info message" in caplog.text


def test_error_logging(sample_logger, caplog):
    sample_logger.error("Test error message")
    assert "Test error message" in caplog.text


def test_exception_logging(sample_logger, capsys):
    with patch("logging.Logger.exception") as mock_exception:
        sample_logger.exception("Test exception message")
        mock_exception.assert_called_once_with("Test exception message")


def test_set_level(sample_logger):
    sample_logger.logger.setLevel = MagicMock()
    sample_logger.logger.setLevel("test_level")
    sample_logger.logger.setLevel.assert_called_once_with("test_level")
