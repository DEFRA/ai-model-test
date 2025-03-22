from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.antropic_bedrock.router import router as anthropic_bedrock_router
from app.bedrock.router import router as bedrock_router
from app.common.mongo import get_mongo_client
from app.common.tracing import TraceIdMiddleware
from app.example.router import router as example_router
from app.health.router import router as health_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    logger.info("MongoDB client connected")
    client = await get_mongo_client()
    logger.info("MongoDB client connected")
    yield
    # Shutdown
    if client:
        await client.close()
        logger.info("MongoDB client closed")


app = FastAPI(lifespan=lifespan)

# Setup middleware
app.add_middleware(TraceIdMiddleware)

# Setup Routes
app.include_router(health_router)
app.include_router(example_router)
app.include_router(anthropic_bedrock_router)
app.include_router(bedrock_router)
