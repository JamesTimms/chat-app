"""Initalise the main app server"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.api import chat_router
from src.settings import Settings
from src.logger.logger import Logger
from src.data.rooms_data import RoomsData
from src.data.messaging_data import MessageData
from src.managers.rooms_manager import RoomsManager
from src.managers.messaging_manager import MessagingManager


async def run_app(settings: Settings, logger: Logger):
    # Instance of the FastAPI app

    app = FastAPI()

    app.state.api_logger = logger

    app.state.api_logger.info("Adding Middleware...")
    # Adding the CORS middleware to the app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Creating the managers
    app.state.api_logger.info("Creating Managers...")
    app.state.chat_manager = MessagingManager()
    app.state.rooms_manager = RoomsManager()
    app.state.api_logger.info("Creating Room Data...")
    app.state.rooms_data = RoomsData(settings.MONGO_URI, settings.CHAT_DB)
    app.state.api_logger.info("Creating Messaging Data...")
    app.state.messages_data = MessageData(settings.MONGO_URI, settings.CHAT_DB)

    app.state.settings = settings

    app.state.api_logger.info("Adding chat router...")
    app.include_router(chat_router)

    return app
