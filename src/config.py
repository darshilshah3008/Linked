"""Configuration module for Job Search Copilot."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(
        default="sqlite:///data/app.db",
        description="SQLAlchemy database URL",
    )

    # LLM
    llm_provider: str = Field(default="mock", description="LLM provider: mock | openai")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model name")

    # Lead search
    lead_keywords: str = Field(
        default="embedded software engineer,firmware engineer,embedded systems,RTOS,CAN,J1939,industrial automation",
        description="Comma-separated lead keywords",
    )

    # Location
    preferred_locations: str = Field(
        default="Manitowoc,Wisconsin,Remote,USA",
        description="Comma-separated preferred locations",
    )

    # Content
    posts_per_week: int = Field(default=3, description="Target posts per week")
    content_tone: str = Field(default="practical", description="Content tone")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="data/copilot.log", description="Log file path")

    @property
    def lead_keywords_list(self) -> list[str]:
        return [k.strip() for k in self.lead_keywords.split(",") if k.strip()]

    @property
    def preferred_locations_list(self) -> list[str]:
        return [loc.strip() for loc in self.preferred_locations.split(",") if loc.strip()]

    model_config = {"env_prefix": "", "case_sensitive": False}


# Singleton
_settings: Settings | None = None


def get_settings() -> Settings:
    """Return cached settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
