import boto3
from langchain_aws import BedrockEmbeddings

from app.config import config as settings

USE_CREDENTIALS = settings.AWS_USE_CREDENTIALS_BEDROCK == "true"

if USE_CREDENTIALS:
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=settings.AWS_REGION_BEDROCK,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID_BEDROCK,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_BEDROCK
    )
else:
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
    )


def embedding_bedrock():
    return BedrockEmbeddings(
        client=bedrock_runtime,
        model_id="amazon.titan-embed-text-v2:0",
    )
