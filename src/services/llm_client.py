"""LLM client abstraction.

Provides a swappable interface for LLM interactions.
- MockLLMClient: returns template-based responses (default)
- OpenAIClient: wraps the OpenAI-compatible API (optional)
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.config import get_settings


class LLMClient(ABC):
    """Abstract LLM client interface."""

    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt and return the completion text."""
        ...


class MockLLMClient(LLMClient):
    """Mock client that returns a placeholder response.

    Used for testing and development when no LLM API is configured.
    """

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return (
            "[Mock LLM Response] This is a placeholder. "
            "Connect an LLM provider for real generation. "
            f"User asked: {user_prompt[:200]}"
        )


class OpenAIClient(LLMClient):
    """OpenAI-compatible API client.

    Requires the 'openai' package and OPENAI_API_KEY env var.
    """

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI client")
        # Import here to keep openai optional
        import openai

        self._client = openai.OpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content or ""


def get_llm_client() -> LLMClient:
    """Return the configured LLM client based on settings."""
    settings = get_settings()
    if settings.llm_provider == "openai":
        return OpenAIClient()
    return MockLLMClient()
