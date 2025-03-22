from langchain_aws import ChatBedrock

from app.config import config as settings

USE_CREDENTIALS = settings.AWS_USE_CREDENTIALS_BEDROCK == "true"

def chat_bedrock(question):
    if USE_CREDENTIALS:
        llm = ChatBedrock(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID_BEDROCK,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_BEDROCK,
                region=settings.AWS_REGION_BEDROCK,
                # model: 'anthropic.claude-3-haiku-20240307-v1:0',
                model="anthropic.claude-3-sonnet-20240229-v1:0",
                beta_use_converse_api=True
        )
    else:
        llm = ChatBedrock(
                # model: 'anthropic.claude-3-haiku-20240307-v1:0',
                model="anthropic.claude-3-sonnet-20240229-v1:0",
                beta_use_converse_api=True
        )

    return llm.invoke(question)
