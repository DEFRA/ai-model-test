from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

from app.config import config as settings


def chat_azureopenai(question):
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4",
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version=settings.AZURE_API_VERSION
    )

    llm.openai_proxy = settings.HTTPS_PROXY

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=question),
    ]

    return llm.invoke(messages)
