from typing import Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict()
    port: int = 8085
    mongo_uri: str = "mongodb://127.0.0.1:27017/"
    mongo_database: str = "ai-model-test"
    mongo_truststore: str = "TRUSTSTORE_CDP_ROOT_CA"
    http_proxy: Optional[HttpUrl] = None
    enable_metrics: bool = False
    tracing_header: str = "x-cdp-request-id"

    OPENAI_API_KEY: Optional[str] = None

    AWS_ACCESS_KEY_ID_BEDROCK: Optional[str] = None
    AWS_SECRET_ACCESS_KEY_BEDROCK: Optional[str] = None
    AWS_REGION_BEDROCK: Optional[str] = None


config = AppConfig()
