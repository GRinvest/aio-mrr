"""Генератор HMAC SHA1 подписей для MRR API аутентификации.

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
"""

from __future__ import annotations
import hashlib
import hmac

from aio_mrr.auth.nonce import NonceGenerator


class AuthSigner:
    """Генератор HMAC SHA1 подписей для аутентификации в MRR API.

    MRR API использует HMAC SHA1 для аутентификации запросов. Этот класс
    генерирует необходимые заголовки для подписанных запросов:
    - x-api-key: API ключ пользователя
    - x-api-nonce: Уникальный nonce (number used once)
    - x-api-sign: HMAC SHA1 подпись

    Строка для подписи формируется как: {api_key}{nonce}{endpoint}
    где endpoint — полный path включая query string (без trailing slash).

    Пример:
        >>> signer = AuthSigner(api_key="test_key", api_secret="test_secret")
        >>> headers = await signer.get_auth_headers("/account/balance")
        >>> "x-api-key" in headers
        True
        >>> "x-api-nonce" in headers
        True
        >>> "x-api-sign" in headers
        True
    """

    def __init__(self, api_key: str, api_secret: str) -> None:
        """Инициализирует генератор подписей.

        Args:
            api_key: API ключ для аутентификации в MRR API.
            api_secret: API секрет для генерации HMAC подписей.
        """
        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._nonce_generator: NonceGenerator = NonceGenerator()

    async def get_auth_headers(self, endpoint: str) -> dict[str, str]:
        """Генерирует заголовки аутентификации для запроса к MRR API.

        Метод создаёт все необходимые заголовки для подписанного запроса:
        1. Генерирует уникальный nonce через NonceGenerator
        2. Формирует строку для подписи: {api_key}{nonce}{endpoint}
        3. Вычисляет HMAC SHA1 подпись от строки
        4. Возвращает dict c заголовками x-api-key, x-api-nonce, x-api-sign

        Args:
            endpoint: Полный путь эндпоинта включая query string.
                     Примеры:
                     - "/account/balance"
                     - "/rig?status=enabled"
                     - "/info/algos?currency=BTC"
                     Важно: endpoint не должен иметь trailing slash.

        Returns:
            dict[str, str]: Словарь c заголовками аутентификации:
                - "x-api-key": API ключ
                - "x-api-nonce": Сгенерированный nonce
                - "x-api-sign": HMAC SHA1 подпись (hex string)

        Example:
            >>> signer = AuthSigner("key", "secret")
            >>> headers = await signer.get_auth_headers("/account")
            >>> headers["x-api-key"]
            "key"
            >>> "x-api-sign" in headers
            True
        """
        nonce: str = await self._nonce_generator.generate()

        sign_string: str = f"{self._api_key}{nonce}{endpoint}"

        signature: str = hmac.new(
            self._api_secret.encode(),
            sign_string.encode(),
            hashlib.sha1,
        ).hexdigest()

        return {
            "x-api-key": self._api_key,
            "x-api-nonce": nonce,
            "x-api-sign": signature,
        }
