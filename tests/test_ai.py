import os
import unittest
from unittest.mock import MagicMock, patch

from shablbot.core.ai import AIChatService, AIProviderError, build_ai_settings_from_env
from shablbot.core.ai.providers import OpenAICompatibleProvider
from shablbot.settings.settings_model import AISettings


class BuildAISettingsTests(unittest.TestCase):
    def test_openrouter_from_env(self):
        env = {
            "AI_ENABLED": "true",
            "AI_PROVIDER": "openrouter",
            "AI_MODEL": "anthropic/claude-3.5-sonnet",
            "OPENROUTER_API_KEY": "or-test-key",
        }
        with patch.dict(os.environ, env, clear=False):
            settings = build_ai_settings_from_env()

        self.assertTrue(settings.enabled)
        self.assertEqual(settings.provider, "openrouter")
        self.assertEqual(settings.model, "anthropic/claude-3.5-sonnet")
        self.assertEqual(settings.api_key, "or-test-key")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

    def test_polza_from_env(self):
        env = {
            "AI_ENABLED": "true",
            "AI_PROVIDER": "polza",
            "AI_MODEL": "openai/gpt-4o",
            "POLZA_API_KEY": "polza-test-key",
        }
        with patch.dict(os.environ, env, clear=False):
            settings = build_ai_settings_from_env()

        self.assertEqual(settings.provider, "polza")
        self.assertEqual(settings.model, "openai/gpt-4o")
        self.assertEqual(settings.api_key, "polza-test-key")
        self.assertEqual(settings.base_url, "https://polza.ai/api/v1")


class OpenAICompatibleProviderTests(unittest.TestCase):
    def _settings(self) -> AISettings:
        return AISettings(
            enabled=True,
            provider="openrouter",
            model="openai/gpt-4o-mini",
            api_key="test-key",
            base_url="https://openrouter.ai/api/v1",
        )

    def test_complete_returns_message_content(self):
        provider = OpenAICompatibleProvider(self._settings())

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Привет!"}}]
        }

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response):
            answer = provider.complete([{"role": "user", "content": "Привет"}])

        self.assertEqual(answer, "Привет!")

    def test_complete_raises_on_http_error(self):
        provider = OpenAICompatibleProvider(self._settings())

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response):
            with self.assertRaises(AIProviderError):
                provider.complete([{"role": "user", "content": "test"}])


class AIChatServiceTests(unittest.TestCase):
    def test_ask_uses_configured_provider_and_model(self):
        settings = AISettings(
            enabled=True,
            provider="openrouter",
            model="openai/gpt-4o-mini",
            api_key="or-key",
            base_url="https://openrouter.ai/api/v1",
        )
        service = AIChatService(settings)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Ответ нейросети"}}]
        }

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response) as post:
            answer = service.ask(user_id=1, prompt="Привет")

        self.assertEqual(answer, "Ответ нейросети")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "openai/gpt-4o-mini")

    def test_ask_disabled_raises(self):
        settings = AISettings(
            enabled=False,
            api_key="key",
            base_url="https://openrouter.ai/api/v1",
        )
        service = AIChatService(settings)

        with self.assertRaises(AIProviderError):
            service.ask(user_id=1, prompt="Привет")


if __name__ == "__main__":
    unittest.main()
