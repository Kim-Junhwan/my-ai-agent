from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: SecretStr = Field(..., description="OpenAI API 키")
    default_model: str = Field("gpt-5.2", description="기본모델")

    debug: bool = Field(False, description="디버그 모드")

    opensearch_host: str = Field("localhost", description="OpenSearch 호스트 주소")
    opensearch_port: int = Field(9200, description="OpenSearch 포트")

def get_settings() -> Settings:
    """설정 인스턴스르 반환합니다."""
    return Settings()