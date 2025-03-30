from langchain_aws import BedrockEmbeddings

from app.config import config as settings


def embedding_bedrock():
    return BedrockEmbeddings(
        region=settings.AWS_REGION_BEDROCK,
        model_id="amazon.titan-embed-text-v2:0",
    )
