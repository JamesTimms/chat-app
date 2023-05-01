import asyncio, uvicorn, os

from src.server import run_app
from src.settings import Settings
from src.logger.logger import Logger

if __name__ == "__main__":
    # Logger
    logger = Logger("API")
    logger.info("Initialising API server...")

    settings = Settings()

    app = asyncio.run(run_app(settings, logger))
    logger.info("Initialised")

    logger.info("Running API server...")
    uvicorn.run(
        app,
        port=settings.API_PORT,
        host=settings.API_HOST,
    )
