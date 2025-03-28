from logging import getLogger

from openai import AzureOpenAI, DefaultHttpxClient

from app.config import config as settings

logger = getLogger(__name__)

model_name = "gpt-4"
deployment = "gpt-4"

http_proxy = settings.HTTPS_PROXY


def chat_azureopenai(question):
    client = AzureOpenAI(
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY
    )

    if http_proxy:
        logger.info("Using HTTP Proxy")
        client.with_options(http_client=DefaultHttpxClient(
            proxy=http_proxy
        ))

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    return response.choices[0].message.content
