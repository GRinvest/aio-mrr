"""Manages the lifecycle of aiohttp.ClientSession.

Provides lazy initialization and proper management of
connection pooling via TCPConnector.

Attributes:
    limit: Maximum number of parallel connections (default: 200).
    limit_per_host: Maximum connections per host (default: 50).
    keepalive_timeout: Time to keep idle connections alive in seconds (default: 30).
"""

from __future__ import annotations
from aiohttp import ClientSession, TCPConnector


class AioHTTPSession:
    """Manages the lifecycle of aiohttp.ClientSession.

    Provides lazy initialization and proper management of
    connection pooling via TCPConnector.

    Attributes:
        limit: Maximum number of parallel connections (default: 200).
        limit_per_host: Maximum connections per host (default: 50).
        keepalive_timeout: Time to keep idle connections alive in seconds (default: 30).
    """

    def __init__(
        self,
        limit: int = 200,
        limit_per_host: int = 50,
        keepalive_timeout: int = 30,
    ) -> None:
        """Initializes AioHTTPSession.

        Args:
            limit: Maximum number of parallel connections.
            limit_per_host: Maximum connections per host.
            keepalive_timeout: Time to keep idle connections alive in seconds.
        """
        self._limit = limit
        self._limit_per_host = limit_per_host
        self._keepalive_timeout = keepalive_timeout
        self._session: ClientSession | None = None

    def _create_connector(self) -> TCPConnector:
        """Creates a TCPConnector with configured connection pooling.

        Returns:
            TCPConnector: Configured connector for aiohttp.ClientSession.
        """
        return TCPConnector(
            limit=self._limit,
            limit_per_host=self._limit_per_host,
        )

    def get_session(self) -> ClientSession:
        """Lazy initialization of aiohttp.ClientSession.

        Creates a session on first call if not already created.
        Session is created with TCPConnector for connection pooling management.

        Returns:
            ClientSession: aiohttp.ClientSession instance.

        Raises:
            RuntimeError: If the session cannot be created.
        """
        if self._session is None:
            connector = self._create_connector()
            self._session = ClientSession(connector=connector)
        return self._session

    async def __aenter__(self) -> ClientSession:
        """Async context manager entry.

        Initializes the session upon entering the context.

        Returns:
            ClientSession: aiohttp.ClientSession instance.
        """
        return self.get_session()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        """Async context manager exit — closes session.

        Closes the session when exiting the context.

        Args:
            exc_type: Exception type, if raised.
            exc_val: Exception instance, if raised.
            exc_tb: Traceback, if raised.
        """
        if self._session is not None:
            await self._session.close()
            self._session = None
