from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.antropic_bedrock.router import router as anthropic_bedrock_router
from app.azure_openai.router import router as azure_openai_router
from app.common.mongo import get_mongo_client
from app.common.s3 import S3Client
from app.common.tracing import TraceIdMiddleware
from app.data_ingestion.router import router as data_ingestion_router
from app.example.router import router as example_router
from app.health.router import router as health_router
from app.langchain_azure_openai.router import router as langchain_azure_openai_router
from app.langchain_bedrock.router import router as langchain_bedrock_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    # s3_client = S3Client()
    # s3_client.check_connection()

    mongo_client = await get_mongo_client()
    logger.info("MongoDB client connected")
    yield

    # Shutdown

    # if s3_client:
        # s3_client.close_connection()
        # logger.info("S3 client closed")

    if mongo_client:
        await mongo_client.close()
        logger.info("MongoDB client closed")


app = FastAPI(lifespan=lifespan)

# Setup middleware
app.add_middleware(TraceIdMiddleware)

# Setup Routes
app.include_router(health_router)
app.include_router(example_router)
app.include_router(anthropic_bedrock_router)
app.include_router(langchain_bedrock_router)
app.include_router(data_ingestion_router)
app.include_router(azure_openai_router)
app.include_router(langchain_azure_openai_router)


