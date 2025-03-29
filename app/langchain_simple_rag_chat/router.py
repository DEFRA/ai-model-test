from logging import getLogger

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.langchain_simple_rag_chat import run_llm

logger = getLogger(__name__)

router = APIRouter()
chat_history = []

class QuestionRequest(BaseModel):
    question: str  = Field(
        description="The question to ask the model",
        examples=["What is machine learning?"],
    )

@router.post("/langchain/simple/rag/chat")
async def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        question = request.question
        response = run_llm(question, chat_history)
        answer = response["answer"]
        chat_history.append(("human", question))
        chat_history.append(("ai", answer))

        return {
            "status": "success",
            **response,
        }

    except Exception as e:
            logger.exception("Failed to chat with LangGraph Rag Chat")
            raise HTTPException(status_code=500, detail=str(e)) from e
