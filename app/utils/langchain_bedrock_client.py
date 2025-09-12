from langchain_aws import ChatBedrock

from app.config import config as settings


def chat_bedrock_client():
    model = settings.AWS_BEDROCK_MODEL

    llm = ChatBedrock(
            region=settings.aws_region,
            model=model,
            beta_use_converse_api=True,
            guardrails={"guardrailId": settings.AWS_BEDROCK_GUARDRAIL, "guardrailVersion": settings.AWS_BEDROCK_GUARDRAIL_VERSION, "trace": "enabled"}
    )

    return llm


def chat_bedrock(question):
    llm = chat_bedrock_client()
    return llm.invoke(question)
