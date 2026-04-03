"""HTTP session management for aio-mrr library."""

from __future__ import annotations
from aiohttp import ClientSession, TCPConnector


class AioHTTPSession:
    """Управление жизненным циклом aiohttp.ClientSession.

    Предоставляет lazy initialization и корректное управление
    connection pooling через TCPConnector.

    Attributes:
        limit: Максимальное количество параллельных соединений (дефолт: 200).
        limit_per_host: Максимальное соединений на один хост (дефолт: 50).
        keepalive_timeout: Время удерживания idle соединений в секундах (дефолт: 30).
    """

    def __init__(
        self,
        limit: int = 200,
        limit_per_host: int = 50,
        keepalive_timeout: int = 30,
    ) -> None:
        """Инициализация AioHTTPSession.

        Args:
            limit: Максимальное количество параллельных соединений.
            limit_per_host: Максимальное соединений на один хост.
            keepalive_timeout: Время удерживания idle соединений в секундах.
        """
        self._limit = limit
        self._limit_per_host = limit_per_host
        self._keepalive_timeout = keepalive_timeout
        self._session: ClientSession | None = None

    def _create_connector(self) -> TCPConnector:
        """Создаёт TCPConnector с настроенным connection pooling.

        Returns:
            TCPConnector: Конфигурированный connector для aiohttp.ClientSession.
        """
        return TCPConnector(
            limit=self._limit,
            limit_per_host=self._limit_per_host,
        )

    def get_session(self) -> ClientSession:
        """Lazy initialization of aiohttp.ClientSession.

        Создаёт session при первом вызове, если она ещё не была создана.
        Session создаётся с TCPConnector для управления connection pooling.

        Returns:
            ClientSession: Экземпляр aiohttp.ClientSession.

        Raises:
            RuntimeError: Если session не может быть создана.
        """
        if self._session is None:
            connector = self._create_connector()
            self._session = ClientSession(connector=connector)
        return self._session

    async def __aenter__(self) -> ClientSession:
        """Async context manager entry.

        Инициализирует session при входе в контекст.

        Returns:
            ClientSession: Экземпляр aiohttp.ClientSession.
        """
        return self.get_session()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        """Async context manager exit — closes session.

        Закрывает session при выходе из контекста.

        Args:
            exc_type: Тип исключения, если было выброшено.
            exc_val: Экземпляр исключения, если было выброшено.
            exc_tb: Traceback, если было выброшено.
        """
        if self._session is not None:
            await self._session.close()
            self._session = None
