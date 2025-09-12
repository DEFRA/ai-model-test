import boto3
from langchain_aws import BedrockEmbeddings

from app.config import config as settings

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=settings.aws_region
)


def embedding_bedrock():
    return BedrockEmbeddings(
        client=bedrock_runtime,
        model_id=settings.AWS_BEDROCK_EMBEDDING_MODEL
    )
