from logging import getLogger

import httpx
from openai import AzureOpenAI, DefaultHttpxClient

from app.config import config as settings

logger = getLogger(__name__)

model_name = "gpt-4"
deployment = "gpt-4"

cdp_https_proxy = settings.CDP_HTTPS_PROXY
cdp_http_proxy = settings.CDP_HTTP_PROXY


def chat_azureopenai(question):
    client = AzureOpenAI(
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY
    )

    if cdp_https_proxy:
        logger.info(f"Using HTTP Proxy: {cdp_http_proxy}")
        client.with_options(http_client=DefaultHttpxClient(
            proxy=cdp_http_proxy,
            transport=httpx.HTTPTransport(local_address="0.0.0.0"),
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
