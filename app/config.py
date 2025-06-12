from typing import Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    python_env: str = "development"
    model_config = SettingsConfigDict()
    host: str = "0.0.0.0"
    port: int = 8085
    mongo_uri: str = "mongodb://127.0.0.1:27017/"
    mongo_database: str = "ai-model-test"
    mongo_truststore: str = "TRUSTSTORE_CDP_ROOT_CA"
    rds_truststore: str = "TRUSTSTORE_RDS_ROOT_CA"
    http_proxy: Optional[HttpUrl] = None
    enable_metrics: bool = False
    tracing_header: str = "x-cdp-request-id"
    log_config: str = "logging.json"

    aws_region: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    S3_ENDPOINT: Optional[str] = None

    OPENAI_API_KEY: Optional[str] = None

    # Bedrock
    AWS_ACCESS_KEY_ID_BEDROCK: Optional[str] = None
    AWS_SECRET_ACCESS_KEY_BEDROCK: Optional[str] = None
    AWS_REGION_BEDROCK: Optional[str] = None
    AWS_BEDROCK_MODEL: Optional[str] = None
    AWS_USE_CREDENTIALS_BEDROCK: Optional[str] = None

    # Anthropic
    ANTHROPIC_MAX_TOKENS: Optional[int] = None
    ANTHROPIC_TEMPERATURE: Optional[float] = None

    # AZURE
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_API_VERSION: Optional[str] = None

    CDP_HTTPS_PROXY: Optional[str] = None
    CDP_HTTP_PROXY: Optional[str] = None
    HTTPS_PROXY: Optional[str] = None

    postgres_host: str
    postgres_port: int = 5432
    postgres_user: Optional[str] = "ai_model_test"
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = "ai_model_test"


config = AppConfig()
