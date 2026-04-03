"""MRRClient — главный фасад библиотеки aio-mrr.

Этот модуль предоставляет MRRClient — единую точку входа для взаимодействия
с MiningRigRentals API v2. Client использует паттерн Facade для упрощения
доступа ко всем подсистемам API через единый интерфейс.

Автор: GRinvest / SibNeuroTech
Лицензия: MIT

Паттерн использования:
    async with MRRClient(
        api_key="YOUR_KEY",
        api_secret="YOUR_SECRET",
        connect_timeout=30.0,
        read_timeout=60.0,
        max_retries=3,
    ) as client:
        response = await client.account.get_balance()
        if response.success:
            print(response.data)
"""

from __future__ import annotations

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.subclients.account_client import AccountClient
from aio_mrr.subclients.info_client import InfoClient
from aio_mrr.subclients.pricing_client import PricingClient
from aio_mrr.subclients.rental_client import RentalClient
from aio_mrr.subclients.rig_client import RigClient
from aio_mrr.subclients.riggroup_client import RigGroupClient


class MRRClient:
    """Главный фасад для взаимодействия с MiningRigRentals API v2.

    Этот класс предоставляет единую точку входа для всех API операций.
    Он создаёт и управляет жизненным циклом всех sub-clients и HTTP-сессии.

    Attributes:
        info: Client для /info/* endpoints.
        account: Client для /account/* endpoints.
        rig: Client для /rig/* endpoints.
        riggroup: Client для /riggroup/* endpoints.
        rental: Client для /rental/* endpoints.
        pricing: Client для /pricing endpoint.

    Example:
        >>> async with MRRClient(
        ...     api_key="YOUR_KEY",
        ...     api_secret="YOUR_SECRET",
        ... ) as client:
        ...     response = await client.account.get_balance()
        ...     if response.success:
        ...         print(response.data)
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        connect_timeout: float = 30.0,
        read_timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Инициализирует MRRClient.

        Args:
            api_key: API ключ MRR.
            api_secret: API секрет MRR.
            connect_timeout: Таймаут подключения в секундах (дефолт: 30.0).
            read_timeout: Таймаут чтения в секундах (дефолт: 60.0).
            max_retries: Максимальное количество попыток retry (дефолт: 3).
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._max_retries = max_retries

        # HTTP-client with shared settings
        self._http_client = HTTPClient(
            api_key=api_key,
            api_secret=api_secret,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            max_retries=max_retries,
        )

        # Sub-clients with shared HTTP-client
        self.info: InfoClient = InfoClient(http_client=self._http_client)
        self.account: AccountClient = AccountClient(http_client=self._http_client)
        self.rig: RigClient = RigClient(http_client=self._http_client)
        self.riggroup: RigGroupClient = RigGroupClient(http_client=self._http_client)
        self.rental: RentalClient = RentalClient(http_client=self._http_client)
        self.pricing: PricingClient = PricingClient(http_client=self._http_client)

    async def __aenter__(self) -> MRRClient:
        """Async context manager entry.

        Returns:
            MRRClient: Сам клиент для использования в async with.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Async context manager exit.

        Закрывает HTTP-сессию при выходе из контекста.

        Args:
            exc_type: Тип исключения если произошло.
            exc_val: Значение исключения если произошло.
            exc_tb: Stack trace если произошло.
        """
        await self._http_client.close()

    async def whoami(self) -> MRRResponse[dict[str, str]]:
        """Получает информацию о текущем пользователе.

        Выполняет GET запрос к /whoami endpoint для получения
        информации о аутентифицированном пользователе.

        Returns:
            MRRResponse[dict] — ответ с информацией о пользователе:
            - success: True если запрос успешен
            - data: Словарь с полями userid и username
            - error: Информация об ошибке если success=False

        Example:
            >>> response = await client.whoami()
            >>> if response.success:
            ...     print(f"User: {response.data['username']}")
            ... else:
            ...     print(f"Error: {response.error.message}")
        """
        return await self._http_client.request(method="GET", endpoint="/whoami")
