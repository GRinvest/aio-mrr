"""Base sub-client для aio-mrr библиотеки.

Этот модуль предоставляет базовый класс для всех sub-clients с dependency injection
HTTPClient. Sub-clients наследуются от BaseSubClient и получают HTTP-клиент через
конструктор, делегируя ему управление сессией, retry, таймаутами и аутентификацией.

Автор: GRinvest / SibNeuroTech
Лицензия: MIT
"""

from __future__ import annotations

from aio_mrr.http.http_client import HTTPClient


class BaseSubClient:
    """Базовый класс для всех sub-clients.

    Этот класс обеспечивает общую структуру для всех sub-clients библиотеки,
    получая HTTPClient через dependency injection. Все подклассы должны
    использовать self._http для выполнения HTTP-запросов.
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует базовый sub-client.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        self._http: HTTPClient = http_client
