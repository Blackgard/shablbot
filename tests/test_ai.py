import unittest
from unittest.mock import MagicMock, patch

from shablbot.core.ai import AIChatService, AIProviderError
from shablbot.core.ai.providers import AIProviderName, OpenAICompatibleProvider
from shablbot.settings.settings_model import AIProviderConfig, AISettings


class OpenAICompatibleProviderTests(unittest.TestCase):
    def test_complete_returns_message_content(self):
        provider = OpenAICompatibleProvider(
            name=AIProviderName.OPENROUTER,
            config=AIProviderConfig(
                enabled=True,
                api_key="test-key",
                base_url="https://openrouter.ai/api/v1",
                default_model="openai/gpt-4o-mini",
            ),
            timeout=10,
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Привет!"}}]
        }

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response):
            answer = provider.complete(
                [{"role": "user", "content": "Привет"}],
            )

        self.assertEqual(answer, "Привет!")

    def test_complete_raises_on_http_error(self):
        provider = OpenAICompatibleProvider(
            name=AIProviderName.POLZA,
            config=AIProviderConfig(
                enabled=True,
                api_key="test-key",
                base_url="https://polza.ai/api/v1",
            ),
            timeout=10,
        )

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response):
            with self.assertRaises(AIProviderError):
                provider.complete([{"role": "user", "content": "test"}])


class AIChatServiceTests(unittest.TestCase):
    def _build_settings(self) -> AISettings:
        return AISettings(
            enabled=True,
            default_provider="openrouter",
            openrouter=AIProviderConfig(
                enabled=True,
                api_key="or-key",
                base_url="https://openrouter.ai/api/v1",
            ),
            polza=AIProviderConfig(
                enabled=True,
                api_key="polza-key",
                base_url="https://polza.ai/api/v1",
            ),
        )

    def test_ask_openrouter(self):
        service = AIChatService(self._build_settings())
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Ответ нейросети"}}]
        }

        with patch("shablbot.core.ai.providers.requests.post", return_value=mock_response):
            answer = service.ask("openrouter", user_id=1, prompt="Привет")

        self.assertEqual(answer, "Ответ нейросети")

    def test_ask_disabled_raises(self):
        settings = self._build_settings()
        settings.enabled = False
        service = AIChatService(settings)

        with self.assertRaises(AIProviderError):
            service.ask("openrouter", user_id=1, prompt="Привет")


if __name__ == "__main__":
    unittest.main()
