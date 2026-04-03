"""Тесты для AuthSigner."""

from __future__ import annotations
import hashlib
import hmac
from unittest.mock import AsyncMock, patch
import pytest

from aio_mrr.auth.signer import AuthSigner


class TestAuthSigner:
    """Тесты для класса AuthSigner."""

    @pytest.mark.asyncio
    async def test_init(self, api_key: str, api_secret: str) -> None:
        """Тестирует инициализацию AuthSigner."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        assert signer._api_key == api_key
        assert signer._api_secret == api_secret
        assert signer._nonce_generator is not None

    @pytest.mark.asyncio
    async def test_get_auth_headers_structure(self, api_key: str, api_secret: str, sample_endpoint: str) -> None:
        """Тестирует структуру возвращаемых заголовков."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "1234567890"

            headers = await signer.get_auth_headers(sample_endpoint)

        assert isinstance(headers, dict)
        assert "x-api-key" in headers
        assert "x-api-nonce" in headers
        assert "x-api-sign" in headers

    @pytest.mark.asyncio
    async def test_get_auth_headers_values(self, api_key: str, api_secret: str, sample_endpoint: str) -> None:
        """Тестирует значения в заголовках аутентификации."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        test_nonce = "1234567890"
        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = test_nonce

            headers = await signer.get_auth_headers(sample_endpoint)

        assert headers["x-api-key"] == api_key
        assert headers["x-api-nonce"] == test_nonce
        assert "x-api-sign" in headers
        assert len(headers["x-api-sign"]) == 40  # SHA1 hex digest

    @pytest.mark.asyncio
    async def test_signature_calculation(self, api_key: str, api_secret: str, sample_endpoint: str) -> None:
        """Тестирует правильность вычисления HMAC подписи."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        test_nonce = "1234567890"
        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = test_nonce

            headers = await signer.get_auth_headers(sample_endpoint)

        # Проверяем, что подпись соответствует ожидаемой
        expected_sign_string = f"{api_key}{test_nonce}{sample_endpoint}"
        expected_signature = hmac.new(
            api_secret.encode(),
            expected_sign_string.encode(),
            hashlib.sha1,
        ).hexdigest()

        assert headers["x-api-sign"] == expected_signature

    @pytest.mark.asyncio
    async def test_signature_with_query_string(
        self, api_key: str, api_secret: str, sample_endpoint_with_query: str
    ) -> None:
        """Тестирует подпись с query string в эндпоинте."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        test_nonce = "9876543210"
        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = test_nonce

            headers = await signer.get_auth_headers(sample_endpoint_with_query)

        # Проверяем, что query string включён в подпись
        expected_sign_string = f"{api_key}{test_nonce}{sample_endpoint_with_query}"
        expected_signature = hmac.new(
            api_secret.encode(),
            expected_sign_string.encode(),
            hashlib.sha1,
        ).hexdigest()

        assert headers["x-api-sign"] == expected_signature

    @pytest.mark.asyncio
    async def test_nonce_uniqueness(self, api_key: str, api_secret: str) -> None:
        """Тестирует, что каждый вызов генерирует уникальный nonce."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        nonces = []
        for _ in range(10):
            headers = await signer.get_auth_headers("/test")
            nonces.append(headers["x-api-nonce"])

        # All nonces must be unique
        assert len(nonces) == len(set(nonces))

    @pytest.mark.asyncio
    async def test_nonce_monotonicity(self, api_key: str, api_secret: str) -> None:
        """Тестирует монотонность nonce."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        previous_nonce = 0
        for _ in range(10):
            headers = await signer.get_auth_headers("/test")
            current_nonce = int(headers["x-api-nonce"])

            assert current_nonce > previous_nonce
            previous_nonce = current_nonce

    @pytest.mark.asyncio
    async def test_endpoint_variations(self, api_key: str, api_secret: str) -> None:
        """Тестирует различные форматы эндпоинтов."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        endpoints = [
            "/account",
            "/account/balance",
            "/rig?status=enabled",
            "/info/algos?currency=BTC",
            "/account/profile/123",
        ]

        for endpoint in endpoints:
            # Mock nonce для предсказуемости
            test_nonce = "1111111111"
            with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
                mock_generate.return_value = test_nonce

                headers = await signer.get_auth_headers(endpoint)

            assert "x-api-key" in headers
            assert "x-api-nonce" in headers
            assert "x-api-sign" in headers
            assert len(headers["x-api-sign"]) == 40

    @pytest.mark.asyncio
    async def test_signature_is_hex(self, api_key: str, api_secret: str) -> None:
        """Тестирует, что подпись является валидной hex строкой."""
        signer = AuthSigner(api_key=api_key, api_secret=api_secret)

        headers = await signer.get_auth_headers("/test")
        signature = headers["x-api-sign"]

        # Проверяем, что подпись - валидная hex строка
        try:
            int(signature, 16)
        except ValueError:
            pytest.fail("Signature is not a valid hex string")

    @pytest.mark.asyncio
    async def test_empty_api_key(self) -> None:
        """Тестирует работу с пустым API ключом."""
        signer = AuthSigner(api_key="", api_secret="secret")

        test_nonce = "123456"
        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = test_nonce

            headers = await signer.get_auth_headers("/test")

        assert headers["x-api-key"] == ""
        assert headers["x-api-nonce"] == test_nonce
        assert len(headers["x-api-sign"]) == 40

    @pytest.mark.asyncio
    async def test_special_characters_in_secret(self) -> None:
        """Тестирует работу с особыми символами в секрете."""
        special_secret = "secret!@#$%^&*()_+-=[]{}|;':\",./<>?"
        signer = AuthSigner(api_key="key", api_secret=special_secret)

        test_nonce = "123456"
        with patch.object(signer._nonce_generator, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = test_nonce

            headers = await signer.get_auth_headers("/test")

        assert len(headers["x-api-sign"]) == 40
        # Проверяем, что подпись вычисляется корректно
        expected_sign_string = f"key{test_nonce}/test"
        expected_signature = hmac.new(
            special_secret.encode(),
            expected_sign_string.encode(),
            hashlib.sha1,
        ).hexdigest()

        assert headers["x-api-sign"] == expected_signature
