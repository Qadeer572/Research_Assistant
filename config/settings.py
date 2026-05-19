from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Any
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace


class Settings(BaseSettings):
    huggingface_api_key: str = Field(..., env="HUGGINGFACE_API_KEY")
    hf_model_id: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.3",
        env="HF_MODEL_ID"
    )
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")
    news_api_key: str = Field("", env="NEWS_API_KEY")
    max_new_tokens: int = Field(default=1024, env="MAX_NEW_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    max_research_sources: int = Field(default=10, env="MAX_RESEARCH_SOURCES")
    research_output_dir: str = Field(
        default="outputs/research",
        env="RESEARCH_OUTPUT_DIR"
    )
    report_output_dir: str = Field(
        default="outputs/reports",
        env="REPORT_OUTPUT_DIR"
    )
    app_env: str = Field(default="development", env="APP_ENV")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")

    # Stored as a raw string so .env comma-separated values work without JSON
    # Use .cors_origins_list for the parsed List[str]
    cors_origins: str = Field(
        default="http://localhost:3000",
        env="CORS_ORIGINS"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Returns CORS_ORIGINS as a list, split on commas."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_llm() -> ChatHuggingFace:
    settings = get_settings()
    endpoint = HuggingFaceEndpoint(
        repo_id=settings.hf_model_id,
        huggingfacehub_api_token=settings.huggingface_api_key,
        max_new_tokens=settings.max_new_tokens,
        temperature=settings.temperature,
        task="text-generation"
    )
    return ChatHuggingFace(llm=endpoint)
