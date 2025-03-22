"""Singleton Anthropic client utility."""
from logging import getLogger
from typing import Optional

from anthropic import AsyncAnthropicBedrock

from app.config import config as settings

logger = getLogger(__name__)

USE_CREDENTIALS = settings.AWS_USE_CREDENTIALS_BEDROCK == "true"

class BedrockAnthropicClient:
    """AWS Bedrock Anthropic client implementation."""
    _instance: Optional[AsyncAnthropicBedrock] = None

    @classmethod
    def get_client(cls) -> AsyncAnthropicBedrock:
        if cls._instance is None:
            if USE_CREDENTIALS:
                cls._instance = AsyncAnthropicBedrock(
                    aws_access_key=settings.AWS_ACCESS_KEY_ID_BEDROCK,
                    aws_secret_key=settings.AWS_SECRET_ACCESS_KEY_BEDROCK,
                    aws_region=settings.AWS_REGION_BEDROCK
                )
            else:
                cls._instance = AsyncAnthropicBedrock()
        return cls._instance

class AnthropicClient:
    """Main interface for Anthropic client operations."""
    _instance: Optional[AsyncAnthropicBedrock] = None

    @classmethod
    def get_client(cls) -> AsyncAnthropicBedrock:
        if cls._instance is None:
            cls._instance = BedrockAnthropicClient.get_client()
        return cls._instance

    @classmethod
    async def create_message(
        cls,
        prompt: str,
        system_prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Create a message using the Anthropic Bedrock client."""
        client = cls.get_client()
        model = settings.AWS_BEDROCK_MODEL

        try:
            response = await client.messages.create(
                model=model,
                max_tokens=max_tokens or settings.ANTHROPIC_MAX_TOKENS,
                system=system_prompt,
                temperature=temperature or settings.ANTHROPIC_TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text if response.content else ""
        except Exception as e:
            logger.error("Error creating message: %s", e)
            raise
