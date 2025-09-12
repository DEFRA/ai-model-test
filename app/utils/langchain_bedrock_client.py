from langchain_aws import ChatBedrock

from app.config import config as settings

USE_CREDENTIALS = settings.AWS_USE_CREDENTIALS_BEDROCK == "true"

def chat_bedrock_client():
    model = settings.AWS_BEDROCK_MODEL
    if USE_CREDENTIALS:
        llm = ChatBedrock(
                region=settings.aws_region,
                model=model,
                beta_use_converse_api=True,
                guardrails={"guardrailId": settings.AWS_BEDROCK_GUARDRAIL, "guardrailVersion": settings.AWS_BEDROCK_GUARDRAIL_VERSION, "trace": "enabled"}
        )
    else:
        llm = ChatBedrock(
                model=model,
                beta_use_converse_api=True,
                guardrails={"guardrailId": settings.AWS_BEDROCK_GUARDRAIL, "guardrailVersion": settings.AWS_BEDROCK_GUARDRAIL_VERSION, "trace": "enabled"}
        )

    return llm

def chat_bedrock(question):
    llm = chat_bedrock_client()
    return llm.invoke(question)
