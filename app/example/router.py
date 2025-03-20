from logging import getLogger

from fastapi import APIRouter, Depends

from app.common.http_client import async_client
from app.common.mongo import get_db

router = APIRouter(prefix="/example")
logger = getLogger(__name__)


# remove this example route
@router.get("/test")
async def root():
    logger.info("TEST ENDPOINT")
    return {"ok": True}


@router.get("/db")
async def db_query(db=Depends(get_db)):
    await db.example.insert_one({"foo": "bar"})
    data = await db.example.find_one({}, {"_id": 0})
    return {"ok": data}


@router.get("/http")
async def http_query(client=Depends(async_client)):
    resp = await client.get("http://localhost:9999/test")
    return {"ok": resp.status_code}
