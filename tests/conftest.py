"""Pytest fixtures и конфигурация для тестов aio-mrr."""

from __future__ import annotations
import pytest


@pytest.fixture
def api_key() -> str:
    """Фикстура для тестового API ключа."""
    return "test_api_key_12345"


@pytest.fixture
def api_secret() -> str:
    """Фикстура для тестового API секрета."""
    return "test_api_secret_67890"


@pytest.fixture
def auth_signer(api_key: str, api_secret: str) -> object:
    """Фикстура для AuthSigner с тестовыми credentials.

    Возвращает кортеж (signer, api_key, api_secret) для тестирования.
    """
    from aio_mrr.auth.signer import AuthSigner

    signer = AuthSigner(api_key=api_key, api_secret=api_secret)
    return signer, api_key, api_secret


@pytest.fixture
def nonce_generator() -> object:
    """Фикстура для NonceGenerator."""
    from aio_mrr.auth.nonce import NonceGenerator

    return NonceGenerator()


@pytest.fixture
def sample_endpoint() -> str:
    """Фикстура для тестового эндпоинта."""
    return "/account/balance"


@pytest.fixture
def sample_endpoint_with_query() -> str:
    """Фикстура для тестового эндпоинта с query string."""
    return "/rig?status=enabled"
