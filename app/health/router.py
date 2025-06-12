from fastapi import APIRouter
from logging import getLogger

router = APIRouter()

logger = getLogger(__name__)

# Do not remove - used for health checks
@router.get("/health")
async def health():
    return {"status": "ok"}
