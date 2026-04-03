"""HTTP Client для aio-mrr библиотеки.

Этот модуль предоставляет центральный HTTP-клиент с функциональностью:
- Retry логика через tenacity (для 5xx, 429, connection errors)
- Timeout конфигурация (connect и read)
- Аутентификация через AuthSigner
- Логирование через loguru
- НИКОГДА не бросает исключений наружу — все ошибки возвращаются как MRRResponse(success=False)

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
"""

from __future__ import annotations
import asyncio
import json
import logging
from typing import Any
import aiohttp
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

from aio_mrr.auth.signer import AuthSigner
from aio_mrr.http.response import parse_response
from aio_mrr.http.session import AioHTTPSession
from aio_mrr.logging.config import get_logger
from aio_mrr.models.base import MRRResponse, MRRResponseError

# Retry-логгер (секреты автоматически маскируются через SecretMasker)
_retry_logger = get_logger("http_client_retry")


def _is_retryable_result(response: aiohttp.ClientResponse) -> bool:
    """Определяет, нужно ли ретраить по HTTP статусу.

    Args:
        response: aiohttp ClientResponse объект.

    Returns:
        True если статус требует retry (429, 500, 502, 503, 504).
    """
    return response.status in {429, 500, 502, 503, 504}


def _get_retry_params(status: int | None) -> dict[str, Any]:
    """Возвращает параметры retry в зависимости от статуса.

    Args:
        status: HTTP статус код или None для connection errors.

    Returns:
        Словарь с параметрами stop и wait для tenacity.
    """
    if status == 429:
        return {
            "stop": stop_after_attempt(5),
            "wait": wait_exponential(multiplier=5, min=5, max=60) + wait_random(0, 5),
        }
    return {
        "stop": stop_after_attempt(3),
        "wait": wait_exponential(multiplier=1, min=1, max=8) + wait_random(0, 1),
    }


def _log_retry_attempt(retry_state: Any) -> None:
    """Логгирует попытку retry.

    Args:
        retry_state: Состояние retry от tenacity.
    """
    _retry_logger.debug(f"Retry attempt: {retry_state.attempt_number} (will retry {retry_state.upcoming_sleep:.2f}s)")


