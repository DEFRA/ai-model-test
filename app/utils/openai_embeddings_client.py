from langchain_openai import OpenAIEmbeddings

from app.config import config as settings


def embedding_openai():
    embeddings = OpenAIEmbeddings()

    if settings.HTTPS_PROXY is not None:
        embeddings.openai_proxy = settings.HTTPS_PROXY

    return embeddings
