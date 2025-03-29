from langchain_aws import ChatBedrock

from app.config import config as settings

USE_CREDENTIALS = settings.AWS_USE_CREDENTIALS_BEDROCK == "true"

def chat_bedrock_client():
    model = settings.AWS_BEDROCK_MODEL
    if USE_CREDENTIALS:
        llm = ChatBedrock(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID_BEDROCK,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_BEDROCK,
                region=settings.AWS_REGION_BEDROCK,
                model=model,
                beta_use_converse_api=True
        )
    else:
        llm = ChatBedrock(
                model=model,
                beta_use_converse_api=True
        )

    return llm

def chat_bedrock(question):
    llm = chat_bedrock_client()
    return llm.invoke(question)
