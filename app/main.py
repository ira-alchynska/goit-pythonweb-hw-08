import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import routes
from .models.models import Base
from .core.database import engine


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting up the application...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Application startup complete.")

    yield  

    logger.info("Shutting down the application...")


app = FastAPI(title="Contacts API", lifespan=lifespan)
app.include_router(routes.router, prefix="/api")
