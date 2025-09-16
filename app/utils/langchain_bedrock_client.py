from langchain_aws import ChatBedrockConverse

from app.config import config as settings


def chat_bedrock_client():
    model = settings.AWS_BEDROCK_MODEL

    llm = ChatBedrockConverse(
            region=settings.aws_region,
            model_id=model,
            provider="anthropic",
            guardrails={"guardrailId": settings.AWS_BEDROCK_GUARDRAIL, "guardrailVersion": settings.AWS_BEDROCK_GUARDRAIL_VERSION, "trace": "enabled"}
    )

    return llm


def chat_bedrock(question):
    llm = chat_bedrock_client()
    return llm.invoke(question)
