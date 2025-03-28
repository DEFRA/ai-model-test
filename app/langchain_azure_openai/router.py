from logging import getLogger

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.langchain_azure_openai_client import chat_azureopenai

logger = getLogger(__name__)

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str  = Field(
        description="The question to ask the model",
        examples=["What is machine learning?"],
    )

@router.post("/langchain/azureopenai/chat")
async def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        response = chat_azureopenai(request.question)

        return {
            "status": "success",
            "answer": response.content,
        }

    except Exception as e:
            logger.exception("Failed to chat with Langchain Azure OpenAI")
            raise HTTPException(status_code=500, detail=str(e)) from e
