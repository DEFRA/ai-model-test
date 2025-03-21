from langchain_aws import ChatBedrock

from app.config import config


def chat_bedrock(question):
    llm = ChatBedrock(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID_BEDROCK,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_BEDROCK,
            region=config.AWS_REGION_BEDROCK,
            # model: 'anthropic.claude-3-haiku-20240307-v1:0',
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            beta_use_converse_api=True
        )

    return llm.invoke(question)

