"""
    Logger class to log the messages to the console
"""
from colorlog import ColoredFormatter
from dataclasses import dataclass
import logging


@dataclass()
class Logger:
    '''
        Logger class to log the messages to the console
    '''


    def __init__(self, logger_name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(logger_name)
        handler = logging.StreamHandler()

        handler.setFormatter(
            ColoredFormatter(
                "%(log_color)s%(asctime)s [%(name)s] %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S:%f",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        self.logger.setLevel(log_level)
        self.logger.addHandler(handler)


    def info(self, message: object):
        '''
            Logs the message with level INFO
        '''
        self.logger.info(message)


    def error(self, message: object):
        '''
            Logs the message with level ERROR
        '''
        self.logger.error(message)


    def exception(self, message: object):
        '''
            Logs the message with level EXCEPTION
        '''
        self.logger.exception(message)
