from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from docu_mentor.types.enums import EnvironmentEnum


class Settings(BaseSettings):
    # Settings Configurations
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # API secrets
    openai_api_key: str = Field(..., description="API key of Open AI.")
    pinecone_api_key: str = Field(..., description="API key of Pinecone DB.")
    langsmith_api_key: Optional[str] = Field(
        default=None, description="API key of Langsmith Tracing."
    )

    # Project Configurations
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


settings = Settings()
