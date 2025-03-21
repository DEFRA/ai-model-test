from fastapi import APIRouter, HTTPException
from langchain_aws import ChatBedrock
from pydantic import BaseModel, Field

from app.config import config

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
        llm = ChatBedrock(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID_BEDROCK,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_BEDROCK,
            region=config.AWS_REGION_BEDROCK,
            # model: 'anthropic.claude-3-haiku-20240307-v1:0',
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            beta_use_converse_api=True
        )

        response = llm.invoke(request.question)

        return {
            "status": "success",
            "question": request,
            "response": response.content,
            "usage": response.usage_metadata
        }

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