class HTTPClient:
    """Центральный HTTP-клиент с retry, timeout, auth, логированием.

    Этот класс предоставляет низкоуровневый HTTP-клиент для взаимодействия
    с MiningRigRentals API v2. Все сетевые ошибки, таймауты и HTTP ошибки
    обрабатываются внутри — метод request() НИКОГДА не бросает исключений.

    Retry стратегия:
    - 500, 502, 503, 504: 3 попытки, exponential backoff 1-8с + jitter
    - 429 (Rate Limit): 5 попыток, exponential backoff 5-60с + jitter
    - Connection errors: 3 попытки, exponential backoff 1-8с + jitter

    Attributes:
        api_key: API ключ MRR (хранится только в памяти).
        api_secret: API секрет MRR (хранится только в памяти).
        connect_timeout: Таймаут подключения в секундах (дефолт: 30.0).
        read_timeout: Таймаут чтения в секундах (дефолт: 60.0).
        max_retries: Максимальное количество попыток retry (дефолт: 3).
    """

    BASE_URL: str = "https://www.miningrigrentals.com/api/v2"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        connect_timeout: float = 30.0,
        read_timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Инициализирует HTTPClient.

        Args:
            api_key: API ключ MRR.
            api_secret: API секрет MRR.
            connect_timeout: Таймаут подключения в секундах.
            read_timeout: Таймаут чтения в секундах.
            max_retries: Максимальное количество попыток retry.
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._max_retries = max_retries

        self._session_manager = AioHTTPSession()
        self._auth_signer = AuthSigner(api_key=api_key, api_secret=api_secret)
        self._logger = get_logger("http_client")

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> MRRResponse[Any]:
        """Выполняет HTTP запрос с retry, timeout, auth.

        Метод выполняет HTTP запрос к MRR API с автоматическим retry,
        timeout, аутентификацией и логированием. НИКОГДА не бросает
        исключений наружу — все ошибки возвращаются как MRRResponse(success=False).

        Args:
            method: HTTP метод (GET, PUT, POST, DELETE).
            endpoint: API endpoint (без базового URL, например "/account/balance").
            params: Query параметры (опционально).
            body: Тело запроса для JSON (опционально).

        Returns:
            MRRResponse[Any] — универсальный ответ:
            - При успехе: MRRResponse(success=True, data=...)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> client = HTTPClient(api_key="key", api_secret="secret")
            >>> response = await client.request("GET", "/account/balance")
            >>> if response.success:
            ...     print(response.data)
            ... else:
            ...     print(f"Error: {response.error.message}")
        """
        full_url = f"{self.BASE_URL}{endpoint}"

        self._logger.debug(f"{method} {full_url}")

        # Таймауты
        timeout = aiohttp.ClientTimeout(
            total=self._read_timeout,
            connect=self._connect_timeout,
        )

        # Retry конфигурация - определяем ПЕРЕД созданием стратегии retry
        retry_params = _get_retry_params(None)  # По умолчанию для connection errors

        # Создаём retry стратегию динамически
        retry_decorator = retry(
            stop=retry_params["stop"],
            wait=retry_params["wait"],
            retry=(
                retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError, OSError))
                | retry_if_result(_is_retryable_result)
            ),
            before_sleep=before_sleep_log(_retry_logger, logging.DEBUG),
            reraise=True,
        )

        try:
            session = self._session_manager.get_session()

            # Оборачиваем _do_request в retry декоратор
            @retry_decorator
            async def _do_request_with_retry() -> aiohttp.ClientResponse:
                return await self._do_request(
                    method=method,
                    url=full_url,
                    endpoint=endpoint,
                    params=params,
                    body=body,
                    timeout=timeout,
                    session=session,
                )

            # Выполняем запрос c retry
            response = await _do_request_with_retry()

            # Всегда возвращаем MRRResponse
            return await self._handle_response(response)

        except Exception as e:
            # Фолбэк на случай непредвиденных ошибок (никогда не должно происходить)
            self._logger.error(f"Unexpected error in request: {e}")
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="network_error",
                    message=f"Unexpected error: {e!s}",
                    details={"method": method, "endpoint": endpoint, "error": str(e)},
                ),
            )

    def _convert_params(self, params: dict[str, Any] | None) -> dict[str, Any] | None:
        """Конвертирует булевы значения в строки для aiohttp.

        Args:
            params: Словарь с параметрами запроса.

        Returns:
            Словарь с булевыми значениями, конвертированными в строки 'true'/'false'.
        """
        if params is None:
            return None

        converted: dict[str, Any] = {}
        for key, value in params.items():
            if isinstance(value, bool):
                converted[key] = str(value).lower()
            else:
                converted[key] = value
        return converted

    async def _do_request(
        self,
        method: str,
        url: str,
        endpoint: str,
        params: dict[str, Any] | None,
        body: dict[str, Any] | None,
        timeout: aiohttp.ClientTimeout,
        session: aiohttp.ClientSession,
    ) -> aiohttp.ClientResponse:
        """Выполняет один HTTP запрос.

        Args:
            method: HTTP метод.
            url: Полный URL запроса.
            params: Query параметры.
            body: Тело запроса.
            timeout: Таймауты запроса.
            session: aiohttp ClientSession.

        Returns:
            aiohttp.ClientResponse — для проверки статуса и retry логики.
        """
        # Генерируем заголовки аутентификации (подписываем только endpoint без base URL)
        auth_headers = await self._auth_signer.get_auth_headers(endpoint=endpoint)

        # Объединяем заголовки
        headers = {
            "Content-Type": "application/json",
            **auth_headers,
        }

        # Конвертируем булевы значения в строки для aiohttp
        converted_params = self._convert_params(params)

        # Выполняем запрос
        response = await session.request(
            method=method,
            url=url,
            params=converted_params,
            json=body,
            headers=headers,
            timeout=timeout,
        )

        # Логируем ответ (секреты автоматически маскируются)
        self._logger.debug(f"{method} {url} -> {response.status}")

        return response

    async def _handle_response(self, response: aiohttp.ClientResponse) -> MRRResponse[Any]:
        """Обрабатывает HTTP ответ и возвращает MRRResponse.

        Args:
            response: aiohttp ClientResponse.

        Returns:
            MRRResponse[Any] — универсальный ответ API.
        """
        # Читаем тело ответа
        response_text = await response.text()

        # Если статус не 2xx, возвращаем ошибку
        if response.status >= 400:
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="http_error",
                    message=f"HTTP {response.status}",
                    details={"status": response.status},
                    http_status=response.status,
                ),
            )

        # Пытаемся распарсить JSON
        try:
            json_data = json.loads(response_text)
            return parse_response(
                json_data=json_data,
                http_status=response.status,
            )
        except json.JSONDecodeError:
            return MRRResponse(
                success=False,
                data=None,
                error=MRRResponseError(
                    code="validation_error",
                    message="Invalid JSON response",
                    details={"status": response.status, "response": response_text[:200]},
                    http_status=response.status,
                ),
            )

    async def close(self) -> None:
        """Закрывает HTTP session.

        Должен вызываться при завершении работы клиента.
        """
        await self._session_manager.__aexit__(None, None, None)

    async def __aenter__(self) -> HTTPClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        """Async context manager exit."""
        await self.close()
