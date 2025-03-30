from langchain_openai import AzureOpenAIEmbeddings

from app.config import config as settings


def embedding_azureopenai():
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-small",
        azure_deployment="text-embedding-3-small",
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version="2024-12-01-preview",
        openai_api_type="azure_openai_chat"
    )

    embeddings.openai_proxy = settings.HTTPS_PROXY

    return embeddings
