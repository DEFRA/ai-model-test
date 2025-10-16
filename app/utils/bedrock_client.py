import boto3
import json

from app.config import config as settings

bedrock_client: boto3.client = None


def get_bedrock_client():
    global bedrock_client
    
    if bedrock_client is None:
        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region
        )

    return bedrock_client


def chat_bedrock(question: str) -> str:
    bedrock_client = get_bedrock_client()

    request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": settings.ANTHROPIC_MAX_TOKENS,
        "temperature": settings.ANTHROPIC_TEMPERATURE,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": question}]
            }
        ]
    }

    json_request = json.dumps(request)

    invoke_args = {
        "modelId": settings.AWS_BEDROCK_MODEL,
        "body": json_request
    }

    if settings.AWS_BEDROCK_GUARDRAIL and settings.AWS_BEDROCK_GUARDRAIL_VERSION:
        invoke_args["guardrailIdentifier"] = settings.AWS_BEDROCK_GUARDRAIL
        invoke_args["guardrailVersion"] = settings.AWS_BEDROCK_GUARDRAIL_VERSION

    response = bedrock_client.invoke_model(**invoke_args)

    model_response = json.loads(response["body"].read())

    return model_response["content"][0]["text"]
