from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection

from app.common.mongo import get_db

logger = getLogger(__name__)

router = APIRouter()

@router.get("/chat/history/session/{session_id}")
async def get_history(session_id: str, db=Depends(get_db)):
    try:
        chat_collection: Collection = db["chat_history"]

        chat_history = await chat_collection.find_one({"session_id": session_id})

        return {
            "status": "success",
            "session_id": session_id,
            "email": chat_history.get("email") if chat_history else None,
            "chat_history": chat_history.get("chat_history") if chat_history else [],
        }

    except Exception as e:
        logger.exception("Failed to get chat history for session ID: %s", session_id)
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/chat/history/session")
async def get_historyby_email(email: str, db=Depends(get_db)):
    try:
        chat_collection: Collection = db["chat_history"]

        chat_history_cursor = chat_collection.find({"email": email})
        chat_history_records = await chat_history_cursor.to_list(length=None)

        result = [
            {
                "email": record.get("email"),
                "session": record.get("session_id"),
                "chat_history": record.get("chat_history")[0][1]
            }
            for record in chat_history_records
        ]

        return {
            "status": "success",
            "email": email,
            "chat_history": result,
        }

    except Exception as e:
        logger.exception("Failed to get chat history for email: %s", email)
        raise HTTPException(status_code=500, detail=str(e)) from e
