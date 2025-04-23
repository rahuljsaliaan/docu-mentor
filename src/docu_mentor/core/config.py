from typing import Optional, Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from docu_mentor.types.enums import EnvironmentEnum, OpenAIModelEnum
from docu_mentor.types.types import EmbeddingSettingsDict


class APIKeySettings(BaseSettings):
    """Holds API keys for external services."""

    openai_api_key: str = Field(..., description="API key of Open AI.")
    pinecone_api_key: str = Field(..., description="API key of Pinecone DB.")
    langsmith_api_key: Optional[str] = Field(
        default=None, description="API key of Langsmith Tracing."
    )


class URLSettings(BaseSettings):
    """Contains URLs and file paths used in the project."""

    langchain_docs_path: str = Field(
        default="", description="Relative file path of the langchain documentation."
    )
    retrieval_qa_chat_prompt_url: str = Field(default="langchain-ai/retrieval-qa-chat")


class ProjectConfig(BaseSettings):
    """Project-specific environment and configuration values."""

    environment: EnvironmentEnum = Field(
        default=EnvironmentEnum.production,
        description="Project's operational environment.",
    )
    port: int = Field(
        default=8000, description="Port number on which the project will run."
    )
    langchain_project: str = Field(
        default="DocuMentor", description="Name of the project."
    )
    langsmith_url: Optional[str] = Field(
        default=None, description="URL of Langsmith Tracing."
    )
    langchain_tracing_v2: bool = Field(
        default=False, description="Flag to enable or global tracing."
    )
    index_name: str = Field(
        default="langchain-doc-index",
        description="Name of the index to store the document embeddings.",
    )


class EmbeddingSettings(BaseSettings):
    """Configuration for document chunking and batch processing by model."""

    settings_config: EmbeddingSettingsDict = Field(
        default={
            [OpenAIModelEnum.TEXT_EMBEDDING_3_SMALL.value]: {
                "chunk_size": 500,
                "chunk_overlap": 50,
                "batch_size": 1000,
            },
            [OpenAIModelEnum.TEXT_EMBEDDING_ADA_002.value]: {
                "chunk_size": 800,
                "chunk_overlap": 100,
                "batch_size": 500,
            },
        },
        description="Model-specific chunking and batching configurations.",
    )

    def config(self, model_name: OpenAIModelEnum) -> EmbeddingSettingsDict:
        """Return chunking/batching config for a given model."""
        return self.settings_config[model_name]


class Settings(BaseSettings):
    """Root settings object combining all configuration sections."""

    # Settings Configurations
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    api = APIKeySettings()
    url = URLSettings()
    config = ProjectConfig()
    embedding = EmbeddingSettings()


settings = Settings()
