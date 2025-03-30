from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError
from pymongo.collection import Collection

from app.common.mongo import get_db
from app.utils.langchain_simple_rag_chat import run_llm

logger = getLogger(__name__)

router = APIRouter()
chat_history = []

class QuestionRequest(BaseModel):
    email: str = Field(
        description="The email of the user",
        example="user@example.com",
    )
    session_id: UUID = Field(
        description="The session ID for the chat (must be a valid GUID)",
        example="550e8400-e29b-41d4-a716-446655440000",
    )
    question: str = Field(
        description="The question to ask the model",
        examples=["What is machine learning?"],
    )


@router.post("/langchain/simple/rag/chat")
async def chat(request: QuestionRequest, db=Depends(get_db)):
    try:
        chat_collection: Collection = db["chat_history"]

        session_id = str(request.session_id)
        email = request.email

        chat_entry = await chat_collection.find_one({"email": email, "session_id": session_id})
        chat_history = chat_entry["chat_history"] if chat_entry else []

        question = request.question
        response = run_llm(question, chat_history)
        answer = response["answer"]
        chat_history.append(("human", question))
        chat_history.append(("ai", answer))

        if chat_entry:
            await chat_collection.update_one(
                {"email": email, "session_id": session_id},
                {"$set": {"chat_history": chat_history}}
            )
        else:
            await chat_collection.insert_one({
                "email": email,
                "session_id": session_id,
                "chat_history": chat_history,
            })

        return {
            "status": "success",
            **response
        }

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        raise HTTPException(status_code=422, detail=e.errors()) from e
    except Exception as e:
        logger.exception("Failed to chat with LangGraph Rag Chat")
        raise HTTPException(status_code=500, detail=str(e)) from e
