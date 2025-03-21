from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.bedrock_client import chat_bedrock

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str  = Field(
        description="The question to ask the model",
        examples=["What is machine learning?"],
    )

@router.post("/chat")
async def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        response = chat_bedrock(request.question)

        return {
            "status": "success",
            "question": request,
            "response": response.content,
            "usage": response.usage_metadata
        }

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
