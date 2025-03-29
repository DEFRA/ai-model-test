from logging import getLogger

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.langgraph_rag_chat import run_rag_llm

logger = getLogger(__name__)

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str  = Field(
        description="The question to ask the model",
        examples=["What is machine learning?"],
    )

@router.post("/langgraph/rag/chat")
async def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        question = request.question
        response = run_rag_llm(question)
        answer = response["answer"]

        return {
            "status": "success",
            "answer": answer,
        }

    except Exception as e:
            logger.exception("Failed to chat with LangGraph Rag Chat")
            raise HTTPException(status_code=500, detail=str(e)) from e
