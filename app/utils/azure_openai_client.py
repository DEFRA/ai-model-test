from openai import AzureOpenAI

from app.config import config as settings

model_name = "gpt-4"
deployment = "gpt-4"

def chat_azureopenai(question):
    client = AzureOpenAI(
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY
    )

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
