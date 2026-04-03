"""Info Client для взаимодействия с Info API.

Этот модуль предоставляет InfoClient для работы с Info API endpoints:
- GET /info/servers
- GET /info/algos
- GET /info/algos/{name}
- GET /info/currencies
"""

from __future__ import annotations
from typing import Any

from aio_mrr.http.http_client import HTTPClient
from aio_mrr.models.base import MRRResponse
from aio_mrr.models.info.response import AlgoInfo, CurrencyInfo, ServerInfo, ServersList
from aio_mrr.subclients.base import BaseSubClient


class InfoClient(BaseSubClient):
    """Client для работы с Info API.

    Предоставляет методы для получения информации о системе:
    - список серверов
    - информацию об алгоритмах майнинга
    - список доступных валют

    Пример использования:
        >>> async with MRRClient(api_key="key", api_secret="secret") as client:
        ...     response = await client.info_client.get_servers()
        ...     if response.success:
        ...         print(response.data.servers)
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """Инициализирует InfoClient.

        Args:
            http_client: Экземпляр HTTPClient для выполнения запросов.
        """
        super().__init__(http_client)

    async def get_servers(self) -> MRRResponse[ServersList]:
        """Получает список серверов MRR.

        Возвращает информацию о всех доступных серверах MiningRigRentals,
        включая их идентификаторы, имена, регионы и порты.

        > ⚠️ Поля port и ethereum_port устарели. Используйте /rig/port
        для получения актуальной информации о портах.

        Returns:
            MRRResponse[ServersList] — ответ с списком серверов:
            - При успехе: MRRResponse(success=True, data=ServersList)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_servers()
            >>> if response.success:
            ...     for server in response.data.servers:
            ...         print(f"{server.name} - {server.region}")
        """
        endpoint = "/info/servers"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            servers_data: list[dict[str, Any]] = result.data
            servers_list = ServersList(servers=[ServerInfo.model_validate(s) for s in servers_data])
            return MRRResponse(
                success=True,
                data=servers_list,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_algos(self, currency: str | None = None) -> MRRResponse[list[AlgoInfo]]:
        """Получает список всех алгоритмов майнинга.

        Возвращает информацию обо всех доступных алгоритмах майнинга,
        включая рекомендуемые цены, статистику хешрейта и текущие цены.

        Args:
            currency: Валюта для цен (BTC, LTC, ETH, DOGE, BCH).
                     По умолчанию BTC.

        Returns:
            MRRResponse[list[AlgoInfo]] — ответ со списком алгоритмов:
            - При успехе: MRRResponse(success=True, data=[AlgoInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_algos(currency="BTC")
            >>> if response.success:
            ...     for algo in response.data:
            ...         print(f"{algo.display}: {algo.suggested_price.amount}")
        """
        endpoint = "/info/algos"
        params: dict[str, Any] = {}

        if currency is not None:
            params["currency"] = currency

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            algos_data: list[dict[str, Any]] = result.data
            algos = [AlgoInfo.model_validate(a) for a in algos_data]
            return MRRResponse(
                success=True,
                data=algos,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_algo(self, name: str, currency: str | None = None) -> MRRResponse[AlgoInfo]:
        """Получает информацию о конкретном алгоритме майнинга.

        Возвращает детальную информацию об одном алгоритме, включая
        рекомендуемые цены, статистику хешрейта и текущие рыночные цены.

        Args:
            name: Название алгоритма (например, "scrypt", "sha256", "x11").
            currency: Валюта для цен (BTC, LTC, ETH, DOGE, BCH).
                     По умолчанию BTC.

        Returns:
            MRRResponse[AlgoInfo] — ответ с информацией об алгоритме:
            - При успехе: MRRResponse(success=True, data=AlgoInfo)
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_algo(name="scrypt", currency="BTC")
            >>> if response.success:
            ...     algo = response.data
            ...     print(f"{algo.display}: {algo.stats.available.rigs} rigs available")
        """
        endpoint = f"/info/algos/{name}"
        params: dict[str, Any] = {}

        if currency is not None:
            params["currency"] = currency

        result = await self._http.request(method="GET", endpoint=endpoint, params=params)

        if result.success and result.data is not None:
            algo_data: dict[str, Any] = result.data
            algo = AlgoInfo.model_validate(algo_data)
            return MRRResponse(
                success=True,
                data=algo,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result

    async def get_currencies(self) -> MRRResponse[list[CurrencyInfo]]:
        """Получает список доступных валют для платежей.

        Возвращает информацию о всех валютах, которые можно использовать
        для оплаты аренды ригов. Каждая валюта имеет статус доступности
        и комиссию за вывод средств.

        > ℹ️ Комиссия txfee может меняться каждые 15 минут.

        Returns:
            MRRResponse[list[CurrencyInfo]] — ответ со списком валют:
            - При успехе: MRRResponse(success=True, data=[CurrencyInfo, ...])
            - При ошибке: MRRResponse(success=False, error=...)

        Example:
            >>> response = await info_client.get_currencies()
            >>> if response.success:
            ...     for curr in response.data:
            ...         print(f"{curr.name}: enabled={curr.enabled}, txfee={curr.txfee}")
        """
        endpoint = "/info/currencies"
        result = await self._http.request(method="GET", endpoint=endpoint)

        if result.success and result.data is not None:
            # Ответ имеет структуру {"currencies": [...]}
            currencies_data: dict[str, list[dict[str, Any]]] = result.data
            currencies_list = currencies_data.get("currencies", [])
            currencies = [CurrencyInfo.model_validate(c) for c in currencies_list]
            return MRRResponse(
                success=True,
                data=currencies,
                error=None,
                http_status=result.http_status,
                retry_count=result.retry_count,
            )

        return result
